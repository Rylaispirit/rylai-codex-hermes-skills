---
name: content-research-writer
description: Research, outline, draft, cite, and revise articles, reports, tutorials, newsletters, and case studies with traceable sources and preserved voice.
metadata:
  maintainer: Rylai
  adapted_by: Rylai
  provenance: clean-room-original
  edition: Codex-Hermes-Claude
  edition_version: 1.1.0
  hermes:
    category: content
  claude:
    category: content
---

# Content Research Writer

Build useful prose from a traceable research base. Keep verified facts, source
interpretation, and the writer's own argument clearly separated.

## Runtime Compatibility

- Use the research and file tools available in the active runtime.
- Resolve workspace files from the user's stated project path.
- Confirm network and source access before promising current citations.
- Preserve existing drafts and user edits unless replacement is explicitly requested.

## Establish The Brief

Infer available details, then fill only material gaps:

- topic and central question;
- intended audience;
- purpose and publication format;
- target length and deadline;
- voice or writing samples;
- citation style;
- required, preferred, or excluded sources.

Record uncertain assumptions before research begins.

## Research Workflow

1. **Create research questions**
   - Convert the topic into a short list of claims the piece must establish.
   - Add questions for context, counterarguments, examples, and practical impact.

2. **Choose sources**
   - Prefer primary material for factual and technical claims.
   - Use reputable synthesis for context and competing interpretations.
   - Check publication date, authorship, methodology, and conflicts of interest.

3. **Build a source ledger**

```markdown
| ID | Source | Claim Supported | Evidence | Limits | Status |
|---|---|---|---|---|---|
| S1 | [title and locator] | [claim] | [fact or short note] | [caveat] | verified |
```

Do not put a source in the final reference list unless it was opened and used.

4. **Resolve conflicts**
   - Compare definitions, dates, sample populations, and measurement methods.
   - Report meaningful disagreement instead of selecting a convenient number.

5. **Stop when evidence is sufficient**
   - Each major factual claim has support.
   - Important counterevidence is represented.
   - Additional searching is unlikely to change the structure or conclusion.

## Writing Workflow

1. **Thesis**
   - State the article's central answer in one or two sentences.

2. **Outline**
   - Give every section a job.
   - Link claims to source IDs.
   - Mark evidence gaps before drafting.

3. **Draft**
   - Write from the outline and source ledger.
   - Cite factual claims near the relevant sentence.
   - Use examples to explain, not to substitute for evidence.
   - Keep the user's voice, terminology, and preferred level of formality.

4. **Edit**
   - Check argument order, transitions, redundancy, and paragraph purpose.
   - Replace vague claims with evidence or narrower wording.
   - Remove unsupported authority cues and decorative statistics.

5. **Verify**
   - Open every citation again when accuracy matters.
   - Confirm names, titles, dates, quotations, quantities, and links.
   - Check that the cited source supports the exact nearby claim.

## Collaboration Modes

### Outline First

Return:

- thesis options;
- proposed section order;
- claim-to-source map;
- research gaps;
- questions that require the user's judgment.

### Section Review

Lead with the highest-impact feedback:

- argument or evidence issue;
- structure and flow;
- audience or voice mismatch;
- concrete revision;
- citations still needed.

Do not rewrite the whole section when a focused edit would preserve more of the
writer's voice.

### Full Draft

Deliver the requested article and a short verification note containing:

- citation style used;
- claims still awaiting evidence;
- assumptions or source limitations;
- optional editorial alternatives.

## Citation Rules

- Follow the user's requested citation format.
- Never invent a source, author, title, date, URL, quotation, or page number.
- Prefer direct links or identifiers to vague publication names.
- Quote only when exact wording is necessary; otherwise paraphrase accurately.
- Keep source notes long enough to audit but do not reproduce large passages.
- For current or changing facts, research them at the time of writing.

## Voice Preservation

- Study supplied writing samples before making broad stylistic changes.
- Preserve intentional vocabulary, rhythm, and point of view.
- Distinguish correctness edits from optional stylistic suggestions.
- Avoid flattening personal prose into generic professional language.
- Ask for confirmation only when a voice choice changes meaning or audience fit.

## Final Check

- The thesis answers the stated question.
- Each section advances the piece.
- Important factual claims have traceable support.
- Sources are represented fairly, including limitations and disagreement.
- Citations and reference entries agree.
- The final voice belongs to the user, not to a generic template.
