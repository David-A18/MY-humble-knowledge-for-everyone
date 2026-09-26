# Knowledge-base upgrade agent guide

Use this file when changing files under `knowledge-base-upgrade/`.

## Scope

This area documents how to improve the knowledge base itself. It can contain proposed features, maintainer tools, reusable skill packages, MCP server configuration templates, and upgrade instructions.

## Rules

- Keep upgrade files public-safe and reviewable.
- Treat skill packages and MCP templates as documentation artifacts until a maintainer installs them outside the repository.
- Do not add real tokens, account IDs, private endpoints, private repository names, customer data, or personal reader details.
- Prefer read-only tool and MCP capabilities before write-capable workflows.
- Link every new page from the nearest `README.md` and back to the upgrade hub.
- Record validation evidence and limitations in the page body when the page describes a tool, skill, or MCP configuration.
- Update [../README.md](../README.md), [../context.md](../context.md), [../AGENTS.md](../AGENTS.md), and [../CHANGELOG.md](../CHANGELOG.md) when routes or operating rules change.

## Validation

Before finishing, run the repository checks required by [../AGENTS.md](../AGENTS.md). At minimum, run Markdown lint, local link validation, issue-template validation, and `git diff --check` when those tools are available.

[Back to upgrade hub](README.md)
