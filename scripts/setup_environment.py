#!/usr/bin/env python3
"""
Riftwalker: Paradox Protocol — Environment Setup Alias
Convenience wrapper that runs check_requirements.py.
"""
import sys
import os
import subprocess

if __name__ == '__main__':
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'check_requirements.py')
    cmd = [sys.executable, script_path] + sys.argv[1:]
    sys.exit(subprocess.call(cmd))
