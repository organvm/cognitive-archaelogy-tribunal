"""
Tests for the CLI argument surface.

Regression guard: the insecure ``--github-token`` argument was removed because
process arguments are visible in shell history and via ``ps``, leaking the
token. GitHub authentication is read from the ``GITHUB_TOKEN`` environment
variable instead (resolved inside ``GitHubClient``).
"""

import argparse
import importlib.util
from pathlib import Path

import pytest

MAIN_PATH = Path(__file__).resolve().parent.parent / "main.py"


def _load_main_module():
    spec = importlib.util.spec_from_file_location("_tribunal_main", MAIN_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _build_parser():
    """Rebuild the CLI parser the way main.py defines it, for surface assertions."""
    try:
        module = _load_main_module()
    except ImportError:
        pytest.skip("optional runtime deps for main.py not installed; source guard still applies")
    build = getattr(module, "build_parser", None)
    if build is not None:
        return build()
    pytest.skip("main.py does not expose build_parser(); source-level guard covers this")


def test_github_token_cli_argument_is_removed_from_source():
    source = MAIN_PATH.read_text()
    assert "add_argument('--github-token'" not in source, "insecure --github-token CLI arg must not return"
    assert 'add_argument("--github-token"' not in source, "insecure --github-token CLI arg must not return"
    assert "args.github_token" not in source, "token must come from GITHUB_TOKEN env, not argparse"
    assert "os.environ.get('GITHUB_TOKEN')" in source or 'os.environ.get("GITHUB_TOKEN")' in source


def test_github_token_flag_is_rejected_by_parser():
    parser = _build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["--github-token", "ghp_should_not_exist"])
