from __future__ import annotations

import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path, PurePosixPath

import yaml

from build_claude_packages import should_exclude

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
REQUIRED_EDITION = "Codex-Hermes-Claude"
REQUIRED_VERSION = "1.1.0"
REQUIRED_SKILL_COUNT = 35
MAX_CLAUDE_DESCRIPTION = 200
BANNED_TEXT = {
    "legacy source package": "unverifiable provenance",
    "gooseworks": "removed credential adapter",
    "alicdn.com": "remote placeholder asset",
    "placehold.co": "remote placeholder asset",
    "qoder": "removed marketplace/vendor residue",
    "qorder": "removed marketplace/vendor residue",
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
    "install-claude.sh",
    "install-claude.ps1",
    "build_claude_packages.py",
}
REQUIRED_ROOT_FILES = {
    "install-codex.ps1",
    "install-hermes.sh",
    "install-claude.ps1",
    "install-claude.sh",
    "build_claude_packages.py",
}
REQUIRED_HOSTS = {"codex", "hermes", "claude"}
PACKAGES = ROOT / "packages"


def parse_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\r?\n(.*?)\r?\n---", text, re.DOTALL)
    if not match:
        raise ValueError("invalid frontmatter")
    value = yaml.safe_load(match.group(1))
    if not isinstance(value, dict):
        raise ValueError("frontmatter must be a mapping")
    return value


def skill_hash(directory: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in directory.rglob("*") if item.is_file()):
        relative = path.relative_to(directory).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def markdown_issues(path: Path, text: str) -> list[str]:
    issues: list[str] = []
    fence_char = ""
    fence_length = 0
    fence_line = 0

    for line_number, line in enumerate(text.splitlines(), start=1):
        match = re.match(r"^\s*(`{3,}|~{3,})(.*)$", line)
        if match:
            marker = match.group(1)
            suffix = match.group(2)
            if not fence_char:
                fence_char = marker[0]
                fence_length = len(marker)
                fence_line = line_number
            elif (
                marker[0] == fence_char
                and len(marker) >= fence_length
                and not suffix.strip()
            ):
                fence_char = ""
                fence_length = 0
                fence_line = 0
            continue

        if fence_char:
            continue

        inline_runs = re.findall(r"(?<!\\)(?<!`)`+(?!`)", line)
        if len(inline_runs) % 2:
            issues.append(
                f"{path.relative_to(ROOT)}:{line_number}: odd inline backtick delimiter"
            )

    if fence_char:
        issues.append(
            f"{path.relative_to(ROOT)}:{fence_line}: unclosed fenced code block"
        )
    return issues


failures: list[str] = []
skill_dirs = sorted(path for path in SKILLS.iterdir() if path.is_dir())
notices = (ROOT / "THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8")
readme = (ROOT / "README.md").read_text(encoding="utf-8")

if len(skill_dirs) != REQUIRED_SKILL_COUNT:
    failures.append(
        f"skills/: expected {REQUIRED_SKILL_COUNT} skill folders, found {len(skill_dirs)}"
    )

for name in sorted(REQUIRED_ROOT_FILES):
    if not (ROOT / name).is_file():
        failures.append(f"missing required file: {name}")

for snippet in sorted(REQUIRED_README_SNIPPETS):
    if snippet not in readme:
        failures.append(f"README.md is missing required text: {snippet}")
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
    elif len(str(frontmatter["description"])) > MAX_CLAUDE_DESCRIPTION:
        failures.append(
            f"{directory.name}: description exceeds Claude's "
            f"{MAX_CLAUDE_DESCRIPTION}-character limit"
        )

    metadata = frontmatter.get("metadata")
    if not isinstance(metadata, dict):
        failures.append(f"{directory.name}: missing metadata mapping")
        metadata = {}
    if metadata.get("maintainer") != "Rylai":
        failures.append(f"{directory.name}: missing Rylai maintainer stamp")
    if metadata.get("edition") != REQUIRED_EDITION:
        failures.append(f"{directory.name}: edition must be {REQUIRED_EDITION}")
    if not isinstance(metadata.get("claude"), dict):
        failures.append(f"{directory.name}: missing metadata.claude mapping")

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
    if re.search(r"Codex-Hermes(?!-Claude)", text):
        failures.append(
            f"{path.relative_to(ROOT)}: contains stale Codex-Hermes edition wording"
        )
    if path.suffix.lower() == ".md":
        failures.extend(markdown_issues(path, text))

