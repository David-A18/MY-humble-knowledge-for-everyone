---
type: Template
title: Knowledge article template
description: Start a focused explanation or how-to guide with complete OKF metadata, evidence, and navigation.
tags: [templates, knowledge-article]
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
---

# Knowledge article template

> [!IMPORTANT]
> Copy this file, then replace every frontmatter value. Choose either `Explanation` or `How-to Guide` as the new concept type; do not make one page serve both reader outcomes.

## Purpose

State the single question the reader will understand or the single task they will complete.

## When to use this

- Describe the starting situation.
- State the result the reader should expect.
- Link prerequisite concepts or official documentation.

## Explanation or procedure

For an **Explanation**, describe the model, relationships, trade-offs, and decision criteria.

For a **How-to Guide**, state prerequisites, then give safe dependency-ordered steps. Put a warning before any destructive, expensive, credential-sensitive, or production-impacting action.

```bash
tool command --flag value
```

What it does: explain what the command reads, changes, or validates.

Expected result: describe the observable success condition and the first useful failure signal.

## Evidence and freshness

- Add official source records to frontmatter for material technical claims.
- Record `stale_after` when the page is reviewed.
- Add a `verified` record only for a real review or execution event.
- Keep `status: draft` until the page has current evidence and an owner.

## Related links

- [Writing instructions](../../instructions.md)
- [Back to templates index](index.md)
- [Back to knowledge index](../index.md)
