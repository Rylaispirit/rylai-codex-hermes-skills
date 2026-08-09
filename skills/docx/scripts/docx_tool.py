#!/usr/bin/env python3
"""Original Rylai helper for practical DOCX workflows."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

try:
    from docx import Documen
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Inches, P
except ImportError as exc:
    raise SystemExit(
        "python-docx is required. Install it only with the user's approval."
    ) from exc


AUTHOR = "Rylai"
INLINE_RE = re.compile(r"(\*\*[^*]+\*\*|__[^_]+__|`[^`]+`|\*[^*]+\*|_[^_]+_)")
TABLE_SEPARATOR_RE = re.compile(r"^:?-{3,}:?$")


def set_document_defaults(document: Document, author: str, title: str = "") -> None:
    props = document.core_properties
    props.author = author
    props.last_modified_by = author
    if title:
        props.title = title

    normal = document.styles["Normal"]
    normal.font.name = "Arial"
    normal.font.size = Pt(11)

    for style_name, size in (("Title", 22), ("Heading 1", 16), ("Heading 2", 14), ("Heading 3", 12)):
        style = document.styles[style_name]
        style.font.name = "Arial"
        style.font.size = Pt(size)
        style.font.bold = True

    for section in document.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.85)
        section.right_margin = Inches(0.85)


def add_inline(paragraph, text: str) -> None:
    cursor = 0
    for match in INLINE_RE.finditer(text):
        if match.start() > cursor:
            paragraph.add_run(text[cursor : match.start()])
        token = match.group(0)
        run = paragraph.add_run(token)
        if token.startswith(("**", "__")):
            run.text = token[2:-2]
            run.bold = True
        elif token.startswith("`"):
            run.text = token[1:-1]
            run.font.name = "Consolas"
        else:
            run.text = token[1:-1]
            run.italic = True
        cursor = match.end()
    if cursor < len(text):
        paragraph.add_run(text[cursor:])


def split_table_row(line: str) -> list[str]:
    stripped = line.strip().strip("|")
    return [cell.strip() for cell in stripped.split("|")]


def is_table_separator(line: str) -> bool:
    cells = split_table_row(line)
    return bool(cells) and all(TABLE_SEPARATOR_RE.fullmatch(cell) for cell in cells)


def add_table(document: Document, rows: list[list[str]]) -> None:
    width = max(len(row) for row in rows)
    table = document.add_table(rows=len(rows), cols=width)
    table.style = "Table Grid"
    for row_index, row in enumerate(rows):
        for column_index in range(width):
            value = row[column_index] if column_index < len(row) else ""
            paragraph = table.cell(row_index, column_index).paragraphs[0]
            add_inline(paragraph, value)
            if row_index == 0:
                for run in paragraph.runs:
                    run.bold = True


def create_docx(markdown_path: Path, output_path: Path, title: str, author: str) -> None:
    lines = markdown_path.read_text(encoding="utf-8-sig").splitlines()
    document = Document()
    set_document_defaults(document, author, title)
    if title:
        paragraph = document.add_paragraph(style="Title")
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        paragraph.add_run(title)

    index = 0
    while index < len(lines):
        line = lines[index].rstrip()
        stripped = line.strip()
        if not stripped:
            index += 1
            continue

        if (
            "|" in stripped
            and index + 1 < len(lines)
            and "|" in lines[index + 1]
            and is_table_separator(lines[index + 1])
        ):
            rows = [split_table_row(stripped)]
            index += 2
            while index < len(lines) and "|" in lines[index] and lines[index].strip():
                rows.append(split_table_row(lines[index]))
                index += 1
            add_table(document, rows)
            continue

        heading = re.match(r"^(#{1,3})\s+(.+)$", stripped)
        bullet = re.match(r"^[-+*]\s+(.+)$", stripped)
        numbered = re.match(r"^\d+[.)]\s+(.+)$", stripped)
        quote = re.match(r"^>\s?(.*)$", stripped)

        if heading:
            paragraph = document.add_paragraph(style=f"Heading {len(heading.group(1))}")
            add_inline(paragraph, heading.group(2))
        elif bullet:
            paragraph = document.add_paragraph(style="List Bullet")
            add_inline(paragraph, bullet.group(1))
        elif numbered:
            paragraph = document.add_paragraph(style="List Number")
            add_inline(paragraph, numbered.group(1))
        elif quote:
            paragraph = document.add_paragraph()
            paragraph.paragraph_format.left_indent = Inches(0.3)
            run = paragraph.add_run(quote.group(1))
            run.italic = True
        else:
            paragraph = document.add_paragraph()
            add_inline(paragraph, stripped)
        index += 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    document.save(output_path)
    Document(output_path)


def iter_paragraphs(document: Document):
    yield from document.paragraphs
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                yield from cell.paragraphs
    for section in document.sections:
        yield from section.header.paragraphs
        yield from section.footer.paragraphs


def inspect_docx(path: Path, include_text: bool) -> dict:
    document = Document(path)
    paragraphs = list(iter_paragraphs(document))
    text_lines = [paragraph.text for paragraph in paragraphs if paragraph.text.strip()]
    headings = [
        paragraph.tex
        for paragraph in document.paragraphs
        if paragraph.text.strip() and paragraph.style.name.startswith("Heading")
    ]
    result = {
        "path": str(path.resolve()),
        "author": document.core_properties.author or "",
        "last_modified_by": document.core_properties.last_modified_by or "",
        "title": document.core_properties.title or "",
        "paragraphs": len(paragraphs),
        "nonempty_paragraphs": len(text_lines),
        "tables": len(document.tables),
        "sections": len(document.sections),
        "headings": headings,
        "word_count": sum(len(re.findall(r"\S+", line)) for line in text_lines),
    }
    if include_text:
        result["text"] = "\n".join(text_lines)
    return resul


def replace_in_paragraph(paragraph, replacements: list[tuple[str, str]]) -> int:
    if not paragraph.runs:
        return 0
    original = "".join(run.text for run in paragraph.runs)
    updated = original
    hits = 0
    for old, new in replacements:
        count = updated.count(old)
        if count:
            updated = updated.replace(old, new)
            hits += coun
    if updated != original:
        paragraph.runs[0].text = updated
        for run in paragraph.runs[1:]:
            run.text = ""
    return hits


def replace_docx(
    input_path: Path,
    output_path: Path,
    replacements: list[tuple[str, str]],
    author: str,
) -> int:
    document = Document(input_path)
    hits = sum(replace_in_paragraph(paragraph, replacements) for paragraph in iter_paragraphs(document))
    document.core_properties.author = author
    document.core_properties.last_modified_by = author
    output_path.parent.mkdir(parents=True, exist_ok=True)
    document.save(output_path)
    Document(output_path)
    return hits


def find_soffice() -> str | None:
    found = shutil.which("soffice") or shutil.which("libreoffice")
    if found:
        return found
    candidates = (
        Path(r"C:\Program Files\LibreOffice\program\soffice.exe"),
        Path(r"C:\Program Files (x86)\LibreOffice\program\soffice.exe"),
    )
    return next((str(path) for path in candidates if path.exists()), None)


def render_docx(input_path: Path, output_dir: Path) -> Path:
    soffice = find_soffice()
    if not soffice:
        raise SystemExit("LibreOffice was not found; DOCX creation and inspection still work.")
    output_dir.mkdir(parents=True, exist_ok=True)
    command = [
        soffice,
        "--headless",
        "--convert-to",
        "pdf",
        "--outdir",
        str(output_dir),
        str(input_path),
    ]
    completed = subprocess.run(command, capture_output=True, text=True, timeout=120)
    expected = output_dir / f"{input_path.stem}.pdf"
    if completed.returncode != 0 or not expected.exists():
        detail = completed.stderr.strip() or completed.stdout.strip() or "unknown error"
        raise SystemExit(f"LibreOffice rendering failed: {detail}")
    return expected


def parse_replacements(values: list[str]) -> list[tuple[str, str]]:
    replacements = []
    for value in values:
        if "=" not in value:
            raise SystemExit(f"Replacement must use OLD=NEW: {value}")
        old, new = value.split("=", 1)
        if not old:
            raise SystemExit("Replacement source text cannot be empty.")
        replacements.append((old, new))
    return replacements


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Rylai DOCX helper")
    subparsers = parser.add_subparsers(dest="command", required=True)

    create = subparsers.add_parser("create", help="Create DOCX from simple Markdown")
    create.add_argument("input", type=Path)
    create.add_argument("output", type=Path)
    create.add_argument("--title", default="")
    create.add_argument("--author", default=AUTHOR)

    inspect = subparsers.add_parser("inspect", help="Inspect DOCX metadata and structure")
    inspect.add_argument("input", type=Path)
    inspect.add_argument("--text", action="store_true")

    replace = subparsers.add_parser("replace", help="Replace text in a DOCX copy")
    replace.add_argument("input", type=Path)
    replace.add_argument("output", type=Path)
    replace.add_argument("--set", dest="replacements", action="append", required=True)
    replace.add_argument("--author", default=AUTHOR)

    render = subparsers.add_parser("render", help="Render DOCX to PDF with LibreOffice")
    render.add_argument("input", type=Path)
    render.add_argument("output_dir", type=Path)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "create":
        create_docx(args.input, args.output, args.title, args.author)
        print(json.dumps(inspect_docx(args.output, False), ensure_ascii=False, indent=2))
    elif args.command == "inspect":
        print(json.dumps(inspect_docx(args.input, args.text), ensure_ascii=False, indent=2))
    elif args.command == "replace":
        hits = replace_docx(
            args.input,
            args.output,
            parse_replacements(args.replacements),
            args.author,
        )
        result = inspect_docx(args.output, False)
        result["replacements"] = hits
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(render_docx(args.input, args.output_dir))
    return 0


if __name__ == "__main__":
    sys.exit(main())
