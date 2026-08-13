#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Install the Rylai skill bundle for Claude.

Usage:
  bash install-claude.sh [--force] [--project | --target <dir>]

Options:
  --force           Replace existing skills. Each replaced folder is backed up first.
  --project         Install into ./.claude/skills so the skills apply to the
                    current project only.
  --target <dir>    Install into an explicit directory.
  -h, --help        Show this message.

Default target: ${HOME}/.claude/skills (available in every Claude session).
USAGE
}

force=0
target_root="${HOME}/.claude/skills"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --force)
      force=1
      shift
      ;;
    --project)
      target_root="$(pwd)/.claude/skills"
      shift
      ;;
    --target)
      if [[ $# -lt 2 ]]; then
        echo "Missing directory after --target" >&2
        exit 2
      fi
      target_root="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

source_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/skills"
target_parent="$(cd "$(dirname "${target_root}")" 2>/dev/null && pwd || dirname "${target_root}")"
backup_root="${target_parent}/rylai-skill-backups/$(date -u +%Y%m%d-%H%M%S)"
mkdir -p "${target_root}"

installed=0
skipped=0

for source in "${source_root}"/*; do
  [[ -d "${source}" ]] || continue
  name="$(basename "${source}")"
  target="${target_root}/${name}"
  if [[ -e "${target}" ]]; then
    if [[ "${force}" -ne 1 ]]; then
      echo "Skip existing skill: ${name}. Re-run with --force to replace." >&2
      skipped=$((skipped + 1))
      continue
    fi
    mkdir -p "${backup_root}"
    cp -a "${target}" "${backup_root}/${name}"
    rm -rf -- "${target}"
  fi
  cp -a "${source}" "${target}"
  echo "Installed ${name}"
  installed=$((installed + 1))
done

echo
echo "Installed ${installed} skill(s), skipped ${skipped}."
echo "Target: ${target_root}"
if [[ "${force}" -eq 1 ]]; then
  echo "Backup root: ${backup_root}"
fi
echo "Start a new Claude session so the skills are picked up."
