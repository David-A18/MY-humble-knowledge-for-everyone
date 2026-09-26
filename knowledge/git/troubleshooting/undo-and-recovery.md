---
type: "Troubleshooting Guide"
title: "Undo and recovery"
description: "Use Git's inspection tools before undoing work, then choose the least destructive recovery path."
tags: [git, troubleshooting, undo-and-recovery]
status: stable
maturity: maintained
audience: "Developers learning safe Git recovery"
maintainer: unassigned
sources:
  - id: git-status
    resource: https://git-scm.com/docs/git-status
    title: git-status documentation
  - id: git-diff
    resource: https://git-scm.com/docs/git-diff
    title: git-diff documentation
  - id: git-restore
    resource: https://git-scm.com/docs/git-restore
    title: git-restore documentation
  - id: git-revert
    resource: https://git-scm.com/docs/git-revert
    title: git-revert documentation
  - id: git-reset
    resource: https://git-scm.com/docs/git-reset
    title: git-reset documentation
  - id: git-reflog
    resource: https://git-scm.com/docs/git-reflog
    title: git-reflog documentation
  - id: git-clean
    resource: https://git-scm.com/docs/git-clean
    title: git-clean documentation
  - id: pro-git-undoing-things
    resource: https://git-scm.com/book/en/v2/Git-Basics-Undoing-Things
    title: Pro Git - Undoing Things
stale_after: 2026-12-21
---

# Undo and recovery

## Purpose

Use Git's inspection tools before undoing work, then choose the least destructive recovery path.

Status: Maintained
Audience: Developers learning safe Git recovery
Page type: Troubleshooting
Maintainer: Unassigned
Last substantive review: 2026-09-21
Applicable versions: Official Git reference documentation current on 2026-09-21; locally reproduced with Git 2.53.0
Validation evidence: Source reviewed against official Git status, diff, restore, revert, reset, reflog, and clean documentation; core examples executed in a disposable local repository
Known limitations: Examples cover normal single-repository tracked-file, untracked-file, revert, reset, and reflog behavior. Sparse checkout, submodule working trees, corrupt repositories, and complex merge-conflict recovery still need separate focused guides.
Next review: 2026-12-21 or after a relevant Git undo, restore, reset, reflog, or clean behavior change

## First checks

Run these commands from the repository root before choosing a recovery action:

```bash
git status --short --branch
git diff
git diff --staged
git log --oneline --decorate --graph --max-count=20
```

What it does: `git status --short --branch` shows the current branch and a compact file-state summary. `git diff` shows changes in the working tree that are not staged. `git diff --staged` shows changes already staged for the next commit. The short log shows recent commits and branch labels so you can decide whether the problem is a file-state issue, a local commit issue, or a shared-history issue.[^git-status][^git-diff]

Expected result: you should know which bucket you are in before running a destructive command.

| Bucket | Signal | Safer first move |
| --- | --- | --- |
| Unstaged tracked edits | `git status` shows a modified path, and `git diff` shows the unwanted change. | Restore only the affected path after confirming the diff. |
| Staged by mistake | `git diff --staged` shows a change that should not be in the next commit. | Unstage the path and keep the file content. |
| Bad local commit | The commit exists only on your branch or fork and has not been pulled by others. | Create a backup branch, then amend or reset depending on whether you need the content. |
| Bad shared commit | The commit was pushed to a branch others may use. | Prefer a revert commit. |
| Lost branch tip | A reset, amend, rebase, or branch move hid a commit you still need. | Inspect reflog and create a recovery branch. |
| Untracked build output | `git status` shows `??` paths that should be deleted. | Preview with `git clean -fdn` before deleting anything. |

> [!IMPORTANT]
> If you are not certain whether a commit has been shared, treat it as shared and use `git revert` or ask the repository owner. Rewriting a branch that collaborators use can make their local histories diverge.

## Common recovery commands

