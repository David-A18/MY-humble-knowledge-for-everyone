---
type: Reference
title: Git productivity tricks
description: Use git worktree, history search with git log -S, git reflog recovery, and aliases to work faster and recover safely.
tags: [git, tricks, productivity]
status: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
  - id: git-worktree
    resource: https://git-scm.com/docs/git-worktree
    title: git worktree documentation
  - id: git-log
    resource: https://git-scm.com/docs/git-log
    title: git log documentation
  - id: git-reflog
    resource: https://git-scm.com/docs/git-reflog
    title: git reflog documentation
  - id: git-config
    resource: https://git-scm.com/docs/git-config
    title: git config documentation
---

# Git productivity tricks

These are four Git features that save real time once you know them. Each one is
safe to use: none of them rewrites shared history.

## Work on two branches at once with `git worktree`

Instead of stashing your work to fix something on another branch, check that
branch out in a second folder:

```bash
git worktree add ../hotfix main
cd ../hotfix
# fix, commit, and push as usual
cd -
git worktree remove ../hotfix
```

What it does: creates a second working folder that shares the same repository,
with `main` checked out, and removes it when you finish. Your original folder
and its uncommitted changes stay untouched.[^git-worktree]

## Find when a piece of code appeared or disappeared

```bash
git log -S "retry_limit" --oneline
```

What it does: lists the commits that added or removed the text `retry_limit`.
It is the fastest way to answer "when did this setting change, and why?"
Add `-p` to see each diff.[^git-log]

## Recover "lost" commits with `git reflog`

After a bad reset or a deleted branch, the commits usually still exist. Git
records where `HEAD` has been:

```bash
git reflog
git branch rescue HEAD@{2}
```

What it does: lists recent positions of `HEAD`, then creates a branch called
`rescue` at the position from two moves ago, so the commits are reachable
again. Pick the entry from the list that shows your lost work.[^git-reflog]
The reflog is local and entries expire, so recover soon. See
[undo and recovery](../troubleshooting/undo-and-recovery.md) for the full
procedure.

## Save typing with aliases

```bash
git config --global alias.st "status --short --branch"
git config --global alias.lg "log --oneline --graph --decorate"
```

What it does: adds `git st` for a compact status and `git lg` for a one-line
history graph to your user configuration.[^git-config] Keep aliases simple and
readable; a teammate following your instructions will not have them.

## Related links

- [Daily Git commands](../commands/daily-commands.md)
- [Advanced Git commands](../commands/advanced-commands.md)
- [Back to Git tricks](index.md)

[^git-worktree]: [git worktree documentation](https://git-scm.com/docs/git-worktree)
[^git-log]: [git log documentation](https://git-scm.com/docs/git-log)
[^git-reflog]: [git reflog documentation](https://git-scm.com/docs/git-reflog)
[^git-config]: [git config documentation](https://git-scm.com/docs/git-config)
