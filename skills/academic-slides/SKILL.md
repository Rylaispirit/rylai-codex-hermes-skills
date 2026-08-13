---
name: academic-slides
description: Plan, create, and review academic presentations for conference talks, thesis defenses, seminars, lab meetings, and paper-to-slide workflows.
metadata:
  maintainer: Rylai
  adapted_by: Rylai
  edition: Codex-Hermes-Claude
  edition_version: 1.1.0
  provenance: adapted-open-source
  upstream:
    url: https://github.com/EvoScientist/EvoSkills
    revision: 2e474118106f86c29082a6466b995ba59236614c
    license: Apache-2.0
  hermes:
    category: presentations
  claude:
    category: presentations
---

> Rylai Codex-Hermes-Claude Edition | Maintained and adapted by Rylai

## Runtime Compatibility

- Codex: install under `~/.agents/skills/academic-slides`.
- Hermes: install under `~/.hermes/skills/academic-slides` or expose the bundle through `skills.external_dirs`.
- Claude Code: install under `~/.claude/skills/academic-slides` or `<project>/.claude/skills/academic-slides`.
- Claude.ai and Cowork: upload and enable the matching per-skill ZIP.
- Resolve bundled files relative to this skill directory; do not depend on paths from another machine.
- Check tools, packages, credentials, network access, and runtime capabilities before execution.

# Academic Slides

Create or improve an academic presentation and its talk narrative.

## Workflow

1. Confirm audience, setting, duration, slide count, source paper, and required output.
2. Define one main claim and an evidence sequence that fits the allotted time.
3. Build a slide outline with action titles, visual intent, and speaker purpose.
4. Use the presentation tooling available in the runtime or repository.
5. Keep methods and results legible; move secondary detail to backup slides.
6. Add rehearsal timing, likely questions, and a backup-slide plan.
7. Render and visually inspect the deck before delivery.

## Bundled Guidance

- `assets/talk-outline-template.md`: planning worksheet.
- `references/talk-structure.md`: narrative structures by talk type.
- `references/slide-design.md`: hierarchy and density rules.
- `references/slide-creation.md`: implementation and QA workflow.
- `references/delivery-and-qa.md`: rehearsal, timing, and Q&A preparation.

## Quality Bar

- Titles should state takeaways rather than topic labels.
- Avoid dense paper paragraphs, tiny figures, and unsupported decorative visuals.
- Never claim a slide or deck was rendered when only an outline was produced.
