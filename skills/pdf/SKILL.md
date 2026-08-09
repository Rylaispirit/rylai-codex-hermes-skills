---
name: pdf
description: Create, inspect, extract, merge, split, rotate, and render PDF files with local open-source tools. Use whenever Codex or Hermes must read, produce, modify, or visually verify a PDF.
metadata:
  maintainer: "Rylai"
  adapted_by: "Rylai"
  edition: "Codex-Hermes"
  edition_version: "2.0.0"
  provenance: "clean-room-original"
  hermes:
    category: "documents"
---

# Rylai PDF

Original Codex-Hermes skill by Rylai.

Use local files and deterministic tools. Preserve the source document unless the user explicitly
requests an in-place replacement. Never invent passwords, embed credentials, or upload documents
to an external service without direct approval.

## Runtime

Use Python 3 with:

- `pypdf` for page-level inspection and editing.
- `pdfplumber` when higher-quality text extraction is useful.
- `pypdfium2` or Poppler `pdftoppm` for optional page rendering.
- LibreOffice only when converting an Office source into PDF.

Probe before installing:

```bash
python -c "import pypdf; print(pypdf.__version__)"
python -c "import pdfplumber; print(pdfplumber.__version__)"


Install only missing Python packages:

```bash
python -m pip install pypdf pdfplumber pypdfium2


Resolve `scripts/rylai_pdf.py` relative to this skill directory.

## Workflow

1. Confirm the input path, requested operation, output path, and page range.
2. Run `info` before editing an unfamiliar or encrypted PDF.
3. Write to a new output path. Use `--force` only when replacement is intended.
4. Re-open the result and check page count, metadata, and extracted text where applicable.
5. For layout-sensitive work, render representative pages and inspect the PNG output.
6. Report skipped checks when Poppler, LibreOffice, OCR, or another optional dependency is absent.

For scanned pages with no useful text layer, use an available local OCR engine. Keep the original
PDF and state which OCR tool and language model were used.

## Bundled CLI

Inspect:

```bash
python scripts/rylai_pdf.py info input.pdf


Extract selected pages:

```bash
python scripts/rylai_pdf.py extract input.pdf output.txt --pages 1-3,7


Merge:

```bash
python scripts/rylai_pdf.py merge output.pdf first.pdf second.pdf


Split selected pages into individual files:

```bash
python scripts/rylai_pdf.py split input.pdf output-pages --pages 2-5


Rotate selected pages clockwise:

```bash
python scripts/rylai_pdf.py rotate input.pdf rotated.pdf 90 --pages 1,3


Render with local PDFium or Poppler:

```bash
python scripts/rylai_pdf.py render input.pdf rendered-pages --dpi 144


Add `--password` only when the user supplied the password for that document.

## Quality Bar

- The output opens without repair warnings.
- Page order, count, rotation, and selected ranges match the request.
- Extracted text is not silently empty; scanned pages are identified.
- Rendered pages have no unexpected clipping or blank output.
- No source file, temporary file, password, or user path is bundled with the skill.
