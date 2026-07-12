# Daily Git commands

## Purpose

Keep the most common Git commands in one focused reference for day-to-day repository work.

## Quick reference

| Task | Command |
| --- | --- |
| Check current branch and changes | `git status --short --branch` |
| List tracked files | `git ls-files` |
| Show recent commits | `git log --oneline --decorate --graph --max-count=20` |
| Stage a file | `git add path/to/file.md` |
| Commit staged changes | `git commit -m "Describe the change"` |
| Fetch remote updates | `git fetch --all --prune` |
| Push current branch | `git push -u origin HEAD` |

## Inspect repository state

```bash
git status --short --branch
```

Expected output:

```text
## main...origin/main
 M README.md
?? new-file.md
```

## Review changes before committing

```bash
git diff
git diff --staged
```

> [!TIP]
> Review both unstaged and staged changes before committing. It catches accidental edits and keeps commits easier to review.

## Create a branch

```bash
git switch -c feature/example-change
```

## Related links

- [Git command reference](https://git-scm.com/docs)
- [Back to Git commands](README.md)
- [Back to Git index](../README.md)
- [Back to root index](../../README.md)
