---
name: notion-infographic
description: Turn articles, notes, transcripts, or research into a consistent series of clean hand-drawn infographics. Use when Codex or Hermes should plan, generate, and visually verify a multi-image social or presentation series with concise text.
metadata:
  maintainer: "Rylai"
  adapted_by: "Rylai"
  edition: "Codex-Hermes"
  edition_version: "2.0.0"
  provenance: "clean-room-original"
  hermes:
    category: "media"
---

# Rylai Notes Infographic

Create a coherent infographic series from source material. This is an original Rylai workflow for Codex and Hermes. The visual direction is a general notebook-style aesthetic and is not an official Notion product or brand asset.

## Workflow

1. Read the complete source before proposing images.
2. Extract the central promise and the smallest set of independent supporting ideas.
3. Honor a user-specified image count. Otherwise create three to eight images; use at most twelve.
4. Write a short series plan before generation:

```json
[
  {
    "file": "infographic-01.png",
    "role": "cover",
    "headline": "Short visible headline",
    "message": "One idea the image must communicate",
    "scene": "Concrete visual metaphor or diagram"
  }
]


5. Generate images one at a time so the next prompt can correct consistency problems.
6. Inspect every result. Regenerate images with unreadable text, accidental logos, inconsistent characters, clipped content, or a different palette.
7. Deliver the ordered files and a one-line description of the series.

## Prompt Construction

Build each prompt from a fixed style block plus one variable scene block.

Fixed style block:

```tex
Rylai notebook infographic, editorial hand-drawn linework on warm white paper,
confident imperfect marker strokes, simple flat shapes, generous whitespace,
black ink with teal, coral, and golden-yellow accents, clear visual hierarchy,
friendly human proportions, minimal decoration, no gradients, no 3D rendering,
no photorealism, no logos, no watermark.


Variable scene block:

- State the one idea for this image.
- Describe a concrete subject, diagram, sequence, or comparison.
- Specify only the essential visible labels.
- Repeat any recurring character, clothing, props, and palette exactly.
- Add the requested aspect ratio and language.

Keep on-image text short. When exact typography matters, generate the artwork without text and add text later with a local deterministic editor.

## Series Structure

- Cover: topic and clear promise.
- Body: one independent idea per image.
- Summary: synthesis, checklist, or call to action when useful.

Do not add a cover or summary merely to increase the count. Merge overlapping ideas and split overloaded images.

## Runtime Mapping

- Codex: use `image_gen`.
- Hermes: use `image_generate` or the configured image backend.
- If a backend cannot preserve a consistent character, use the best approved image as a visual reference for later generations.
- Save outputs in the user's workspace with zero-padded names such as `infographic-01.png`.

## Quality Gate

- The image communicates one idea within three seconds.
- Text is readable at the target publishing size.
- Every claim comes from the supplied source or is clearly labeled as interpretation.
- Palette, line quality, character design, margins, and aspect ratio match across the series.
- No external logo, trademarked UI, remote asset, or creator signature appears unless the user supplied and authorized it.

Authored by Rylai for Codex and Hermes.
