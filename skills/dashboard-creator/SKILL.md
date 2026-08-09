---
name: dashboard-creator
description: "Design, build, and verify practical dashboards for KPIs, trends, comparisons, status monitoring, and operational decisions. Use for HTML dashboards, application dashboard views, metric panels, chart collections, filters, and responsive data interfaces."
metadata:
  maintainer: "Rylai"
  adapted_by: "Rylai"
  edition: "Codex-Hermes"
  edition_version: "2.0.0"
  provenance: "clean-room-original"
  hermes:
    category: "data"
---

# Rylai Dashboard Creator

Build the working dashboard as the primary experience. Optimize for scanning, comparison, and repeated use.

## Establish The Metric Contrac

For each metric, determine:

- exact definition and unit;
- source and refresh time;
- aggregation level and time window;
- comparison baseline;
- whether higher or lower is desirable;
- states for missing, delayed, partial, and invalid data.

Do not invent values to make a screen look complete. Clearly label sample data when a prototype requires it.

## Build Workflow

1. **Inspect the target**
   - Reuse the repository's framework, components, tokens, and data-access patterns.
   - For a standalone deliverable, choose the smallest format that supports the required interaction.

2. **Create the information hierarchy**
   - Put global filters and freshness near the top.
   - Show a small set of decision-critical KPIs first.
   - Follow with trends, comparisons, breakdowns, and detailed records.
   - Keep related controls beside the view they affect.

3. **Choose visual forms**
   - Line: change over ordered time.
   - Bar: comparison across categories.
   - Scatter: relationship or outliers.
   - Distribution: spread and concentration.
   - Table: exact values, dense comparison, or operational action.
   - Progress: bounded completion against a known target.

4. **Implement states**
   - Loading, empty, error, stale, and permission-limited states must preserve layout.
   - Filters must have visible active values and a clear reset path.
   - Tooltips must add detail, not carry essential meaning.

5. **Verify**
   - Test realistic long labels, zero values, negative values, and missing values.
   - Check desktop and mobile widths.
   - Confirm keyboard access, focus visibility, contrast, and non-color status cues.
   - Validate calculations against the source data.
   - Inspect the rendered dashboard for clipping, overlap, and layout shift.

## Presentation Rules

- Use restrained surfaces and compact spacing appropriate to operational software.
- Keep cards for individual metrics or repeated records; do not wrap every section in a card.
- Use consistent scales across charts that users will compare.
- Start numeric axes at zero for bars unless a different baseline is explicitly justified.
- Show units in labels or values, not only in explanatory text.
- Avoid decorative graphics that compete with the data.
- Keep table headers visible and align numbers for comparison.

## Delivery

Provide:

- the runnable dashboard or edited application;
- the data assumptions and metric definitions;
- the preview path or local URL;
- the viewport and interaction checks performed;
- any unavailable live data or unresolved integration requirement.

## Runtime Notes

- Resolve files from the active workspace and keep generated assets local.
- Use installed icon and chart libraries when the existing project already depends on them.
- For a standalone dashboard, avoid unnecessary network dependencies.
- Preserve compatibility with both Codex and Hermes by checking available tools before invoking runtime-specific features.
