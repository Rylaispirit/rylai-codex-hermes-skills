#!/usr/bin/env python3
"""Small local PDF utility for the Rylai Codex-Hermes-Claude skill."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Iterable


class PdfToolError(RuntimeError):
    pass


def load_pypdf():
    try:
        import pypdf
    except ImportError as exc:
        raise PdfToolError("Missing dependency: install pypdf with Python.") from exc
    return pypdf


def existing_file(value: str) -> Path:
    path = Path(value).expanduser().resolve()
    if not path.is_file():
        raise PdfToolError(f"Input file does not exist: {path}")
    return path


def output_file(value: str, force: bool) -> Path:
    path = Path(value).expanduser().resolve()
    if path.exists() and not force:
        raise PdfToolError(f"Output already exists: {path}. Add --force to replace it.")
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def open_reader(path: Path, password: str | None = None):
    pypdf = load_pypdf()
    reader = pypdf.PdfReader(str(path))
    if reader.is_encrypted:
        if password is None:
            raise PdfToolError("The PDF is encrypted. Supply its password with --password.")
        if reader.decrypt(password) == 0:
            raise PdfToolError("The supplied PDF password was rejected.")
    return reader


def parse_pages(spec: str | None, count: int) -> list[int]:
    if spec is None:
        return list(range(count))

    pages: list[int] = []
    for token in spec.split(","):
        token = token.strip()
        if not token:
            continue
        if "-" in token:
            start_text, end_text = token.split("-", 1)
            start, end = int(start_text), int(end_text)
            if start > end:
                raise PdfToolError(f"Invalid descending page range: {token}")
            pages.extend(range(start - 1, end))
        else:
            pages.append(int(token) - 1)

    if not pages:
        raise PdfToolError("The page selection is empty.")
    if min(pages) < 0 or max(pages) >= count:
        raise PdfToolError(f"Page selection must stay between 1 and {count}.")

    return list(dict.fromkeys(pages))


def command_info(args: argparse.Namespace) -> None:
    path = existing_file(args.input)
    reader = open_reader(path, args.password)
    metadata = {}
    if reader.metadata:
        metadata = {str(key): str(value) for key, value in reader.metadata.items()}
    result = {
        "file": str(path),
        "bytes": path.stat().st_size,
        "pages": len(reader.pages),
        "encrypted": bool(reader.is_encrypted),
        "metadata": metadata,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))


def extract_with_pdfplumber(
    path: Path, pages: Iterable[int], password: str | None
) -> list[str] | None:
    try:
        import pdfplumber
    except ImportError:
        return None

    extracted = []
    with pdfplumber.open(str(path), password=password) as pdf:
        for index in pages:
            extracted.append(pdf.pages[index].extract_text() or "")
    return extracted


def command_extract(args: argparse.Namespace) -> None:
    source = existing_file(args.input)
    reader = open_reader(source, args.password)
    pages = parse_pages(args.pages, len(reader.pages))
    output = output_file(args.output, args.force)

    texts = extract_with_pdfplumber(source, pages, args.password)
    if texts is None:
        texts = [reader.pages[index].extract_text() or "" for index in pages]

    sections = [
        f"===== Page {page_index + 1} =====\n{text.rstrip()}"
        for page_index, text in zip(pages, texts)
    ]
    output.write_text("\n\n".join(sections) + "\n", encoding="utf-8")
    print(f"Wrote {len(pages)} page(s) to {output}")


def command_merge(args: argparse.Namespace) -> None:
    pypdf = load_pypdf()
    sources = [existing_file(value) for value in args.inputs]
    output = output_file(args.output, args.force)
    if output in sources:
        raise PdfToolError("The merge output must differ from every input.")

    writer = pypdf.PdfWriter()
    for source in sources:
        reader = open_reader(source)
        for page in reader.pages:
            writer.add_page(page)
    with output.open("wb") as stream:
        writer.write(stream)
    print(f"Merged {len(sources)} file(s) into {output}")


def command_split(args: argparse.Namespace) -> None:
    pypdf = load_pypdf()
    source = existing_file(args.input)
    reader = open_reader(source, args.password)
    pages = parse_pages(args.pages, len(reader.pages))
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    for index in pages:
        output = output_dir / f"page-{index + 1:04d}.pdf"
        if output.exists() and not args.force:
            raise PdfToolError(f"Output already exists: {output}. Add --force to replace it.")
        writer = pypdf.PdfWriter()
        writer.add_page(reader.pages[index])
        with output.open("wb") as stream:
            writer.write(stream)
    print(f"Wrote {len(pages)} PDF file(s) to {output_dir}")


def command_rotate(args: argparse.Namespace) -> None:
    pypdf = load_pypdf()
    source = existing_file(args.input)
    reader = open_reader(source, args.password)
    selected = set(parse_pages(args.pages, len(reader.pages)))
    output = output_file(args.output, args.force)
    if output == source:
        raise PdfToolError("Use a separate output path for rotation.")

    writer = pypdf.PdfWriter()
    for index, page in enumerate(reader.pages):
        if index in selected:
            page.rotate(args.degrees)
        writer.add_page(page)
    with output.open("wb") as stream:
        writer.write(stream)
    print(f"Rotated {len(selected)} page(s) into {output}")


def run_external(command: list[str]) -> None:
    executable = Path(command[0])
    if os.name == "nt" and executable.suffix.lower() in {".bat", ".cmd"}:
        subprocess.run(subprocess.list2cmdline(command), shell=True, check=True)
    else:
        subprocess.run(command, check=True)


def render_with_pdfium(source: Path, output_dir: Path, dpi: int) -> int:
    try:
        import pypdfium2
    except ImportError:
        return 0

    document = pypdfium2.PdfDocument(str(source))
    count = 0
    try:
        for index in range(len(document)):
            page = document[index]
            try:
                bitmap = page.render(scale=dpi / 72)
                image = bitmap.to_pil()
                image.save(output_dir / f"page-{index + 1:04d}.png")
                count += 1
            finally:
                page.close()
    finally:
        document.close()
    return coun


def command_render(args: argparse.Namespace) -> None:
    source = existing_file(args.input)
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    rendered_count = render_with_pdfium(source, output_dir, args.dpi)
    if rendered_count:
        print(f"Rendered {rendered_count} page(s) to {output_dir}")
        return

    tool = shutil.which("pdftoppm")
    if tool is None:
        raise PdfToolError("Neither pypdfium2 nor Poppler pdftoppm is available.")
    prefix = output_dir / "page"
    run_external([tool, "-png", "-r", str(args.dpi), str(source), str(prefix)])
    rendered = sorted(output_dir.glob("page-*.png"))
    if not rendered:
        raise PdfToolError("Poppler finished without producing PNG files.")
    print(f"Rendered {len(rendered)} page(s) to {output_dir}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Local PDF utility by Rylai.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    info = subparsers.add_parser("info", help="Print page count, size, and metadata.")
    info.add_argument("input")
    info.add_argument("--password")
    info.set_defaults(func=command_info)

    extract = subparsers.add_parser("extract", help="Extract text into a UTF-8 file.")
    extract.add_argument("input")
    extract.add_argument("output")
    extract.add_argument("--pages", help="One-based selection such as 1-3,7.")
    extract.add_argument("--password")
    extract.add_argument("--force", action="store_true")
    extract.set_defaults(func=command_extract)

    merge = subparsers.add_parser("merge", help="Merge PDFs in the supplied order.")
    merge.add_argument("output")
    merge.add_argument("inputs", nargs="+")
    merge.add_argument("--force", action="store_true")
    merge.set_defaults(func=command_merge)

    split = subparsers.add_parser("split", help="Write selected pages as individual PDFs.")
    split.add_argument("input")
    split.add_argument("output_dir")
    split.add_argument("--pages", help="One-based selection such as 1-3,7.")
    split.add_argument("--password")
    split.add_argument("--force", action="store_true")
    split.set_defaults(func=command_split)

    rotate = subparsers.add_parser("rotate", help="Rotate selected pages clockwise.")
    rotate.add_argument("input")
    rotate.add_argument("output")
    rotate.add_argument("degrees", type=int, choices=(90, 180, 270))
    rotate.add_argument("--pages", help="One-based selection such as 1-3,7.")
    rotate.add_argument("--password")
    rotate.add_argument("--force", action="store_true")
    rotate.set_defaults(func=command_rotate)

    render = subparsers.add_parser("render", help="Render every page to PNG.")
    render.add_argument("input")
    render.add_argument("output_dir")
    render.add_argument("--dpi", type=int, default=144)
    render.set_defaults(func=command_render)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        args.func(args)
    except (PdfToolError, ValueError, OSError, subprocess.CalledProcessError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
