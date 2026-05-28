from __future__ import annotations

import importlib
import json
import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _qt_settings_source(src: str) -> str:
    start = src.index("class SettingsPage(PageBase):")
    end = src.index("class ToolsPage(PageBase):")
    return src[start:end]


def _method_block(src: str, start_marker: str, end_marker: str) -> str:
    start = src.index(start_marker)
    end = src.index(end_marker)
    return src[start:end]


def _load_module_with_settings_path(settings_path: Path):
    os.environ["FLASHGUI_SETTINGS_PATH"] = str(settings_path)
    if "flashgui" in sys.modules:
        del sys.modules["flashgui"]
    return importlib.import_module("flashgui")


def test_b1_save_to_file_contains_expected_keys(flashgui_source: str) -> None:
    src = _qt_settings_source(flashgui_source)
    body = _method_block(src, "def _save_to_file(self) -> None:", "def _populate_from_dict(self, data: dict[str, object]) -> None:")

    expected = {
        '"preferred_font"',
        '"font_size"',
        '"flashrom_bin"',
        '"flashprog_bin"',
        '"workspace_dir"',
        '"window_geometry"',
        '"log_file_path"',
        '"use_sudo"',
        '"auto_detect_programmer"',
        '"theme"',
        '"layout_mode"',
        '"beep_on_complete"',
    }
    for key in expected:
        assert key in body


def test_b2_load_populates_mapped_controls(flashgui_source: str) -> None:
    src = _qt_settings_source(flashgui_source)
    body = _method_block(src, "def _populate_from_dict(self, data: dict[str, object]) -> None:", "def _reset_defaults(self) -> None:")

    assert "self.font_combo.setCurrentText(font)" in body
    assert "self.font_size_slider.setValue" in body
    assert "self.flashrom_edit.setText" in body
    assert "self.flashprog_edit.setText" in body
    assert "self.workspace_edit.setText" in body
    assert "self.log_file_edit.setText" in body
    assert "self.use_sudo.setChecked" in body
    assert "self.auto_detect.setChecked" in body
    assert "self.beep.setChecked" in body
    assert "self.theme_combo.setCurrentText(theme)" in body


def test_b3_boolean_string_tolerance() -> None:
    import flashgui

    assert flashgui._as_bool("false", True) is False
    assert flashgui._as_bool("true", False) is True
    assert flashgui._as_bool("off", True) is False


def test_c1_tab_mode_persists_across_reload(tmp_path: Path) -> None:
    settings_path = tmp_path / "settings.json"
    mod = _load_module_with_settings_path(settings_path)

    state = mod.AppState()
    state.layout_mode = "tab"
    state.save_settings(geometry="800x600")

    mod = _load_module_with_settings_path(settings_path)
    reloaded = mod.AppState()
    assert reloaded.layout_mode == "tab"


def test_c2_sidebar_mode_persists_across_reload(tmp_path: Path) -> None:
    settings_path = tmp_path / "settings.json"
    mod = _load_module_with_settings_path(settings_path)

    state = mod.AppState()
    state.layout_mode = "sidebar"
    state.save_settings(geometry="1024x768")

    mod = _load_module_with_settings_path(settings_path)
    reloaded = mod.AppState()
    assert reloaded.layout_mode == "sidebar"


def test_c_layout_invalid_value_normalizes_to_sidebar(tmp_path: Path) -> None:
    settings_path = tmp_path / "settings.json"
    settings_path.write_text(json.dumps({"layout_mode": "banana"}), encoding="utf-8")

    mod = _load_module_with_settings_path(settings_path)
    state = mod.AppState()
    assert state.layout_mode == "sidebar"


def test_e5_ft232h_divisor_persists_across_reload(tmp_path: Path) -> None:
    settings_path = tmp_path / "settings.json"
    mod = _load_module_with_settings_path(settings_path)

    state = mod.AppState()
    state.ft232h_divisor = "2"
    state.save_settings(geometry="900x700")

    mod = _load_module_with_settings_path(settings_path)
    reloaded = mod.AppState()
    assert reloaded.ft232h_divisor == "2"
