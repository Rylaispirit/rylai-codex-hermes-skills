---
name: skill-seekers
description: Convert documentation websites, GitHub repositories, PDFs, and reference sets into portable Agent Skills with source traceability and validation.
metadata:
  maintainer: Rylai
  adapted_by: Rylai
  edition: Codex-Hermes-Claude
  edition_version: 1.1.0
  provenance: adapted-open-source
  upstream:
    url: https://github.com/yusufkaraaslan/Skill_Seekers
    revision: f3972efa33fa79634b96936acf1fac321cdcf7c1
    license: MIT
  hermes:
    category: tooling
  claude:
    category: tooling
---

> Rylai Codex-Hermes-Claude Edition | Maintained and adapted by Rylai

## Runtime Compatibility

- Codex: install under `~/.agents/skills/skill-seekers`.
- Hermes: install under `~/.hermes/skills/skill-seekers` or expose the bundle through `skills.external_dirs`.
- Claude Code: install under `~/.claude/skills/skill-seekers` or `<project>/.claude/skills/skill-seekers`.
- Claude.ai and Cowork: upload and enable the matching per-skill ZIP.
- Resolve bundled files relative to this skill directory; do not depend on paths from another machine.
- Check tools, packages, credentials, network access, and runtime capabilities before execution.

# Source-To-Skill Converter

Turn a documentation site, GitHub repository, PDF, or supplied reference set into a portable Agent Skill.

## Workflow

1. Inspect the exact source and record its URL, revision, file, or document identity.
2. Extract only stable workflows, schemas, commands, and domain rules.
3. Separate concise trigger/procedure instructions into `SKILL.md`.
4. Put detailed source material in `references/`, deterministic helpers in `scripts/`, and reusable templates in `assets/`.
5. Replace source-specific tool names with capability-based instructions for Codex, Hermes, and Claude.
6. Add source traceability and author metadata.
7. Validate the package and forward-test it on realistic prompts.

## Integrity Rules

- Do not copy secrets, credentials, session data, or private identifiers.
- Do not fabricate missing files or claim examples are verified facts.
- Respect source licenses and retain required attribution.
- Mark unavailable integrations and dependencies explicitly.
