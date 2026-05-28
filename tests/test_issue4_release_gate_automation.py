from __future__ import annotations


def _source_slice(src: str, start_marker: str, end_marker: str) -> str:
    start = src.index(start_marker)
    end = src.index(end_marker)
    return src[start:end]


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
    op_base_src = _source_slice(flashgui_source, "class OpPageBase(PageBase):", "class ChipMixin:")

    assert "self.cmd_preview.setReadOnly(False)" in op_base_src
    assert 'grid.addWidget(_caption("Commands :"), 1, 0)' in op_base_src
    assert "def _parse_command_preview(self) -> list[str] | None:" in op_base_src
    assert "parsed = shlex.split" in op_base_src


def test_e2_completion_clarity_timetaken_and_completed_logs(flashgui_source: str) -> None:
    read_src = _source_slice(flashgui_source, "class ReadPage(OpPageBase, ChipMixin):", "class WritePage(OpPageBase, ChipMixin):")
    write_src = _source_slice(flashgui_source, "class WritePage(OpPageBase, ChipMixin):", "class VerifyPage(OpPageBase, ChipMixin):")

    assert 'self.log(f"TimeTaken: {_fmt_elapsed(elapsed)}")' in read_src
    assert 'self.log("Completed: Ok")' in read_src

    assert 'self.log(f"TimeTaken: {_fmt_elapsed(elapsed)}")' in write_src
    assert 'self.log(f"Completed: {status}")' in write_src


def test_e3_oversized_image_preflight_blocks_write(flashgui_source: str) -> None:
    write_src = _source_slice(flashgui_source, "class WritePage(OpPageBase, ChipMixin):", "class VerifyPage(OpPageBase, ChipMixin):")

    assert "if file_size > chip_size:" in write_src
    assert 'self.log("ERROR: Selected image is larger than the detected chip size.")' in write_src
    assert 'f"Image size {_fmt_bytes(file_size)} ({file_size} B) > "' in write_src
    assert 'f"chip size {_fmt_bytes(chip_size)} ({chip_size} B)."' in write_src
    assert 'self.log("Write aborted before flashing. Choose a smaller image or a larger chip.")' in write_src


def test_e4_detect_is_blocked_while_operations_active(flashgui_source: str) -> None:
    chip_mixin_src = _source_slice(flashgui_source, "class ChipMixin:", "class ReadPage(OpPageBase, ChipMixin):")
    main_window_src = _source_slice(flashgui_source, "class FlashGUIQt(QMainWindow):", "def main() -> int:")

    assert "if _has_active_operations():" in chip_mixin_src
    assert "Detect ROM is disabled while" in chip_mixin_src

    assert "if _has_active_operations():" in main_window_src
    assert "Programmer detection is disabled while" in main_window_src
