---
name: domain-name-brainstormer
description: Generate and rank brandable domain candidates, then perform live RDAP registration checks across selected TLDs before recommending names.
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

# Domain Name Brainstormer

Original portable workflow by Rylai.

Use this workflow to move from a naming brief to a short, checked domain list. Treat registration data as time-sensitive and advisory.

## Workflow

1. Extract the product purpose, audience, tone, language, required words, forbidden words, preferred length, and acceptable TLDs.
2. Generate candidates in several families:
   - direct combinations
   - compact compounds
   - invented pronounceable names
   - action or outcome names
   - local-language or bilingual variants when relevant
3. Remove candidates that are hard to spell, easy to mishear, misleading, or too close to a known competitor.
4. Normalize each candidate to a complete domain before checking it.
5. Run the bundled RDAP checker on the strongest candidates.
6. Rank the results by name quality first and registration signal second.
7. Tell the user to confirm price, premium status, trademark risk, and final availability with their chosen registrar.

## Generate Candidates

Aim for 15 to 30 candidates before filtering. Prefer names that:

- can be spoken once and typed correctly
- avoid hyphens and digits unless the brief requires them
- remain useful if the product expands
- have no accidental negative meaning in the audience's language
- look distinct in lowercase

Do not claim a trademark is clear without a current trademark search.

## Check Domains

Run commands from this skill directory:

```powershell
python scripts/check_domains.py rylailabs.com rylaiworks.dev rylaihub.ai
```

Apply one or more TLDs to bare name stems:

```powershell
python scripts/check_domains.py rylailabs rylaiworks --tld com --tld dev --tld io
```

Write machine-readable results:

```powershell
python scripts/check_domains.py rylailabs.com rylaiworks.dev --json results.json
```

Useful controls:

```text
--timeout SECONDS
--workers COUNT
--json PATH
```

The checker reports:

- `registered`: RDAP returned a current domain record
- `likely_available`: RDAP returned a domain-not-found response
- `unknown`: the registry, network, or rate limit did not provide a reliable answer
- `invalid`: the domain syntax is invalid

Never convert `unknown` into `available`. Even `likely_available` must be confirmed at a registrar immediately before purchase.

## Present Results

Return a compact table with:

1. domain
2. registration signal and check time
3. naming rationale
4. spelling or pronunciation risk
5. final recommendation

Keep unverified price estimates out of the answer. Domain prices and premium classifications change by registrar and date.

## Runtime Notes

- The script uses Python's standard library and HTTPS RDAP requests.
- Network access is required for live checks.
- Codex, Hermes, and Claude should resolve `scripts/check_domains.py` relative to this skill folder.
- If live access is unavailable, provide ideation only and label every availability field `not_checked`.
