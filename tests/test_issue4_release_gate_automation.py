from __future__ import annotations

import os
import importlib
import sys
from pathlib import Path
from unittest import mock

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _source_slice(src: str, start_marker: str, end_marker: str) -> str:
    start = src.index(start_marker)
    end = src.index(end_marker)
    return src[start:end]


def _load_flashgui() -> object:
    """Import flashgui with a throwaway settings path."""
    os.environ["FLASHGUI_SETTINGS_PATH"] = "/tmp/_test_kde_settings.json"
    if "flashgui" in sys.modules:
        del sys.modules["flashgui"]
    return importlib.import_module("flashgui")


def test_d_apply_and_save_path_has_save_and_success_log(flashgui_source: str) -> None:
    settings_src = _source_slice(
        flashgui_source,
        "class SettingsPage(PageBase):",
        "class ToolsPage(PageBase):",
    )
    apply_start = settings_src.index("def _apply(self) -> None:")
    apply_body = settings_src[apply_start:]

    assert "self.state.save_settings(geometry=self.state.window_geometry)" in apply_body
    assert 'self._log("Settings saved.")' in apply_body


def test_e1_commands_field_is_editable_and_parseable(flashgui_source: str) -> None:
    op_base_src = _source_slice(
        flashgui_source, "class OpPageBase(PageBase):", "class ChipMixin:"
    )

    assert "self.cmd_preview.setReadOnly(False)" in op_base_src
    assert 'grid.addWidget(_caption("Commands :"), 1, 0)' in op_base_src
    assert "def _parse_command_preview(self) -> list[str] | None:" in op_base_src
    assert "parsed = shlex.split" in op_base_src


def test_e2_completion_clarity_timetaken_and_completed_logs(
    flashgui_source: str,
) -> None:
    read_src = _source_slice(
        flashgui_source,
        "class ReadPage(OpPageBase, ChipMixin):",
        "class WritePage(OpPageBase, ChipMixin):",
    )
    write_src = _source_slice(
        flashgui_source,
        "class WritePage(OpPageBase, ChipMixin):",
        "class VerifyPage(OpPageBase, ChipMixin):",
    )

    assert 'self.log(f"TimeTaken: {_fmt_elapsed(elapsed)}")' in read_src
    assert 'self.log("Completed: Ok")' in read_src

    assert 'self.log(f"TimeTaken: {_fmt_elapsed(elapsed)}")' in write_src
    assert 'self.log(f"Completed: {status}")' in write_src


def test_e3_oversized_image_preflight_blocks_write(flashgui_source: str) -> None:
    write_src = _source_slice(
        flashgui_source,
        "class WritePage(OpPageBase, ChipMixin):",
        "class VerifyPage(OpPageBase, ChipMixin):",
    )

    assert "if file_size > chip_size:" in write_src
    assert (
        'self.log("ERROR: Selected image is larger than the detected chip size.")'
        in write_src
    )
    assert 'f"Image size {_fmt_bytes(file_size)} ({file_size} B) > "' in write_src
    assert 'f"chip size {_fmt_bytes(chip_size)} ({chip_size} B)."' in write_src
    assert (
        'self.log("Write aborted before flashing. Choose a smaller image or a larger chip.")'
        in write_src
    )


def test_e4_detect_is_blocked_while_operations_active(flashgui_source: str) -> None:
    chip_mixin_src = _source_slice(
        flashgui_source, "class ChipMixin:", "class ReadPage(OpPageBase, ChipMixin):"
    )
    main_window_src = _source_slice(
        flashgui_source, "class FlashGUIQt(QMainWindow):", "def main() -> int:"
    )

    assert "if _has_active_operations():" in chip_mixin_src
    assert "Detect ROM is disabled while" in chip_mixin_src

    assert "if _has_active_operations():" in main_window_src
    assert "Programmer detection is disabled while" in main_window_src


# ---------------------------------------------------------------------------
# KDE native dialog regression tests (v1.1.10 fix)
#
# Pre-fix behaviour: on KDE/Plasma with native dialogs enabled, Qt's native
# file dialog was used directly. This could hang or render incorrectly
# because Qt's native dialog integration on KDE is unreliable across
# Plasma versions.
#
# Post-fix behaviour:
#   1. _effective_use_native_file_dialogs() returns False on KDE so
#      QFileDialog falls back to its own non-native widget.
#   2. _can_use_kdialog() gates KDE-native picker use to Linux + KDE +
#      kdialog binary present + user opted in.
#   3. Qt wrapper helpers try kdialog first and fall back to the Qt
#      non-native dialog — never to Qt's native dialog on KDE.
# ---------------------------------------------------------------------------


