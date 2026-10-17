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

## Teach for understanding

The knowledge base is a teaching hub. A beginner should leave a page with an
accurate mental model, then follow specific official documentation for deeper
study. Simplify by leaving detail out, never by stating something false.

For an Explanation, and for the conceptual opening of a foundational Tutorial
or Learning Path, include these elements in roughly this order:

1. **Simple definition.** One or two sentences in plain language. Define every
   term before relying on it.
2. **Why it matters.** The problem the subject solves and what goes wrong when
   people misunderstand it.
3. **Accurate mental model.** The parts, how they relate, and what moves
   between them. Prefer a small table or list of parts over a feature tour.
4. **Analogy with limitations.** An original analogy, followed by a list of
   the places where it breaks. Use each break to teach a true fact. Do not
   reuse the analogy an official source already uses; link to it instead.
5. **One bounded example.** Realistic names, a clear start and end, and what
   changes at each step. Label it as illustrative unless it was actually run,
   and never imply a runtime test that did not happen.
6. **Visual, only if it teaches a relationship.** Use a small Mermaid diagram
   for a flow, ownership chain, or lifecycle that prose alone makes hard to
   see. Skip decorative diagrams.
7. **Text alternative.** Directly after each diagram, name the actors, the
   direction of flow, and the decision the diagram helps the reader make.
8. **Official primary references.** Keyed footnotes for material claims, plus
   a short "deeper study" list placed after the practical explanation. Link
   the specific page that answers the next question, not only a product home
   page.
9. **Check your understanding and next step.** Two to four questions the
   reader should now be able to answer, and links to the how-to, tutorial, or
   troubleshooting page that applies the model.

Tailor the elements to the Diátaxis type instead of forcing every element onto
every page:

| Type | Required teaching elements | Usually omit |
| --- | --- | --- |
| `Explanation` | All nine; a common-misconceptions list is encouraged. | Step-by-step commands, which belong in a how-to guide. |
| `Tutorial` | Definition, why it matters, the tutorial itself as the bounded example, understanding checks, and next step. Link to the matching explanation for the model. | A long analogy; repeated conceptual background. |
| `How-to Guide` | Purpose, prerequisites, expected results, and a link to the explanation for the model. | Analogy; diagrams other than a decision flow. |
| `Troubleshooting Guide` | Symptom-first entry, safe first checks, and a link to the explanation. A small decision diagram can help. | Analogy. |
| `Reference` | Precise facts and a link to the explanation. | Analogy; narrative examples; diagrams unless they show structure. |
| `Glossary` | A one-sentence definition and a link to the canonical explanation. | Analogy, examples, and diagrams. |
| `Decision Record` | Context, decision, consequences, and reconsideration trigger. | Analogy; diagrams unless the decision changes an architecture. |
| `Learning Path` | Sequence, outcome per step, understanding checks, and next route. Put explanations before the tasks that depend on them. | Repeating the content of linked pages. |

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
The validator accepts `status: draft`, `stable`, or `deprecated`.
The validator accepts `maturity: initial-outline`, `draft`,
`maintained`, or `deprecated`. Use `initial-outline` for a new
skeleton; move to another value only when the page itself justifies it.
Use `status: stable` only when a page has current, recorded review evidence,
official `sources`, and `stale_after`. Keep draft content discoverable, but do
not present it as fully trusted guidance.
Do not add `generated`, `verified`, `sources`, or `stale_after` during a move or
mechanical edit. Add them when the stated evidence actually exists. Cite sources
for important technical claims with keyed Markdown footnotes linked to
`sources[].id`.
The copyable templates mark values to replace with `REPLACE_WITH_`.
The OKF validator rejects that marker in concept frontmatter. Search
the newly copied page for markers in its body and for example URLs
before publication; no placeholder is evidence of a real source or run.

When evidence exists, the metadata shapes are:

```yaml
sources:
  - id: REPLACE_WITH_KEBAB_CASE_SOURCE_ID
    resource: https://REPLACE_WITH_SPECIFIC_OFFICIAL_PAGE
    title: REPLACE_WITH_SOURCE_TITLE
verified:
  - by: REPLACE_WITH_REAL_ACTOR
    at: null # replace with the real ISO date or omit verified
stale_after: null # replace with a decided ISO deadline or omit
```

Add only the fields supported by the actual work. `verified` names the
actor and time; it does not describe the environment, commands, or
result. Put that evidence in the page body or a linked record instead
of implying the metadata alone proves an execution or review.

## Indexes, logs, and links

- Every knowledge directory has an `index.md` that lists its direct concepts and child directories.
- Only the bundle-root `knowledge/index.md` has frontmatter, and it contains only `okf_version: "0.2"`.
- `log.md` files use newest-first `## YYYY-MM-DD` headings.
- Use relative links that resolve in GitHub. Include a concise description beside each index link.
- Link a reader's return to the knowledge home to `knowledge/index.md`, using
  the correct relative path. Link the repository `README.md` only when the
  reader needs repository setup or governance outside the published bundle.
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
