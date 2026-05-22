from __future__ import annotations

import py_compile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_main_script_compiles() -> None:
    py_compile.compile(str(ROOT / "flashgui.py"), doraise=True)


def test_legacy_script_compiles() -> None:
    py_compile.compile(str(ROOT / "flashgui_legacy.py"), doraise=True)
