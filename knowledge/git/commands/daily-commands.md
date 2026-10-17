---
type: "How-to Guide"
title: "Daily Git commands"
description: "Inspect one local change, stage only the intended file, review the staged snapshot, and create a commit safely."
tags: [git, daily-commands]
status: draft
maturity: draft
audience: "Engineering learners and practitioners"
maintainer: "unassigned"
sources:
  - id: git-status
    resource: https://git-scm.com/docs/git-status
    title: Git - git-status Documentation
  - id: git-diff
    resource: https://git-scm.com/docs/git-diff
    title: Git - git-diff Documentation
  - id: git-add
    resource: https://git-scm.com/docs/git-add
    title: Git - git-add Documentation
  - id: git-commit
    resource: https://git-scm.com/docs/git-commit
    title: Git - git-commit Documentation
  - id: git-restore
    resource: https://git-scm.com/docs/git-restore
    title: Git - git-restore Documentation
---

# Daily Git commands

## Goal and starting point

Use this guide to turn **one intended file change** into a local commit. You
will inspect the working tree, stage that file, check the exact staged
snapshot, then commit it. You need an existing Git repository, a branch where
you intend to work, a configured Git author identity, and a file you have
already edited. This guide does not push, merge, or rewrite shared history.

If the working tree, index, and commit are unfamiliar, read [Git
fundamentals](../git-fundamentals.md) first. Think of this loop as choosing
what goes into a package, checking its contents, then sealing it. The
**index** is the package being prepared; the commit is the saved result.

The commands below use `README.md` as an example. Replace that path with
your file. Run them from the root of **your intended repository**. Commands
that only inspect are marked “read”; commands that change Git state are
marked “write.” The example has been checked in a disposable local
repository, not against your project.

## 1. Find out what changed (read)

```bash
git status --short --branch
git diff -- README.md
```

The first command shows the branch and compact file states. The second
shows unstaged edits to the tracked file. `git status` also reveals new
untracked files; `git diff` alone does not show their contents.[^git-status][^git-diff]

**Expected:** the branch is the one you meant to use, and the diff contains
only the change you meant to save. If other files have changes, leave them
alone while following this example. If `README.md` is untracked, read it in
your editor because `git diff` will not display it yet.

**Stop if:** the branch, repository, or file is wrong. A commit on the wrong
branch is easier to avoid than to repair.

## 2. Stage the intended file (write to the index)

```bash
git add -- README.md
git status --short --branch
```

`git add` copies the file's current content into the index for the next
commit. It does not commit or push.[^git-add] The `--` separates options
from the path, which matters if a filename begins with a dash.

**Expected:** `README.md` appears as staged in `git status` (for example,
`M` in the left status column for a changed tracked file, or `A` there for
a new file). Other changes should remain unstaged or untracked unless you
explicitly selected them.

If you want only some lines from a file, use `git add -p -- README.md`
instead. It asks about each diff hunk. Read every hunk before accepting it;
the index can contain a different version of a file from the one currently
in your working tree.[^git-add]

## 3. Review the snapshot (read)

```bash
git diff --cached -- README.md
git diff --cached --check
git status --short --branch
```

`git diff --cached` compares the index with the current commit, so it shows
what is staged for the next commit. `--check` reports whitespace errors in
staged changes; it does not test whether the change behaves correctly.
Before committing, also run any project-specific checks required by that
repository.[^git-diff]

**Expected:** the staged diff includes exactly the intended text. If it
does not, unstage the file without discarding your working-tree edit:

```bash
git restore --staged -- README.md
```

Then inspect and stage again. `--staged` changes the index; it leaves the
working-tree version of the file in place.[^git-restore]

## 4. Commit the reviewed snapshot (write to history)

```bash
git commit -m "Explain the daily Git loop"
git status --short --branch
git log -1 --oneline
```

`git commit` records the currently staged content as a new local commit.
The message should explain the actual change in your project; the one above
is just an example. `git status` shows whether other work remains, and
`git log -1` confirms the new commit at the tip of this branch.[^git-commit]

**Expected:** Git reports one new commit. If unrelated changes remain in
your working tree, that can be fine; they were not included unless staged.
If Git says there is nothing to commit, return to steps 1–3 and check whether
the file was actually changed and staged.

## What this proves, and what it does not

A clean staged diff plus a successful commit proves which local snapshot you
saved. It does not prove that tests pass, that a remote has the commit, or
that a pull request is ready. A commit is local until you push it.

For the next distinct task, use [common Git use
cases](common-use-cases.md) for branches and remotes, [solve Git
issues](solve-issues.md) for mistakes, and [Git undo and
recovery](../troubleshooting/undo-and-recovery.md) before using any history
rewriting command. The [complete command
catalog](complete-command-catalog.md) remains the broad lookup page.

## Check your understanding

- Why is `git diff --cached` more useful than plain `git diff` immediately
  before committing?
- If you stage the wrong file, which command keeps the working-tree edit?
- What extra step is needed before a teammate can see your local commit on
  the remote?

## Official documentation for deeper study

- [git-status](https://git-scm.com/docs/git-status) defines staged, unstaged, and untracked reporting.
- [git-diff](https://git-scm.com/docs/git-diff) explains working-tree and index comparisons.
- [git-add](https://git-scm.com/docs/git-add) covers staging and interactive hunks.
- [git-restore](https://git-scm.com/docs/git-restore) explains unstaging without discarding working-tree edits.
- [git-commit](https://git-scm.com/docs/git-commit) defines what a commit records.

See the [Git commands index](index.md) or [Git index](../index.md).

[^git-status]: [git-status](https://git-scm.com/docs/git-status).
[^git-diff]: [git-diff](https://git-scm.com/docs/git-diff).
[^git-add]: [git-add](https://git-scm.com/docs/git-add).
[^git-restore]: [git-restore](https://git-scm.com/docs/git-restore).
[^git-commit]: [git-commit](https://git-scm.com/docs/git-commit).
