---
name: analytics-data-analysis
description: Build reproducible analytics scripts or notebooks for ingestion, cleaning, transformation, statistics, visualization, and delivery.
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

# Rylai Analytics Implementation

Build analysis that another person can rerun and audit.

## Define The Contract

Capture the following before choosing methods:

- decision or question the analysis must support;
- input files, tables, date range, units, and grain;
- metric definitions and inclusion rules;
- expected deliverable: script, notebook, chart set, table, or report;
- runtime limits, privacy constraints, and required output path.

Inspect the real input before assuming its schema.

## Implementation Workflow

1. **Inventory**
   - Record source names, sizes, columns, types, row counts, and keys.
   - Detect encoding, delimiter, duplicate-key, timezone, and locale issues.

2. **Validate**
   - Check missingness, ranges, uniqueness, referential integrity, and impossible values.
   - Separate source defects from intentional filtering.
   - Stop or quarantine records when a defect would invalidate the result.

3. **Transform**
   - Keep raw input unchanged.
   - Make cleaning steps explicit and deterministic.
   - Preserve units and document joins, filters, imputations, and derived fields.

4. **Analyze**
   - Start with counts and distributions.
   - Choose statistical methods that match variable type, sample design, and question.
   - Report effect size or practical magnitude when significance tests are used.
   - Test important assumptions and provide a fallback when they fail.

5. **Visualize**
   - Select a chart based on the comparison, trend, distribution, or relationship.
   - Label units, time windows, filters, and sample sizes.
   - Avoid visual encodings that exaggerate small differences.

6. **Package**
   - Keep configuration and paths separate from analysis logic.
   - Use stable output names and create parent directories deliberately.
   - Include a concise run command and dependency information when code is delivered.

7. **Verify**
   - Run the analysis from a clean start.
   - Reconcile important totals against the source.
   - Inspect generated tables and charts, not only exit codes.

## Code Standards

- Prefer clear functions with explicit inputs and outputs.
- Use structured parsers for structured data.
- Favor vectorized or set-based operations where they improve clarity and scale.
- Never hide data loss inside broad exception handling.
- Add assertions at boundaries where a silent mismatch would corrupt results.
- Use a fixed random seed only when randomness is part of the method, and record it.
- Do not overwrite source files unless the user explicitly requests it.

## Notebook Standards

- Put purpose and assumptions before the first analysis cell.
- Keep setup, loading, validation, transformation, analysis, and conclusions in visible sections.
- Ensure cells run top to bottom without relying on stale state.
- Remove noisy exploratory output while preserving evidence needed to review the result.

## Delivery

Summarize:

- inputs and scope;
- cleaning and exclusion decisions;
- methods and assumptions;
- key outputs;
- validation performed;
- limitations and unresolved data-quality risks.

Never present an estimate as observed fact or infer causation from association alone.

## Runtime Notes

- Use tools and libraries already available in the workspace when practical.
- If a dependency is missing, explain the smallest installation or fallback required.
- Keep paths portable between Codex, Hermes, and Claude by resolving from the workspace or skill directory.
