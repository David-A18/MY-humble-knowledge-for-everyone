# Branching and release flow for knowledge-base upgrades

## Purpose

Define how `develop` should carry upgrade work before it is merged into the stable `main` branch.

Status: Draft
Audience: Maintainers and AI agents working across repository branches
Page type: Procedure
Maintainer: Unassigned
Last substantive review: 2026-09-20
Applicable versions: Current repository branch model after creating `develop`
Validation evidence: Markdown lint and local link validation must pass before publication
Known limitations: This flow does not enforce branch protection by itself
Next review: Before the first `develop` to `main` merge

## Branch roles

| Branch | Role | Expected content |
| --- | --- | --- |
| `main` | Stable public knowledge base | Validated documentation, indexes, and maintenance files. |
| `develop` | Upgrade integration branch | New knowledge-base features, tools, skills, MCP templates, and operating instructions before release to `main`. |
| Topic branches | Optional focused work branches | One bounded feature or article group before merging into `develop`. |

## Release flow

1. Create upgrade work from `develop`.
2. Keep commits focused and public-safe.
3. Run local validation before pushing.
4. Let CI finish on `develop`.
5. Review whether the change updates repository routes, contributor instructions, or validation policy.
6. Merge `develop` into `main` only after the upgrade is complete, indexed, validated, and ready for normal readers.
7. After merge, confirm `main` CI passes.

## Merge checklist

- [ ] [Knowledge-base upgrade hub](../README.md) and affected indexes are current.
- [ ] [AGENTS.md](../../AGENTS.md), [context.md](../../context.md), and [CONTRIBUTING.md](../../CONTRIBUTING.md) agree on routing and validation.
- [ ] Skill packages are reviewed as instructions and not treated as installed runtime behavior.
- [ ] MCP templates use placeholders and contain no secrets.
- [ ] Required local checks and GitHub Actions pass.
- [ ] [CHANGELOG.md](../../CHANGELOG.md) records the upgrade.

## Related links

- [Instruction index](README.md)
- [Upgrade workflow](upgrade-workflow.md)
- [Validation command matrix](../tools/validation-command-matrix.md)
- [Back to upgrade hub](../README.md)
- [Back to root index](../../README.md)
