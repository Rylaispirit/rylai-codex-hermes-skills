---
name: video-generation
description: "Generate videos through the native or configured video backend in Codex or Hermes using structured prompts, explicit output paths, and verified delivery."
metadata:
  maintainer: "Rylai"
  adapted_by: "Rylai"
  edition: "Codex-Hermes"
  edition_version: "1.0.0"
  provenance: "clean-room-original"
  hermes:
    category: "media"
---

> Rylai Codex-Hermes Edition | Original portable workflow by Rylai

## Runtime Compatibility

- Codex: install under `~/.agents/skills/video-generation` and use `agents/openai.yaml` for UI metadata.
- Hermes: install under `~/.hermes/skills/video-generation` or expose the bundle through `skills.external_dirs`.
- Resolve bundled files relative to this skill directory; do not depend on paths from another runtime.
- Map capabilities to the current runtime: Codex image generation uses `image_gen`; Hermes uses `image_generate`.
- Verify binaries, packages, credentials, network access, and tool availability before execution.
- Upstream package status: `adapted-core`. The main workflow was rewritten to avoid missing legacy resources; advanced upstream features may remain unavailable.

# Portable Video Generation

Generate a video only through a backend that is available and configured in the current runtime.

## Runtime Routes

- Codex: use the installed Sora skill or an explicitly configured video provider.
- Hermes: use `video_generate` when the video toolset and provider are enabled.

## Workflow

1. Convert the request into a structured prompt containing subject, action, setting, camera, lighting, style, duration, aspect ratio, and audio requirements.
2. Save prompt and job metadata in the active workspace.
3. Confirm provider limits, credentials, quota, and accepted reference-image formats.
4. Submit the generation job and poll its actual status.
5. Download the exact completed asset into the task output directory.
6. Inspect the video or representative frames before delivery.
7. Deliver the file through the current runtime's normal artifact or file mechanism.

## Provider Boundary
