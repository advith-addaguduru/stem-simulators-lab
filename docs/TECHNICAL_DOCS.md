# 🔧 STEM Lab — Technical Documentation

## Architecture Overview

STEM Lab is a **Streamlit** web application that dynamically loads interactive science and mathematics simulators organised into themed **simulator packs**.

```
stem-simulators-lab/
├── app.py                          # Main application (auth gate, router, admin)
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variable template
├── .streamlit/config.toml          # Streamlit Cloud theme
├── LICENSE                         # Apache License 2.0
├── README.md
├── core/                           # Platform infrastructure
│   ├── settings.py                 # Centralised env-based configuration
│   ├── database.py                 # SQLite database layer (users, sessions, audit)
│   ├── auth.py                     # Authentication (signup, login, sessions, bcrypt)
│   ├── guardrails.py               # Input sanitization, rate limiting, password policy
│   ├── logger.py                   # Rotating file + console logging
│   ├── audit.py                    # Audit trail (DB + file)
│   └── admin.py                    # Admin dashboard helpers
├── data/                           # SQLite database (auto-created, git-ignored)
├── logs/                           # Application & audit logs (auto-created, git-ignored)
├── docs/
│   ├── USER_GUIDE.md               # End-user guide
│   └── TECHNICAL_DOCS.md           # Developer documentation (this file)
└── simulators/
    ├── __init__.py
    ├── utils.py                    # Shared helpers (nice_axes, close_fig)
    ├── config.py                   # Simulator catalog / registry (pack-based)
    ├── physics/
    │   ├── lower_secondary/        # Foundation pack
    │   ├── igcse_9_10/             # Core STEM pack
    │   ├── cambridge_as/           # Advanced pack — AS Level
    │   ├── cambridge_a/            # Advanced pack — A Level
    │   ├── cbse/                   # Advanced pack — CBSE
    │   └── icse/                   # Core STEM pack — ICSE
    ├── chemistry/                  # (same sub-folders)
    ├── maths/                      # (same sub-folders)
    └── cross_disciplinary/         # Cross-Disciplinary Enrichment pack
```

---

## Core Components

### `app.py` — Application Entry Point

| Section | Purpose |
|---------|---------|
| Page config | `st.set_page_config()` — title, icon, layout |
| Custom CSS | Injected via `st.markdown(unsafe_allow_html=True)` for hero banner, cards, breadcrumbs, footer |
| Auth gate | `_restore_session()` + `_page_auth()` — login / signup with guardrail-protected inputs |
| `_run()` | Dynamic module loader using `importlib.import_module()` |
| Sidebar | Pack → Subject → Topic navigation + user pill + logout |
| Router | Maps sidebar selection to page renderer functions |
| Error boundary | Simulators wrapped in `safe_run_simulator()` for graceful degradation |

### `simulators/config.py` — Simulator Catalog

The `CATALOG` dictionary maps:

```
Pack → Subject → [Topics]
```

Each **pack** has `icon`, `desc`, and `subjects` keys. Each **topic** entry:

```python
{
    "name": "Display Name",        # User-friendly title
    "icon": "🚀",                  # Emoji icon
    "desc": "Short description",   # For card display
    "detail": "Longer description…",  # 2–3 sentences shown on the simulator page
    "refs": [                      # Educational reference links (shown as pills)
        {"title": "Khan Academy — Topic", "url": "https://…"},
    ],
    "module": "simulators.physics.lower_secondary.forces_and_motion",
    "func": "simulate",            # Function to call (default: "simulate")
}
```

`get_stats()` returns aggregate counts for the home page metrics.

### `simulators/utils.py` — Shared Utilities

- `nice_axes(ax, xlabel, ylabel, title)` — Consistent axis formatting.
- `close_fig(fig)` — Safely close matplotlib figures.

---

## Core Infrastructure (`core/`)

### `core/settings.py` — Configuration

All settings are loaded from environment variables with sensible defaults. See `.env.example` for the full list.

