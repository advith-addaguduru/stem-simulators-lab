"""
Unit tests for core.auth module.
"""

import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

from core.auth import (
    hash_password,
    verify_password,
    _validate_signup,
    signup,
    login,
    get_current_user,
    logout,
    logout_all,
    is_admin,
    is_teacher,
)


class TestPasswordFunctions:
    """Test password hashing and verification."""

    def test_hash_password(self):
        """Test password hashing."""
        hashed = hash_password("testpassword")
        assert isinstance(hashed, str)
        assert len(hashed) > 0
        assert hashed != "testpassword"

    def test_verify_password_correct(self):
        """Test correct password verification."""
        hashed = hash_password("testpassword")
        assert verify_password("testpassword", hashed) is True

    def test_verify_password_incorrect(self):
        """Test incorrect password verification."""
        hashed = hash_password("testpassword")
        assert verify_password("wrongpassword", hashed) is False


class TestValidateSignup:
    """Test signup validation."""

    @patch('core.auth.INPUT_MAX_USERNAME', 30)
    @patch('core.auth.INPUT_MAX_EMAIL', 254)
    @patch('core.auth.INPUT_MAX_DISPLAY_NAME', 100)
    @patch('core.auth.INPUT_MAX_PASSWORD', 128)
    def test_validate_signup_valid(self):
        """Test valid signup data."""
        errors = _validate_signup("testuser", "test@example.com", "Password123!", "Test User")
        assert errors == []

    def test_validate_signup_invalid_username(self):
        """Test invalid username."""
        errors = _validate_signup("123user", "test@example.com", "Password123!")
        assert len(errors) > 0
        assert any("Username" in err for err in errors)

    def test_validate_signup_invalid_email(self):
        """Test invalid email."""
        errors = _validate_signup("testuser", "invalid-email", "Password123!")
        assert len(errors) > 0
        assert any("email" in err.lower() for err in errors)

    def test_validate_signup_short_password(self):
        """Test too short password."""
        errors = _validate_signup("testuser", "test@example.com", "short")
        assert len(errors) > 0
        assert any("at least" in err for err in errors)

    @patch('core.auth.validate_password_strength')
    def test_validate_signup_weak_password(self, mock_validate):
        """Test weak password."""
        mock_validate.return_value = ["Password too weak"]
        errors = _validate_signup("testuser", "test@example.com", "weakpass")
        assert "Password too weak" in errors


class TestSignup:
    """Test user signup."""

    @patch('core.auth.get_db')
    @patch('core.auth._validate_signup')
    @patch('core.auth.hash_password')
    def test_signup_success(self, mock_hash, mock_validate, mock_get_db):
        """Test successful signup."""
        mock_validate.return_value = []
        mock_hash.return_value = "hashed_password"
        mock_conn = MagicMock()
        mock_conn.execute.return_value.lastrowid = 123
        mock_get_db.return_value.__enter__.return_value = mock_conn

        result = signup("testuser", "test@example.com", "password123")

        assert result["ok"] is True
        assert result["user_id"] == 123

    @patch('core.auth.get_db')
    @patch('core.auth._validate_signup')
    def test_signup_validation_errors(self, mock_validate, mock_get_db):
        """Test signup with validation errors."""
        mock_validate.return_value = ["Invalid username"]

        result = signup("invalid", "test@example.com", "password123")

        assert result["ok"] is False
        assert "Invalid username" in result["errors"]

    @patch('core.auth.get_db')
    @patch('core.auth._validate_signup')
    @patch('core.auth.hash_password')
    def test_signup_database_error(self, mock_hash, mock_validate, mock_get_db):
        """Test signup with database error."""
        mock_validate.return_value = []
        mock_hash.return_value = "hashed_password"
        mock_conn = MagicMock()
        mock_conn.execute.side_effect = Exception("UNIQUE constraint failed: users.username")
        mock_get_db.return_value.__enter__.return_value = mock_conn

        result = signup("testuser", "test@example.com", "password123")

        assert result["ok"] is False
        assert "already taken" in " ".join(result["errors"])


