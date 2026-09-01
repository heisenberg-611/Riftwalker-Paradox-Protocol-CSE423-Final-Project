# Riftwalker: Paradox Protocol — PowerShell Launcher
# Usage: .\run_game.ps1

$ErrorActionPreference = "Continue"

Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host "   RIFTWALKER: PARADOX PROTOCOL — POWERSHELL LAUNCHER" -ForegroundColor Cyan
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host ""

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonCmd = $null

# Check virtual environment first
if (Test-Path "$scriptDir\.venv\Scripts\python.exe") {
    $pythonCmd = "$scriptDir\.venv\Scripts\python.exe"
    Write-Host "[INFO] Using virtual environment Python: $pythonCmd" -ForegroundColor DarkCyan
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCmd = "python"
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    $pythonCmd = "py"
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    $pythonCmd = "python3"
}

if (-not $pythonCmd) {
    Write-Host "[ERROR] Python was not found in your system PATH!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Python 3.8 or higher from: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "Make sure to check the box 'Add Python to PATH' during installation." -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit..."
    Exit 1
}

$scriptPath = "$scriptDir\scripts\check_requirements.py"
if (-not (Test-Path $scriptPath)) {
    $scriptPath = "$scriptDir\check_requirements.py"
}

Write-Host "[OK] Using Python: $pythonCmd" -ForegroundColor Green
Write-Host ""

# Run requirements checker and start the game
& $pythonCmd "$scriptPath" --run
