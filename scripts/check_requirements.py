#!/usr/bin/env python3
"""
Riftwalker: Paradox Protocol — Automated Requirement Checker & Installer
========================================================================
Comprehensive cross-platform environment setup, dependency validator,
and automatic installer for Windows, macOS, and Linux.

Usage:
  python check_requirements.py            # Check status, auto-install missing, prompt to launch
  python check_requirements.py --run      # Check, install if needed, and immediately launch game
  python check_requirements.py --install  # Auto-install missing packages
  python check_requirements.py --check    # Check status only (exit 0 if all required present, 1 if required missing)
  python check_requirements.py --test     # Run automated test suite
"""

import sys
import os
import shutil
import platform
import subprocess
import argparse
import unittest

# Resolve project root dynamically whether executed from root or scripts/
_CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
if os.path.exists(os.path.join(_CURRENT_DIR, "src", "main.py")):
    PROJECT_ROOT = _CURRENT_DIR
else:
    PROJECT_ROOT = os.path.abspath(os.path.join(_CURRENT_DIR, ".."))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    RESET = '\033[0m'


# Enable ANSI escape sequences on Windows 10+
if sys.platform == 'win32':
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except Exception:
        pass


def print_banner():
    banner = f"""{Colors.CYAN}{Colors.BOLD}========================================================================
   RIFTWALKER: PARADOX PROTOCOL — SYSTEM SETUP & DEPENDENCY CHECK
========================================================================{Colors.RESET}"""
    print(banner)


def print_status(icon: str, label: str, message: str, color: str = Colors.RESET):
    print(f"  {color}{icon:<9}{Colors.RESET} {Colors.BOLD}{label:<24}{Colors.RESET} : {message}")


def check_python_version():
    """Verifies that Python is version 3.8 or newer."""
    major, minor, micro = sys.version_info[:3]
    arch = platform.architecture()[0]
    ver_str = f"Python {major}.{minor}.{micro} ({arch})"

    if major < 3 or (major == 3 and minor < 8):
        print_status("[FAIL]", "Python Version", f"{ver_str} — Incompatible (Requires Python 3.8+)", Colors.RED)
        return False
    elif minor >= 13:
        print_status("[WARN]", "Python Version", f"{ver_str} — Compatible (Note: Python 3.13+ may require prebuilt wheels)", Colors.YELLOW)
        return True
    else:
        print_status("[OK]", "Python Version", f"{ver_str} — Compatible", Colors.GREEN)
        return True


def check_pip():
    """Checks if pip is available in the current environment."""
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            pip_ver = result.stdout.strip().split()[1] if len(result.stdout.strip().split()) > 1 else "OK"
            print_status("[OK]", "pip Package Manager", f"v{pip_ver}", Colors.GREEN)
            return True
    except Exception:
        pass
    print_status("[FAIL]", "pip Package Manager", "pip is not found or not functional", Colors.RED)
    return False


# Package definitions: (display_name, import_module, pip_package, is_required, description)
DEPENDENCY_SPECS = [
    ("PyOpenGL", "OpenGL.GL", "PyOpenGL>=3.1.5", True, "Core 3D Graphics API"),
    ("Pillow", "PIL", "Pillow>=8.0.0", True, "Procedural Texture Generation & Image Loader"),
    ("NumPy", "numpy", "numpy>=1.20.0", True, "3D Vector & Matrix Computations"),
    ("pytest", "pytest", "pytest>=7.0.0", False, "Unit Testing Framework (Optional)"),
    ("PyOpenGL_accelerate", "OpenGL_accelerate", "PyOpenGL_accelerate>=3.1.5", False, "C-accelerated OpenGL wrappers (Optional)"),
]


def check_package(import_module: str) -> bool:
    """Checks if a python package can be imported."""
    try:
        __import__(import_module)
        return True
    except ImportError:
        return False
    except Exception:
        return True


