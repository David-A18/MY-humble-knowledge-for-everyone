# Daily Git commands

## Purpose

Use this page for the Git commands most developers run every day: inspect work, stage changes, commit, branch, sync with remotes, and keep short-term work safe.

## Inspect work

| Task | Command | When to use it |
| --- | --- | --- |
| Check current state | `git status --short --branch` | Before staging, committing, pulling, rebasing, or switching branches. |
| Show unstaged changes | `git diff` | Before staging files. |
| Show staged changes | `git diff --staged` | Before committing. |
| List tracked files | `git ls-files` | When you need to know what Git already tracks. |

### Check current state

```bash
git status --short --branch
```

What it does: shows the current branch, upstream status, staged changes, unstaged changes, and untracked files in a compact format. This is safe and should be your first Git habit.

### Review changes

```bash
git diff README.md
git diff --staged
```

What it does: `git diff` shows work that is not staged yet. `git diff --staged` shows exactly what will go into the next commit.

### List tracked files

```bash
git ls-files git/commands
```

What it does: prints files that are already in Git's index. Ignored files can still appear here if they were tracked before being added to `.gitignore`.

## Stage and commit

| Task | Command | When to use it |
| --- | --- | --- |
| Stage a file | `git add <path>` | When a change is ready for the next commit. |
| Stage selected hunks | `git add -p` | When one file contains changes for more than one commit. |
| Unstage a file | `git restore --staged <path>` | When a file was staged by mistake. |
| Commit staged changes | `git commit -m "<message>"` | When staged changes are complete and tested. |
| Amend the last local commit | `git commit --amend` | When the previous commit has not been shared and needs a small fix. |

### Stage changes

```bash
git add git/commands/daily-commands.md
git add -p README.md
```

What it does: `git add` copies the current file content into the staging area. `git add -p` lets you choose individual hunks so each commit can stay focused.

### Unstage a file

```bash
git restore --staged README.md
```

What it does: removes the file from the staging area while keeping your working tree changes.

### Commit staged changes

```bash
git commit -m "Add Git command reference"
```

What it does: records a snapshot of staged content in repository history. Use a clear message that explains the intent of the change.

### Amend the last local commit

```bash
git commit --amend --no-edit
```

What it does: replaces the previous commit with a new commit. This rewrites history, so use it only before other people may have pulled that commit.

## Branch and history

| Task | Command | When to use it |
| --- | --- | --- |
| Show recent history | `git log --oneline --decorate --graph --max-count=<n>` | When reviewing branch history. |
| Show one commit | `git show <commit>` | When reviewing a specific commit. |
| Create and switch to a branch | `git switch -c <branch>` | When starting focused work. |
| Switch branches | `git switch <branch>` | When moving to another branch. |
| List branches | `git branch --all` | When looking for local and remote-tracking branches. |
| Rename current branch | `git branch -m <new-name>` | When a local branch name should be clearer. |

### Show recent history

```bash
git log --oneline --decorate --graph --max-count=20
```

What it does: shows recent commits, branch labels, tags, and the shape of the commit graph.

### Show one commit

```bash
git show HEAD~1
```

What it does: shows commit metadata and the diff introduced by one commit.

### Work with branches

```bash
git switch -c feature/git-command-reference
git switch main
git branch --all
git branch -m feature/git-commands
```

What it does: creates, switches, lists, and renames branches. Start feature branches from the correct base branch and check `git status` before switching.

## Sync and temporary work

| Task | Command | When to use it |
| --- | --- | --- |
| Fetch remote updates | `git fetch --all --prune` | Before comparing, merging, rebasing, or pruning stale remote branches. |
| Pull remote updates | `git pull --ff-only` | When your branch should fast-forward to upstream. |
| Push current branch first time | `git push -u origin HEAD` | First push of a new branch. |
| Push later updates | `git push` | After upstream tracking is set. |
| Save temporary work | `git stash push -m "<message>"` | When you need a clean working tree but are not ready to commit. |
| Restore temporary work | `git stash pop` | When returning to stashed work. |
| List stashes | `git stash list` | Before applying or dropping a stash. |
| Tag a release point | `git tag <tag>` | When marking an important commit such as a release. |

### Fetch and pull

```bash
git fetch --all --prune
git pull --ff-only
```

What it does: `git fetch` downloads remote refs without changing your current branch. `git pull --ff-only` updates your branch only if Git can fast-forward cleanly.

### Push a branch

```bash
git push -u origin HEAD
git push
```

What it does: the first command pushes the current branch and sets upstream tracking. After that, `git push` is enough.

### Stash temporary work

```bash
git stash push -m "wip before pull"
git stash list
git stash pop
```

What it does: saves unfinished tracked changes outside the branch history, lists saved stashes, and restores the newest stash.

### Tag a release point

```bash
git tag v1.0.0
```

What it does: creates a tag pointing at the current commit. For public releases, prefer an annotated tag such as `git tag -a v1.0.0 -m "Release v1.0.0"`.

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
