# FlashGUI v1.1.4

## ✨ Highlights

- Fixed Minipro progress handling while keeping `flashrom` / `flashprog` progress behavior unchanged.
- Reduced noisy Minipro output in live logs by filtering duplicated ANSI/status spam.
- Fixed Minipro erase operation by using the correct uppercase `-E` action flag.
- `FW Info` now prompts for a `.dat` file or a folder containing `.dat` files.
- Binwalk tooling now includes both:
  - `Binwalk ROMs` (scan)
  - `Binwalk Extract & Analize` (extract + analyze)
- Added **T48** to Help/About tested programmers.

## 🖼️ Screenshots & Docs

- Added/updated README screenshots for Minipro T48 init/read/write/verify/erase flows.
- Updated README release/tag examples to `v1.1.4`.
- Release notes updated in `RELEASE_NOTES.md`.

## 📁 Expected Artifacts

- `flashgui-v1.1.4-windows-x64-portable.zip`
- `flashgui-v1.1.4-linux-x64-portable.zip`
- `flashgui-v1.1.4-macos-x64-portable.zip`
