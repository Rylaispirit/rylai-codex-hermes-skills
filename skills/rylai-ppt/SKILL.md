---
name: rylai-ppt
description: Create editable PowerPoint decks from a local JSON specification using Rylai's visual system, python-pptx, deterministic slide types, and optional rendering.
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

# Rylai PPT

Use the bundled Python workflow to create a clean, editable `.pptx`. The
renderer is an original Rylai implementation built on `python-pptx`. It uses
local PowerPoint elements and does not load HTML templates, remote images, or
hosted assets.

## Requirements

- Python 3
- `python-pptx`
- Optional LibreOffice for rendering to PDF

## Workflow

1. Read the user's source material and identify the audience, purpose, slide count, language, and required facts.
2. Create a JSON deck specification by adapting `examples/deck.json`.
3. Keep one message per slide. Split dense content instead of shrinking text.
4. Validate the specification:

```bash
python <skill-dir>/scripts/build_deck.py build <deck.json> <output.pptx>
```

5. Build the presentation:

```bash
python <skill-dir>/scripts/build_deck.py inspect <output.pptx>
```

6. Render the result when LibreOffice is available:

```bash
python <skill-dir>/scripts/build_deck.py render <output.pptx> <render-dir>
```

7. Check clipping, contrast, reading order, repeated wording, and slide count
   before delivery.

## Slide Types

- `cover`: title, subtitle, eyebrow, footer
- `section`: number, title, summary
- `bullets`: title, kicker, and two to six structured items
- `metrics`: title and two to four value cards
- `comparison`: two labeled lists with two to five items each
- `timeline`: two to five ordered steps
- `quote`: quotation and attribution
- `closing`: final title, subtitle, and contact line

Read `references/deck-spec.md` when field-level constraints are needed. Unknown slide fields fail validation so the deck stays portable and deterministic.

## Design Rules

- Use the theme fields in the JSON spec rather than editing renderer constants for each deck.
- Use a restrained multi-color palette with one primary accent and one secondary accent.
- Keep titles short, body copy specific, and metrics attributable to the user's material.
- Use only the supported local vector icons: `circle`, `square`, `diamond`, `check`, and `arrow`.
- Do not add remote URLs as image sources. This workflow intentionally has no image field.
- Preserve user-provided brand wording. Do not invent customer names, testimonials, statistics, or claims.

## Runtime Notes

- Codex, Hermes, and Claude execute the same bundled Python scripts.
- Resolve all bundled paths from this skill directory.
- Write generated decks to the user's requested workspace, not inside the installed skill.
- Report the final path and the number and types of slides created.

Authored by Rylai for Codex, Hermes, and Claude.
