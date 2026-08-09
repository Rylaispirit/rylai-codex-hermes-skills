---
name: content-analysis
description: "Analyze articles, documents, videos, podcasts, transcripts, and mixed media for arguments, evidence, themes, assumptions, contradictions, practical lessons, and unanswered questions. Use when the user wants more than a summary or asks for insights, critique, takeaways, or source-grounded analysis."
metadata:
  maintainer: "Rylai"
  adapted_by: "Rylai"
  provenance: "clean-room-original"
  edition: "Codex-Hermes"
  edition_version: "2.0.0"
  hermes:
    category: "content"
---

# Content Analysis

Turn source material into a structured explanation of what it says, how i
supports its claims, what follows from it, and where uncertainty remains.

## Runtime Compatibility

- Resolve local files from the current workspace or this skill directory.
- Use available Codex or Hermes tools to fetch, transcribe, or inspect the source.
- Verify that extraction or transcription is usable before analyzing details.
- If access is incomplete, describe the exact boundary of the analysis.

## Select The Analysis Lens

Choose only the lenses that serve the request:

- **Argument:** claims, reasons, evidence, and conclusion.
- **Editorial:** structure, clarity, pacing, framing, and audience fit.
- **Research:** method, evidence quality, limits, and competing explanations.
- **Practical:** decisions, habits, procedures, and applications.
- **Comparative:** agreement, conflict, and differences in assumptions.
- **Media:** speaker roles, sequence, emphasis, and transcript reliability.

## Workflow

1. **Identify the source**
   - Record title, creator, date, format, and available sections when known.
   - Distinguish original material from commentary, reposts, and excerpts.

2. **Check completeness**
   - For video or audio, confirm transcript coverage and speaker labels.
   - For documents, check page or section coverage.
   - For web material, note paywalls, dynamic content, or missing attachments.

3. **Map the content**
   - State the central question or purpose.
   - Break the material into major claims, themes, or stages.
   - Attach supporting evidence to the claim it is meant to support.

4. **Evaluate**
   - Test whether evidence actually supports the conclusion.
   - Identify assumptions, omitted alternatives, contradictions, and ambiguity.
   - Separate source statements from your own inference.

5. **Extract value**
   - Rank the strongest insights.
   - Convert applicable ideas into concrete actions or questions.
   - Preserve important limits and conditions.

6. **Verify the report**
   - Check quotes against the source.
   - Check names, numbers, dates, and attribution.
   - Remove observations that cannot be traced to the material.

## Default Outpu

```markdown
## Overview
[Purpose and central message]

## Main Ideas
1. [Claim or theme]
2. [Claim or theme]

## Evidence And Reasoning
- [Claim]: [support and evaluation]

## Strongest Insights
- [Source-grounded insight]

## Assumptions Or Gaps
- [Missing evidence, ambiguity, or alternative explanation]

## Practical Use
- [Action, decision, or question]

## Source Limits
- [Access, extraction, transcription, or scope limitation]


Change this structure when the user asks for a critique, comparison, timeline,
study guide, action plan, or another specific deliverable.

## Source Integrity

- Quote only words present in the inspected source.
- Keep quotations short and attribute them when the speaker is known.
- Do not invent transcript segments, timestamps, facts, or recommendations.
- Label deductions as analysis rather than source claims.
- Treat promotional claims and personal anecdotes as evidence of limited type.
- For multiple sources, identify which source supports each disputed point.
- When a source cannot be opened, request the text or transcript instead of
  presenting a complete analysis.

## Final Check

- The report answers the user's actual analytical question.
- Summary, evidence, inference, and opinion remain distinguishable.
- Every quoted or quantitative detail is traceable.
- Important counterevidence and limitations are visible.
- Action items follow from the analysis rather than generic advice.
