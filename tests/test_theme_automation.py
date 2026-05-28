from __future__ import annotations


def _qt_settings_source(src: str) -> str:
    start = src.index("class SettingsPage(PageBase):")
    end = src.index("class ToolsPage(PageBase):")
    return src[start:end]


def _method_block(src: str, start_marker: str, end_marker: str) -> str:
    start = src.index(start_marker)
    end = src.index(end_marker)
    return src[start:end]


def test_a1_preview_is_visual_only_not_persisted(flashgui_source: str) -> None:
    src = _qt_settings_source(flashgui_source)
    body = _method_block(src, "def _preview_theme(self) -> None:", "def _revert_theme(self) -> None:")

    assert "self.app.apply_theme(theme)" in body
    assert 'self._log(f"Theme preview: {theme} (not yet saved)")' in body
    assert "self.state.theme =" not in body
    assert "save_settings(" not in body


def test_a2_revert_restores_theme_original(flashgui_source: str) -> None:
    src = _qt_settings_source(flashgui_source)
    body = _method_block(src, "def _revert_theme(self) -> None:", "def _default_theme(self) -> None:")

    assert "self.theme_combo.setCurrentText(self.theme_original)" in body
    assert "self.app.apply_theme(self.theme_original)" in body
    assert 'self._log(f"Theme reverted to: {self.theme_original}")' in body


def test_a3_default_applies_default_theme_immediately(flashgui_source: str) -> None:
    src = _qt_settings_source(flashgui_source)
    body = _method_block(src, "def _default_theme(self) -> None:", "def _apply_theme(self) -> None:")

    assert 'self.theme_combo.setCurrentText("default")' in body
    assert 'self.app.apply_theme("default")' in body
    assert 'self._log("Theme reset to default: default")' in body


def test_a4_apply_persists_theme_and_updates_baseline(flashgui_source: str) -> None:
    src = _qt_settings_source(flashgui_source)
    body = _method_block(src, "def _apply_theme(self) -> None:", "def _save_sudo_keyring(self) -> None:")

    assert "self.state.theme = theme" in body
    assert "self.theme_original = theme" in body
    assert "self.app.apply_theme(theme)" in body
    assert "self.state.save_settings(geometry=self.state.window_geometry)" in body
    assert 'self._log(f"Theme applied and saved: {theme}")' in body
