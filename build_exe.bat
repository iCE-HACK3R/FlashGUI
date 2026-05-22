@echo off
REM Build script for FlashGUI PyInstaller executable (PySide6-only)
REM Usage: build_exe.bat

setlocal enabledelayedexpansion
cd /d "%~dp0"

set "APP_NAME=flashgui"
set "ENTRY_FILE=flashgui.py"
set "ICON_FILE=resources\icons\flashrom.ico"
set "ICON_ARG="
if "%PYTHON_CMD%"=="" set "PYTHON_CMD=python"

if exist "%ICON_FILE%" (
    set "ICON_ARG=--icon=%ICON_FILE%"
)

echo ===============================================
echo FlashGUI - Build Executable Script
echo ===============================================
echo.

REM Check Python is installed
%PYTHON_CMD% --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python command not found: %PYTHON_CMD%
    echo Please install Python 3.10+ and ensure it is available.
    echo Tip: set PYTHON_CMD to a specific interpreter, e.g.:
    echo   set PYTHON_CMD=py -3.12
    pause
    exit /b 1
)

%PYTHON_CMD% -c "import sys; raise SystemExit(0 if (3,10) <= sys.version_info[:2] < (3,14) else 1)" >nul 2>&1
if errorlevel 1 (
    echo ERROR: Unsupported Python version detected.
    echo This project currently builds with CPython 3.10-3.13.
    echo PySide6 wheels are not available for your current interpreter.
    echo Tip: use official python.org CPython 3.12 x64 for Windows builds.
    echo You can run with: set PYTHON_CMD=py -3.12
    pause
    exit /b 1
)

%PYTHON_CMD% -c "import PySide6" >nul 2>&1
if errorlevel 1 (
    echo ERROR: PySide6 is not installed in this environment.
    echo Install dependencies first:
    echo   %PYTHON_CMD% -m pip install -r requirements-build.txt
    pause
    exit /b 1
)

echo [1/5] Installing PyInstaller...
%PYTHON_CMD% -m pip install pyinstaller wheel --quiet
if errorlevel 1 (
    echo ERROR: Failed to install PyInstaller
    pause
    exit /b 1
)

echo [2/5] Verifying application can be imported...
%PYTHON_CMD% -c "import py_compile; py_compile.compile('flashgui.py', doraise=True); print('ok')" >nul 2>&1
if errorlevel 1 (
    echo ERROR: Application import failed
    echo Check that %ENTRY_FILE% exists and is valid
    pause
    exit /b 1
)

echo [3/5] Cleaning previous builds...
rmdir /s /q "build" 2>nul
rmdir /s /q "dist" 2>nul
del /q "%APP_NAME%.spec" 2>nul

echo [4/5] Building executable with PyInstaller...
%PYTHON_CMD% -m PyInstaller ^
    --noconfirm ^
    --clean ^
    --name=%APP_NAME% ^
    --onefile ^
    --windowed ^
    %ICON_ARG% ^
    --add-data="resources;resources" ^
    --exclude-module=tkinter ^
    --exclude-module=_tkinter ^
    %ENTRY_FILE%

if errorlevel 1 (
    echo ERROR: PyInstaller build failed
    echo Check console output for details
    pause
    exit /b 1
)

echo [5/5] Verifying executable was created...
if exist "dist\%APP_NAME%.exe" (
    echo.
    echo ===============================================
    echo ✓ BUILD SUCCESSFUL
    echo ===============================================
    echo.
    echo Executable: dist\%APP_NAME%.exe
    echo Size: 
    for %%A in (dist\%APP_NAME%.exe) do echo   %%~zA bytes
    echo.
    echo Next steps:
    echo   1. Test: dist\%APP_NAME%.exe
    echo   2. Deploy: Copy dist\%APP_NAME%.exe (and any required docs/licenses)
    echo   3. Distribute: Package with THIRD_PARTY_NOTICES.md and licenses
    echo.
) else (
    echo ERROR: Executable not found at dist\%APP_NAME%.exe
    pause
    exit /b 1
)

echo Build complete. Press any key to continue...
pause >nul
exit /b 0
