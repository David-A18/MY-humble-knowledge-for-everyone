# Git troubleshooting commands

## Purpose

Use this page to diagnose why Git is behaving unexpectedly before choosing a fix.

## First checks

| Task | Command | When to use it |
| --- | --- | --- |
| Check repository state | `git status --short --branch` | First step in almost every Git problem. |
| Inspect branch tracking | `git branch -vv` | Push or pull goes to the wrong branch. |
| Inspect remotes | `git remote -v` | Fetch, pull, or push reaches the wrong repository. |
| Inspect remote refs | `git ls-remote <remote>` | A branch or tag exists remotely but not locally. |
| Update remote-tracking refs | `git fetch --all --prune` | Local remote branch list is stale. |

### Start with repository state

```bash
git status --short --branch
git branch -vv
git remote -v
```

What it does: shows your current branch, file state, upstream tracking, ahead/behind counts, and remote URLs.

### Refresh remote information

```bash
git ls-remote origin
git fetch --all --prune
```

What it does: checks what refs the remote advertises, then updates local remote-tracking refs without changing your current branch.

## Push, pull, and branch problems

| Task | Command | When to use it |
| --- | --- | --- |
| Diagnose rejected push | `git log --oneline --left-right --graph HEAD...@{upstream}` | Push is rejected because histories diverged. |
| Diagnose detached HEAD | `git symbolic-ref --short HEAD` | You are not sure whether you are on a branch. |
| Find current commit | `git rev-parse --short HEAD` | You need the exact commit currently checked out. |

### Diagnose diverged history

```bash
git log --oneline --left-right --graph HEAD...@{upstream}
```

What it does: shows commits that exist only locally and only upstream so you can decide whether to merge, rebase, or ask for help.

### Check detached HEAD

```bash
git symbolic-ref --short HEAD
git rev-parse --short HEAD
```

What it does: prints the current branch if `HEAD` is attached, or helps identify the checked-out commit if it is detached.

## Ignore, conflict, and file problems

| Task | Command | When to use it |
| --- | --- | --- |
| Check ignored file rules | `git check-ignore -v <path>` | A file is ignored and you do not know why. |
| See tracked ignored files | `git ls-files -ci --exclude-standard` | `.gitignore` is not stopping files already in Git. |
| Remove a tracked ignored file | `git rm --cached <path>` | A file should stay locally but stop being tracked. |
| Show conflict files | `git diff --name-only --diff-filter=U` | During merge, rebase, or cherry-pick conflicts. |
| Inspect conflict stages | `git ls-files -u` | You need lower-level conflict details. |
| Use a merge tool | `git mergetool` | Conflicts are easier to resolve visually. |
| Reuse conflict resolutions | `git rerere status` | You enabled rerere and want to inspect recorded resolutions. |

### Debug ignore rules

```bash
git check-ignore -v .env
git ls-files -ci --exclude-standard
git rm --cached .env
```

What it does: finds the ignore rule, lists tracked files that match ignore patterns, and removes a tracked file from the index while keeping the local copy.

### Inspect conflicts

```bash
git diff --name-only --diff-filter=U
git ls-files -u
git mergetool
```

What it does: lists unresolved conflict files, shows low-level conflict stages, and opens the configured merge tool.

### Check recorded resolutions

```bash
git rerere status
```

What it does: shows paths where Git may reuse recorded conflict resolutions. Enable rerere intentionally with `git config rerere.enabled true`.

## Credentials, line endings, and hooks

| Task | Command | When to use it |
| --- | --- | --- |
| Diagnose credential helper | `git config --show-origin --get-all credential.helper` | Git repeatedly asks for credentials or uses the wrong helper. |
| Clear bad HTTPS credential | `git credential reject` | A saved password or token is wrong. |
| Check line-ending config | `git config --show-origin --get-regexp core.autocrlf` | Files appear fully changed due to line endings. |
| Renormalize files after attributes change | `git add --renormalize .` | After changing `.gitattributes` line-ending rules. |
| Test hook execution | `git hook run --ignore-missing <hook-name>` | A hook may be affecting commits, merges, or pushes. |
| Bypass local commit hooks once | `git commit --no-verify` | Only when a local hook is broken and team process allows it. |

### Diagnose credentials

```bash
git config --show-origin --get-all credential.helper
git credential reject
```

What it does: shows configured credential helpers and can remove a bad saved credential. Do not paste tokens into command history.

### Fix line-ending noise

```bash
git config --show-origin --get-regexp core.autocrlf
git add --renormalize .
```

What it does: shows line-ending configuration and reapplies normalization rules to tracked files. Review the diff carefully before committing.

### Check hook behavior

```bash
git hook run --ignore-missing pre-commit
git commit --no-verify -m "Emergency docs fix"
```

What it does: tests a hook if it exists. `--no-verify` bypasses local commit hooks once; use it only when the team process allows bypassing.

## Repository health and performance

| Task | Command | When to use it |
| --- | --- | --- |
| Verify repository objects | `git fsck` | You suspect repository corruption or missing objects. |
| Measure object storage | `git count-objects -vH` | Repository feels large or slow. |
| Run maintenance | `git maintenance run` | Repository has many objects or operations are slow. |
| Garbage collect objects | `git gc` | After large history operations or when Git recommends it. |
| Generate a bug report bundle | `git bugreport` | Reporting a Git issue upstream or to platform support. |
| Generate diagnostics archive | `git diagnose` | Support asks for detailed repository diagnostics. |

### Check repository health

```bash
git fsck --full
git count-objects -vH
```

What it does: verifies object connectivity and shows storage statistics for loose objects and packs.

### Run maintenance

```bash
git maintenance run
git gc
```

What it does: runs optimization tasks and packs repository data. Prefer `git maintenance run` for routine use.

### Generate diagnostics

```bash
git bugreport
git diagnose
```

What it does: creates diagnostic output for support or upstream Git bug reports. Review files before sharing them.

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
