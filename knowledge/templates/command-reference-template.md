---
type: Template
title: Command reference template
description: Start a safe, scannable command reference with context checks, expected results, and recovery guidance.
tags: [templates, command-reference]
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
---

# Command reference template

> [!IMPORTANT]
> Replace the frontmatter and command placeholders. A command reference is a `Reference`, not a tutorial; keep it precise and task-oriented.

## Purpose

State which tool, command family, or operational task this reference covers.

## Before running commands

- State the required tools, versions, permissions, account, cluster, or working directory.
- Show a harmless context check before a command can alter data or infrastructure.
- Link to the related tutorial or troubleshooting guide when the task needs more explanation.

## Quick reference

| Task | Command | Success signal |
| --- | --- | --- |
| Describe the task | `tool command --flag` | State what confirms the result. |

## Command details

### Command name

Use this when: describe the exact condition.

> [!WARNING]
> Explain destructive, irreversible, credential-sensitive, or production-impacting behavior before the affected command.

```bash
tool command --flag value
```

What it does: explain the command in plain language.

Expected result: show a short expected output or observable invariant.

If it fails: name the first diagnostic command or link to a troubleshooting guide.

## Evidence and freshness

Use official command documentation in frontmatter `sources`. Record the version or review scope in the page only when it is real.

## Related links

- [Writing instructions](../../instructions.md)
- [Back to templates index](index.md)
- [Back to knowledge index](../index.md)
