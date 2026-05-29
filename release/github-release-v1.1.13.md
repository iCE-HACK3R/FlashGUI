# FlashGUI v1.1.13

Release alignment and publish readiness update.

## What’s new

- Repository branch cleanup completed so `main` is the only active branch.
- Bumped release/application versions to `v1.1.13` in both UI paths.
- Updated README and release-note references for the new tag/artifact set.

## Version

- `flashgui.py`: `VERSION = "1.1.13"`
- `flashgui_legacy.py`: `VERSION = "1.1.13"`

## Suggested artifacts

- `flashgui-v1.1.13-windows-x64-portable.zip`
- `flashgui-v1.1.13-linux-x64-portable.zip`
- `flashgui-v1.1.13-macos-arm64-portable.zip`
- `flashgui-v1.1.13-macos-x64-portable.zip`

## Validation checklist

1. `python -m pytest -q`
2. Optional local packaging smoke check:
   - `python scripts/build_binaries.py --target windows`
