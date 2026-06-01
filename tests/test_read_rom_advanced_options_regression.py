from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _readpage_qt_source() -> str:
    source = (ROOT / "flashgui.py").read_text(encoding="utf-8")
    start = source.index("class ReadPage(OpPageBase, ChipMixin):")
    end = source.index("class WritePage(OpPageBase, ChipMixin):")
    return source[start:end]


def _readpage_legacy_source() -> str:
    source = (ROOT / "flashgui_legacy.py").read_text(encoding="utf-8")
    start = source.index("class PageRead(_ChipMixin):")
    end = source.index("class PageWrite(_ChipMixin):")
    return source[start:end]


def test_qt_read_page_uses_collapsible_advanced_options() -> None:
    src = _readpage_qt_source()

    assert 'adv_group = CollapsibleQGroupBox("🔧 Advanced Options")' in src
    assert 'adv_group.add_layout(adv_lay)' in src
    assert 'adv_group.toggle_collapse()' in src
    assert 'self.form_lay.addRow(adv_group)' in src

    assert 'self.opt_reveal = QCheckBox("Reveal file upon completion")' in src
    assert 'self.opt_nopad = QCheckBox("Remove padding (0xFF) from dump")' in src
    assert 'adv_lay.addWidget(self.opt_reveal)' in src
    assert 'adv_lay.addWidget(self.opt_nopad)' in src


def test_legacy_read_page_uses_collapsible_advanced_options() -> None:
    src = _readpage_legacy_source()

    assert 'self.adv_frame = _CollapsibleFrame(control_frame, text="🔧 Advanced Options")' in src
    assert 'self.adv_frame.grid(row=4, column=0, columnspan=3, sticky="ew", pady=(10, 0))' in src

    assert 'ttk.Checkbutton(self.adv_frame.container, text="Reveal file upon completion", variable=self.opt_reveal).pack(' in src
    assert 'ttk.Checkbutton(self.adv_frame.container, text="Remove padding (0xFF) from dump", variable=self.opt_nopad).pack(' in src

    assert 'self.progress.grid(row=5, column=0, columnspan=3, pady=10, sticky="ew")' in src
    assert 'ttk.Button(control_frame, text="Read ROM", width=12, command=self._run).grid(row=6, column=0, columnspan=3, pady=4)' in src
