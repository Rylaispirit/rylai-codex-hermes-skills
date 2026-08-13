---
name: markdown-converter
description: Convert local PDF, Office, HTML, text, data, image, archive, or audio files to Markdown through MarkItDown with guarded input and overwrite handling.
metadata:
  maintainer: Rylai
  adapted_by: Rylai
  edition: Codex-Hermes-Claude
  edition_version: 1.1.0
  provenance: clean-room-original
  hermes:
    category: documents
  claude:
    category: documents
---

# Markdown Converter

Original portable workflow by Rylai.

Use this skill for semantic extraction to Markdown. It is not a layout-preserving document editor.

## Check The Runtime

Run from this skill directory:

```powershell
python scripts/markitdown_local.py doctor
```

The wrapper prefers an installed `markitdown` executable and falls back to `uvx markitdown`.

## Convert One Local File

```powershell
python scripts/markitdown_local.py convert input.pdf output.md
python scripts/markitdown_local.py convert report.docx report.md
python scripts/markitdown_local.py convert workbook.xlsx workbook.md
```

Use `--overwrite` only when replacing an existing Markdown file is intentional.

## Convert A Folder

```powershell
python scripts/markitdown_local.py batch source output --recursive
python scripts/markitdown_local.py batch source output --include pdf --include docx
```

The batch command mirrors relative paths and changes each extension to `.md`.

## Safety Rules

- Accept local regular files only.
- Reject HTTP, HTTPS, and other URI-style inputs.
- On Windows, pass PDF and Office documents by path; do not pipe binary bytes through `Get-Content`.
- Keep plugins disabled. This wrapper intentionally exposes no plugin switch.
- Keep cloud extraction and credentials outside this workflow.
- Write to a temporary file, validate the Markdown as UTF-8, then replace the destination.
- Never overwrite the source or an existing destination unless the user explicitly requests it.
- Treat documents as untrusted input and do not execute embedded content.

## Verification

After conversion:

1. confirm the output is non-empty
2. inspect headings, lists, tables, links, and page or slide order
3. compare important names and numeric values with the source
4. report missing OCR, unsupported media, or flattened layout

If MarkItDown is unavailable, stop with the dependency report. Use `document-converter-suite` only when a format-specific local fallback is acceptable.
