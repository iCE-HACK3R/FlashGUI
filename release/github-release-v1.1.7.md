# FlashGUI v1.1.7

## ✨ Highlights

- Hardened flashrom chip autodetection so chip names emitted in **single quotes** and with **lowercase** detection keywords are recognized.
  - Fixes "No chip detected" on FT232H probes that reported `found Winbond flash chip 'W25Q64JVSIQ' ...`
  - Applies to both Qt (`flashgui.py`) and legacy Tk (`flashgui_legacy.py`) detection paths.
- CI: Linux runner now installs `libegl1` / `libgl1` so PySide6 imports succeed during tests.
- README: re-added `python3 ...` workflow notes for Linux/macOS users.

## 🛠️ Reliability / QA

- Added `tests/test_chip_detection.py` covering single-quoted chip names + FT232H programmer hint parsing.
- Existing suites pass:
  - `tests/test_minipro_detection.py`
  - `tests/test_project_layout.py`
  - `tests/test_python_syntax.py`

## 📁 Artifacts

- `flashgui-v1.1.7-windows-x64-portable.zip`
- `flashgui-v1.1.7-linux-x64-portable.zip`
- `flashgui-v1.1.7-macos-x64-portable.zip`
