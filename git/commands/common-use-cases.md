# Common Git use cases

## Purpose

Use this page when you know what you want to do, but you are not sure which Git commands belong together.

## Start or configure a repository

| Task | Command | When to use it |
| --- | --- | --- |
| Start tracking an existing folder | `git init` | When a local project is not yet a Git repository. |
| Clone a repository | `git clone <url>` | When starting from an existing remote repository. |
| Check identity configuration | `git config --global --get <key>` | Before making commits on a new machine. |
| Set commit identity | `git config --global user.name "<name>"` | On a new workstation or account. |

### Start a repository

```bash
git init
git add .
git commit -m "Initial commit"
```

What it does: creates the `.git` directory, stages the current files, and records the first commit.

### Clone a repository

```bash
git clone https://github.com/example/project.git
```

What it does: downloads the repository and sets `origin` as the default remote.

### Configure your identity

```bash
git config --global --get user.email
git config --global user.name "Alex Rivera"
git config --global user.email "alex@example.com"
```

What it does: reads or sets the name and email used on future commits. Use repository-local config without `--global` when separating work and personal identities.

## Work on a feature branch

| Task | Command | When to use it |
| --- | --- | --- |
| Create a feature branch | `git switch -c <branch>` | Before starting a focused change. |
| Sync base branch safely | `git fetch` then `git pull --ff-only` | Before starting or updating feature work. |
| Rebase feature branch on base | `git rebase <base>` | For local feature commits that can be rewritten. |
| Merge base branch into feature branch | `git merge <base>` | When preserving exact history matters or rewriting is not allowed. |
| Review your branch against base | `git diff <base>...HEAD` | Before opening a pull request. |
| List branch commits not on base | `git log <base>..HEAD --oneline` | Before review or rebase. |

### Create and sync a feature branch

```bash
git fetch origin
git switch main
git pull --ff-only
git switch -c feature/login-audit
```

What it does: updates local knowledge of the remote, fast-forwards `main`, and creates a focused feature branch from the updated base.

### Update a feature branch

```bash
git rebase origin/main
```

What it does: replays local commits on top of the latest base branch. Do not rebase shared commits that others may have based work on.

### Review before a pull request

```bash
git diff origin/main...HEAD
git log origin/main..HEAD --oneline
```

What it does: shows the code changes and commits introduced by your branch since it split from the base.

## Share work

| Task | Command | When to use it |
| --- | --- | --- |
| Push a new branch | `git push -u origin HEAD` | First remote publish of a branch. |
| Update a pull request branch | `git push` | After more commits on a branch with upstream tracking. |
| Inspect a remote URL | `git remote -v` | When checking where fetches and pushes go. |
| Change a remote URL | `git remote set-url <name> <url>` | When switching between HTTPS and SSH or moving repositories. |

### Push branch work

```bash
git push -u origin HEAD
git push
```

What it does: publishes the current branch and sets tracking on the first push. Later pushes can use the shorter command.

### Check or change remotes

```bash
git remote -v
git remote set-url origin git@github.com:example/project.git
```

What it does: shows where Git fetches and pushes, then updates the remote URL when a repository moves or you switch between HTTPS and SSH.

## Releases and context switching

| Task | Command | When to use it |
| --- | --- | --- |
| Make a release tag | `git tag -a <tag> -m "<message>"` | When marking an official release. |
| Push a tag | `git push origin <tag>` | After creating a release tag locally. |
| Save work before context switching | `git stash push -m "<message>"` | When switching tasks without committing incomplete work. |
| Work on two branches at once | `git worktree add <path> <branch>` | When you need separate working directories for parallel branches. |
| Remove a worktree | `git worktree remove <path>` | When a linked working tree is no longer needed. |
| Remove tracked files that should be ignored | `git rm --cached <path>` | After adding a tracked file to `.gitignore`. |

### Tag a release

```bash
git tag -a v1.2.0 -m "Release v1.2.0"
git push origin v1.2.0
```

What it does: creates an annotated release tag and publishes only that tag. Avoid `git push --tags` unless you intend to publish every local tag.

### Save unfinished work

```bash
git stash push -m "checkout before hotfix"
```

What it does: saves tracked local changes outside the branch history so you can switch tasks with a clean working tree.

### Use a worktree

```bash
git worktree add ../project-hotfix hotfix/login
git worktree remove ../project-hotfix
```

What it does: creates and later removes a second working directory connected to the same repository. Keep each worktree on a different branch.

### Stop tracking an ignored file

```bash
git rm --cached .env
```

What it does: removes the file from Git tracking while leaving it in your working tree. If the file contained a secret, rotate the secret too.

## Recommended feature branch workflow

1. `git fetch --all --prune`
2. `git switch main`
3. `git pull --ff-only`
4. `git switch -c feature/descriptive-name`
5. Work, test, `git add -p`, and `git commit`.
6. `git diff origin/main...HEAD`
7. `git push -u origin HEAD`

## Related links

- [Everyday Git](https://git-scm.com/docs/giteveryday)
- [Git workflows](https://git-scm.com/docs/gitworkflows)
- [Back to Git commands](README.md)
- [Back to Git index](../README.md)
- [Back to root index](../../README.md)
