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
| `News Brief` | A reader learns what changed, why it matters, and what to do. Dated and expiring; see the [news editorial policy](governance/news-editorial-policy.md). |
| `Learning Path`, `Template`, `Glossary` | A specialized repository resource. |

## Write for everyone

The knowledge base is for learners and practitioners, so keep explanations
simple and useful:

- **Open with the answer.** Start each concept with two or three plain sentences
  that a newcomer can follow: what this is and when it matters.
- **Show, then explain.** Give a small, concrete example early, then explain
  what it does and why.
- **Use plain words.** Prefer short sentences and everyday words. Define each
  technical term the first time, or link to the [glossary](knowledge/glossary.md).
- **Keep it relevant.** Include only what serves the page's single reader
  outcome. Move tangents to their own concept and link to them.
- **Keep pages short.** Aim for under about 2,000 words. Split longer pages by
  reader task. Lookup pages such as the glossary may be longer.
- **Keep repository mechanics out of the explanation.** Put review dates,
  tested versions, and what was not tested in a final `## Evidence and limits`
  section, just before the related links. Validation records belong in
  metadata, logs, or [governance](governance/README.md).
- **Text only.** Use tables, lists, and Mermaid diagrams instead of images, and
  keep runnable files in [examples](examples/README.md). The
  [content policy](governance/content-policy.md) lists what is allowed.

## Concept metadata

Use this frontmatter for every concept under `knowledge/`:

```yaml
---
type: How-to Guide
title: Clear human-readable title
description: One sentence suitable for a search result or index entry.
tags: [kubernetes, troubleshooting]
status: draft
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
