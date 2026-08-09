---
name: finance-news-analysis
description: "Analyze current financial news for sentiment, market or sector impact, affected instruments, uncertainty, and risk scenarios without giving trade advice."
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

- Codex: install under `~/.agents/skills/finance-news-analysis` and use `agents/openai.yaml` for UI metadata.
- Hermes: install under `~/.hermes/skills/finance-news-analysis` or expose the bundle through `skills.external_dirs`.
- Resolve bundled files relative to this skill directory; do not depend on paths from another runtime.
- Map capabilities to the current runtime: Codex image generation uses `image_gen`; Hermes uses `image_generate`.
- Verify binaries, packages, credentials, network access, and tool availability before execution.
- Upstream package status: `adapted-core`. The main workflow was rewritten to avoid missing legacy resources; advanced upstream features may remain unavailable.

# Portable Finance News Analysis

Analyze current financial news without presenting personalized investment advice.

## Workflow

1. Collect the exact article, event, issuer, market, and publication time.
2. Verify the event through current authoritative or primary sources.
3. Separate reported facts from commentary, forecasts, and market rumor.
4. Classify direction as positive, negative, mixed, or uncertain.
5. Map possible effects across market, sector, company, rates, currencies, or commodities.
6. Identify affected instruments only when the relationship is evidence-backed.
7. Present base, upside, and downside scenarios with explicit uncertainty.

## Outpu

- Event summary
- Source and timing
- Sentiment and confidence
- Transmission mechanism
- Potentially affected sectors or instruments
- Counterarguments and risks
- What evidence would change the conclusion
