---
type: "Troubleshooting Guide"
title: "Solve Git issues"
description: "Identify whether a Git mistake is in a file, the staging area, a local commit, or shared history before choosing a recovery path."
tags: [git, solve-issues]
status: draft
maturity: draft
audience: "Engineering learners and practitioners"
maintainer: "unassigned"
sources:
  - id: git-status
    resource: https://git-scm.com/docs/git-status
    title: Git - git-status
  - id: git-diff
    resource: https://git-scm.com/docs/git-diff
    title: Git - git-diff
  - id: git-restore
    resource: https://git-scm.com/docs/git-restore
    title: Git - git-restore
  - id: git-revert
    resource: https://git-scm.com/docs/git-revert
    title: Git - git-revert
  - id: git-reset
    resource: https://git-scm.com/docs/git-reset
    title: Git - git-reset
  - id: git-reflog
    resource: https://git-scm.com/docs/git-reflog
    title: Git - git-reflog
  - id: git-clean
    resource: https://git-scm.com/docs/git-clean
    title: Git - git-clean
---

# Solve Git issues

## First, find where the mistake lives

A Git mistake has a safer fix when you know **which copy** is
wrong: the file in your working tree, the staged copy in the
index, a local commit, or a commit people may already have
pulled. These locations behave differently. Start with
[Git fundamentals](../git-fundamentals.md) if this model is new.

Run these read-only checks in the affected repository:

```bash
git status
git status --short --branch
git diff
git diff --staged
git log --oneline --decorate --max-count=8
```

`status` identifies changed and untracked paths. The first diff
shows unstaged tracked edits; the second shows what is staged.
The log shows recent commits. If Git reports a merge, rebase,
cherry-pick, or revert in progress, identify that operation
before trying an unrelated recovery command.[^git-status]
[^git-diff]

Do not assume a commit is private merely because it is on your
current branch. If it may have been pushed or pulled, treat it
as shared history.

## Choose the smallest recovery scope

| Symptom | What the checks should show | First route |
| --- | --- | --- |
| A file is staged but should stay edited | `git diff --staged` shows it. | Unstage only that path with `git restore --staged -- <path>`; the working-tree edit stays. |
| An unstaged tracked edit should be discarded | `git diff -- <path>` shows the exact unwanted lines. | Follow the single-file restore procedure in [Undo and recovery](../troubleshooting/undo-and-recovery.md). |
| A file was deleted from the working tree | `git status` marks a tracked path deleted. | Use the [tracked-file recovery checks](../troubleshooting/undo-and-recovery.md#if-a-tracked-file-was-deleted-by-mistake) to distinguish an unstaged from a staged deletion. |
| An unwanted file was never tracked | `git status` shows `??`. | Inspect that path, then use the [directory-scoped clean preview](../troubleshooting/undo-and-recovery.md#if-untracked-files-should-be-deleted). |
| The last commit is wrong but private | The commit is only local and no one depends on it. | Back up the branch, then consider a [content-preserving reset](../troubleshooting/undo-and-recovery.md#if-the-commit-is-private-and-its-content-should-stay). |
| A pushed commit is wrong | Others may have the commit. | Follow the [shared-commit revert procedure](../troubleshooting/undo-and-recovery.md#if-a-bad-commit-has-been-shared), and be ready to resolve or abort a conflict. |
| A commit seems lost after reset, amend, or rebase | The commit is absent from normal log output. | Follow the [reflog recovery procedure](../troubleshooting/undo-and-recovery.md#if-a-branch-tip-or-commit-seems-lost) to name the right commit. |
| Git reports an operation in progress | `git status` names the operation and conflicted paths. | Follow that operation's continue or abort instructions; first decide whether to keep the conflict resolutions you made. |

Unstaging is usually reversible because it leaves your file
content alone. Restoring a file, cleaning untracked files, and
`reset --hard` can discard content that Git cannot recover if it
was never committed. `git revert` records a new commit rather
than moving a shared branch backward.[^git-restore][^git-clean]
[^git-reset][^git-revert]

## Example: you staged the wrong note

The paths and edits below are illustrative. Suppose you edited
`knowledge/glossary.md` and staged it, then noticed it belongs
in a later commit. Keep its content while removing it from the
next snapshot:

```bash
git diff --staged -- knowledge/glossary.md
git restore --staged -- knowledge/glossary.md
git diff --staged -- knowledge/glossary.md
git diff -- knowledge/glossary.md
```

Expected result: the second staged diff is empty for that path,
while the final working-tree diff still shows your edit. The
command changes the index copy, **not** the working-tree file.
If you had already committed the change, this procedure would
not remove it from that commit.[^git-restore]

## Stop before a destructive or shared-history change

- If you cannot tell whether a file is staged, compare both diffs
  for that exact path before using `restore`.
- If a commit may be shared, do not guess with `reset` or a force
  push. Prefer the public-history-safe revert route.
- If a cleanup preview includes work you need, narrow the path
  or move that work elsewhere before running `git clean`.
- If the branch tip moved unexpectedly, inspect reflog before
  doing more resets. Reflog is **local** to this repository and
  does not replace a backup.[^git-reflog]

For exact commands, expected results, conflict handling, and
recovery limits, follow [Undo and recovery](../troubleshooting/undo-and-recovery.md).
For a repository that is slow, has ignored-file surprises, or
cannot contact a remote, start with
[Git troubleshooting commands](troubleshooting-commands.md).

## Check your understanding

1. Which diff tells you what the next commit would contain?
2. Why does `git restore --staged -- <path>` keep the file edit?
3. Why is reverting a shared commit different from resetting a
   private branch?
4. Why can reflog help recover a commit but not an untracked file
   deleted by `git clean`?

## Deeper study

- [Git status](https://git-scm.com/docs/git-status)
  and [Git diff](https://git-scm.com/docs/git-diff)
  for locating a change.
- [Git restore](https://git-scm.com/docs/git-restore)
  for index versus working-tree restoration.
- [Git revert](https://git-scm.com/docs/git-revert)
  and [Git reset](https://git-scm.com/docs/git-reset)
  for their different commit-history effects.
- [Git reflog](https://git-scm.com/docs/git-reflog)
  and [Git clean](https://git-scm.com/docs/git-clean)
  for local recovery and untracked-file cleanup.

[Back to Git commands](index.md)

[^git-status]: [Git - git-status](https://git-scm.com/docs/git-status).
[^git-diff]: [Git - git-diff](https://git-scm.com/docs/git-diff).
[^git-restore]: [Git - git-restore](https://git-scm.com/docs/git-restore).
[^git-revert]: [Git - git-revert](https://git-scm.com/docs/git-revert).
[^git-reset]: [Git - git-reset](https://git-scm.com/docs/git-reset).
[^git-reflog]: [Git - git-reflog](https://git-scm.com/docs/git-reflog).
[^git-clean]: [Git - git-clean](https://git-scm.com/docs/git-clean).
