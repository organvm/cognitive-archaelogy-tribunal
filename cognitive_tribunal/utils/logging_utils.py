"""Audit logging helper.

Routes detailed error information to a log file instead of leaking it to the
console via raw exception messages (distills Sentinel PR #60: "Fix error
handling information leakage"). Raw exception text can expose internal paths,
API structure, or tokens embedded in URLs; the console should show a generic
message while the full detail lands in the audit log for the operator.
"""

import logging
from pathlib import Path

DEFAULT_AUDIT_LOG = "audit.log"


def get_audit_logger(name: str = "cognitive_tribunal", log_path=None) -> logging.Logger:
    """Return a logger that writes detailed records to an audit-log file.

    The logger does not propagate to the root logger, so configuring it never
    causes exception detail to be echoed to the console.
    """
    logger = logging.getLogger(name)
    if not any(isinstance(h, logging.FileHandler) for h in logger.handlers):
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(Path(log_path or DEFAULT_AUDIT_LOG))
        handler.setFormatter(
            logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
        )
        logger.addHandler(handler)
        logger.propagate = False
    return logger