# -- Source-analysis tests (structural guarantees) --------------------------


def test_kde_detection_function_exists(flashgui_source: str) -> None:
    assert "def _is_kde_desktop() -> bool:" in flashgui_source


def test_effective_native_dialog_disables_native_on_kde(flashgui_source: str) -> None:
    fn_start = flashgui_source.index(
        "def _effective_use_native_file_dialogs(use_native_dialogs: bool) -> bool:"
    )
    fn_end = flashgui_source.index(
        "def _can_use_kdialog(use_native_dialogs: bool) -> bool:"
    )
    body = flashgui_source[fn_start:fn_end]
    assert "not _is_kde_desktop()" in body


def test_can_use_kdialog_requires_linux_kde_and_binary(flashgui_source: str) -> None:
    fn_start = flashgui_source.index(
        "def _can_use_kdialog(use_native_dialogs: bool) -> bool:"
    )
    fn_end = flashgui_source.index(
        "def _qt_filter_to_kdialog_filter(file_filter: str) -> str:"
    )
    body = flashgui_source[fn_start:fn_end]
    assert 'sys.platform.startswith("linux")' in body
    assert "_is_kde_desktop()" in body
    assert 'shutil.which("kdialog") is not None' in body
    assert "bool(use_native_dialogs)" in body


def test_qfiledialog_options_adds_dont_use_native_on_kde(flashgui_source: str) -> None:
    fn_start = flashgui_source.index(
        "def _qfiledialog_options(use_native_dialogs: bool) -> QFileDialog.Option:"
    )
    fn_end = flashgui_source.index("def _qt_get_open_file_name(")
    body = flashgui_source[fn_start:fn_end]
    assert "_effective_use_native_file_dialogs(use_native_dialogs)" in body
    assert "QFileDialog.Option.DontUseNativeDialog" in body


def test_qt_wrappers_try_kdialog_with_fallback(flashgui_source: str) -> None:
    open_start = flashgui_source.index("def _qt_get_open_file_name(")
    save_start = flashgui_source.index("def _qt_get_save_file_name(")
    dir_start = flashgui_source.index("def _qt_get_existing_directory(")
    mono_start = flashgui_source.index("def _qt_preferred_mono_family() -> str:")

    open_body = flashgui_source[open_start:save_start]
    save_body = flashgui_source[save_start:dir_start]
    dir_body = flashgui_source[dir_start:mono_start]

    for label, body in [("open", open_body), ("save", save_body), ("dir", dir_body)]:
        assert (
            "_can_use_kdialog(use_native_dialogs)" in body
        ), f"{label}: missing kdialog gate"
        assert "QFileDialog" in body, f"{label}: missing Qt fallback"


def test_kdialog_cancel_does_not_trigger_second_dialog(flashgui_source: str) -> None:
    fn_start = flashgui_source.index(
        "def _run_kdialog(cmd: list[str]) -> tuple[str, bool, bool]:"
    )
    fn_end = flashgui_source.index("def _kde_get_open_file_name(")
    body = flashgui_source[fn_start:fn_end]
    assert 'return "", True, True' in body


# -- Functional tests (behavioural guarantees) ------------------------------


class TestIsKdeDesktop:
    """Verify _is_kde_desktop() detects KDE via environment variables."""

    _KDE_ENVS = {
        "XDG_CURRENT_DESKTOP": "",
        "DESKTOP_SESSION": "",
        "KDE_FULL_SESSION": "",
    }

    def _call(self, mod: object, env_overrides: dict[str, str]) -> bool:
        env = {**self._KDE_ENVS, **env_overrides}
        with mock.patch.dict(os.environ, env, clear=False):
            return mod._is_kde_desktop()  # type: ignore[attr-defined]

    def test_xdg_kde(self) -> None:
        mod = _load_flashgui()
        assert self._call(mod, {"XDG_CURRENT_DESKTOP": "KDE"}) is True

    def test_xdg_plasma(self) -> None:
        mod = _load_flashgui()
        assert self._call(mod, {"XDG_CURRENT_DESKTOP": "KDE:plasma"}) is True

    def test_desktop_session_kde(self) -> None:
        mod = _load_flashgui()
        assert self._call(mod, {"DESKTOP_SESSION": "plasma-kde"}) is True

    def test_kde_full_session_flag(self) -> None:
        mod = _load_flashgui()
        assert self._call(mod, {"KDE_FULL_SESSION": "true"}) is True

    def test_non_kde_desktop(self) -> None:
        mod = _load_flashgui()
        assert self._call(mod, {"XDG_CURRENT_DESKTOP": "GNOME"}) is False

    def test_empty_environment(self) -> None:
        mod = _load_flashgui()
        assert self._call(mod, {}) is False


