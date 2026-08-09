#!/usr/bin/env python3
"""Fill named placeholders in local text, DOCX, or PDF form files.

Original utility maintained by Rylai for Codex and Hermes skill workflows.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import zipfile
from xml.etree import ElementTree


PLACEHOLDER = re.compile(r"\{\{\s*([A-Za-z][A-Za-z0-9_.-]*)\s*\}\}")
WORD_PARAGRAPH = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p"
WORD_TEXT = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t"


def load_values(json_path: Path | None, pairs: list[str]) -> dict[str, str]:
    values: dict[str, str] = {}
    if json_path:
        payload = json.loads(json_path.read_text(encoding="utf-8-sig"))
        if not isinstance(payload, dict):
            raise RuntimeError("values JSON must contain an object")
        for key, value in payload.items():
            if isinstance(value, (dict, list)):
                values[str(key)] = json.dumps(value, ensure_ascii=False)
            elif value is None:
                values[str(key)] = ""
            else:
                values[str(key)] = str(value)
    for pair in pairs:
        if "=" not in pair:
            raise RuntimeError(f"invalid --set value: {pair}")
        key, value = pair.split("=", 1)
        key = key.strip()
        if not key:
            raise RuntimeError("--set requires a non-empty key")
        values[key] = value
    if not values:
        raise RuntimeError("provide --values or at least one --set KEY=VALUE")
    return values


def replace_placeholders(text: str, values: dict[str, str], drop_missing: bool) -> str:
    def replacement(match: re.Match[str]) -> str:
        key = match.group(1)
        if key in values:
            return values[key]
        return "" if drop_missing else match.group(0)

    return PLACEHOLDER.sub(replacement, text)


def prepare_paths(source_arg: Path, output_arg: Path, overwrite: bool) -> tuple[Path, Path]:
    source = source_arg.expanduser().resolve()
    output = output_arg.expanduser().resolve()
    if not source.is_file():
        raise FileNotFoundError(f"template not found: {source}")
    if source == output:
        raise RuntimeError("template and output must be different files")
    if output.exists() and not overwrite:
        raise FileExistsError(f"output already exists: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    return source, outpu


def temporary_output(destination: Path, suffix: str = ".tmp") -> Path:
    with tempfile.NamedTemporaryFile(
        delete=False,
        dir=destination.parent,
        prefix=f".{destination.name}.",
        suffix=suffix,
    ) as handle:
        return Path(handle.name)


def fill_text(
    source: Path,
    output: Path,
    values: dict[str, str],
    drop_missing: bool,
) -> None:
    text = source.read_text(encoding="utf-8-sig")
    rendered = replace_placeholders(text, values, drop_missing)
    temporary = temporary_output(output)
    try:
        temporary.write_text(rendered, encoding="utf-8", newline="\n")
        os.replace(temporary, output)
    finally:
        temporary.unlink(missing_ok=True)


def replace_word_xml(data: bytes, values: dict[str, str], drop_missing: bool) -> bytes:
    try:
        root = ElementTree.fromstring(data)
    except ElementTree.ParseError:
        return data
    changed = False
    for paragraph in root.iter(WORD_PARAGRAPH):
        text_nodes = list(paragraph.iter(WORD_TEXT))
        if not text_nodes:
            continue
        original = "".join(node.text or "" for node in text_nodes)
        rendered = replace_placeholders(original, values, drop_missing)
        if rendered == original:
            continue
        text_nodes[0].text = rendered
        for node in text_nodes[1:]:
            node.text = ""
        changed = True
    if not changed:
        return data
    return ElementTree.tostring(root, encoding="utf-8", xml_declaration=True)


def fill_docx(
    source: Path,
    output: Path,
    values: dict[str, str],
    drop_missing: bool,
) -> None:
    temporary = temporary_output(output, ".docx")
    try:
        with zipfile.ZipFile(source, "r") as input_archive:
            with zipfile.ZipFile(temporary, "w") as output_archive:
                for item in input_archive.infolist():
                    data = input_archive.read(item.filename)
                    if item.filename.startswith("word/") and item.filename.endswith(".xml"):
                        data = replace_word_xml(data, values, drop_missing)
                    output_archive.writestr(item, data)
        os.replace(temporary, output)
    finally:
        temporary.unlink(missing_ok=True)


def fill_pdf(source: Path, output: Path, values: dict[str, str]) -> None:
    try:
        from pypdf import PdfReader, PdfWriter
    except ImportError as error:
        raise RuntimeError("install pypdf to fill PDF form fields") from error

    reader = PdfReader(str(source))
    fields = reader.get_fields() or {}
    if not fields:
        raise RuntimeError("the PDF has no interactive form fields")
    matching_values = {key: value for key, value in values.items() if key in fields}
    if not matching_values:
        raise RuntimeError("none of the provided keys match a PDF form field")

    writer = PdfWriter()
    writer.clone_document_from_reader(reader)
    for page in writer.pages:
        writer.update_page_form_field_values(page, matching_values, auto_regenerate=False)

    temporary = temporary_output(output, ".pdf")
    try:
        with temporary.open("wb") as handle:
            writer.write(handle)
        os.replace(temporary, output)
    finally:
        temporary.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--values", type=Path, help="UTF-8 JSON object")
    parser.add_argument("--set", action="append", default=[], metavar="KEY=VALUE")
    parser.add_argument("--drop-missing", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    try:
        source, output = prepare_paths(args.source, args.output, args.overwrite)
        values = load_values(args.values, args.set)
        extension = source.suffix.lower()
        if extension in {".txt", ".md", ".markdown", ".html", ".htm", ".xml", ".csv"}:
            fill_text(source, output, values, args.drop_missing)
        elif extension == ".docx":
            fill_docx(source, output, values, args.drop_missing)
        elif extension == ".pdf":
            fill_pdf(source, output, values)
        else:
            raise RuntimeError(f"unsupported template format: {extension or 'extensionless input'}")
        print(f"Wrote {output}")
        return 0
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
