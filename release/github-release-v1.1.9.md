# FlashGUI v1.1.9

Qt persistence + dialog UX hardening release.

## What’s new

- **Global log splitter persistence (Qt) now autosaves during drag**
  - Splitter state is saved on handle movement (debounced), not only on app close.
  - Improves resilience when app/session closes unexpectedly.

- **New Settings toggle: `Use native file dialogs`**
  - Location: **Settings → Behavior**
  - Default: enabled (`true`)
  - When disabled, Qt non-native dialogs are used for file/folder pickers.
  - Useful when native dialogs have mounted-drive visibility quirks on some environments.

- **Unified file-dialog behavior in Qt flows**
  - Read/Write/Verify ROM file pickers
  - Tools file/folder pickers (`Binwalk Extract`, `Firmware Info`, `Firmware Update`)
  - Settings load/save JSON and log path pickers

## Why this matters

Issue #4 included usability concerns around visibility/persistence and file dialog behavior. v1.1.9 improves operational continuity and gives users control over dialog mode for problematic host setups.

## Version

- `flashgui.py`: `VERSION = "1.1.9"`
- `flashgui_legacy.py`: `VERSION = "1.1.9"`

## Suggested artifacts

- `flashgui-v1.1.9-windows-x64-portable.zip`
- `flashgui-v1.1.9-linux-x64-portable.zip`
- `flashgui-v1.1.9-macos-arm64-portable.zip`
- `flashgui-v1.1.9-macos-x64-portable.zip`

## Issue #4 closeout note

Please validate on **latest release v1.1.9**. If any symptom remains, open a separate issue per symptom with:

1. Tool + programmer + chip
2. Exact repro steps
3. `Commands:` line shown in UI
4. Relevant global log excerpt
