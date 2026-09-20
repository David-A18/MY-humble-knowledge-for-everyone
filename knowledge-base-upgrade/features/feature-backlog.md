# Knowledge-base upgrade feature backlog

## Purpose

Prioritize improvements that make the knowledge base easier to search, maintain, validate, and reuse with AI tools.

Status: Draft
Audience: Maintainers and contributors selecting upgrade work
Page type: Planning backlog
Maintainer: Unassigned
Last substantive review: 2026-09-20
Applicable versions: Current repository structure on the `develop` branch
Validation evidence: Markdown lint and local link validation must pass before publication
Known limitations: Items are proposals until implemented and validated
Next review: Before merging `develop` into `main`

## Feature candidates

| ID | Feature | Reader or maintainer outcome | First useful deliverable | Evidence needed |
| --- | --- | --- | --- | --- |
| KBU-F01 | Searchable local index | Readers can find guides by topic, command, provider, and task phrase. | Static JSON search index generated from Markdown headings, titles, and related links. | Local generation test and query examples. |
| KBU-F02 | Evidence registry | Maintainers can see source-reviewed, static-checked, locally executed, sandbox-executed, and reader-tested pages in one place. | Generated or manually maintained evidence table. | Link validation plus spot checks against article review blocks. |
| KBU-F03 | Topic alias map | Common names, acronyms, tools, and provider names route to canonical pages. | `aliases.yml` or Markdown alias table linked from the root index. | Search tests for high-demand terms. |
| KBU-F04 | Reader feedback intake | Readers can report missing prerequisites, confusing terms, and broken examples without leaking private data. | Issue form refinements and contributor triage guide. | Issue-template validation and privacy review. |
| KBU-F05 | MCP read-only adapter | AI agents can search and fetch curated public knowledge without direct write access. | Public-safe server template with `search`, `fetch`, and `list_routes` tools. | Config review and local mock test. |
| KBU-F06 | Skill pack for maintainers | AI agents can follow repeatable workflows for curation, source ingestion, and evidence recording. | Reviewed skill files under [skills](../skills/README.md). | Markdown lint and dry-run review against sample pages. |
| KBU-F07 | Release checklist dashboard | Maintainers can see what must be validated before merging `develop` to `main`. | Checklist page or generated report. | Local validation and CI status evidence. |
| KBU-F08 | Source freshness queue | Fast-changing topics have review triggers tied to upstream versions or dates. | Queue entries linked from priority operational guides. | Source review dates and official-reference links. |

## Prioritization guide

1. Choose the smallest feature that improves findability, safety, or maintenance effort.
2. Prefer features that reuse current Markdown, indexes, and validation scripts.
3. Avoid adding a database, service, or runtime dependency until a static file or script cannot solve the problem.
4. Keep generated artifacts out of the repository unless they are intentionally versioned and easy to rebuild.
5. Record implementation evidence in [CHANGELOG.md](../../CHANGELOG.md) and the affected feature row.

## Related links

- [Features index](README.md)
- [Tool catalog](../tools/tool-catalog.md)
- [MCP server catalog](../mcp-servers/server-catalog.md)
- [Upgrade workflow](../instructions/upgrade-workflow.md)
- [Back to upgrade hub](../README.md)
- [Back to root index](../../README.md)
