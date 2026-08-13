---
name: seo
description: Perform an evidence-led SEO audit using accessible pages, source code, crawl data, and current search documentation without assuming missing plugins.
metadata:
  maintainer: Rylai
  adapted_by: Rylai
  edition: Codex-Hermes-Claude
  edition_version: 1.1.0
  provenance: adapted-open-source
  upstream:
    url: https://github.com/AgriciDaniel/claude-seo
    revision: 09d37c7b66ed3ca9c6efbdb765a805a6c76a8f01
    license: MIT
  hermes:
    category: research
  claude:
    category: research
---

> Rylai Codex-Hermes-Claude Edition | Maintained and adapted by Rylai

## Runtime Compatibility

- Codex: install under `~/.agents/skills/seo`.
- Hermes: install under `~/.hermes/skills/seo` or expose the bundle through `skills.external_dirs`.
- Claude Code: install under `~/.claude/skills/seo` or `<project>/.claude/skills/seo`.
- Claude.ai and Cowork: upload and enable the matching per-skill ZIP.
- Resolve bundled files relative to this skill directory; do not depend on paths from another machine.
- Check tools, packages, credentials, network access, and runtime capabilities before execution.
- Upstream package status: `adapted-core`. The main workflow was rewritten to avoid missing legacy resources; advanced upstream features may remain unavailable.

# Portable SEO Audi

Audit the exact website or page using evidence available to the current runtime.

## Workflow

1. Confirm the target URL, market, language, business type, and audit scope.
2. Fetch or browse the live page and inspect rendered content, HTML, metadata, links, and indexability signals.
3. Review technical basics: status codes, canonicals, robots directives, sitemap exposure, headings, structured data, mobile behavior, and performance evidence.
4. Review search intent, page usefulness, internal linking, duplication, and content gaps.
5. Separate observed defects from recommendations that need Search Console, analytics, backlink, or crawl data.
6. Prioritize findings by impact, confidence, effort, and affected routes.
7. Re-check current search-engine documentation before asserting time-sensitive rules.

## Boundaries

- Do not claim a full crawl, Search Console result, Core Web Vitals measurement, or backlink audit without the relevant data.
- Do not invent rankings, traffic, index status, or competitor metrics.
- Prefer narrow implementation fixes tied to evidence.
