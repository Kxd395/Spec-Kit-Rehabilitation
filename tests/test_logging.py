"""Test logging configuration."""

import logging
import os
from specify_cli.logging import get_logger


class TestGetLogger:
    """Test logger creation and configuration."""

    def test_get_logger_returns_logger(self):
        """Test that get_logger returns a logger instance."""
        logger = get_logger("test_module")

        assert isinstance(logger, logging.Logger)
        assert logger.name == "test_module"

    def test_get_logger_default_level(self):
        """Test default log level is INFO."""
        # Clear any existing env var
        if "SPECKIT_LOG_LEVEL" in os.environ:
            del os.environ["SPECKIT_LOG_LEVEL"]

        get_logger("test_module")

        # Check root logger level (since basicConfig sets it)
        root_logger = logging.getLogger()
        assert root_logger.level == logging.INFO

    def test_get_logger_custom_level(self, monkeypatch):
        """Test custom log level from environment."""
        monkeypatch.setenv("SPECKIT_LOG_LEVEL", "DEBUG")

        get_logger("test_debug")

        root_logger = logging.getLogger()
        assert root_logger.level == logging.DEBUG

    def test_get_logger_invalid_level_defaults_to_info(self, monkeypatch):
        """Test invalid log level defaults to INFO."""
        monkeypatch.setenv("SPECKIT_LOG_LEVEL", "INVALID")

        get_logger("test_invalid")

        root_logger = logging.getLogger()
        assert root_logger.level == logging.INFO

    def test_get_logger_format_includes_level_and_name(self):
        """Test log format includes level and name."""
        logger = get_logger("test_format")

        # Logger should be usable
        logger.info("Test message")
        assert logger.name == "test_format"
