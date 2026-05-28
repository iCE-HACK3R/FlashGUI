from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _settings_page_source() -> str:
    source = (ROOT / "flashgui.py").read_text(encoding="utf-8")
    start = source.index("class SettingsPage(PageBase):")
    end = source.index("class ToolsPage(PageBase):")
    return source[start:end]


def _legacy_settings_page_source() -> str:
    source = (ROOT / "flashgui_legacy.py").read_text(encoding="utf-8")
    start = source.index("class PageSettings:")
    end = source.index("class AppState:")
    return source[start:end]


def test_settings_background_runner_uses_qt_worker_pipeline() -> None:
    src = _settings_page_source()
    assert "w = Worker(_worker)" in src
    assert "w.signals.finished.connect(on_done)" in src
    assert "threading.Thread(target=_entry" not in src


def test_settings_check_permissions_is_non_mutating() -> None:
    src = _settings_page_source()
    start = src.index("def _check_binary_perms(self) -> None:")
    end = src.index("def _fix_binary_perms(self) -> None:")
    check_src = src[start:end]
    assert "chmod" not in check_src
    assert "self._sudo_run(" not in check_src


def test_settings_fix_permissions_covers_all_core_tools() -> None:
    src = _settings_page_source()
    start = src.index("def _fix_binary_perms(self) -> None:")
    end = src.index("def _download_binaries(self) -> None:")
    fix_src = src[start:end]

    for name in ("flashrom", "flashprog", "minipro", "fwinfo"):
        assert f'("{name}",' in fix_src

    assert "self._sudo_run([\"chmod\", \"+x\", path])" in fix_src


def test_settings_refresh_disables_platform_inapplicable_buttons() -> None:
    src = _settings_page_source()
    start = src.index("def _refresh_system_fix_buttons(self) -> None:")
    end = src.index("@staticmethod\n    def _merge_font_candidates")
    refresh_src = src[start:end]

    assert "self.btn_check_perms.setEnabled(not is_windows)" in refresh_src
    assert "self.btn_fix_perms.setEnabled(not is_windows)" in refresh_src
    assert "self.btn_check_udev.setEnabled(is_linux)" in refresh_src
    assert "self.btn_fix_udev.setEnabled(is_linux)" in refresh_src


def test_legacy_settings_check_permissions_is_non_mutating() -> None:
    src = _legacy_settings_page_source()
    start = src.index("def _check_binary_perms(self) -> None:")
    end = src.index("def _fix_binary_perms(self) -> None:")
    check_src = src[start:end]
    assert "chmod" not in check_src
    assert "self._sudo_run(" not in check_src


def test_legacy_settings_fix_permissions_covers_all_core_tools() -> None:
    src = _legacy_settings_page_source()
    start = src.index("def _fix_binary_perms(self) -> None:")
    end = src.index("def _check_udev(self) -> None:")
    fix_src = src[start:end]

    for name in ("flashrom", "flashprog", "minipro", "fwinfo"):
        assert f'("{name}",' in fix_src

    assert "self._sudo_run([\"chmod\", \"+x\", path])" in fix_src


def test_legacy_settings_refresh_disables_platform_inapplicable_buttons() -> None:
    src = _legacy_settings_page_source()
    start = src.index("def _refresh_system_fix_buttons(self) -> None:")
    end = src.index("def _fix_dependencies(self) -> None:")
    refresh_src = src[start:end]

    assert "self.btn_check_perms.config(state=\"disabled\" if is_windows else \"normal\")" in refresh_src
    assert "self.btn_fix_perms.config(state=\"disabled\" if is_windows else \"normal\")" in refresh_src
    assert "self.btn_check_udev.config(state=\"normal\" if is_linux else \"disabled\")" in refresh_src
    assert "self.btn_fix_udev.config(state=\"normal\" if is_linux else \"disabled\")" in refresh_src
