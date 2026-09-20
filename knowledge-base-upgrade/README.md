# Knowledge-base upgrade hub

## Purpose

This area collects planned upgrades for the knowledge base itself: new reader-facing features, maintainer tools, reusable AI skills, MCP server templates, and operating instructions.

Status: Draft
Audience: Maintainers, contributors, and AI agents improving this repository
Page type: Reference and operating guide
Maintainer: Unassigned
Last substantive review: 2026-09-20
Applicable versions: Current repository structure on the `develop` branch
Validation evidence: Markdown lint and local link validation must pass before publication
Known limitations: Templates are public-safe starting points; they are not installed tools or live MCP servers
Next review: Before merging `develop` into `main`

Use this hub when an improvement changes how the knowledge base is maintained, searched, validated, extended, or exposed to AI tools. Keep product-specific technical content in its normal topic area, and keep upgrade mechanics here.

## Upgrade areas

| Area | Use it for |
| --- | --- |
| [Features](features/README.md) | Search, navigation, feedback, evidence, and reader-experience improvements. |
| [Tools](tools/README.md) | Maintainer command catalogs, validation commands, generated indexes, and local automation ideas. |
| [Skills](skills/README.md) | Reusable AI-agent workflows for curation, ingestion, and evidence recording. |
| [MCP servers](mcp-servers/README.md) | Public-safe MCP server roles and configuration templates for read-only knowledge-base access. |
| [Instructions](instructions/README.md) | Branching, release, evidence, and upgrade workflows for this area. |
| [Upgrade agent guide](AGENTS.md) | Area-specific routing and safety rules for AI agents changing upgrade files. |

## Upgrade principles

| Principle | Rule |
| --- | --- |
| Documentation stays canonical | Markdown in Git remains the source of truth. Generated indexes, caches, and search data must be rebuildable. |
| Public-safe by default | Do not commit secrets, customer data, private infrastructure names, access tokens, or personal reader details. |
| Review before installation | Skill and MCP templates in this repository are documentation artifacts until a maintainer explicitly installs or connects them. |
| Prefer read-only serving | MCP servers and tools should start with search, fetch, index, validation, and reporting capabilities. Write paths need separate review. |
| Evidence stays visible | Pages should say whether content was source-reviewed, statically checked, locally executed, sandbox executed, or reader-tested. |
| Small upgrades beat platforms | Add one useful capability, validate it, index it, and only then expand. |

## Suggested implementation order

1. Review [feature backlog](features/feature-backlog.md) and choose one bounded upgrade.
2. Check whether a documented [tool](tools/tool-catalog.md), [skill](skills/README.md), or [MCP server template](mcp-servers/server-catalog.md) already covers the need.
3. Follow the [upgrade workflow](instructions/upgrade-workflow.md).
4. Record evidence using [evidence levels](instructions/evidence-levels.md).
5. Keep branch behavior aligned with [branching and release flow](instructions/branching-and-release-flow.md).
6. Update this hub, affected indexes, and [CHANGELOG.md](../CHANGELOG.md).

## Related links

- [AI tooling](../knowledge/ai/ai-tooling/index.md)
- [Agent knowledge bases](../knowledge/ai/ai-tooling/knowledge-bases/index.md)
- [AI agent router](../AGENTS.md)
- [AI agent context](../context.md)
- [Contributing](../CONTRIBUTING.md)
- [Back to root index](../README.md)
