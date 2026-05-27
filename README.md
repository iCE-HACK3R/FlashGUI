# flashgui

Desktop GUI for `flashrom`, `flashprog` & `minipro` focused on safer firmware operations and practical chip/datasheet workflows.

This repository currently ships as a Python desktop app (`flashgui.py`) with a Qt UI and a Tk fallback path.

## Latest release (v1.1.9)

- Added robust **global log pane splitter persistence** in Qt (autosaves on drag + on close).
- Added **Use native file dialogs** setting (Settings → Behavior) for systems where non-native dialogs improve mounted-drive visibility.
- Kept issue #4 stabilization flow: please re-test on the latest release and report any remaining symptom as a separate issue.

## Platform status

- Windows: tested
- Linux: tested
- macOS: **currently untested**

## What it does

- Detects and uses either `flashrom` or `flashprog` & `minipro` (if available) for supported operations
- Supports `minipro` workflows (including T48/T56 class programmers)
- Helps with programmer/chip probing and operation setup
- Supports safer workflows (backup-first habits, explicit write actions, status logging)
- Includes Binwalk tooling for ROM analysis and extract+analyze flows
- Includes datasheet resolution helpers (including handling ambiguous chip-ID matches)

## UI Feature Matrix (Tk vs Qt)

| Feature                                                         | Tk UI | Qt UI |
| --------------------------------------------------------------- | :---: | :---: |
| Tool selection (`flashrom` / `flashprog` / `minipro`)           |  ✅   |  ✅   |
| Programmer detection (including minipro hardware probe)         |  ✅   |  ✅   |
| Chip detect / ROM autodetect                                    |  ✅   |  ✅   |
| Read ROM workflow                                               |  ✅   |  ✅   |
| Write ROM workflow                                              |  ✅   |  ✅   |
| Verify ROM workflow                                             |  ✅   |  ✅   |
| Erase ROM workflow                                              |  ✅   |  ✅   |
| Write-Protect controls (non-minipro)                            |  ✅   |  ✅   |
| About ROM / chip info page                                      |  ✅   |  ✅   |
| Datasheet open + chip candidate resolution                      |  ✅   |  ✅   |
| Progress + completion status (`SHA256`, elapsed, result)        |  ✅   |  ✅   |
| Command preview + per-operation output log controls             |  ✅   |  ✅   |
| Startup settings validation + first-run setup prompt            |  ✅   |  ✅   |
| Settings page (paths, theme/font, behavior, diagnostics)        |  ✅   |  ✅   |
| Global log panel with font/verbose controls                     |  ➖   |  ✅   |
| Dedicated Tools page (Binwalk/hash/convert/diff/fwinfo helpers) |  ➖   |  ✅   |
| Serial Programmer Console (connect/send/receive terminal)       |  ➖   |  ✅   |
| Help & About page with update/help shortcuts                    |  ➖   |  ✅   |

Legend: ✅ = available in this UI, ➖ = not exposed in this UI.

## Screenshots

### About ROM / Help pages

![About ROM chip info (basic view)](screenshots/about-rom-chip-info-basic.png)

![About ROM chip info (verbose / write-protect)](screenshots/about-rom-chip-info-verbose-wp.png)

![Help & About page](screenshots/help-about.png)

### Read ROM flow

![Read ROM in progress (serprog, GD25Q128C, macOS)](screenshots/read-rom-progress-serprog-gd25q128c-mac.png)

![Read ROM completed (serprog, GD25Q128C, macOS)](screenshots/read-rom-complete-serprog-gd25q128c-mac.png)

![Read ROM completed (serprog, MX25V16066, Linux)](screenshots/read-rom-complete-serprog-mx25v16066-linux.png)

### Write / Verify / Erase flow

![Write ROM confirmation dialog (CH341A)](screenshots/write-rom-confirm-dialog-ch341a.png)

![Write ROM completed (CH341A, MX25L1605)](screenshots/write-rom-complete-ch341a-mx25l1605.png)

