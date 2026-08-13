# Model-Neutral Academic Editing Prompts

> Portable Codex-Hermes-Claude replacement authored by Rylai.

## Full Pass

```text
Edit the passage for academic clarity and precision.

Constraints:
- Preserve scientific meaning, citations, numbers, equations, and terminology.
- Do not invent evidence, references, results, or stronger claims.
- Remove redundancy and vague wording.
- Keep the author's preferred voice and field conventions.

Return:
1. Revised passage.
2. A short list of substantive wording changes.
3. Any claim that needs evidence or clarification.
```

## Concision Pass

```text
Reduce the passage by approximately [target percent] without removing evidence,
qualifications, definitions, or logical transitions. List any content that could
not be removed safely.
```

## Coherence Pass

```text
Check whether each sentence has one clear role and whether paragraph order
supports the argument. Propose the smallest reordering needed. Do not rewrite
technical content unless clarity requires it.
```

## Claim Calibration Pass

```text
Mark claims as descriptive, correlational, causal, comparative, or speculative.
Revise wording so claim strength matches the supplied evidence. Do not add
citations or results.
```

## Verification

After editing, compare source and revision for:

- unchanged numbers and units
- unchanged citations and labels
- unchanged negation and direction of effects
- preserved limitations and uncertainty
- consistent abbreviations and technical terms
