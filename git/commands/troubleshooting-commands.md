# Git troubleshooting commands

## Purpose

Use this page to diagnose why Git is behaving unexpectedly before choosing a fix.

## Troubleshooting command table

| Task | Command | Example | When to use it | What it does | Risk/notes |
| --- | --- | --- | --- | --- | --- |
| Check repository state | `git status --short --branch` | `git status --short --branch` | First step in almost every Git problem. | Shows branch, upstream, staged, unstaged, untracked, and conflict state. | Safe read-only command. |
| Inspect branch tracking | `git branch -vv` | `git branch -vv` | Push or pull goes to the wrong branch. | Shows local branches, upstream branches, and ahead/behind counts. | Safe read-only command. |
| Inspect remotes | `git remote -v` | `git remote -v` | Fetch, pull, or push reaches the wrong repository. | Lists remote names and URLs. | Safe read-only command. |
| Inspect remote refs | `git ls-remote <remote>` | `git ls-remote origin` | A branch or tag exists remotely but not locally. | Lists refs advertised by the remote. | Safe read-only command. |
| Update remote-tracking refs | `git fetch --all --prune` | `git fetch --all --prune` | Local remote branch list is stale. | Downloads remote refs and removes stale remote-tracking refs. | Does not update the current branch. |
| Diagnose rejected push | `git log --oneline --left-right --graph HEAD...@{upstream}` | `git log --oneline --left-right --graph HEAD...@{upstream}` | Push is rejected because histories diverged. | Shows commits only on local and only on upstream. | Safe read-only command. |
| Check ignored file rules | `git check-ignore -v <path>` | `git check-ignore -v .env` | A file is ignored and you do not know why. | Prints the ignore rule and file that matched. | Safe read-only command. |
| See tracked ignored files | `git ls-files -ci --exclude-standard` | `git ls-files -ci --exclude-standard` | `.gitignore` is not stopping files already in Git. | Lists tracked files that also match ignore rules. | Remove tracking with `git rm --cached <path>` if appropriate. |
| Remove a tracked ignored file | `git rm --cached <path>` | `git rm --cached .env` | A file should stay locally but stop being tracked. | Removes the file from the index, leaving the working copy. | Commit the removal. Rotate secrets if they were committed. |
| Show conflict files | `git diff --name-only --diff-filter=U` | `git diff --name-only --diff-filter=U` | During merge, rebase, or cherry-pick conflicts. | Lists unmerged paths. | Safe read-only command. |
| Inspect conflict stages | `git ls-files -u` | `git ls-files -u` | You need lower-level conflict details. | Shows index entries for base, ours, and theirs. | Advanced read-only command. |
| Use a merge tool | `git mergetool` | `git mergetool` | Conflicts are easier to resolve visually. | Opens the configured merge conflict tool. | Review the result before staging. |
| Reuse conflict resolutions | `git rerere status` | `git rerere status` | You enabled rerere and want to inspect recorded resolutions. | Shows paths where recorded resolutions may apply. | Enable intentionally with `git config rerere.enabled true`. |
| Diagnose detached HEAD | `git symbolic-ref --short HEAD` | `git symbolic-ref --short HEAD` | You are not sure whether you are on a branch. | Prints the current branch name if `HEAD` is attached. | Fails in detached HEAD; use `git switch -c <branch>` to keep work. |
| Find current commit | `git rev-parse --short HEAD` | `git rev-parse --short HEAD` | You need the exact commit currently checked out. | Prints the abbreviated object ID of `HEAD`. | Safe read-only command. |
| Diagnose credential helper | `git config --show-origin --get-all credential.helper` | `git config --show-origin --get-all credential.helper` | Git repeatedly asks for credentials or uses the wrong helper. | Shows configured credential helpers and where they came from. | Do not paste tokens into command history. |
| Clear bad HTTPS credential | `git credential reject` | `git credential reject` | A saved password or token is wrong. | Removes a credential matching protocol/host/user input. | Follow official credential-helper guidance for your OS. |
| Check line-ending config | `git config --show-origin --get-regexp core.autocrlf` | `git config --show-origin --get-regexp core.autocrlf` | Files appear fully changed due to line endings. | Shows line-ending conversion config and source files. | Coordinate `.gitattributes` changes with the team. |
| Renormalize files after attributes change | `git add --renormalize .` | `git add --renormalize .` | After changing `.gitattributes` line-ending rules. | Reapplies clean filters and normalization to tracked files. | Review the diff carefully before committing. |
| Test hook execution | `git hook run --ignore-missing <hook-name>` | `git hook run --ignore-missing pre-commit` | A hook may be affecting commits, merges, or pushes. | Runs a specific hook if it exists and succeeds when it is missing. | Hook support varies by Git version. Inspect `.git/hooks` when needed. |
| Bypass local commit hooks once | `git commit --no-verify` | `git commit --no-verify -m "Emergency docs fix"` | Only when a local hook is broken and the team process allows bypassing. | Commits without running pre-commit and commit-msg hooks. | Do not use to skip required quality checks. |
| Verify repository objects | `git fsck` | `git fsck --full` | You suspect repository corruption or missing objects. | Checks object connectivity and validity. | Read-only by default, but output can be technical. |
| Measure object storage | `git count-objects -vH` | `git count-objects -vH` | Repository feels large or slow. | Shows loose object count and pack size. | Safe read-only command. |
| Run maintenance | `git maintenance run` | `git maintenance run` | Repository has many objects or operations are slow. | Runs configured maintenance tasks. | Usually safe. Let Git choose defaults unless you know the repository needs more. |
| Garbage collect objects | `git gc` | `git gc` | After large history operations or when Git recommends it. | Packs objects and prunes unreachable data according to safety windows. | Avoid interrupting. Prefer `git maintenance run` for routine use. |
| Generate a bug report bundle | `git bugreport` | `git bugreport` | Reporting a Git issue upstream or to platform support. | Creates diagnostic text for a bug report. | Review before sharing; it may include environment details. |
| Generate diagnostics archive | `git diagnose` | `git diagnose` | Support asks for detailed repository diagnostics. | Produces an archive of diagnostic information. | Review before sharing outside your organization. |

## Common troubleshooting sequence

1. Run `git status --short --branch`.
2. Check branch tracking with `git branch -vv`.
3. Fetch with `git fetch --all --prune`.
4. Inspect differences with `git log`, `git diff`, or conflict-specific commands.
5. Choose a safe fix from [Solve Git issues](solve-issues.md).

## Related links

- [Git FAQ](https://git-scm.com/docs/gitfaq)
- [git status documentation](https://git-scm.com/docs/git-status)
- [git fsck documentation](https://git-scm.com/docs/git-fsck)
- [Back to Git commands](README.md)
- [Back to Git index](../README.md)
- [Back to root index](../../README.md)
