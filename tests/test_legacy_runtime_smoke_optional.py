from __future__ import annotations

import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def test_legacy_flashgui_bootstrap_when_tk_available(monkeypatch: pytest.MonkeyPatch) -> None:
    """Optional runtime smoke for legacy Tk UI.

    This test intentionally skips in environments where tkinter is unavailable
    (or where no GUI display/session is available), so CI without Tk support
    does not fail.
    """
    pytest.importorskip("tkinter")

    import tkinter as tk
    import flashgui_legacy as legacy

    # Keep smoke lightweight/non-invasive: allow page construction but skip
    # interactive/heavy startup actions.
    monkeypatch.setattr(legacy.FlashGUI, "_refresh_tool", lambda self: None)
    monkeypatch.setattr(legacy.FlashGUI, "_apply_startup_settings_validation", lambda self: None)
    monkeypatch.setattr(legacy.FlashGUI, "_on_detect_programmer", lambda self: None)

    app = None
    try:
        app = legacy.FlashGUI()
        app.root.update_idletasks()

        # Basic sanity: app constructed and Read page has the advanced frame.
        assert app.root.winfo_exists() == 1
        assert hasattr(app.page_read, "adv_frame")
    except tk.TclError as exc:
        pytest.skip(f"Tk runtime unavailable in this environment: {exc}")
    finally:
        if app is not None:
            try:
                app.root.destroy()
            except Exception:
                pass
