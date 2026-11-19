---
type: How-to Guide
title: Commits, branches, and pull requests
description: Keep Git history easy to read and review with focused commits, clear messages, short-lived branches, and small pull requests.
tags: [git, best-practices, pull-requests]
status: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
  - id: git-commit
    resource: https://git-scm.com/docs/git-commit
    title: git commit documentation
  - id: gitworkflows
    resource: https://git-scm.com/docs/gitworkflows
    title: gitworkflows
  - id: git-diff
    resource: https://git-scm.com/docs/git-diff
    title: git diff documentation
---

# Commits, branches, and pull requests

Git history is a record your team reads for years: to review changes, find when
a bug appeared, and undo mistakes safely. A few habits make that record easy to
use. Each commit does one thing, each message explains why, branches live for
days rather than months, and pull requests stay small enough to review well.

## Make focused commits

A focused commit contains one logical change, such as "fix the timeout" or
"rename the config field", not both. Focused commits are easier to review, to
revert, and to search later.

Review exactly what you are about to commit:

```bash
git diff            # changes not yet staged
git add -p          # stage part of a file, one change at a time
git diff --staged   # what the next commit will contain
```

What it does: shows unstaged changes, lets you choose each change to stage
interactively, then shows the final staged content before you commit.[^git-diff]

Keep formatting-only changes, such as running a code formatter, in their own
commit. Mixed with behavior changes, they hide what really changed.

## Write messages that explain why

Git's own guidance is a short summary line, a blank line, then a body that
explains the change.[^git-commit]

```text
Retry uploads when the storage API times out

Large uploads failed about once a day when the storage API took longer
than 30 seconds. Retry up to three times with backoff so a slow response
no longer fails the whole job.
```

What it shows: a summary of about 50 characters in the imperative mood ("Retry",
not "Retried"), and a body that says what problem the change solves and why
this approach was chosen. The diff already shows *what* changed.

## Keep branches short-lived

- Create a branch per change, named for its purpose, for example
  `fix/upload-timeout` or `docs/terraform-backends`.
- Update it from the main branch often, so conflicts stay small.
- Merge and delete it within days. Long-lived branches drift and become risky
  to merge.[^gitworkflows]

## Open pull requests that are easy to review

- **Small:** a few hundred changed lines at most. Split bigger work into a
  series of pull requests.
- **Explained:** say what changed, why, and how you tested it.
- **Self-reviewed:** read your own diff first; you will often catch a mistake.
- **Green:** make sure automated checks pass before asking for review.

## Keep secrets and local files out

Never commit passwords, keys, or tokens. Once pushed, assume a secret is
exposed: rotate it, then remove it. Add editor files, build output, and local
configuration to `.gitignore` so they are never staged by accident.

## Checklist

- [ ] Each commit does one thing and its message explains why.
- [ ] Formatting-only changes are in their own commit.
- [ ] The branch is up to date with the main branch.
- [ ] The pull request is small, explained, self-reviewed, and passing checks.
- [ ] No secrets, generated files, or local settings are included.

## Related links

- [Git undo and recovery](../troubleshooting/undo-and-recovery.md)
- [Daily Git commands](../commands/daily-commands.md)
- [Back to Git best practices](index.md)

[^git-commit]: [git commit documentation](https://git-scm.com/docs/git-commit)
[^gitworkflows]: [gitworkflows](https://git-scm.com/docs/gitworkflows)
[^git-diff]: [git diff documentation](https://git-scm.com/docs/git-diff)
