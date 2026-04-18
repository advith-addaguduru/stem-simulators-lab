"""
STEM Lab — Authentication Module
=================================
Signup, login, logout, session management with bcrypt password hashing.
"""

import uuid
import re
from datetime import datetime, timedelta

import bcrypt

from core.settings import (
    BCRYPT_ROUNDS,
    SESSION_TIMEOUT_SECONDS,
    MAX_LOGIN_ATTEMPTS,
    LOGIN_LOCK_SECONDS,
    ROLE_STUDENT,
    ROLES,
    INPUT_MAX_USERNAME,
    INPUT_MAX_EMAIL,
    INPUT_MAX_DISPLAY_NAME,
    INPUT_MAX_PASSWORD,
)
from core.database import get_db
from core.guardrails import (
    sanitize_text,
    check_length,
    validate_password_strength,
    check_login_rate,
    reset_login_rate,
    enforce_session_limit,
)

# ─── Password helpers ────────────────────────────────────────────────────────

def hash_password(plain: str) -> str:
    """Return a bcrypt hash for *plain* text password."""
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt(rounds=BCRYPT_ROUNDS)).decode()


def verify_password(plain: str, hashed: str) -> bool:
    """Check *plain* against a bcrypt *hashed* value."""
    return bcrypt.checkpw(plain.encode(), hashed.encode())


# ─── Validation ───────────────────────────────────────────────────────────────

_USERNAME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_]{2,29}$")
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_PASSWORD_MIN_LEN = 8


def _validate_signup(username: str, email: str, password: str, display_name: str = "") -> list[str]:
    """Return a list of validation error messages (empty → valid)."""
    errors: list[str] = []
    # Length guardrails
    if (err := check_length(username, "Username", INPUT_MAX_USERNAME)):
        errors.append(err)
    if (err := check_length(email, "Email", INPUT_MAX_EMAIL)):
        errors.append(err)
    if (err := check_length(password, "Password", INPUT_MAX_PASSWORD)):
        errors.append(err)
    if display_name and (err := check_length(display_name, "Display name", INPUT_MAX_DISPLAY_NAME)):
        errors.append(err)
    # Format checks
    if not _USERNAME_RE.match(username):
        errors.append(
            "Username must be 3-30 characters, start with a letter, "
            "and contain only letters, digits, or underscores."
        )
    if not _EMAIL_RE.match(email):
        errors.append("Invalid email address.")
    if len(password) < _PASSWORD_MIN_LEN:
        errors.append(f"Password must be at least {_PASSWORD_MIN_LEN} characters.")
    # Password strength
    errors.extend(validate_password_strength(password))
    return errors


# ─── Signup ───────────────────────────────────────────────────────────────────

def signup(
    username: str,
    email: str,
    password: str,
    display_name: str = "",
    role: str = ROLE_STUDENT,
) -> dict:
    """
    Create a new user account.

    Returns ``{"ok": True, "user_id": int}`` on success,
    ``{"ok": False, "errors": list[str]}`` on failure.
    """
    username = sanitize_text(username, max_length=INPUT_MAX_USERNAME, strip_html=False)
    email = sanitize_text(email, max_length=INPUT_MAX_EMAIL, strip_html=False).lower()
    display_name = sanitize_text(display_name, max_length=INPUT_MAX_DISPLAY_NAME) or username

    errors = _validate_signup(username, email, password, display_name)
    if role not in ROLES:
        errors.append(f"Invalid role: {role}")
    if errors:
        return {"ok": False, "errors": errors}

    pw_hash = hash_password(password)

    try:
        with get_db() as conn:
            cur = conn.execute(
                "INSERT INTO users (username, email, password_hash, display_name, role) "
                "VALUES (?, ?, ?, ?, ?)",
                (username, email, pw_hash, display_name, role),
            )
            return {"ok": True, "user_id": cur.lastrowid}
    except Exception as exc:
        msg = str(exc).lower()
        if "unique" in msg and "username" in msg:
            return {"ok": False, "errors": ["Username already taken."]}
        if "unique" in msg and "email" in msg:
            return {"ok": False, "errors": ["Email already registered."]}
        if "unique" in msg:
            return {"ok": False, "errors": ["Username or email already registered."]}
        raise


# ─── Login ────────────────────────────────────────────────────────────────────

def _is_locked(user: dict) -> bool:
    if user["locked_until"] is None:
        return False
    lock_end = datetime.fromisoformat(user["locked_until"])
    return datetime.utcnow() < lock_end


