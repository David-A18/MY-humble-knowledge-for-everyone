---
type: Template
title: Architecture decision record template
description: Copy a decision record that separates decision state from document maturity and preserves rationale, consequences, and a reconsideration trigger.
tags: [templates, decision-record]
status: draft
maturity: draft
audience: Knowledge-base contributors
maintainer: unassigned
---

# Architecture decision record template

A Decision Record explains **why a choice was made**, what it changes,
and when it should be revisited. Its decision state is separate from the
OKF `status` of the page: an accepted decision can still be a draft
article awaiting review.

## Before you copy

Copy only the fenced skeleton into a new lowercase kebab-case file.
Replace every `REPLACE_WITH_` value.
Use one decision per record. Set the body decision state to `Proposed`,
`Accepted`, `Accepted with part superseded`, `Superseded by ADR-NNNN`,
or `Deprecated`; link the replacing record when any part is superseded.
Name the new file `adr-REPLACE_WITH_NUMBER-short-decision-name.md`.
Use a real decision
date if known, and leave it
out rather than guess. Leave `maintainer: unassigned` until a person or
team agrees to own the record.

## Copyable Decision Record skeleton

````markdown
---
type: Decision Record
title: "ADR-REPLACE_WITH_NUMBER: REPLACE_WITH_DECISION_TITLE"
description: "REPLACE_WITH_ONE_SENTENCE_CHOICE_AND_REASON"
tags: [decision-records, REPLACE_WITH_TOPIC]
status: draft
maturity: initial-outline
audience: REPLACE_WITH_READER_AUDIENCE
maintainer: unassigned
---

# ADR-REPLACE_WITH_NUMBER: REPLACE_WITH_DECISION_TITLE

## Decision state

REPLACE_WITH_DECISION_STATE_AND_KNOWN_DATE_IF_ANY

## In plain terms

REPLACE_WITH_ONE_SENTENCE_PLAIN_SUMMARY

## Context

REPLACE_WITH_PROBLEM_CONSTRAINTS_EVIDENCE_AND_AFFECTED_READERS

## Decision

REPLACE_WITH_CHOICE_SCOPE_AND_RESULT_WITHOUT_INVENTED_REVIEWER

## Options considered

| Option | Benefit | Cost or risk |
| --- | --- | --- |
| REPLACE_WITH_OPTION_A | REPLACE_WITH_BENEFIT_A | REPLACE_WITH_TRADEOFF_A |
| REPLACE_WITH_OPTION_B | REPLACE_WITH_BENEFIT_B | REPLACE_WITH_TRADEOFF_B |

## Consequences

- REPLACE_WITH_EXPECTED_IMPROVEMENT.
- REPLACE_WITH_ACCEPTED_COST.
- REPLACE_WITH_FOLLOWUP_AND_AGREED_OWNER_OR_UNASSIGNED.

## Reconsider when

REPLACE_WITH_OBSERVABLE_RECONSIDERATION_TRIGGER

## Evidence and limitations

REPLACE_WITH_REAL_EVIDENCE_AND_UNTESTED_LIMITS

## Related links

- [Parent decision index](index.md)
- [Replacing decision](REPLACE_WITH_REPLACING_ADR_LINK.md) or remove
  this line if the decision remains active.
- [Back to knowledge index](../index.md)
````

## Before you publish

Replace every placeholder. Link the record from its parent `index.md`,
rebuild the catalog, and run the [required
checks](../../AGENTS.md#validation-and-publication). If a new decision
supersedes an old one, update **both** records and the index. Preserve
the old rationale as history; do not make it look like current policy.

[Back to templates index](index.md) | [Back to knowledge index](../index.md)
