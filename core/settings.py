"""
STEM Lab — Application Settings
================================
Centralised configuration loaded from environment variables / .env file.
"""

import os
from pathlib import Path

# ─── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# ─── Database ─────────────────────────────────────────────────────────────────
DATABASE_URL = os.getenv("STEMLAB_DATABASE_URL", str(DATA_DIR / "stemlab.db"))

# ─── Security ─────────────────────────────────────────────────────────────────
SECRET_KEY = os.getenv("STEMLAB_SECRET_KEY", "change-me-in-production")
# bcrypt rounds
BCRYPT_ROUNDS = int(os.getenv("STEMLAB_BCRYPT_ROUNDS", "12"))
# Session idle timeout (seconds) — default 30 min
SESSION_TIMEOUT_SECONDS = int(os.getenv("STEMLAB_SESSION_TIMEOUT", "1800"))
# Maximum failed login attempts before temporary lock
MAX_LOGIN_ATTEMPTS = int(os.getenv("STEMLAB_MAX_LOGIN_ATTEMPTS", "5"))
# Lock duration after max failed attempts (seconds) — default 15 min
LOGIN_LOCK_SECONDS = int(os.getenv("STEMLAB_LOGIN_LOCK_SECONDS", "900"))

# ─── Roles ────────────────────────────────────────────────────────────────────
ROLE_STUDENT = "student"
ROLE_TEACHER = "teacher"
ROLE_ADMIN = "admin"
ROLES = [ROLE_STUDENT, ROLE_TEACHER, ROLE_ADMIN]

# ─── Logging ──────────────────────────────────────────────────────────────────
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_LEVEL = os.getenv("STEMLAB_LOG_LEVEL", "INFO")
LOG_FILE = str(LOG_DIR / "stemlab.log")
AUDIT_LOG_FILE = str(LOG_DIR / "audit.log")

# ─── Guardrails ───────────────────────────────────────────────────────────
# Rate limiting (sliding window)
RATE_LIMIT_WINDOW = int(os.getenv("STEMLAB_RATE_LIMIT_WINDOW", "60"))          # seconds
RATE_LIMIT_MAX_REQUESTS = int(os.getenv("STEMLAB_RATE_LIMIT_MAX_LOGIN", "10")) # per window
SIGNUP_RATE_LIMIT_MAX = int(os.getenv("STEMLAB_RATE_LIMIT_MAX_SIGNUP", "5"))   # per window
# Concurrent sessions per user
MAX_SESSIONS_PER_USER = int(os.getenv("STEMLAB_MAX_SESSIONS", "3"))
# Input length limits
INPUT_MAX_USERNAME = 30
INPUT_MAX_EMAIL = 254
INPUT_MAX_DISPLAY_NAME = 100
INPUT_MAX_PASSWORD = 128
INPUT_MAX_SEARCH = 200
# Password complexity
PASSWORD_REQUIRE_UPPER = os.getenv("STEMLAB_PW_REQUIRE_UPPER", "1") == "1"
PASSWORD_REQUIRE_LOWER = os.getenv("STEMLAB_PW_REQUIRE_LOWER", "1") == "1"
PASSWORD_REQUIRE_DIGIT = os.getenv("STEMLAB_PW_REQUIRE_DIGIT", "1") == "1"
PASSWORD_REQUIRE_SPECIAL = os.getenv("STEMLAB_PW_REQUIRE_SPECIAL", "0") == "1"

# ─── App Metadata ─────────────────────────────────────────────────────────
APP_NAME = "STEM Lab"
APP_VERSION = "5.2"
APP_TAGLINE = "Interactive Science & Mathematics Simulators"
SUPPORT_EMAIL = os.getenv("STEMLAB_SUPPORT_EMAIL", "support@stemlab.example.com")
