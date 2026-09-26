---
type: "Decision Record"
title: "ADR-0001: Knowledge base structure"
description: "The repository is intended to grow over time across Git, GitHub Actions, Terraform, Kubernetes, AWS, FinOps, architecture, troubleshooting, and best practices. A single large document would become difficult to navigate, review, and maintain."
tags: [decision-records]
status: draft
maturity: draft
audience: "Engineering learners and practitioners"
maintainer: "unassigned"
---

# ADR-0001: Knowledge base structure

Status: Accepted

## Context

The repository is intended to grow over time across Git, GitHub Actions, Terraform, Kubernetes, AWS, FinOps, architecture, troubleshooting, and best practices. A single large document would become difficult to navigate, review, and maintain.

## Decision

Use a directory-based documentation structure with one `README.md` index per documentation directory and focused Markdown articles under topic-specific subdirectories.

## Consequences

- Readers can start from the root index and navigate by topic.
- New content has a predictable home.
- Indexes must be updated whenever articles are added, moved, or removed.
- Small articles are preferred over large catch-all documents.

## Related links

- [Templates](../templates/index.md)
- [Contributing](../../CONTRIBUTING.md)
- [Back to decision records](index.md)
- [Back to root index](../../README.md)
