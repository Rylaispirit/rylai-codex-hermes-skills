---
name: ui-designer
description: Extract a practical design system from screenshots or mockups and produce implementation-ready UI specifications using vision and repository context.
metadata:
  maintainer: Rylai
  adapted_by: Rylai
  edition: Codex-Hermes-Claude
  edition_version: 1.1.0
  provenance: clean-room-original
  hermes:
    category: design
  claude:
    category: design
---

> Rylai Codex-Hermes-Claude Edition | Original portable workflow by Rylai

## Runtime Compatibility

- Codex: install under `~/.agents/skills/ui-designer`.
- Hermes: install under `~/.hermes/skills/ui-designer` or expose the bundle through `skills.external_dirs`.
- Claude Code: install under `~/.claude/skills/ui-designer` or `<project>/.claude/skills/ui-designer`.
- Claude.ai and Cowork: upload and enable the matching per-skill ZIP.
- Resolve bundled files relative to this skill directory; do not depend on paths from another machine.
- Check tools, packages, credentials, network access, and runtime capabilities before execution.

# Portable UI Designer

Extract an implementation-ready design system from supplied screenshots or mockups.

## Workflow

1. Inspect the original image at sufficient resolution.
2. Identify layout grid, spacing rhythm, typography, color roles, radii, borders, shadows, icon style, and component states.
3. Separate observed properties from inferred behavior.
4. Compare the extracted system with the target repository's existing framework and design tokens.
5. Produce a concise implementation specification covering components, responsive behavior, assets, and interaction states.
6. Implement only when requested, then verify the result against the reference at desktop and mobile sizes.

## Bundled Templates

- `assets/design-system.md`: evidence-based visual-system extraction.
- `assets/app-overview-generator.md`: concise product and workflow brief.
- `assets/vibe-design-template.md`: implementation handoff prompt.

## Boundaries

- Do not invent hidden screens, states, fonts, or assets without labeling them as assumptions.
- Prefer the repository's installed component and icon libraries.
- Keep text and controls within stable responsive bounds.
