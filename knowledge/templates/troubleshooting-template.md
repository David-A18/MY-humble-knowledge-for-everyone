---
type: Template
title: Troubleshooting guide template
description: Start a symptom-led troubleshooting guide with safe diagnostics, recovery, and prevention.
tags: [templates, troubleshooting]
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
---

# Troubleshooting guide template

> [!IMPORTANT]
> Replace the frontmatter and placeholders. A troubleshooting guide starts from an observable symptom and ends with a safe diagnosis, recovery, or escalation condition.

## Purpose

Name the failure mode, affected system boundary, and reader outcome.

## Symptoms

- Observable symptom, error message, metric, or log pattern.
- Scope: which environment, resources, or versions the guide applies to.

## First checks

- [ ] Confirm the target context and impact.
- [ ] Capture the exact error before changing anything.
- [ ] Check recent changes and rollback options.
- [ ] Preserve evidence that an escalation will need.

## Decision sequence

1. Run a safe diagnostic and state what result confirms the common cause.
2. If confirmed, apply the least-destructive recovery action.
3. If not confirmed, collect the next discriminating evidence.
4. Stop and escalate when the documented safety boundary is reached.

## Diagnostics

```bash
tool inspect --target example
```

What it does: gathers evidence before changing the system.

## Recovery

> [!WARNING]
> Place warnings before destructive or production-impacting recovery commands.

```bash
tool recover --target example
```

What it does: describe the recovery action, its expected result, and its rollback path.

## Prevention

- Preventive practice.
- Monitoring or alerting recommendation.
- Link to the relevant how-to or reference page.

## Evidence and freshness

Use official sources for product-specific behavior and set a review deadline for fast-changing systems.

## Related links

- [Writing instructions](../../instructions.md)
- [Back to templates index](index.md)
- [Back to knowledge index](../index.md)
