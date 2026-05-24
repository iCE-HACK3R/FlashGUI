# Release Notes

## v1.1.2

### Highlights (v1.1.2)

- Fixed lingering **Save & Apply** font persistence issues in the Qt UI.
- Fixed startup font propagation so restored app font is applied across built page widgets.
- Added recovery logic for previously mis-saved downloadable font family names.

### Documentation (v1.1.2)

- Updated README release references for `v1.1.2`.
- Added a dedicated GitHub release draft file for `v1.1.2`.

### Version (v1.1.2)

- Bumped application version in `flashgui.py`:
  - `VERSION = "1.1.2"`

### Build Artifact (v1.1.2)

- Target release bundle names:
  - `release/flashgui-v1.1.2-windows-x64.zip`
  - `release/flashgui-v1.1.2-linux-x64.zip`

## v1.1.1

### Highlights (v1.1.1)

- Improved cross-platform programmer detection flow (Windows/macOS serial-aware paths).
- Improved macOS behavior around monospace font handling in the UI.
- Settings page now better reflects platform-specific options.

### Documentation (v1.1.1)

- README release references updated for `v1.1.1`.
- README screenshots section retained/expanded with current UI captures.
- Platform status keeps macOS explicitly marked as **currently untested**.

### Version (v1.1.1)

- Bumped application version in `flashgui.py`:
  - `VERSION = "1.1.1"`

### Build Artifact (v1.1.1)

- Target release bundle name:
  - `release/flashgui-v1.1.1-windows-x64.zip`

## v1.1.0

### Highlights

- Added dedicated **Console Font** selector in the Global Logs toolbar.
- Added **Console Font Size** selector with `Auto` and explicit point-size options.
- Console font settings now apply to:
  - Global Logs output
  - Programmer Console output window
- Updated Console Font label icon for better visual consistency.
- Added programmer console screenshot to README.

### Documentation

- Updated `README.md` screenshots section with Programmer Console image.

### Version

- Bumped application version in `flashgui.py`:
  - `VERSION = "1.1.0"`

### Build Artifact

- Generated one-file Windows executable using PyInstaller:
  - `dist/flashgui.exe`
