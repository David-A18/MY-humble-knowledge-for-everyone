# Undo and recovery

## Purpose

Use Git's inspection tools before undoing work, then choose the least destructive recovery path.

## First checks

- [ ] Run `git status --short --branch`.
- [ ] Review unstaged changes with `git diff`.
- [ ] Review staged changes with `git diff --staged`.
- [ ] Confirm whether the commit was pushed.

## Common recovery commands

| Situation | Safer command | When to use it |
| --- | --- | --- |
| File was staged by mistake | `git restore --staged <path>` | You want to keep the file changes but remove them from the next commit. |
| Unstaged file changes should be discarded | `git restore <path>` | You want the working tree file back to the version in the index. |
| Bad commit was pushed | `git revert <commit>` | You need a public-history-safe undo commit. |
| Commit or branch tip seems lost | `git reflog` | You need to find a previous `HEAD` or branch position. |

### Unstage a file

```bash
git restore --staged path/to/file
```

What it does: removes the file from the staging area while keeping the working tree changes.

### Discard one file's local edits

> [!WARNING]
> `git restore path/to/file` discards unstaged edits in that file. If the file is staged, the working tree is restored from the staged version, not necessarily from `HEAD`.

```bash
git restore path/to/file
```

What it does: replaces the working tree file with the version currently in the index. Use `git restore --source=HEAD path/to/file` when you explicitly want the working tree file restored from the current commit.

### Undo a pushed commit

```bash
git revert abc1234
```

What it does: creates a new commit that reverses the selected commit without rewriting shared history.

### Recover a moved branch tip

```bash
git reflog --date=local
```

What it does: shows recent positions of `HEAD` and branch refs so you can find commits that no longer appear in normal branch history.

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