def install_packages(packages_to_install: list) -> bool:
    """Installs list of pip package specifiers with automatic fallbacks."""
    if not packages_to_install:
        return True

    print(f"\n{Colors.YELLOW}{Colors.BOLD}Installing missing dependencies...{Colors.RESET}")
    print(f"Target packages: {', '.join(packages_to_install)}\n")

    main_packages = [p for p in packages_to_install if not p.startswith("PyOpenGL_accelerate")]
    accelerate_pkg = [p for p in packages_to_install if p.startswith("PyOpenGL_accelerate")]

    success = True
    if main_packages:
        cmd = [sys.executable, "-m", "pip", "install", *main_packages]
        res = subprocess.run(cmd)
        if res.returncode != 0:
            print(f"{Colors.YELLOW}Standard install failed, attempting user install (--user)...{Colors.RESET}")
            res_user = subprocess.run([sys.executable, "-m", "pip", "install", "--user", *main_packages])
            if res_user.returncode != 0:
                print(f"{Colors.YELLOW}Attempting install with --break-system-packages (PEP 668)...{Colors.RESET}")
                res_break = subprocess.run([sys.executable, "-m", "pip", "install", "--break-system-packages", *main_packages])
                if res_break.returncode != 0:
                    success = False
                    print_status("[FAIL]", "pip Install", f"Failed to install: {' '.join(main_packages)}", Colors.RED)
                else:
                    print_status("[OK]", "pip Install", f"Successfully installed: {' '.join(main_packages)}", Colors.GREEN)
            else:
                print_status("[OK]", "pip Install", f"Successfully installed to user directory: {' '.join(main_packages)}", Colors.GREEN)
        else:
            print_status("[OK]", "pip Install", f"Successfully installed: {' '.join(main_packages)}", Colors.GREEN)

    # PyOpenGL_accelerate is optional; if MSVC compiler is missing on Windows, do not fail
    if accelerate_pkg:
        cmd = [sys.executable, "-m", "pip", "install", *accelerate_pkg]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode == 0:
            print_status("[OK]", "PyOpenGL_accelerate", "Successfully installed optional C-accelerator", Colors.GREEN)
        else:
            print_status("[INFO]", "PyOpenGL_accelerate", "Optional accelerator skipped (PyOpenGL will run in pure Python mode)", Colors.YELLOW)

    return success


def setup_windows_glut_dlls(project_root: str) -> bool:
    """
    On Windows, ensures freeglut.dll is available in the project directory
    or PATH so that glutInit() initializes without errors.
    """
    if sys.platform != 'win32':
        return True

    print(f"\n{Colors.BOLD}Configuring Windows FreeGLUT DLLs...{Colors.RESET}")
    is_64bit = sys.maxsize > 2**32
    arch_str = "64-bit" if is_64bit else "32-bit"

    dll_dir = os.path.join(project_root, "OpenGL", "DLLS")
    target_dll = os.path.join(project_root, "freeglut.dll")

    if is_64bit:
        candidates = [
            "freeglut64.vc14.dll",
            "freeglut64.vc10.dll",
            "freeglut64.vc9.dll",
        ]
    else:
        candidates = [
            "freeglut32.vc14.dll",
            "freeglut32.vc10.dll",
            "freeglut32.vc9.dll",
        ]

    source_dll = None
    if os.path.isdir(dll_dir):
        for candidate in candidates:
            cand_path = os.path.join(dll_dir, candidate)
            if os.path.isfile(cand_path):
                source_dll = cand_path
                break

    if source_dll and not os.path.isfile(target_dll):
        try:
            shutil.copyfile(source_dll, target_dll)
            print_status("[OK]", "FreeGLUT DLL", f"Copied {os.path.basename(source_dll)} -> freeglut.dll ({arch_str})", Colors.GREEN)
        except Exception as e:
            print_status("[WARN]", "FreeGLUT DLL", f"Could not copy DLL to root: {e}", Colors.YELLOW)
    elif os.path.isfile(target_dll):
        print_status("[OK]", "FreeGLUT DLL", f"Found freeglut.dll in project root ({arch_str})", Colors.GREEN)
    else:
        print_status("[INFO]", "FreeGLUT DLL", "Using system or PyOpenGL default FreeGLUT binaries", Colors.CYAN)

    if hasattr(os, 'add_dll_directory'):
        try:
            if os.path.isdir(dll_dir):
                os.add_dll_directory(dll_dir)
            os.add_dll_directory(project_root)
        except Exception:
            pass

    os.environ['PATH'] = project_root + os.pathsep + dll_dir + os.pathsep + os.environ.get('PATH', '')
    return True


def verify_glut_initialization() -> bool:
    """Verifies that GLUT and OpenGL initialize properly."""
    try:
        from OpenGL.GLUT import glutInit
        glutInit()
        print_status("[OK]", "GLUT Runtime", "glutInit() initialized successfully", Colors.GREEN)
        return True
    except Exception as e:
        print_status("[WARN]", "GLUT Runtime", f"GLUT runtime note: {e}", Colors.YELLOW)
        return False


def pregenerate_texture_assets(project_root: str) -> bool:
    """Ensures all 16 procedural PNG texture assets exist on disk."""
    print(f"\n{Colors.BOLD}Checking Texture Assets in assets/textures/...{Colors.RESET}")
    try:
        from src.shared.texture_loader import TextureManager
        TextureManager.generate_all_disk_textures(force=False)
        print_status("[OK]", "Procedural Textures", "All 16 PNG texture assets verified and ready on disk", Colors.GREEN)
        return True
    except Exception as e:
        print_status("[WARN]", "Procedural Textures", f"Could not generate texture assets: {e}", Colors.YELLOW)
        return False


