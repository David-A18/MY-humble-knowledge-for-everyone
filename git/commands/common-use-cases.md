# Common Git use cases

## Purpose

Use this page when you know what you want to do, but you are not sure which Git commands belong together.

## Use case command table

| Task | Command | Example | When to use it | What it does | Risk/notes |
| --- | --- | --- | --- | --- | --- |
| Start tracking an existing folder | `git init` | `git init` | When a local project is not yet a Git repository. | Creates the `.git` directory and repository metadata. | Does not automatically commit files. Run `git add` and `git commit` next. |
| Clone a repository | `git clone <url>` | `git clone https://github.com/example/project.git` | When starting from an existing remote repository. | Downloads the repository and sets `origin` as the default remote. | Use trusted URLs. Check access method: HTTPS or SSH. |
| Check identity configuration | `git config --global --get user.name` | `git config --global --get user.email` | Before making commits on a new machine. | Reads Git configuration values. | Safe read-only command. |
| Set commit identity | `git config --global user.name "<name>"` | `git config --global user.name "Alex Rivera"` | On a new workstation or account. | Sets the author name for future commits in the global config. | Use repository-local config without `--global` for work/personal separation. |
| Create a feature branch | `git switch -c <branch>` | `git switch -c feature/login-audit` | Before starting a focused change. | Creates and checks out a new branch. | Branch from the intended base branch. |
| Sync base branch safely | `git fetch` then `git switch <base>` then `git pull --ff-only` | `git fetch origin` | Before starting or updating feature work. | Downloads remote changes, switches to base, and fast-forwards if possible. | `--ff-only` refuses unexpected merge commits. |
| Rebase feature branch on base | `git rebase <base>` | `git rebase origin/main` | For local feature commits that have not been shared or that the team agrees can be rewritten. | Replays your commits on top of a newer base. | Do not rebase shared commits that others may have based work on. |
| Merge base branch into feature branch | `git merge <base>` | `git merge origin/main` | When preserving exact branch history matters or rewriting is not allowed. | Creates a merge commit if histories diverged. | Resolve conflicts carefully, then commit the merge. |
| Review your branch against base | `git diff <base>...HEAD` | `git diff origin/main...HEAD` | Before opening a pull request. | Shows changes introduced by your branch since the merge base. | Safe read-only command. |
| List branch commits not on base | `git log <base>..HEAD --oneline` | `git log origin/main..HEAD --oneline` | Before review or rebase. | Lists commits reachable from your branch but not the base. | Safe read-only command. |
| Push a new branch | `git push -u origin HEAD` | `git push -u origin HEAD` | First remote publish of a branch. | Pushes current branch and configures upstream tracking. | Confirm branch name before pushing. |
| Update a pull request branch | `git push` | `git push` | After more commits on a branch with upstream tracking. | Uploads new commits to the tracked remote branch. | If rejected, fetch first and inspect remote changes. |
| Make a release tag | `git tag -a <tag> -m "<message>"` | `git tag -a v1.2.0 -m "Release v1.2.0"` | When marking an official release. | Creates an annotated tag with metadata and message. | Push tags intentionally with `git push origin <tag>`. |
| Push a tag | `git push origin <tag>` | `git push origin v1.2.0` | After creating a release tag locally. | Uploads the tag to the remote. | Avoid `git push --tags` unless you intend to publish every local tag. |
| Save work before context switching | `git stash push -m "<message>"` | `git stash push -m "checkout before hotfix"` | When switching tasks without committing incomplete work. | Saves tracked local changes outside the branch history. | Include `-u` only when you also need untracked files. |
| Work on two branches at once | `git worktree add <path> <branch>` | `git worktree add ../project-hotfix hotfix/login` | When you need separate working directories for parallel branches. | Creates another working tree connected to the same repository. | Keep each worktree on a different branch. |
| Remove a worktree | `git worktree remove <path>` | `git worktree remove ../project-hotfix` | When a linked working tree is no longer needed. | Removes the linked worktree directory and metadata. | Commit, stash, or discard local changes first. |
| Inspect a remote URL | `git remote -v` | `git remote -v` | When checking where fetches and pushes go. | Lists remotes and their fetch/push URLs. | Safe read-only command. |
| Change a remote URL | `git remote set-url <name> <url>` | `git remote set-url origin git@github.com:example/project.git` | When switching between HTTPS and SSH or moving repositories. | Updates the configured remote URL. | Verify the target before pushing. |
| Remove tracked files that should be ignored | `git rm --cached <path>` | `git rm --cached .env` | After adding a file to `.gitignore` that was already tracked. | Removes the file from Git tracking while leaving it in the working tree. | Commit the change and make sure secrets are rotated if they were exposed. |

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
