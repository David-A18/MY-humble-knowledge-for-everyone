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
  - id: git-help
    resource: https://git-scm.com/docs/git-help
    title: git-help
  - id: git-branch
    resource: https://git-scm.com/docs/git-branch
    title: git-branch
  - id: git-reset
    resource: https://git-scm.com/docs/git-reset
    title: git-reset
  - id: git-switch
    resource: https://git-scm.com/docs/git-switch
    title: git-switch
  - id: git-checkout
    resource: https://git-scm.com/docs/git-checkout
    title: git-checkout
  - id: git-merge
    resource: https://git-scm.com/docs/git-merge
    title: git-merge
  - id: git-rebase
    resource: https://git-scm.com/docs/git-rebase
    title: git-rebase
  - id: git-bisect
    resource: https://git-scm.com/docs/git-bisect
    title: git-bisect
---

# Find the right Git command

## The simple idea

Git commands act on different parts of a repository. Before choosing one,
ask **what state you need to read or change**: files in your working tree,
the staged index, a commit, a branch pointer, or a remote repository. The
same command can have different effects with different options; a command
name alone is not a safety guarantee.

Start with [Git fundamentals](../git-fundamentals.md) if the working
tree, index, commits, and refs are unfamiliar. Its packing-box analogy
shows the current files and saved snapshots, then explains where the
picture breaks: the index is the **full proposed next snapshot**, not
just a list of selected edits. Staging updates the index's copy of a
path; it does not remove other tracked paths from that snapshot. A
remote has its own refs and any access controls set by its host.

