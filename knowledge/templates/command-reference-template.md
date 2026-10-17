---
type: Template
title: Command reference template
description: Copy a scoped command lookup with version, context, side effects, expected results, and official command sources.
tags: [templates, command-reference]
status: draft
maturity: draft
audience: Knowledge-base contributors
maintainer: unassigned
---

# Command reference template

A Reference helps a reader **look up a precise command or option**.
Keep the scope narrow and consistent. Put a task journey in a How-to
Guide and the underlying model in an Explanation.

## Before you copy

Copy only the fenced skeleton into a new lowercase kebab-case file.
Replace every `REPLACE_WITH_` value.
Check the tool version against official documentation; do not guess
that a command works in older or newer releases. State whether an
output is captured from a real run or illustrative.

## Copyable Reference skeleton

````markdown
---
type: Reference
title: "REPLACE_WITH_COMMAND_FAMILY_TITLE"
description: "REPLACE_WITH_ONE_SENTENCE_LOOKUP_SCOPE"
tags: [REPLACE_WITH_TOPIC, commands]
status: draft
maturity: initial-outline
audience: REPLACE_WITH_READER_AUDIENCE
maintainer: unassigned
---

# REPLACE_WITH_COMMAND_FAMILY_TITLE

## Scope

REPLACE_WITH_TOOL_COMMAND_FAMILY_PLATFORM_AND_CHECKED_VERSION

Read the [matching Explanation](REPLACE_WITH_EXPLANATION_LINK.md)
first if these commands are unfamiliar.

## Context before commands

- Required access: REPLACE_WITH_ROLES_AND_PERMISSIONS.
- Target: REPLACE_WITH_CONTEXT_TO_CHECK.
- Stop if: REPLACE_WITH_UNSAFE_CONDITION.

## Quick lookup

| Need | Detail below | Changes state? | Success signal |
| --- | --- | --- | --- |
| REPLACE_WITH_LOOKUP_NEED | REPLACE_WITH_COMMAND_NAME | REPLACE_WITH_YES_OR_NO | REPLACE_WITH_SUCCESS_SIGNAL |

## Command details

### REPLACE_WITH_COMMAND_NAME

Use when: REPLACE_WITH_EXACT_CONDITION_AND_VERSION.

> [!WARNING]
> REPLACE_WITH_SIDE_EFFECT_AND_REVIEW_OR_REMOVE_CALLOUT

```bash
REPLACE_WITH_COMMAND_AND_SAFE_PLACEHOLDERS
```

Inputs: REPLACE_WITH_FLAGS_PATHS_PERMISSIONS_AND_DEFAULTS.

Expected result: REPLACE_WITH_REAL_OUTPUT_OR_LABELLED_ILLUSTRATIVE_INVARIANT.

Failure signal: REPLACE_WITH_READ_ONLY_DIAGNOSTIC_OR_TROUBLESHOOTING_LINK.

Undo or recovery: REPLACE_WITH_REVERSAL_OR_IRREVERSIBLE_LIMIT.

## Official command documentation

- [Specific official command page](https://REPLACE_WITH_OFFICIAL_SOURCE)
  for the syntax and version described above.

## Related links

- [Matching Explanation](REPLACE_WITH_EXPLANATION_LINK.md)
- [Troubleshooting or How-to Guide](REPLACE_WITH_RELATED_LINK.md)
- [Back to parent index](index.md)
````

## Before you publish

Replace every placeholder. Link specific official command pages and
add matching `sources` records only after checking them. Record
`verified` for a real run, not for illustrative output. Put warnings
before commands with side effects. List the page in its parent
`index.md`, rebuild the catalog, and run the [required
checks](../../AGENTS.md#validation-and-publication).

[Back to templates index](index.md) | [Back to knowledge index](../index.md)
