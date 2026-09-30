---
type: Template
title: Knowledge article template
description: Start either a teaching-oriented explanation or a task-oriented how-to guide from a separate skeleton, with complete OKF metadata, evidence, and navigation.
tags: [templates, knowledge-article]
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
---

# Knowledge article template

> [!IMPORTANT]
> This file holds two separate skeletons. Copy **one** of them into a new file, then replace every frontmatter value and placeholder. Do not make one page serve both reader outcomes: an Explanation builds understanding, and a How-to Guide completes a task.

## Choose a skeleton

| The reader wants to | Use | Set `type` to |
| --- | --- | --- |
| Understand what something is, how its parts relate, and why it behaves as it does. | [Explanation skeleton](#explanation-skeleton) | `Explanation` |
| Complete one known task safely under stated conditions. | [How-to Guide skeleton](#how-to-guide-skeleton) | `How-to Guide` |

If a draft needs both, write two pages and link them to each other. The
teaching sequence and what each page type should leave out are defined in
[Teach for understanding](../../instructions.md#teach-for-understanding).

## Shared frontmatter

Both skeletons start with this frontmatter. Add `sources` when you cite real
official pages. Do not add `verified`, `generated`, or `stale_after` until the
review, generation, or freshness decision has actually happened.

```yaml
---
type: Explanation
title: Clear human-readable title
description: One sentence suitable for a search result or index entry.
tags: [topic, subtopic]
status: draft
maturity: initial-outline
audience: Who this page is written for
maintainer: unassigned
sources:
  - id: product-topic-page
    resource: https://example.com/official/specific-page
    title: Official page title
---
```

What it does: declares the required OKF profile fields and one source record.
The `id` is the key you reuse in footnotes. Replace the placeholder URL with
the specific official page that supports the claim, or remove `sources` if the
page cites nothing yet.

## Explanation skeleton

Use every section unless the note under it says it is optional. Keep commands
out; link to a how-to guide instead.

````markdown
# Title

## Purpose

What the reader will understand after this page, and what the page does not
cover.

## What it is

One or two plain sentences. Define each term before relying on it.

## Why it matters

The problem this solves, and what goes wrong when people misunderstand it.

## The mental model

The parts, how they relate, and what moves between them. A small table of
parts works well. Simplify by leaving detail out, never by stating something
false. Cite material claims.[^product-topic-page]

## An analogy

An original analogy in a few bullets.

Where the analogy stops being accurate:

- One break per bullet. Use each break to teach a true fact.

## Visual

Optional. Include a small Mermaid diagram only if it shows a flow, ownership
chain, or lifecycle that prose makes hard to see.

Text alternative: name the actors, the direction of flow, and the decision the
diagram helps the reader make.

## Example

One bounded example with realistic names, a clear start and end, and what
changes at each step. Say whether it is illustrative or was actually run. Do
not imply a test that did not happen.

## Common misconceptions

Optional. Short "people assume X; in fact Y" bullets.

## Check your understanding

- Two to four questions the reader should now be able to answer.

## Next steps

- Link the how-to, tutorial, or troubleshooting page that applies this model.

## Official documentation for deeper study

- What this link is for: [Specific official page](https://example.com/official/specific-page).

## Related links

- [Back to the parent index](index.md)

[^product-topic-page]: [Official page title](https://example.com/official/specific-page), source record `product-topic-page`.
````

## How-to Guide skeleton

Keep conceptual background to a sentence or two and link to the matching
Explanation. Do not add an analogy.

````markdown
# Title

## Purpose

The single task the reader will complete, and the situation in which this is
the right guide.

## Before you start

- Prerequisites: tools, versions, access, and permissions.
- Context to confirm: working directory, account, cluster, or environment.
- Background: link the Explanation that teaches the model this task relies on.

## Steps

Give dependency-ordered steps. Put a warning **before** any destructive,
expensive, credential-sensitive, or production-impacting action.

### 1. Name the step by its outcome

```bash
tool command --flag value
```

What it does: what the command reads, changes, or validates.

Expected result: the observable success condition.

If it fails: the first safe diagnostic, and when to stop.

## Verify the result

How the reader confirms the task is complete, using a read-only check.

## Recover or roll back

How to undo the change or return to a safe state, and what cannot be undone.

## Clean up

Optional. Remove anything the task created that should not remain.

## Related links

- [Matching explanation](explanation-page.md)
- [Official reference for the commands used](https://example.com/official/specific-page)
- [Back to the parent index](index.md)
````

## Evidence and freshness

- Cite official primary sources for material technical claims with keyed
  footnotes that match `sources[].id`.
- Record `stale_after` when the page is reviewed, not when it is drafted.
- Add a `verified` record only for a real review or execution event.
- Keep `status: draft` until the page has current evidence and an owner.

## Related links

- [Teach for understanding](../../instructions.md#teach-for-understanding)
- [Writing instructions](../../instructions.md)
- [Troubleshooting template](troubleshooting-template.md)
- [Command reference template](command-reference-template.md)
- [Back to templates index](index.md)
- [Back to knowledge index](../index.md)
