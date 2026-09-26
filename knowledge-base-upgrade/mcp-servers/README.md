# Knowledge-base MCP servers

## Purpose

Document public-safe MCP server roles and configuration templates that could expose this knowledge base to AI hosts.

Status: Draft
Audience: Maintainers evaluating agent-facing access to the knowledge base
Page type: MCP server index
Maintainer: Unassigned
Last substantive review: 2026-09-20
Applicable versions: Current repository structure on the `develop` branch
Validation evidence: Markdown lint and local link validation must pass before publication
Known limitations: Config files are templates only and are not connected to live hosts by this repository
Next review: Before connecting any MCP server to a real host

## MCP server index

| Guide | Use it for |
| --- | --- |
| [Server catalog](server-catalog.md) | Choose safe MCP server roles for knowledge-base access. |
| [Configuration templates](configs/README.md) | Review placeholder JSONC config templates for read-only filesystem, GitHub review, and search-index adapters. |

## Safety baseline

Start with read-only operations:

- List routes and indexes.
- Search Markdown headings and aliases.
- Fetch a page or section by path.
- Report validation status from checked-in evidence.

Avoid write tools until the repository has a documented approval, audit, and rollback path.

## Related links

- [Knowledge-base upgrade hub](../README.md)
- [Model Context Protocol guide](../../knowledge/ai/ai-tooling/model-context-protocol.md)
- [MCP configuration templates](configs/README.md)
- [Back to root index](../../README.md)
