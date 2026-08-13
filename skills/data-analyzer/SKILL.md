---
name: data-analyzer
description: Inspect datasets, calculate trustworthy summaries, identify patterns and anomalies, and explain decision-relevant findings with explicit assumptions.
metadata:
  maintainer: Rylai
  adapted_by: Rylai
  edition: Codex-Hermes-Claude
  edition_version: 1.1.0
  provenance: clean-room-original
  hermes:
    category: data
  claude:
    category: data
---

# Rylai Data Analyzer

Turn supplied data into supported conclusions. Prefer a smaller set of reliable findings over a long list of weak observations.

## Analysis Workflow

1. **Clarify the question**
   - Identify the decision, target metric, comparison, population, and time window.
   - If the user asks broadly, begin with a profile and surface the most consequential patterns.

2. **Inspect the data**
   - Record row count, columns, types, units, date coverage, and likely keys.
   - Check missing values, duplicates, impossible values, inconsistent categories, and parsing failures.
   - Preserve the original data and make exclusions visible.

3. **Create trustworthy summaries**
   - Use counts and rates for categorical data.
   - Use center, spread, range, and quantiles for numeric data.
   - Segment results only where group sizes and definitions remain meaningful.
   - Use robust statistics when outliers make ordinary averages misleading.

4. **Investigate**
   - Compare periods, groups, or cohorts relevant to the question.
   - Examine trend, seasonality, concentration, relationships, and anomalies.
   - Test alternative explanations before calling a pattern important.

5. **Interpret**
   - Separate observed facts from inference.
   - Quantify magnitude and denominator, not only percentage change.
   - State uncertainty, sample limitations, and data-quality risks.
   - Do not claim causation without a design that supports it.

6. **Verify**
   - Recalculate important totals independently.
   - Check that filters, joins, units, and date boundaries match the stated scope.
   - Trace each headline finding back to a reproducible calculation.

## Output Contract

Return a compact report with:

### Scope

Question, data source, period, record count, and filters.

### Data Quality

Missingness, duplicates, exclusions, parsing issues, and material caveats.

### Findings

For each finding, provide the value, comparison, denominator, and why it matters.

### Recommended Actions

Tie actions to evidence and distinguish immediate decisions from further analysis.

### Methods

List calculations, statistical assumptions, and transformations needed to reproduce the result.

Use tables or charts only when they make comparison easier. Never fabricate missing observations or silently replace them with zeros.

## Runtime Notes

- Use the runtime's structured data and spreadsheet tools when available.
- Inspect generated tables and charts before reporting completion.
- Keep temporary analysis artifacts separate from user-facing deliverables.
- State clearly when the dataset is too incomplete to support the requested conclusion.
