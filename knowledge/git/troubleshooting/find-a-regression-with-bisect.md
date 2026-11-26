---
type: Troubleshooting Guide
title: Find the commit that introduced a regression with Git bisect
description: Reproduce a failure, bisect it in a separate worktree, and inspect the first failing commit.
tags: [git, troubleshooting, regression]
status: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
  - id: bisect
    resource: https://git-scm.com/docs/git-bisect
    title: Git bisect command reference
  - id: worktree
    resource: https://git-scm.com/docs/git-worktree
    title: Git worktree command reference
  - id: show
    resource: https://git-scm.com/docs/git-show
    title: Git show command reference
---

# Find the commit that introduced a regression with Git bisect

Use `git bisect` when you can reproduce a failure on one commit and confirm
that another commit passes the same check. Git uses those two endpoints to
choose revisions for you to test until it can identify the first failing
commit.[^bisect]

## Prepare a reproducible check

Choose a check you can repeat on each candidate. Run it first on the known
good and bad endpoints with the same inputs and environment. Use a disposable
test environment for builds or tests that write data. If the check is
intermittent, make it reliable before interpreting a bisect result.

Set `BAD_COMMIT` and `GOOD_COMMIT` to the verified commit IDs. Run this from
your existing checkout, using a new path for the linked worktree.[^worktree][^bisect]

```bash
git worktree add --detach ../review-bisect "$BAD_COMMIT"
git -C ../review-bisect bisect start "$BAD_COMMIT" "$GOOD_COMMIT"
```

What it does: checks out the bad commit in a separate working directory and
starts a bisect there. Run the test from that worktree because bisect changes
which revision it has checked out.[^worktree][^bisect]

## Classify the candidate

If you are testing manually, run the same check at each candidate and use
one of these commands from the original checkout.[^bisect]

| Result | Command |
| --- | --- |
| The regression reproduces | `git -C ../review-bisect bisect bad` |
| The check passes | `git -C ../review-bisect bisect good` |
| The candidate cannot be tested | `git -C ../review-bisect bisect skip` |

For a repeatable test, use `git bisect run`. Exit code 0 means good, 125
means skip, and 1 through 127 except 125 mean bad. Git aborts for other exit
codes. A failed setup that exits with 1 will be counted as bad, so make sure
your test distinguishes the regression from an unusable revision.[^bisect]

```bash
git -C ../review-bisect bisect run sh -c 'test -r status.txt || exit 125; test "$(cat status.txt)" = healthy'
```

What it does: demonstrates the contract using a synthetic file that contains
`healthy` in a good revision. An unreadable marker produces a skip. Replace
the file check with your own regression test when adapting the example.
Skipped commits near the boundary can leave more than one possible first
bad commit.[^bisect]

## Inspect the result and clean up

Record the reported commit and inspect its changes. Rerun the check at the
boundary before treating a result as the cause.[^bisect][^show]

```bash
git -C ../review-bisect bisect log
git -C ../review-bisect show "$FIRST_BAD_COMMIT"
git -C ../review-bisect bisect reset
git worktree remove ../review-bisect
```

What it does: prints the bisect decisions, shows the commit you recorded in
`FIRST_BAD_COMMIT`, restores the starting checkout in the linked worktree,
then removes the clean disposable worktree. If removal reports untracked
build artifacts or edits, inspect and preserve anything you need before
retrying.[^bisect][^show][^worktree]

## Evidence and limits

On 26 November 2026, Git 2.53.0 on Ubuntu 26.04 under WSL identified the
expected first bad commit in a three-commit synthetic repository. The
rehearsal verified reset to the starting revision and removal of the linked
worktree. The fixture did not include merge commits or skipped candidates.

## Related links

- [Git issue-solving commands](../commands/solve-issues.md)
- [Git troubleshooting](index.md)
- [Git index](../index.md)
- [Knowledge home](../../index.md)

[^bisect]: [Git bisect command reference](https://git-scm.com/docs/git-bisect)
[^worktree]: [Git worktree command reference](https://git-scm.com/docs/git-worktree)
[^show]: [Git show command reference](https://git-scm.com/docs/git-show)
