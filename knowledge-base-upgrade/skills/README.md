# Knowledge-base upgrade skills

## Purpose

Store reusable AI-agent skill packages for maintaining and improving this knowledge base.

Status: Draft
Audience: Maintainers and AI agents reviewing reusable workflows
Page type: Skill index
Maintainer: Unassigned
Last substantive review: 2026-09-20
Applicable versions: Current repository structure on the `develop` branch
Validation evidence: Markdown lint and local link validation must pass before publication
Known limitations: Skills in this directory are not installed automatically; review and install them explicitly if needed
Next review: Before installing any skill outside the repository

## Skill packages

| Skill | Use it for |
| --- | --- |
| [Knowledge curator](knowledge-curator/README.md) | Improve an existing article or add a focused article while keeping indexes and evidence current. |
| [Source ingestion router](source-ingestion-router/README.md) | Convert raw notes into curated destination pages with traceability. |
| [Evidence recorder](evidence-recorder/README.md) | Record validation evidence, limitations, follow-ups, and changelog entries consistently. |

## Installation rule

These files are repository-reviewed skill drafts. To use one in a local Codex skill directory, copy it intentionally after review. Do not install automatically from this repository, and do not add local machine paths or account-specific configuration to these skill files.

## Related links

- [Knowledge-base upgrade hub](../README.md)
- [Upgrade workflow](../instructions/upgrade-workflow.md)
- [AI tooling](../../ai/ai-tooling/README.md)
- [Back to root index](../../README.md)
