# Solve Git issues

## Purpose

Use this page when you made a mistake and need the safest command for the situation.

> [!IMPORTANT]
> Inspect before you undo. Start with `git status --short --branch`, `git diff`, `git diff --staged`, and `git log --oneline --decorate --graph --max-count=20`.

## Unstage or restore files

| Task | Command | When to use it |
| --- | --- | --- |
| Unstage a file | `git restore --staged <path>` | You staged a file by mistake. |
| Discard unstaged changes in one file | `git restore <path>` | You want the file back to the version in `HEAD`. |
| Restore a deleted tracked file | `git restore <path>` | You deleted a tracked file by mistake. |
| Restore from another commit | `git restore --source=<commit> <path>` | You need a file as it existed at another commit. |

### Unstage a file

```bash
git restore --staged README.md
```

What it does: removes the file from the index but keeps your working tree change.

### Discard local file edits

```bash
git restore README.md
```

What it does: replaces the working tree file with the committed version. This destroys uncommitted edits in that file.

### Restore a file from history

```bash
git restore --source=HEAD~1 README.md
```

What it does: copies the selected path from another commit into your working tree so you can review and commit it intentionally.

## Fix commits

| Task | Command | When to use it |
| --- | --- | --- |
| Amend the last local commit | `git commit --amend` | The latest commit is local and needs a small correction. |
| Undo a pushed commit | `git revert <commit>` | A bad commit is already shared. |
| Undo several pushed commits | `git revert <old>..<new>` | Multiple shared commits need to be reversed. |
| Move branch back but keep changes staged | `git reset --soft <commit>` | You want to redo the last local commit message or grouping. |
| Move branch back and unstage changes | `git reset --mixed <commit>` | You want to break the last local commit into smaller commits. |
| Discard local commits and file changes | `git reset --hard <commit>` | You intentionally want the branch and working tree to match a known commit. |

### Amend the last local commit

```bash
git commit --amend --no-edit
```

What it does: replaces the last commit with a new one. This rewrites history, so avoid it after others may have pulled the commit.

### Revert a pushed commit

```bash
git revert abc1234
```

What it does: creates a new commit that reverses the selected commit. This is the safest default for public history.

### Reset local commits

```bash
git reset --soft HEAD~1
git reset HEAD~1
git reset --hard origin/main
```

What it does: `--soft` keeps changes staged, mixed reset keeps changes unstaged, and `--hard` discards tracked file changes. Use `--hard` only after saving anything important.

## Clean and recover work

| Task | Command | When to use it |
| --- | --- | --- |
| Preview untracked cleanup | `git clean -fdn` | Before running a destructive cleanup. |
| Remove untracked files | `git clean -fd` | Build artifacts or generated files should be deleted. |
| Recover a lost commit | `git reflog` | A branch moved, a commit disappeared, or amend/reset went wrong. |
| Create a recovery branch | `git switch -c <branch> <commit>` | After finding a commit in `git reflog`. |

### Clean untracked files

```bash
git clean -fdn
git clean -fd
```

What it does: the first command previews what Git would remove. The second deletes untracked files and directories. Always preview first.

### Recover a lost commit

```bash
git reflog --date=local
git switch -c recovery/lost-work abc1234
```

What it does: `git reflog` shows recent positions of `HEAD` and branch refs. Once you find the commit, create a branch so it cannot disappear from normal cleanup.

## Abort or continue operations

| Task | Command | When to use it |
| --- | --- | --- |
| Abort a merge | `git merge --abort` | A merge conflict is not worth resolving right now. |
| Abort a rebase | `git rebase --abort` | A rebase conflict is too complex or wrong. |
| Continue a rebase | `git rebase --continue` | After resolving rebase conflicts. |
| Skip a rebase commit | `git rebase --skip` | A replayed commit is unnecessary because its changes already exist. |
| Abort a cherry-pick | `git cherry-pick --abort` | A cherry-pick conflict should be abandoned. |
| Continue a cherry-pick | `git cherry-pick --continue` | After resolving cherry-pick conflicts. |

### Merge, rebase, and cherry-pick controls

```bash
git merge --abort
git rebase --abort
git rebase --continue
git cherry-pick --abort
git cherry-pick --continue
```

What it does: abort commands stop the in-progress operation and try to return to the previous state. Continue commands move forward after you resolve conflicts and stage the fixed files.

## Investigate before fixing

| Task | Command | When to use it |
| --- | --- | --- |
| Find which commit changed a line | `git blame <path>` | You need the origin of a line before changing or reverting it. |
| Find when a bug appeared | `git bisect` | You know one good commit and one bad commit. |

### Find line history

```bash
git blame README.md
```

What it does: shows the last commit and author for each line. Use it for investigation, not as a people problem.

### Find the commit that introduced a bug

```bash
git bisect start
```

What it does: starts a binary search through history. Mark commits as good or bad until Git identifies the first bad commit.

## Recovery rules

- If the bad change was pushed, prefer `git revert`.
- If the bad change is local, choose the least destructive command first.
- If you are unsure, create a backup branch before rewriting: `git branch backup/before-recovery`.
- Committed work can often be recovered with `git reflog`; uncommitted discarded work often cannot.

## Related links

- [Pro Git: Undoing Things](https://git-scm.com/book/en/v2/Git-Basics-Undoing-Things)
- [git restore documentation](https://git-scm.com/docs/git-restore)
- [git revert documentation](https://git-scm.com/docs/git-revert)
- [Back to Git commands](README.md)
- [Back to Git index](../README.md)
- [Back to root index](../../README.md)
