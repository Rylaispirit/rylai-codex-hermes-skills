# Rylai Codex-Hermes-Claude Skills

A personal collection of portable Agent Skills curated, adapted, and maintained
by **Rylai** for Codex, Hermes, and Claude.

The bundle contains 35 independent skills for writing, research, data, documents,
presentations, design, media, finance, deployment, and skill creation. The skills
can be installed together or copied individually.

Every skill is a plain `SKILL.md` folder with no runtime lock-in, so the same
files load in Codex, Hermes, and Claude. Only the install location differs.

## Ownership And Sources

- Rylai authors the bundle structure, installers, validators, Vietnamese guide,
  clean-room replacements, compatibility notes, and original helper scripts.
- Skills adapted from public GitHub projects retain their upstream repository,
  revision, author, and license information.
- An upstream credit means the corresponding author owns their original work.
  Rylai is the maintainer and adapter of this Codex-Hermes-Claude edition.
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

### Claude

```bash
bash install-claude.sh
```

```powershell
.\install-claude.ps1
```

Use `--force` (`-Force` in PowerShell) to replace existing skills. Existing
folders are backed up first.

The default target is the personal skill directory, so the skills load in every
Claude session. Pass `--project` (`-Project`) to install into `.claude/skills`
next to the current project instead, or `--target <dir>` (`-Target <dir>`) to
choose the directory yourself. Skills are discovered when a session starts, so
start a new Claude session after installing.

Claude reads the same `SKILL.md` frontmatter as the other runtimes. The extra
`agents/openai.yaml` file in each skill is ignored there and is kept only so one
checkout serves all three agents.

### Prebuilt Claude ZIP Files

`packages/` holds one `.zip` archive per skill, built from `skills/` by
`build_claude_packages.py`. Each ZIP has the skill folder at its root, including
that folder's `SKILL.md` and bundled resources.

Use these with Claude.ai or Cowork through the skill-management interface.
Claude Code should use the unpacked folders through `install-claude.sh`,
`install-claude.ps1`, or a manual copy into a Claude skill directory.

Rebuild them after editing any skill:

```bash
python build_claude_packages.py --clean
```

Archives are reproducible, so an unchanged skill keeps its checksum. Per-archive
hashes are written to `packages/checksums.sha256`.

### Install One Skill

Copy one directory from `skills/` into the skill directory used by your agent:

```text
Codex:  ~/.agents/skills/<skill-name>
Hermes: ~/.hermes/skills/<skill-name>
Claude: ~/.claude/skills/<skill-name>          personal, every session
        <project>/.claude/skills/<skill-name>  one project only
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
provenance, manifest consistency, Markdown fences and inline code spans, private
paths, banned vendor residue, third-party notices, and whether all 35 Claude ZIP
packages are still in sync with `skills/`.

`checksums.sha256` covers the source files in this repository. The generated
archives are covered separately by `packages/checksums.sha256`. Both are plain
sha256 manifests:

```bash
sha256sum -c checksums.sha256
cd packages && sha256sum -c checksums.sha256
```

The archive manifest lists bare file names, so check it from inside `packages/`.

```powershell
Get-FileHash -Algorithm SHA256 <file>
```

Regenerate the release checksum file after changing any source file:

```bash
python build_claude_packages.py --release-checksums
```

## Repository Layout

```text
skills/
  <skill-name>/
    SKILL.md
    agents/openai.yaml
    scripts/ references/ assets/ ... when required
manifest.json
PROVENANCE.yml
THIRD_PARTY_NOTICES.md
packages/
  <skill-name>.zip
  checksums.sha256
GIAI_THICH_SKILLS_VI.md
install-codex.ps1
install-hermes.sh
install-claude.ps1
install-claude.sh
build_claude_packages.py
verify_bundle.py
```

## License

Rylai-authored material is released under the MIT License. Third-party material
keeps its original license; see the notices and provenance files.

This is a community project and is not endorsed by the agent platforms or the
upstream repositories listed in the notices.
