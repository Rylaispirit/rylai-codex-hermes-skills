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
7. Run `python verify_bundle.py` before opening a pull request.

Keep changes focused. A skill should contain only instructions and reusable
resources needed to perform its task.
