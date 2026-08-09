---
name: summarization
description: "Create accurate summaries of documents, articles, meetings, conversations, research, code changes, and multi-source material. Use for TLDRs, executive briefs, key points, action items, technical summaries, research digests, or concise catch-up notes."
metadata:
  maintainer: "Rylai"
  adapted_by: "Rylai"
  provenance: "clean-room-original"
  edition: "Codex-Hermes"
  edition_version: "2.0.0"
  hermes:
    category: "content"
---

# Summarization

Reduce reading time while preserving the source's meaning, evidence, decisions,
uncertainty, and useful detail.

## Runtime Compatibility

- Resolve bundled files relative to this skill directory.
- Use available Codex or Hermes tools to read the actual source material.
- Do not claim full coverage of inaccessible, truncated, or unsupported input.
- Verify extraction quality when the source is a scan, recording, or complex file.

## Intake

Infer these settings from the request and source:

- audience;
- purpose;
- output length;
- required format;
- facts that must survive compression;
- whether attribution to speakers or documents matters.

When the request is underspecified, choose a practical format and state the
compression level in one short line.

## Workflow

1. **Establish source boundaries**
   - Identify every file, message range, URL, transcript, or diff included.
   - Note missing pages, failed extraction, inaudible segments, or truncation.

2. **Build a source map**
   - Record the central claim or purpose.
   - Capture decisions, evidence, dates, quantities, people, risks, and open items.
   - Separate facts, opinions, proposals, and unresolved statements.

3. **Rank information**
   - Keep what the target reader needs to decide, act, understand, or verify.
   - Remove repetition, scene-setting, and low-impact detail unless requested.

4. **Write the summary**
   - Put the bottom line first.
   - Group related points rather than following source order mechanically.
   - Preserve qualifications that change the meaning of a claim.

5. **Audit against the source**
   - Check names, figures, dates, units, ownership, and negation.
   - Confirm that no new conclusion was introduced.
   - Flag contradictions instead of silently resolving them.

## Format Selection

### Executive Brief

Use for reports, proposals, and decision material:

- bottom line;
- strongest evidence;
- risks or uncertainty;
- required decision;
- next actions.

### Technical Summary

Use for specifications, architecture, incidents, and code:

- purpose and scope;
- behavior or design;
- interfaces and dependencies;
- important decisions;
- trade-offs and limitations;
- breaking changes or follow-up work.

### Meeting Or Conversation

Use for notes, chats, and email threads:

- decisions;
- action items with owner and due date when stated;
- key reasoning;
- disagreements;
- unresolved questions.

Do not assign an owner or deadline that was not explicitly agreed.

### Research Diges

Use for papers and analytical material:

- research question;
- method and sample;
- main findings;
- limitations;
- implications.

Keep correlation, causation, statistical confidence, and author interpretation
distinct.

### Multi-Source Synthesis

- Read all available sources before drafting.
- Organize by theme or question.
- Attribute disputed or source-specific claims.
- Surface conflicts in dates, measurements, definitions, or conclusions.
- Avoid presenting repeated claims as independent confirmation.

## Compression Levels

- **Snapshot:** one paragraph or a few bullets.
- **Brief:** bottom line plus essential evidence and actions.
- **Detailed:** structured coverage of all major sections and caveats.

Scale by information density and user need, not page count alone.

## Output Rules

- Do not invent context, intent, consensus, or causality.
- Preserve exact numbers and dates when they affect meaning.
- Use direct quotes only when wording itself matters and the source is available.
- Mark uncertainty with precise language.
- Distinguish source omissions from your own inability to access material.
- Keep recommendations separate from the summary unless the user requests them.

## Optional Templates

Load `summary-templates.md` when a reusable output skeleton will save time. Adap
the template to the source instead of filling empty sections mechanically.

## Final Check

- The opening states the most important conclusion or purpose.
- All critical figures, decisions, and caveats match the source.
- The summary is useful without pretending to replace unavailable evidence.
- The length and terminology fit the intended reader.
