# Bundled tools

Place embedded tool binaries here before packaging.

Expected paths:

- `tools/windows-x64/flashrom.exe`
- `tools/windows-x64/flashprog.exe`
- `tools/linux-x64/flashrom`
- `tools/linux-x64/flashprog`

`flashgui` will automatically set:

- `FLASHGUI_FLASHROM_BIN`
- `FLASHGUI_FLASHPROG_BIN`

for the backend when these files exist.

If bundled binaries are missing, backend falls back to system PATH.
