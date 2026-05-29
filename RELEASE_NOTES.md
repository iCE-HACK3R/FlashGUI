# Release Notes

## v1.1.11

### Highlights (v1.1.11)

- Merged `#7`: expanded KDE native dialog regression coverage for the v1.1.10 dialog fix.
  - Added broad structural and functional tests for `_is_kde_desktop`, `_effective_use_native_file_dialogs`, `_can_use_kdialog`, and `_run_kdialog` cancel/success/exception behavior.
  - Reinforces KDE safety guarantees: prefer `kdialog` when eligible, avoid Qt native picker on KDE, and preserve clean fallback behavior.
- Merged `#8`: security hardening for runtime/storage paths in both Qt and legacy Tk flows.
  - Settings writes now enforce owner-only permissions (`0o600`).
  - Font cache moved from world-readable temp paths to user-private cache directories.
  - Downloaded font files now require valid TTF/OTF signatures before acceptance.
  - Temporary ROM operation directories moved to app-private locations.
  - Added binary-path safety validation for environment/config overrides.

### Version (v1.1.11)

- Bumped application versions:
  - `flashgui.py`: `VERSION = "1.1.11"`
  - `flashgui_legacy.py`: `VERSION = "1.1.11"`

### Build Artifact Targets (v1.1.11)

- `release/flashgui-v1.1.11-windows-x64-portable.zip`
- `release/flashgui-v1.1.11-linux-x64-portable.zip`
- `release/flashgui-v1.1.11-macos-arm64-portable.zip`
- `release/flashgui-v1.1.11-macos-x64-portable.zip`

## v1.1.10

### Highlights (v1.1.10)

- Qt UI: added **KDE/Plasma native file dialog support** using `kdialog` for open/save/folder pickers when native dialogs are enabled.
- Qt UI: kept dialog behavior **KDE-only and Linux-only**, preserving existing behavior on Windows, macOS, and non-KDE Linux desktops.
- Qt UI: added **cancel-safe fallback handling** so canceling a KDE native picker does not open a second Qt dialog.
- Tests: added automated regression coverage for KDE dialog gating and expanded automated checklist coverage for theme/settings/layout and release-gate issue checks.

### Version (v1.1.10)

- Bumped application versions:
  - `flashgui.py`: `VERSION = "1.1.10"`
  - `flashgui_legacy.py`: `VERSION = "1.1.10"`

### Issue #5 closeout target (v1.1.10)

- Addresses GitHub issue `#5` requesting native file dialogs on KDE desktop environments.
- Native dialog flow now prefers KDE `kdialog` when available and falls back to the Qt dialog path if KDE-native integration is unavailable at runtime.
- Recommended reporter validation on KDE/Plasma:
  - open file picker,
  - save file picker,
  - existing-directory picker,
  - confirm cancel does not trigger a second dialog.

## v1.1.9

### Highlights (v1.1.9)

- Qt UI: improved **global log splitter persistence** by autosaving splitter state when handles move (debounced), in addition to close-time save.
- Qt UI: added **Use native file dialogs** toggle in Settings → Behavior.
  - Default: enabled (native dialogs)
  - Optional: disable native dialogs to use Qt dialogs when mounted-drive visibility is problematic on specific host setups.
- Routed Qt file/folder pickers through the unified dialog-mode setting for ROM read/write/verify, tools page flows, and settings load/save paths.

### Version (v1.1.9)

- Bumped application versions:
  - `flashgui.py`: `VERSION = "1.1.9"`
  - `flashgui_legacy.py`: `VERSION = "1.1.9"`

### Issue #4 follow-up (v1.1.9)

- This release addresses the remaining UX hardening items tracked in the issue #4 umbrella.
- Reporter note: please verify behavior on the **latest release** and open a focused follow-up issue only if a specific symptom still reproduces.

## v1.1.8

### Highlights (v1.1.8)

- Added a user-tunable **FT232H SPI clock divisor** setting (Settings → Behavior). Default `4` (safe for both 1.8 V and 3.3 V targets); choose `2` for faster reads on 3.3 V-only setups.
- Honored on every flashrom probe / detect / read / write that uses the autodetected FT232H entry — the `_USB_PROGRAMMER_MAP` row for `0403:6014` is updated in place when the setting changes.
- New environment override `FLASHGUI_FT232H_DIVISOR=2|4` for power users and CI.
- Mirrored the same setting + UI control into the legacy Tk app (`flashgui_legacy.py`); the legacy FT232H entry now also emits `ft2232_spi:divisor=4,type=232h` instead of bare `ft2232_spi`.
- Added `macos-13` (Intel x64) build matrix entry so v1.1.8 ships both `macos-arm64` and `macos-x64` portable artifacts.

### Tests (v1.1.8)

- Added `tests/test_ft232h_divisor.py` with regression coverage for divisor normalization, in-place map mutation, and fallback behavior.

### Version (v1.1.8)

- Bumped application versions:
  - `flashgui.py`: `VERSION = "1.1.8"`
  - `flashgui_legacy.py`: `VERSION = "1.1.8"`

### Build Artifact Targets (v1.1.8)

- `release/flashgui-v1.1.8-windows-x64-portable.zip`
- `release/flashgui-v1.1.8-linux-x64-portable.zip`
- `release/flashgui-v1.1.8-macos-arm64-portable.zip`
- `release/flashgui-v1.1.8-macos-x64-portable.zip`

### Issue #4 checkpoint and follow-up flow (v1.1.8)

- Treat GitHub issue `#4` as a multi-topic umbrella report.
- Publish current code to `main` as a stabilization checkpoint.
- Keep `#4` open while follow-up symptoms are split into focused issues.
- Implemented in this checkpoint:
  - Detect ROM actions are blocked during active flash operations.
  - Oversized image writes are rejected in preflight with explicit size details.
- Ask reporter(s) to file one issue per remaining symptom with:
  - tool/programmer/chip details,
  - exact reproduction steps,
  - `Commands:` line from UI,
  - relevant global log excerpt.

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
- `release/flashgui-v1.1.7-macos-arm64-portable.zip` (note: `macos-latest` runner is now Apple Silicon; an Intel `macos-x64` build is added from v1.1.8 onward via a `macos-13` matrix entry)

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
