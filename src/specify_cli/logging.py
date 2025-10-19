"""Logging configuration for Spec-Kit."""

import logging
import os


def get_logger(name: str) -> logging.Logger:
    """Get configured logger for Spec-Kit modules.

    Args:
        name: Logger name (usually __name__)

    Returns:
        Configured logger instance
    """
    level = os.getenv("SPECKIT_LOG_LEVEL", "INFO").upper()
    logging.basicConfig(
        level=getattr(logging, level, logging.INFO),
        format="%(levelname)s %(name)s: %(message)s",
    )
    return logging.getLogger(name)
