# FlashGUI v1.1.15

Read ROM advanced-options UX update and release alignment.

## What’s new

- In **Read ROM**, options are now grouped under **🔧 Advanced Options** in both Qt and legacy UI paths.
- Read ROM advanced options default to **collapsed**.
- Added structural regression coverage:
  - `tests/test_read_rom_advanced_options_regression.py`
- Added optional legacy runtime smoke test:
  - `tests/test_legacy_runtime_smoke_optional.py`
- Bumped release/application versions to `v1.1.15`.

## Version

- `flashgui.py`: `VERSION = "1.1.15"`
- `flashgui_legacy.py`: `VERSION = "1.1.15"`

## Suggested artifacts

- `flashgui-v1.1.15-windows-x64-portable.zip`
- `flashgui-v1.1.15-linux-x64-portable.zip`
- `flashgui-v1.1.15-macos-arm64-portable.zip`
- `flashgui-v1.1.15-macos-x64-portable.zip`

## Validation checklist

1. `python -m pytest -q`
2. Focused regression checks:
   - `python -m pytest -q tests/test_read_rom_advanced_options_regression.py`
   - `python -m pytest -q tests/test_legacy_runtime_smoke_optional.py`
3. Optional local packaging smoke check:
   - `python scripts/build_binaries.py --target windows`
