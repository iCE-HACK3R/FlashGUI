# FlashGUI v1.1.3

## ✨ Highlights

- Fixed `Read Chip Info` parsing for `flashprog -V` (`probe_spi_rdid` / `SPI_RDID` chip-id formats).
- Fixed `Write Protection` extraction in `About ROM` for `flashprog --flash-name` output.
- `Read ROM` auto filename now includes tool prefix:
  - `FR_...` for flashrom
  - `FP_...` for flashprog
- `Tested Chips (ROMs)` is now data-driven from `resources/chips/tested_chips.json`.

## 📦 Build & Release Improvements

- Added `scripts/build_binaries.py` for cross-platform packaging.
- Release outputs are now portable-only per OS.
- Bundles now include assets/attachments (`resources/`, `screenshots/`, and key release docs).
- Added CI matrix workflow for Windows/Linux/macOS builds.
- Release event now auto-attaches artifacts to GitHub Releases.

## 🖼️ Documentation

- README screenshots refreshed to include all current screenshots.
- README build/release docs updated for portable/installer/native artifact flow.

## 📁 Expected Artifacts

- `flashgui-v1.1.3-windows-x64-portable.zip`
- `flashgui-v1.1.3-linux-x64-portable.zip`
- `flashgui-v1.1.3-macos-x64-portable.zip`
