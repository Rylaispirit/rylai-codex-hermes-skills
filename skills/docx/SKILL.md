---
name: docx
description: Create, inspect, edit, and verify Microsoft Word .docx documents with python-docx. Use when Codex or Hermes must produce a Word report, convert simple Markdown into DOCX, replace text in an existing document, inspect document structure and metadata, or render a DOCX to PDF with an optional local LibreOffice installation.
metadata:
  maintainer: "Rylai"
  adapted_by: "Rylai"
  edition: "Codex-Hermes"
  edition_version: "2.0.0"
  provenance: "clean-room-original"
  hermes:
    category: "documents"
---

# Rylai DOCX

This is an original Rylai Codex-Hermes workflow. Use the open-source
`python-docx` package for document work and LibreOffice only when local
rendering is useful.

## Runtime

- Required for the bundled script: Python 3 and `python-docx`.
- Optional: LibreOffice (`soffice`) for PDF rendering.
- Resolve `scripts/docx_tool.py` relative to this skill folder.
- Do not install packages unless the user approves installation.
- Set new or modified document author metadata to `Rylai` unless the user
  explicitly requests another author.

## Workflow

1. Inspect source files and identify the requested document structure.
2. Keep instructions out of the final document body.
3. Create a new output path instead of overwriting the user's source.
4. Reopen the saved DOCX to verify that it is readable.
5. For layout-sensitive work, render to PDF with LibreOffice and inspect the
   result.

## Bundled CLI

Create a styled DOCX from simple Markdown:

```bash
python scripts/docx_tool.py create input.md output.docx --title "Report"


Supported Markdown includes headings, paragraphs, bullet lists, numbered
lists, block quotes, simple emphasis, inline code, and pipe tables.

Inspect structure and metadata:

```bash
python scripts/docx_tool.py inspect output.docx
python scripts/docx_tool.py inspect output.docx --tex


Replace text while keeping the source unchanged:

```bash
python scripts/docx_tool.py replace input.docx output.docx \
  --set "{{client}}=Rylai Studio" \
  --set "{{date}}=2026-08-09"


Render to PDF when LibreOffice is available:

```bash
python scripts/docx_tool.py render output.docx rendered


## Quality Rules

- Preserve the visual conventions of an existing document unless the user
  asks for a redesign.
- Use real heading styles instead of visually enlarged body paragraphs.
- Keep tables readable and avoid squeezing too many columns onto one page.
- Verify metadata, paragraph count, table count, and extracted text with the
  `inspect` command.
- Report that visual verification was skipped when LibreOffice is unavailable.
