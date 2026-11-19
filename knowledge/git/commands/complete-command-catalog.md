---
type: "How-to Guide"
title: "Complete Git command catalog"
description: "Use this catalog to recognize the Git command surface. Daily users should start with [Daily Git commands](daily-commands.md), [Common Git use cases](common-use-cases.md), and [Solve Git issues](solve-issues.md). This page keeps the complete inventory skimmable by separating command tables from examples."
tags: [git, complete-command-catalog]
status: draft
audience: "Engineering learners and practitioners"
maintainer: "unassigned"
---

# Complete Git command catalog

## Purpose

Use this catalog to recognize the Git command surface. Daily users should start with [Daily Git commands](daily-commands.md), [Common Git use cases](common-use-cases.md), and [Solve Git issues](solve-issues.md). This page keeps the complete inventory skimmable by separating command tables from examples.

> [!IMPORTANT]
> The official Git reference is the source of truth for command behavior. Some commands listed by `git help -a` depend on platform, installed extras, or Git version.

## Contents

- [Main porcelain commands](#main-porcelain-commands)
- [Ancillary commands](#ancillary-commands)
- [Interacting with other systems](#interacting-with-other-systems)
- [Low-level manipulators](plumbing-and-internal-commands.md#low-level-manipulators)
- [Low-level interrogators](plumbing-and-internal-commands.md#low-level-interrogators)
- [Server and protocol commands](plumbing-and-internal-commands.md#server-and-protocol-commands)
- [Internal helpers and repository interfaces](plumbing-and-internal-commands.md#internal-helpers-and-repository-interfaces)
- [Developer-facing formats and protocols](plumbing-and-internal-commands.md#developer-facing-formats-and-protocols)
- [Local external helpers shown by this workstation](plumbing-and-internal-commands.md#local-external-helpers-shown-by-this-workstation)
- [Related links](#related-links)

## Main porcelain commands

| Command | Use | Notes |
| --- | --- | --- |
| `git add` | Stage file content. | Run again after later edits. |
| `git am` | Apply mailbox patches as commits. | Common in email patch workflows. |
| `git archive` | Export files from a commit or tree. | Does not include `.git` metadata. |
| `git backfill` | Download missing objects in a partial clone. | Newer command; check local Git support. |
| `git bisect` | Find the commit that introduced a bug. | Requires reliable good/bad tests. |
| `git branch` | List, create, rename, or delete branches. | Deleting branches can hide work until reflog recovery. |
| `git bundle` | Package refs and objects into one file. | Useful for offline transfer or backup. |
| `git checkout` | Legacy branch switching or file restore. | Prefer `git switch` and `git restore` for clarity. |
| `git cherry-pick` | Apply one existing commit elsewhere. | Can duplicate changes if used casually. |
| `git citool` | Graphical commit interface. | Availability depends on installation. |
| `git clean` | Remove untracked files. | Destructive; preview with `-n`. |
| `git clone` | Copy an existing repository. | Use trusted URLs. |
| `git commit` | Record staged content. | Review `git diff --staged` first. |
| `git describe` | Give an object a human-readable name. | Output depends on available tags. |
| `git diff` | Compare changes. | Safe read-only unless paired with external tools that edit. |
| `git fetch` | Download remote refs and objects. | Does not update the current branch. |
| `git format-patch` | Create patch files from commits. | Review patches before sharing. |
| `git gc` | Clean and pack repository data. | Avoid aggressive pruning unless you understand reachability. |
| `git gitk` | Browse history graphically. | GUI availability depends on installation. |
| `git grep` | Search tracked content. | Safe read-only command. |
| `git gui` | Portable graphical Git interface. | Availability depends on installation. |
| `git history` | Experimental history rewrite command. | Experimental; avoid in shared repositories. |
| `git init` | Create or reinitialize a repository. | Does not commit files automatically. |
| `git log` | Show commit history. | Safe read-only command. |
| `git maintenance` | Run repository maintenance tasks. | Prefer defaults unless tuning is needed. |
| `git merge` | Join histories. | Resolve conflicts carefully. |
| `git mv` | Move or rename tracked paths. | Stages the move. |
| `git notes` | Attach notes to objects. | Notes need explicit sharing. |
| `git pull` | Fetch and integrate remote changes. | `--ff-only` is safer for routine pulls. |
| `git push` | Upload refs and objects. | Avoid force pushing shared history without agreement. |
| `git range-diff` | Compare two commit ranges. | Excellent after rebasing a patch series. |
| `git rebase` | Replay commits onto another base. | Do not rebase shared commits others may depend on. |
| `git reset` | Move `HEAD`, index, and sometimes working tree. | `--hard` is destructive. |
| `git restore` | Restore files or index entries. | Destructive when discarding unstaged edits. |
| `git revert` | Create a commit that reverses another commit. | Preferred for public history. |
| `git rm` | Remove paths from index and possibly working tree. | `--cached` keeps the local file. |
| `git scalar` | Manage large Git repositories. | Check platform and team guidance. |
| `git shortlog` | Summarize commit log by author. | Good for release notes. |
| `git show` | Show commits, tags, trees, or blobs. | Safe read-only command. |
| `git sparse-checkout` | Limit working tree paths. | Tooling may expect full checkouts. |
| `git stash` | Save temporary dirty working tree state. | Use messages so stashes are recognizable. |
| `git status` | Show working tree state. | Make this a first habit. |
| `git submodule` | Manage nested repositories. | Adds workflow complexity. |
| `git survey` | Measure repository dimensions of scale. | Experimental; output may change. |
| `git switch` | Switch branches. | Clearer than checkout for branch movement. |
| `git tag` | Create, list, delete, or verify tags. | Push tags intentionally. |
| `git worktree` | Manage multiple working trees. | Keep each worktree on a different branch. |

### Main porcelain examples

```bash
git status --short --branch
git add -p
git commit -m "Describe the change"
git fetch --all --prune
git pull --ff-only
git push -u origin HEAD
```

What it does: these are the normal day-to-day commands for checking state, staging carefully, committing, syncing, and publishing branch work.

```bash
git rebase origin/main
git range-diff origin/main..v1 origin/main..v2
git revert abc1234
```

What it does: these commands reshape or compare history. Prefer `git revert` for shared mistakes, and only rebase commits that are safe to rewrite.

## Ancillary commands

| Command | Use | Notes |
| --- | --- | --- |
| `git config` | Read or set repository, global, or system options. | Know which config level you are editing. |
| `git fast-export` | Export history as a fast-import stream. | Migration/tooling command. |
| `git fast-import` | Import fast-import formatted history. | Can create many refs and objects. |
| `git filter-branch` | Legacy history rewrite tool. | High risk; prefer modern alternatives when available. |
| `git mergetool` | Open a merge conflict tool. | Review results before staging. |
| `git pack-refs` | Pack loose refs. | Mostly administrative. |
| `git prune` | Remove unreachable loose objects. | Prefer `git gc` for normal cleanup. |
| `git reflog` | Inspect recent ref movements. | Important recovery tool. |
| `git refs` | Low-level access to refs. | Advanced and version-dependent. |
| `git remote` | Manage remote repositories. | Verify URLs before pushing. |
| `git repack` | Repack object database. | Prefer `git gc` unless administering repositories. |
| `git replace` | Replace one object with another locally. | Can make history look different. |
| `git annotate` | Show line attribution. | Prefer `git blame` for common use. |
| `git blame` | Show last commit for each line. | Use for context, not blame in the human sense. |
| `git bugreport` | Collect bug report information. | Review before sharing. |
| `git count-objects` | Count loose objects and disk use. | Safe read-only command. |
| `git diagnose` | Create diagnostic archive. | Review before sharing. |
| `git difftool` | Open an external diff tool. | Tool may create temporary files. |
| `git fsck` | Verify object connectivity and validity. | Read-only by default. |
| `git gitweb` | Git web frontend support. | Server/admin use. |
| `git help` | Show command documentation. | Safe read-only command. |
| `git instaweb` | Start temporary gitweb browser. | Opens a local service. |
| `git merge-tree` | Calculate a merge without touching worktree. | Useful for analysis. |
| `git rerere` | Reuse recorded conflict resolutions. | Review reused resolutions. |
| `git show-branch` | Show branch relationships. | Safe read-only command. |
| `git verify-commit` | Verify commit signatures. | Requires trust configuration. |
| `git verify-tag` | Verify tag signatures. | Requires trust configuration. |
| `git version` | Show installed Git version. | Useful for support. |
| `git whatchanged` | Legacy log-with-diff view. | Prefer `git log` for most use. |

### Ancillary examples

```bash
git config --global user.email "alex@example.com"
git remote -v
git reflog --date=local
git fsck --full
```

What it does: configures identity, checks remote URLs, reviews recovery history, and validates repository objects.

```bash
git mergetool
git rerere status
git count-objects -vH
git bugreport
```

What it does: helps with conflict resolution, repeated conflicts, repository size checks, and bug reporting.

## Interacting with other systems

| Command | Use | Notes |
| --- | --- | --- |
| `git archimport` | Import GNU Arch history. | Niche migration command. |
| `git cvsexportcommit` | Export one Git commit to CVS. | Legacy interoperability. |
| `git cvsimport` | Import CVS history. | Legacy migration command. |
| `git cvsserver` | Emulate a CVS server from Git. | Legacy interoperability. |
| `git imap-send` | Send patches to an IMAP folder. | Requires mail configuration. |
| `git p4` | Interoperate with Perforce. | Migration or bridge workflow. |
| `git quiltimport` | Import a Quilt patchset. | Niche patch workflow. |
| `git request-pull` | Generate text asking upstream to pull. | Not the same as a GitHub pull request object. |
| `git send-email` | Send patch emails. | Requires careful email setup. |
| `git svn` | Interoperate with Subversion. | Can be slow and workflow-sensitive. |

### External system examples

```bash
git svn clone https://svn.example.org/project
git p4 clone //depot/project
git request-pull v1.0 origin main
```

What it does: bridges Git with older or external source control workflows, or creates pull-request text for distributed projects.

```bash
git format-patch origin/main
git send-email *.patch
```

What it does: creates patch files and sends them for mailing-list based contribution workflows.

## Related pages

Plumbing and internal commands that most people never type have their own page:

- [Git plumbing and internal commands](plumbing-and-internal-commands.md) - Look up Git's low-level, server, protocol, and internal helper commands that scripts and Git itself use.

## Related links

- [Git reference documentation](https://git-scm.com/docs)
- [git command documentation](https://git-scm.com/docs/git)
- [Everyday Git](https://git-scm.com/docs/giteveryday)
- [Back to Git commands](index.md)
- [Back to Git index](../index.md)
- [Back to root index](../../../README.md)
