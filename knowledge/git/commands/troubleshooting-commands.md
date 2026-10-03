---
type: "Troubleshooting Guide"
title: "Git troubleshooting commands"
description: "Trace a Git problem to branch tracking, a remote, an ignored file, a conflict, or repository health before changing state."
tags: [git, troubleshooting-commands]
status: draft
maturity: draft
audience: "Engineering learners and practitioners"
maintainer: "unassigned"
sources:
  - id: git-status
    resource: https://git-scm.com/docs/git-status
    title: Git - git-status
  - id: git-branch
    resource: https://git-scm.com/docs/git-branch
    title: Git - git-branch
  - id: git-remote
    resource: https://git-scm.com/docs/git-remote
    title: Git - git-remote
  - id: git-fetch
    resource: https://git-scm.com/docs/git-fetch
    title: Git - git-fetch
  - id: git-log
    resource: https://git-scm.com/docs/git-log
    title: Git - git-log
  - id: git-check-ignore
    resource: https://git-scm.com/docs/git-check-ignore
    title: Git - git-check-ignore
  - id: git-ls-files
    resource: https://git-scm.com/docs/git-ls-files
    title: Git - git-ls-files
  - id: git-diff
    resource: https://git-scm.com/docs/git-diff
    title: Git - git-diff
  - id: git-fsck
    resource: https://git-scm.com/docs/git-fsck
    title: Git - git-fsck
---

# Git troubleshooting commands

## Start with the question, not a fix

Use this page when Git behaves differently from what you expected:
a push is rejected, a file seems ignored, a merge stops, or the
repository may be damaged. The first job is to find **which
boundary** failed: your current branch, its upstream, the remote
repository, the index and working tree, or the object database.
This page gathers evidence; [Solve Git issues](solve-issues.md)
helps choose a recovery action after you know what happened.

From the affected repository, run:

```bash
git status --short --branch
git branch -vv
git remote -v
```

Expected result: you can name the current branch, see whether
Git reports local edits or an unfinished operation, see whether
that branch has an upstream, and identify its remote URL. These
commands inspect local state; they do not fetch, merge, or push.
Be careful when sharing a remote URL from a private repository:
some URLs contain credentials or internal hostnames.[^git-status]
[^git-branch][^git-remote]

