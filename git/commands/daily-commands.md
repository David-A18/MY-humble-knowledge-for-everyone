# Daily Git commands

## Purpose

Use this page for the Git commands most developers run every day: inspect work, stage changes, commit, branch, sync with remotes, and keep short-term work safe.

## Daily command table

| Task | Command | Example | When to use it | What it does | Risk/notes |
| --- | --- | --- | --- | --- | --- |
| Check current state | `git status --short --branch` | `git status --short --branch` | Before staging, committing, pulling, rebasing, or switching branches. | Shows the current branch, upstream status, staged changes, unstaged changes, and untracked files in a compact format. | Safe read-only command. Make it the first habit. |
| Show unstaged changes | `git diff` | `git diff README.md` | Before staging files. | Shows changes in the working tree that are not staged. | Safe read-only command. |
| Show staged changes | `git diff --staged` | `git diff --staged` | Before committing. | Shows exactly what will be included in the next commit. | Safe read-only command. |
| List tracked files | `git ls-files` | `git ls-files git/commands` | When you need to know what Git already tracks. | Prints files in the index. | Safe read-only command. Ignored files may still be tracked if they were committed earlier. |
| Stage a file | `git add <path>` | `git add git/commands/daily-commands.md` | When a change is ready for the next commit. | Copies the current file content into the staging area. | If you edit the file again after staging, run `git add` again to stage the newer content. |
| Stage selected hunks | `git add -p` | `git add -p README.md` | When one file contains changes for more than one commit. | Lets you choose individual hunks interactively. | Review carefully so each commit stays focused. |
| Unstage a file | `git restore --staged <path>` | `git restore --staged README.md` | When a file was staged by mistake. | Removes the file from the staging area while keeping the working tree change. | Safe for file content in the working tree. |
| Commit staged changes | `git commit -m "<message>"` | `git commit -m "Add Git command reference"` | When staged changes are complete and tested. | Records a snapshot of staged content in repository history. | Prefer specific messages that explain the intent. |
| Amend the last local commit | `git commit --amend` | `git commit --amend --no-edit` | When the previous commit has not been shared and needs a small fix. | Replaces the previous commit with a new commit. | Rewrites history. Avoid on commits other people may already have. |
| Show recent history | `git log --oneline --decorate --graph --max-count=<n>` | `git log --oneline --decorate --graph --max-count=20` | When reviewing branch history. | Shows recent commits, branch labels, tags, and graph shape. | Safe read-only command. |
| Show one commit | `git show <commit>` | `git show HEAD~1` | When reviewing a specific commit. | Shows commit metadata and the diff introduced by that commit. | Safe read-only command. |
| Create and switch to a branch | `git switch -c <branch>` | `git switch -c feature/git-command-reference` | When starting focused work. | Creates a new branch from the current commit and checks it out. | Start from an up-to-date base branch. |
| Switch branches | `git switch <branch>` | `git switch main` | When moving to another branch. | Checks out the named branch. | Git may stop if uncommitted changes would be overwritten. |
| List branches | `git branch --all` | `git branch --all` | When looking for local and remote-tracking branches. | Shows local branches and remote-tracking refs. | Safe read-only command. |
| Rename current branch | `git branch -m <new-name>` | `git branch -m feature/git-commands` | When a local branch name should be clearer. | Renames the current branch. | Update the remote branch separately if it was already pushed. |
| Fetch remote updates | `git fetch --all --prune` | `git fetch --all --prune` | Before comparing, merging, rebasing, or pruning old remote branches. | Downloads remote refs and removes stale remote-tracking refs. | Does not change your working tree or current branch. |
| Pull remote updates | `git pull` | `git pull --ff-only` | When your branch should integrate upstream changes. | Runs fetch, then merge or rebase depending on configuration and options. | Prefer `--ff-only` when you do not intend to create a merge commit. |
| Push current branch | `git push -u origin HEAD` | `git push -u origin HEAD` | First push of a new branch. | Pushes the current branch and sets upstream tracking. | Check branch name before pushing public work. |
| Push later updates | `git push` | `git push` | After upstream is set. | Uploads local commits to the configured upstream branch. | Rejected pushes usually mean you need to fetch and integrate remote changes. |
| Save temporary work | `git stash push -m "<message>"` | `git stash push -m "wip before pull"` | When you need a clean working tree but are not ready to commit. | Stores tracked changes on the stash stack. | Use a message so the stash is recognizable later. |
| Restore temporary work | `git stash pop` | `git stash pop` | When returning to stashed work. | Applies the newest stash and drops it if the apply succeeds. | Use `git stash apply` if you want to keep the stash as a backup. |
| List stashes | `git stash list` | `git stash list` | Before applying or dropping a stash. | Shows saved stashes. | Safe read-only command. |
| Tag a release point | `git tag <tag>` | `git tag v1.0.0` | When marking an important commit such as a release. | Creates a tag pointing at the current commit. | Annotated tags are better for public releases: `git tag -a v1.0.0 -m "Release v1.0.0"`. |

## Professional daily flow

1. Run `git status --short --branch`.
2. Review work with `git diff` and `git diff --staged`.
3. Stage only the intended change with `git add <path>` or `git add -p`.
4. Commit with a message that explains the purpose.
5. Fetch before integrating remote changes.
6. Push only after confirming the branch and commit history.

## Related links

- [Git reference documentation](https://git-scm.com/docs)
- [Everyday Git](https://git-scm.com/docs/giteveryday)
- [Back to Git commands](README.md)
- [Back to Git index](../README.md)
- [Back to root index](../../README.md)
