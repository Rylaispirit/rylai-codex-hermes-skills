# Conversion Routes

Maintainer: Rylai

Choose a route by output purpose, not only by file extension.

| Task | First route | Fallback | Expected loss |
|---|---|---|---|
| PDF or Office to Markdown | MarkItDown | Format-specific Python reader | Page layout, floating objects, some media |
| PDF to text | MarkItDown | `pypdf` | Columns, tables, scanned text |
| DOCX to text or Markdown | MarkItDown | `python-docx` | Positioned objects, some headers and fields |
| PPTX to text or Markdown | MarkItDown | `python-pptx` | Visual relationships, animations |
| XLSX to Markdown | MarkItDown | `openpyxl` | Styling, charts, cached formula behavior |
| Markdown or HTML to DOCX/PDF | Pandoc | None | Reference styling without extra templates |
| Office to PDF or another Office type | LibreOffice headless mode | None | Font metrics, pagination, unsupported features |
| CSV, TSV, JSON, text, HTML | Python standard library | None | Rich HTML layout |

## Optional Python Packages

- `pypdf`: PDF reading, writing, page operations, and AcroForm filling
- `python-docx`: DOCX text fallback
- `python-pptx`: PPTX text fallback
- `openpyxl`: XLSX text and table fallback
- `pdfplumber`: PDF table extraction

## Verification

- Confirm the output opens.
- Compare headings, tables, links, page counts, and row counts against the source.
- Render visually when layout matters.
- Recalculate spreadsheets in an office engine before trusting formula results.
- Stop and report the limitation when every available route would discard essential content.
