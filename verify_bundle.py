from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
SKILLS = ROOT / "skills"
ALLOWED_FRONTMATTER = {
    "name",
    "description",
    "license",
    "allowed-tools",
    "metadata",
}
ALLOWED_PROVENANCE = {"clean-room-original", "adapted-open-source"}
BANNED_TEXT = {
    "legacy source package": "unverifiable provenance",
    "gooseworks": "removed credential adapter",
    "alicdn.com": "remote placeholder asset",
    "placehold.co": "remote placeholder asset",
}
TEXT_SUFFIXES = {
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".py",
    ".js",
    ".mjs",
    ".cjs",
    ".html",
    ".css",
    ".sh",
    ".ps1",
}
REQUIRED_README_SNIPPETS = {
    "requirements-verify.txt",
    "## Repository Layout",
    "THIRD_PARTY_NOTICES.md",
    "PROVENANCE.yml",
}


def parse_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\r?\n(.*?)\r?\n---", text, re.DOTALL)
    if not match:
        raise ValueError("invalid frontmatter")
    value = yaml.safe_load(match.group(1))
    if not isinstance(value, dict):
        raise ValueError("frontmatter must be a mapping")
    return value


failures: list[str] = []
skill_dirs = sorted(path for path in SKILLS.iterdir() if path.is_dir())
notices = (ROOT / "THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8")
readme = (ROOT / "README.md").read_text(encoding="utf-8")

for snippet in sorted(REQUIRED_README_SNIPPETS):
    if snippet not in readme:
        failures.append(f"README.md is missing required text: {snippet}")
if readme.count("```") % 2:
    failures.append("README.md contains an unclosed fenced code block")
if notices.count("`") % 2:
    failures.append("THIRD_PARTY_NOTICES.md contains an unclosed inline code span")
if "- License: MI\n" in notices:
    failures.append("THIRD_PARTY_NOTICES.md contains truncated MIT license text")

for directory in skill_dirs:
    skill_file = directory / "SKILL.md"
    ui_file = directory / "agents" / "openai.yaml"

    if not skill_file.exists():
        failures.append(f"{directory.name}: missing SKILL.md")
        continue

    try:
        frontmatter = parse_frontmatter(skill_file)
    except (OSError, UnicodeError, ValueError, yaml.YAMLError) as exc:
        failures.append(f"{directory.name}: {exc}")
        continue

    extra = set(frontmatter) - ALLOWED_FRONTMATTER
    if extra:
        failures.append(f"{directory.name}: unsupported keys {sorted(extra)}")
    if frontmatter.get("name") != directory.name:
        failures.append(f"{directory.name}: name mismatch")
    if not str(frontmatter.get("description", "")).strip():
        failures.append(f"{directory.name}: missing description")

    metadata = frontmatter.get("metadata")
    if not isinstance(metadata, dict):
        failures.append(f"{directory.name}: missing metadata mapping")
        metadata = {}
    if metadata.get("maintainer") != "Rylai":
        failures.append(f"{directory.name}: missing Rylai maintainer stamp")

    provenance = metadata.get("provenance")
    if provenance not in ALLOWED_PROVENANCE:
        failures.append(f"{directory.name}: invalid provenance {provenance!r}")
    if provenance == "adapted-open-source":
        upstream = metadata.get("upstream")
        if not isinstance(upstream, dict):
            failures.append(f"{directory.name}: missing upstream mapping")
        else:
            for key in ("url", "revision", "license"):
                if not str(upstream.get(key, "")).strip():
                    failures.append(f"{directory.name}: missing upstream.{key}")
        if directory.name not in notices:
            failures.append(f"{directory.name}: missing third-party notice")
        if metadata.get("author") == "Rylai":
            failures.append(f"{directory.name}: adapted skill cannot claim Rylai as upstream author")

    if not ui_file.exists():
        failures.append(f"{directory.name}: missing agents/openai.yaml")
    else:
        try:
            ui = yaml.safe_load(ui_file.read_text(encoding="utf-8"))
            prompt = ui.get("interface", {}).get("default_prompt", "")
            if f"${directory.name}" not in prompt:
                failures.append(f"{directory.name}: default prompt lacks skill name")
        except (OSError, UnicodeError, yaml.YAMLError, AttributeError) as exc:
            failures.append(f"{directory.name}: invalid agents/openai.yaml: {exc}")

for path in ROOT.rglob("*"):
    if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
        continue
    if path.resolve() == Path(__file__).resolve():
        continue
    if ".git" in path.parts:
        continue
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeError:
        failures.append(f"{path.relative_to(ROOT)}: text file is not UTF-8")
        continue
    lowered = text.lower()
    for needle, reason in BANNED_TEXT.items():
        if needle in lowered:
            failures.append(f"{path.relative_to(ROOT)}: contains {reason}: {needle}")
    if re.search(r"(?i)c:\\users\\[^\\\s]+", text):
        failures.append(f"{path.relative_to(ROOT)}: contains an absolute Windows user path")
    if re.search(r"(?i)/(?:home|users)/[^/\s]+", text):
        failures.append(f"{path.relative_to(ROOT)}: contains an absolute Unix user path")

manifest_path = ROOT / "manifest.json"
try:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest_names = [item["name"] for item in manifest["skills"]]
    actual_names = [path.name for path in skill_dirs]
    if manifest.get("skill_count") != len(skill_dirs):
        failures.append("manifest skill_count mismatch")
    if manifest_names != actual_names:
        failures.append("manifest skill order or names mismatch")
except (OSError, UnicodeError, ValueError, KeyError, TypeError) as exc:
    failures.append(f"manifest.json: {exc}")

if failures:
    print("\n".join(failures))
    sys.exit(1)

print(f"PASS: {len(skill_dirs)} Rylai Codex-Hermes skills validated")
