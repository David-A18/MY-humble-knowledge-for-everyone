---
type: Template
title: Tutorial template
description: Start a bounded, reproducible learning tutorial with prerequisites, validation, recovery, and cleanup.
tags: [templates, tutorial]
status: draft
maturity: draft
audience: Beginning platform engineer
maintainer: unassigned
---

# Tutorial template

> [!IMPORTANT]
> Replace the frontmatter and placeholders. A tutorial teaches one bounded experience from a known starting point to a verified result.

## Goal

Describe the concrete result the reader will produce and what they will understand afterwards.

## Prerequisites

- Tool versions and installation links.
- Permissions, accounts, local resources, and cost boundaries.
- A disposable environment when commands can modify state.

## Files

| File | Purpose |
| --- | --- |
| `example.file` | Explain why it exists. |

## Steps

1. Prepare the environment and confirm the target context.
2. Apply the configuration or command.
3. Observe the intended result.
4. Introduce one safe, useful diagnostic or failure condition when it teaches the goal.
5. Recover and confirm the result again.

## Validation

```bash
tool validate --target example
```

What it does: confirms the exercise reached the intended state.

Expected result: state the visible condition that proves success.

## Cleanup

> [!WARNING]
> Put this warning before commands that delete resources, incur cost, or affect shared infrastructure.

```bash
tool delete --target example
```

What it does: removes resources created by the exercise and prevents ongoing cost or state drift.

Expected result: state how the reader proves cleanup is complete.

## Evidence and freshness

Record actual local or sandbox execution in `verified`; do not claim execution that did not happen.

## Related links

- [Writing instructions](../../instructions.md)
- [Back to templates index](index.md)
- [Back to knowledge index](../index.md)
