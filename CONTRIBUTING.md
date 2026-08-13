# Contributing

Contributions are welcome when they keep the bundle portable and traceable.

1. Put each skill in `skills/<skill-name>/`.
2. Include `SKILL.md` and `agents/openai.yaml`.
3. Set `metadata.maintainer` to `Rylai` only for this maintained edition.
4. Set provenance to `clean-room-original` or `adapted-open-source`.
5. For an adaptation, include the upstream URL, immutable revision, license,
   and a matching entry in `THIRD_PARTY_NOTICES.md`.
6. Do not include credentials, personal paths, remote placeholder assets,
   proprietary files, or marketplace control instructions.
7. Rebuild the packaged skills whenever a skill changes, and commit the updated
   `packages/` output.
8. Regenerate the release checksum file and commit it. The packaging script
   does both steps in one command:

   ```bash
   python build_claude_packages.py --clean --release-checksums
   ```

9. Run `python verify_bundle.py` before opening a pull request.

Keep changes focused. A skill should contain only instructions and reusable
resources needed to perform its task.

## Supported Hosts

The same `skills/` tree serves three hosts: Codex (`install-codex.ps1`), Hermes
(`install-hermes.sh`), and Claude (`install-claude.sh`, `install-claude.ps1`).
A change must keep working on all three, so avoid host-specific tool names, file
paths, and runtime assumptions inside `SKILL.md`.

`agents/openai.yaml` stays required for Codex-facing interface metadata and
portable bundle validation. Claude ignores it and reads `SKILL.md`.
