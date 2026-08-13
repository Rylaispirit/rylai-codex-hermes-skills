---
name: academic-pptx
description: Plan, build, render, and verify academic presentation decks with citations, accessible visuals, clear argument flow, speaker-ready pacing, and visual QA.
metadata:
  maintainer: Rylai
  adapted_by: Rylai
  edition: Codex-Hermes-Claude
  edition_version: 1.1.0
  provenance: clean-room-original
  hermes:
    category: presentations
  claude:
    category: presentations
---

# Academic PPTX

This clean-room workflow is maintained and adapted by Rylai for Codex, Hermes, and Claude. It covers the reasoning, production, rendering, and verification needed
for an academic deck. It does not depend on a private template or closed helper.

Read these resources when needed:

- [content_guidelines.md](content_guidelines.md) for argument, evidence, timing,
  citations, and speaker-note decisions.
- [slide_patterns.md](slide_patterns.md) for reusable academic slide structures.

## Runtime Contract

- Respect the user's institution template, existing deck, and repository.
- Use standard presentation tooling available in the environment, such as
  PptxGenJS, python-pptx, LibreOffice, PowerPoint automation, or a runtime
  presentation tool.
- Check fonts, packages, rendering tools, image support, and file access before
  committing to an implementation path.
- Keep source documents unchanged unless the user asks to edit them.
- Resolve paths from the active project or this skill directory.
- Never fabricate research results, citations, quotations, or missing values.

## Expected Deliverables

Unless the request is planning-only, produce:

- an editable `.pptx`;
- the slide outline or build source used to create it;
- rendered slide previews or a PDF for visual inspection when tooling permits;
- a concise verification report covering content, layout, and file integrity.

## Workflow

### 1. Inventory the Evidence

Read the supplied paper, manuscript, notes, figures, tables, data, branding, and
existing slides. Build an evidence ledger with:

- claim or message;
- supporting source;
- figure, table, quotation, or calculation available;
- citation details;
- confidence or unresolved gap;
- permission or provenance notes for external media.

Mark missing information explicitly. Do not fill gaps with plausible-sounding
content.

### 2. Set the Talk Contract

Determine:

- audience knowledge and likely questions;
- presentation type;
- allotted talk time and question time;
- required sections or institutional rules;
- one sentence the audience should remember;
- one action or judgment the closing should support.

Use reasonable defaults when the user has not specified them, and record those
defaults in the working outline.

### 3. Allocate Time and Slides

Reserve time for orientation, evidence, synthesis, and a deliberate close.
Estimate slide count from content complexity and speaking time, not from a fixed
ratio. Dense equations, methods diagrams, and result interpretation need more
time than title or transition slides.

Move secondary analyses, derivations, extended literature comparisons, and
anticipated challenge questions to an appendix.

### 4. Build the Argument Outline

Create a slide-by-slide plan containing:

- slide number;
- message title written as a conclusion or question;
- purpose in the argument;
- evidence or visual;
- citation;
- expected speaking time;
- notes or transition.

Read only the message titles in order. They should form a defensible chain from
problem to evidence to conclusion. Repair missing logic before creating slides.

### 5. Choose a Production Path

Prefer the project's existing presentation stack. Otherwise select a standard
tool according to the task:

- **PptxGenJS:** strong for programmatic layouts, charts, and reusable helpers.
- **python-pptx:** suitable for deterministic text, shapes, tables, and image
  placement.
- **LibreOffice or PowerPoint automation:** useful for conversion, rendering,
  and final compatibility checks.
- **Existing template editing:** appropriate when the institution supplies a
  required master deck.

Do not introduce a new dependency when the installed stack can complete the
work. Keep generated source deterministic so a later revision can be rebuilt.

### 6. Define the Slide System

Before building all slides, define:

- slide size, normally 16:9 unless a template specifies otherwise;
- safe margins and a stable content grid;
- title, body, caption, citation, and numeric text roles;
- a restrained color system with accessible contrast;
- chart colors that remain distinguishable without color alone;
- placement rules for slide numbers, sources, and affiliation;
- image cropping and attribution behavior.

Build one representative content slide and render it early. Correct the system
before multiplying layout problems across the deck.

### 7. Build the Deck

Use master layouts or reusable functions for repeated structures. Keep each
slide focused on one audience decision:

- what to notice;
- how the evidence supports it;
- what qualification is necessary;
- how it connects to the next slide.

Prefer direct labels and annotations over legends that require eye travel.
Preserve uncertainty, units, sample sizes, and baseline definitions. Put sources
on the slide where borrowed evidence appears.

Use speaker notes for delivery cues, transitions, caveats, and detail that
should not crowd the projected slide.

### 8. Render and Inspect

Open or render the generated file using an independent presentation engine when
available. Inspect every slide as an image or in slide-sorter view.

Check:

- missing fonts, images, symbols, equations, or glyphs;
- clipped text and objects outside the canvas;
- accidental overlaps and inconsistent alignment;
- titles that wrap into content;
- tiny axes, labels, citations, and footnotes;
- stretched or poorly cropped images;
- chart values and table cells against the source;
- visual continuity between adjacent slides.

Repeat the render after corrections. A successful file write is not visual
proof.

### 9. Rehearsal Pass

Review the deck in speaking order:

- opening reaches the research question quickly;
- terminology is introduced before use;
- each result receives interpretation;
- transitions explain why the next slide follows;
- limitations match the actual evidence;
- the conclusion answers the opening problem;
- main-deck timing fits without rushing;
- appendix slides cover foreseeable technical questions.

When rehearsal exceeds the limit, remove or relocate content instead of reducing
legibility.

### 10. Structural Validation

Run the checks available for the chosen stack:

- open the PPTX as a ZIP package and confirm required parts exist;
- reopen it with a presentation library or application;
- confirm slide count and expected media;
- scan source text for placeholders and unresolved TODO markers;
- verify links and citations where possible;
- confirm the output path and final filenames;
- report any check that could not be performed.

## Presentation Modes

### Conference or Seminar

Move rapidly from motivation to the central question. Spend most time on the
strongest evidence and its interpretation. Keep literature context selective.

### Thesis Defense

Make the research program visible: problem, contributions, chapter or study
relationship, evidence, limitations, and future work. Prepare appendix answers
for methods, robustness, and committee-specific concerns.

### Grant or Review Panel

Connect significance, proposed work, feasibility, evaluation, risk controls,
milestones, and requested support. Distinguish completed evidence from planned
work.

### Teaching or Invited Lecture

Sequence concepts by prerequisite. Include examples, pauses for synthesis, and
recap slides. Avoid assuming that a research-paper structure is also a teaching
structure.

## Completion Gate

Do not report completion until:

- all claims trace to supplied or verified sources;
- the argument works when reading message titles alone;
- the deck opens in at least one presentation engine;
- every slide has been rendered or visually inspected;
- no clipping, overlap, placeholder text, or unreadable citation remains;
- charts, tables, equations, and images match their sources;
- pacing is plausible for the allotted time;
- the editable source and final PPTX are both present;
- limitations in tooling or verification are stated clearly.
