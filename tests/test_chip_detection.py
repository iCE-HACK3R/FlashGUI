from __future__ import annotations

import sys
from types import SimpleNamespace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import flashgui


def test_detect_chips_accepts_single_quoted_chip_names(monkeypatch) -> None:
    def fake_run(cmd, **kwargs):
        assert cmd == ["flashrom", "-V", "-p", "ft2232_spi:divisor=4,type=232h"]
        assert kwargs["check"] is False
        assert kwargs["capture_output"] is True
        assert kwargs["text"] is True
        assert kwargs["errors"] == "replace"
        assert kwargs["timeout"] == 30
        return SimpleNamespace(
            returncode=0,
            stdout=(
                "found Winbond flash chip 'W25Q64JVSIQ' (8192 kB, SPI) on ft2232_spi.\n"
                "Found Macronix flash chip 'MX25L6404E' (8192 kB, SPI) on ft2232_spi.\n"
                "Use flashrom -p ft2232_spi:divisor=4,type=232h\n"
            ),
            stderr="",
        )

    monkeypatch.setattr(flashgui.subprocess, "run", fake_run)

    chips, suggested, probe_ids, failure_hint = flashgui._detect_chips(
        "flashrom", "ft2232_spi:divisor=4,type=232h"
    )

    assert chips == ["W25Q64JVSIQ", "MX25L6404E"]
    assert suggested == "ft2232_spi:divisor=4,type=232h"
    assert probe_ids == []
    assert failure_hint is None
