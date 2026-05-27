# FlashGUI v1.1.6

## ✨ Highlights

- Fixed FT232H programmer detection path for USB ID `0403:6014` by using:
  - `ft2232_spi:divisor=4,type=232h`
- Fixed Qt Settings page overflow/expansion behavior on constrained displays by changing **Systems & Settings** actions from one long row to a wrapped grid layout.
- Added regression tests covering:
  - FT232H mapping guard (`_USB_PROGRAMMER_MAP`)
  - Linux `lsusb` autodetect behavior in `_detect_programmer_usb()`

## 🛠️ Reliability / QA

- Focused tests and syntax checks pass:
  - `tests/test_minipro_detection.py`
  - `tests/test_python_syntax.py`
  - `python -m py_compile flashgui.py flashgui_legacy.py`

## 📁 Artifacts

- `flashgui-v1.1.6-windows-x64-portable.zip`
- `flashgui-v1.1.6-linux-x64-portable.zip`
- `flashgui-v1.1.6-macos-x64-portable.zip`