manifest_path = ROOT / "manifest.json"
try:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest_names = [item["name"] for item in manifest["skills"]]
    actual_names = [path.name for path in skill_dirs]
    if manifest.get("skill_count") != len(skill_dirs):
        failures.append("manifest skill_count mismatch")
    if manifest.get("version") != REQUIRED_VERSION:
        failures.append(f"manifest version must be {REQUIRED_VERSION}")
    if manifest.get("edition") != REQUIRED_EDITION:
        failures.append(f"manifest edition must be {REQUIRED_EDITION}")
    if manifest_names != actual_names:
        failures.append("manifest skill order or names mismatch")
    manifest_by_name = {item["name"]: item for item in manifest["skills"]}
    for directory in skill_dirs:
        entry = manifest_by_name.get(directory.name, {})
        files = [path for path in directory.rglob("*") if path.is_file()]
        expected_bytes = sum(path.stat().st_size for path in files)
        if entry.get("files") != len(files):
            failures.append(f"manifest.json: wrong file count for {directory.name}")
        if entry.get("bytes") != expected_bytes:
            failures.append(f"manifest.json: wrong byte count for {directory.name}")
        if entry.get("skill_sha256") != skill_hash(directory):
            failures.append(f"manifest.json: wrong skill hash for {directory.name}")
        if entry.get("compatible_hosts") != ["codex", "hermes", "claude"]:
            failures.append(
                f"manifest.json: wrong compatible_hosts for {directory.name}"
            )
    hosts = manifest.get("hosts")
    if not isinstance(hosts, dict):
        failures.append("manifest.json: missing hosts mapping")
    else:
        for host in sorted(REQUIRED_HOSTS - set(hosts)):
            failures.append(f"manifest.json: missing host entry {host}")
        for host, entry in sorted(hosts.items()):
            if not isinstance(entry, dict) or not str(entry.get("skill_dir", "")).strip():
                failures.append(f"manifest.json: host {host} is missing skill_dir")
except (OSError, UnicodeError, ValueError, KeyError, TypeError) as exc:
    failures.append(f"manifest.json: {exc}")

legacy_packages = sorted(path.relative_to(ROOT) for path in ROOT.rglob("*.skill"))
for path in legacy_packages:
    failures.append(f"{path}: stale .skill package; use a .zip archive")

if not PACKAGES.is_dir():
    failures.append("packages/ is missing; run python build_claude_packages.py")
else:
    archives = sorted(PACKAGES.glob("*.zip"))
    if len(archives) != REQUIRED_SKILL_COUNT:
        failures.append(
            f"packages/: expected {REQUIRED_SKILL_COUNT} ZIP archives, "
            f"found {len(archives)}"
        )
    packaged = sorted(path.stem for path in archives)
    expected = [path.name for path in skill_dirs]
    if packaged != expected:
        missing = sorted(set(expected) - set(packaged))
        extra = sorted(set(packaged) - set(expected))
        if missing:
            failures.append(f"packages/ is missing archives for {missing}")
        if extra:
            failures.append(f"packages/ has archives without a skill folder: {extra}")
    stale = "; rebuild with python build_claude_packages.py --clean"
    for name in packaged:
        archive = PACKAGES / f"{name}.zip"
        source = SKILLS / name
        try:
            with zipfile.ZipFile(archive) as bundle:
                if bundle.testzip() is not None:
                    failures.append(f"packages/{name}.zip: corrupt archive")
                    continue
                names = bundle.namelist()
                if len(names) != len(set(names)):
                    failures.append(f"packages/{name}.zip: duplicate archive entries")
                    continue
                invalid_paths = [
                    entry
                    for entry in names
                    if PurePosixPath(entry).is_absolute()
                    or ".." in PurePosixPath(entry).parts
                ]
                if invalid_paths:
                    failures.append(
                        f"packages/{name}.zip: unsafe archive paths {invalid_paths}"
                    )
                    continue
                wrong_roots = [
                    entry for entry in names if not entry.startswith(f"{name}/")
                ]
                if wrong_roots:
                    failures.append(
                        f"packages/{name}.zip: entries outside {name}/ {wrong_roots}"
                    )
                    continue
                if f"{name}/SKILL.md" not in names:
                    failures.append(f"packages/{name}.zip: missing {name}/SKILL.md at the archive root")
                    continue
                if not source.is_dir():
                    continue
                expected = {
                    path.relative_to(source.parent).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
                    for path in source.rglob("*")
                    if path.is_file() and not should_exclude(path.relative_to(source))
                }
                actual = {
                    entry: hashlib.sha256(bundle.read(entry)).hexdigest()
                    for entry in bundle.namelist()
                }
                if set(expected) != set(actual):
                    added = sorted(set(actual) - set(expected))
                    removed = sorted(set(expected) - set(actual))
                    detail = ", ".join(filter(None, [
                        f"extra {added}" if added else "",
                        f"missing {removed}" if removed else "",
                    ]))
                    failures.append(f"packages/{name}.zip: does not match skills/{name} ({detail}){stale}")
                else:
                    changed = sorted(key for key, value in expected.items() if actual[key] != value)
                    if changed:
                        failures.append(f"packages/{name}.zip: stale content for {changed}{stale}")
        except (OSError, zipfile.BadZipFile) as exc:
            failures.append(f"packages/{name}.zip: {exc}")

    package_checksums = PACKAGES / "checksums.sha256"
    if not package_checksums.is_file():
        failures.append("packages/checksums.sha256 is missing")
    else:
        recorded = {}
        for line in package_checksums.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            digest, _, filename = line.partition("  ")
            recorded[filename.strip()] = digest.strip()
        for name in packaged:
            archive = PACKAGES / f"{name}.zip"
            digest = hashlib.sha256(archive.read_bytes()).hexdigest()
            if recorded.get(f"{name}.zip") != digest:
                failures.append(f"packages/checksums.sha256: wrong or missing hash for {name}.zip{stale}")
        for filename in sorted(set(recorded) - {f"{name}.zip" for name in packaged}):
            failures.append(f"packages/checksums.sha256: entry for unknown archive {filename}{stale}")

if failures:
    print("\n".join(failures))
    sys.exit(1)

print(f"PASS: {len(skill_dirs)} Rylai skills validated for Codex, Hermes, and Claude")
