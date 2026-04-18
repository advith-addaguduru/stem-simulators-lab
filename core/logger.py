"""
STEM Lab — Logging Configuration
==================================
Rotating file + console handlers with structured formatting.
"""

import logging
from logging.handlers import RotatingFileHandler

from core.settings import LOG_LEVEL, LOG_FILE, AUDIT_LOG_FILE

_FMT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
_DATE_FMT = "%Y-%m-%d %H:%M:%S"

_formatter = logging.Formatter(_FMT, datefmt=_DATE_FMT)


def _rotating_handler(path: str, max_bytes: int = 5_000_000, backup: int = 3):
    h = RotatingFileHandler(path, maxBytes=max_bytes, backupCount=backup, encoding="utf-8")
    h.setFormatter(_formatter)
    return h


def get_logger(name: str = "stemlab") -> logging.Logger:
    """Return a configured application logger."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))
        logger.addHandler(_rotating_handler(LOG_FILE))
        console = logging.StreamHandler()
        console.setFormatter(_formatter)
        logger.addHandler(console)
    return logger


def get_audit_logger() -> logging.Logger:
    """Return a logger dedicated to the audit trail file."""
    logger = logging.getLogger("stemlab.audit")
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        logger.addHandler(_rotating_handler(AUDIT_LOG_FILE))
    return logger
