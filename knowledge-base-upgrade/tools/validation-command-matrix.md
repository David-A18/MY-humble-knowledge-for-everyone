# Validation command matrix

## Purpose

Map common knowledge-base upgrade changes to the checks maintainers should run before commit and before merging `develop` into `main`.

Status: Draft
Audience: Maintainers and AI agents validating repository changes
Page type: Command reference
Maintainer: Unassigned
Last substantive review: 2026-09-20
Applicable versions: Current repository validation scripts
Validation evidence: Markdown lint and local link validation must pass before publication
Known limitations: Commands assume the repository tooling is installed locally
Next review: When validation scripts or CI workflows change

## Command matrix

| Change type | Required checks | Also run when relevant |
| --- | --- | --- |
| Markdown-only content | `npx markdownlint-cli2 "**/*.md"`; `node scripts/test-local-link-validator.mjs`; `node scripts/validate-local-links.mjs`; `git diff --check` | Source-specific commands if examples changed. |
| Issue templates or labels | Markdown checks; `python3 scripts/test-issue-template-validator.py`; `python3 scripts/validate-issue-templates.py`; `python3 scripts/check-github-labels.py --repo David-A18/MY-humble-knowledge-for-everyone` | GitHub Actions status after push. |
| Validation scripts | Script-specific tests; full Markdown and link checks; `git diff --check` | Add or update fixtures before relying on new behavior. |
| Skill package | Markdown checks; local-link validation; dry-run review against a sample page | Confirm no secrets, private data, or unreviewed write action is included. |
| MCP config template | Markdown checks; local-link validation; JSON or JSONC parser if available | Confirm placeholders are not real credentials or private endpoints. |
| Branch or release guidance | Markdown checks; local-link validation; issue-template validation if forms changed | Confirm [AGENTS.md](../../AGENTS.md), [context.md](../../context.md), and [CONTRIBUTING.md](../../CONTRIBUTING.md) agree. |

## Standard local validation batch

```bash
git status --short --branch
python3 scripts/test-issue-template-validator.py
python3 scripts/validate-issue-templates.py
python3 scripts/check-github-labels.py --repo David-A18/MY-humble-knowledge-for-everyone
npx markdownlint-cli2 "**/*.md"
node scripts/test-local-link-validator.mjs
node scripts/validate-local-links.mjs
git diff --check
```

What it does: checks branch state, issue-template policy, live GitHub labels, Markdown style, local links, local link validator fixtures, and whitespace problems.

## Related links

- [Tools index](README.md)
- [Tool catalog](tool-catalog.md)
- [Upgrade workflow](../instructions/upgrade-workflow.md)
- [Back to upgrade hub](../README.md)
- [Back to root index](../../README.md)
