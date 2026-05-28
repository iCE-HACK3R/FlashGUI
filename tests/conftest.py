from __future__ import annotations

import importlib
import os
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture(scope="session")
def flashgui_source() -> str:
    return (ROOT / "flashgui.py").read_text(encoding="utf-8")


@pytest.fixture()
def fresh_flashgui_module() -> object:
    if "flashgui" in sys.modules:
        del sys.modules["flashgui"]
    mod = importlib.import_module("flashgui")
    yield mod


def load_flashgui_with_settings_path(settings_path: str) -> object:
    os.environ["FLASHGUI_SETTINGS_PATH"] = settings_path
    if "flashgui" in sys.modules:
        del sys.modules["flashgui"]
    return importlib.import_module("flashgui")
