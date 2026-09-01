#!/usr/bin/env bash
# Riftwalker: Paradox Protocol — Unix / macOS / Linux Launcher
# Usage: ./run_game.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR" || exit 1

PYTHON_EXE=""

if [ -f "$SCRIPT_DIR/.venv/bin/python" ]; then
    PYTHON_EXE="$SCRIPT_DIR/.venv/bin/python"
elif command -v python3 &>/dev/null; then
    PYTHON_EXE="python3"
elif command -v python &>/dev/null; then
    PYTHON_EXE="python"
fi

if [ -z "$PYTHON_EXE" ]; then
    echo "[ERROR] Python 3 is not installed or not in PATH."
    echo "Please install Python 3.8+ from https://python.org"
    exit 1
fi

"$PYTHON_EXE" "$SCRIPT_DIR/check_requirements.py" --run "$@"
