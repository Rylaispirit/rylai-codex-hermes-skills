---
name: image-analyzer
description: Inspect supplied images with available vision tools for OCR, visual description, object inspection, layout review, comparison, and structured extraction.
metadata:
  maintainer: Rylai
  adapted_by: Rylai
  edition: Codex-Hermes-Claude
  edition_version: 1.1.0
  provenance: clean-room-original
  hermes:
    category: media
  claude:
    category: media
---

> Rylai Codex-Hermes-Claude Edition | Original portable workflow by Rylai

# Image Analyzer

Analyze the supplied image itself before making claims.

## Workflow

1. Resolve the exact local file, attachment, or user-approved URL.
2. Inspect the original resolution when small text, fine detail, or cropping matters.
3. Match the analysis to the request: description, OCR, layout, objects, comparison, or extraction.
4. Separate direct observations from interpretation and uncertainty.
5. Preserve reading order for OCR and mark unreadable regions instead of guessing.
6. For structured extraction, define the schema first and use `null` for unavailable fields.
7. When comparing images, use the same checklist for every image.
8. Return concise evidence and note any resolution or visibility limits.

## Runtime Routes

- Use the image viewer or native vision capability available in Codex, Hermes,
  or Claude.
- Use an external OCR or vision service only when the user approves it and the
  required credentials are already configured.

## Safety

- Do not infer sensitive identity, health, ethnicity, or exact location without
  reliable evidence and a legitimate user request.
- Do not claim that an object, logo, person, or place is certain when the image
  only supports a tentative match.
- Never upload a private image to an external service without user approval.
