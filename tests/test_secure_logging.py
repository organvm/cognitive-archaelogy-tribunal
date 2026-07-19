"""
Tests for secure error logging.

Distills Sentinel PR #60 ("Fix error handling information leakage"): detailed
error text must go to the audit-log file, not leak to the console via raw
exception messages.
"""

import logging
from pathlib import Path

from cognitive_tribunal.utils.logging_utils import get_audit_logger


def test_audit_logger_writes_detail_to_file(tmp_path, capsys):
    log_path = tmp_path / "audit.log"
    logger = get_audit_logger(name=f"test_{tmp_path.name}", log_path=str(log_path))
    logger.error("boom: %s", "secret-internal-detail")
    for handler in logger.handlers:
        handler.flush()

    contents = log_path.read_text()
    assert "secret-internal-detail" in contents

    # Nothing leaked to stdout/stderr.
    captured = capsys.readouterr()
    assert "secret-internal-detail" not in captured.out
    assert "secret-internal-detail" not in captured.err


def test_github_utils_does_not_print_raw_exceptions():
    source = (
        Path(__file__).resolve().parent.parent
        / "cognitive_tribunal" / "utils" / "github_utils.py"
    ).read_text()
    assert 'print(f"Error fetching' not in source
    assert "get_audit_logger" in source


def test_main_console_error_messages_do_not_interpolate_exception():
    source = (Path(__file__).resolve().parent.parent / "main.py").read_text()
    # The console-facing error lines must not embed the raw exception object.
    assert "Error analyzing personal repos: {e}" not in source
    assert "Error analyzing org repos: {e}" not in source
    assert "details in audit.log" in source