Key categories:
- **Paths**: `BASE_DIR`, `DATA_DIR`, `DATABASE_URL`
- **Security**: `SECRET_KEY`, `BCRYPT_ROUNDS`, `SESSION_TIMEOUT_SECONDS`, `MAX_LOGIN_ATTEMPTS`, `LOGIN_LOCK_SECONDS`
- **Guardrails**: `RATE_LIMIT_WINDOW`, `RATE_LIMIT_MAX_REQUESTS`, `SIGNUP_RATE_LIMIT_MAX`, `MAX_SESSIONS_PER_USER`, `INPUT_MAX_*`, `PASSWORD_REQUIRE_*`
- **Roles**: `ROLE_STUDENT`, `ROLE_TEACHER`, `ROLE_ADMIN`
- **Logging**: `LOG_DIR`, `LOG_LEVEL`, `LOG_FILE`, `AUDIT_LOG_FILE`
- **Metadata**: `APP_NAME`, `APP_VERSION`, `SUPPORT_EMAIL`

### `core/database.py` — SQLite Layer

- Thread-local connections with WAL mode and foreign keys enabled.
- `get_db()` context manager — commits on success, rolls back on error.
- `init_db()` bootstraps schema on first import.

**Tables**: `users`, `sessions`, `audit_log` (all with parameterised queries — no string interpolation).

### `core/auth.py` — Authentication

- **Password hashing**: bcrypt with configurable rounds.
- **Signup validation**: username regex, email regex, password min length, **password strength** (configurable complexity: upper, lower, digit, special), **input length enforcement**.
- **Login**: account lockout after configurable failed attempts, **rate limiting** via sliding-window limiter.
- **Session management**: UUID tokens, idle timeout, **concurrent session limit** (oldest sessions auto-invalidated).
- **Role helpers**: `is_admin()`, `is_teacher()`.

### `core/guardrails.py` — Security Guardrails

Centralised module providing:

| Function | Purpose |
|----------|---------|
| `sanitize_text()` | Strip whitespace, enforce max length, remove control chars, HTML-escape |
| `sanitize_log()` | Escape newlines and control chars to prevent log injection |
| `check_length()` | Validate input length against per-field limits |
| `validate_password_strength()` | Enforce configurable complexity rules (upper/lower/digit/special) |
| `check_login_rate()` | Sliding-window rate limiter for login attempts |
| `reset_login_rate()` | Clear rate-limit state after successful login |
| `check_signup_rate()` | Sliding-window rate limiter for signup attempts |
| `enforce_session_limit()` | Invalidate oldest sessions when user exceeds `MAX_SESSIONS_PER_USER` |
| `can_modify_user()` | Prevent admins from deactivating/demoting their own account |
| `safe_run_simulator()` | Error boundary — catches `ModuleNotFoundError`, `AttributeError`, and generic exceptions with typed messages |

The rate limiters use an in-memory sliding-window design (thread-safe via `threading.Lock`). They reset automatically as entries age out.

### `core/logger.py` — Logging

- `get_logger(name)` — Rotating file handler (5 MB, 3 backups) + console.
- `get_audit_logger()` — Dedicated audit log file.

### `core/audit.py` — Audit Trail

- Writes every auditable action to **both** the database and the audit log file.
- Log-injection prevention via `sanitize_log()` on all values written to the file logger.
- Query helpers: `recent()`, `count_by_action()`, `user_history()`.

### `core/admin.py` — Admin Helpers

- `list_users()` — search with sanitised input.
- `set_role()` / `set_active()` — server-side `can_modify_user()` guard to prevent self-modification.
- `dashboard_stats()` — aggregate metrics for the admin dashboard.

---

## Security & Guardrails Summary

The guardrails system protects the application at multiple layers:

```
User Input  ──►  Sanitization (HTML escape, length, control chars)
                      │
                 Rate Limiting (login / signup sliding window)
                      │
                 Validation (format + password strength)
                      │
                 Auth & Sessions (bcrypt, timeout, concurrent limit, lockout)
                      │
                 RBAC + Admin Self-Guard
                      │
                 Audit Trail (DB + sanitised file log)
                      │
                 Error Boundary (simulator load failures → graceful UI)
```

All guardrail settings are configurable via environment variables. See the **Configuration** table in the README.

---

## Simulator Module Contract

Every simulator module must expose a **callable function** (default name: `simulate`) that:

1. Accepts **no arguments** — all user input comes from Streamlit widgets.
2. Uses `streamlit` (`st`) for UI rendering.
3. Uses `matplotlib` for visualisations and calls `plt.close(fig)` after `st.pyplot()`.
4. Is self-contained — no return values, no global state.

Example skeleton:

```python
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def simulate():
    st.header("My Simulator")
    x = st.slider("Parameter", 0, 100, 50)
    fig, ax = plt.subplots()
    ax.plot(range(x))
    st.pyplot(fig)
    plt.close(fig)
```

