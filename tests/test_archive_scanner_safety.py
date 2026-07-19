"""
Tests for ArchiveScanner sensitive-directory guardrail.

Distills the Sentinel PR cluster (#16, #21, #28, #30, #38, #42, #51, #54, #57,
#64, #67, #71, #73, #111, #113): the scanner must refuse to descend into
sensitive system/credential directories and must not be traversable into them.
"""

import os
import tempfile
from pathlib import Path

import pytest

from cognitive_tribunal.modules.archive_scanner import ArchiveScanner


@pytest.fixture
def scanner():
    return ArchiveScanner()


@pytest.mark.parametrize("unsafe", ["/", "/etc", "/proc", "/sys", "/boot", "/dev", "/run"])
def test_system_roots_are_unsafe(scanner, unsafe):
    assert scanner.is_safe_scan_target(unsafe) is False


def test_path_inside_etc_is_unsafe(scanner):
    assert scanner.is_safe_scan_target("/etc/ssh") is False


def test_home_credential_dirs_are_unsafe(scanner):
    home = Path.home()
    assert scanner.is_safe_scan_target(str(home / ".ssh")) is False
    assert scanner.is_safe_scan_target(str(home / ".aws" / "credentials")) is False


def test_ordinary_temp_dir_is_safe(scanner):
    with tempfile.TemporaryDirectory() as tmp:
        assert scanner.is_safe_scan_target(tmp) is True


def test_scan_directory_refuses_sensitive_root(scanner):
    # /etc exists on POSIX hosts; skip cleanly where it does not.
    if not Path("/etc").is_dir():
        pytest.skip("/etc not present on this host")
    result = scanner.scan_directory("/etc")
    assert "error" in result
    assert "sensitive" in result["error"].lower()


def test_scan_directory_allows_ordinary_dir(scanner):
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "note.txt").write_text("hello")
        result = scanner.scan_directory(tmp)
        assert "error" not in result


def test_symlink_into_etc_is_not_followed(scanner):
    if not Path("/etc").is_dir():
        pytest.skip("/etc not present on this host")
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "real.txt").write_text("keep")
        link = Path(tmp) / "escape"
        try:
            os.symlink("/etc", link)
        except (OSError, NotImplementedError):
            pytest.skip("symlinks unsupported on this host")
        result = scanner.scan_directory(tmp)
        assert "error" not in result
        # The scan completed without traversing the symlink into /etc.
        for meta in scanner.scanned_files:
            resolved = str(Path(meta.get("path", "")).resolve())
            assert not resolved.startswith(str(Path("/etc").resolve()))