def login(identifier: str, password: str) -> dict:
    """
    Authenticate by username or email.

    Returns ``{"ok": True, "session_id": str, "user": dict}`` or
    ``{"ok": False, "error": str}``.
    """
    identifier = identifier.strip()

    # Rate-limit guard
    if not check_login_rate(identifier):
        return {"ok": False, "error": "Too many login attempts. Please wait and try again."}

    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE username = ? OR email = ?",
            (identifier, identifier.lower()),
        ).fetchone()

        if row is None:
            return {"ok": False, "error": "Invalid credentials."}

        user = dict(row)

        if not user["is_active"]:
            return {"ok": False, "error": "Account is deactivated. Contact support."}

        if _is_locked(user):
            return {"ok": False, "error": "Account temporarily locked. Try again later."}

        if not verify_password(password, user["password_hash"]):
            # Increment failed attempts
            attempts = user["failed_attempts"] + 1
            locked_until = None
            if attempts >= MAX_LOGIN_ATTEMPTS:
                locked_until = (
                    datetime.utcnow() + timedelta(seconds=LOGIN_LOCK_SECONDS)
                ).isoformat()
            conn.execute(
                "UPDATE users SET failed_attempts = ?, locked_until = ? WHERE id = ?",
                (attempts, locked_until, user["id"]),
            )
            remaining = MAX_LOGIN_ATTEMPTS - attempts
            if remaining > 0:
                return {"ok": False, "error": f"Invalid credentials. {remaining} attempt(s) remaining."}
            return {"ok": False, "error": "Account locked due to too many failed attempts."}

        # Successful login — reset failed attempts, update last_login_at
        conn.execute(
            "UPDATE users SET failed_attempts = 0, locked_until = NULL, "
            "last_login_at = datetime('now') WHERE id = ?",
            (user["id"],),
        )

        # Enforce concurrent session limit, then create session
        enforce_session_limit(user["id"], conn)
        session_id = uuid.uuid4().hex
        conn.execute(
            "INSERT INTO sessions (id, user_id) VALUES (?, ?)",
            (session_id, user["id"]),
        )
        reset_login_rate(identifier)

        safe_user = {
            k: user[k]
            for k in ("id", "username", "email", "display_name", "role", "created_at")
        }
        return {"ok": True, "session_id": session_id, "user": safe_user}


# ─── Session management ──────────────────────────────────────────────────────

def get_current_user(session_id: str | None) -> dict | None:
    """Return user dict for a valid session, or ``None``."""
    if not session_id:
        return None

    with get_db() as conn:
        row = conn.execute(
            "SELECT s.*, u.id AS uid, u.username, u.email, u.display_name, "
            "u.role, u.is_active, u.created_at "
            "FROM sessions s JOIN users u ON s.user_id = u.id "
            "WHERE s.id = ? AND s.is_valid = 1",
            (session_id,),
        ).fetchone()

        if row is None:
            return None

        sess = dict(row)

        if not sess["is_active"]:
            return None

        # Check session timeout
        last_active = datetime.fromisoformat(sess["last_active_at"])
        if (datetime.utcnow() - last_active).total_seconds() > SESSION_TIMEOUT_SECONDS:
            conn.execute("UPDATE sessions SET is_valid = 0 WHERE id = ?", (session_id,))
            return None

        # Touch session
        conn.execute(
            "UPDATE sessions SET last_active_at = datetime('now') WHERE id = ?",
            (session_id,),
        )

        return {
            "id": sess["uid"],
            "username": sess["username"],
            "email": sess["email"],
            "display_name": sess["display_name"],
            "role": sess["role"],
            "created_at": sess["created_at"],
        }


def logout(session_id: str):
    """Invalidate a session."""
    if not session_id:
        return
    with get_db() as conn:
        conn.execute("UPDATE sessions SET is_valid = 0 WHERE id = ?", (session_id,))


def logout_all(user_id: int):
    """Invalidate all sessions for a given user."""
    with get_db() as conn:
        conn.execute("UPDATE sessions SET is_valid = 0 WHERE user_id = ?", (user_id,))


# ─── Role helpers ─────────────────────────────────────────────────────────────

def is_admin(user: dict | None) -> bool:
    return user is not None and user.get("role") == "admin"


def is_teacher(user: dict | None) -> bool:
    return user is not None and user.get("role") in ("teacher", "admin")
