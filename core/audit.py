"""
STEM Lab — Audit Trail
=======================
Logs user actions to both the database and a dedicated audit log file.
"""

from core.database import get_db
from core.logger import get_audit_logger
from core.guardrails import sanitize_log

_audit = get_audit_logger()

# ─── Action constants ─────────────────────────────────────────────────────────
SIGNUP = "SIGNUP"
LOGIN = "LOGIN"
LOGIN_FAILED = "LOGIN_FAILED"
LOGOUT = "LOGOUT"
SIM_ACCESS = "SIM_ACCESS"
PROFILE_UPDATE = "PROFILE_UPDATE"
PASSWORD_CHANGE = "PASSWORD_CHANGE"
ADMIN_USER_UPDATE = "ADMIN_USER_UPDATE"
ADMIN_ROLE_CHANGE = "ADMIN_ROLE_CHANGE"
ADMIN_DEACTIVATE = "ADMIN_DEACTIVATE"
ADMIN_ACTIVATE = "ADMIN_ACTIVATE"


# ─── Write ────────────────────────────────────────────────────────────────────

def log(
    action: str,
    *,
    user_id: int | None = None,
    username: str = "",
    detail: str = "",
    ip_address: str = "",
    level: str = "INFO",
):
    """Record an auditable event in the DB and the audit log file."""
    # DB
    with get_db() as conn:
        conn.execute(
            "INSERT INTO audit_log (user_id, username, action, detail, ip_address, level) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, username, action, detail, ip_address, level),
        )
    # File (sanitize to prevent log injection)
    _audit.info(
        "%s | user=%s (%s) | %s | %s",
        sanitize_log(action),
        sanitize_log(username),
        user_id,
        sanitize_log(detail),
        sanitize_log(ip_address),
    )


# ─── Query helpers (for admin dashboard) ──────────────────────────────────────

def recent(limit: int = 100, action: str | None = None) -> list[dict]:
    """Return the *limit* most-recent audit entries, optionally filtered by action."""
    with get_db() as conn:
        if action:
            rows = conn.execute(
                "SELECT * FROM audit_log WHERE action = ? ORDER BY timestamp DESC LIMIT ?",
                (action, limit),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM audit_log ORDER BY timestamp DESC LIMIT ?",
                (limit,),
            ).fetchall()
    return [dict(r) for r in rows]


def count_by_action() -> list[dict]:
    """Aggregate audit entries grouped by action."""
    with get_db() as conn:
        rows = conn.execute(
            "SELECT action, COUNT(*) AS cnt FROM audit_log GROUP BY action ORDER BY cnt DESC"
        ).fetchall()
    return [dict(r) for r in rows]


def user_history(user_id: int, limit: int = 50) -> list[dict]:
    """Return audit entries for a specific user."""
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM audit_log WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?",
            (user_id, limit),
        ).fetchall()
    return [dict(r) for r in rows]
