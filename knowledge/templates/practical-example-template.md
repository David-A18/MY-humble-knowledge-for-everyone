---
type: Template
title: Tutorial template
description: Copy a bounded learning exercise with a clear starting point, observable result, safe recovery, and next lesson.
tags: [templates, tutorial]
status: draft
maturity: draft
audience: Knowledge-base contributors
maintainer: unassigned
---

# Tutorial template

A Tutorial helps a beginner **learn by doing one bounded exercise**. It
is not a production runbook or a list of every command a tool offers.
Pick a disposable environment and one result the learner can see.

## Before you copy

- Choose the parent topic in the [knowledge index](../index.md). Check
  what the reader already needs to know and link its Explanation.
- Copy only the fenced skeleton below into a new lowercase kebab-case
  file. Replace every `REPLACE_WITH_` value. Change the parent-index
  link to the real parent.
- Keep `status: draft` unless real review evidence, official sources,
  and a freshness deadline support `stable`.
- If you did not run the exercise end to end, label it **Illustrative,
  not executed** and leave out `verified`. If you did run it, record
  the environment, steps, and observed result in the page; `verified`
  metadata alone cannot hold that detail.

## Copyable Tutorial skeleton

````markdown
---
type: Tutorial
title: "REPLACE_WITH_TUTORIAL_TITLE"
description: "REPLACE_WITH_ONE_SENTENCE_READER_OUTCOME"
tags: [REPLACE_WITH_TOPIC]
status: draft
maturity: initial-outline
audience: REPLACE_WITH_LEARNER_AUDIENCE
maintainer: unassigned
---

# REPLACE_WITH_TUTORIAL_TITLE

## What you will learn

REPLACE_WITH_PLAIN_DEFINITION_PURPOSE_AND_VISIBLE_RESULT

## Before you start

- Knowledge: REPLACE_WITH_PREREQUISITE_EXPLANATION_LINK.
- Tools and versions: REPLACE_WITH_CHECKED_PREREQUISITES.
- Place to work: REPLACE_WITH_DISPOSABLE_ENVIRONMENT.
- Access and cost: REPLACE_WITH_PERMISSIONS_LIMITS_AND_STOP_CONDITION.

REPLACE_WITH_ILLUSTRATIVE_OR_EXECUTED_LABEL_AND_EVIDENCE_NOTE

## 1. Confirm the starting point

REPLACE_WITH_READ_ONLY_CONTEXT_CHECK_AND_EXPECTED_RESULT

## 2. Create the small example

> [!WARNING]
> REPLACE_WITH_RISK_WARNING_OR_REMOVE_CALLOUT

```bash
REPLACE_WITH_EXERCISE_COMMAND
```

What it does: REPLACE_WITH_STATE_CHANGE.

Expected result: REPLACE_WITH_OBSERVABLE_SIGNAL.

If it fails: REPLACE_WITH_SAFE_CHECK_AND_STOP_CONDITION.

## 3. Inspect the result

REPLACE_WITH_READ_ONLY_VERIFICATION_AND_FAILURE_SIGNAL

## 4. Recover or reset

REPLACE_WITH_RECOVERY_STEPS_AND_IRREVERSIBLE_LIMIT

## Clean up

REPLACE_WITH_CLEANUP_WARNING_STEPS_AND_VERIFICATION

## Check your understanding

1. REPLACE_WITH_WHY_QUESTION
2. REPLACE_WITH_VERIFICATION_QUESTION

## Go deeper

- [Next lesson or practice task](REPLACE_WITH_NEXT_LEARNING_LINK.md)
- [Matching explanation](REPLACE_WITH_EXPLANATION_LINK.md)
- [Specific official documentation](https://REPLACE_WITH_OFFICIAL_SOURCE)
- [Back to parent index](index.md)
````

## Before you publish

Check that every placeholder is gone, the commands were verified or
clearly labelled illustrative, and the exercise has a recovery path.
List the new page in its parent `index.md`, rebuild the catalog, and run
the [required checks](../../AGENTS.md#validation-and-publication).
Record `sources`, `verified`, and `stale_after` only when the evidence
behind each field exists.

[Back to templates index](index.md) | [Back to knowledge index](../index.md)
