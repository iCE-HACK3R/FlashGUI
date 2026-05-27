from __future__ import annotations

import sys
from types import SimpleNamespace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import flashgui


def test_detect_minipro_hardware_prefers_version_probe(monkeypatch) -> None:
    calls: list[list[str]] = []

    def fake_run(cmd, **kwargs):
        calls.append(list(cmd))
        assert kwargs["check"] is False
        assert kwargs["capture_output"] is True
        assert kwargs["text"] is True
        assert kwargs["errors"] == "replace"
        assert kwargs["timeout"] == 120
        if cmd[-1] == "-V":
            return SimpleNamespace(
                stdout=(
                    "Found T48 00.1.39 (0x127)\n"
                    "Warning: Firmware is newer than expected.\n"
                    "Device code: 48A17776\n"
                ),
                stderr="",
            )
        raise AssertionError(f"unexpected command: {cmd}")

    monkeypatch.setattr(flashgui.subprocess, "run", fake_run)

    detected, label, lines = flashgui._detect_minipro_hardware("minipro.exe")

    assert detected is True
    assert label == "Found T48 00.1.39 (0x127)"
    assert any("Found T48" in line for line in lines)
    assert calls == [["minipro.exe", "-V"]]


def test_detect_minipro_hardware_falls_back_to_list_probe(monkeypatch) -> None:
    calls: list[list[str]] = []

    def fake_run(cmd, **kwargs):
        calls.append(list(cmd))
        assert kwargs["check"] is False
        assert kwargs["capture_output"] is True
        assert kwargs["text"] is True
        assert kwargs["errors"] == "replace"
        assert kwargs["timeout"] == 120
        if cmd[-1] == "-V":
            return SimpleNamespace(stdout="minipro version 0.7.4\n", stderr="")
        if cmd[-1] == "-l":
            return SimpleNamespace(stdout="Found T48 00.1.39 (0x127)\n", stderr="")
        raise AssertionError(f"unexpected command: {cmd}")

    monkeypatch.setattr(flashgui.subprocess, "run", fake_run)

    detected, label, lines = flashgui._detect_minipro_hardware("minipro.exe")

    assert detected is True
    assert label == "Found T48 00.1.39 (0x127)"
    assert lines == ["Found T48 00.1.39 (0x127)"]
    assert calls == [["minipro.exe", "-V"], ["minipro.exe", "-l"]]


def test_minipro_spi_autodetect_falls_back_to_supported_parts(monkeypatch) -> None:
    calls: list[list[str]] = []

    def fake_run(cmd, **kwargs):
        calls.append(list(cmd))
        assert kwargs["check"] is False
        assert kwargs["capture_output"] is True
        assert kwargs["text"] is True
        assert kwargs["errors"] == "replace"
        if cmd[-1] == "8" or cmd[-1] == "16":
            return SimpleNamespace(stdout="minipro version 0.7.4\n", stderr="")
        if cmd[-1] == "-l":
            return SimpleNamespace(stdout="P24C02\nAT24C04\n", stderr="")
        raise AssertionError(f"unexpected command: {cmd}")

    monkeypatch.setattr(flashgui.subprocess, "run", fake_run)

    detected, label, chips, lines, bus = flashgui._autodetect_minipro_spi_devices("minipro.exe")

    assert detected is False
    assert label == ""
    assert chips == ["P24C02", "AT24C04"]
    assert bus == ""
    assert any("supported minipro parts" in line for line in lines)
    assert calls == [["minipro.exe", "-a", "8"], ["minipro.exe", "-a", "16"], ["minipro.exe", "-l"]]


def test_ft232h_usb_mapping_uses_required_programmer_params() -> None:
    usb_map = {
        (vid, pid): prog
        for vid, pid, prog, _label in flashgui._USB_PROGRAMMER_MAP
    }

    # Regression guard for issue #1: FT232H needs explicit type/divisor args.
    assert usb_map[("0403", "6014")] == "ft2232_spi:divisor=4,type=232h"

    # Neighbor FTDI variants should remain on their existing defaults.
    assert usb_map[("0403", "6010")] == "ft2232_spi"
    assert usb_map[("0403", "6011")] == "ft2232_spi"


def test_detect_programmer_usb_maps_ft232h_from_lsusb(monkeypatch) -> None:
    calls: list[list[str]] = []

    def fake_run(cmd, **kwargs):
        calls.append(list(cmd))
        assert kwargs["check"] is False
        assert kwargs["capture_output"] is True
        assert kwargs["text"] is True
        assert kwargs["errors"] == "replace"
        assert kwargs["timeout"] == 6

        if cmd == ["lsusb"]:
            return SimpleNamespace(stdout="Bus 001 Device 002: ID 0403:6014 FTDI FT232H\n", stderr="")
        if cmd in (["dmesg", "--color=never", "-T"], ["dmesg"]):
            return SimpleNamespace(stdout="", stderr="")
        raise AssertionError(f"unexpected command: {cmd}")

    monkeypatch.setattr(flashgui.sys, "platform", "linux")
    monkeypatch.setattr(flashgui.subprocess, "run", fake_run)

    detected = flashgui._detect_programmer_usb()

    assert detected == [
        ("ft2232_spi:divisor=4,type=232h", "FTDI FT232H  [0403:6014]"),
    ]
    assert calls[0] == ["lsusb"]
