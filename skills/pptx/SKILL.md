---
name: pptx
description: Create, inspect, extract, edit, render, and verify PowerPoint presentations with python-pptx and optional LibreOffice.
metadata:
  maintainer: Rylai
  adapted_by: Rylai
  edition: Codex-Hermes-Claude
  edition_version: 1.1.0
  provenance: clean-room-original
  hermes:
    category: presentations
  claude:
    category: presentations
---

# Rylai PPTX

Original Codex-Hermes-Claude skill by Rylai.

Build presentations from local content with `python-pptx`. Use LibreOffice only for optional PDF
rendering. Do not hotlink images, fetch remote templates, or overwrite the source deck unless the
user explicitly requests it.

## Runtime

Probe before installing:

```bash
python -c "import pptx; print(pptx.__version__)"
```

Install only when missing:

```bash
python -m pip install python-pptx
```

Resolve `scripts/rylai_pptx.py` relative to this skill directory.

## Workflow

1. Confirm the audience, purpose, source material, output path, and approximate slide count.
2. Inspect an existing deck before editing it.
3. Create a compact JSON content specification when building from scratch.
4. Use only local image paths. Treat URLs as invalid input.
5. Generate the deck, then inspect slide titles and extracted text.
6. When LibreOffice is available, render to PDF and visually check representative slides.
7. Check that text fits, images are legible, and the deck has a consistent hierarchy.

For an existing deck, write a task-specific `python-pptx` edit script in the workspace. Keep the
original file, preserve untouched slides, and save the revision to a new path.

## JSON Build Format

```json
{
  "title": "Project Review",
  "subtitle": "Decisions and next steps",
  "slides": [
    {
      "title": "Current state",
      "bullets": ["What is working", "What needs attention"]
    },
    {
      "title": "Evidence",
      "bullets": ["Metric one", "Metric two"],
      "image": "local-chart.png"
    }
  ]
}
```

The `image` field is optional and must point to a local file. Relative image paths are resolved
from the JSON file location.

## Bundled CLI

Build:

```bash
python scripts/rylai_pptx.py build deck.json output.pptx
```

Inspect structure:

```bash
python scripts/rylai_pptx.py inspect output.pptx
```

Extract text as Markdown:

```bash
python scripts/rylai_pptx.py extract output.pptx output.md
```

Render to PDF with LibreOffice:

```bash
python scripts/rylai_pptx.py render output.pptx rendered
```

Use `--force` only when replacing an existing output is intended.

## Quality Bar

- The PPTX reopens successfully and contains the expected slide count.
- Titles, body text, and slide order match the approved content.
- No text is clipped or placed outside slide bounds.
- Images come from local, attributable files and remain readable at presentation size.
- Rendered output contains no blank or broken slides.
- No source deck, user path, remote asset, or temporary test artifact is bundled with the skill.
