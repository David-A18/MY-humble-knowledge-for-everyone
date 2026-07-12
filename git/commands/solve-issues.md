# Solve Git issues

## Purpose

Use this page when you made a mistake and need the safest command for the situation.

> [!IMPORTANT]
> Inspect before you undo. Start with `git status --short --branch`, `git diff`, `git diff --staged`, and `git log --oneline --decorate --graph --max-count=20`.

## Issue solving command table

| Task | Command | Example | When to use it | What it does | Risk/notes |
| --- | --- | --- | --- | --- | --- |
| Unstage a file | `git restore --staged <path>` | `git restore --staged README.md` | You staged a file by mistake. | Removes the file from the index but keeps the working tree change. | Safe for local file content. |
| Discard unstaged changes in one file | `git restore <path>` | `git restore README.md` | You want the file back to the version in `HEAD`. | Replaces the working tree file with the committed version. | Destructive for uncommitted edits in that file. |
| Restore a deleted tracked file | `git restore <path>` | `git restore src/app.js` | You deleted a tracked file by mistake. | Recreates the file from `HEAD`. | Safe if the committed version is what you want. |
| Restore from another commit | `git restore --source=<commit> <path>` | `git restore --source=HEAD~1 README.md` | You need a file as it existed at another commit. | Copies that path from the selected commit into the working tree. | Review and commit the restored content intentionally. |
| Amend the last local commit | `git commit --amend` | `git commit --amend --no-edit` | The latest commit is local and needs a small correction. | Replaces the last commit with a new one. | Rewrites history. Avoid after others may have pulled it. |
| Undo a pushed commit | `git revert <commit>` | `git revert abc1234` | A bad commit is already shared. | Creates a new commit that reverses the selected commit. | Preferred public-history fix because it preserves history. |
| Undo several pushed commits | `git revert <old>..<new>` | `git revert main~3..main` | Multiple shared commits need to be reversed. | Creates revert commits for the selected range. | Review the range carefully before confirming. |
| Move branch back but keep changes staged | `git reset --soft <commit>` | `git reset --soft HEAD~1` | You want to redo the last local commit message or grouping. | Moves `HEAD` while leaving changes staged. | Rewrites local history. Do not use on shared commits. |
| Move branch back and unstage changes | `git reset --mixed <commit>` | `git reset HEAD~1` | You want to break the last local commit into smaller commits. | Moves `HEAD` and resets the index, leaving working tree changes. | Default reset mode. Rewrites local history. |
| Discard local commits and file changes | `git reset --hard <commit>` | `git reset --hard origin/main` | You intentionally want the branch and working tree to match a known commit. | Moves `HEAD`, resets the index, and resets tracked files. | Destructive. Confirm `git status` and save needed work first. |
| Remove untracked files | `git clean -fd` | `git clean -fd` | Build artifacts or generated files are untracked and should be deleted. | Deletes untracked files and directories. | Destructive. Preview with `git clean -fdn` first. |
| Preview untracked cleanup | `git clean -fdn` | `git clean -fdn` | Before running `git clean -fd`. | Shows what would be removed. | Safe dry run. |
| Recover a lost commit | `git reflog` | `git reflog --date=local` | A branch moved, a commit disappeared, or an amend/reset went wrong. | Shows recent positions of `HEAD` and branch refs. | Read-only. Copy the commit ID you want to recover. |
| Create a recovery branch | `git switch -c <branch> <commit>` | `git switch -c recovery/lost-work abc1234` | After finding a commit in `git reflog`. | Creates a branch pointing at the recovered commit. | Safe way to preserve recovered work. |
| Abort a merge | `git merge --abort` | `git merge --abort` | A merge conflict is not worth resolving right now. | Attempts to return the working tree to the pre-merge state. | Safer when you had a clean working tree before merging. |
| Abort a rebase | `git rebase --abort` | `git rebase --abort` | A rebase conflict is too complex or wrong. | Stops the rebase and returns to the original branch state. | Use before continuing with other history edits. |
| Continue a rebase | `git rebase --continue` | `git rebase --continue` | After resolving rebase conflicts. | Records conflict resolutions and continues replaying commits. | Run `git status` to see remaining conflict files first. |
| Skip a rebase commit | `git rebase --skip` | `git rebase --skip` | A replayed commit is unnecessary because its changes already exist. | Drops the current commit from the rebase sequence. | Can lose intended changes. Use only when you understand the skipped commit. |
| Abort a cherry-pick | `git cherry-pick --abort` | `git cherry-pick --abort` | A cherry-pick conflict should be abandoned. | Stops the cherry-pick and restores the pre-operation state. | Safest when working tree was clean before cherry-pick. |
| Continue a cherry-pick | `git cherry-pick --continue` | `git cherry-pick --continue` | After resolving cherry-pick conflicts. | Completes the cherry-pick operation. | Stage resolved files first. |
| Find which commit changed a line | `git blame <path>` | `git blame README.md` | You need the origin of a line before changing or reverting it. | Shows the last commit and author for each line. | Use for investigation, not blame in the human sense. |
| Find when a bug appeared | `git bisect` | `git bisect start` | You know one good commit and one bad commit. | Runs a binary search through history. | Requires reliable test steps. |

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
