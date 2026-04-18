"""
Unit tests for core.guardrails module.
"""

import pytest
from unittest.mock import patch, MagicMock

from core.guardrails import (
    sanitize_text,
    sanitize_log,
    check_length,
    validate_password_strength,
    check_login_rate,
    reset_login_rate,
    check_signup_rate,
    can_modify_user,
    safe_run_simulator,
)


class TestSanitizeText:
    """Test text sanitization functions."""

    def test_sanitize_text_basic(self):
        """Test basic text sanitization."""
        assert sanitize_text("  hello world  ") == "hello world"
        assert sanitize_text("hello<script>alert('xss')</script>") == "hello&lt;script&gt;alert(&#x27;xss&#x27;)&lt;/script&gt;"

    def test_sanitize_text_max_length(self):
        """Test max length enforcement."""
        long_text = "a" * 1000
        result = sanitize_text(long_text, max_length=100)
        assert len(result) == 100
        assert result == "a" * 100

    def test_sanitize_text_strip_html_false(self):
        """Test with HTML stripping disabled."""
        result = sanitize_text("<b>bold</b>", strip_html=False)
        assert result == "<b>bold</b>"

    def test_sanitize_text_control_chars(self):
        """Test control character removal."""
        result = sanitize_text("hello\x00world\x1f")
        assert result == "helloworld"


class TestSanitizeLog:
    """Test log sanitization."""

    def test_sanitize_log_newlines(self):
        """Test newline replacement."""
        assert sanitize_log("line1\nline2\r\nline3") == "line1\\nline2\\r\\nline3"

    def test_sanitize_log_control_chars(self):
        """Test control character removal."""
        assert sanitize_log("hello\x00world") == "helloworld"


class TestCheckLength:
    """Test length validation."""

    def test_check_length_valid(self):
        """Test valid length."""
        assert check_length("hello", "Test", 10) is None

    def test_check_length_too_long(self):
        """Test length exceeded."""
        result = check_length("a" * 20, "Test", 10)
        assert result == "Test must be at most 10 characters."


class TestValidatePasswordStrength:
    """Test password strength validation."""

    @patch('core.guardrails.PASSWORD_REQUIRE_UPPER', True)
    @patch('core.guardrails.PASSWORD_REQUIRE_LOWER', True)
    @patch('core.guardrails.PASSWORD_REQUIRE_DIGIT', True)
    @patch('core.guardrails.PASSWORD_REQUIRE_SPECIAL', False)
    def test_validate_password_strength_all_requirements(self):
        """Test password with all requirements."""
        errors = validate_password_strength("Password123")
        assert errors == []

    @patch('core.guardrails.PASSWORD_REQUIRE_UPPER', True)
    @patch('core.guardrails.PASSWORD_REQUIRE_LOWER', True)
    @patch('core.guardrails.PASSWORD_REQUIRE_DIGIT', True)
    @patch('core.guardrails.PASSWORD_REQUIRE_SPECIAL', False)
    def test_validate_password_strength_missing_upper(self):
        """Test password missing uppercase."""
        errors = validate_password_strength("password123")
        assert "uppercase letter" in " ".join(errors)

    @patch('core.guardrails.PASSWORD_REQUIRE_UPPER', True)
    @patch('core.guardrails.PASSWORD_REQUIRE_LOWER', True)
    @patch('core.guardrails.PASSWORD_REQUIRE_DIGIT', True)
    @patch('core.guardrails.PASSWORD_REQUIRE_SPECIAL', False)
    def test_validate_password_strength_missing_lower(self):
        """Test password missing lowercase."""
        errors = validate_password_strength("PASSWORD123")
        assert "lowercase letter" in " ".join(errors)

    @patch('core.guardrails.PASSWORD_REQUIRE_UPPER', True)
    @patch('core.guardrails.PASSWORD_REQUIRE_LOWER', True)
    @patch('core.guardrails.PASSWORD_REQUIRE_DIGIT', True)
    @patch('core.guardrails.PASSWORD_REQUIRE_SPECIAL', False)
    def test_validate_password_strength_missing_digit(self):
        """Test password missing digit."""
        errors = validate_password_strength("Password")
        assert "digit" in " ".join(errors)


class TestRateLimiting:
    """Test rate limiting functions."""

    def test_check_login_rate(self):
        """Test login rate limiting."""
        # First few calls should succeed
        assert check_login_rate("test@example.com") is True
        assert check_login_rate("test@example.com") is True

    def test_reset_login_rate(self):
        """Test resetting login rate."""
        reset_login_rate("test@example.com")
        # Should work after reset
        assert check_login_rate("test@example.com") is True

    def test_check_signup_rate(self):
        """Test signup rate limiting."""
        assert check_signup_rate("127.0.0.1") is True


class TestCanModifyUser:
    """Test admin action guards."""

    def test_can_modify_user_different_users(self):
        """Test modifying different user."""
        allowed, reason = can_modify_user(1, 2)
        assert allowed is True
        assert reason == ""

    def test_can_modify_user_same_user(self):
        """Test modifying own account."""
        allowed, reason = can_modify_user(1, 1)
        assert allowed is False
        assert "own account" in reason


class TestSafeRunSimulator:
    """Test simulator error boundary."""

    def test_safe_run_simulator_success(self):
        """Test successful simulator run."""
        def mock_run(module, func):
            pass  # Success

        success, error = safe_run_simulator(mock_run, "test.module", "simulate")
        assert success is True
        assert error is None

    def test_safe_run_simulator_module_not_found(self):
        """Test module not found error."""
        def mock_run(module, func):
            raise ModuleNotFoundError("No module")

        success, error = safe_run_simulator(mock_run, "test.module", "simulate")
        assert success is False
        assert "not found" in error

    def test_safe_run_simulator_attribute_error(self):
        """Test function not found error."""
        def mock_run(module, func):
            raise AttributeError("No function")

        success, error = safe_run_simulator(mock_run, "test.module", "simulate")
        assert success is False
        assert "not found" in error

    def test_safe_run_simulator_generic_error(self):
        """Test generic simulator error."""
        def mock_run(module, func):
            raise ValueError("Test error")

        success, error = safe_run_simulator(mock_run, "test.module", "simulate")
        assert success is False
        assert error == "Test error"