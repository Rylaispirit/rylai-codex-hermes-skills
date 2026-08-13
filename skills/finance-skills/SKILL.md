---
name: finance-skills
description: Route finance requests to capabilities available in the active runtime and report missing market data, tools, credentials, or verification explicitly.
metadata:
  maintainer: Rylai
  adapted_by: Rylai
  edition: Codex-Hermes-Claude
  edition_version: 1.1.0
  provenance: clean-room-original
  hermes:
    category: finance
  claude:
    category: finance
---

> Rylai Codex-Hermes-Claude Edition | Original portable workflow by Rylai

## Runtime Compatibility

- Codex: install under `~/.agents/skills/finance-skills`.
- Hermes: install under `~/.hermes/skills/finance-skills` or expose the bundle through `skills.external_dirs`.
- Claude Code: install under `~/.claude/skills/finance-skills` or `<project>/.claude/skills/finance-skills`.
- Claude.ai and Cowork: upload and enable the matching per-skill ZIP.
- Resolve bundled files relative to this skill directory; do not depend on paths from another machine.
- Check tools, packages, credentials, network access, and runtime capabilities before execution.
- Upstream package status: `adapted-core`. The main workflow was rewritten to avoid missing legacy resources; advanced upstream features may remain unavailable.

# Portable Finance Capability Router

Route a finance request only to capabilities that are actually available.

## Routing

- Market price or index lookup: use the runtime's current finance or web data tool.
- Financial statement analysis: inspect supplied filings or authoritative filing sources.
- Risk or scenario analysis: state assumptions and calculate reproducibly.
- Quantitative analysis: verify Python/R/STATA libraries before promising execution.
- China-market data: verify AkShare or another current source before use.
- News impact: use the portable finance-news analysis workflow.

## Rules

- Report missing data, credentials, libraries, or child skills explicitly.
- Do not imply that the eight child skills named in the legacy source are installed.
- Do not provide personalized buy/sell instructions.
- Keep currency, units, dates, market timezone, and data provenance visible.
