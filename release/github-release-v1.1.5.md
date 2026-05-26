# FlashGUI v1.1.5

## ✨ Highlights

- About ROM for **Minipro** now combines both commands:
  - `minipro -p <chip> -D` for **Chip ID**
  - `minipro -d <chip>` for model/vendor/size and remaining details
- Added remove-chip safety confirmation before Minipro hardware self-test (`-t`) in both Tk and Qt flows.
- Kept prior Minipro operation improvements (progress normalization, erase with `-E`, FW Info `.dat` workflow, Binwalk split actions).

## 🛠️ Build / Release Improvements

- Hardened `scripts/build_binaries.py` with a PyInstaller preflight check and clearer interpreter guidance.
- Documented Windows interpreter caveat where `python3` may resolve to MSYS/MinGW; README now recommends `python` from activated venv.

## 📁 Artifacts

- `flashgui-v1.1.5-windows-x64-portable.zip`
- `flashgui-v1.1.5-linux-x64-portable.zip`
- `flashgui-v1.1.5-macos-x64-portable.zip`
