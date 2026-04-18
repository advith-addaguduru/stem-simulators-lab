"""
STEM Lab — Interactive Science & Mathematics Simulators
=======================================================
Open-source educational platform organised into four themed
simulator packs: Foundation, Core STEM, Advanced, and
Cross-Disciplinary Enrichment.
Features: Authentication, Audit Trail, Admin Dashboard, Logging.
Licensed under the Apache License 2.0.

Run:  streamlit run app.py
"""

import streamlit as st
import importlib

from simulators.config import CATALOG, get_stats
from core.settings import APP_NAME, APP_VERSION, SUPPORT_EMAIL, ROLES
from core.logger import get_logger
from core import auth, audit, admin
from core.guardrails import (
    sanitize_text,
    check_signup_rate,
    validate_password_strength,
    safe_run_simulator,
    can_modify_user,
    sanitize_log,
)
from core.settings import (
    INPUT_MAX_USERNAME,
    INPUT_MAX_EMAIL,
    INPUT_MAX_DISPLAY_NAME,
    INPUT_MAX_PASSWORD,
    INPUT_MAX_SEARCH,
)

log = get_logger(__name__)

# ─── Page Configuration ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="STEM Lab · Interactive Simulators",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom Styling ──────────────────────────────────────────────────────────
_CSS = """<style>
.hero{background:linear-gradient(135deg,#1e3a5f 0%,#2563eb 100%);color:#fff;
      padding:2.5rem 2rem;border-radius:14px;margin-bottom:1.5rem}
.hero h1{margin:0;font-size:2.2rem;font-weight:700}
.hero p{margin:.4rem 0 0;opacity:.85}
.bc{font-size:.82rem;color:#6b7280;margin-bottom:.75rem}
.bc .sep{margin:0 6px}.bc .cur{color:#2563eb;font-weight:600}
.tcard{background:#fff;border:1px solid #e5e7eb;border-radius:12px;
       padding:1.25rem;margin-bottom:.75rem;
       transition:border-color .15s,box-shadow .15s}
.tcard:hover{border-color:#93c5fd;box-shadow:0 2px 8px rgba(37,99,235,.1)}
.tcard .ic{font-size:1.6rem}
.tcard h4{margin:.4rem 0 .25rem;font-size:.95rem}
.tcard p{margin:0;font-size:.8rem;color:#6b7280}
.foot{text-align:center;color:#9ca3af;font-size:.75rem;
      padding:2rem 0 .5rem;margin-top:3rem;border-top:1px solid #f1f5f9}
.sim-desc{background:#f8fafc;border-left:4px solid #2563eb;padding:1rem 1.25rem;
          border-radius:0 8px 8px 0;margin-bottom:1rem;font-size:.9rem;color:#334155}
.ref-list{display:flex;flex-wrap:wrap;gap:.5rem;margin-bottom:1.25rem}
.ref-list a{display:inline-block;background:#eff6ff;color:#2563eb;
            padding:4px 12px;border-radius:20px;font-size:.78rem;
            text-decoration:none;border:1px solid #dbeafe;
            transition:background .15s,border-color .15s}
.ref-list a:hover{background:#dbeafe;border-color:#93c5fd}
.auth-box{max-width:420px;margin:4rem auto;padding:2rem;
          background:#fff;border:1px solid #e5e7eb;border-radius:14px;
          box-shadow:0 4px 16px rgba(0,0,0,.06)}
.user-pill{display:inline-flex;align-items:center;gap:6px;background:#eff6ff;
           color:#1e3a5f;padding:4px 12px;border-radius:20px;font-size:.82rem;
           font-weight:500}
</style>"""
st.markdown(_CSS, unsafe_allow_html=True)


# ─── Session state defaults ──────────────────────────────────────────────────
for _k, _v in {"session_id": None, "user": None, "auth_tab": "Login"}.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v


# ─── Auth helpers ─────────────────────────────────────────────────────────────

