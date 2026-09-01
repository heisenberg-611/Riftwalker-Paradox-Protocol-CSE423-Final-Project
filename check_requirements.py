#!/usr/bin/env python3
"""
Riftwalker: Paradox Protocol — Requirement Checker Forwarder
Forwards execution to scripts/check_requirements.py.
"""
import sys
import os
import subprocess

if __name__ == '__main__':
    target = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts', 'check_requirements.py')
    cmd = [sys.executable, target] + sys.argv[1:]
    sys.exit(subprocess.call(cmd))
