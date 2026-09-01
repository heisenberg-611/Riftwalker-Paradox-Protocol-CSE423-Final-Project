@echo off
setlocal enabledelayedexpansion
title Riftwalker: Paradox Protocol - Requirements Installer

echo ========================================================================
echo    RIFTWALKER: PARADOX PROTOCOL — DEPENDENCY INSTALLER
echo ========================================================================
echo.

set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%~dp0..\"

:: 1. Detect Python executable
set "PYTHON_EXE="

if exist "%PROJECT_ROOT%.venv\Scripts\python.exe" (
    set "PYTHON_EXE=%PROJECT_ROOT%.venv\Scripts\python.exe"
    echo [INFO] Detected virtual environment in .venv\
    goto :found_python
)

where python >nul 2>nul
if %errorlevel% equ 0 (
    set "PYTHON_EXE=python"
    goto :found_python
)

where py >nul 2>nul
if %errorlevel% equ 0 (
    set "PYTHON_EXE=py"
    goto :found_python
)

where python3 >nul 2>nul
if %errorlevel% equ 0 (
    set "PYTHON_EXE=python3"
    goto :found_python
)

:found_python
if not defined PYTHON_EXE (
    echo [ERROR] Python was not found in your system PATH!
    echo.
    echo Please install Python 3.8 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo IMPORTANT: Make sure to check the box:
    echo   "Add Python to PATH" during installation!
    echo.
    pause
    exit /b 1
)

echo [OK] Using Python: %PYTHON_EXE%
echo.

:: 2. Upgrade pip (optional) and install all requirements with test verification
echo [INFO] Verifying and installing requirements...
"%PYTHON_EXE%" "%SCRIPT_DIR%check_requirements.py" --install --test

echo.
echo ========================================================================
echo  Requirements check & installation finished!
echo  To launch the game, simply double-click: run_game.bat
echo ========================================================================
echo.
pause
