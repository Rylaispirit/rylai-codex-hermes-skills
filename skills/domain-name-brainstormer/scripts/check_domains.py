#!/usr/bin/env python3
"""Check domain registration signals through RDAP.

Original utility maintained by Rylai for Codex, Hermes, and Claude skill workflows.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


RDAP_BASE_URL = "https://rdap.org/domain/"
LABEL_PATTERN = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$")


@dataclass(frozen=True)
class DomainResult:
    domain: str
    status: str
    checked_at: str
    detail: str
    rdap_url: str
    registry_statuses: list[str]
    expiration_date: str | None


def normalize_domain(value: str) -> str:
    candidate = value.strip().rstrip(".").lower()
    if not candidate:
        raise ValueError("empty domain")
    try:
        ascii_domain = candidate.encode("idna").decode("ascii")
    except UnicodeError as error:
        raise ValueError("IDN encoding failed") from error
    if len(ascii_domain) > 253 or "." not in ascii_domain:
        raise ValueError("expected a complete domain such as name.tld")
    labels = ascii_domain.split(".")
    if any(not LABEL_PATTERN.fullmatch(label) for label in labels):
        raise ValueError("invalid label syntax")
    if len(labels[-1]) < 2:
        raise ValueError("top-level domain is too short")
    return ascii_domain


def expand_candidates(names: list[str], tlds: list[str]) -> tuple[list[str], list[DomainResult]]:
    cleaned_tlds = []
    for raw_tld in tlds:
        for item in raw_tld.split(","):
            tld = item.strip().lower().lstrip(".")
            if tld and tld not in cleaned_tlds:
                cleaned_tlds.append(tld)

    expanded: list[str] = []
    invalid: list[DomainResult] = []
    for raw_name in names:
        name = raw_name.strip().rstrip(".")
        if not name:
            continue
        candidates = [name] if "." in name else [f"{name}.{tld}" for tld in cleaned_tlds]
        if not candidates:
            candidates = [name]
        for candidate in candidates:
            try:
                normalized = normalize_domain(candidate)
            except ValueError as error:
                invalid.append(
                    DomainResult(
                        domain=candidate,
                        status="invalid",
                        checked_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
                        detail=str(error),
                        rdap_url="",
                        registry_statuses=[],
                        expiration_date=None,
                    )
                )
                continue
            if normalized not in expanded:
                expanded.append(normalized)
    return expanded, invalid


def find_expiration(payload: dict[str, Any]) -> str | None:
    for event in payload.get("events", []):
        action = str(event.get("eventAction", "")).lower()
        if action in {"expiration", "expiry"}:
            value = event.get("eventDate")
            return str(value) if value else None
    return None


def check_domain(domain: str, timeout: float) -> DomainResult:
    checked_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    rdap_url = RDAP_BASE_URL + quote(domain, safe=".-")
    request = Request(
        rdap_url,
        headers={
            "Accept": "application/rdap+json, application/json",
            "User-Agent": "Rylai-Domain-Checker/1.0",
        },
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8", errors="replace"))
        statuses = sorted({str(item) for item in payload.get("status", [])})
        handle = payload.get("handle")
        detail = f"RDAP record found{f' ({handle})' if handle else ''}"
        return DomainResult(
            domain=domain,
            status="registered",
            checked_at=checked_at,
            detail=detail,
            rdap_url=rdap_url,
            registry_statuses=statuses,
            expiration_date=find_expiration(payload),
        )
    except HTTPError as error:
        if error.code == 404:
            status = "likely_available"
            detail = "RDAP returned domain not found"
        elif error.code == 429:
            status = "unknown"
            detail = "RDAP rate limit reached"
        else:
            status = "unknown"
            detail = f"RDAP HTTP error {error.code}"
    except (URLError, TimeoutError) as error:
        status = "unknown"
        detail = f"network error: {error.reason if isinstance(error, URLError) else error}"
    except (json.JSONDecodeError, OSError) as error:
        status = "unknown"
        detail = f"unreadable RDAP response: {error}"

    return DomainResult(
        domain=domain,
        status=status,
        checked_at=checked_at,
        detail=detail,
        rdap_url=rdap_url,
        registry_statuses=[],
        expiration_date=None,
    )


def print_table(results: list[DomainResult]) -> None:
    domain_width = max(len("DOMAIN"), *(len(item.domain) for item in results))
    status_width = max(len("STATUS"), *(len(item.status) for item in results))
    print(f"{'DOMAIN':<{domain_width}}  {'STATUS':<{status_width}}  DETAIL")
    print(f"{'-' * domain_width}  {'-' * status_width}  {'-' * 32}")
    for item in results:
        print(f"{item.domain:<{domain_width}}  {item.status:<{status_width}}  {item.detail}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("names", nargs="+", help="Complete domains or bare names used with --tld")
    parser.add_argument("--tld", action="append", default=[], help="TLD for bare names; repeat or use commas")
    parser.add_argument("--timeout", type=float, default=12.0, help="Per-request timeout in seconds")
    parser.add_argument("--workers", type=int, default=4, help="Parallel requests, from 1 to 8")
    parser.add_argument("--json", type=Path, dest="json_path", help="Optional JSON output path")
    args = parser.parse_args()

    if args.timeout <= 0:
        parser.error("--timeout must be greater than zero")
    if not 1 <= args.workers <= 8:
        parser.error("--workers must be between 1 and 8")

    valid_domains, invalid_results = expand_candidates(args.names, args.tld)

    results_by_domain: dict[str, DomainResult] = {}
    if valid_domains:
        with ThreadPoolExecutor(max_workers=min(args.workers, len(valid_domains))) as executor:
            futures = {
                executor.submit(check_domain, domain, args.timeout): domain
                for domain in valid_domains
            }
            for future in as_completed(futures):
                domain = futures[future]
                try:
                    results_by_domain[domain] = future.result()
                except Exception as error:  # Defensive boundary around worker failures.
                    invalid_results.append(
                        DomainResult(
                            domain=domain,
                            status="unknown",
                            checked_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
                            detail=f"checker failure: {error}",
                            rdap_url=RDAP_BASE_URL + quote(domain, safe=".-"),
                            registry_statuses=[],
                            expiration_date=None,
                        )
                    )

    results = [results_by_domain[domain] for domain in valid_domains if domain in results_by_domain]
    results.extend(invalid_results)
    if not results:
        print("ERROR: no domain candidates were provided", file=sys.stderr)
        return 2
    print_table(results)

    if args.json_path:
        args.json_path.parent.mkdir(parents=True, exist_ok=True)
        args.json_path.write_text(
            json.dumps([asdict(item) for item in results], ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        print(f"JSON: {args.json_path}")

    if any(item.status == "unknown" for item in results):
        return 1
    return 2 if any(item.status == "invalid" for item in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
