# Complete Git command catalog

## Purpose

Use this catalog to recognize the Git command surface. Daily users should start with [Daily Git commands](daily-commands.md), [Common Git use cases](common-use-cases.md), and [Solve Git issues](solve-issues.md). This page keeps the complete inventory skimmable by separating command tables from examples.

> [!IMPORTANT]
> The official Git reference is the source of truth for command behavior. Some commands listed by `git help -a` depend on platform, installed extras, or Git version.

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

- [Git reference documentation](https://git-scm.com/docs)
- [git command documentation](https://git-scm.com/docs/git)
- [Everyday Git](https://git-scm.com/docs/giteveryday)
- [Back to Git commands](README.md)
- [Back to Git index](../README.md)
- [Back to root index](../../README.md)
