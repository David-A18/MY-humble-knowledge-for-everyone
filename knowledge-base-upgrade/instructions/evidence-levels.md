# Evidence levels for knowledge-base upgrades

## Purpose

Use consistent labels for what was verified when changing documentation, tools, skills, MCP templates, or operating instructions.

Status: Draft
Audience: Maintainers and AI agents recording validation evidence
Page type: Reference
Maintainer: Unassigned
Last substantive review: 2026-09-20
Applicable versions: Current repository structure on the `develop` branch
Validation evidence: Markdown lint and local link validation must pass before publication
Known limitations: Evidence labels describe confidence; they do not remove the need for reader judgment
Next review: When validation policy changes

## Evidence labels

| Label | Use when | Do not claim |
| --- | --- | --- |
| Source-reviewed | Official docs or authoritative sources were checked. | That commands were executed. |
| Statically checked | Linters, parsers, schema checks, or link validators passed. | That runtime behavior is correct. |
| Locally executed | Commands ran in a local disposable environment. | That cloud or production behavior was tested. |
| Sandbox executed | Commands ran in an authorized non-production environment. | That production behavior or customer systems were tested. |
| Reader-tested | Intended readers attempted tasks and anonymous outcomes were recorded. | That every future reader will succeed. |
| Template-reviewed | A config, skill, or workflow template was checked for safety and consistency. | That the template is installed or connected. |

## Recording pattern

Use this shape in operational pages when evidence matters:

```text
Validation evidence: Source-reviewed against official documentation; Markdown lint and local link validation passed. Runtime execution is optional follow-up evidence and has not been claimed.
Known limitations: The MCP configuration is a placeholder template and is not connected to a live host.
```

What it does: makes the confidence level clear without overstating what was tested.

## Related links

- [Instruction index](README.md)
- [Evidence recorder skill](../skills/evidence-recorder/SKILL.md)
- [External evidence request checklist](../../external-evidence-request.md)
- [Back to upgrade hub](../README.md)
- [Back to root index](../../README.md)
