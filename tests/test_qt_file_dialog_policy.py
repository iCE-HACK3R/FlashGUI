from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _source() -> str:
    return (ROOT / "flashgui.py").read_text(encoding="utf-8")


def test_effective_native_dialog_policy_exists() -> None:
    src = _source()
    assert "def _effective_use_native_file_dialogs(use_native_dialogs: bool) -> bool:" in src


def test_effective_native_dialog_policy_is_kde_safe() -> None:
    src = _source()
    start = src.index("def _effective_use_native_file_dialogs(use_native_dialogs: bool) -> bool:")
    end = src.index("def _qfiledialog_options(use_native_dialogs: bool) -> QFileDialog.Option:")
    body = src[start:end]

    assert "return bool(use_native_dialogs) and not _is_kde_desktop()" in body


def test_qfiledialog_options_uses_effective_policy() -> None:
    src = _source()
    start = src.index("def _qfiledialog_options(use_native_dialogs: bool) -> QFileDialog.Option:")
    end = src.index("def _qt_get_open_file_name(")
    body = src[start:end]

    assert "_effective_use_native_file_dialogs(use_native_dialogs)" in body
    assert "QFileDialog.Option.DontUseNativeDialog" in body


def test_kdialog_guard_is_kde_linux_native_only() -> None:
    src = _source()
    start = src.index("def _can_use_kdialog(use_native_dialogs: bool) -> bool:")
    end = src.index("def _qt_filter_to_kdialog_filter(file_filter: str) -> str:")
    body = src[start:end]

    assert "sys.platform.startswith(\"linux\")" in body
    assert "_is_kde_desktop()" in body
    assert "shutil.which(\"kdialog\") is not None" in body
    assert "bool(use_native_dialogs)" in body


def test_qt_wrappers_try_kdialog_before_qt_fallback() -> None:
    src = _source()

    open_start = src.index("def _qt_get_open_file_name(")
    save_start = src.index("def _qt_get_save_file_name(")
    dir_start = src.index("def _qt_get_existing_directory(")
    mono_start = src.index("def _qt_preferred_mono_family() -> str:")

    open_body = src[open_start:save_start]
    save_body = src[save_start:dir_start]
    dir_body = src[dir_start:mono_start]

    assert "_can_use_kdialog(use_native_dialogs)" in open_body
    assert "_kde_get_open_file_name" in open_body
    assert "QFileDialog.getOpenFileName" in open_body

    assert "_can_use_kdialog(use_native_dialogs)" in save_body
    assert "_kde_get_save_file_name" in save_body
    assert "QFileDialog.getSaveFileName" in save_body

    assert "_can_use_kdialog(use_native_dialogs)" in dir_body
    assert "_kde_get_existing_directory" in dir_body
    assert "QFileDialog.getExistingDirectory" in dir_body
