"""
Tests for the empty-state welcome panel.

Distills the Palette empty-state PR cluster (#37, #55, #59, #61, #65, #66, #69,
#74, #108, #110, #112): running the CLI with no module selected should greet the
user with copy-pasteable examples, not a bare argparse error.
"""

import io

from rich.console import Console

import importlib.util
from pathlib import Path

MAIN_PATH = Path(__file__).resolve().parent.parent / "main.py"


def _load_main():
    spec = importlib.util.spec_from_file_location("cat_main_welcome", MAIN_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_welcome_body_lists_examples():
    module = _load_main()
    body = module.welcome_body()
    assert "--all" in body
    assert "--scan-archives" in body
    assert "--help" in body
    # Every declared example command appears in the body.
    for _label, cmd in module.WELCOME_EXAMPLES:
        assert cmd in body


def test_render_welcome_emits_panel():
    module = _load_main()
    buffer = io.StringIO()
    module.render_welcome(Console(file=buffer, width=100))
    out = buffer.getvalue()
    assert "COGNITIVE ARCHAEOLOGY TRIBUNAL" in out
    assert "python main.py --all" in out
