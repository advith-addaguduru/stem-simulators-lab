"""
STEM Lab — Admin Helpers
========================
User-management queries and actions consumed by the admin dashboard in app.py.
"""

from core.database import get_db
from core import audit
from core.guardrails import sanitize_text, can_modify_user
from core.settings import INPUT_MAX_SEARCH


# ─── User queries ─────────────────────────────────────────────────────────────

def list_users(
    search: str = "",
    role: str | None = None,
    active_only: bool = False,
) -> list[dict]:
    """Return users, optionally filtered by search term, role, or active status."""
    clauses: list[str] = []
    params: list = []

    if search:
        search = sanitize_text(search, max_length=INPUT_MAX_SEARCH, strip_html=False)
        clauses.append("(username LIKE ? OR email LIKE ? OR display_name LIKE ?)")
        like = f"%{search}%"
        params.extend([like, like, like])
    if role:
        clauses.append("role = ?")
        params.append(role)
    if active_only:
        clauses.append("is_active = 1")

    where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
    with get_db() as conn:
        rows = conn.execute(
            f"SELECT id, username, email, display_name, role, is_active, "
            f"created_at, last_login_at FROM users {where} ORDER BY created_at DESC",
            params,
        ).fetchall()
    return [dict(r) for r in rows]


def get_user(user_id: int) -> dict | None:
    with get_db() as conn:
        row = conn.execute(
            "SELECT id, username, email, display_name, role, is_active, "
            "created_at, last_login_at, failed_attempts, locked_until "
            "FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()
    return dict(row) if row else None


def user_count() -> int:
    with get_db() as conn:
        return conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]


# ─── User mutations ──────────────────────────────────────────────────────────

def set_role(user_id: int, new_role: str, *, admin_name: str = "admin", admin_id: int | None = None):
    if admin_id is not None:
        allowed, _ = can_modify_user(admin_id, user_id)
        if not allowed:
            return
    with get_db() as conn:
        conn.execute(
            "UPDATE users SET role = ?, updated_at = datetime('now') WHERE id = ?",
            (new_role, user_id),
        )
    audit.log(
        audit.ADMIN_ROLE_CHANGE,
        username=admin_name,
        detail=f"user_id={user_id} new_role={new_role}",
    )


def set_active(user_id: int, active: bool, *, admin_name: str = "admin", admin_id: int | None = None):
    if admin_id is not None:
        allowed, _ = can_modify_user(admin_id, user_id)
        if not allowed:
            return
    with get_db() as conn:
        conn.execute(
            "UPDATE users SET is_active = ?, updated_at = datetime('now') WHERE id = ?",
            (int(active), user_id),
        )
    action = audit.ADMIN_ACTIVATE if active else audit.ADMIN_DEACTIVATE
    audit.log(action, username=admin_name, detail=f"user_id={user_id}")


def unlock_user(user_id: int, *, admin_name: str = "admin"):
    with get_db() as conn:
        conn.execute(
            "UPDATE users SET failed_attempts = 0, locked_until = NULL, "
            "updated_at = datetime('now') WHERE id = ?",
            (user_id,),
        )
    audit.log(
        audit.ADMIN_USER_UPDATE,
        username=admin_name,
        detail=f"Unlocked user_id={user_id}",
    )


# ─── Dashboard stats ─────────────────────────────────────────────────────────

def dashboard_stats() -> dict:
    with get_db() as conn:
        total = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        active = conn.execute("SELECT COUNT(*) FROM users WHERE is_active = 1").fetchone()[0]
        by_role = dict(
            conn.execute(
                "SELECT role, COUNT(*) FROM users GROUP BY role"
            ).fetchall()
        )
        recent_signups = conn.execute(
            "SELECT COUNT(*) FROM users WHERE created_at >= datetime('now', '-7 days')"
        ).fetchone()[0]
        active_sessions = conn.execute(
            "SELECT COUNT(*) FROM sessions WHERE is_valid = 1"
        ).fetchone()[0]
        audit_24h = conn.execute(
            "SELECT COUNT(*) FROM audit_log WHERE timestamp >= datetime('now', '-1 day')"
        ).fetchone()[0]
    return {
        "total_users": total,
        "active_users": active,
        "inactive_users": total - active,
        "by_role": by_role,
        "recent_signups_7d": recent_signups,
        "active_sessions": active_sessions,
        "audit_events_24h": audit_24h,
    }