class TestEffectiveUseNativeFileDialogs:
    """Verify native dialogs are disabled on KDE (the core fix)."""

    def test_native_enabled_on_kde_returns_false(self) -> None:
        mod = _load_flashgui()
        with mock.patch.object(mod, "_is_kde_desktop", return_value=True):
            result = mod._effective_use_native_file_dialogs(True)  # type: ignore[attr-defined]
        assert result is False

    def test_native_enabled_on_non_kde_returns_true(self) -> None:
        mod = _load_flashgui()
        with mock.patch.object(mod, "_is_kde_desktop", return_value=False):
            result = mod._effective_use_native_file_dialogs(True)  # type: ignore[attr-defined]
        assert result is True

    def test_native_disabled_on_kde_returns_false(self) -> None:
        mod = _load_flashgui()
        with mock.patch.object(mod, "_is_kde_desktop", return_value=True):
            result = mod._effective_use_native_file_dialogs(False)  # type: ignore[attr-defined]
        assert result is False

    def test_native_disabled_on_non_kde_returns_false(self) -> None:
        mod = _load_flashgui()
        with mock.patch.object(mod, "_is_kde_desktop", return_value=False):
            result = mod._effective_use_native_file_dialogs(False)  # type: ignore[attr-defined]
        assert result is False


class TestCanUseKdialog:
    """Verify kdialog gating requires all four conditions."""

    def _call(
        self,
        mod: object,
        *,
        use_native: bool,
        platform: str,
        is_kde: bool,
        kdialog_present: bool,
    ) -> bool:
        which_rv = "/usr/bin/kdialog" if kdialog_present else None
        with (
            mock.patch.object(mod, "_is_kde_desktop", return_value=is_kde),
            mock.patch("sys.platform", platform),
            mock.patch("shutil.which", return_value=which_rv),
        ):
            return mod._can_use_kdialog(use_native)  # type: ignore[attr-defined]

    def test_all_conditions_met(self) -> None:
        mod = _load_flashgui()
        assert (
            self._call(
                mod,
                use_native=True,
                platform="linux",
                is_kde=True,
                kdialog_present=True,
            )
            is True
        )

    def test_not_linux(self) -> None:
        mod = _load_flashgui()
        assert (
            self._call(
                mod,
                use_native=True,
                platform="win32",
                is_kde=True,
                kdialog_present=True,
            )
            is False
        )

    def test_not_kde(self) -> None:
        mod = _load_flashgui()
        assert (
            self._call(
                mod,
                use_native=True,
                platform="linux",
                is_kde=False,
                kdialog_present=True,
            )
            is False
        )

    def test_kdialog_missing(self) -> None:
        mod = _load_flashgui()
        assert (
            self._call(
                mod,
                use_native=True,
                platform="linux",
                is_kde=True,
                kdialog_present=False,
            )
            is False
        )

    def test_native_disabled(self) -> None:
        mod = _load_flashgui()
        assert (
            self._call(
                mod,
                use_native=False,
                platform="linux",
                is_kde=True,
                kdialog_present=True,
            )
            is False
        )


class TestRunKdialogCancelHandling:
    """Verify _run_kdialog returns (handled=True, canceled=True) on cancel."""

    def test_cancel_returns_handled_and_canceled(self) -> None:
        mod = _load_flashgui()
        fake_proc = mock.Mock(returncode=1, stdout="", stderr="")
        with mock.patch("subprocess.run", return_value=fake_proc):
            path, handled, canceled = mod._run_kdialog(["kdialog", "--getopenfilename", "/tmp"])  # type: ignore[attr-defined]
        assert path == ""
        assert handled is True
        assert canceled is True

    def test_success_returns_path(self) -> None:
        mod = _load_flashgui()
        fake_proc = mock.Mock(returncode=0, stdout="/home/user/rom.bin\n", stderr="")
        with mock.patch("subprocess.run", return_value=fake_proc):
            path, handled, canceled = mod._run_kdialog(["kdialog", "--getopenfilename", "/tmp"])  # type: ignore[attr-defined]
        assert path == "/home/user/rom.bin"
        assert handled is True
        assert canceled is False

    def test_exception_falls_back(self) -> None:
        mod = _load_flashgui()
        with mock.patch("subprocess.run", side_effect=OSError("not found")):
            path, handled, canceled = mod._run_kdialog(["kdialog", "--getopenfilename", "/tmp"])  # type: ignore[attr-defined]
        assert path == ""
        assert handled is False
        assert canceled is False
