# Knowledge curator

## Purpose

Use this skill when improving an existing knowledge-base article or adding a focused article from verified context.

## Workflow

1. Read the root [AI agent router](../../../AGENTS.md), [context](../../../context.md), [instructions](../../../instructions.md), and [contributing guide](../../../CONTRIBUTING.md).
2. Identify the closest parent index and related articles with `rg`.
3. Decide whether to update an existing page or add a focused page using the nearest template.
4. Add practical content: purpose, prerequisites, decisions, commands, expected outputs, failure modes, and related links.
5. Keep examples outside tables and place warnings near risky commands.
6. Update parent indexes, related links, glossary entries, route maps, and changelog entries when affected.
7. Record the actual evidence level: source-reviewed, statically checked, locally executed, sandbox executed, or reader-tested.
8. Run the required validation checks before finishing.

## Output standard

A completed curation task should leave the repository with:

- A focused page or precise edit in the correct route.
- Working relative links from the parent index and related pages.
- A visible review-information block when the page is operational or substantially reviewed.
- No secrets, private infrastructure details, or unverified claims.
- Validation results recorded in the final handoff or plan record.

## Related links

- [Skill index](../README.md)
- [Knowledge-base upgrade hub](../../README.md)
- [Back to root index](../../../README.md)
