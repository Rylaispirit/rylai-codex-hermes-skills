---
name: academic-paper-polish
description: Polish academic and research writing for clarity, structure, terminology, argumentation, and cautious claims without inventing evidence or citations.
metadata:
  maintainer: Rylai
  adapted_by: Rylai
  edition: Codex-Hermes-Claude
  edition_version: 1.1.0
  provenance: clean-room-original
  hermes:
    category: academic
  claude:
    category: academic
---

> Rylai Codex-Hermes-Claude Edition | Original portable workflow by Rylai

## Runtime Compatibility

- Codex: install under `~/.agents/skills/academic-paper-polish`.
- Hermes: install under `~/.hermes/skills/academic-paper-polish` or expose the bundle through `skills.external_dirs`.
- Claude Code: install under `~/.claude/skills/academic-paper-polish` or `<project>/.claude/skills/academic-paper-polish`.
- Claude.ai and Cowork: upload and enable the matching per-skill ZIP.
- Resolve bundled files relative to this skill directory; do not depend on paths from another machine.
- Check tools, packages, credentials, network access, and runtime capabilities before execution.

# Academic Paper Polish

Improve an academic draft without changing its scientific meaning.

## Workflow

1. Identify the field, venue, audience, manuscript section, and requested level of editing.
2. Preserve claims, equations, variable names, citations, and technical terminology.
3. Improve argument order, paragraph logic, transitions, concision, and hedging.
4. Flag claims that need evidence instead of inventing sources.
5. Return either tracked suggestions, a revised passage, or both, according to the request.
6. Perform a final consistency check for abbreviations, tense, terminology, figure references, and citation style.

## Bundled References

- `references/section-phrases.md`: section-specific rhetorical patterns.
- `references/vocabulary.md`: precise academic wording and weak-phrase replacements.
- `references/ai-polish.md`: reusable editing prompts and verification passes.

## Boundaries

- Do not fabricate experiments, results, references, reviewer comments, or statistical significance.
- Distinguish language polishing from substantive scientific review.
- Keep author voice when the user supplies a style sample.
