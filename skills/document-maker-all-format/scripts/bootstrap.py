#!/usr/bin/env python3
"""
Bootstrap: probe environment and install missing dependencies.
Run: python scripts/bootstrap.py

This script is safe to run multiple times (idempotent).
It reports what is installed, installs what is missing, and
verifies the final state — no silent failures.
"""
import importlib
import subprocess
import sys
import shutil
import io
from pathlib import Path

# Ensure stdout handles Unicode on Windows (cp1252 → utf-8)
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf_8"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if sys.stderr.encoding and sys.stderr.encoding.lower() not in ("utf-8", "utf_8"):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# ─── Required library → pip package mapping ──────────────────────────────────
REQUIRED: dict[str, str] = {
    "reportlab":  "reportlab>=5.0",
    "docx":       "python-docx>=1.0",
    "pptx":       "python-pptx>=1.0",
    "openpyxl":   "openpyxl>=3.1",
    "pypdf":      "pypdf>=6.0",
    "jinja2":     "Jinja2>=3.1",
    "lxml":       "lxml>=6.0",
    "PIL":        "Pillow>=12.0",
    "markdown_it": "markdown-it-py>=4.0",
}

# ─── Optional tools ──────────────────────────────────────────────────────────
OPTIONAL: dict[str, str] = {
    "pandoc":      "pandoc (system binary — install separately)",
    "weasyprint":  "pip install weasyprint",
}


def check_python() -> None:
    major, minor = sys.version_info[:2]
    if (major, minor) < (3, 11):
        print(f"⚠️  Python {major}.{minor} detected. Python 3.11+ recommended.")
    else:
        print(f"✅ Python {major}.{minor}.{sys.version_info.micro}")


def probe_libraries() -> list[str]:
    """Return list of pip specs for missing libraries."""
    missing: list[str] = []
    print("\n── Library Check ────────────────────────────────────────────────")
    for module, pip_spec in REQUIRED.items():
        try:
            mod = importlib.import_module(module)
            ver = getattr(mod, "__version__", "unknown")
            print(f"  ✅ {module:<18} {ver}")
        except ImportError:
            print(f"  ❌ {module:<18} NOT FOUND  →  will install: {pip_spec}")
            missing.append(pip_spec)
    return missing


def install_missing(missing: list[str]) -> None:
    if not missing:
        print("\n✅ All required libraries are already installed.")
        return
    print(f"\n── Installing {len(missing)} missing package(s) ─────────────────────────")
    cmd = [sys.executable, "-m", "pip", "install", "--quiet", *missing]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ❌ pip install failed:\n{result.stderr}")
        sys.exit(1)
    print(f"  ✅ Installed: {', '.join(missing)}")


def verify_after_install(missing: list[str]) -> None:
    if not missing:
        return
    print("\n── Post-install Verification ────────────────────────────────────")
    failed: list[str] = []
    for module in REQUIRED:
        try:
            importlib.import_module(module)
            importlib.invalidate_caches()
        except ImportError:
            failed.append(module)

    if failed:
        print(f"  ❌ Still missing after install: {failed}")
        sys.exit(1)
    print("  ✅ All libraries verified after install.")


def probe_optional() -> None:
    print("\n── Optional Tools ───────────────────────────────────────────────")
    # pandoc binary
    pandoc_path = shutil.which("pandoc")
    if pandoc_path:
        result = subprocess.run(["pandoc", "--version"], capture_output=True, text=True)
        ver_line = result.stdout.splitlines()[0] if result.stdout else "unknown"
        print(f"  ✅ pandoc             {ver_line}")
    else:
        print("  ⬜ pandoc             NOT found  (optional: advanced conversions)")
    # weasyprint
    try:
        import weasyprint
        print(f"  ✅ weasyprint         {weasyprint.__version__}")
    except ImportError:
        print("  ⬜ weasyprint         NOT found  (optional: HTML→PDF with CSS)")


def probe_output_dir() -> None:
    """Ensure ./output/ directory exists."""
    out = Path("output")
    out.mkdir(exist_ok=True)
    print(f"\n  ✅ Output directory: {out.resolve()}")


def main() -> None:
    print("=" * 62)
    print("  document-maker-all-format — Bootstrap & Environment Probe")
    print("=" * 62)

    check_python()
    missing = probe_libraries()
    install_missing(missing)
    verify_after_install(missing)
    probe_optional()
    probe_output_dir()

    print("\n" + "=" * 62)
    print("  ✅ Environment ready. document-maker-all-format is active.")
    print("=" * 62 + "\n")


if __name__ == "__main__":
    main()
