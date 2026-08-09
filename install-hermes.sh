#!/usr/bin/env bash
set -euo pipefail

force=0
if [[ "${1:-}" == "--force" ]]; then
  force=1
fi

source_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/skills"
target_root="${HOME}/.hermes/skills"
backup_root="${target_root}/.rylai_backups/$(date -u +%Y%m%d-%H%M%S)"
mkdir -p "${target_root}"

for source in "${source_root}"/*; do
  [[ -d "${source}" ]] || continue
  name="$(basename "${source}")"
  target="${target_root}/${name}"
  if [[ -e "${target}" ]]; then
    if [[ "${force}" -ne 1 ]]; then
      echo "Skip existing skill: ${name}. Re-run with --force to replace." >&2
      continue
    fi
    mkdir -p "${backup_root}"
    cp -a "${target}" "${backup_root}/${name}"
    rm -rf -- "${target}"
  fi
  cp -a "${source}" "${target}"
  echo "Installed ${name}"
done
