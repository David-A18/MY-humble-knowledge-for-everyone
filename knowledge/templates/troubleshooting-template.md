---
type: "Template"
title: "Troubleshooting title"
description: "Diagnose and resolve a specific failure mode."
tags: [templates, troubleshooting-template]
status: draft
maturity: initial-outline
audience: "Beginning platform engineer"
maintainer: "Unassigned"
---

# Troubleshooting title

Status: Initial outline
Audience: Beginning platform engineer
Page type: Troubleshooting
Maintainer: Unassigned
Last substantive review: Not yet reviewed
Applicable versions: To be established before execution
Validation evidence: Not yet tested
Known limitations: To be documented
Next review: Assign after substantive review

## Purpose

Diagnose and resolve a specific failure mode.

## Symptoms

- Observable symptom.
- Error message.
- Metric or log pattern.

## First checks

- [ ] Confirm scope and impact.
- [ ] Capture exact error messages.
- [ ] Check recent changes.
- [ ] Identify rollback options.

## Decision sequence

1. Check the most common cause.
2. If confirmed, apply the documented fix.
3. If not confirmed, collect additional evidence.
4. Escalate with logs, commands, timestamps, and affected resources.

## Commands

```bash
tool inspect --target example
```

What it does: gather evidence before changing the system.

## Recovery

> [!WARNING]
> Place warnings before destructive or production-impacting recovery commands.

```bash
tool recover --target example
```

What it does: describe the recovery action and its rollback path.

## Prevention

- Preventive practice.
- Monitoring or alerting recommendation.

## Related links

- [Writing instructions](../../instructions.md)
- [Back to templates index](index.md)
- [Back to root index](../../README.md)
