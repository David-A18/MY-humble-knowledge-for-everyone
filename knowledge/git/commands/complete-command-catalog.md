---
type: Reference
title: Find the right Git command
description: Choose a Git command by the state or task it affects, read its exact manual, and inspect before changing files, commits, or refs.
tags: [git, complete-command-catalog, reference]
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
  - id: git-command-reference
    resource: https://git-scm.com/docs/git
    title: Git command reference
  - id: git-everyday
    resource: https://git-scm.com/docs/giteveryday
    title: Everyday Git
  - id: git-cli
    resource: https://git-scm.com/docs/gitcli
    title: Git command-line conventions
  - id: git-revisions
    resource: https://git-scm.com/docs/gitrevisions
    title: Specifying revisions
  - id: git-status
    resource: https://git-scm.com/docs/git-status
    title: git-status
  - id: git-diff
    resource: https://git-scm.com/docs/git-diff
    title: git-diff
---

# Find the right Git command

## The simple idea

Git commands act on different parts of a repository. Before choosing one,
ask **what state you need to read or change**: files in your working tree,
the staged index, a commit, a branch pointer, or a remote repository. The
same command can have different effects with different options; a command
name alone is not a safety guarantee.[^git-reference][^git-cli]

Think of the working tree as papers on a desk, the index as a tray of
pages selected for the next snapshot, commits as saved snapshots, and
branches as labels pointing to commits. This picture helps locate an
edit. It does not describe every Git detail: a commit also records
parents and metadata, and a remote has its own refs and permissions.
Read [Git fundamentals](../git-fundamentals.md) for the full model.

This is a **task map**, not an exhaustive or version-frozen command list.
Git's [official command reference](https://git-scm.com/docs/git) groups
high-level commands, low-level commands, guides, interfaces, formats, and
protocols. Your installed `git help -a` lists commands available on that
machine; extras and versions differ.[^git-reference]

## Start with the installed manual and current state

These commands identify the Git version, available commands, and
working-tree state without changing repository content:

```bash
git --version
git help -a
git status --short --branch
```

