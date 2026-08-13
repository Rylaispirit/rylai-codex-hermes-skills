---
name: frontend-design
description: Design, implement, and verify production frontend interfaces while respecting the existing repository, accessibility, responsive behavior, interaction, and visual QA.
metadata:
  maintainer: Rylai
  adapted_by: Rylai
  edition: Codex-Hermes-Claude
  edition_version: 1.1.0
  provenance: clean-room-original
  hermes:
    category: design
  claude:
    category: design
---

# Frontend Design

This skill is a practical build workflow maintained and adapted by Rylai for
Codex, Hermes, and Claude. Its goal is a usable, coherent interface that survives real
content, real interaction, and real viewport changes.

## Runtime Contract

- Work inside the user's existing repository when one is provided.
- Follow higher-priority project instructions and established design tokens.
- Reuse the installed framework, component library, and icon set when suitable.
- Resolve files relative to this skill or the active project, never a private
  path from another machine.
- Check tool and package availability before relying on them.
- Use the runtime's browser, screenshot, and image-generation capabilities by
  their local names.

## Required Outcome

A finished interface must:

- perform the requested workflow rather than merely illustrate it;
- preserve or deliberately extend the product's visual language;
- support keyboard, pointer, touch, zoom, and reduced-motion use;
- remain readable from narrow mobile screens through wide desktop screens;
- expose loading, empty, error, disabled, success, and destructive states when
  the workflow can reach them;
- avoid layout shifts caused by labels, icons, validation text, or late data;
- be verified in a real browser before completion is reported.

## Workflow

### 1. Inspect Before Designing

Read the relevant routes, components, styles, assets, package manifest, and
tests. Identify:

- the user and their main task;
- the current navigation and information hierarchy;
- reusable components and tokens;
- framework and build constraints;
- nearby screens that establish product conventions;
- existing user changes that must remain intact.

For a reference image or existing page, separate structural facts from
decorative details. Record the important relationships: hierarchy, alignment,
density, rhythm, image treatment, interaction priority, and responsive intent.

### 2. Define the Experience

Write a short internal brief before editing:

- **Primary task:** what the user must accomplish.
- **Priority content:** what must be visible first.
- **Interaction path:** the shortest reliable path through the task.
- **Visual character:** a few concrete qualities tied to the domain.
- **Constraints:** framework, data, accessibility, performance, and deadlines.
- **Proof:** which interactions and viewports will demonstrate completion.

Do not add a marketing introduction when the request is for a working tool.
Start with the actual product surface.

### 3. Plan the Screen Structure

Choose the smallest structure that supports the workflow:

- persistent navigation only when users need repeated movement;
- toolbars for frequent commands;
- tabs for peer views;
- menus for compact option sets;
- dialogs for focused, reversible interruption;
- cards only for genuinely repeated, self-contained items;
- tables or aligned lists when comparison matters.

Map each important action to a visible control. Prefer familiar icons for
common tool actions and provide an accessible name or tooltip when the meaning
is not obvious.

### 4. Establish the Visual System

Derive a small set of reusable decisions:

- typography roles for display, section, body, label, and data text;
- spacing steps and content width;
- surface, border, text, accent, success, warning, and danger colors;
- corner radius and elevation rules;
- stable sizes for controls, rows, panels, and fixed-format content;
- focus, hover, pressed, selected, and disabled treatments.

Use color to express hierarchy and state. Do not let one hue dominate every
surface. Choose imagery and illustration that reveal the actual product,
subject, or task rather than acting as unrelated atmosphere.

### 5. Implement the Core Path

Build the semantic structure first, then styling, then motion. Keep state close
to the component that owns it unless the repository has an established state
pattern. Prefer existing helpers and native platform behavior over new
abstractions.

The primary path must be functional. Connect real data when the project
provides it; otherwise use explicit local fixtures that can be replaced without
rewriting the component.

### 6. Complete Interaction States

For every interactive control, verify:

- pointer and keyboard activation;
- visible focus;
- disabled behavior;
- progress feedback for delayed actions;
- validation near the field or action that caused it;
- recovery guidance for failures;
- confirmation for destructive or irreversible actions;
- stable geometry while labels and messages change.

Do not leave controls that look clickable but perform no action.

### 7. Make Responsiveness Intentional

Design responsive behavior from content pressure, not device labels.

- Let grids reduce columns before content becomes cramped.
- Allow toolbars to wrap, collapse, or move secondary actions into a menu.
- Preserve the primary action and essential context on small screens.
- Give tables an explicit narrow-screen strategy: horizontal scroll, selected
  columns, stacked records, or a detail view.
- Use `minmax()`, `clamp()` for dimensions, `aspect-ratio`, and bounded
  containers where they prevent layout drift.
- Wrap long labels and test unusually long values.

Check at least one narrow mobile width, one tablet-like width, and one desktop
width. Add a wide-screen check for dense dashboards or full-bleed media.

### 8. Apply Accessibility

Use semantic HTML before ARIA. Confirm:

- one clear page heading and logical heading order;
- labels for inputs and accessible names for icon controls;
- keyboard traversal that follows the visible reading order;
- focus that is never hidden by overlays or sticky regions;
- sufficient text and control contrast;
- status messages announced when needed;
- dialogs that manage focus and close predictably;
- meaningful alternative text for informative images;
- decorative images excluded from assistive output;
- no information conveyed by color alone;
- motion reduced when the user requests it;
- content remains usable at browser zoom.

Use automated checks as a supplement to keyboard and visual inspection.

### 9. Control Performance

- Avoid shipping large media when a smaller representation is enough.
- Reserve dimensions for images and asynchronous content.
- Lazy-load below-the-fold media when appropriate.
- Keep animation on opacity and transforms when possible.
- Avoid unnecessary rerenders and broad dependency additions.
- Respect the project's established bundling and data-fetching strategy.

### 10. Verify in a Browser

Run the project's normal checks, start the appropriate local server, and inspect
the interface in a real browser.

Verification should cover:

1. initial render and console output;
2. the full primary interaction path;
3. loading, empty, error, and success states;
4. keyboard navigation and visible focus;
5. narrow, medium, desktop, and relevant wide viewports;
6. long content, validation messages, and overflow;
7. screenshots for visual comparison and overlap detection;
8. production build or equivalent repository check.

When a visual reference exists, compare screenshots against it and correct
hierarchy, spacing, scale, cropping, and alignment. Do not claim fidelity from
code inspection alone.

## Domain Modes

### Operational Products

Favor scanability, predictable navigation, compact controls, clear status, and
fast repeated action. Dashboards, CRMs, editors, and admin tools should spend
space on useful information rather than decorative introductions.

### Content and Editorial Experiences

Prioritize reading rhythm, meaningful imagery, clear sequencing, and restrained
navigation. Preserve enough visible continuation that users understand there is
more content below the first viewport.

### Brand and Product Pages

Make the brand, product, place, or person unmistakable in the first viewport.
Use real or generated bitmap media that shows the subject clearly. Supporting
copy explains value; the main heading names the offer or subject.

### Games and Creative Tools

Allow stronger motion and illustration, but keep controls learnable and state
legible. Use a proven engine for established game rules, physics, parsing, or
3D behavior when the project permits it.

## Completion Gate

Before finishing, confirm:

- the requested workflow works end to end;
- no unrelated files were changed;
- no visible element overlaps or clips at tested widths;
- text fits controls and containers with realistic long content;
- controls have complete states and accessible names;
- keyboard and reduced-motion behavior are usable;
- the browser console has no new actionable errors;
- tests and the production build pass, or limitations are reported precisely;
- screenshots represent the final implementation, not an earlier draft.
