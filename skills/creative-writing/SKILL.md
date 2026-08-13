---
name: creative-writing
description: Plan, draft, revise, and audit creative or long-form writing with a portable core workflow that does not depend on missing legacy templates.
metadata:
  maintainer: Rylai
  adapted_by: Rylai
  edition: Codex-Hermes-Claude
  edition_version: 1.1.0
  provenance: clean-room-original
  hermes:
    category: content
  claude:
    category: content
---

> Rylai Codex-Hermes-Claude Edition | Original portable workflow by Rylai

## Runtime Compatibility

- Codex: install under `~/.agents/skills/creative-writing`.
- Hermes: install under `~/.hermes/skills/creative-writing` or expose the bundle through `skills.external_dirs`.
- Claude Code: install under `~/.claude/skills/creative-writing` or `<project>/.claude/skills/creative-writing`.
- Claude.ai and Cowork: upload and enable the matching per-skill ZIP.
- Resolve bundled files relative to this skill directory; do not depend on paths from another machine.
- Check tools, packages, credentials, network access, and runtime capabilities before execution.
- Upstream package status: `adapted-core`. The main workflow was rewritten to avoid missing legacy resources; advanced upstream features may remain unavailable.

# Portable Creative Writing

Plan, draft, revise, or audit prose while preserving the user's intended voice and canon.

## Workflow

1. Confirm form, audience, tone, point of view, tense, length, and non-negotiable canon.
2. Inspect existing drafts, outlines, character notes, or style samples before writing.
3. Define the scene or section objective, conflict, change, and ending beat.
4. Draft with concrete sensory detail, varied sentence architecture, and purposeful dialogue.
5. Revise for continuity, pacing, repetition, exposition, voice, and emotional logic.
6. Run a final no-fabrication and canon check.

## Bundled Starting Points

- Genre guides: `references/blog-writing.md`, `references/research-writing.md`, `references/fiction-writing.md`, `references/essay-writing.md`, and `references/marketing-writing.md`.
- Templates: `templates/blog-post.md`, `templates/research-article.md`, `templates/fiction-chapter.md`, `templates/essay.md`, and `templates/landing-page.md`.

## Boundaries

- Do not claim missing templates, checklists, or pipeline commands exist.
- Do not overwrite completed prose unless the user requests a rewrite.
- Keep facts, names, chronology, and established world rules stable.
