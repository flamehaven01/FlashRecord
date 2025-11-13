#!/usr/bin/env python3
"""Doc sanity check helper.

Validates that internal Markdown links reference existing files and flags lines
containing Hangul characters so documentation stays ASCII/English-only.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Iterable, List, Tuple

INTERNAL_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
HANGUL_CHARS = re.compile(r"[\u3130-\u318F\uAC00-\uD7A3]")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate documentation links and language consistency."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        default=["README.md", "CONTRIBUTING.md", "docs"],
        help="Files or directories to scan (default: README, CONTRIBUTING, docs/).",
    )
    return parser.parse_args()


def iter_markdown_files(targets: Iterable[str]) -> List[Path]:
    files: List[Path] = []
    for raw_target in targets:
        target = Path(raw_target)
        if not target.exists():
            print(f"[warn] target not found: {target}", file=sys.stderr)
            continue
        if target.is_dir():
            files.extend(sorted(target.rglob("*.md")))
        else:
            files.append(target)
    return files


def check_links(md_file: Path) -> List[str]:
    errors: List[str] = []
    text = md_file.read_text(encoding="utf-8")
    for match in INTERNAL_LINK.finditer(text):
        link = match.group(2).strip()
        if not link or link.startswith(("http://", "https://", "mailto:", "#")):
            continue
        if "://" in link:
            continue  # Skip other protocols (e.g., ftp)
        local_target = link.split("#", 1)[0].split("?", 1)[0]
        resolved = (md_file.parent / local_target).resolve()
        if not resolved.exists():
            errors.append(
                f"{md_file}: missing link target '{link}' (resolves to {resolved})"
            )
    return errors


def check_hangul(md_file: Path) -> List[str]:
    issues: List[str] = []
    for idx, line in enumerate(md_file.read_text(encoding="utf-8").splitlines(), 1):
        if HANGUL_CHARS.search(line):
            issues.append(f"{md_file}:{idx} contains Hangul characters -> {line.strip()}")
    return issues


def main() -> int:
    args = parse_args()
    files = iter_markdown_files(args.paths)
    if not files:
        print("[error] no markdown files found to inspect", file=sys.stderr)
        return 2

    missing_links: List[str] = []
    hangul_hits: List[str] = []

    for md_file in files:
        missing_links.extend(check_links(md_file))
        hangul_hits.extend(check_hangul(md_file))

    if missing_links:
        print("\n[missing references]")
        for msg in missing_links:
            print(f" - {msg}")

    if hangul_hits:
        print("\n[non-english lines detected]")
        for msg in hangul_hits[:50]:
            print(f" - {msg}")
        if len(hangul_hits) > 50:
            remaining = len(hangul_hits) - 50
            print(f"   ...and {remaining} more lines")

    if not missing_links and not hangul_hits:
        print("[ok] documentation sanity check passed")
        return 0

    print(
        f"[fail] documentation issues found: "
        f"{len(missing_links)} broken link(s), {len(hangul_hits)} hangul line(s)"
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
