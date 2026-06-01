# Bundled tools

Place embedded tool binaries here before packaging.

Expected paths:

- `tools/windows-x64/flashrom.exe`
- `tools/windows-x64/flashprog.exe`
- `tools/windows-x64/minipro.exe`
- `tools/windows-x64/fwinfo.exe`
- `tools/linux-x64/flashrom`
- `tools/linux-x64/flashprog`
- `tools/linux-x64/minipro`
- `tools/linux-x64/fwinfo`
- `tools/macos-x64/flashrom`
- `tools/macos-x64/flashprog`
- `tools/macos-x64/minipro`
- `tools/macos-x64/fwinfo`

`flashgui` will automatically set:

- `FLASHGUI_FLASHROM_BIN`
- `FLASHGUI_FLASHPROG_BIN`
- `FLASHGUI_MINIPRO_BIN`
- `FLASHGUI_FWINFO_BIN`

for the backend when these files exist.

If bundled binaries are missing, backend falls back to system PATH.
