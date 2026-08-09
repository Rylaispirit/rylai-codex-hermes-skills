# Academic Slide Creation

> Portable Codex-Hermes replacement authored by Rylai.

## Build Sequence

1. Confirm aspect ratio and institutional template requirements.
2. Create the outline and run the ghost-deck test.
3. Define type, spacing, color, citation, and chart rules.
4. Build slides with the installed presentation skill or repository toolchain.
5. Add real figures, tables, equations, and citations.
6. Render every slide to images.
7. Inspect at presentation size and fix clipping, density, alignment, and contrast.

## Technical Handoff

When using the bundled `pptx` skill, prefer its existing `python-pptx` recipes
and editing guide. Reuse repository helpers before adding a new dependency.

## Data Visuals

- Keep source data and generation code with the deck.
- Use consistent scales across comparisons.
- Highlight only the evidence discussed by the title.
- Do not trace or redraw a figure in a way that changes its meaning.

## Delivery Gate

Do not report a finished deck until the PPTX opens, slide count matches the
outline, all assets resolve, and rendered slide images pass visual review.
