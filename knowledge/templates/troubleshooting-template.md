---
type: Template
title: Troubleshooting guide template
description: Copy a symptom-led guide that separates safe evidence gathering, likely causes, recovery, and escalation.
tags: [templates, troubleshooting]
status: draft
maturity: draft
audience: Knowledge-base contributors
maintainer: unassigned
---

# Troubleshooting guide template

A Troubleshooting Guide starts with a **symptom the reader can observe**.
It should help the reader narrow causes with read-only checks before
any recovery command changes state.

## Before you copy

Copy only the fenced skeleton into a new lowercase kebab-case file.
Replace each `REPLACE_WITH_` value. Use a real error string when there
is one, and link the Explanation of the system boundary involved.
Repeat the cause and its recovery block together for each distinct
failure cause, so a fix cannot be mistaken for another cause's fix.

## Copyable Troubleshooting Guide skeleton

````markdown
---
type: Troubleshooting Guide
title: "REPLACE_WITH_SYMPTOM_TITLE"
description: "REPLACE_WITH_ONE_SENTENCE_DIAGNOSIS_OUTCOME"
tags: [REPLACE_WITH_TOPIC, troubleshooting]
status: draft
maturity: initial-outline
audience: REPLACE_WITH_OPERATOR_AUDIENCE
maintainer: unassigned
---

# REPLACE_WITH_SYMPTOM_TITLE

## Symptom and scope

REPLACE_WITH_VISIBLE_SYMPTOM_SCOPE_AND_EXACT_ERROR_TEXT

## Before changing anything

1. Confirm the account, cluster, project, or working directory.
2. Save the exact error, time, and affected resource names.
3. Note recent changes and whether a known-good copy exists.
4. Stop if these checks would expose secrets or touch another user's
   production system without authorization.

## Follow the evidence

| Observation | Next check |
| --- | --- |
| REPLACE_WITH_SYMPTOM_A | REPLACE_WITH_READ_ONLY_CHECK_A |
| REPLACE_WITH_SYMPTOM_B | REPLACE_WITH_READ_ONLY_CHECK_B |

### Possible cause: REPLACE_WITH_CAUSE

```bash
REPLACE_WITH_READ_ONLY_DIAGNOSTIC
```

What it reads: REPLACE_WITH_EVIDENCE_SOURCE.

Confirms this cause when: REPLACE_WITH_CONFIRMING_RESULT.

Rules it out when: REPLACE_WITH_RULE_OUT_RESULT.

If confirmed, consider the recovery for **this cause** below. If not,
move to the next cause or stop when the evidence is insufficient.

### Recover this cause only

> [!WARNING]
> REPLACE_WITH_SIDE_EFFECTS_DATA_RISK_AND_REQUIRED_APPROVAL

REPLACE_WITH_ILLUSTRATIVE_OR_EXECUTED_LABEL_AND_EVIDENCE_NOTE

```bash
REPLACE_WITH_RECOVERY_COMMAND
```

Expected result: REPLACE_WITH_SUCCESS_SIGNAL.

If it fails: REPLACE_WITH_SAFE_CHECK_AND_ESCALATION.

Undo or rollback: REPLACE_WITH_REVERSAL_OR_IRREVERSIBLE_LIMIT.

## Verify the real outcome

REPLACE_WITH_READ_ONLY_SYSTEM_AND_APPLICATION_CHECK

## Stop and escalate when

- REPLACE_WITH_EVIDENCE_GAP_OR_RISK_THAT_REQUIRES_ESCALATION.
- REPLACE_WITH_LOGS_STATUS_AND_RECENT_CHANGES_WITHOUT_CREDENTIALS.

## Prevent recurrence

REPLACE_WITH_PREVENTION_STEP_OR_REMOVE_SECTION_IF_CAUSE_UNKNOWN

## Related learning and official documentation

- [Explanation of the affected system](REPLACE_WITH_EXPLANATION_LINK.md)
- [Specific official troubleshooting page](https://REPLACE_WITH_OFFICIAL_SOURCE)
- [Back to parent index](index.md)
````

## Before you publish

Replace every placeholder. Put warnings before risky actions, label
unrun recovery examples **Illustrative, not executed**, and use real
sources for product-specific claims. Add `verified` or `stale_after`
only after the relevant work and review happened. List the page in its
parent `index.md`, rebuild the catalog, and run the [required
checks](../../AGENTS.md#validation-and-publication).

[Back to templates index](index.md) | [Back to knowledge index](../index.md)
