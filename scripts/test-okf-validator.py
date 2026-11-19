#!/usr/bin/env python3
"""Fixture tests for the repository OKF v0.2 profile validator."""

from __future__ import annotations

import importlib.util
import tempfile
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("validate-okf.py")
SPEC = importlib.util.spec_from_file_location("validate_okf", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


def write(root: Path, relative: str, content: str) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


VALID_CONCEPT = """---
type: Reference
title: Example
description: A valid example concept.
tags: [example]
status: draft
audience: Readers
maintainer: unassigned
---

# Example
"""


with tempfile.TemporaryDirectory(prefix="okf-validator-") as temporary:
    root = Path(temporary)
    write(root, "index.md", "---\nokf_version: \"0.2\"\n---\n\n# Root\n\n- [Example](example.md)\n")
    write(root, "log.md", "# Log\n\n## 2026-09-20\n\n- **Creation**: Example.\n")
    write(root, "example.md", VALID_CONCEPT)
    assert MODULE.validate_bundle(root) == []

    write(root, "example.md", "# Missing frontmatter\n")
    assert any("missing YAML frontmatter" in error for error in MODULE.validate_bundle(root))

    write(root, "example.md", VALID_CONCEPT)
    write(root, "nested/index.md", "---\ntype: Reference\n---\n")
    assert any("nested index files" in error for error in MODULE.validate_bundle(root))

    write(root, "nested/index.md", "# Nested\n")
    write(root, "log.md", "# Log\n\n## 2026-01-01\n\n- Old.\n\n## 2026-09-20\n\n- New.\n")
    assert any("newest first" in error for error in MODULE.validate_bundle(root))

NEWS_BRIEF = """---
type: News Brief
title: Example brief
description: A dated example brief.
tags: [news]
status: {status}
audience: Readers
maintainer: unassigned
published: {published}
stale_after: {stale_after}
sources:
  - id: primary
    resource: https://example.com/announcement
    title: Announcement
---

# Example brief
"""


def news_errors(path: str, **fields: str) -> list[str]:
    values = {"status": "draft", "published": "2026-11-19", "stale_after": "2027-03-19"} | fields
    with tempfile.TemporaryDirectory(prefix="okf-news-") as temporary:
        root = Path(temporary)
        write(root, "index.md", "---\nokf_version: \"0.2\"\n---\n\n# Root\n\n- [News](news/index.md)\n")
        write(root, "news/index.md", "# News\n\n- [2026](2026/index.md)\n")
        write(root, "news/2026/index.md", "# 2026\n\n- [November](11/index.md)\n")
        directory = path.rsplit("/", 1)[0]
        if directory != "news/2026":
            write(root, f"{directory}/index.md", f"# Month\n\n- [Brief]({path.rsplit('/', 1)[1]})\n")
        write(root, path, NEWS_BRIEF.format(**values))
        return MODULE.validate_bundle(root)


assert news_errors("news/2026/11/example-brief.md") == []
assert any("cannot be stable" in e for e in news_errors("news/2026/11/example-brief.md", status="stable"))
assert any("does not match published" in e for e in news_errors("news/2026/10/example-brief.md"))
assert any("later than published" in e for e in news_errors("news/2026/11/example-brief.md", stale_after="2026-11-01"))
assert any("published ISO date" in e for e in news_errors("news/2026/11/example-brief.md", published="soon"))
assert any("news/YYYY/MM" in e for e in news_errors("news/2026/example-brief.md"))

print("OKF validator fixtures passed.")
