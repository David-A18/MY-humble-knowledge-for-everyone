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
    "News Brief",
}
STATUSES = {"draft", "stable", "deprecated"}
ACTOR = re.compile(r"^(?:human:[A-Za-z0-9._-]+|process:[A-Za-z0-9._-]+|[A-Za-z0-9._-]+/[A-Za-z0-9._-]+)$")
MAINTAINER = re.compile(r"^(?:unassigned|human:[A-Za-z0-9._-]+|team:[A-Za-z0-9._-]+)$")
SOURCE_ID = re.compile(r"^[a-z0-9][a-z0-9-]*$")
NEWS_PATH = re.compile(r"^news/(\d{4})/(\d{2})/[a-z0-9][a-z0-9-]*\.md$")
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


def as_date(value) -> date | None:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(str(value))
    except ValueError:
        return None


ALERTS = {"critical"}


def validate_alert(rel: str, metadata: dict, published: date | None, stale_after: date | None) -> list[str]:
    """An optional editorial alert on a news brief: `alert: critical`, ending at `alert_until` or else at `stale_after`."""
    errors = []
    has_alert, has_until = "alert" in metadata, "alert_until" in metadata
    if has_alert and (not isinstance(metadata["alert"], str) or metadata["alert"] not in ALERTS):
        errors.append(f"{rel}: alert must be one of {sorted(ALERTS)}")
    if has_until and not has_alert:
        errors.append(f"{rel}: alert_until needs an alert")
    if has_until:
        until = as_date(metadata["alert_until"])
        if until is None:
            errors.append(f"{rel}: alert_until must be an ISO date")
        elif published and until < published:
            errors.append(f"{rel}: alert_until must not be earlier than published")
        elif stale_after and until > stale_after:
            errors.append(f"{rel}: alert_until must not be later than stale_after")
    return errors


def validate_news(rel: str, metadata: dict) -> list[str]:
    """News briefs are dated, sourced, expiring, and filed by publication month (ADR-0006)."""
    is_brief = metadata.get("type") == "News Brief"
    if rel.startswith("news/") and not is_brief:
        return [f"{rel}: concepts under news/ must use type News Brief"]
    if not is_brief:
        if "alert" in metadata or "alert_until" in metadata:
            return [f"{rel}: only news briefs can carry alert or alert_until"]
        return []
    errors = []
    published = as_date(metadata.get("published"))
    stale_after = as_date(metadata.get("stale_after"))
    if published is None:
        errors.append(f"{rel}: news briefs need a published ISO date")
    if stale_after is None:
        errors.append(f"{rel}: news briefs need a stale_after ISO date")
    elif published and stale_after <= published:
        errors.append(f"{rel}: stale_after must be later than published")
    if not metadata.get("sources"):
        errors.append(f"{rel}: news briefs need at least one source")
    if metadata.get("status") == "stable":
        errors.append(f"{rel}: news briefs cannot be stable; use draft or deprecated")
    match = NEWS_PATH.match(rel)
    if not match:
        errors.append(f"{rel}: news briefs belong in news/YYYY/MM/<kebab-name>.md")
    elif published and (int(match.group(1)), int(match.group(2))) != (published.year, published.month):
        errors.append(f"{rel}: folder news/{match.group(1)}/{match.group(2)}/ does not match published {published.isoformat()}")
    errors.extend(validate_alert(rel, metadata, published, stale_after))
    return errors


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
        for field in ("type", "title", "description", "tags", "status", "audience", "maintainer"):
            if field not in metadata or metadata[field] in (None, "", []):
                errors.append(f"{rel}: missing required profile field {field}")
        if metadata.get("type") not in PROFILE_TYPES:
            errors.append(f"{rel}: unsupported profile type {metadata.get('type')!r}")
        if metadata.get("status") not in STATUSES:
            errors.append(f"{rel}: status must be one of {sorted(STATUSES)}")
        if "maturity" in metadata:
            errors.append(f"{rel}: maturity was retired; use status only")
        if not isinstance(metadata.get("tags"), list) or not all(isinstance(tag, str) and tag for tag in metadata.get("tags", [])):
            errors.append(f"{rel}: tags must be a non-empty list of strings")
        elif len(set(metadata["tags"])) != len(metadata["tags"]):
            errors.append(f"{rel}: tags must not contain duplicates")
        if not MAINTAINER.match(str(metadata.get("maintainer", ""))):
            errors.append(f"{rel}: maintainer must be unassigned, human:<handle>, or team:<name>")
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
            if not isinstance(sources, list) or not all(
                isinstance(source, dict)
                and SOURCE_ID.match(str(source.get("id", "")))
                and source.get("resource")
                and source.get("title")
                for source in sources
            ):
                errors.append(f"{rel}: each source must have a kebab-case id, resource, and title")
            elif len({source["id"] for source in sources}) != len(sources):
                errors.append(f"{rel}: source ids must be unique within a concept")
        for date_field in ("stale_after",):
            if date_field in metadata and not isinstance(metadata[date_field], (str, date, datetime)):
                errors.append(f"{rel}: {date_field} must be an ISO date or timestamp")
        if metadata.get("status") == "stable" and (not metadata.get("sources") or not metadata.get("stale_after")):
            errors.append(f"{rel}: stable concepts need sources and stale_after")

        errors.extend(validate_news(rel, metadata))

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
