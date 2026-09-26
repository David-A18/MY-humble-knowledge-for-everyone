# Knowledge-base MCP server catalog

## Purpose

Define MCP server roles that can improve knowledge-base access while keeping the Markdown repository authoritative and safe.

Status: Draft
Audience: Maintainers and AI agents designing MCP integrations
Page type: Server reference
Maintainer: Unassigned
Last substantive review: 2026-09-20
Applicable versions: Current repository structure on the `develop` branch
Validation evidence: Markdown lint and local link validation must pass before publication
Known limitations: Server roles are design templates, not installed services
Next review: Before implementing or connecting an MCP server

## Server roles

| Server role | Tools or resources | Write access | First use case |
| --- | --- | --- | --- |
| Filesystem read-only KB server | `list_routes`, `fetch_page`, `fetch_section` | No | Let an AI host read curated Markdown by path. |
| Search index server | `search_knowledge`, `list_aliases`, `explain_result` | No | Find likely pages without loading the whole repository. |
| GitHub documentation review server | `list_open_doc_issues`, `fetch_issue_context`, `list_recent_doc_commits` | No by default | Connect maintenance work to issue and commit context. |
| Validation status server | `latest_validation_summary`, `list_required_checks` | No | Show what checks protect a branch before merge. |
| Draft patch server | `propose_patch` | Yes, gated | Create reviewable diffs only after the read-only path is stable. |

## Minimum server contract

Every server proposal should document:

- Host and transport assumptions.
- Tool names, inputs, outputs, and error cases.
- Which repository paths the server can read.
- Whether the server can write, and how writes are reviewed.
- Secret handling and redaction rules.
- Local validation command or mock test.

## Related links

- [MCP server index](README.md)
- [Configuration templates](configs/README.md)
- [Tool catalog](../tools/tool-catalog.md)
- [Back to upgrade hub](../README.md)
- [Back to root index](../../README.md)
