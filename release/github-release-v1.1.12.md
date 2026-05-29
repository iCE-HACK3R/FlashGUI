# FlashGUI v1.1.12

Release refresh and version-alignment publish.

## What’s new

- Bumped release metadata and application versions to `v1.1.12`.
- Kept Qt + legacy paths in version lockstep.
- Updated README and release notes references for the new tag/artifact set.

## Why this matters

This release keeps project metadata, packaging targets, and publish automation aligned after post-`v1.1.11` maintenance updates.

## Version

- `flashgui.py`: `VERSION = "1.1.12"`
- `flashgui_legacy.py`: `VERSION = "1.1.12"`

## Suggested artifacts

- `flashgui-v1.1.12-windows-x64-portable.zip`
- `flashgui-v1.1.12-linux-x64-portable.zip`
- `flashgui-v1.1.12-macos-arm64-portable.zip`
- `flashgui-v1.1.12-macos-x64-portable.zip`

## Validation checklist

1. `python -m pytest -q`
2. Optional local packaging smoke check:
   - `python scripts/build_binaries.py --target windows`