| Symptom | First question | Focused check |
| --- | --- | --- |
| Push was rejected | Is the remote or upstream wrong, or did the remote branch move? | [Branch and remote](#a-push-or-pull-uses-the-wrong-target-or-is-rejected). |
| A file does not appear, or appears despite `.gitignore` | Is the path already tracked? Which ignore rule matches it? | [Ignore and tracking](#a-file-is-missing-or-ignore-seems-broken). |
| Merge, rebase, or cherry-pick stopped | Which operation is active, and which paths are unmerged? | [Conflict](#an-operation-stopped-on-a-conflict). |
| Git reports missing or corrupt objects | Does the object database pass a read-only integrity check? | [Repository health](#git-reports-object-errors). |
| A commit or local edit seems lost | Was the branch tip moved, or was uncommitted content discarded? | [Undo and recovery](../troubleshooting/undo-and-recovery.md). |

## A push or pull uses the wrong target or is rejected

First read the exact error. An authentication failure, a protected
branch rule, and a non-fast-forward rejection require different
responses. Inspect the target before fetching:

```bash
git branch -vv
git remote -v
```

`branch -vv` shows tracking information for local branches;
`remote -v` shows fetch and push URLs. If the branch has no
upstream, a command using `@{upstream}` below will fail; stop
and decide which remote branch should be tracked.[^git-branch]
[^git-remote]

If the URL and upstream are right, refresh your view and compare
the two histories. These commands assume the upstream is on
`origin`; use its actual remote name if yours differs:

```bash
git fetch origin
git log --left-right --graph --oneline HEAD...@{upstream}
```

`fetch` updates remote-tracking references; it does **not**
merge into the checked-out branch. The log marks commits on
each side of the split. If there are remote-only commits,
the rejection may be a normal divergence. If the server
reported permission or branch-rule denial, this graph does
not override that message. Do not force-push as a diagnostic.
[^git-fetch][^git-log]

For the safe branch-to-review path, use
[Common Git use cases](common-use-cases.md).

## A file is missing or ignore seems broken

Suppose a generated file at `build/output.txt` appears in
status even though `.gitignore` contains `build/`. Inspect
whether Git already tracks it and which rule would match:

```bash
git status --short -- build/output.txt
git ls-files -- build/output.txt
git check-ignore -v --no-index -- build/output.txt
```

If `ls-files` prints the path, Git tracks it. Ignore rules
normally apply to **untracked** paths, so adding `build/`
to `.gitignore` does not remove a tracked file. The
`--no-index` flag asks `check-ignore` to show the matching
rule even for a tracked path. If no rule matches, that command
may print nothing and exit nonzero. Inspect the rule before
changing tracking; the first question is whether this file
should remain versioned.[^git-ls-files][^git-check-ignore]

This example is about a generated file, not a credential.
If a secret was committed, removing it from current tracking
does not erase it from existing commits; rotate the secret and
follow the repository's incident process.

## An operation stopped on a conflict

```bash
git status
git diff --name-only --diff-filter=U
```

`status` names the in-progress operation and suggests its
next command. The filtered diff lists paths still marked
unmerged. Inspect the conflicted files and decide what the
combined content should be before staging a resolution.
Do not run `merge --abort`, `rebase --abort`, or a reset
merely because the conflict feels surprising: first confirm
which operation you would abandon and whether you have
other edits to preserve.[^git-status][^git-diff]

For recovery choices after inspection, use
[Undo and recovery](../troubleshooting/undo-and-recovery.md).

## Git reports object errors

When Git says an object is missing or corrupt, avoid
cleanup commands until you understand the damage. In a
local repository where an integrity scan is appropriate:

```bash
git fsck --full
```

This checks connectivity and validity of objects; it may
take time in a large repository. A failing result is
evidence to preserve the repository and compare it with
a known-good clone or backup. A successful result does
not diagnose every slow command, credential failure, or
remote service problem.[^git-fsck]

## Check your understanding

1. Why does `git fetch origin` help compare a rejected
   push without merging into your branch?
2. Why can a tracked file still appear even when its path
   matches `.gitignore`?
3. Which command tells you what operation is in progress
   before you consider an abort?
4. What does a failing `git fsck --full` establish, and
   what does a passing result leave unanswered?

## Deeper study

- [Git status](https://git-scm.com/docs/git-status),
  [branch](https://git-scm.com/docs/git-branch), and
  [remote](https://git-scm.com/docs/git-remote)
  for the local target and tracking model.
- [Git fetch](https://git-scm.com/docs/git-fetch)
  and [log](https://git-scm.com/docs/git-log)
  for comparing local and remote commits.
- [Git check-ignore](https://git-scm.com/docs/git-check-ignore)
  and [ls-files](https://git-scm.com/docs/git-ls-files)
  for ignore-rule versus tracked-file behavior.
- [Git fsck](https://git-scm.com/docs/git-fsck)
  for object integrity checks.

[Back to Git commands](index.md)

[^git-status]: [Git - git-status](https://git-scm.com/docs/git-status).
[^git-branch]: [Git - git-branch](https://git-scm.com/docs/git-branch).
[^git-remote]: [Git - git-remote](https://git-scm.com/docs/git-remote).
[^git-fetch]: [Git - git-fetch](https://git-scm.com/docs/git-fetch).
[^git-log]: [Git - git-log](https://git-scm.com/docs/git-log).
[^git-check-ignore]: [Git - git-check-ignore](https://git-scm.com/docs/git-check-ignore).
[^git-ls-files]: [Git - git-ls-files](https://git-scm.com/docs/git-ls-files).
[^git-diff]: [Git - git-diff](https://git-scm.com/docs/git-diff).
[^git-fsck]: [Git - git-fsck](https://git-scm.com/docs/git-fsck).
