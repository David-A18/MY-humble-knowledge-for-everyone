# Knowledge authoring instructions

## Choose the reader outcome

Use [Diátaxis](https://diataxis.fr/) to choose one primary job for each concept:

| OKF `type` | Reader outcome |
| --- | --- |
| `Tutorial` | A learner completes a bounded learning experience. |
| `How-to Guide` | A practitioner completes a specific task. |
| `Reference` | A reader finds accurate facts, commands, syntax, or limits. |
| `Explanation` | A reader understands concepts, relationships, and trade-offs. |
| `Troubleshooting Guide` | A reader moves from a symptom to diagnosis and safe recovery. |
| `Decision Record` | A maintainer understands a recorded decision and its consequences. |
| `Learning Path`, `Template`, `Glossary`, `Asset Guide` | A specialized repository resource. |

`Playbook`, `Attested Computation`, `Source Reference`, `Executor Reference`,
and `Attester Reference` are reserved for the embedded OKF example, where they
demonstrate the format's open vocabulary.

## Concept metadata

Use this frontmatter for every concept under `knowledge/`:

```yaml
---
type: How-to Guide
title: Clear human-readable title
description: One sentence suitable for a search result or index entry.
tags: [kubernetes, troubleshooting]
status: draft
maturity: initial-outline
audience: Engineering learners and practitioners
maintainer: unassigned
---
```

`maintainer` must be `unassigned`, `human:<handle>`, or `team:<name>`.
Use `status: stable` only when a page has current, recorded review evidence,
official `sources`, and `stale_after`. Keep draft content discoverable, but do
not present it as fully trusted guidance.
Do not add `generated`, `verified`, `sources`, or `stale_after` during a move or
mechanical edit. Add them when the stated evidence actually exists. Cite sources
for important technical claims with keyed Markdown footnotes linked to
`sources[].id`.

## Indexes, logs, and links

- Every knowledge directory has an `index.md` that lists its direct concepts and child directories.
- Only the bundle-root `knowledge/index.md` has frontmatter, and it contains only `okf_version: "0.2"`.
- `log.md` files use newest-first `## YYYY-MM-DD` headings.
- Use relative links that resolve in GitHub. Include a concise description beside each index link.
- Keep examples outside tables, explain what they do, and place risk warnings before risky actions.
- Keep indexes focused on navigation. Move a substantial tutorial, reference, or
  explanation into a named concept so people and agents can discover its metadata.
- Rebuild the generated catalog after changing concept metadata; do not edit it by hand.

## Licensing and citations

Write original prose. The contents of `knowledge/` are CC BY 4.0, but external
documentation remains subject to its own terms. Cite it as evidence and do not
copy it unless permission clearly allows that use.

## Required checks

Run the validation commands in [AGENTS.md](AGENTS.md) before committing.
