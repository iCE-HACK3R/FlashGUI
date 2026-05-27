# FlashGUI v1.1.8

User-tunable FT232H SPI clock divisor + minor build polish.

## What's new

- **FT232H SPI clock divisor setting** (Settings → Behavior)
  - Default `4` — safe for both 1.8 V and 3.3 V targets (slightly slower).
  - Option `2` — faster reads, 3.3 V targets only.
  - Honored by every flashrom probe / detect / read / write that uses the autodetected FT232H entry.
- **Environment override:** `FLASHGUI_FT232H_DIVISOR=2|4` for power users and CI.
- **Legacy Tk parity:** same setting and UI mirrored into `flashgui_legacy.py`; the legacy FT232H entry now correctly emits `ft2232_spi:divisor=4,type=232h` instead of bare `ft2232_spi`.
- **macOS Intel build restored:** v1.1.8 ships both `macos-arm64` and `macos-x64` artifacts.

## Why this matters

Per the issue #1 reporter, divisor=4 works at both 1.8 V and 3.3 V, while divisor=2 is faster but only stable at 3.3 V. v1.1.8 keeps the safe default and lets advanced users opt in to higher speeds without editing source.

## Tests

- New `tests/test_ft232h_divisor.py` regression coverage for normalization, in-place map mutation, and fallback behavior.
- Full suite (24 tests) green locally.

## Artifacts

- `flashgui-v1.1.8-windows-x64-portable.zip`
- `flashgui-v1.1.8-linux-x64-portable.zip`
- `flashgui-v1.1.8-macos-arm64-portable.zip`
- `flashgui-v1.1.8-macos-x64-portable.zip`
