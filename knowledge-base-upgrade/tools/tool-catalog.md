# Knowledge-base upgrade tool catalog

## Purpose

List small tools that can improve the knowledge base without replacing the Markdown repository as the source of truth.

Status: Draft
Audience: Maintainers choosing implementation work
Page type: Tool reference
Maintainer: Unassigned
Last substantive review: 2026-09-20
Applicable versions: Current repository structure on the `develop` branch
Validation evidence: Markdown lint and local link validation must pass before publication
Known limitations: Proposed tools need implementation and tests before use in CI
Next review: Before adding or changing maintained scripts

## Tool candidates

| Tool | Type | First implementation | Safe default |
| --- | --- | --- | --- |
| Search index builder | Local script | Parse Markdown titles, headings, review blocks, and related links into JSON. | Read-only, deterministic, excludes ignored source archives. |
| Alias checker | Local script | Validate that high-demand aliases route to existing pages. | Fails on missing local targets or duplicate aliases. |
| Evidence registry builder | Local script | Extract review-information blocks into a single table. | Reports missing evidence instead of editing pages. |
| Stale-page reporter | Local script or CI job | Compare `Next review` dates to the current date. | Warns first; does not fail CI until policy is explicit. |
| Source-intake classifier | Skill plus script | Suggest target section from raw note metadata and keywords. | Suggests only; human or maintainer approves moves. |
| Link graph reporter | Local script | Show orphaned pages, deep pages, and missing parent links. | Reports only; no automatic rewrites. |
| MCP read-only server | MCP server | Expose `search_knowledge`, `fetch_page`, and `list_routes`. | No write tools, no shell execution, no secrets. |

## Implementation checklist

- Add the tool under `scripts/` only after the behavior is clear enough to test.
- Add fixture tests when the tool enforces repository policy.
- Document inputs, outputs, ignored paths, and failure modes.
- Update [validation command matrix](validation-command-matrix.md) when the tool becomes a required check.
- Update [context.md](../../context.md) if the tool becomes part of the route map or validation workflow.

## Related links

- [Tools index](README.md)
- [Validation command matrix](validation-command-matrix.md)
- [Feature backlog](../features/feature-backlog.md)
- [Back to upgrade hub](../README.md)
- [Back to root index](../../README.md)
