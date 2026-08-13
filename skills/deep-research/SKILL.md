---
name: deep-research
description: Conduct systematic source-backed research with scoped questions, triangulation, contradiction handling, and citation-ready synthesis.
metadata:
  maintainer: Rylai
  adapted_by: Rylai
  edition: Codex-Hermes-Claude
  edition_version: 1.1.0
  provenance: clean-room-original
  hermes:
    category: research
  claude:
    category: research
---

> Rylai Codex-Hermes-Claude Edition | Original portable workflow by Rylai

## Runtime Compatibility

- Codex: install under `~/.agents/skills/deep-research`.
- Hermes: install under `~/.hermes/skills/deep-research` or expose the bundle through `skills.external_dirs`.
- Claude Code: install under `~/.claude/skills/deep-research` or `<project>/.claude/skills/deep-research`.
- Claude.ai and Cowork: upload and enable the matching per-skill ZIP.
- Resolve bundled files relative to this skill directory; do not depend on paths from another machine.
- Check tools, packages, credentials, network access, and runtime capabilities before execution.

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
