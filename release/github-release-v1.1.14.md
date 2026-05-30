# FlashGUI v1.1.14

Minipro verbose-mode behavior fix and release alignment update.

## What’s new

- Minipro mode now forces **Verbose Mode** to **Off**.
- Global verbosity flags (`-V`, `-VV`, `-VVV`) are no longer injected into minipro commands.
- Added regression coverage to keep this behavior stable in future releases.
- Bumped release/application versions to `v1.1.14`.

## Version

- `flashgui.py`: `VERSION = "1.1.14"`
- `flashgui_legacy.py`: `VERSION = "1.1.14"`

## Suggested artifacts

- `flashgui-v1.1.14-windows-x64-portable.zip`
- `flashgui-v1.1.14-linux-x64-portable.zip`
- `flashgui-v1.1.14-macos-arm64-portable.zip`
- `flashgui-v1.1.14-macos-x64-portable.zip`

## Validation checklist

1. `python -m pytest -q`
2. Focused regression check:
   - `python -m pytest -q tests/test_minipro_detection.py`
3. Optional local packaging smoke check:
   - `python scripts/build_binaries.py --target windows`
