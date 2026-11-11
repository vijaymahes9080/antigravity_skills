#!/usr/bin/env python3
"""
bootstrap.py — Unified Dependency & Environment Verification Engine
Part of document-maker skill.
"""

import sys
import subprocess
import importlib

REQUIRED_PACKAGES = {
    "reportlab": {"min_version": "4.0.0", "pip_name": "reportlab"},
    "docx": {"min_version": "1.0.0", "pip_name": "python-docx"},
    "pptx": {"min_version": "1.0.0", "pip_name": "python-pptx"},
    "openpyxl": {"min_version": "3.1.0", "pip_name": "openpyxl"},
    "pypdf": {"min_version": "4.0.0", "pip_name": "pypdf"},
    "PIL": {"min_version": "10.0.0", "pip_name": "Pillow"},
    "jinja2": {"min_version": "3.1.0", "pip_name": "Jinja2"},
}

OPTIONAL_PACKAGES = {
    "lxml": {"min_version": "5.0.0", "pip_name": "lxml"},
    "markdown_it": {"min_version": "3.0.0", "pip_name": "markdown-it-py"},
    "xlsxwriter": {"min_version": "3.0.0", "pip_name": "xlsxwriter"},
    "weasyprint": {"min_version": "60.0.0", "pip_name": "weasyprint"}
}

def check_package(module_name):
    try:
        mod = importlib.import_module(module_name)
        ver = getattr(mod, "__version__", "unknown")
        return True, ver
    except ImportError:
        return False, None

def verify_all(auto_install=False):
    print("================================================================")
    print("  Document Maker — Environment & Dependency Verification")
    print(f"  Python Version: {sys.version.split()[0]} on {sys.platform}")
    print("================================================================\n")

    missing = []
    print("Core Dependencies:")
    for mod, meta in REQUIRED_PACKAGES.items():
        ok, ver = check_package(mod)
        if ok:
            print(f"  [PASS] {meta['pip_name']:<18} version {ver}")
        else:
            print(f"  [FAIL] {meta['pip_name']:<18} MISSING")
            missing.append(meta['pip_name'])

    print("\nOptional Enhancements:")
    for mod, meta in OPTIONAL_PACKAGES.items():
        ok, ver = check_package(mod)
        if ok:
            print(f"  [PASS] {meta['pip_name']:<18} version {ver} (Active)")
        else:
            print(f"  [INFO] {meta['pip_name']:<18} Not installed (Optional)")

    if missing:
        if auto_install:
            print(f"\nInstalling missing core packages: {', '.join(missing)}...")
            cmd = [sys.executable, "-m", "pip", "install", *missing]
            res = subprocess.run(cmd)
            if res.returncode == 0:
                print("All packages installed successfully.")
                return 0
            else:
                print("Installation failed.")
                return 1
        else:
            print(f"\nMissing required packages: {', '.join(missing)}")
            print("Run with --install to automatically install them.")
            return 1

    print("\n[SUCCESS] Document Maker runtime environment is fully operational.")
    return 0

if __name__ == "__main__":
    install_flag = "--install" in sys.argv
    sys.exit(verify_all(auto_install=install_flag))

