@echo off
setlocal enabledelayedexpansion
title Riftwalker: Paradox Protocol - Launcher

echo ========================================================================
echo    RIFTWALKER: PARADOX PROTOCOL — WINDOWS LAUNCHER
echo ========================================================================
echo.

:: 1. Detect Python executable
set "PYTHON_EXE="

:: Check virtual environment first if present
if exist "%~dp0.venv\Scripts\python.exe" (
    set "PYTHON_EXE=%~dp0.venv\Scripts\python.exe"
    echo [INFO] Detected active virtual environment in .venv\
    goto :found_python
)

:: Check system python
where python >nul 2>nul
if %errorlevel% equ 0 (
    set "PYTHON_EXE=python"
    goto :found_python
)

:: Check py launcher
where py >nul 2>nul
if %errorlevel% equ 0 (
    set "PYTHON_EXE=py"
    goto :found_python
)

:: Check python3
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

:: 2. Run automated check, missing dependencies installation, and launch game
"%PYTHON_EXE%" "%~dp0check_requirements.py" --run

if %errorlevel% neq 0 (
    echo.
    echo [INFO] Game process exited with code %errorlevel%.
    pause
)