def _restore_session():
    """Re-validate the stored session on each rerun."""
    if st.session_state.session_id:
        user = auth.get_current_user(st.session_state.session_id)
        if user is None:
            st.session_state.session_id = None
            st.session_state.user = None
        else:
            st.session_state.user = user


def _current_user() -> dict | None:
    return st.session_state.user


# ─── Dynamic Loader ──────────────────────────────────────────────────────────
def _run(module_path: str, func_name: str = "simulate"):
    mod = importlib.import_module(module_path)
    getattr(mod, func_name)()


# ═══════════════════════════════════════════════════════════════════════════════
#  AUTH PAGES — Login / Signup
# ═══════════════════════════════════════════════════════════════════════════════

def _page_auth():
    st.markdown(
        '<div class="hero">'
        "<h1>🔬 STEM Lab</h1>"
        "<p>Interactive Science &amp; Mathematics Simulators</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    tab_login, tab_signup = st.tabs(["🔑 Login", "📝 Sign Up"])

    with tab_login:
        with st.form("login_form"):
            identifier = st.text_input("Username or Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Log In", use_container_width=True)
        if submitted:
            if not identifier or not password:
                st.warning("Please fill in both fields.")
            else:
                identifier = sanitize_text(identifier, max_length=INPUT_MAX_EMAIL, strip_html=False)
                result = auth.login(identifier, password)
                if result["ok"]:
                    st.session_state.session_id = result["session_id"]
                    st.session_state.user = result["user"]
                    audit.log(
                        audit.LOGIN,
                        user_id=result["user"]["id"],
                        username=result["user"]["username"],
                    )
                    log.info("User logged in: %s", result["user"]["username"])
                    st.rerun()
                else:
                    audit.log(
                        audit.LOGIN_FAILED,
                        detail=f"identifier={identifier}",
                    )
                    st.error(result["error"])

    with tab_signup:
        with st.form("signup_form"):
            su_display = st.text_input("Display Name")
            su_user = st.text_input("Username")
            su_email = st.text_input("Email")
            su_pass = st.text_input("Password", type="password", key="su_pass")
            su_pass2 = st.text_input("Confirm Password", type="password", key="su_pass2")
            agreed = st.checkbox("I agree to the [Terms of Service](#) and [Privacy Policy](#)")
            su_submit = st.form_submit_button("Create Account", use_container_width=True)
        if su_submit:
            if not agreed:
                st.warning("You must agree to the Terms of Service and Privacy Policy.")
            elif su_pass != su_pass2:
                st.warning("Passwords do not match.")
            elif not su_user or not su_email or not su_pass:
                st.warning("Please fill in all required fields.")
            elif not check_signup_rate():
                st.error("Too many signup attempts. Please wait a minute and try again.")
            else:
                su_display = sanitize_text(su_display, max_length=INPUT_MAX_DISPLAY_NAME)
                result = auth.signup(su_user, su_email, su_pass, su_display)
                if result["ok"]:
                    audit.log(
                        audit.SIGNUP,
                        user_id=result["user_id"],
                        username=su_user,
                    )
                    log.info("New user signed up: %s", su_user)
                    st.success("Account created! You can now log in.")
                else:
                    for err in result["errors"]:
                        st.error(err)


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN APP — Authenticated content
# ═══════════════════════════════════════════════════════════════════════════════

def _main_app():
    user = _current_user()

    # ── Sidebar ───────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("## 🔬 STEM Lab")
        st.markdown(
            f'<span class="user-pill">👤 {user["display_name"]} '
            f'<span style="opacity:.6">({user["role"]})</span></span>',
            unsafe_allow_html=True,
        )
        st.markdown("---")

        nav_items = ["🏠 Home", "🧪 Simulators", "📖 User Guide", "👤 Profile", "ℹ️ About"]
        if auth.is_admin(user):
            nav_items.insert(-1, "🛡️ Admin")
        nav_items.extend(["📜 Terms", "🔒 Privacy"])

        page = st.radio("Navigate", nav_items, label_visibility="collapsed")

        _topic = None
        _pack = _subj = None

        if page == "🧪 Simulators":
            st.markdown("---")
            st.markdown("#### 🎯 Choose a Simulator")

            _pack = st.selectbox("Simulator Pack", list(CATALOG.keys()))
            _pdata = CATALOG[_pack]

            _subjs = list(_pdata["subjects"])
            _subj = st.radio("Subject", _subjs, horizontal=True)

            _topics = _pdata["subjects"][_subj]
            if _topics:
                _labels = [f'{t["icon"]}  {t["name"]}' for t in _topics]
                _idx = st.selectbox(
                    "Topic", range(len(_topics)), format_func=lambda i: _labels[i]
                )
                _topic = _topics[_idx]

        st.markdown("---")
        _s = get_stats()
        st.caption(f"📊 {_s['simulators']} simulators · {_s['packs']} packs · {_s['subjects']} subjects")

        st.markdown("---")
        if st.button("🚪 Log Out", use_container_width=True):
            audit.log(audit.LOGOUT, user_id=user["id"], username=user["username"])
            auth.logout(st.session_state.session_id)
            st.session_state.session_id = None
            st.session_state.user = None
            log.info("User logged out: %s", user["username"])
            st.rerun()

    # ── Router ────────────────────────────────────────────────────────────────
    if page == "🏠 Home":
        _page_home()
    elif page == "🧪 Simulators":
        _page_sim(_topic, _pack, _subj, user)
    elif page == "📖 User Guide":
        _page_guide()
    elif page == "👤 Profile":
        _page_profile(user)
    elif page == "🛡️ Admin" and auth.is_admin(user):
        _page_admin(user)
    elif page == "📜 Terms":
        _page_terms()
    elif page == "🔒 Privacy":
        _page_privacy()
    elif page == "ℹ️ About":
        _page_about()


# ─── Page: Home ──────────────────────────────────────────────────────────────
def _page_home():
    st.markdown(
        '<div class="hero">'
        "<h1>🔬 STEM Lab</h1>"
        "<p>Interactive Science &amp; Mathematics Simulators</p>"
        '<p style="opacity:.65;font-size:.85rem">Foundation · Core STEM · Advanced · Cross-Disciplinary</p>'
        "</div>",
        unsafe_allow_html=True,
    )

    s = get_stats()
    c1, c2, c3 = st.columns(3)
    c1.metric("🧪 Simulators", s["simulators"])
    c2.metric("📦 Packs", s["packs"])
    c3.metric("📝 Subjects", s["subjects"])

    st.markdown("### 📦 Simulator Packs")
    cols = st.columns(2)
    for i, (pk, pd) in enumerate(CATALOG.items()):
        with cols[i % 2]:
            n = sum(len(t) for t in pd["subjects"].values())
            subjs = " · ".join(pd["subjects"])
            st.markdown(
                f'<div class="tcard"><span class="ic">{pd["icon"]}</span>'
                f"<h4>{pk}</h4>"
                f'<p>{pd["desc"]}</p>'
                f"<p style='font-size:.8rem;margin-top:4px'>{subjs}</p>"
                f'<p style="color:#2563eb;font-weight:600;margin-top:4px">'
                f'{n} simulator{"s" if n != 1 else ""}</p></div>',
                unsafe_allow_html=True,
            )

    st.markdown("---")
    st.markdown(
        "### 🚀 Quick Start\n"
        "1. Click **🧪 Simulators** in the sidebar\n"
        "2. Choose a **simulator pack**\n"
        "3. Pick a **subject** — Physics, Chemistry, Mathematics, or Applied STEM\n"
        "4. Select a **topic** and explore the interactive simulator\n"
        "5. Adjust sliders and parameters to see real-time results\n"
    )
    _footer()


# ─── Page: Simulators ────────────────────────────────────────────────────────
def _page_sim(_topic, _pack, _subj, user):
    if _topic is None:
        st.info("👈 Select a pack, subject, and topic from the sidebar to begin.")
        return

    st.markdown(
        f'<div class="bc">{_pack}<span class="sep">›</span>'
        f'{_subj}<span class="sep">›</span>'
        f'<span class="cur">{_topic["icon"]} {_topic["name"]}</span></div>',
        unsafe_allow_html=True,
    )

    # Audit simulator access
    audit.log(
        audit.SIM_ACCESS,
        user_id=user["id"],
        username=user["username"],
        detail=sanitize_log(f'{_pack} > {_subj} > {_topic["name"]}'),
    )

    detail = _topic.get("detail")
    if detail:
        st.markdown(f'<div class="sim-desc">{detail}</div>', unsafe_allow_html=True)

    refs = _topic.get("refs")
    if refs:
        links = "".join(
            f'<a href="{r["url"]}" target="_blank" rel="noopener noreferrer">'
            f'{r["title"]}</a>'
            for r in refs
        )
        st.markdown(
            f'<div class="ref-list">📚 {links}</div>',
            unsafe_allow_html=True,
        )

    try:
        ok, err = safe_run_simulator(_run, _topic["module"], _topic.get("func", "simulate"))
        if not ok:
            st.error(f"Could not load simulator: {err}")
            st.info("Try selecting a different topic or refreshing the page.")
    except Exception as exc:
        log.error("Simulator load error: %s – %s", _topic["module"], exc)
        st.error(f"Could not load simulator: {exc}")
        st.info("Try selecting a different topic or refreshing the page.")


# ─── Page: User Guide ────────────────────────────────────────────────────────
def _page_guide():
    st.title("📖 User Guide")

    with st.expander("Getting Started", expanded=True):
        st.markdown(
            "1. Open the **sidebar** (click **>** on mobile)\n"
            "2. Select **🧪 Simulators**\n"
            "3. Choose a **simulator pack** and **subject**\n"
            "4. Pick a **topic** to load the simulator\n"
            "5. Use sliders and controls to change parameters\n"
            "6. Watch graphs and values update in real time"
        )

    with st.expander("Tips for Effective Learning"):
        st.markdown(
            "- **Change one thing at a time** — observe the effect before adjusting another\n"
            "- **Try extreme values** — push sliders to the limits to see boundary behaviour\n"
            "- **Cross-reference your textbook** — equations match your syllabus\n"
            "- **Predict first, then check** — guess the outcome before moving a slider\n"
            "- **Use reference links** — each simulator includes curated educational links\n"
            "- **Take notes** — write down observations for deeper understanding"
        )

    with st.expander("Pack & Age Guide"):
        st.markdown(
            "| Pack | Typical Age | Target Levels |\n"
            "|------|------------|---------------|\n"
            "| Foundation (6–8) | 11–14 | Cambridge Lower Secondary |\n"
            "| Core STEM (9–10) | 14–16 | IGCSE / ICSE |\n"
            "| Advanced (11–12) | 16–18 | AS / A Level / CBSE |\n"
            "| Cross-Disciplinary | All ages | Enrichment |"
        )

    with st.expander("Simulator Catalog"):
        for pk, pd in CATALOG.items():
            st.markdown(f"**{pd['icon']} {pk}**")
            for subj, topics in pd["subjects"].items():
                st.markdown(f"*{subj}*")
                for t in topics:
                    st.markdown(
                        f"- {t['icon']} **{t['name']}** — {t['desc']}"
                    )

    with st.expander("Subjects"):
        st.markdown(
            "**🔬 Physics** — Motion, forces, energy, waves, electricity, optics\n\n"
            "**⚗️ Chemistry** — Atoms, bonding, reactions, equilibrium, organic\n\n"
            "**📐 Mathematics** — Algebra, geometry, trigonometry, calculus, statistics"
        )

    with st.expander("Technical Notes"):
        st.markdown(
            "- All simulators use **SI units** unless noted\n"
            "- Models are idealised — some real-world factors are omitted\n"
            "- Built with **Streamlit**, **NumPy**, **Matplotlib**, and **SciPy**"
        )
    _footer()


# ─── Page: Profile ───────────────────────────────────────────────────────────
def _page_profile(user):
    st.title("👤 My Profile")

    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown(
            f'<div style="font-size:4rem;text-align:center">👤</div>',
            unsafe_allow_html=True,
        )
        st.markdown(f"**{user['display_name']}**")
        st.caption(f"@{user['username']} · {user['role'].title()}")
    with c2:
        st.markdown("##### Account Details")
        st.text_input("Email", value=user["email"], disabled=True)
        st.text_input("Member Since", value=user["created_at"][:10], disabled=True)

    st.markdown("---")

    # ── Change password ──
    st.markdown("##### 🔒 Change Password")
    with st.form("change_pw"):
        old_pw = st.text_input("Current Password", type="password")
        new_pw = st.text_input("New Password", type="password")
        new_pw2 = st.text_input("Confirm New Password", type="password")
        pw_submit = st.form_submit_button("Update Password")
    if pw_submit:
        if not old_pw or not new_pw:
            st.warning("Please fill in all fields.")
        elif new_pw != new_pw2:
            st.warning("New passwords do not match.")
        elif len(new_pw) < 8:
            st.warning("New password must be at least 8 characters.")
        else:
            strength_errors = validate_password_strength(new_pw)
            if strength_errors:
                for se in strength_errors:
                    st.warning(se)
            else:
                from core.database import get_db

            with get_db() as conn:
                row = conn.execute(
                    "SELECT password_hash FROM users WHERE id = ?", (user["id"],)
                ).fetchone()
            if row and auth.verify_password(old_pw, row["password_hash"]):
                new_hash = auth.hash_password(new_pw)
                with get_db() as conn:
                    conn.execute(
                        "UPDATE users SET password_hash = ?, updated_at = datetime('now') WHERE id = ?",
                        (new_hash, user["id"]),
                    )
                audit.log(
                    audit.PASSWORD_CHANGE,
                    user_id=user["id"],
                    username=user["username"],
                )
                st.success("Password updated successfully.")
            else:
                st.error("Current password is incorrect.")

    # ── Activity log ──
    st.markdown("---")
    st.markdown("##### 📋 Recent Activity")
    history = audit.user_history(user["id"], limit=20)
    if history:
        for entry in history:
            st.markdown(
                f"- **{entry['action']}** — {entry.get('detail', '')} "
                f"<small style='color:#9ca3af'>{entry['timestamp']}</small>",
                unsafe_allow_html=True,
            )
    else:
        st.caption("No activity recorded yet.")

    _footer()


# ─── Page: Admin Dashboard ───────────────────────────────────────────────────
def _page_admin(user):
    st.title("🛡️ Admin Dashboard")

    # ── Stats ──
    stats = admin.dashboard_stats()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("👥 Total Users", stats["total_users"])
    c2.metric("✅ Active Users", stats["active_users"])
    c3.metric("🔑 Active Sessions", stats["active_sessions"])
    c4.metric("📝 Audit Events (24h)", stats["audit_events_24h"])

    st.markdown("---")

    tab_users, tab_audit = st.tabs(["👥 User Management", "📋 Audit Log"])

    # ── User management ──
    with tab_users:
        search = sanitize_text(
            st.text_input("🔍 Search users", placeholder="Username, email, or name"),
            max_length=INPUT_MAX_SEARCH,
            strip_html=False,
        )
        users = admin.list_users(search=search)

        if users:
            for u in users:
                with st.expander(
                    f"{'🟢' if u['is_active'] else '🔴'} "
                    f"{u['username']} — {u['email']} ({u['role']})"
                ):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        new_role = st.selectbox(
                            "Role",
                            ROLES,
                            index=ROLES.index(u["role"]),
                            key=f"role_{u['id']}",
                        )
                        if new_role != u["role"]:
                            if st.button("Update Role", key=f"ur_{u['id']}"):
                                allowed, reason = can_modify_user(user["id"], u["id"])
                                if not allowed:
                                    st.warning(reason)
                                else:
                                    admin.set_role(u["id"], new_role, admin_name=user["username"])
                                    st.success(f"Role updated to {new_role}.")
                                    st.rerun()
                    with col2:
                        if u["is_active"]:
                            if st.button("🔴 Deactivate", key=f"da_{u['id']}"):
                                allowed, reason = can_modify_user(user["id"], u["id"])
                                if not allowed:
                                    st.warning(reason)
                                else:
                                    admin.set_active(u["id"], False, admin_name=user["username"])
                                    st.rerun()
                        else:
                            if st.button("🟢 Activate", key=f"ac_{u['id']}"):
                                admin.set_active(u["id"], True, admin_name=user["username"])
                                st.rerun()
                    with col3:
                        if st.button("🔓 Unlock", key=f"ul_{u['id']}"):
                            admin.unlock_user(u["id"], admin_name=user["username"])
                            st.success("User unlocked.")
        else:
            st.info("No users found.")

    # ── Audit log viewer ──
    with tab_audit:
        col1, col2 = st.columns([1, 3])
        with col1:
            action_filter = st.selectbox(
                "Filter by action",
                ["All", audit.LOGIN, audit.LOGOUT, audit.SIGNUP,
                 audit.LOGIN_FAILED, audit.SIM_ACCESS, audit.PASSWORD_CHANGE,
                 audit.ADMIN_ROLE_CHANGE, audit.ADMIN_DEACTIVATE, audit.ADMIN_ACTIVATE],
            )
        with col2:
            limit = st.slider("Entries", 10, 500, 100)

        action_val = None if action_filter == "All" else action_filter
        entries = audit.recent(limit=limit, action=action_val)

        if entries:
            for e in entries:
                st.markdown(
                    f"`{e['timestamp']}` **{e['action']}** — "
                    f"user={e.get('username', '?')} — {e.get('detail', '')}"
                )
        else:
            st.info("No audit entries.")

        st.markdown("---")
        st.markdown("##### 📊 Action Summary")
        summary = audit.count_by_action()
        if summary:
            for s in summary:
                st.markdown(f"- **{s['action']}** — {s['cnt']} events")

    _footer()


# ─── Page: Terms of Service ──────────────────────────────────────────────────
def _page_terms():
    st.title("📜 Terms of Service")
    st.markdown(f"*Effective Date: January 1, 2026 · {APP_NAME} v{APP_VERSION}*")
    st.markdown(f"""
### 1. Acceptance of Terms
By accessing or using {APP_NAME} ("the Service"), you agree to be bound by these
Terms of Service. If you do not agree, do not use the Service.

### 2. Description of Service
{APP_NAME} is an interactive educational platform providing science and mathematics
simulators organised into four themed packs — Foundation, Core STEM, Advanced, and
Cross-Disciplinary Enrichment.

### 3. User Accounts
- You must provide accurate information during registration.
- You are responsible for maintaining the confidentiality of your credentials.
- You must notify us immediately of any unauthorized use of your account.
- Accounts are for individual use and may not be shared.

### 4. Acceptable Use
You agree **not** to:
- Use the Service for any unlawful purpose.
- Attempt to gain unauthorized access to other accounts or systems.
- Reverse-engineer, decompile, or disas­semble any part of the Service.
- Use automated tools to scrape or extract data from the Service.

### 5. Intellectual Property
All content, simulators, and materials on {APP_NAME} are the intellectual property
of their respective owners. You may use them for personal educational purposes only.

### 6. Limitation of Liability
The Service is provided "as is" without warranty. We are not liable for any indirect,
incidental, or consequential damages arising from your use of the Service.

### 7. Termination
We reserve the right to suspend or terminate your account at our discretion for
violation of these terms.

### 8. Changes to Terms
We may update these terms at any time. Continued use constitutes acceptance.

### 9. Contact
Questions? Email **{SUPPORT_EMAIL}**
""")
    _footer()


# ─── Page: Privacy Policy ────────────────────────────────────────────────────
def _page_privacy():
    st.title("🔒 Privacy Policy")
    st.markdown(f"*Effective Date: January 1, 2026 · {APP_NAME} v{APP_VERSION}*")
    st.markdown(f"""
### 1. Information We Collect
- **Account Data**: Username, email, display name (provided at registration).
- **Usage Data**: Simulator access logs, timestamps, and session information.
- **Technical Data**: Browser type and session metadata for security purposes.

### 2. How We Use Your Information
- To provide and maintain the Service.
- To authenticate your identity and manage your account.
- To generate aggregate usage analytics (no individual tracking is sold).
- To improve simulator content and platform features.
- To detect and prevent fraud or abuse.

### 3. Data Storage & Security
- Passwords are **hashed using bcrypt** and never stored in plain text.
- All data is stored in a local database under your deployment's control.
- We implement industry-standard security measures including session management,
  account lockout, and audit logging.

### 4. Data Sharing
We do **not** sell, trade, or share your personal information with third parties,
except as required by law.

### 5. Data Retention
- Account data is retained while your account is active.
- Audit logs are retained for a minimum of 12 months for security purposes.
- You may request deletion of your account by contacting **{SUPPORT_EMAIL}**.

### 6. Your Rights
- **Access**: Request a copy of your personal data.
- **Correction**: Update inaccurate or incomplete data.
- **Deletion**: Request removal of your account and associated data.
- **Portability**: Receive your data in a structured, machine-readable format.

### 7. Cookies & Sessions
{APP_NAME} uses session tokens to keep you logged in. These are essential for
the Service to function and are not used for advertising.

### 8. Changes to This Policy
We may update this policy at any time. Changes will be posted on this page.

### 9. Contact
Privacy inquiries: **{SUPPORT_EMAIL}**
""")
    _footer()


# ─── Page: About ─────────────────────────────────────────────────────────────
def _page_about():
    st.title("ℹ️ About STEM Lab")
    s = get_stats()
    st.markdown(
        f"**{APP_NAME}** is an open-source educational platform "
        f"providing {s['simulators']} interactive simulators for Physics, Chemistry, "
        f"Mathematics, and Applied STEM across {s['packs']} themed packs."
    )

    st.markdown("### Technology Stack")
    cols = st.columns(5)
    cols[0].markdown("**Streamlit**\n\nInteractive UI")
    cols[1].markdown("**NumPy**\n\nNumerical computing")
    cols[2].markdown("**Matplotlib**\n\nVisualisations")
    cols[3].markdown("**SciPy**\n\nScientific computing")
    cols[4].markdown("**SQLite + bcrypt**\n\nAuth & Data")

    st.markdown("### Features")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            "- 🔐 Secure authentication (signup / login)\n"
            "- 📋 Full audit trail & activity logging\n"
            "- 🛡️ Admin dashboard & user management\n"
            "- 👤 User profiles with password management"
        )
    with c2:
        st.markdown(
            f"- 📊 {s['simulators']}+ interactive simulators\n"
            f"- 📦 {s['packs']} themed simulator packs\n"
            "- 📜 Terms of Service & Privacy Policy\n"
            "- 🔄 Session management with timeout"
        )

    st.markdown("### Version")
    st.markdown(
        f"**v{APP_VERSION}** · 2026 · Apache License 2.0 · Auth, audit & admin"
    )
    _footer()


# ─── Footer ──────────────────────────────────────────────────────────────────
def _footer():
    st.markdown(
        f'<div class="foot">{APP_NAME} v{APP_VERSION} · Built with Streamlit '
        f"· © 2026</div>",
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════
_restore_session()

if _current_user() is None:
    _page_auth()
else:
    _main_app()
