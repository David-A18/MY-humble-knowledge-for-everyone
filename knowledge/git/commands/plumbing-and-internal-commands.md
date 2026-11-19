---
type: Reference
title: Git plumbing and internal commands
description: Look up Git's low-level, server, protocol, and internal helper commands that scripts and Git itself use.
tags: [git, commands, plumbing]
status: draft
audience: Engineering learners and practitioners
maintainer: unassigned
---

# Git plumbing and internal commands

These are the low-level commands that Git and automation scripts use under the hood. Everyday work rarely needs them. It is part of [Complete Git command catalog](complete-command-catalog.md).

## Low-level manipulators

| Command | Use | Notes |
| --- | --- | --- |
| `git apply` | Apply or validate raw patches. | Use `--check` before applying. |
| `git checkout-index` | Copy files from index. | Plumbing command. |
| `git commit-graph` | Write or verify commit graph data. | Usually handled by maintenance. |
| `git commit-tree` | Create a commit object directly. | Does not update branch refs by itself. |
| `git hash-object` | Compute or write object IDs. | `-w` writes objects. |
| `git index-pack` | Build index for a packfile. | Administrative/plumbing use. |
| `git merge-file` | Run a three-way file merge. | Can modify files. |
| `git merge-index` | Run merge program for unmerged index entries. | Plumbing command. |
| `git mktag` | Create a validated tag object. | Porcelain `git tag` is safer. |
| `git mktree` | Build a tree object from text. | Plumbing command. |
| `git multi-pack-index` | Write or verify multi-pack indexes. | Usually handled by maintenance. |
| `git pack-objects` | Create packfiles. | Server/admin command. |
| `git prune-packed` | Remove loose objects already in packs. | Usually handled by `git gc`. |
| `git read-tree` | Read tree data into the index. | Can replace index contents. |
| `git replay` | Experimental commit replay. | Prefer `git rebase` unless needed. |
| `git symbolic-ref` | Read or update symbolic refs. | Updating refs manually is advanced. |
| `git unpack-objects` | Unpack objects from a pack. | Plumbing/admin command. |
| `git update-index` | Update index content or metadata. | Do not use as a `.gitignore` substitute. |
| `git update-ref` | Update refs safely from scripts. | Can move branch pointers. |
| `git write-tree` | Create a tree object from the index. | Plumbing command. |

### Low-level manipulator examples

```bash
git apply --check fix.patch
git hash-object README.md
git update-index --chmod=+x script.sh
git write-tree
```

What it does: validates patches, computes object IDs, updates index metadata, and writes a tree object from the index.

## Low-level interrogators

| Command | Use | Notes |
| --- | --- | --- |
| `git cat-file` | Inspect object content, type, or size. | Safe read-only command. |
| `git cherry` | Find commits not yet applied upstream. | Compares patch equivalence. |
| `git diff-files` | Compare working tree and index. | Low-level diff command. |
| `git diff-index` | Compare tree to index or worktree. | Useful in scripts. |
| `git diff-pairs` | Compare provided blob pairs. | Internal/advanced. |
| `git diff-tree` | Compare tree objects. | Useful for scripted commit diffs. |
| `git for-each-ref` | Iterate refs with formatting. | Useful in scripts. |
| `git for-each-repo` | Run Git command across configured repos. | Validate repo list first. |
| `git get-tar-commit-id` | Extract commit ID from `git archive` output. | Safe read-only command. |
| `git last-modified` | Show when files were last modified. | Experimental. |
| `git ls-files` | Show index and tracked file info. | Safe read-only command. |
| `git ls-remote` | List refs in a remote repository. | Safe read-only command. |
| `git ls-tree` | List contents of a tree object. | Safe read-only command. |
| `git merge-base` | Find best common ancestors. | Useful for branch comparison. |
| `git name-rev` | Find symbolic names for revisions. | Safe read-only command. |
| `git pack-redundant` | Find redundant pack files. | Rare admin command. |
| `git repo` | Retrieve repository information. | Version-dependent. |
| `git rev-list` | List commits matching criteria. | Useful in scripts. |
| `git rev-parse` | Parse revisions and repository metadata. | Validate user input in scripts. |
| `git show-index` | Show pack index contents. | Low-level read-only command. |
| `git show-ref` | List local refs. | Safe read-only command. |
| `git unpack-file` | Create temp file with blob content. | Mostly internal. |
| `git var` | Show Git logical variables. | Safe read-only command. |
| `git verify-pack` | Validate packed object files. | Low-level read-only command. |

### Low-level interrogator examples

```bash
git cat-file -p HEAD
git ls-tree -r --name-only HEAD
git merge-base main feature/login
git rev-list --count origin/main..HEAD
git rev-parse --show-toplevel
```

What it does: inspects object content, tree contents, branch ancestry, commit counts, and repository paths.

## Server and protocol commands

