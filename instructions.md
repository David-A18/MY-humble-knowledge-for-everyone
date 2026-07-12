# AI documentation instructions

Use this file when creating or refactoring documentation in this repository. The goal is to make every page easy to scan, easy to understand, and practical for readers with different experience levels.

## Core writing standard

- Write for people who may be learning the topic for the first time but want professional habits.
- Prefer clear explanations over dense reference dumps.
- Use short sections with descriptive headings.
- Keep tables narrow and readable on GitHub.
- Put examples outside tables so command usage is visually obvious.
- Explain what each example does immediately after the code block.
- Warn clearly before destructive, irreversible, expensive, or history-rewriting operations.
- Prefer official documentation links for technical references.
- Keep internal links relative.

## Recommended article structure

Use this structure for most focused knowledge articles:

````markdown
# Clear article title

## Purpose

Explain what the page helps the reader do.

## Topic or workflow group

| Task | Command or concept | When to use it |
| --- | --- | --- |
| Short task | `tool command` | Practical situation. |

### Example title

```bash
tool command --flag value
```

What it does: explain the command in plain language.

> [!WARNING]
> Add risk notes near risky examples, not hidden in a huge table.

## Related links

- Back to parent index: README.md
- Back to root index: ../README.md
````

Adjust the bottom navigation path for the article location.

## Tables

Use tables for scanning and comparison, not for full explanations.

Good table columns:

| Use case | Good columns |
| --- | --- |
| Command references | `Task`, `Command`, `When to use it` |
| Concept comparisons | `Concept`, `Meaning`, `Why it matters` |
| Troubleshooting | `Symptom`, `Check`, `Likely cause` |
| Catalogs | `Command`, `Use`, `Notes` |
| Decision guides | `Situation`, `Choose`, `Reason` |

Avoid wide tables with many long text columns. Do not put command examples, long explanations, and risk notes all in the same table row.

## Examples

Every important command or workflow should have an example outside the table.

Use this pattern:

````markdown
### Stage selected changes

```bash
git add -p README.md
```

What it does: lets you choose individual hunks so the next commit stays focused.
````

For multi-step workflows:

````markdown
### Start a feature branch

```bash
git fetch --all --prune
git switch main
git pull --ff-only
git switch -c feature/descriptive-name
```

What it does: updates remote knowledge, fast-forwards the base branch, and creates a new branch for focused work.
````

## Risk notes

Put risk notes close to the relevant example.

Use GitHub alerts when the reader could lose work, rewrite history, expose secrets, create cost, or affect shared infrastructure:

```markdown
> [!WARNING]
> `git reset --hard` discards tracked file changes. Save work before running it.
```

Use:

- `[!WARNING]` for destructive or risky operations.
- `[!IMPORTANT]` for rules the reader should not miss.
- `[!TIP]` for safer habits or useful shortcuts.
- `[!NOTE]` for background context.

## Command reference standard

Command pages should usually follow this flow:

1. Start with a short `Purpose`.
2. Group commands by task or workflow.
3. Use small tables with only the scan-level information.
4. Add examples below each table.
5. Put `What it does:` directly below each example.
6. Add risk notes near risky examples.
7. End with official docs and navigation links.

Example section:

````markdown
## Inspect work

| Task | Command | When to use it |
| --- | --- | --- |
| Check current state | `git status --short --branch` | Before staging, committing, pulling, or switching branches. |
| Show unstaged changes | `git diff` | Before staging files. |

### Check current state

```bash
git status --short --branch
```

What it does: shows the current branch, upstream status, staged changes, unstaged changes, and untracked files.
````

## Troubleshooting standard

Troubleshooting pages should help the reader move from symptom to diagnosis to safe fix.

Recommended structure:

1. Purpose.
2. First checks.
3. Symptom tables.
4. Diagnostic examples.
5. Safe fix examples.
6. Escalation or recovery notes.
7. Related links.

Do not start with the most destructive fix. Show inspection commands first.

## Catalog standard

Catalog pages may be long, but they should still be readable.

- Split catalogs into categories.
- Use `Command`, `Use`, and `Notes` columns.
- Put examples after each category, not inside the table.
- Keep notes short.
- Link to official documentation when the catalog depends on external command behavior.

## Navigation standard

Every focused article should end with links back to:

- the parent index,
- the major area index when different from the parent,
- the root index.

Example:

```markdown
## Related links

- Official documentation: https://example.com/docs
- Back to Git commands: README.md
- Back to Git index: ../README.md
- Back to root index: ../../README.md
```

## Validation before committing

Before committing documentation changes:

- Run `git status --short --branch`.
- Confirm only intended files changed.
- Run markdown lint when available:

```bash
npx markdownlint-cli2 "**/*.md"
```

- Check internal links when possible.
- Update parent indexes for new or moved pages.
- Update `CHANGELOG.md` for meaningful content, structure, or workflow changes.
- Update `context.md` when routes, conventions, or agent instructions change.

## Related links

- [AI agent context](context.md)
- [Templates](templates/README.md)
- [Contributing](CONTRIBUTING.md)
- [Back to root index](README.md)
