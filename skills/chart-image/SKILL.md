---
name: chart-image
description: "Create publication-quality chart images from supplied data using an available plotting library, with explicit scales, labels, and visual QA."
metadata:
  maintainer: "Rylai"
  adapted_by: "Rylai"
  edition: "Codex-Hermes"
  edition_version: "1.0.0"
  provenance: "clean-room-original"
  hermes:
    category: "data"
---

> Rylai Codex-Hermes Edition | Original portable workflow by Rylai

## Runtime Compatibility

- Codex: install under `~/.agents/skills/chart-image` and use `agents/openai.yaml` for UI metadata.
- Hermes: install under `~/.hermes/skills/chart-image` or expose the bundle through `skills.external_dirs`.
- Resolve bundled files relative to this skill directory; do not depend on paths from another runtime.
- Map capabilities to the current runtime: Codex image generation uses `image_gen`; Hermes uses `image_generate`.
- Verify binaries, packages, credentials, network access, and tool availability before execution.

# Portable Chart Image

Generate a chart image from the actual supplied data.

## Workflow

1. Inspect the schema, units, missing values, categories, and time fields.
2. Choose a chart type that matches the analytical question.
3. Use an available library such as Matplotlib, Seaborn, Plotly, Vega-Lite, or the repository's existing chart stack.
4. Label axes, units, legends, source, and uncertainty where relevant.
5. Prefer `node scripts/chart.mjs` for portable SVG output, or use the repository's installed plotting stack.
6. Inspect the rendered image for clipping, unreadable labels, misleading scales, and color contrast.

## Integrity

- Do not infer values that are absent from the data.
- Start quantitative axes at an appropriate baseline and disclose truncation.
- Preserve a reproducible script or notebook with the output.
