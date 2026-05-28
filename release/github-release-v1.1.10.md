# FlashGUI v1.1.10

KDE native file dialog release.

## What’s new

- **KDE/Plasma native file dialogs in Qt**
  - FlashGUI now prefers KDE `kdialog` for open/save/folder pickers when:
    - native dialogs are enabled,
    - the app is running on Linux,
    - KDE/Plasma is detected,
    - and `kdialog` is installed.

- **Safe fallback behavior**
  - If `kdialog` is unavailable or cannot be invoked successfully, FlashGUI falls back to the existing Qt dialog path.
  - If the user cancels the KDE dialog, FlashGUI returns cleanly without opening a second dialog.

- **Regression coverage expanded**
  - Added tests for KDE dialog gating and wrapper behavior.
  - Added automated checklist coverage for theme/settings/layout persistence and release-gate regressions.

## Why this matters

This release targets GitHub issue **#5**: KDE users requested truly native file dialogs instead of the Qt fallback-only path. `v1.1.10` keeps the fix tightly scoped to KDE/Linux while preserving existing behavior elsewhere.

## Version

- `flashgui.py`: `VERSION = "1.1.10"`
- `flashgui_legacy.py`: `VERSION = "1.1.10"`

## Suggested artifacts

- `flashgui-v1.1.10-windows-x64-portable.zip`
- `flashgui-v1.1.10-linux-x64-portable.zip`
- `flashgui-v1.1.10-macos-arm64-portable.zip`
- `flashgui-v1.1.10-macos-x64-portable.zip`

## Issue #5 closeout note

Please validate on KDE/Plasma using **latest release v1.1.10**:

1. Open-file dialog
2. Save-file dialog
3. Existing-directory dialog
4. Cancel each once and confirm no second dialog appears

If a KDE-specific edge case remains, open a follow-up issue with:

- distro + version
- KDE/Plasma version
- whether `kdialog` is installed
- exact picker flow that failed
- relevant log excerpt