For exact flags and effects, use `git help <command>` or the linked
official manual. If the local help viewer is unavailable, open
[git-scm.com/docs](https://git-scm.com/docs). The examples below use
Git 2.53.0; check your own version before adopting an option.
[^git-reference][^git-status]

## Choose by the question you have

| Question | Start with | What to check before changing anything |
| --- | --- | --- |
| Which files differ, and where? | [`status`](https://git-scm.com/docs/git-status), [`diff`](https://git-scm.com/docs/git-diff) | Separate working-tree changes from staged changes. |
| What did a commit or branch contain? | [`log`](https://git-scm.com/docs/git-log), [`show`](https://git-scm.com/docs/git-show) | Confirm the revision and path you are reading. |
| Which branch or remote am I using? | [`branch`](https://git-scm.com/docs/git-branch), [`remote`](https://git-scm.com/docs/git-remote), [`rev-parse`](https://git-scm.com/docs/git-rev-parse) | Branch name, upstream, and remote URL. |
| How do I select and record edits? | [`add`](https://git-scm.com/docs/git-add), [`commit`](https://git-scm.com/docs/git-commit) | Review the staged diff before committing. |
| How do I move among local branches? | [`switch`](https://git-scm.com/docs/git-switch), [`merge`](https://git-scm.com/docs/git-merge) | Save or resolve unfinished work and know the integration target. |
| How do I receive remote work? | [`fetch`](https://git-scm.com/docs/git-fetch), then inspect; [`pull`](https://git-scm.com/docs/git-pull) if integration is intended | Fetch updates remote-tracking refs; pull also integrates into the current branch. |
| How do I publish a branch or tag? | [`push`](https://git-scm.com/docs/git-push) | Destination remote, destination ref, and whether history would be replaced. |
| How do I undo a mistake? | [`restore`](https://git-scm.com/docs/git-restore), [`revert`](https://git-scm.com/docs/git-revert), [`reset`](https://git-scm.com/docs/git-reset), [`clean`](https://git-scm.com/docs/git-clean) | First locate the mistake in files, index, private history, or shared history. Use the [recovery guide](../troubleshooting/undo-and-recovery.md). |
| How do I find where behavior changed? | [`grep`](https://git-scm.com/docs/git-grep), [`blame`](https://git-scm.com/docs/git-blame), [`bisect`](https://git-scm.com/docs/git-bisect) | Decide whether you need content search, line history, or a repeatable good/bad test. |
| How do I inspect another revision beside unfinished edits? | [`worktree`](https://git-scm.com/docs/git-worktree) | Use the [second-worktree guide](advanced-commands.md) and choose a clean sibling path. |
| How do I diagnose repository object problems? | [`fsck`](https://git-scm.com/docs/git-fsck), [`count-objects`](https://git-scm.com/docs/git-count-objects) | Preserve evidence and backups before maintenance or pruning. |

These are starting routes. The [daily commands guide](daily-commands.md)
walks through a first local commit; [common use cases](common-use-cases.md)
follows a change to review; [solve Git issues](solve-issues.md) helps
choose a recovery path.

## Read one small state example

Suppose `lesson.md` is tracked and you edited it, but have not staged it.
Run:

```bash
git status --short --branch
git diff -- lesson.md
git diff --cached -- lesson.md
```

The two columns in short status describe the index and working tree.
Before staging, the file line is:

```text
 M lesson.md
```

The blank first column and `M` second column mean the working-tree copy
changed while the index copy did not. The first diff shows the edit;
the cached diff is empty. After staging, the file line becomes:

```text
M  lesson.md
```

Now the index changed while the working-tree copy matches it.
[^git-status][^git-diff]

This example was checked in a disposable Git 2.53.0 repository. It does
not imply that every status code is a file modification; conflicts,
renames, untracked files, and submodules have their own forms. Read
Git's [short-status reference](https://git-scm.com/docs/git-status)
when a code is unfamiliar.

## Know which commands can move or discard state

| State touched | Examples | Practical question |
| --- | --- | --- |
| Only read by the command shown | `status`, `diff`, `log`, `show`, `help` | Am I reading the expected repository and revision? |
| Index or files | `add`, `restore`, `clean`, `mv`, `rm` | Which path and which copy will change? |
| Local commits or refs | `commit`, `reset`, `rebase`, `branch`, `tag` | Will this replace commits or move a pointer someone else uses? |
| Remote interaction and local integration | `push`, `fetch`, `pull`, `submodule` | Which remote, ref, and credentials are involved? Will the current branch change? |
| Repository objects or maintenance data | `gc`, `maintenance`, `update-ref`, `prune` | Is this normal maintenance, or do I need a backup and expert diagnosis? |

The table describes common effects, not every option. For example,
`git branch` without arguments lists branches, while deletion options
remove a ref. `git reset` has modes with different effects on `HEAD`,
the index, and working-tree files. Read the exact manual and inspect
the target before using an unfamiliar option.[^git-reference]

## When the command you need is not here

- Use `git help -a` and the [official Git reference](https://git-scm.com/docs/git)
  to find a command by category. The online manual may describe a newer
  version than the one installed locally.
- Read [Git's revision syntax](https://git-scm.com/docs/gitrevisions)
  before supplying ranges such as `main..feature` or `HEAD~1`.
- For scripts that inspect objects or refs, start with
  [`cat-file`](https://git-scm.com/docs/git-cat-file),
  [`ls-tree`](https://git-scm.com/docs/git-ls-tree),
  [`rev-list`](https://git-scm.com/docs/git-rev-list), and
  [`merge-base`](https://git-scm.com/docs/git-merge-base).
  Low-level mutation commands such as `update-ref` need an explicit
  repository-state design, not a copied one-line recipe.
- For email patch, server, migration, and platform-specific helpers,
  use the category links in the [official reference](https://git-scm.com/docs/git)
  and check what your installation actually provides.

## Check your understanding

- If `git diff --cached` is empty but `git diff` shows your edit, where
  is the edit?
- Why does `git fetch` differ from `git pull` for your current branch?
- Why can the same command name be safe to read with one option and
  destructive with another?
- Where would you look for a command absent from this map?

## Official documentation and next routes

- [Git command reference](https://git-scm.com/docs/git) and
  [Everyday Git](https://git-scm.com/docs/giteveryday).
- [Command-line conventions](https://git-scm.com/docs/gitcli) and
  [revision syntax](https://git-scm.com/docs/gitrevisions).
- Return to [Git commands](index.md), [Git](../index.md), or the
  [knowledge index](../../index.md).

[^git-reference]: [Git documentation, git command reference](https://git-scm.com/docs/git).
[^git-cli]: [Git documentation, command-line conventions](https://git-scm.com/docs/gitcli).
[^git-status]: [Git documentation, git-status](https://git-scm.com/docs/git-status).
[^git-diff]: [Git documentation, git-diff](https://git-scm.com/docs/git-diff).
