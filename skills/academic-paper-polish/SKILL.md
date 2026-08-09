---
name: academic-paper-polish
description: "Polish academic and research writing for clarity, structure, terminology, argumentation, and cautious claims without inventing evidence or citations."
metadata:
  maintainer: "Rylai"
  adapted_by: "Rylai"
  edition: "Codex-Hermes"
  edition_version: "1.0.0"
  provenance: "clean-room-original"
  hermes:
    category: "academic"
---

> Rylai Codex-Hermes Edition | Original portable workflow by Rylai

## Runtime Compatibility

- Codex: install under `~/.agents/skills/academic-paper-polish` and use `agents/openai.yaml` for UI metadata.
- Hermes: install under `~/.hermes/skills/academic-paper-polish` or expose the bundle through `skills.external_dirs`.
- Resolve bundled files relative to this skill directory; do not depend on paths from another runtime.
- Map capabilities to the current runtime: Codex image generation uses `image_gen`; Hermes uses `image_generate`.
- Verify binaries, packages, credentials, network access, and tool availability before execution.

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