![Verify ROM completed (CH341A, MX25L1605)](screenshots/verify-rom-complete-ch341a-mx25l1605.png)

![Erase ROM confirmation dialog (CH341A, MX25L1605)](screenshots/erase-rom-confirm-ch341a-mx25l1605.png)

![Erase ROM completed (CH341A, MX25L1605)](screenshots/erase-rom-complete-ch341a-mx25l1605.png)

### Minipro T48 flow

![Minipro T48 initialization](screenshots/minipro-t48-init.png)

![Minipro T48 read progress](screenshots/minipro-t48-read-progress.png)

![Minipro T48 read completed](screenshots/minipro-t48-read-completed.png)

![Minipro T48 write progress](screenshots/minipro-t48-write-progress.png)

![Minipro T48 write completed](screenshots/minipro-t48-write-complete.png)

![Minipro T48 verify progress](screenshots/minipro-t48-verify-progress.png)

![Minipro T48 verify completed](screenshots/minipro-t48-verify-complete.png)

![Minipro T48 erase completed](screenshots/minipro-t48-erase-complete.png)

### Programmer terminal / console

![Programmer terminal](screenshots/programmer-terminal.png)

![Programmer terminal help](screenshots/programmer-terminal-help.png)

![Programmer terminal (Bus Pirate)](screenshots/programmer-terminal-bp.png)

![Programmer terminal (HydraBus)](screenshots/programmer-terminal-hb.png)

### Settings across platforms

![Settings on Windows](screenshots/settings-windows.png)

![Settings on Linux](screenshots/settings-linux.png)

![Settings on macOS](screenshots/settings-darwin.png)

## Quick start

1. Install Python 3.10+
1. Create a virtual environment:

- `python -m venv .venv`
- Linux/macOS alternative: `python3 -m venv .venv`

1. Activate the virtual environment:

- Linux/macOS: `source .venv/bin/activate`
- Windows (PowerShell): `.venv\Scripts\Activate.ps1`

1. Install dependencies:

- `python -m pip install -r requirements.txt`
- Linux/macOS alternative: `python3 -m pip install -r requirements.txt`

1. Run:

- `python flashgui.py`
- Linux/macOS alternative: `python3 flashgui.py`

Windows note: in some setups `python3` may resolve to MSYS/MinGW Python instead of your `.venv`; prefer `python` after activating your virtual environment.

If PySide6/Qt startup fails on Linux, the app will attempt a Tk fallback (`flashgui_legacy.py`).

## Usage

- Launch the app:
  - `python flashgui.py`
- Select tool/programmer, detect chip, then perform read/verify/write operations from the GUI.
- Keep `resources/` next to the executable/script so icons, datasheets, and optional tool bundles resolve correctly.

Settings persistence:

- Settings are stored in a per-user config file (not next to the executable).
  - Windows: `%APPDATA%/FlashGUI/flashgui_settings.json`
  - Linux: `$XDG_CONFIG_HOME/flashgui/flashgui_settings.json` (or `~/.config/flashgui/flashgui_settings.json`)
  - macOS: `~/Library/Application Support/flashgui/flashgui_settings.json`
- Optional override: set `FLASHGUI_SETTINGS_PATH` to use a custom settings file path.

## Development notes

- Use Python 3.10+ (CPython 3.10–3.13 recommended).
- If dependency installation fails, verify the Python interpreter/version first.
- For local checks, you can run `pytest` after installing development/build dependencies from `requirements-build.txt`.

## Build binaries (Windows/Linux/macOS)

Use the build helper script:

- `python scripts/build_binaries.py`

Optional target override (run on the matching OS):

- `python scripts/build_binaries.py --target windows`
- `python scripts/build_binaries.py --target linux`
- `python scripts/build_binaries.py --target macos`

What it does:

