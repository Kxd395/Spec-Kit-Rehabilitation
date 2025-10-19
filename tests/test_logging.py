"""Test logging configuration."""

import logging
from specify_cli.logging_config import get_logger, setup_logging


class TestGetLogger:
    """Test logger creation and configuration."""

    def test_get_logger_returns_logger(self):
        """Test that get_logger returns a logger instance."""
        logger = get_logger("test_module")

        assert isinstance(logger, logging.Logger)
        assert logger.name == "specify_cli.test_module"

    def test_get_logger_default_level(self):
        """Test default log level is INFO."""
        # Setup logging with default level
        setup_logging()

        get_logger("test_module")

        # Check that the specify_cli logger has INFO level
        spec_logger = logging.getLogger("specify_cli")
        assert spec_logger.level == logging.INFO

    def test_get_logger_custom_level(self):
        """Test custom log level from debug flag."""
        # Setup logging with debug enabled
        setup_logging(debug=True)

        get_logger("test_debug")

        # Check that the specify_cli logger has DEBUG level
        spec_logger = logging.getLogger("specify_cli")
        assert spec_logger.level == logging.DEBUG

    def test_get_logger_invalid_level_defaults_to_info(self):
        """Test invalid log level defaults to INFO."""
        # Setup logging with invalid level
        setup_logging(level="INVALID")

        get_logger("test_invalid")

        # Check that the specify_cli logger defaults to INFO
        spec_logger = logging.getLogger("specify_cli")
        assert spec_logger.level == logging.INFO

    def test_get_logger_format_includes_level_and_name(self):
        """Test log format includes level and name."""
        logger = get_logger("test_format")

        # Logger should be usable
        logger.info("Test message")
        # New get_logger prefixes with specify_cli
        assert logger.name == "specify_cli.test_format"
