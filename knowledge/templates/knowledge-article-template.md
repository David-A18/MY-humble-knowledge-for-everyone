---
type: Template
title: Knowledge article template
description: Start either a teaching-oriented explanation or a task-oriented how-to guide from a separate skeleton, with complete OKF metadata, evidence, and navigation.
tags: [templates, knowledge-article]
status: draft
maturity: draft
audience: Knowledge-base contributors
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

## Metadata and evidence

Each block below includes its own complete frontmatter. Copy **only
one block** and replace all `REPLACE_WITH_` values. Add `sources` only
after you open a real official page that supports a claim; give it a
stable `id` and cite the same ID in a footnote. Do not add `verified`,
`generated`, or `stale_after` until the work behind each field really
happened.

## Explanation skeleton

Use every section unless the note under it says it is optional. Keep commands
out; link to a how-to guide instead.
If you remove the optional Visual section, remove its text alternative too.

````markdown
---
type: Explanation
title: "REPLACE_WITH_CLEAR_TITLE"
description: "REPLACE_WITH_ONE_SENTENCE_READER_OUTCOME"
tags: [REPLACE_WITH_TOPIC]
status: draft
maturity: initial-outline
audience: REPLACE_WITH_READER_AUDIENCE
maintainer: unassigned
---

# REPLACE_WITH_CLEAR_TITLE

## Purpose

REPLACE_WITH_READER_OUTCOME_AND_SCOPE

## What it is

REPLACE_WITH_ONE_OR_TWO_SENTENCE_DEFINITION

## Terms used

REPLACE_WITH_NEEDED_TERMS_OR_REMOVE_SECTION

## Why it matters

REPLACE_WITH_PROBLEM_AND_COST_OF_MISUNDERSTANDING

## The mental model

REPLACE_WITH_ACCURATE_PARTS_RELATIONSHIPS_AND_REAL_SOURCE_FOOTNOTES

## An analogy

REPLACE_WITH_ORIGINAL_ANALOGY

Where the analogy stops being accurate:

- REPLACE_WITH_ANALOGY_LIMIT_AND_TRUE_FACT.

## Example

REPLACE_WITH_BOUNDED_EXAMPLE_AND_ILLUSTRATIVE_OR_EXECUTED_LABEL

## Visual

REPLACE_WITH_SMALL_TEACHING_DIAGRAM_OR_REMOVE_SECTION

Text alternative: REPLACE_WITH_ACTORS_FLOW_AND_READER_DECISION.

## Common misconceptions

REPLACE_WITH_CONCRETE_MISCONCEPTION_OR_REMOVE_SECTION

## Check your understanding

- REPLACE_WITH_TWO_TO_FOUR_QUESTIONS.

## Next steps

- REPLACE_WITH_RELATED_TASK_OR_DIAGNOSIS_LINK.

## Official documentation for deeper study

- REPLACE_WITH_WHAT_THIS_SOURCE_ANSWERS: [Specific official page](https://REPLACE_WITH_OFFICIAL_SOURCE).

## Related links

- [Back to the parent index](index.md)

REPLACE_WITH_KEYED_FOOTNOTES_FOR_REAL_SOURCES_OR_REMOVE_LINE
````

## How-to Guide skeleton

Keep conceptual background to a sentence or two and link to the matching
Explanation. Do not add an analogy.

````markdown
---
type: How-to Guide
title: "REPLACE_WITH_CLEAR_TITLE"
description: "REPLACE_WITH_ONE_SENTENCE_TASK_OUTCOME"
tags: [REPLACE_WITH_TOPIC]
status: draft
maturity: initial-outline
audience: REPLACE_WITH_READER_AUDIENCE
maintainer: unassigned
---

# REPLACE_WITH_CLEAR_TITLE

## Purpose

REPLACE_WITH_SINGLE_TASK_EXPECTED_OUTCOME_AND_USE_CONDITION

## Before you start

- Prerequisites: REPLACE_WITH_CHECKED_TOOLS_VERSIONS_ACCESS_AND_PERMISSIONS.
- Context to confirm: REPLACE_WITH_WORKING_DIRECTORY_ACCOUNT_OR_CLUSTER.
- Stop if: REPLACE_WITH_UNSAFE_CONDITION.
- Background: [Matching Explanation](REPLACE_WITH_EXPLANATION_LINK.md).

REPLACE_WITH_ILLUSTRATIVE_OR_EXECUTED_LABEL_AND_EVIDENCE_NOTE

## Steps

REPLACE_WITH_DEPENDENCY_ORDERED_STEPS

### 1. REPLACE_WITH_STEP_OUTCOME

> [!WARNING]
> REPLACE_WITH_RISK_WARNING_OR_REMOVE_CALLOUT

```bash
REPLACE_WITH_SAFE_COMMAND
```

What it does: REPLACE_WITH_READ_CHANGE_OR_VALIDATION.

Expected result: REPLACE_WITH_OBSERVABLE_SUCCESS_CONDITION.

If it fails: REPLACE_WITH_SAFE_DIAGNOSTIC_AND_STOP_CONDITION.

## Verify the result

REPLACE_WITH_READ_ONLY_VERIFICATION

## Recover or roll back

REPLACE_WITH_ROLLBACK_AND_IRREVERSIBLE_LIMIT

## Clean up

REPLACE_WITH_CLEANUP_AND_CHECK_OR_REMOVE_SECTION

## Related links

- [Matching explanation](REPLACE_WITH_EXPLANATION_LINK.md)
- [Official reference for the commands used](https://REPLACE_WITH_OFFICIAL_SOURCE)
- [Back to the parent index](index.md)
````

## Evidence and freshness

- Cite official primary sources for material technical claims with keyed
  footnotes that match `sources[].id`.
- Record `stale_after` when the page is reviewed, not when it is drafted.
- Add a `verified` record only for a real review or execution event.
- Keep `status: draft` until the page has real review evidence, current
  official sources, and a decided freshness deadline.

## Before you publish

Replace every `REPLACE_WITH_` marker and instruction prompt, including
link targets. Check that terms are defined before use, warnings appear
before risky commands, and examples are labelled illustrative unless
actually run. List the page in its parent `index.md`, rebuild the
catalog, and run the [required
checks](../../AGENTS.md#validation-and-publication).

## Related links

- [Teach for understanding](../../instructions.md#teach-for-understanding)
- [Writing instructions](../../instructions.md)
- [Troubleshooting template](troubleshooting-template.md)
- [Command reference template](command-reference-template.md)
- [Back to templates index](index.md)
- [Back to knowledge index](../index.md)
