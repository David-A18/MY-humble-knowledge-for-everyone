# Evidence recorder

## Purpose

Use this skill when recording validation evidence, limitations, optional follow-ups, or publication status for knowledge-base changes.

## Evidence rules

- Say exactly what was checked.
- Record tool versions when they affect behavior.
- Separate Markdown validation from technical correctness.
- Do not claim live execution, reader testing, sandbox testing, or production validation unless it happened.
- Treat optional runtime and reader evidence as follow-ups when the documentation scope is already complete.
- Keep credentials, account IDs, private endpoints, customer data, and unnecessary reader details out of evidence records.

## Evidence levels

| Level | Meaning |
| --- | --- |
| Source-reviewed | Checked against official documentation or authoritative source material. |
| Statically checked | Syntax, schema, lint, link, or parser checks passed. |
| Locally executed | Commands were run in a local disposable environment. |
| Sandbox executed | Commands were run against an authorized non-production environment. |
| Reader-tested | Intended readers attempted tasks and anonymous outcomes were recorded. |

## Workflow

1. Locate the page, plan record, queue entry, or issue that needs evidence.
2. Add the evidence level and exact checks performed.
3. Add limitations close to the affected command, decision, or procedure.
4. Add optional follow-up links when stronger evidence can be collected later.
5. Update [CHANGELOG.md](../../../CHANGELOG.md) for meaningful validation or scope changes.
6. Run validation before finishing.

## Related links

- [Skill index](../README.md)
- [Evidence levels](../../instructions/evidence-levels.md)
- [External evidence request checklist](../../../external-evidence-request.md)
- [Back to root index](../../../README.md)
