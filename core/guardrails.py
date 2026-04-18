"""
STEM Lab — Guardrails Module
==============================
Input sanitization, rate limiting, password strength validation,
content length enforcement, log-injection prevention, concurrent
session limiting, and error-boundary helpers.
"""

import html
import re
import time
import threading
from collections import defaultdict
from functools import wraps

from core.settings import (
    MAX_SESSIONS_PER_USER,
    RATE_LIMIT_WINDOW,
    RATE_LIMIT_MAX_REQUESTS,
    SIGNUP_RATE_LIMIT_MAX,
    INPUT_MAX_USERNAME,
    INPUT_MAX_EMAIL,
    INPUT_MAX_DISPLAY_NAME,
    INPUT_MAX_PASSWORD,
    INPUT_MAX_SEARCH,
    PASSWORD_REQUIRE_UPPER,
    PASSWORD_REQUIRE_LOWER,
    PASSWORD_REQUIRE_DIGIT,
    PASSWORD_REQUIRE_SPECIAL,
)
from core.logger import get_logger

_log = get_logger("stemlab.guardrails")

# ─── Input Sanitization ──────────────────────────────────────────────────────

_CONTROL_CHAR_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


def sanitize_text(value: str, *, max_length: int = 500, strip_html: bool = True) -> str:
    """
    Sanitize a user-provided text value.

    1. Strip leading/trailing whitespace.
    2. Enforce *max_length*.
    3. Remove ASCII control characters (keeps \\n, \\r, \\t).
    4. Optionally HTML-escape to prevent stored XSS.
    """
    value = value.strip()
    if len(value) > max_length:
        value = value[:max_length]
    value = _CONTROL_CHAR_RE.sub("", value)
    if strip_html:
        value = html.escape(value, quote=True)
    return value


def sanitize_log(value: str) -> str:
    """
    Sanitize a string before writing it to log files.
    Replaces newlines and control characters to prevent log injection.
    """
    value = value.replace("\n", "\\n").replace("\r", "\\r")
    return _CONTROL_CHAR_RE.sub("", value)


# ─── Content Length Validation ────────────────────────────────────────────────

def check_length(value: str, field_name: str, max_len: int) -> str | None:
    """Return an error message if *value* exceeds *max_len*, else ``None``."""
    if len(value) > max_len:
        return f"{field_name} must be at most {max_len} characters."
    return None


# ─── Password Strength ───────────────────────────────────────────────────────

def validate_password_strength(password: str) -> list[str]:
    """
    Return a list of password-strength error messages (empty → strong enough).
    Checks complexity rules configured in settings.
    """
    errors: list[str] = []
    if PASSWORD_REQUIRE_UPPER and not re.search(r"[A-Z]", password):
        errors.append("Password must contain at least one uppercase letter.")
    if PASSWORD_REQUIRE_LOWER and not re.search(r"[a-z]", password):
        errors.append("Password must contain at least one lowercase letter.")
    if PASSWORD_REQUIRE_DIGIT and not re.search(r"\d", password):
        errors.append("Password must contain at least one digit.")
    if PASSWORD_REQUIRE_SPECIAL and not re.search(r"[!@#$%^&*(),.?\":{}|<>\[\]\\;'`~_+\-=/]", password):
        errors.append("Password must contain at least one special character.")
    return errors


# ─── Rate Limiter (in-memory sliding window) ─────────────────────────────────

class _RateLimiter:
    """Thread-safe sliding-window rate limiter keyed by an arbitrary string."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        # key -> list of timestamps
        self._buckets: dict[str, list[float]] = defaultdict(list)

    def allow(self, key: str, max_requests: int, window_seconds: int) -> bool:
        """Return ``True`` if the request is within limits."""
        now = time.monotonic()
        cutoff = now - window_seconds
        with self._lock:
            bucket = self._buckets[key]
            # Evict expired entries
            self._buckets[key] = [t for t in bucket if t > cutoff]
            if len(self._buckets[key]) >= max_requests:
                return False
            self._buckets[key].append(now)
            return True

    def reset(self, key: str) -> None:
        """Clear rate-limit state for *key* (e.g. after successful login)."""
        with self._lock:
            self._buckets.pop(key, None)


# Singleton rate limiters
_login_limiter = _RateLimiter()
_signup_limiter = _RateLimiter()


def check_login_rate(identifier: str) -> bool:
    """Return ``True`` if the login attempt is within rate limits."""
    return _login_limiter.allow(
        f"login:{identifier}",
        max_requests=RATE_LIMIT_MAX_REQUESTS,
        window_seconds=RATE_LIMIT_WINDOW,
    )


def reset_login_rate(identifier: str) -> None:
    """Clear rate-limit state after a successful login."""
    _login_limiter.reset(f"login:{identifier}")


def check_signup_rate(ip_or_key: str = "global") -> bool:
    """Return ``True`` if the signup attempt is within rate limits."""
    return _signup_limiter.allow(
        f"signup:{ip_or_key}",
        max_requests=SIGNUP_RATE_LIMIT_MAX,
        window_seconds=RATE_LIMIT_WINDOW,
    )


# ─── Concurrent Session Limit ────────────────────────────────────────────────

def enforce_session_limit(user_id: int, conn) -> None:
    """
    If the user exceeds *MAX_SESSIONS_PER_USER*, invalidate the oldest
    sessions so only the newest ones survive.
    """
    rows = conn.execute(
        "SELECT id FROM sessions WHERE user_id = ? AND is_valid = 1 "
        "ORDER BY last_active_at DESC",
        (user_id,),
    ).fetchall()
    if len(rows) > MAX_SESSIONS_PER_USER:
        excess = [r["id"] for r in rows[MAX_SESSIONS_PER_USER:]]
        conn.executemany(
            "UPDATE sessions SET is_valid = 0 WHERE id = ?",
            [(sid,) for sid in excess],
        )
        _log.info(
            "Session limit enforced for user_id=%s — invalidated %d old session(s)",
            user_id, len(excess),
        )


# ─── Admin Action Guards ─────────────────────────────────────────────────────

def can_modify_user(admin_id: int, target_id: int) -> tuple[bool, str]:
    """Return ``(allowed, reason)`` — admins cannot deactivate/demote themselves."""
    if admin_id == target_id:
        return False, "You cannot modify your own account from the admin panel."
    return True, ""


# ─── Simulator Error Boundary ────────────────────────────────────────────────

def safe_run_simulator(run_fn, module_path: str, func_name: str):
    """
    Wrapper around the simulator dynamic loader.
    Catches all exceptions and returns ``(success: bool, error: str | None)``.
    """
    try:
        run_fn(module_path, func_name)
        return True, None
    except ModuleNotFoundError:
        msg = f"Simulator module not found: {module_path}"
        _log.error(msg)
        return False, msg
    except AttributeError:
        msg = f"Simulator function '{func_name}' not found in {module_path}"
        _log.error(msg)
        return False, msg
    except Exception as exc:
        msg = f"Simulator error ({module_path}): {exc}"
        _log.error(msg, exc_info=True)
        return False, str(exc)