- Builds a one-file executable with PyInstaller
- Names output as `flashgui-<target>-<arch>` (plus `.exe` on Windows)
- Creates a **portable** release zip in `release/`:
  - `flashgui-v<version>-<target>-<arch>-portable.zip`
- Bundles app assets/attachments into releases (including `resources/`, `screenshots/`, and release docs)

Note: cross-compiling to a different OS is not supported in this script; run it on the target platform.

Optional flags:

- `python scripts/build_binaries.py --no-screenshots` (skip bundling screenshots)

## License

📜 License
MIT License — see `LICENSE` for details.

## Repository layout

- `flashgui.py` — main application entrypoint (Qt-first)
- `flashgui_legacy.py` — fallback/legacy UI path
- `flashgui_settings.json` — persisted UI/runtime settings
- `resources/`
  - `chips/` — chip metadata and hint maps
  - `datasheets/` — local datasheet cache
  - `icons/` — application icons
  - `tools/` — optional bundled tool binaries (`flashrom` / `flashprog` / `minipro`)
- `MANUAL_QA_CHECKLIST.md` — manual QA checklist used for release sanity checks

## Publishing / release notes

- Ensure acknowledgements and upstream links remain intact (see below).
- If distributing bundled third-party binaries, include their required license notices in your release artifacts.
- Use `THIRD_PARTY_NOTICES.md` as your release checklist and attribution baseline.
- `THIRD_PARTY_NOTICES.md` currently tracks notices for `flashrom`, `flashprog`, and `minipro`.
- Validate your release build with the checklist in `MANUAL_QA_CHECKLIST.md`.

Build/publish one-file executable with icon:

- `python -m PyInstaller --name=flashgui --onefile --icon=resources\icons\flashgui.ico flashgui.py`
- `python -m PyInstaller --name=flashgui --onefile --icon=resources/icons/flashgui.ico flashgui.py`

Or use the cross-platform helper:

- `python scripts/build_binaries.py`

To create a release that triggers the Windows/Linux/macOS GitHub Actions matrix:

- `python scripts/release.py`

Optional flags:

- `python scripts/release.py --skip-local-build` (skip the local build validation step)
- `python scripts/release.py --allow-dirty` (allow publishing with uncommitted changes)

Release bundle generated in this repo:

- `release/flashgui-v1.1.6-windows-x64-portable.zip`

GitHub publish flow (tag-based):

- Commit release changes (version bump, docs, screenshots)
- Create an annotated tag (example: `v1.1.6`)
- Push branch and tag to `origin`
- Create a GitHub Release from tag `v1.1.6`
- CI will build on Windows/Linux/macOS and auto-attach generated portable artifacts to that release

## Mentions & thanks

Big thanks to the open-source projects and documentation that made this app possible:

- [`flashrom/flashrom`](https://github.com/flashrom/flashrom) — core flashing engine and broad hardware support.
- [`SourceArcade/flashprog`](https://github.com/SourceArcade/flashprog) — actively maintained flashprog ecosystem.
- [`Jazzzny/iFR`](https://github.com/Jazzzny/iFR) — useful early Python GUI reference.
- [`KantBStoppd/FlashromGUI`](https://github.com/KantBStoppd/FlashromGUI) — community GUI project with safety/usability focus.

Helpful official docs we rely on and recommend:

- [flashrom classic CLI manpage](https://www.flashrom.org/classic_cli_manpage.html)
- [FT2232 SPI programmer notes](https://www.flashrom.org/supported_hw/supported_prog/ft2232_spi.html)
- [In-system programming guidance](https://www.flashrom.org/user_docs/in_system.html)

Also worth a look from the "flashrom gui" ecosystem search:

- [`RestlessGoose/QuickFlash`](https://github.com/RestlessGoose/QuickFlash) (archived)

> This project is an independent frontend and is not affiliated with or endorsed by the `flashrom` or `flashprog` maintainers.

## For the EZP2020 serprog FW

- [EZP2020_CH552x-FW](https://github.com/iCE-HACK3R/EZP2020_CH552x-FW)
