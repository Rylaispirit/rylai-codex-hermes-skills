---
name: video-generation
description: Generate videos through an available or configured video backend using structured prompts, explicit output paths, capability checks, and verified delivery.
metadata:
  maintainer: Rylai
  adapted_by: Rylai
  edition: Codex-Hermes-Claude
  edition_version: 1.1.0
  provenance: clean-room-original
  hermes:
    category: media
  claude:
    category: media
---

> Rylai Codex-Hermes-Claude Edition | Original portable workflow by Rylai

## Runtime Compatibility

- Codex: install under `~/.agents/skills/video-generation`.
- Hermes: install under `~/.hermes/skills/video-generation` or expose the bundle through `skills.external_dirs`.
- Claude Code: install under `~/.claude/skills/video-generation` or `<project>/.claude/skills/video-generation`.
- Claude.ai and Cowork: upload and enable the matching per-skill ZIP.
- Resolve bundled files relative to this skill directory; do not depend on paths from another machine.
- Check tools, packages, credentials, network access, and runtime capabilities before execution.
- Upstream package status: `adapted-core`. The main workflow was rewritten to avoid missing legacy resources; advanced upstream features may remain unavailable.

# Portable Video Generation

Generate a video only through a backend that is available and configured in the current runtime.

## Runtime Routes

- Use a video-generation tool, skill, MCP server, or API configured in the active runtime.
- Do not assume a runtime-specific command exists; verify the provider, credentials, quota, and output controls before submission.

## Workflow

1. Convert the request into a structured prompt containing subject, action, setting, camera, lighting, style, duration, aspect ratio, and audio requirements.
2. Save prompt and job metadata in the active workspace.
3. Confirm provider limits, credentials, quota, and accepted reference-image formats.
4. Submit the generation job and poll its actual status.
5. Download the exact completed asset into the task output directory.
6. Inspect the video or representative frames before delivery.
7. Deliver the file through the current runtime's normal artifact or file mechanism.

## Provider Boundary
