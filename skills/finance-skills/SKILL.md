---
name: finance-skills
description: "Route finance requests to the capabilities actually available in the current Codex or Hermes runtime and report missing data or tools explicitly."
metadata:
  maintainer: "Rylai"
  adapted_by: "Rylai"
  edition: "Codex-Hermes"
  edition_version: "1.0.0"
  provenance: "clean-room-original"
  hermes:
    category: "finance"
---

> Rylai Codex-Hermes Edition | Original portable workflow by Rylai

## Runtime Compatibility

- Codex: install under `~/.agents/skills/finance-skills` and use `agents/openai.yaml` for UI metadata.
- Hermes: install under `~/.hermes/skills/finance-skills` or expose the bundle through `skills.external_dirs`.
- Resolve bundled files relative to this skill directory; do not depend on paths from another runtime.
- Map capabilities to the current runtime: Codex image generation uses `image_gen`; Hermes uses `image_generate`.
- Verify binaries, packages, credentials, network access, and tool availability before execution.
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