| Situation | Safer command | When to use it |
| --- | --- | --- |
| File was staged by mistake | `git restore --staged <path>` | You want to keep the file changes but remove them from the next commit. |
| Unstaged file changes should be discarded | `git restore <path>` | You want the working tree file back to the version in the index. |
| File should match the current commit | `git restore --source=HEAD <path>` | You want to ignore a staged version and restore the file from `HEAD`. |
| Bad commit was pushed | `git revert <commit>` | You need a public-history-safe undo commit. |
| Local commits should be regrouped | `git reset --soft <commit>` or `git reset <commit>` | The commits are local and you want to keep the file content. |
| Local branch and tracked files should match a commit | `git reset --hard <commit>` | You intentionally want to discard tracked changes and local commits after saving anything important. |
| Commit or branch tip seems lost | `git reflog` | You need to find a previous `HEAD` or branch position. |
| Untracked files should be removed | `git clean -fdn`, then `git clean -fd` | You want to delete untracked files or directories after reviewing the preview. |

## Recovery workflows

### Unstage a file

```bash
git restore --staged path/to/file
```

What it does: restores the path in the index from `HEAD`, which removes it from the staging area while keeping the working tree content.[^git-restore]

Expected result: `git diff --staged -- path/to/file` no longer shows the file, and `git diff -- path/to/file` still shows the local edit.

### Discard one file's local edits

> [!WARNING]
> `git restore path/to/file` discards unstaged edits in that file. If the file is staged, the working tree is restored from the staged version, not necessarily from `HEAD`.[^git-restore]

```bash
git restore path/to/file
```

What it does: replaces the working tree file with the version currently in the index. Use `git restore --source=HEAD path/to/file` when you explicitly want the working tree file restored from the current commit.

Expected result: `git diff -- path/to/file` is empty for that path.

If it fails: check for a typo in the path, confirm the file is tracked with `git ls-files -- path/to/file`, and inspect whether the repository is in an unmerged conflict state.

### Restore a file from the current commit

> [!WARNING]
> This discards both unstaged working tree edits and any staged version for the selected path.

```bash
git restore --source=HEAD --staged --worktree path/to/file
```

What it does: restores both the index and the working tree copy from `HEAD`. The Git restore documentation describes the index as `--staged` and the working tree as `--worktree`; using both updates both locations.[^git-restore]

Expected result: neither `git diff -- path/to/file` nor `git diff --staged -- path/to/file` shows that path.

### Undo a pushed commit

> [!IMPORTANT]
> `git revert` requires a clean working tree. Commit, stash, or restore unrelated local changes before running it.[^git-revert]

```bash
git revert abc1234
```

What it does: creates a new commit that reverses the selected commit without rewriting shared history.[^git-revert]

Expected result: `git log --oneline --max-count=3` shows a new commit whose message starts with `Revert`.

If it conflicts: resolve the conflicted files, stage them, and run `git revert --continue`. If the selected revert was the wrong action, use `git revert --abort` before continuing.

### Regroup local commits without losing content

> [!WARNING]
> Use reset only for local history that other people have not based work on. Create a backup branch first when the work matters.

```bash
git branch backup/before-reset
git reset --soft HEAD~1
```

What it does: creates a recovery reference, then moves the current branch back one commit while leaving the index and working tree unchanged. This is useful when the last local commit should be recommitted with a different message or combined with more staged changes.[^git-reset]

Expected result: `git status --short --branch` shows the branch at the earlier commit with the previous commit's changes still staged.

```bash
git branch backup/before-reset
git reset HEAD~1
```

What it does: moves the branch back one commit and leaves the previous commit's changes in the working tree as unstaged changes.

Expected result: `git diff` shows the previous commit's file changes, and `git diff --staged` is empty unless other staged work already existed.

### Discard local tracked changes and local commits

> [!WARNING]
> `git reset --hard <commit>` overwrites tracked files and moves the branch. Save needed work first with a commit, stash, patch file, or backup branch.

```bash
git branch backup/before-hard-reset
git reset --hard origin/main
```

What it does: saves the current tip under a backup branch, then makes the current branch, index, and tracked working tree match `origin/main`. Official Git documentation describes `--hard` as updating the index and working tree to the target commit and removing tracked files that are not present there.[^git-reset]

Expected result: `git status --short --branch` shows a clean tracked working tree against the selected branch.

If it fails: do not repeat the command blindly. Check whether files are unmerged, whether the remote reference exists with `git branch -r`, and whether untracked files are blocking checkout of tracked paths.

### Recover a moved branch tip

```bash
git reflog --date=local
```

