# Release Notes

## v1.1.7

### Highlights (v1.1.7)

- Hardened flashrom chip-detect parser to accept single-quoted chip names and lowercase detection keywords (`found` / `multiple` / `match`). Resolves "No chip detected" on FT232H probes that emit `'W25Q64JVSIQ'`-style names.
- Applied the same parser hardening to the legacy Tk path (`flashgui_legacy.py::_detect_chips`).
- CI: install `libegl1` / `libgl1` on Linux so PySide6 imports succeed during tests.
- README: re-added `python3 ...` workflow notes for Linux/macOS.

### Tests (v1.1.7)

- Added `tests/test_chip_detection.py` regression coverage for single-quoted chip names + FT232H hint parsing.

### Version (v1.1.7)

- Bumped application versions:
  - `flashgui.py`: `VERSION = "1.1.7"`
  - `flashgui_legacy.py`: `VERSION = "1.1.7"`

### Build Artifact Targets (v1.1.7)

- `release/flashgui-v1.1.7-windows-x64-portable.zip`
- `release/flashgui-v1.1.7-linux-x64-portable.zip`
- `release/flashgui-v1.1.7-macos-x64-portable.zip`

## v1.1.6

### Highlights (v1.1.6)

- Fixed FT232H autodetect flow by mapping USB ID `0403:6014` to:
  - `ft2232_spi:divisor=4,type=232h`
- Fixed Settings page layout overflow on constrained displays (for example Debian KDE FHD) by changing the Qt **Systems & Settings** action area from a single long row to a wrapped grid layout.
- Added regression coverage for FT232H mapping and Linux `lsusb` autodetect behavior.

### Version (v1.1.6)

- Bumped application versions:
  - `flashgui.py`: `VERSION = "1.1.6"`
  - `flashgui_legacy.py`: `VERSION = "1.1.6"`

### Build Artifact Targets (v1.1.6)

- `release/flashgui-v1.1.6-windows-x64-portable.zip`
- `release/flashgui-v1.1.6-linux-x64-portable.zip`
- `release/flashgui-v1.1.6-macos-x64-portable.zip`

## v1.1.5

### Highlights (v1.1.5)

- About ROM for Minipro now combines both command outputs:
  - `-D` to populate **Chip ID**
  - `-d` to populate model/vendor/size and remaining details
- Added a remove-chip warning confirmation before Minipro hardware self-test (`-t`) in both Tk and Qt flows.

### Build & Release (v1.1.5)

- Hardened `scripts/build_binaries.py` with a PyInstaller preflight check and clearer interpreter guidance.
- Updated README commands to prefer `python` on Windows, avoiding MSYS `python3` mismatches.

### Version (v1.1.5)

- Bumped application versions:
  - `flashgui.py`: `VERSION = "1.1.5"`
  - `flashgui_legacy.py`: `VERSION = "1.1.5"`

### Build Artifact Targets (v1.1.5)

- `release/flashgui-v1.1.5-windows-x64-portable.zip`
- `release/flashgui-v1.1.5-linux-x64-portable.zip`
- `release/flashgui-v1.1.5-macos-x64-portable.zip`

## v1.1.4

### Highlights (v1.1.4)

- Fixed Minipro progress handling while preserving existing `flashrom` / `flashprog` progress behavior.
- Reduced noisy Minipro terminal output by cleaning duplicated ANSI/status spam in live logs.
- Fixed Minipro erase action by switching to the correct uppercase `-E` flag.
- Improved `FW Info` UX: now prompts for a `.dat` file or a folder containing `.dat` files.
- Expanded Binwalk tooling:
  - kept `Binwalk ROMs` (scan flow)
  - added `Binwalk Extract & Analize` (extract + analyze flow)
- Updated Help/About tested programmer list to include **T48**.

### Documentation (v1.1.4)

- Added Minipro T48 workflow screenshots to `README.md`.
- Updated release/tag examples and artifact references to `v1.1.4`.

### Version (v1.1.4)

- Bumped application versions:
  - `flashgui.py`: `VERSION = "1.1.4"`
  - `flashgui_legacy.py`: `VERSION = "1.1.4"`

### Build Artifact Targets (v1.1.4)

- `release/flashgui-v1.1.4-windows-x64-portable.zip`
- `release/flashgui-v1.1.4-linux-x64-portable.zip`
- `release/flashgui-v1.1.4-macos-x64-portable.zip`

## v1.1.3

### Highlights (v1.1.3)

- Fixed `Read Chip Info` parsing for `flashprog -V` so chip IDs are captured from verbose formats including:
  - `probe_spi_rdid: id1 ... id2 ...`
  - `SPI_RDID: id1 ... id2 ...`
- Fixed `Write Protection` population in `About ROM` when using `flashprog --flash-name` output.
- Updated `Read ROM` auto-generated output filenames to include tool prefixes:
  - `FR_...` for `flashrom`
  - `FP_...` for `flashprog`
- Made `Tested Chips (ROMs)` data-driven from `resources/chips/tested_chips.json`.

### Build & Release (v1.1.3)

- Added cross-platform build helper: `scripts/build_binaries.py`.
- Build helper now produces per-OS portable artifacts (`-portable.zip`).
- Release bundles now include bundled assets/attachments (`resources/`, `screenshots/`, and release docs).
- Added GitHub Actions workflow `.github/workflows/build-binaries.yml`:
  - matrix builds for Windows/Linux/macOS
  - artifact upload for portable outputs
  - release-event auto-attach to GitHub Release assets

### Documentation (v1.1.3)

- Expanded README screenshots section to include all current screenshots.
- Updated README build/release documentation for new artifact names and native installer modes.
- Updated tag/release examples to `v1.1.3`.

### Version (v1.1.3)

- Bumped application version in `flashgui.py`:
  - `VERSION = "1.1.3"`

### Build Artifact Targets (v1.1.3)

- `release/flashgui-v1.1.3-windows-x64-portable.zip`
- `release/flashgui-v1.1.3-linux-x64-portable.zip`
- `release/flashgui-v1.1.3-macos-x64-portable.zip`

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
