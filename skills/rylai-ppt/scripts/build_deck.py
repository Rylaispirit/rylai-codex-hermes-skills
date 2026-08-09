#!/usr/bin/env python3
"""Local PPTX utility for the Rylai Codex-Hermes skill."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse


class PptxToolError(RuntimeError):
    pass


def load_pptx():
    try:
        from pptx import Presentation
        from pptx.dml.color import RGBColor
        from pptx.enum.text import PP_ALIGN
        from pptx.util import Inches, P
    except ImportError as exc:
        raise PptxToolError("Missing dependency: install python-pptx with Python.") from exc
    return Presentation, RGBColor, PP_ALIGN, Inches, P


def existing_file(value: str) -> Path:
    path = Path(value).expanduser().resolve()
    if not path.is_file():
        raise PptxToolError(f"Input file does not exist: {path}")
    return path


def output_file(value: str, force: bool) -> Path:
    path = Path(value).expanduser().resolve()
    if path.exists() and not force:
        raise PptxToolError(f"Output already exists: {path}. Add --force to replace it.")
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def set_background(slide, color, RGBColor) -> None:
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(*color)


def add_text_box(
    slide,
    text: str,
    x: float,
    y: float,
    width: float,
    height: float,
    size: int,
    color,
    Inches,
    Pt,
    RGBColor,
    bold: bool = False,
) -> None:
    shape = slide.shapes.add_textbox(
        Inches(x), Inches(y), Inches(width), Inches(height)
    )
    frame = shape.text_frame
    frame.clear()
    frame.word_wrap = True
    paragraph = frame.paragraphs[0]
    paragraph.text = tex
    for run in paragraph.runs:
        run.font.name = "Aptos"
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.color.rgb = RGBColor(*color)


def local_image_path(value: str, spec_dir: Path) -> Path:
    parsed = urlparse(value)
    if parsed.scheme or parsed.netloc or value.startswith("//"):
        raise PptxToolError("Image URLs are not allowed. Use a local file path.")
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = spec_dir / path
    path = path.resolve()
    if not path.is_file():
        raise PptxToolError(f"Local image does not exist: {path}")
    return path


def add_contained_picture(slide, image: Path, x, y, width, height, Inches) -> None:
    try:
        from PIL import Image
    except ImportError as exc:
        raise PptxToolError("Pillow is required for local image placement.") from exc

    with Image.open(image) as source:
        source_width, source_height = source.size
    scale = min(width / source_width, height / source_height)
    draw_width = source_width * scale
    draw_height = source_height * scale
    draw_x = x + (width - draw_width) / 2
    draw_y = y + (height - draw_height) / 2
    slide.shapes.add_picture(
        str(image),
        Inches(draw_x),
        Inches(draw_y),
        Inches(draw_width),
        Inches(draw_height),
    )


def add_footer(slide, number: int, Inches, Pt, RGBColor) -> None:
    add_text_box(
        slide,
        f"Rylai  |  {number}",
        10.8,
        7.05,
        2.0,
        0.25,
        9,
        (88, 94, 99),
        Inches,
        Pt,
        RGBColor,
    )


def build_deck(spec: dict, spec_dir: Path):
    Presentation, RGBColor, _, Inches, Pt = load_pptx()
    presentation = Presentation()
    presentation.slide_width = Inches(13.333)
    presentation.slide_height = Inches(7.5)
    blank_layout = presentation.slide_layouts[6]

    background = (247, 247, 243)
    ink = (31, 39, 43)
    muted = (88, 94, 99)
    accent = (15, 118, 110)
    highlight = (226, 91, 70)

    title = str(spec.get("title") or "Untitled presentation").strip()
    subtitle = str(spec.get("subtitle") or "").strip()
    slides = spec.get("slides")
    if slides is None:
        slides = []
    if not isinstance(slides, list):
        raise PptxToolError("'slides' must be a JSON array.")

    title_slide = presentation.slides.add_slide(blank_layout)
    set_background(title_slide, background, RGBColor)
    line = title_slide.shapes.add_shape(
        1, Inches(0.7), Inches(1.05), Inches(0.14), Inches(5.1)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = RGBColor(*highlight)
    line.line.fill.background()
    add_text_box(
        title_slide,
        title,
        1.2,
        1.2,
        10.9,
        2.2,
        34,
        ink,
        Inches,
        Pt,
        RGBColor,
        bold=True,
    )
    if subtitle:
        add_text_box(
            title_slide,
            subtitle,
            1.2,
            3.7,
            9.8,
            1.0,
            18,
            muted,
            Inches,
            Pt,
            RGBColor,
        )
    add_text_box(
        title_slide,
        "Rylai",
        1.2,
        6.4,
        2.0,
        0.4,
        12,
        accent,
        Inches,
        Pt,
        RGBColor,
        bold=True,
    )

    for slide_number, item in enumerate(slides, start=2):
        if not isinstance(item, dict):
            raise PptxToolError("Every slide entry must be a JSON object.")
        slide = presentation.slides.add_slide(blank_layout)
        set_background(slide, background, RGBColor)
        slide_title = str(item.get("title") or f"Slide {slide_number}").strip()
        bullets = item.get("bullets") or []
        if not isinstance(bullets, list):
            raise PptxToolError(f"'bullets' on slide {slide_number} must be an array.")

        add_text_box(
            slide,
            slide_title,
            0.75,
            0.55,
            11.7,
            0.75,
            25,
            ink,
            Inches,
            Pt,
            RGBColor,
            bold=True,
        )
        rule = slide.shapes.add_shape(
            1, Inches(0.75), Inches(1.42), Inches(1.35), Inches(0.08)
        )
        rule.fill.solid()
        rule.fill.fore_color.rgb = RGBColor(*accent)
        rule.line.fill.background()

        image_value = item.get("image")
        text_width = 6.5 if image_value else 11.6
        bullet_text = "\n\n".join(f"- {str(value).strip()}" for value in bullets)
        if not bullet_text:
            bullet_text = str(item.get("body") or "").strip()
        add_text_box(
            slide,
            bullet_text,
            0.9,
            1.9,
            text_width,
            4.55,
            18,
            ink,
            Inches,
            Pt,
            RGBColor,
        )

        if image_value:
            image = local_image_path(str(image_value), spec_dir)
            add_contained_picture(
                slide, image, 8.0, 1.8, 4.55, 4.7, Inches
            )
        add_footer(slide, slide_number, Inches, Pt, RGBColor)

    return presentation


def command_build(args: argparse.Namespace) -> None:
    spec_path = existing_file(args.spec)
    output = output_file(args.output, args.force)
    try:
        spec = json.loads(spec_path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise PptxToolError(f"Invalid JSON specification: {exc}") from exc
    if not isinstance(spec, dict):
        raise PptxToolError("The JSON root must be an object.")
    presentation = build_deck(spec, spec_path.parent)
    presentation.save(str(output))
    print(f"Wrote {len(presentation.slides)} slide(s) to {output}")


def presentation_summary(path: Path) -> dict:
    Presentation, _, _, _, _ = load_pptx()
    presentation = Presentation(str(path))
    slides = []
    for number, slide in enumerate(presentation.slides, start=1):
        texts = []
        for shape in slide.shapes:
            if getattr(shape, "has_text_frame", False):
                text = shape.text.strip()
                if text:
                    texts.append(text)
        slides.append(
            {
                "number": number,
                "title": texts[0] if texts else "",
                "text_blocks": len(texts),
                "shapes": len(slide.shapes),
            }
        )
    return {
        "file": str(path),
        "slides": len(presentation.slides),
        "width_emu": presentation.slide_width,
        "height_emu": presentation.slide_height,
        "items": slides,
    }


def command_inspect(args: argparse.Namespace) -> None:
    path = existing_file(args.input)
    print(json.dumps(presentation_summary(path), indent=2, ensure_ascii=False))


def command_extract(args: argparse.Namespace) -> None:
    Presentation, _, _, _, _ = load_pptx()
    source = existing_file(args.input)
    output = output_file(args.output, args.force)
    presentation = Presentation(str(source))
    sections = []
    for number, slide in enumerate(presentation.slides, start=1):
        lines = []
        for shape in slide.shapes:
            if getattr(shape, "has_text_frame", False):
                text = shape.text.strip()
                if text:
                    lines.append(text)
            if getattr(shape, "has_table", False):
                for row in shape.table.rows:
                    lines.append(" | ".join(cell.text.strip() for cell in row.cells))
        sections.append(f"## Slide {number}\n\n" + "\n\n".join(lines))
    output.write_text("# Presentation text\n\n" + "\n\n".join(sections) + "\n", encoding="utf-8")
    print(f"Extracted {len(presentation.slides)} slide(s) to {output}")


def run_external(command: list[str]) -> None:
    executable = Path(command[0])
    if os.name == "nt" and executable.suffix.lower() in {".bat", ".cmd"}:
        subprocess.run(subprocess.list2cmdline(command), shell=True, check=True)
    else:
        subprocess.run(command, check=True)


def command_render(args: argparse.Namespace) -> None:
    source = existing_file(args.input)
    tool = shutil.which("soffice") or shutil.which("libreoffice")
    if tool is None:
        raise PptxToolError("LibreOffice was not found on PATH.")
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    run_external(
        [
            tool,
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            str(output_dir),
            str(source),
        ]
    )
    output = output_dir / f"{source.stem}.pdf"
    if not output.is_file():
        raise PptxToolError("LibreOffice finished without producing the expected PDF.")
    print(f"Rendered presentation to {output}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Local PPTX utility by Rylai.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    build = subparsers.add_parser("build", help="Build a deck from a JSON specification.")
    build.add_argument("spec")
    build.add_argument("output")
    build.add_argument("--force", action="store_true")
    build.set_defaults(func=command_build)

    inspect = subparsers.add_parser("inspect", help="Print a JSON deck summary.")
    inspect.add_argument("input")
    inspect.set_defaults(func=command_inspect)

    extract = subparsers.add_parser("extract", help="Extract slide text as Markdown.")
    extract.add_argument("input")
    extract.add_argument("output")
    extract.add_argument("--force", action="store_true")
    extract.set_defaults(func=command_extract)

    render = subparsers.add_parser("render", help="Render the deck to PDF with LibreOffice.")
    render.add_argument("input")
    render.add_argument("output_dir")
    render.set_defaults(func=command_render)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        args.func(args)
    except (
        PptxToolError,
        ValueError,
        OSError,
        subprocess.CalledProcessError,
    ) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
