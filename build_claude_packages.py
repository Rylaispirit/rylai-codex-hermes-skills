#!/usr/bin/env python3
"""Build one distributable ZIP archive per skill in this bundle.

A package is a ZIP archive whose top-level entry is the skill folder, for
example ``deep-research/SKILL.md``. Upload an individual ZIP through the
Claude.ai or Cowork skill-management interface. Claude Code uses the unpacked
directories under ``~/.claude/skills`` or ``<project>/.claude/skills``.

Usage:
    python build_claude_packages.py                      # write to packages/
    python build_claude_packages.py --out dist           # write somewhere else
    python build_claude_packages.py --clean              # remove stale archives first
    python build_claude_packages.py --release-checksums  # also refresh checksums.sha256

Archives are byte-for-byte reproducible: entries are sorted and every member
uses a fixed timestamp, so rebuilding an unchanged skill leaves its checksum
untouched.
"""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKILLS = ROOT / "skills"

EXCLUDE_DIRS = {"__pycache__", "node_modules", ".git"}
EXCLUDE_FILES = {".DS_Store", "Thumbs.db"}
EXCLUDE_GLOBS = ("*.pyc", "*.pyo", "*.log", "*.tmp", "*.bak")
FIXED_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


def should_exclude(relative: Path) -> bool:
    if any(part in EXCLUDE_DIRS for part in relative.parts):
        return True
    if relative.name in EXCLUDE_FILES:
        return True
    return any(fnmatch.fnmatch(relative.name, pattern) for pattern in EXCLUDE_GLOBS)


def package(skill_dir: Path, out_dir: Path) -> tuple[Path, int]:
    archive = out_dir / f"{skill_dir.name}.zip"
    members = sorted(
        path
        for path in skill_dir.rglob("*")
        if path.is_file() and not should_exclude(path.relative_to(skill_dir))
    )
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as bundle:
        for path in members:
            arcname = path.relative_to(skill_dir.parent).as_posix()
            info = zipfile.ZipInfo(arcname, date_time=FIXED_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            # ZipInfo defaults this to 0 on Windows and 3 elsewhere. Pin it so a
            # rebuild on any platform produces the same bytes.
            info.create_system = 3
            bundle.writestr(info, path.read_bytes())
    return archive, len(members)


def write_release_checksums() -> int:
    """Rewrite the repository-level checksums.sha256 for the source files.

    Generated archives are covered by the checksum file inside the output
    directory, so they are deliberately left out here.
    """
    skipped_roots = {".git", "packages"}
    entries = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT)
        if relative.parts[0] in skipped_roots or relative.name == "checksums.sha256":
            continue
        if should_exclude(relative):
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        entries.append(f"{digest}  {relative.as_posix()}")
    (ROOT / "checksums.sha256").write_text(
        "\n".join(entries) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return len(entries)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default="packages", help="output directory (default: packages)")
    parser.add_argument("--clean", action="store_true", help="delete the output directory first")
    parser.add_argument(
        "--release-checksums",
        action="store_true",
        help="also rewrite the repository-level checksums.sha256 for the source files",
    )
    args = parser.parse_args()

    if not SKILLS.is_dir():
        print("skills/ directory not found", file=sys.stderr)
        return 1

    if not args.out.strip():
        print("--out must name a directory", file=sys.stderr)
        return 1

    out_dir = Path(args.out)
    out_dir = out_dir.resolve() if out_dir.is_absolute() else (ROOT / out_dir).resolve()

    # --clean deletes the target, so refuse anything that would take the repo,
    # the skills tree, or a parent directory with it.
    protected = {ROOT, ROOT.parent, SKILLS, Path(ROOT.anchor)}
    if out_dir in protected or out_dir in ROOT.parents or out_dir == Path.home():
        print(f"refusing to use {out_dir} as the output directory", file=sys.stderr)
        return 1

    if args.clean and out_dir.is_dir():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    skill_dirs = sorted(path for path in SKILLS.iterdir() if path.is_dir())
    if not skill_dirs:
        print("no skills found", file=sys.stderr)
        return 1

    checksums: list[str] = []
    for skill_dir in skill_dirs:
        if not (skill_dir / "SKILL.md").is_file():
            print(f"skip {skill_dir.name}: missing SKILL.md", file=sys.stderr)
            continue
        archive, count = package(skill_dir, out_dir)
        digest = hashlib.sha256(archive.read_bytes()).hexdigest()
        checksums.append(f"{digest}  {archive.name}")
        print(f"{archive.name:34} {count:3} file(s)  {archive.stat().st_size:>7} bytes")

    (out_dir / "checksums.sha256").write_text(
        "\n".join(checksums) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    try:
        shown = f"{out_dir.relative_to(ROOT)}/"
    except ValueError:
        shown = str(out_dir)
    print(f"\nWrote {len(checksums)} archive(s) to {shown}")

    if args.release_checksums:
        count = write_release_checksums()
        print(f"Wrote {count} entries to checksums.sha256")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