class TestLogin:
    """Test user login."""

    @patch('core.auth.get_db')
    @patch('core.auth.check_login_rate')
    @patch('core.auth.verify_password')
    @patch('core.auth.reset_login_rate')
    @patch('core.auth.enforce_session_limit')
    def test_login_success(self, mock_enforce, mock_reset, mock_verify, mock_rate, mock_get_db):
        """Test successful login."""
        mock_rate.return_value = True
        mock_verify.return_value = True

        mock_conn = MagicMock()
        mock_user = {
            'id': 1, 'username': 'testuser', 'email': 'test@example.com',
            'display_name': 'Test User', 'role': 'student', 'is_active': True,
            'failed_attempts': 0, 'locked_until': None, 'password_hash': 'hashed_password',
            'created_at': '2023-01-01'
        }
        mock_conn.execute.return_value.fetchone.return_value = mock_user
        mock_get_db.return_value.__enter__.return_value = mock_conn

        result = login("testuser", "password123")

        assert result["ok"] is True
        assert "session_id" in result
        assert result["user"]["username"] == "testuser"

    @patch('core.auth.get_db')
    @patch('core.auth.check_login_rate')
    def test_login_rate_limited(self, mock_rate, mock_get_db):
        """Test login rate limiting."""
        mock_rate.return_value = False

        result = login("testuser", "password123")

        assert result["ok"] is False
        assert "Too many" in result["error"]

    @patch('core.auth.get_db')
    @patch('core.auth.check_login_rate')
    def test_login_invalid_credentials(self, mock_rate, mock_get_db):
        """Test invalid credentials."""
        mock_rate.return_value = True
        mock_conn = MagicMock()
        mock_conn.execute.return_value.fetchone.return_value = None
        mock_get_db.return_value.__enter__.return_value = mock_conn

        result = login("testuser", "wrongpassword")

        assert result["ok"] is False
        assert "Invalid credentials" in result["error"]


class TestSessionManagement:
    """Test session management."""

    @patch('core.auth.get_db')
    def test_get_current_user_valid(self, mock_get_db):
        """Test getting current user with valid session."""
        mock_conn = MagicMock()
        mock_session = {
            'id': 'session123', 'user_id': 1, 'is_valid': 1, 'last_active_at': datetime.utcnow().isoformat(),
            'uid': 1, 'username': 'testuser', 'email': 'test@example.com',
            'display_name': 'Test User', 'role': 'student', 'is_active': True, 'created_at': '2023-01-01'
        }
        mock_conn.execute.return_value.fetchone.return_value = mock_session
        mock_get_db.return_value.__enter__.return_value = mock_conn

        user = get_current_user("session123")

        assert user is not None
        assert user["username"] == "testuser"

    @patch('core.auth.get_db')
    def test_get_current_user_invalid_session(self, mock_get_db):
        """Test getting current user with invalid session."""
        mock_conn = MagicMock()
        mock_conn.execute.return_value.fetchone.return_value = None
        mock_get_db.return_value.__enter__.return_value = mock_conn

        user = get_current_user("invalid_session")

        assert user is None

    @patch('core.auth.get_db')
    def test_logout(self, mock_get_db):
        """Test session logout."""
        mock_conn = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_conn

        logout("session123")

        mock_conn.execute.assert_called_once()


class TestRoleHelpers:
    """Test role checking functions."""

    def test_is_admin_admin_user(self):
        """Test admin user."""
        user = {"role": "admin"}
        assert is_admin(user) is True

    def test_is_admin_non_admin_user(self):
        """Test non-admin user."""
        user = {"role": "student"}
        assert is_admin(user) is False

    def test_is_admin_none_user(self):
        """Test None user."""
        assert is_admin(None) is False

    def test_is_teacher_teacher_user(self):
        """Test teacher user."""
        user = {"role": "teacher"}
        assert is_teacher(user) is True

    def test_is_teacher_admin_user(self):
        """Test admin user (also teacher)."""
        user = {"role": "admin"}
        assert is_teacher(user) is True

    def test_is_teacher_student_user(self):
        """Test student user."""
        user = {"role": "student"}
        assert is_teacher(user) is False