| Command | Use | Notes |
| --- | --- | --- |
| `git daemon` | Serve repositories over the Git protocol. | Server administration command. |
| `git fetch-pack` | Receive missing objects from another repository. | Usually invoked by porcelain commands. |
| `git http-backend` | Implement Git over HTTP server side. | Web server configuration required. |
| `git send-pack` | Send objects over Git protocol. | Usually invoked by `git push`. |
| `git update-server-info` | Support dumb HTTP transports. | Server/admin use. |

### Server examples

```bash
git daemon --base-path=/srv/git
git update-server-info
```

What it does: serves Git repositories or updates auxiliary files for simple HTTP hosting. These are server administration commands.

## Internal helpers and repository interfaces

| Command or interface | Use | Notes |
| --- | --- | --- |
| `git check-attr` | Debug `.gitattributes`. | Safe read-only command. |
| `git check-ignore` | Debug `.gitignore`. | Safe read-only command. |
| `git check-mailmap` | Resolve names through mailmap rules. | Safe read-only command. |
| `git check-ref-format` | Validate ref names. | Useful in scripts. |
| `git column` | Display text in columns. | Helper command. |
| `git credential` | Read/write credential protocol records. | Avoid exposing tokens. |
| `git credential-cache` | Temporarily cache credentials in memory. | Stores secrets temporarily. |
| `git credential-store` | Store credentials on disk. | Plain text; prefer OS credential manager. |
| `git fmt-merge-msg` | Produce merge commit messages. | Usually invoked by merge. |
| `git hook` | Run hook commands. | Hook support varies by version. |
| `git interpret-trailers` | Add or parse structured trailers. | Useful for signoffs and review metadata. |
| `git mailinfo` | Extract patch and author data from email. | Usually used by `git am`. |
| `git mailsplit` | Split mbox messages. | Usually used by `git am`. |
| `git merge-one-file` | Merge one conflicted file. | Internal helper. |
| `git patch-id` | Compute stable patch IDs. | Safe read-only command. |
| `git sh-i18n` | Shell translation setup. | Internal helper. |
| `git sh-setup` | Common shell script setup. | Internal helper. |
| `git stripspace` | Remove unnecessary whitespace. | Helper command. |
| `gitattributes` | Define path attributes. | Can affect line endings, diffs, and merges. |
| `gitcli` | Document Git command-line conventions. | Documentation interface. |
| `githooks` | Document hook names and behavior. | Local hooks are not cloned by default. |
| `gitignore` | Define intentionally untracked files. | Does not untrack files already committed. |
| `gitmailmap` | Map names and emails for display. | Does not rewrite commits. |
| `gitmodules` | Define submodule properties. | Keep URLs reviewed and trusted. |
| `gitrepository-layout` | Document `.git` layout. | Documentation interface. |
| `gitrevisions` | Document revision and range syntax. | Essential for safe advanced usage. |

### Interface examples

```bash
git check-ignore -v .env
git check-attr --all README.md
git hook run --ignore-missing pre-commit
git interpret-trailers --parse < commit-message.txt
```

What it does: debugs ignore rules and attributes, tests hooks, and parses structured commit-message trailers.

## Developer-facing formats and protocols

| Interface | Use | Notes |
| --- | --- | --- |
| `gitformat-bundle` | Bundle file format documentation. | Developer-facing docs. |
| `gitformat-chunk` | Chunk-based file format documentation. | Developer-facing docs. |
| `gitformat-commit-graph` | Commit-graph format documentation. | Developer-facing docs. |
| `gitformat-index` | Index file format documentation. | Developer-facing docs. |
| `gitformat-pack` | Pack file format documentation. | Developer-facing docs. |
| `gitformat-signature` | Cryptographic signature format documentation. | Developer-facing docs. |
| `gitprotocol-capabilities` | Protocol v0 and v1 capability docs. | Developer-facing docs. |
| `gitprotocol-common` | Shared protocol concept docs. | Developer-facing docs. |
| `gitprotocol-http` | Git HTTP protocol docs. | Developer-facing docs. |
| `gitprotocol-pack` | Pack transfer protocol docs. | Developer-facing docs. |
| `gitprotocol-v2` | Git wire protocol v2 docs. | Developer-facing docs. |

### Developer documentation examples

```bash
git help format-pack
git help protocol-v2
```

What it does: opens documentation for Git file formats and wire protocols used by Git-compatible tooling.

## Local external helpers shown by this workstation

| Command | Use | Notes |
| --- | --- | --- |
| `git askpass` | Prompt for passwords. | Usually invoked by Git or GUI tools. |
| `git askyesno` | Prompt yes/no in Git for Windows. | Platform-specific helper. |
| `git credential-helper-selector` | Select credential helper. | Git for Windows helper. |
| `git credential-manager` | Manage secure credentials. | Prefer over plain-text credential storage. |
| `git lfs` | Manage Git Large File Storage. | Requires project/server LFS support. |
| `git update-git-for-windows` | Update Git for Windows. | Platform-specific external command. |

### External helper examples

```bash
git credential-manager version
git lfs track "*.zip"
git update-git-for-windows
```

What it does: checks Git Credential Manager, configures Git LFS tracking, or launches the Git for Windows updater.

## Related links

- [Complete Git command catalog](complete-command-catalog.md)
- [Back to index](index.md)
