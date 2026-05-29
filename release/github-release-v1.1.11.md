# FlashGUI v1.1.11

Security hardening + KDE regression coverage release.

## What’s new

- **KDE native-dialog regression coverage expanded**
  - Merged PR [#7](https://github.com/iCE-HACK3R/FlashGUI/pull/7).
  - Added broad structural and functional tests around KDE detection, native-dialog gating, `kdialog` eligibility, and cancel/success/exception handling in picker wrappers.

- **Security hardening in Qt + legacy paths**
  - Merged PR [#8](https://github.com/iCE-HACK3R/FlashGUI/pull/8).
  - Settings file writes now enforce owner-only permissions (`0o600`).
  - Font cache moved to user-private cache paths.
  - Downloaded font files are validated for expected TrueType/OpenType signatures.
  - Operation temp dirs moved to app-private paths.
  - Binary override paths are validated for unsafe traversal/metacharacter patterns.

## Why this matters

`v1.1.11` improves release confidence and local-host safety without changing normal flashing workflows. It locks in KDE dialog behavior with stronger tests and reduces risk from permissive filesystem/default path usage.

## Version

- `flashgui.py`: `VERSION = "1.1.11"`
- `flashgui_legacy.py`: `VERSION = "1.1.11"`

## Suggested artifacts

- `flashgui-v1.1.11-windows-x64-portable.zip`
- `flashgui-v1.1.11-linux-x64-portable.zip`
- `flashgui-v1.1.11-macos-arm64-portable.zip`
- `flashgui-v1.1.11-macos-x64-portable.zip`

## Validation checklist

1. Run focused suites:
   - `python -m pytest -q tests/test_qt_startup_responsiveness.py tests/test_python_syntax.py tests/test_legacy_parity_regression.py`
2. Run full suite:
   - `python -m pytest -q`
3. Spot-check:
   - KDE file-pickers (if available),
   - settings save permissions,
   - startup/runtime flows on Qt and legacy paths.
