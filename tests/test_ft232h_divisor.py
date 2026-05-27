"""Regression tests for the FT232H SPI clock divisor settings override."""
from __future__ import annotations

import importlib
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


@pytest.fixture()
def flashgui():
    # Reload so module-level _FT232H_DIVISOR / _USB_PROGRAMMER_MAP are fresh per test.
    if "flashgui" in sys.modules:
        del sys.modules["flashgui"]
    mod = importlib.import_module("flashgui")
    yield mod
    # Restore default for any later imports
    mod._apply_ft232h_divisor(mod._FT232H_DEFAULT_DIVISOR)


def _ft232h_entry(mod):
    for vid, pid, prog, label in mod._USB_PROGRAMMER_MAP:
        if vid == "0403" and pid == "6014":
            return prog
    raise AssertionError("FT232H entry not found in _USB_PROGRAMMER_MAP")


def test_default_divisor_is_four(flashgui):
    assert flashgui._FT232H_DEFAULT_DIVISOR == "4"
    assert _ft232h_entry(flashgui) == "ft2232_spi:divisor=4,type=232h"


def test_normalize_invalid_falls_back_to_default(flashgui):
    assert flashgui._normalize_ft232h_divisor(None) == "4"
    assert flashgui._normalize_ft232h_divisor("") == "4"
    assert flashgui._normalize_ft232h_divisor("99") == "4"
    assert flashgui._normalize_ft232h_divisor("garbage") == "4"


def test_normalize_accepts_supported_values(flashgui):
    assert flashgui._normalize_ft232h_divisor("2") == "2"
    assert flashgui._normalize_ft232h_divisor(4) == "4"
    assert flashgui._normalize_ft232h_divisor(" 2 ") == "2"


def test_apply_divisor_updates_map_in_place(flashgui):
    flashgui._apply_ft232h_divisor("2")
    assert _ft232h_entry(flashgui) == "ft2232_spi:divisor=2,type=232h"
    flashgui._apply_ft232h_divisor("4")
    assert _ft232h_entry(flashgui) == "ft2232_spi:divisor=4,type=232h"


def test_apply_invalid_divisor_resets_to_default(flashgui):
    flashgui._apply_ft232h_divisor("2")
    assert _ft232h_entry(flashgui) == "ft2232_spi:divisor=2,type=232h"
    flashgui._apply_ft232h_divisor("bogus")
    assert _ft232h_entry(flashgui) == "ft2232_spi:divisor=4,type=232h"


def test_programmer_arg_helper(flashgui):
    assert flashgui._ft232h_programmer_arg("2") == "ft2232_spi:divisor=2,type=232h"
    assert flashgui._ft232h_programmer_arg("4") == "ft2232_spi:divisor=4,type=232h"
    assert flashgui._ft232h_programmer_arg("nonsense") == "ft2232_spi:divisor=4,type=232h"