---

## Adding a New Simulator

1. **Create the module** in the appropriate directory:
   ```
   simulators/<subject>/<level>/<topic_name>.py
   ```

2. **Implement** the `simulate()` function following the contract above.

3. **Register** the simulator in `simulators/config.py` by adding a topic entry to the appropriate pack → subject list.

4. **Test** by running `streamlit run app.py` and navigating to the new topic.

---

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| streamlit | ≥ 1.56.0 | Web framework and UI |
| numpy | ≥ 2.4.4 | Numerical computation |
| matplotlib | ≥ 3.10.8 | Data visualisation |
| scipy | ≥ 1.17.1 | Scientific computing (selected sims) || bcrypt | ≥ 4.3.0 | Password hashing |
Install: `pip install -r requirements.txt`

---

## Deployment

### Streamlit Cloud

1. Push the repository to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io).
3. Connect the repository and set `app.py` as the entry point.
4. Theme is auto-configured via `.streamlit/config.toml`.

### Local Development

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux
pip install -r requirements.txt
cp .env.example .env         # Edit .env — at minimum set STEMLAB_SECRET_KEY
streamlit run app.py
```

### Docker (Optional)

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501"]
```

---

## Testing

Run any simulator module directly for quick validation:

```bash
streamlit run app.py
```

Navigate to the specific simulator via the sidebar. Verify:
- Widgets render without errors.
- Graphs update on parameter changes.
- Edge-case values (0, max) don't crash the simulator.

---

## Performance Notes

- **Lazy loading**: Simulator modules are imported on demand via `importlib`, keeping initial page load fast.
- **Figure cleanup**: All `matplotlib` figures are closed after rendering to prevent memory leaks.
- **No caching needed**: Simulators compute results on each interaction (sub-second for all current modules).

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 5.2 | 2026 | Reorganised catalog from grade-based to pack-based navigation (4 packs: Foundation, Core STEM, Advanced, Cross-Disciplinary). Added 10 new simulators (Projectile Motion, Acids/Bases pH, Probability & Data, Resonance & Damping, Kinetics Lab, Vectors 3D, Bridge Design, Climate Model, Epidemiology SIR, Coding & Maths). New `cross_disciplinary/` module. 62 total simulators. Updated all documentation |
| 5.1 | 2026 | Added `core/guardrails.py` — input sanitization, rate limiting (login + signup), password strength policy, concurrent session limiting, admin self-guard, error boundaries. Integrated guardrails across auth, audit, admin, and app modules. 14 new environment-configurable settings. Updated all documentation |
| 5.0 | 2026 | Added `core/` infrastructure: settings.py, database.py, auth.py, logger.py, audit.py, admin.py. Authentication with bcrypt, session management, role-based access, admin dashboard, user profiles, audit trail, legal pages. SQLite database with WAL mode |
| 4.2 | 2025 | Added 12 new simulators: Simple Circuits (Gr 6), Ratio & Proportion (Gr 6), Magnets (Gr 7), Separation Techniques (Gr 7), Linear Equations (Gr 8), Electricity (IGCSE), Waves & Light (IGCSE), Fields (A-Level), Organic Chemistry (A-Level), Statistics & Probability (A-Level), Optics (CBSE 12), Atomic Structure & Periodic Table (CBSE 11). Updated dependencies to latest stable versions. Total: 54 simulators |
| 4.1 | 2026 | Added simulator descriptions (`detail`) and curated reference URLs (`refs`) to every topic entry. Updated UI to display description and reference link pills on each simulator page. Consolidated documentation: merged changelog into TECHNICAL_DOCS, removed redundant QUICK_START.md and IMPLEMENTATION_SUMMARY.md |
| 4.0 | 2026 | Complete re-architecture to grade-based navigation, enterprise UI, central `CATALOG` registry in `config.py`, dynamic module loading via `importlib`, 9 new Lower Secondary simulators (Grades 6–8), custom CSS (hero banner, topic cards, breadcrumbs, footer), Apache License 2.0, Streamlit Cloud readiness |
| 3.0 | 2026 | Multi-curriculum support (IGCSE, AS, A, CBSE, ICSE) |
| 2.0 | 2025 | Added chemistry and maths |
| 1.0 | 2025 | Initial physics simulators |

---

*STEM Lab · Apache License 2.0 · v5.2 · © 2026*
