# Rylai Codex-Hermes Skills

A personal collection of portable Agent Skills curated, adapted, and maintained
by **Rylai** for Codex and Hermes.

The bundle contains 35 independent skills for writing, research, data, documents,
presentations, design, media, finance, deployment, and skill creation. The skills
can be installed together or copied individually.

## Ownership And Sources

- Rylai authors the bundle structure, installers, validators, Vietnamese guide,
  clean-room replacements, compatibility notes, and original helper scripts.
- Skills adapted from public GitHub projects retain their upstream repository,
  revision, author, and license information.
- An upstream credit means the corresponding author owns their original work.
  Rylai is the maintainer and adapter of this Codex-Hermes edition.
- No private workstation paths, credentials, proprietary vendor schemas, remote
  placeholder images, or marketplace control skills are included.

See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) and
[PROVENANCE.yml](PROVENANCE.yml) for the release provenance.

## Vietnamese Guide

See [GIAI_THICH_SKILLS_VI.md](GIAI_THICH_SKILLS_VI.md) for a Vietnamese
description of every skill, including its purpose, expected inputs and outputs,
runtime requirements, and example requests.

## Installation

### Codex

```powershell
.\install-codex.ps1
```

Use `-Force` to replace existing skills. Existing folders are backed up first.

### Hermes

```bash
bash install-hermes.sh
```

Use `--force` to replace existing skills. Existing folders are backed up first.

### Install One Skill

Copy one directory from `skills/` into the skill directory used by your agent:

```text
Codex:  ~/.agents/skills/<skill-name>
Hermes: ~/.hermes/skills/<skill-name>
```

## Status Meanings

- `ready`: instruction workflow is usable without a special proprietary runtime.
- `conditional`: requires an optional package, binary, login, API, or renderer.
- `adapted-core`: the portable core is available; advanced integrations may be
  intentionally omitted.

Runtime requirements are described in each `SKILL.md` and in `manifest.json`.

## Verification

```bash
python -m pip install -r requirements-verify.txt
python verify_bundle.py
```

The verifier checks skill structure, UI metadata, Rylai maintainer metadata,
provenance, manifest consistency, private paths, banned vendor residue, and
missing third-party notices.

The release checksum file can be checked with:

```powershell
Get-FileHash -Algorithm SHA256 <file>
```

## Repository Layout

```text
skills/
  <skill-name>/
    SKILL.md
    agents/openai.yaml
    scripts/ references/ assets/ ... when required
GIAI_THICH_SKILLS_VI.md
manifest.json
PROVENANCE.yml
THIRD_PARTY_NOTICES.md
install-codex.ps1
install-hermes.sh
verify_bundle.py
```

## License

Rylai-authored material is released under the MIT License. Third-party material
keeps its original license; see the notices and provenance files.

This is a community project and is not endorsed by the agent platforms or the
upstream repositories listed in the notices.
