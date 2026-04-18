"""
Unit tests for core.settings module.
"""

import os
from pathlib import Path
from unittest.mock import patch

from core.settings import (
    BASE_DIR,
    DATA_DIR,
    DATABASE_URL,
    SECRET_KEY,
    BCRYPT_ROUNDS,
    SESSION_TIMEOUT_SECONDS,
    MAX_LOGIN_ATTEMPTS,
    LOGIN_LOCK_SECONDS,
    ROLES,
    ROLE_STUDENT,
    ROLE_TEACHER,
    ROLE_ADMIN,
    LOG_DIR,
    LOG_LEVEL,
    LOG_FILE,
    AUDIT_LOG_FILE,
    RATE_LIMIT_WINDOW,
    RATE_LIMIT_MAX_REQUESTS,
    SIGNUP_RATE_LIMIT_MAX,
    MAX_SESSIONS_PER_USER,
    INPUT_MAX_USERNAME,
    INPUT_MAX_EMAIL,
    INPUT_MAX_DISPLAY_NAME,
    INPUT_MAX_PASSWORD,
    INPUT_MAX_SEARCH,
    PASSWORD_REQUIRE_UPPER,
    PASSWORD_REQUIRE_LOWER,
    PASSWORD_REQUIRE_DIGIT,
    PASSWORD_REQUIRE_SPECIAL,
    APP_NAME,
    APP_VERSION,
    APP_TAGLINE,
    SUPPORT_EMAIL,
)


class TestPaths:
    """Test path configurations."""

    def test_base_dir_exists(self):
        """Test BASE_DIR exists."""
        assert BASE_DIR.exists()
        assert BASE_DIR.is_dir()

    def test_data_dir_exists(self):
        """Test DATA_DIR exists."""
        assert DATA_DIR.exists()
        assert DATA_DIR.is_dir()
        assert DATA_DIR.name == "data"

    def test_log_dir_exists(self):
        """Test LOG_DIR exists."""
        assert LOG_DIR.exists()
        assert LOG_DIR.is_dir()
        assert LOG_DIR.name == "logs"


class TestDatabaseSettings:
    """Test database configuration."""

    @patch.dict(os.environ, {}, clear=True)
    def test_database_url_default(self):
        """Test default database URL."""
        # Reload module to get fresh settings
        import importlib
        import core.settings
        importlib.reload(core.settings)
        from core.settings import DATABASE_URL as db_url

        expected = str(core.settings.DATA_DIR / "stemlab.db")
        assert db_url == expected


class TestSecuritySettings:
    """Test security-related settings."""

    @patch.dict(os.environ, {}, clear=True)
    def test_secret_key_default(self):
        """Test default secret key."""
        import importlib
        import core.settings
        importlib.reload(core.settings)
        from core.settings import SECRET_KEY as sk

        assert sk == "change-me-in-production"

    @patch.dict(os.environ, {"STEMLAB_BCRYPT_ROUNDS": "14"})
    def test_bcrypt_rounds_env(self):
        """Test bcrypt rounds from environment."""
        import importlib
        import core.settings
        importlib.reload(core.settings)
        from core.settings import BCRYPT_ROUNDS as br

        assert br == 14

    @patch.dict(os.environ, {}, clear=True)
    def test_session_timeout_default(self):
        """Test default session timeout."""
        import importlib
        import core.settings
        importlib.reload(core.settings)
        from core.settings import SESSION_TIMEOUT_SECONDS as sts

        assert sts == 1800  # 30 minutes

    @patch.dict(os.environ, {}, clear=True)
    def test_max_login_attempts_default(self):
        """Test default max login attempts."""
        import importlib
        import core.settings
        importlib.reload(core.settings)
        from core.settings import MAX_LOGIN_ATTEMPTS as mla

        assert mla == 5

    @patch.dict(os.environ, {}, clear=True)
    def test_login_lock_seconds_default(self):
        """Test default login lock duration."""
        import importlib
        import core.settings
        importlib.reload(core.settings)
        from core.settings import LOGIN_LOCK_SECONDS as lls

        assert lls == 900  # 15 minutes


class TestRoles:
    """Test role definitions."""

    def test_roles_list(self):
        """Test roles list contains expected values."""
        assert ROLE_STUDENT in ROLES
        assert ROLE_TEACHER in ROLES
        assert ROLE_ADMIN in ROLES
        assert len(ROLES) == 3

    def test_role_constants(self):
        """Test role constant values."""
        assert ROLE_STUDENT == "student"
        assert ROLE_TEACHER == "teacher"
        assert ROLE_ADMIN == "admin"


class TestLoggingSettings:
    """Test logging configuration."""

    @patch.dict(os.environ, {}, clear=True)
    def test_log_level_default(self):
        """Test default log level."""
        import importlib
        import core.settings
        importlib.reload(core.settings)
        from core.settings import LOG_LEVEL as ll

        assert ll == "INFO"

    def test_log_file_path(self):
        """Test log file path construction."""
        assert LOG_FILE.endswith("stemlab.log")
        assert "logs" in LOG_FILE

    def test_audit_log_file_path(self):
        """Test audit log file path construction."""
        assert AUDIT_LOG_FILE.endswith("audit.log")
        assert "logs" in AUDIT_LOG_FILE


class TestGuardrailsSettings:
    """Test guardrails configuration."""

    @patch.dict(os.environ, {}, clear=True)
    def test_rate_limit_defaults(self):
        """Test rate limiting defaults."""
        import importlib
        import core.settings
        importlib.reload(core.settings)
        from core.settings import (
            RATE_LIMIT_WINDOW as rlw,
            RATE_LIMIT_MAX_REQUESTS as rlmr,
            SIGNUP_RATE_LIMIT_MAX as srlm
        )

        assert rlw == 60
        assert rlmr == 10
        assert srlm == 5

    def test_max_sessions_default(self):
        """Test max sessions per user."""
        assert MAX_SESSIONS_PER_USER == 3

    def test_input_limits(self):
        """Test input length limits."""
        assert INPUT_MAX_USERNAME == 30
        assert INPUT_MAX_EMAIL == 254
        assert INPUT_MAX_DISPLAY_NAME == 100
        assert INPUT_MAX_PASSWORD == 128
        assert INPUT_MAX_SEARCH == 200

    @patch.dict(os.environ, {}, clear=True)
    def test_password_requirements_defaults(self):
        """Test password requirement defaults."""
        import importlib
        import core.settings
        importlib.reload(core.settings)
        from core.settings import (
            PASSWORD_REQUIRE_UPPER as pru,
            PASSWORD_REQUIRE_LOWER as prl,
            PASSWORD_REQUIRE_DIGIT as prd,
            PASSWORD_REQUIRE_SPECIAL as prs
        )

        assert pru is True
        assert prl is True
        assert prd is True
        assert prs is False


class TestAppMetadata:
    """Test application metadata."""

    def test_app_constants(self):
        """Test app metadata constants."""
        assert APP_NAME == "STEM Lab"
        assert APP_VERSION == "5.2"
        assert APP_TAGLINE == "Interactive Science & Mathematics Simulators"

    @patch.dict(os.environ, {}, clear=True)
    def test_support_email_default(self):
        """Test default support email."""
        import importlib
        import core.settings
        importlib.reload(core.settings)
        from core.settings import SUPPORT_EMAIL as se

        assert se == "support@stemlab.example.com"