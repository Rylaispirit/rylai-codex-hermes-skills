#!/usr/bin/env python3
"""Inspect and modify PDF page sets with pypdf.

Original utility maintained by Rylai for Codex, Hermes, and Claude skill workflows.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys
import tempfile


def pypdf_classes():
    try:
        from pypdf import PdfReader, PdfWriter
    except ImportError as error:
        raise RuntimeError("install pypdf to use this utility") from error
    return PdfReader, PdfWriter


def source_file(path: Path) -> Path:
    resolved = path.expanduser().resolve()
    if not resolved.is_file():
        raise FileNotFoundError(f"PDF not found: {resolved}")
    return resolved


def output_file(path: Path, sources: list[Path], overwrite: bool) -> Path:
    resolved = path.expanduser().resolve()
    if resolved in sources:
        raise RuntimeError("output must differ from every source file")
    if resolved.exists() and not overwrite:
        raise FileExistsError(f"output already exists: {resolved}")
    resolved.parent.mkdir(parents=True, exist_ok=True)
    return resolved


def select_pages(specification: str, total_pages: int) -> list[int]:
    if specification.strip().lower() == "all":
        return list(range(total_pages))
    selected: list[int] = []
    for raw_part in specification.split(","):
        part = raw_part.strip()
        if not part:
            continue
        if "-" in part:
            start_text, end_text = part.split("-", 1)
            start = int(start_text)
            end = int(end_text)
            if start > end:
                raise ValueError(f"descending page range is not allowed: {part}")
            numbers = range(start, end + 1)
        else:
            numbers = [int(part)]
        for number in numbers:
            index = number - 1
            if index < 0 or index >= total_pages:
                raise ValueError(f"page {number} is outside 1-{total_pages}")
            if index not in selected:
                selected.append(index)
    if not selected:
        raise ValueError("page selection is empty")
    return selected


def write_pdf(writer, destination: Path) -> None:
    with tempfile.NamedTemporaryFile(
        delete=False,
        dir=destination.parent,
        prefix=f".{destination.name}.",
        suffix=".tmp",
    ) as handle:
        temporary_path = Path(handle.name)
        writer.write(handle)
    try:
        os.replace(temporary_path, destination)
    finally:
        temporary_path.unlink(missing_ok=True)


def info_command(path: Path) -> None:
    PdfReader, _ = pypdf_classes()
    source = source_file(path)
    reader = PdfReader(str(source))
    metadata = reader.metadata or {}
    print(f"file: {source}")
    print(f"pages: {len(reader.pages)}")
    print(f"encrypted: {reader.is_encrypted}")
    for key in ("/Title", "/Author", "/Subject", "/Creator", "/Producer"):
        value = metadata.get(key)
        if value:
            print(f"{key.lstrip('/').lower()}: {value}")


def merge_command(output: Path, inputs: list[Path], overwrite: bool) -> None:
    PdfReader, PdfWriter = pypdf_classes()
    sources = [source_file(path) for path in inputs]
    destination = output_file(output, sources, overwrite)
    writer = PdfWriter()
    for source in sources:
        reader = PdfReader(str(source))
        for page in reader.pages:
            writer.add_page(page)
    write_pdf(writer, destination)
    print(f"Wrote {destination}")


def extract_command(
    source_arg: Path,
    output: Path,
    pages: str,
    rotation: int,
    overwrite: bool,
) -> None:
    PdfReader, PdfWriter = pypdf_classes()
    source = source_file(source_arg)
    destination = output_file(output, [source], overwrite)
    reader = PdfReader(str(source))
    writer = PdfWriter()
    for index in select_pages(pages, len(reader.pages)):
        page = reader.pages[index]
        if rotation:
            page.rotate(rotation)
        writer.add_page(page)
    write_pdf(writer, destination)
    print(f"Wrote {destination}")


def split_command(source_arg: Path, output_dir: Path, overwrite: bool) -> None:
    PdfReader, PdfWriter = pypdf_classes()
    source = source_file(source_arg)
    destination_dir = output_dir.expanduser().resolve()
    destination_dir.mkdir(parents=True, exist_ok=True)
    reader = PdfReader(str(source))
    for index, page in enumerate(reader.pages, start=1):
        destination = destination_dir / f"{source.stem}-page-{index:03d}.pdf"
        if destination.exists() and not overwrite:
            raise FileExistsError(f"output already exists: {destination}")
        writer = PdfWriter()
        writer.add_page(page)
        write_pdf(writer, destination)
    print(f"Wrote {len(reader.pages)} page files to {destination_dir}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    info = subparsers.add_parser("info")
    info.add_argument("source", type=Path)

    merge = subparsers.add_parser("merge")
    merge.add_argument("output", type=Path)
    merge.add_argument("inputs", type=Path, nargs="+")
    merge.add_argument("--overwrite", action="store_true")

    extract = subparsers.add_parser("extract")
    extract.add_argument("source", type=Path)
    extract.add_argument("output", type=Path)
    extract.add_argument("--pages", required=True, help="One-based selection such as 1,3-5")
    extract.add_argument("--overwrite", action="store_true")

    rotate = subparsers.add_parser("rotate")
    rotate.add_argument("source", type=Path)
    rotate.add_argument("output", type=Path)
    rotate.add_argument("--pages", default="all")
    rotate.add_argument("--degrees", type=int, choices=[90, 180, 270], required=True)
    rotate.add_argument("--overwrite", action="store_true")

    split = subparsers.add_parser("split")
    split.add_argument("source", type=Path)
    split.add_argument("output_dir", type=Path)
    split.add_argument("--overwrite", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "info":
            info_command(args.source)
        elif args.command == "merge":
            merge_command(args.output, args.inputs, args.overwrite)
        elif args.command == "extract":
            extract_command(args.source, args.output, args.pages, 0, args.overwrite)
        elif args.command == "rotate":
            extract_command(args.source, args.output, args.pages, args.degrees, args.overwrite)
        elif args.command == "split":
            split_command(args.source, args.output_dir, args.overwrite)
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
