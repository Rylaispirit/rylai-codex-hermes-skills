---
name: xlsx
description: Create, inspect, edit, and verify Excel .xlsx workbooks with openpyxl. Use when Codex or Hermes must turn CSV or TSV data into a styled workbook, update cells or formulas in an existing workbook, inspect sheets and formula errors, or optionally recalculate and render a workbook with local LibreOffice.
metadata:
  maintainer: "Rylai"
  adapted_by: "Rylai"
  edition: "Codex-Hermes"
  edition_version: "2.0.0"
  provenance: "clean-room-original"
  hermes:
    category: "data"
---

# Rylai XLSX

This is an original Rylai Codex-Hermes workflow. Use the open-source
`openpyxl` package for workbook operations and LibreOffice only for optional
formula recalculation or PDF rendering.

## Runtime

- Required for the bundled script: Python 3 and `openpyxl`.
- Optional: LibreOffice (`soffice`) for recalculation and PDF rendering.
- Resolve `scripts/xlsx_tool.py` relative to this skill folder.
- Do not install packages unless the user approves installation.
- Set workbook creator and last editor to `Rylai` unless the user explicitly
  requests another author.

## Workflow

1. Inspect the workbook or source table before changing it.
2. Preserve existing sheet names, formulas, and styles unless the task requires
   a change.
3. Save to a new output path instead of overwriting the source.
4. Reopen the saved workbook and inspect formula and error counts.
5. When formula results must be refreshed, use LibreOffice recalculation if i
   is available.

## Bundled CLI

Create a styled workbook from CSV or TSV:

```bash
python scripts/xlsx_tool.py create input.csv output.xlsx --sheet Data
python scripts/xlsx_tool.py create input.tsv output.xlsx --delimiter tab


Inspect workbook structure, formulas, and visible spreadsheet errors:

```bash
python scripts/xlsx_tool.py inspect output.xlsx


Update cells or formulas while keeping the source unchanged:

```bash
python scripts/xlsx_tool.py set input.xlsx output.xlsx \
  --cell "Summary!B2=1250" \
  --cell "Summary!B3==SUM(Data!B2:B20)"


The first `=` separates the cell address from its value. A formula therefore
uses a second `=`.

Recalculate formulas through a LibreOffice save round trip:

```bash
python scripts/xlsx_tool.py recalc input.xlsx recalculated.xlsx


Render workbook sheets to PDF:

```bash
python scripts/xlsx_tool.py render input.xlsx rendered


## Quality Rules

- Use formulas for values that should update when inputs change.
- Keep identifiers with leading zeroes as text.
- Freeze the header and enable filters for newly created data tables.
- Use clear number formats for dates, percentages, currency, and totals.
- Treat `#REF!`, `#DIV/0!`, `#VALUE!`, `#NAME?`, `#N/A`, and `#NUM!` as
  delivery blockers unless the user explicitly expects them.
- Report that recalculation or visual verification was skipped when
  LibreOffice is unavailable.
