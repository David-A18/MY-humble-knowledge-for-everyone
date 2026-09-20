# Knowledge-base upgrade instructions

## Purpose

Define how to plan, validate, and release changes that upgrade the knowledge base itself.

Status: Draft
Audience: Maintainers and AI agents working on the `develop` branch
Page type: Instruction index
Maintainer: Unassigned
Last substantive review: 2026-09-20
Applicable versions: Current repository structure on the `develop` branch
Validation evidence: Markdown lint and local link validation must pass before publication
Known limitations: This guide describes repository workflow; it does not configure external services
Next review: Before merging `develop` into `main`

## Instruction index

| Guide | Use it for |
| --- | --- |
| [Upgrade workflow](upgrade-workflow.md) | Plan and implement one knowledge-base upgrade safely. |
| [Evidence levels](evidence-levels.md) | Record what was source-reviewed, statically checked, executed, or reader-tested. |
| [Branching and release flow](branching-and-release-flow.md) | Keep `main` stable while `develop` collects upgrade work. |

## Related links

- [Knowledge-base upgrade hub](../README.md)
- [Validation command matrix](../tools/validation-command-matrix.md)
- [Back to root index](../../README.md)
