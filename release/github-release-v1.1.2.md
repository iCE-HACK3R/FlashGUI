# FlashGUI v1.1.2

## Highlights

- Fixed lingering **Save & Apply** font persistence issues in the Qt UI.
- Fixed startup font propagation so restored app font is applied across built page widgets.
- Added recovery logic for previously mis-saved downloadable font family names.

## Documentation

- README release references updated to `v1.1.2`.
- Release notes updated with a dedicated `v1.1.2` section.

## Version

- Bumped application version in `flashgui.py`:
  - `VERSION = "1.1.2"`

## Build Artifact

- One-file executables generated with PyInstaller:
  - `dist/flashgui.exe`
  - `dist/flashgui`
- Release bundle targets:
  - `release/flashgui-v1.1.2-windows-x64.zip`
  - `release/flashgui-v1.1.2-linux-x64.zip`
