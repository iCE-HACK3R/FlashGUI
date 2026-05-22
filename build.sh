#!/usr/bin/env bash
# Build script for FlashGUI PyInstaller executable (Linux, PySide6-only)
# Usage: ./build.sh

set -euo pipefail

cd "$(dirname "$0")"

APP_NAME="flashgui"
ENTRY_FILE="flashgui.py"
ICON_FILE="resources/icons/flashrom.png"

echo "==============================================="
echo "FlashGUI - Linux Build Script"
echo "==============================================="
echo

if ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: python3 not found in PATH"
  echo "Please install Python 3.10+ and ensure python3 is available"
  exit 1
fi

if ! python3 -c 'import sys; raise SystemExit(0 if (3,10) <= sys.version_info[:2] < (3,14) else 1)'; then
  echo "ERROR: Unsupported Python version detected."
  echo "This project currently builds with CPython 3.10-3.13."
  echo "PySide6 wheels may be unavailable for your current interpreter."
  exit 1
fi

if ! python3 -c "import PySide6" >/dev/null 2>&1; then
  echo "ERROR: PySide6 is not installed in this environment."
  echo "Install dependencies first: python3 -m pip install -r requirements-build.txt"
  exit 1
fi

echo "[1/5] Installing PyInstaller..."
python3 -m pip install --quiet pyinstaller wheel

echo "[2/5] Verifying application syntax..."
python3 -c "import py_compile; py_compile.compile('flashgui.py', doraise=True)"

echo "[3/5] Cleaning previous builds..."
rm -rf build dist
rm -f "${APP_NAME}.spec"

echo "[4/5] Building executable with PyInstaller..."
PYI_ARGS=(
  --noconfirm
  --clean
  --name "${APP_NAME}"
  --onefile
  --windowed
  --add-data "resources:resources"
  --exclude-module tkinter
  --exclude-module _tkinter
)

if [[ -f "${ICON_FILE}" ]]; then
  PYI_ARGS+=(--icon "${ICON_FILE}")
fi

python3 -m PyInstaller "${PYI_ARGS[@]}" "${ENTRY_FILE}"

echo "[5/5] Verifying executable was created..."
if [[ -f "dist/${APP_NAME}" ]]; then
  echo
  echo "==============================================="
  echo "✓ BUILD SUCCESSFUL"
  echo "==============================================="
  echo
  echo "Executable: dist/${APP_NAME}"
  echo "Size: $(stat -c%s "dist/${APP_NAME}") bytes"
  echo
  echo "Next steps:"
  echo "  1. Test: ./dist/${APP_NAME}"
  echo "  2. Deploy: package dist/${APP_NAME} with notices/licenses"
  echo "  3. Include THIRD_PARTY_NOTICES.md in release artifacts"
  echo
else
  echo "ERROR: Executable not found at dist/${APP_NAME}"
  exit 1
fi