This is a **task map**, not an exhaustive or version-frozen command list.
Git's [official command reference](https://git-scm.com/docs/git) groups
high-level commands, low-level commands, guides, interfaces, formats, and
protocols. Your installed `git help -a` lists commands available on that
machine; extras and versions differ.[^git-reference][^git-help]

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
[git-scm.com/docs](https://git-scm.com/docs). The `lesson.md` state
example below was checked with Git 2.53.0; check your own version
before adopting an option.
[^git-reference][^git-help]

## Choose by the question you have

| Question | Start with | What to check before changing anything |
| --- | --- | --- |
| Which files differ, and where? | [`status`](https://git-scm.com/docs/git-status), [`diff`](https://git-scm.com/docs/git-diff) | Separate working-tree changes from staged changes. |
| What did a commit or branch contain? | [`log`](https://git-scm.com/docs/git-log), [`show`](https://git-scm.com/docs/git-show) | Confirm the revision and path you are reading. |
| Which branch or remote am I using? | [`branch -vv`](https://git-scm.com/docs/git-branch), [`remote -v`](https://git-scm.com/docs/git-remote), [`status -sb`](https://git-scm.com/docs/git-status) | Current branch, configured upstream, and remote URL. |
| How do I select and record edits? | [`add`](https://git-scm.com/docs/git-add), [`commit`](https://git-scm.com/docs/git-commit) | Review the staged diff before committing. |
| How do I change the current branch? | [`switch`](https://git-scm.com/docs/git-switch) | By default it can carry non-conflicting edits and refuses if the switch would lose edits; override options change that. Check unfinished work first.[^git-switch] |
| How do I integrate another branch? | [`merge`](https://git-scm.com/docs/git-merge) | Confirm the current branch; merging may fast-forward it, create a merge commit, or stop with conflicts.[^git-merge] |
| How do I replay my branch on a new base? | [`rebase`](https://git-scm.com/docs/git-rebase) | It replaces commits on the current branch; first check whether others already use them.[^git-rebase] |
| How do I receive remote work? | [`fetch`](https://git-scm.com/docs/git-fetch), then inspect; [`pull`](https://git-scm.com/docs/git-pull) if integration is intended | Fetch updates remote-tracking refs; pull also integrates into the current branch. |
| How do I publish a branch or tag? | [`push`](https://git-scm.com/docs/git-push) | Destination remote, destination ref, and whether history would be replaced. |
| How do I undo a mistake? | [`restore`](https://git-scm.com/docs/git-restore), [`revert`](https://git-scm.com/docs/git-revert), [`reset`](https://git-scm.com/docs/git-reset), [`clean`](https://git-scm.com/docs/git-clean), [`reflog`](https://git-scm.com/docs/git-reflog) | Use [Solve Git issues](solve-issues.md) to locate the mistake, then the [recovery guide](../troubleshooting/undo-and-recovery.md) for the scoped procedure. |
| How do I find where behavior changed? | [`grep`](https://git-scm.com/docs/git-grep) for current content, [`log -S`](https://git-scm.com/docs/git-log) or [`blame`](https://git-scm.com/docs/git-blame) for history, [`bisect`](https://git-scm.com/docs/git-bisect) for a repeatable good/bad test | Bisect checks out commits with detached `HEAD`; start with clean work or use a separate worktree, then finish with `git bisect reset`.[^git-bisect] |
| How do I inspect another revision beside unfinished edits? | [`worktree`](https://git-scm.com/docs/git-worktree) | Use the [second-worktree guide](advanced-commands.md) and choose a clean sibling path. |
| How do I diagnose repository object problems? | [`fsck`](https://git-scm.com/docs/git-fsck), [`count-objects`](https://git-scm.com/docs/git-count-objects) | Preserve evidence and backups before maintenance or pruning. |

`git checkout` is an older, multi-purpose command found in many tutorials.
Its branch-switching job is now clearer with `switch`; its file-restoring
job is clearer with `restore`. In particular, do not copy
`git checkout -- <path>` without checking which local edits it would
discard.[^git-checkout]

These are starting routes. The [daily commands guide](daily-commands.md)
walks through a first local commit; [common use cases](common-use-cases.md)
follows a change to review; [solve Git issues](solve-issues.md) helps
choose a recovery path.

Branch and upstream counts shown by `branch -vv` or `status -sb` use your
last fetched remote-tracking refs. They are not a live check of the
remote.[^git-branch][^git-status]

## Read one small state example

Suppose `lesson.md` is tracked and you edited it, but have not staged it.
Run:

```bash
git status --short --branch
git diff -- lesson.md
git diff --cached -- lesson.md
```

For an ordinary tracked path without a conflict, the first short-status
column compares the index with `HEAD`; the second compares the working
tree with the index. The `--branch` option also prints a `##` branch
header above the file lines. Before staging, the file line is:

```text
 M lesson.md
```

The blank first column and `M` second column mean the index still matches
`HEAD`, while the working-tree copy differs from the index. The first
diff shows the edit; the cached diff is empty. Now stage this one path
and repeat the checks:

```bash
git add -- lesson.md
git status --short --branch
git diff -- lesson.md
git diff --cached -- lesson.md
```

After staging, the file line becomes:

```text
M  lesson.md
```

Now the index differs from `HEAD`, while the working-tree copy matches
the index. `git diff -- lesson.md` is empty and the cached diff shows
the staged edit. For `git diff`, `--staged` is another spelling of
`--cached`. The `--` before `lesson.md` separates a path from any
revision arguments.
[^git-status][^git-diff][^git-cli]

This example was checked on 2026-10-07 in a disposable Git 2.53.0
repository. It does not imply that every status code is a file
modification. Conflicts, renames, untracked files, and submodules have
their own forms. Read Git's
[short-status reference](https://git-scm.com/docs/git-status)
when a code is unfamiliar.

## Know which commands can move or discard state

| State touched | Examples | Practical question |
| --- | --- | --- |
| Inspection without changing project content | `status`, `diff`, `log`, `show`, `help` | Am I reading the expected repository and revision? |
| Working tree or index | `add`, `restore`, `clean`, `mv`, `rm` | Which path and which copy will change? |
| Checkout or stashed work | `switch`, `checkout`, `stash` | Will `HEAD`, files, the index, or the stash ref move? |
| Local commits, refs, or checked-out files | `commit`, `commit --amend`, `merge`, `rebase`, `cherry-pick`, `revert`, `reset`, `pull`, `branch`, `tag`, `update-ref` | Will this create or replace commits, move a branch whose commits may be shared, change files, or stop with conflicts? |
| Fetched refs and objects | `fetch` | Which refs will update, and would `--prune` remove stale local remote-tracking refs? |
| Remote refs | `push` | Which repository and ref will change for other people? |
| Nested repository state | `submodule update` | Which submodule worktrees and commits will change? |
| Object maintenance | `gc`, `maintenance`, `prune` | Is this routine maintenance, or could unreachable objects needed for recovery be deleted? |

The table describes common effects, not every option. For example,
`git branch` without arguments lists branches, while deletion options
remove a ref. `git reset` has modes with different effects on `HEAD`,
the index, and working-tree files. Read the exact manual and inspect
the target before using an unfamiliar option.[^git-branch][^git-reset]

`git status` may refresh cached file information in the index even though
it does not change staged content.[^git-status]

## When the command you need is not here

- Use `git help -a` and the [official Git reference](https://git-scm.com/docs/git)
  to find a command by category. The online manual may describe a newer
  version than the one installed locally.
- Read [Git's revision syntax](https://git-scm.com/docs/gitrevisions)
  before supplying names: `HEAD~1` names the first parent of `HEAD`, while
  `main..feature` names a set of commits for `git log`. For `git diff`,
  that two-dot spelling compares the two endpoint snapshots; it is not
  a set of commits.[^git-revisions][^git-diff]
- For scripts that inspect objects or refs, start with
  [`cat-file`](https://git-scm.com/docs/git-cat-file),
  [`ls-tree`](https://git-scm.com/docs/git-ls-tree),
  [`rev-list`](https://git-scm.com/docs/git-rev-list), and
  [`merge-base`](https://git-scm.com/docs/git-merge-base); use
  [`for-each-ref`](https://git-scm.com/docs/git-for-each-ref) to inspect
  refs and `git status --porcelain=v1` for parseable status output.
  When a background script must avoid an optional index write, use
  `git --no-optional-locks status`.[^git-status]
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
[^git-help]: [Git documentation, git-help](https://git-scm.com/docs/git-help), source record `git-help`.
[^git-branch]: [Git documentation, git-branch](https://git-scm.com/docs/git-branch), source record `git-branch`.
[^git-reset]: [Git documentation, git-reset](https://git-scm.com/docs/git-reset), source record `git-reset`.
[^git-switch]: [Git documentation, git-switch](https://git-scm.com/docs/git-switch), source record `git-switch`.
[^git-checkout]: [Git documentation, git-checkout](https://git-scm.com/docs/git-checkout), source record `git-checkout`.
[^git-revisions]: [Git documentation, gitrevisions](https://git-scm.com/docs/gitrevisions), source record `git-revisions`.
[^git-merge]: [Git documentation, git-merge](https://git-scm.com/docs/git-merge), source record `git-merge`.
[^git-rebase]: [Git documentation, git-rebase](https://git-scm.com/docs/git-rebase), source record `git-rebase`.
[^git-bisect]: [Git documentation, git-bisect](https://git-scm.com/docs/git-bisect), source record `git-bisect`.
