#!/usr/bin/env python3
"""Guarded local-file wrapper for MarkItDown.

Original utility maintained by Rylai for Codex and Hermes skill workflows.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import urlspli


def markitdown_command() -> list[str] | None:
    executable = shutil.which("markitdown")
    if executable:
        return [executable]
    uvx = shutil.which("uvx")
    if uvx:
        return [uvx, "markitdown"]
    return None


def local_source(value: str) -> Path:
    parsed = urlsplit(value)
    if parsed.scheme and not (len(parsed.scheme) == 1 and value[1:3] in {":\\", ":/"}):
        raise RuntimeError("URI inputs are disabled; provide a local file path")
    path = Path(value).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"source file not found: {path}")
    return path


def destination_path(source: Path, value: Path, overwrite: bool) -> Path:
    destination = value.expanduser().resolve()
    if destination.suffix.lower() not in {".md", ".markdown"}:
        raise RuntimeError("destination must use the .md or .markdown extension")
    if destination == source:
        raise RuntimeError("source and destination must be different files")
    if destination.exists() and not overwrite:
        raise FileExistsError(f"destination already exists: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    return destination


def convert_one(source_value: str, output: Path, overwrite: bool, timeout: float) -> str:
    command = markitdown_command()
    if not command:
        raise RuntimeError("MarkItDown is unavailable; install markitdown or install uv for uvx")
    source = local_source(source_value)
    destination = destination_path(source, output, overwrite)
    with tempfile.NamedTemporaryFile(
        delete=False,
        dir=destination.parent,
        prefix=f".{destination.name}.",
        suffix=".md",
    ) as handle:
        temporary = Path(handle.name)
    try:
        completed = subprocess.run(
            [*command, str(source), "-o", str(temporary)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
        if completed.returncode:
            message = completed.stderr.strip() or completed.stdout.strip()
            raise RuntimeError(message or f"MarkItDown exited with code {completed.returncode}")
        content = temporary.read_text(encoding="utf-8")
        if not content.strip():
            raise RuntimeError("MarkItDown produced empty Markdown")
        os.replace(temporary, destination)
        return "installed-markitdown" if len(command) == 1 else "uvx-markitdown"
    finally:
        temporary.unlink(missing_ok=True)


def batch_command(args: argparse.Namespace) -> int:
    source_dir = args.source_dir.expanduser().resolve()
    output_dir = args.output_dir.expanduser().resolve()
    if not source_dir.is_dir():
        raise FileNotFoundError(f"source directory not found: {source_dir}")
    includes = {"." + item.lower().lstrip(".") for item in args.include}
    iterator = source_dir.rglob("*") if args.recursive else source_dir.glob("*")
    sources = []
    for path in iterator:
        if not path.is_file():
            continue
        resolved = path.resolve()
        if output_dir == resolved.parent or output_dir in resolved.parents:
            continue
        if includes and path.suffix.lower() not in includes:
            continue
        sources.append(path)

    failures = 0
    for source in sorted(sources):
        relative = source.relative_to(source_dir).with_suffix(".md")
        destination = output_dir / relative
        try:
            route = convert_one(str(source), destination, args.overwrite, args.timeout)
            print(f"OK   {source} -> {destination} [{route}]")
        except Exception as error:
            failures += 1
            print(f"FAIL {source}: {error}", file=sys.stderr)
    print(f"Processed: {len(sources)}; Failed: {failures}")
    return 1 if failures else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("doctor", help="Report the selected MarkItDown route")

    convert = subparsers.add_parser("convert", help="Convert one local file")
    convert.add_argument("source", help="Local file path")
    convert.add_argument("output", type=Path)
    convert.add_argument("--overwrite", action="store_true")
    convert.add_argument("--timeout", type=float, default=300.0)

    batch = subparsers.add_parser("batch", help="Convert files under a local directory")
    batch.add_argument("source_dir", type=Path)
    batch.add_argument("output_dir", type=Path)
    batch.add_argument("--recursive", action="store_true")
    batch.add_argument("--include", action="append", default=[], help="Source extension; repeatable")
    batch.add_argument("--overwrite", action="store_true")
    batch.add_argument("--timeout", type=float, default=300.0)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        if args.command == "doctor":
            command = markitdown_command()
            if not command:
                print("MISSING MarkItDown and uvx")
                return 1
            print("OK " + " ".join(command))
            return 0
        if args.timeout <= 0:
            raise RuntimeError("--timeout must be greater than zero")
        if args.command == "convert":
            route = convert_one(args.source, args.output, args.overwrite, args.timeout)
            print(f"Wrote {args.output} using {route}")
            return 0
        if args.command == "batch":
            return batch_command(args)
    except subprocess.TimeoutExpired:
        print("ERROR: MarkItDown timed out", file=sys.stderr)
        return 1
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    parser.error("unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