What it does: shows recent positions of `HEAD` and branch refs so you can find commits that no longer appear in normal branch history. Git records reflogs locally when reference tips move, and the `HEAD` reflog also records branch switching.[^git-reflog]

Expected result: find the commit hash or `HEAD@{n}` entry from before the bad reset, amend, rebase, or branch move.

After you find the entry, protect it with a branch:

```bash
git switch -c recovery/lost-work abc1234
```

What it does: creates a named branch at the recovered commit so normal cleanup does not leave your only reference in reflog history.

If you cannot find it: check the branch-specific reflog with `git reflog show <branch>`. Reflog is local to the repository and is not a remote backup; another clone may not have the same entries.

### Preview and remove untracked files

> [!WARNING]
> `git clean -fd` deletes untracked files and directories. Git cannot recover untracked files that were never committed unless another backup system has them.

```bash
git clean -fdn
```

What it does: previews the untracked files and directories that `git clean -fd` would remove. The official command uses `-n` or `--dry-run` to show what would be done without deleting anything.[^git-clean]

Expected result: every listed path is safe to delete.

```bash
git clean -fd
```

What it does: removes the listed untracked files and directories. Use `git clean -fdX` when you only want ignored files, such as build outputs, and `git clean -fdx` only when ignored and unignored untracked files should both be removed.[^git-clean]

Expected result: `git status --short` no longer lists the removed untracked paths.

> [!WARNING]
> Avoid history-rewriting commands on shared branches unless the team has agreed on the workflow.

## Decision sequence

1. Inspect status, unstaged diff, staged diff, and recent history before changing state.
2. If a file is staged by mistake, unstage it with `git restore --staged <path>`.
3. If unstaged tracked edits are unwanted, restore only the affected path.
4. If untracked files are unwanted, preview with `git clean -fdn` before deleting.
5. If a bad commit is shared, prefer `git revert`.
6. If a bad commit is local and the content should stay, create a backup branch and use `git reset --soft` or `git reset`.
7. If a local branch moved unexpectedly, inspect `git reflog` and create a recovery branch before doing more cleanup.

## Recovery limits

- Uncommitted changes discarded by `git restore`, `git reset --hard`, or `git clean` are often unrecoverable from Git. Pro Git explicitly warns that some undo operations can lose work when used incorrectly.[^pro-git-undoing-things]
- Reflog is local repository history, not a shared remote record. Clone-specific reflogs can differ.
- Sparse checkout and submodules change restore and reset behavior. The Git restore and reset references include options for sparse checkout and submodule recursion; use a focused guide before applying broad recovery commands in those repositories.[^git-restore][^git-reset]
- During merge, rebase, cherry-pick, or revert conflicts, prefer the operation-specific `--abort`, `--continue`, and conflict-resolution workflow instead of mixing unrelated reset commands.

## Related links

- [git status documentation](https://git-scm.com/docs/git-status)
- [git diff documentation](https://git-scm.com/docs/git-diff)
- [git restore documentation](https://git-scm.com/docs/git-restore)
- [git revert documentation](https://git-scm.com/docs/git-revert)
- [git reset documentation](https://git-scm.com/docs/git-reset)
- [git reflog documentation](https://git-scm.com/docs/git-reflog)
- [git clean documentation](https://git-scm.com/docs/git-clean)
- [Pro Git: Undoing Things](https://git-scm.com/book/en/v2/Git-Basics-Undoing-Things)
- [Solve Git issues](../commands/solve-issues.md)
- [Back to Git troubleshooting](index.md)
- [Back to Git index](../index.md)
- [Back to root index](../../../README.md)

[^git-status]: Official Git status documentation, source record `git-status`.
[^git-diff]: Official Git diff documentation, source record `git-diff`.
[^git-restore]: Official Git restore documentation, source record `git-restore`.
[^git-revert]: Official Git revert documentation, source record `git-revert`.
[^git-reset]: Official Git reset documentation, source record `git-reset`.
[^git-reflog]: Official Git reflog documentation, source record `git-reflog`.
[^git-clean]: Official Git clean documentation, source record `git-clean`.
[^pro-git-undoing-things]: Pro Git "Undoing Things", source record `pro-git-undoing-things`.
