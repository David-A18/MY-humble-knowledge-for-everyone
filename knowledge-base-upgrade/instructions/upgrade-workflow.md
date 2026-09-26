# Knowledge-base upgrade workflow

## Purpose

Provide a repeatable workflow for adding knowledge-base features, tools, skill packages, MCP templates, and operating instructions.

Status: Draft
Audience: Maintainers and AI agents implementing upgrade work
Page type: Procedure
Maintainer: Unassigned
Last substantive review: 2026-09-20
Applicable versions: Current repository structure on the `develop` branch
Validation evidence: Markdown lint and local link validation must pass before publication
Known limitations: This workflow does not replace topic-specific instructions in other directories
Next review: Before merging `develop` into `main`

## Workflow

1. Start from `develop` for upgrade work and confirm the branch is clean.
2. Read [AGENTS.md](../../AGENTS.md), [context.md](../../context.md), [instructions.md](../../instructions.md), [CONTRIBUTING.md](../../CONTRIBUTING.md), and this upgrade hub.
3. Choose one bounded upgrade from the [feature backlog](../features/feature-backlog.md) or user request.
4. Decide whether the change is a feature, tool, skill, MCP template, instruction, index, or a combination.
5. Add or edit the smallest useful files and update every affected `README.md` index.
6. Keep configuration templates public-safe; use placeholders for commands, paths, and secrets.
7. Record evidence level and limitations in the page body.
8. Update [CHANGELOG.md](../../CHANGELOG.md) and [context.md](../../context.md) when routes, tools, or validation rules change.
9. Run the checks in the [validation command matrix](../tools/validation-command-matrix.md).
10. Commit on `develop` and push the branch for review.

## Done criteria

- The new or changed capability has a clear reader or maintainer outcome.
- Internal links resolve locally.
- New directories have `README.md` indexes.
- Skill packages and MCP templates contain no secrets or live private configuration.
- Validation results are recorded in the final handoff.

## Related links

- [Instruction index](README.md)
- [Feature backlog](../features/feature-backlog.md)
- [Validation command matrix](../tools/validation-command-matrix.md)
- [Back to upgrade hub](../README.md)
- [Back to root index](../../README.md)
