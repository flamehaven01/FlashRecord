#!/usr/bin/env python3
"""Convenience wrapper for building Sphinx documentation."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    docs_dir = repo_root / "docs"
    build_dir = docs_dir / "_build" / "html"

    if not docs_dir.exists():
        print("[-] docs/ directory not found")
        return 1

    build_dir.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["sphinx-build", "-b", "html", str(docs_dir), str(build_dir)]
    print(f"[*] Running {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True)
    except FileNotFoundError:
        print("[-] sphinx-build command not found. Install Sphinx with `pip install sphinx`.")
        return 1
    except subprocess.CalledProcessError as exc:
        print(f"[-] Sphinx build failed (exit code {exc.returncode})")
        return exc.returncode

    print(f"[+] Documentation built at {build_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
