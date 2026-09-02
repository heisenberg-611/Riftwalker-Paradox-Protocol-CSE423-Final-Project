# 🎮 Riftwalker: Paradox Protocol — Complete Setup & Run Guide

Welcome to **Riftwalker: Paradox Protocol**! This guide is designed to get you and your team up and running in **under 2 minutes**, even if you are starting from a completely fresh Windows, macOS, or Linux computer.

---

## ⚡ Quick Start (TL;DR)

| Platform | Recommended Action |
|---|---|
| **Windows (1-Click)** | Double-click **[`run_game.bat`](file:///Users/dhrubojyoti/Projects/CSE423_LAB_Project/run_game.bat)** |
| **Windows (PowerShell)** | Run **`.\run_game.ps1`** |
| **macOS / Linux** | Run **`./run_game.sh`** |
| **Command Line (Any OS)** | Run **`python check_requirements.py --run`** |

> [!NOTE]
> The automated launch script **automatically checks** your Python packages, **installs any missing dependencies** (`PyOpenGL`, `Pillow`, `NumPy`), **configures Windows FreeGLUT DLLs**, **generates all textures**, and **starts the game**!

---

## 🐍 Step 1: If Python Is NOT Installed

If your system does not have Python installed yet, follow these simple steps:

### 🪟 Windows Setup (Most Common)

1. **Download Python:**
   - Go to the official Python download page: [python.org/downloads/windows](https://www.python.org/downloads/windows/)
   - Download the latest stable Python installer (e.g., **Python 3.10**, **3.11**, or **3.12** 64-bit installer).

2. **Run Installer (CRITICAL STEP):**
   - Open the downloaded `.exe` file (e.g., `python-3.11.x-amd64.exe`).
   - > [!CAUTION]
     > **YOU MUST CHECK THE BOX:**  
     > `☑ Add python.exe to PATH` (or `Add Python 3.x to PATH`) at the bottom of the first installer window!  
     > *If you skip this, Windows will not recognize the `python` command.*

3. **Complete Installation:**
   - Click **"Install Now"**.
   - If prompted with *"Disable path length limit"*, click **Yes/Disable**.
   - Click **Close**.

4. **Verify Installation:**
   - Press **`Win + R`**, type **`cmd`**, and press **Enter**.
   - Type:
     ```cmd
     python --version
     ```
   - If you see `Python 3.x.x`, Python is ready!

---

### 🍎 macOS Setup

1. **Via Homebrew (Recommended):**
   ```bash
   brew install python
   ```
2. **Or via Official Installer:**
   - Download the macOS installer from [python.org/downloads/macos](https://www.python.org/downloads/macos/).
   - Run the `.pkg` installer and follow the on-screen steps.
3. **Verify:**
   ```bash
   python3 --version
   ```

---

### 🐧 Linux (Ubuntu / Debian / Mint) Setup

1. Open your terminal and run:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-opengl freeglut3-dev
   ```
2. **Verify:**
   ```bash
   python3 --version
   ```

---

## 🚀 Step 2: Running the Game Using Scripts

Once Python is installed, launching the game requires **zero manual package configuration**:

### 🎯 Option A: Windows 1-Click Launch (Recommended)
1. Navigate to the project root folder.
2. Double-click **[`run_game.bat`](file:///Users/dhrubojyoti/Projects/CSE423_LAB_Project/run_game.bat)**.
3. What happens automatically:
   - ✔ Detects Python executable (`python`, `py`, or `.venv`).
   - ✔ Checks installed packages against `requirements.txt`.
   - ✔ Installs missing packages automatically via `pip`.
   - ✔ Resolves Windows FreeGLUT DLL dependencies from `OpenGL/DLLS`.
   - ✔ Pre-generates all 16 procedural texture PNG files in `assets/textures/`.
   - ✔ Launches the game window!

---

### 💻 Option B: Windows PowerShell
1. Open PowerShell in the project folder (or press **Shift + Right Click** → *Open PowerShell window here*).
2. Run:
   ```powershell
   .\run_game.ps1
   ```

---

### 🍏 Option C: macOS / Linux Terminal
1. Open your terminal in the project directory.
2. Run:
   ```bash
   ./run_game.sh
   ```

---

### ⚙️ Option D: Manual Command-Line Usage

You can also use the cross-platform diagnostic script [`check_requirements.py`](file:///Users/dhrubojyoti/Projects/CSE423_LAB_Project/check_requirements.py) directly:

```bash
# Check dependencies, auto-install missing packages, and launch game immediately:
python check_requirements.py --run

# Check dependency status only without installing:
python check_requirements.py --check

# Install dependencies and run the 44-test unit test suite:
python check_requirements.py --install --test

# Direct launch:
python src/main.py
```

---

## 🛠️ Step 3: Diagnostic & Troubleshooting Guide

| Issue / Error Message | Cause | Solution |
|---|---|---|
| `'python' is not recognized as an internal or external command` | Python was installed without checking *"Add Python to PATH"*. | Re-run the Python installer, select **Modify**, and check **`☑ Add Python to PATH`**, or restart your computer. |
| `OpenGL.error.NullFunctionError: Attempt to call an undefined function glutInit` | Missing FreeGLUT library on Windows. | Run via **`run_game.bat`** (which automatically links `OpenGL/DLLS/freeglut64.vc14.dll`), or copy `OpenGL/DLLS/freeglut64.vc14.dll` to project root as `freeglut.dll`. |
| `pip install PyOpenGL_accelerate failed` | Missing MSVC C++ Build Tools on Windows. | **No action needed!** The script automatically runs PyOpenGL in standard pure Python mode, which has 100% feature parity. |
| `externally-managed-environment (PEP 668)` | Homebrew/Linux system python package restrictions. | Run `python check_requirements.py` — it automatically detects this and applies user or break-system-package fallbacks, or create a virtual environment: `python3 -m venv .venv && source .venv/bin/activate`. |
| Game window closes immediately | A runtime error or missing dependency occurred. | Open Command Prompt (`cmd`), navigate to the folder, and run `python check_requirements.py --run` to see the diagnostic error output. |

---

## 🎮 Step 4: Controls & Gameplay Guide

### ⌨️ Controls Reference

| Key / Input | Action |
|---|---|
| **`W`, `A`, `S`, `D`** | Move Astronaut (Forward, Strafe Left, Backward, Strafe Right) |
| **Mouse Aim** | Look around & aim pitch/yaw |
| **Arrow Keys (`←`, `→`, `↑`, `↓`)** | Continuous smooth camera turn & pitch adjustment |
| **`Left Click` or `Space`** | Fire Hitscan Laser Rifle (with dynamic muzzle flare & recoil) |
| **`V` or `C`** | Toggle **1st-Person (FPS Viewmodel)** $\leftrightarrow$ **3rd-Person (Astronaut Rig)** |
| **`Q`** | **Chrono Slow (Time Dilation):** Requires 100% charge. Slows enemies/projectiles to 30% for 5.0s |
| **`F`** | **Interact / Rift Beacon Teleport:** Stand inside the beacon pad ($R \le 3.5\text{m}$) and press `F` |
| **`E` or `Shift`** | **Blink Dash:** Short-range evasive tactical dash |
| **`F11`** | Toggle Fullscreen |
| **`R`** | Restart Mission (on Game Over or Victory screens) |
| **`Esc`** | Exit Game |

---

## 🗺️ Mission Progression Flow

```
[🎬 Cinematic Intro]  ──(Press Space/Enter/S to Skip)──>
[🛰️ Arena 1: Kepler Relay] ──(Defeat Waves 1, 2, 3)──> [🔓 Rift Beacon Online (Cyan Glow)]
                                                              │
                                                        (Press F on Beacon)
                                                              ▼
[🌌 Arena 2: Sundered Rift] ──(Defeat Waves 1, 2, 3)──> [👑 Wave 4: Rift Guardian Boss]
                                                              │
                                                        (Eliminate Boss)
                                                              ▼
[🏆 Cinematic Victory Epilogue] ──(Rank S / A / B / C / D Summary)──> [Press R to Replay]
```

---

## 🧪 Running Unit Tests

To verify that all game math, physics, collision detection, and rendering subsystems are 100% operational, run:

```bash
python -m unittest discover -s tests
```
*(All 44 tests should pass with `OK`)*
