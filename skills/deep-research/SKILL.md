---
name: deep-research
description: "Conduct systematic source-backed research with scoped questions, triangulation, contradiction handling, and citation-ready synthesis."
metadata:
  maintainer: "Rylai"
  adapted_by: "Rylai"
  edition: "Codex-Hermes"
  edition_version: "1.0.0"
  provenance: "clean-room-original"
  hermes:
    category: "research"
---

> Rylai Codex-Hermes Edition | Original portable workflow by Rylai

## Runtime Compatibility

- Codex: install under `~/.agents/skills/deep-research` and use `agents/openai.yaml` for UI metadata.
- Hermes: install under `~/.hermes/skills/deep-research` or expose the bundle through `skills.external_dirs`.
- Resolve bundled files relative to this skill directory; do not depend on paths from another runtime.
- Map capabilities to the current runtime: Codex image generation uses `image_gen`; Hermes uses `image_generate`.
- Verify binaries, packages, credentials, network access, and tool availability before execution.

# Portable Deep Research

Produce a source-backed answer to a question that genuinely needs multi-source research.

## Workflow

1. Define the research question, scope, date boundary, audience, and decision the report should support.
2. Break the question into independent sub-questions and identify preferred primary sources.
3. Search broadly, then open and inspect the most relevant sources.
4. Use parallel research agents only when the runtime exposes delegation and the subtasks are independent.
5. Build an evidence table containing claim, source, date, confidence, and contradiction notes.
6. Triangulate important claims and explain disagreements instead of silently selecting one source.
7. Synthesize the answer with citations attached to the claims they support.
8. State unresolved gaps, stale evidence, and inference separately from verified fact.

## Boundaries

- Ask a clarification question only when ambiguity materially changes the research result.
- Never invent a citation, quote, URL, statistic, publication date, or source conclusion.
- For current topics, verify freshness at execution time.
