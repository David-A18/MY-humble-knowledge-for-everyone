---
type: "Decision Record"
title: "ADR-0001: Knowledge base structure"
description: "Keep growing knowledge in focused topic pages with an index for each directory; the index filename later changed to index.md under OKF."
tags: [decision-records]
status: draft
maturity: draft
audience: "Engineering learners and practitioners"
maintainer: "unassigned"
---

# ADR-0001: Knowledge base structure

Decision state: Accepted. The page's OKF `status: draft` describes its
review maturity, not whether this decision was adopted.

## Context

The repository is intended to grow over time across Git, GitHub Actions, Terraform, Kubernetes, AWS, FinOps, architecture, troubleshooting, and best practices. A single large document would become difficult to navigate, review, and maintain.

## Decision

Use a directory-based documentation structure with one `README.md` index per documentation directory and focused Markdown articles under topic-specific subdirectories.

## Consequences

- Readers can start from the root index and navigate by topic.
- New content has a predictable home.
- Indexes must be updated whenever articles are added, moved, or removed.
- Small articles are preferred over large catch-all documents.

## How to read this decision today

The important choice is **one focused page per reader outcome**, grouped
under a topic index. That gives a newcomer a place to start and lets a
maintainer review one claim or example without opening a giant file.

The original `README.md` index filename above is historical. The
2026-09-20 [OKF migration](../log.md) changed the reader-facing bundle
to reserved `index.md` files: [knowledge/index.md](../index.md) is the
bundle root, and every child knowledge directory has its own `index.md`.
Follow the current [authoring rules](../../instructions.md) when adding
a page. The directory-and-focused-page decision remains in use.

Reconsider the navigation structure if reader tasks repeatedly cannot
find an article through the index tree, or if a future OKF version
changes the reserved index convention. The [reading-site
decision](adr-0005-git-backed-reading-site.md) adds another
presentation of the same source pages; it does not remove their topic
homes.

## Related links

- [Templates](../templates/index.md)
- [Contributing](../../CONTRIBUTING.md)
- [Back to decision records](index.md)
- [Back to knowledge index](../index.md)