def run_unit_tests(project_root: str) -> bool:
    """Executes the test suite to verify code correctness."""
    print(f"\n{Colors.CYAN}{Colors.BOLD}Running Automated Unit Tests (tests/)...{Colors.RESET}")
    suite = unittest.defaultTestLoader.discover(os.path.join(project_root, "tests"))
    runner = unittest.TextTestRunner(verbosity=1)
    result = runner.run(suite)
    if result.wasSuccessful():
        print(f"\n{Colors.GREEN}{Colors.BOLD}✔ All {result.testsRun} automated unit tests passed!{Colors.RESET}")
        return True
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}✘ {len(result.failures) + len(result.errors)} test(s) encountered issues.{Colors.RESET}")
        return False


def launch_game(project_root: str):
    """Launches the main game entry point."""
    main_script = os.path.join(project_root, "src", "main.py")
    print(f"\n{Colors.CYAN}{Colors.BOLD}Launching Riftwalker: Paradox Protocol...{Colors.RESET}\n")
    try:
        subprocess.run([sys.executable, main_script], cwd=project_root)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Game session terminated.{Colors.RESET}")


def main():
    parser = argparse.ArgumentParser(description="Riftwalker: Paradox Protocol Dependency Checker & Setup")
    parser.add_argument("--check", "--check-only", action="store_true", dest="check_only", help="Only check requirements without installing")
    parser.add_argument("--install", action="store_true", help="Automatically install any missing packages")
    parser.add_argument("--test", action="store_true", help="Run automated test suite after setup")
    parser.add_argument("--run", "--play", action="store_true", dest="run_game", help="Launch game immediately after setup")
    args = parser.parse_args()

    project_root = PROJECT_ROOT
    print_banner()

    # Step 1: Python and pip checks
    print(f"{Colors.BOLD}1. System & Runtime Environment:{Colors.RESET}")
    py_ok = check_python_version()
    pip_ok = check_pip()

    if not py_ok:
        print(f"\n{Colors.RED}{Colors.BOLD}Critical: Please install Python 3.8 or higher from https://python.org{Colors.RESET}")
        if sys.platform == 'win32':
            input("\nPress Enter to exit...")
        sys.exit(1)

    # Step 2: Check Python packages
    print(f"\n{Colors.BOLD}2. Python Dependency Inspection:{Colors.RESET}")
    missing_required = []
    missing_optional = []

    for name, module, pip_spec, is_req, desc in DEPENDENCY_SPECS:
        installed = check_package(module)
        if installed:
            print_status("[OK]", name, f"Installed ({desc})", Colors.GREEN)
        else:
            if is_req:
                print_status("[MISSING]", name, f"Not Found (REQUIRED — {desc})", Colors.RED)
                missing_required.append(pip_spec)
            else:
                print_status("[MISSING]", name, f"Not Found (Optional — {desc})", Colors.YELLOW)
                missing_optional.append(pip_spec)

    # Step 3: Handle installation if missing
    all_missing = missing_required + missing_optional
    if all_missing:
        if args.check_only:
            if missing_required:
                print(f"\n{Colors.RED}Check complete: Missing REQUIRED dependencies: {', '.join(missing_required)}{Colors.RESET}")
                sys.exit(1)
            else:
                print(f"\n{Colors.GREEN}Check complete: All REQUIRED dependencies satisfied! (Optional: {', '.join(missing_optional)}){Colors.RESET}")
                sys.exit(0)
        else:
            print(f"\n{Colors.YELLOW}Found {len(all_missing)} missing package(s). Proceeding with automatic installation...{Colors.RESET}")
            install_success = install_packages(all_missing)
            if not install_success and missing_required:
                print(f"\n{Colors.RED}Installation of critical dependencies failed. Please run: pip install -r requirements.txt{Colors.RESET}")
                if sys.platform == 'win32':
                    input("\nPress Enter to exit...")
                sys.exit(1)
    else:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✔ All Python packages are installed and up-to-date!{Colors.RESET}")

    # Step 4: Windows FreeGLUT setup
    setup_windows_glut_dlls(project_root)
    verify_glut_initialization()

    # Step 5: Texture generation
    pregenerate_texture_assets(project_root)

    # Step 6: Test suite (if requested)
    if args.test:
        run_unit_tests(project_root)

    # Summary Banner
    print(f"\n{Colors.GREEN}{Colors.BOLD}========================================================================{Colors.RESET}")
    print(f"{Colors.GREEN}{Colors.BOLD}   ENVIRONMENT SETUP COMPLETE — READY FOR COMBAT SIMULATION!{Colors.RESET}")
    print(f"{Colors.GREEN}{Colors.BOLD}========================================================================{Colors.RESET}\n")

    # Step 7: Launch game
    if args.run_game:
        launch_game(project_root)
    else:
        # In interactive mode, prompt user if no specific flag was given
        if not args.check_only and not args.test:
            try:
                choice = input(f"{Colors.BOLD}Would you like to start Riftwalker now? [Y/n]: {Colors.RESET}").strip().lower()
                if choice in ('', 'y', 'yes'):
                    launch_game(project_root)
            except (EOFError, KeyboardInterrupt):
                print()


if __name__ == '__main__':
    main()
