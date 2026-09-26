# MCP configuration templates

## Purpose

Store placeholder MCP configuration templates for knowledge-base access patterns.

Status: Draft
Audience: Maintainers reviewing MCP connection shapes
Page type: Configuration index
Maintainer: Unassigned
Last substantive review: 2026-09-20
Applicable versions: Current repository structure on the `develop` branch
Validation evidence: Markdown lint and local link validation must pass before publication
Known limitations: Templates contain placeholders and are not usable until adapted to a specific host and reviewed
Next review: Before connecting any MCP server to a real host

## Templates

| Template | Use it for |
| --- | --- |
| [Filesystem read-only](filesystem-readonly.jsonc) | Expose checked-out Markdown files to a local MCP host without write access. |
| [GitHub docs review](github-docs-review.jsonc) | Read documentation issues and repository metadata through a GitHub-backed MCP server. |
| [Search index](search-index.jsonc) | Serve a generated local search index as a read-only MCP resource. |

## Template rules

- Replace placeholder paths and command names only after reviewing the target host documentation.
- Keep credentials in the host secret store or environment, not in committed files.
- Prefer read-only tools first.
- Record the exact installed server version outside this template before using it for evidence.

## Related links

- [MCP server index](../README.md)
- [Server catalog](../server-catalog.md)
- [Knowledge-base upgrade hub](../../README.md)
- [Back to root index](../../../README.md)
