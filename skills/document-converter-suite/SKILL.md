---
name: document-converter-suite
description: Convert local PDF, Office, Markdown, HTML, text, CSV, TSV, and JSON files with dependency-aware fallbacks; batch-convert folders; extract tables; fill templates; and perform focused PDF page operations. Use when Codex or Hermes needs editable document output and can accept best-effort semantic conversion rather than guaranteed pixel-perfect reproduction.
metadata:
  maintainer: "Rylai"
  adapted_by: "Rylai"
  edition: "Codex-Hermes"
  edition_version: "2.0.0"
  provenance: "clean-room-original"
  hermes:
    category: "documents"
---

# Document Converter Suite

Original portable workflow by Rylai.

Use the bundled scripts for deterministic local-file work. Keep source files unchanged and inspect every generated artifact.

## Start With A Dependency Check

```powershell
python scripts/rylai_convert.py doctor


The report distinguishes required Python support from optional routes provided by MarkItDown, Pandoc, LibreOffice, `pypdf`, `python-docx`, `python-pptx`, `openpyxl`, and `pdfplumber`.

## Convert One File

```powershell
python scripts/rylai_convert.py convert input.docx output.md
python scripts/rylai_convert.py convert notes.md notes.docx
python scripts/rylai_convert.py convert workbook.xlsx workbook.pdf


Add `--overwrite` only after checking that replacing the destination is intended.

## Convert A Folder

```powershell
python scripts/rylai_convert.py batch source output --to md --recursive
python scripts/rylai_convert.py batch source output --to pdf --include docx --include pptx


The batch command preserves relative paths and reports every failed file.

## Focused Utilities

PDF page operations:

```powershell
python scripts/rylai_pdf_pages.py info report.pdf
python scripts/rylai_pdf_pages.py extract report.pdf excerpt.pdf --pages 1,3-5
python scripts/rylai_pdf_pages.py merge combined.pdf part-a.pdf part-b.pdf
python scripts/rylai_pdf_pages.py split report.pdf split-pages
python scripts/rylai_pdf_pages.py rotate report.pdf rotated.pdf --pages all --degrees 90


Table extraction:

```powershell
python scripts/rylai_tables.py data.xlsx table.csv --sheet Summary
python scripts/rylai_tables.py report.pdf table.md --table 2


Template filling:

```powershell
python scripts/rylai_template_fill.py template.docx filled.docx --values values.json
python scripts/rylai_template_fill.py template.md filled.md --set project=Rylai --set status=Ready


Read `references/routes.md` when choosing between conversion engines or explaining limitations.

## Operating Rules

- Resolve scripts relative to this skill folder.
- Accept local files only; do not download a URL and convert it without explicit user approval.
- Never execute macros, embedded programs, or document attachments.
- Treat OCR as a separate step. A scanned PDF may contain no extractable text.
- Prefer semantic extraction for editing and LibreOffice or Pandoc routes for format conversion.
- Do not promise exact fonts, pagination, animation, chart, formula, or layout preservation.
- Use a dedicated format skill when visual fidelity or advanced editing is the primary requirement.
- Report the selected route, missing dependency, and any known loss in the final answer.
