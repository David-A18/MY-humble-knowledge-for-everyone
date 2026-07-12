# Undo and recovery

## Purpose

Use Git's inspection tools before undoing work, then choose the least destructive recovery path.

## First checks

- [ ] Run `git status --short --branch`.
- [ ] Review unstaged changes with `git diff`.
- [ ] Review staged changes with `git diff --staged`.
- [ ] Confirm whether the commit was pushed.

## Common recovery commands

| Situation | Safer command |
| --- | --- |
| Unstage a file | `git restore --staged path/to/file` |
| Discard unstaged changes in one file | `git restore path/to/file` |
| Create a new commit that reverses a pushed commit | `git revert <commit>` |
| Inspect prior branch positions | `git reflog` |

> [!WARNING]
> Avoid history-rewriting commands on shared branches unless the team has agreed on the workflow.

## Decision sequence

1. If changes are unstaged and still needed, commit or stash them before recovery.
2. If changes are staged by mistake, unstage with `git restore --staged`.
3. If a bad commit was pushed, prefer `git revert`.
4. If local history moved unexpectedly, inspect `git reflog` before changing anything else.

## Related links

- [git restore documentation](https://git-scm.com/docs/git-restore)
- [git revert documentation](https://git-scm.com/docs/git-revert)
- [Back to Git troubleshooting](README.md)
- [Back to Git index](../README.md)
- [Back to root index](../../README.md)
