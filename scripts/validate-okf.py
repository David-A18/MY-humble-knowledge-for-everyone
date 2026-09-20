#!/usr/bin/env python3
"""Validate this repository's strict producer profile for an OKF v0.2 bundle."""

from __future__ import annotations

import argparse
import re
from datetime import date, datetime
from pathlib import Path

import yaml


PROFILE_TYPES = {
    "Tutorial",
    "How-to Guide",
    "Reference",
    "Explanation",
    "Troubleshooting Guide",
    "Decision Record",
    "Learning Path",
    "Template",
    "Glossary",
    "Asset Guide",
    # These types are used by the embedded OKF example bundle.
    "Playbook",
    "Attested Computation",
    "Source Reference",
    "Executor Reference",
    "Attester Reference",
}
STATUSES = {"draft", "stable", "deprecated"}
MATURITY = {"initial-outline", "draft", "maintained", "deprecated"}
ACTOR = re.compile(r"^(?:human:[A-Za-z0-9._-]+|process:[A-Za-z0-9._-]+|[A-Za-z0-9._-]+/[A-Za-z0-9._-]+)$")
DATE_HEADING = re.compile(r"^## (\d{4}-\d{2}-\d{2})(?:\b|:)", re.MULTILINE)
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)\s]+)")


def split_frontmatter(markdown: str) -> tuple[dict | None, str, str | None]:
    if not markdown.startswith("---\n"):
        return None, markdown, None
    end = markdown.find("\n---\n", 4)
    if end == -1:
        return None, markdown, "frontmatter has no closing delimiter"
    raw = markdown[4:end]
    try:
        parsed = yaml.safe_load(raw)
    except yaml.YAMLError as error:
        return None, markdown[end + 5 :], f"invalid YAML frontmatter: {error}"
    if not isinstance(parsed, dict):
        return None, markdown[end + 5 :], "frontmatter must be a YAML mapping"
    return parsed, markdown[end + 5 :], None


def markdown_links(markdown: str) -> set[str]:
    return {match.group(1).split("#", 1)[0] for match in LINK.finditer(markdown)}


def validate_bundle(bundle: Path) -> list[str]:
    errors: list[str] = []
    markdown_files = sorted(bundle.rglob("*.md"))
    root_index = bundle / "index.md"
    if not root_index.is_file():
        return [f"{bundle}: missing bundle-root index.md"]

    for path in markdown_files:
        rel = path.relative_to(bundle).as_posix()
        metadata, body, parse_error = split_frontmatter(path.read_text(encoding="utf-8"))
        if parse_error:
            errors.append(f"{rel}: {parse_error}")
            continue

        if path.name == "index.md":
            if path == root_index:
                if metadata != {"okf_version": "0.2"}:
                    errors.append(f"{rel}: root index must contain only okf_version: \"0.2\" frontmatter")
            elif metadata is not None:
                errors.append(f"{rel}: nested index files must not have frontmatter")
            continue

        if path.name == "log.md":
            if metadata is not None:
                errors.append(f"{rel}: log files must not have frontmatter")
            dates = DATE_HEADING.findall(body)
            if not dates:
                errors.append(f"{rel}: log must contain at least one ISO 8601 date heading")
            elif dates != sorted(dates, reverse=True):
                errors.append(f"{rel}: log date headings must be newest first")
            continue

        if metadata is None:
            errors.append(f"{rel}: concept is missing YAML frontmatter")
            continue
        for field in ("type", "title", "description", "tags", "status", "maturity", "audience", "maintainer"):
            if field not in metadata or metadata[field] in (None, "", []):
                errors.append(f"{rel}: missing required profile field {field}")
        if metadata.get("type") not in PROFILE_TYPES:
            errors.append(f"{rel}: unsupported profile type {metadata.get('type')!r}")
        if metadata.get("status") not in STATUSES:
            errors.append(f"{rel}: status must be one of {sorted(STATUSES)}")
        if metadata.get("maturity") not in MATURITY:
            errors.append(f"{rel}: maturity must be one of {sorted(MATURITY)}")
        if not isinstance(metadata.get("tags"), list) or not all(isinstance(tag, str) and tag for tag in metadata.get("tags", [])):
            errors.append(f"{rel}: tags must be a non-empty list of strings")
        for field in ("generated",):
            if field in metadata:
                value = metadata[field]
                if not isinstance(value, dict) or not value.get("by") or not value.get("at") or not ACTOR.match(str(value["by"])):
                    errors.append(f"{rel}: {field} must contain a valid by actor and at value")
        if "verified" in metadata:
            verified = metadata["verified"]
            entries = verified if isinstance(verified, list) else [verified]
            if not all(isinstance(entry, dict) and ACTOR.match(str(entry.get("by", ""))) and entry.get("at") for entry in entries):
                errors.append(f"{rel}: verified entries must contain valid by actors and at values")
        if "sources" in metadata:
            sources = metadata["sources"]
            if not isinstance(sources, list) or not all(isinstance(source, dict) and source.get("resource") for source in sources):
                errors.append(f"{rel}: each source must be a mapping with resource")
        for date_field in ("stale_after",):
            if date_field in metadata and not isinstance(metadata[date_field], (str, date, datetime)):
                errors.append(f"{rel}: {date_field} must be an ISO date or timestamp")

    for directory in sorted({path.parent for path in markdown_files}):
        index = directory / "index.md"
        if not index.is_file():
            errors.append(f"{directory.relative_to(bundle).as_posix()}: missing index.md")
            continue
        index_links = markdown_links(index.read_text(encoding="utf-8"))
        for child in sorted(directory.iterdir()):
            if child.name in {"index.md", "log.md"}:
                continue
            if child.is_file() and child.suffix == ".md":
                expected = child.name
            elif child.is_dir() and any(child.rglob("*.md")):
                expected = f"{child.name}/index.md"
            else:
                continue
            if expected not in index_links and f"{child.name}/" not in index_links:
                errors.append(f"{index.relative_to(bundle).as_posix()}: does not list {expected}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", nargs="?", default="knowledge", type=Path)
    args = parser.parse_args()
    errors = validate_bundle(args.bundle.resolve())
    if errors:
        print("\n".join(errors))
        print(f"OKF validation failed with {len(errors)} error(s).")
        return 1
    print(f"OKF v0.2 profile validation passed for {args.bundle}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
