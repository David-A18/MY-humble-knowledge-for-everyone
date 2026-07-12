# Advanced Git commands

## Purpose

Use this page for professional Git commands that are powerful, useful, and easier to misuse than daily commands.

> [!WARNING]
> Advanced Git commands often rewrite history, change many files, or operate on repository internals. Inspect first, save work, and avoid rewriting commits that other people may have based work on.

## History editing and review

| Task | Command | When to use it |
| --- | --- | --- |
| Rebase local branch | `git rebase <base>` | Keeping local feature commits on top of a newer base. |
| Edit commit series | `git rebase -i <base>` | Squashing, rewording, reordering, or dropping local commits before review. |
| Compare two versions of a branch | `git range-diff <old> <new>` | After rebasing or revising a patch series. |
| Apply one commit elsewhere | `git cherry-pick <commit>` | Backporting or moving a specific commit to another branch. |
| Force push with lease | `git push --force-with-lease` | Updating a remote branch after an agreed history rewrite. |

### Rebase local work

```bash
git rebase origin/main
git rebase -i origin/main
```

What it does: replays local commits on top of another base. Interactive rebase lets you reword, squash, reorder, or drop commits. Do not rebase shared commits that others may have based work on.

### Compare rewritten history

```bash
git range-diff origin/main..v1 origin/main..v2
```

What it does: compares two versions of a commit series by patch identity, which makes it useful after rebasing or revising a branch.

### Move one commit

```bash
git cherry-pick abc1234
```

What it does: applies the changes from an existing commit as a new commit on the current branch.

### Push rewritten history safely

```bash
git push --force-with-lease origin HEAD
```

What it does: force pushes only if the remote still points where your local remote-tracking ref expects. It is safer than `--force`, but it still rewrites public history.

## Debug and search history

| Task | Command | When to use it |
| --- | --- | --- |
| Find the commit that introduced a bug | `git bisect` | A regression exists and you know a good and bad commit. |
| Show line history | `git blame <path>` | Investigating why a line exists. |
| Search tracked content | `git grep <pattern>` | Searching repository files tracked by Git. |
| Reuse recorded conflict resolutions | `git rerere` | Repeated rebases or long-running branches hit the same conflicts. |

### Find a regression

```bash
git bisect start
git bisect bad
git bisect good v1.2.0
```

What it does: binary-searches history until Git finds the first bad commit. Finish with `git bisect reset`.

### Search and inspect history

```bash
git blame src/app.js
git grep "TODO"
```

What it does: `git blame` shows the last commit that changed each line. `git grep` searches tracked files at the current revision.

### Reuse conflict resolutions

```bash
git config rerere.enabled true
git rerere status
```

What it does: records and reapplies previous conflict resolutions. Review auto-applied resolutions before committing.

## Patch, archive, and multi-worktree workflows

| Task | Command | When to use it |
| --- | --- | --- |
| Apply a patch file | `git apply <patch>` | Applying a raw patch without creating a commit automatically. |
| Import mailbox patches | `git am` | Email-based patch workflows. |
| Create patch files | `git format-patch <base>` | Sending a branch as patch files. |
| Send patches by email | `git send-email` | Mailing-list projects that accept patches by email. |
| Maintain several working trees | `git worktree` | Working on multiple branches without stashing. |
| Limit checkout to selected paths | `git sparse-checkout` | Large repositories where you need only part of the tree. |
| Manage nested repositories | `git submodule` | Repository depends on another repository at a fixed commit. |
| Create repository bundle | `git bundle` | Offline transfer or backup of refs and objects. |
| Export a tree archive | `git archive` | Creating source archives without `.git` metadata. |
| Add notes to objects | `git notes` | Adding metadata without changing commits. |

### Apply or create patches

```bash
git apply --check fix.patch
git apply fix.patch
git format-patch origin/main
```

What it does: checks a patch, applies it to the working tree, or creates one patch file per commit.

### Email patch workflow

```bash
git am -3 patches/*.patch
git send-email *.patch
```

What it does: imports patches as commits or sends patch files through email. This is common in mailing-list projects, not most pull-request workflows.

### Work with separate trees

```bash
git worktree add ../repo-hotfix hotfix
git sparse-checkout set docs src
git submodule update --init --recursive
```

What it does: creates another working directory, narrows a checkout to selected paths, or initializes nested repositories.

### Package repository content

```bash
git bundle create backup.bundle --all
git archive --format=zip --output=release.zip HEAD
git notes add -m "Reviewed by security"
```

What it does: creates an offline repository bundle, exports tracked files without `.git` metadata, or attaches notes to objects without changing commits.

## Plumbing and maintenance

| Task | Command | When to use it |
| --- | --- | --- |
| Inspect objects | `git cat-file` | Learning or scripting against Git object data. |
| Inspect tree contents | `git ls-tree` | Listing files in a commit or tree. |
| Compute merge base | `git merge-base <a> <b>` | Scripting comparisons or understanding branch divergence. |
| List commits programmatically | `git rev-list <range>` | Scripts need commit IDs or counts. |
| Parse revisions safely | `git rev-parse <rev>` | Scripts need canonical object IDs or repository paths. |
| List refs with formatting | `git for-each-ref` | Scripts need branch or tag metadata. |
| Update index metadata | `git update-index` | Advanced index changes such as file mode updates. |
| Validate repository objects | `git fsck` | Diagnosing corruption or missing objects. |
| Run cleanup and optimization | `git gc` | After heavy repository maintenance when you understand object reachability. |
| Run background-style maintenance | `git maintenance` | Routine performance maintenance. |
| Rewrite history with old tool | `git filter-branch` | Legacy scripts that still use it. |

### Inspect Git internals

```bash
git cat-file -p HEAD^{tree}
git ls-tree -r --name-only HEAD
git merge-base main feature/login
```

What it does: prints object content, lists tree entries, and finds the best common ancestor between branches.

### Script with revisions and refs

```bash
git rev-list --count origin/main..HEAD
git rev-parse --show-toplevel
git for-each-ref --format="%(refname:short)" refs/heads
```

What it does: counts commits, prints repository metadata, and formats refs for scripts.

### Maintain repository data

```bash
git update-index --chmod=+x script.sh
git fsck --full
git maintenance run
git gc
```

What it does: updates index metadata, verifies object integrity, and runs repository optimization tasks.

### Legacy history rewrite

```bash
git filter-branch --tree-filter "rm -f secret.txt" HEAD
```

What it does: rewrites many commits with a legacy tool. Prefer modern tools such as `git filter-repo` when available, and never rewrite shared history without coordination.

## Advanced safety rules

- Rebase private commits freely; coordinate before rewriting shared history.
- Use `git revert` for public mistakes.
- Prefer `git push --force-with-lease` over `git push --force` when a force push is approved.
- Treat plumbing commands as building blocks for scripts and diagnostics, not normal daily workflow.

## Related links

- [Git reference documentation](https://git-scm.com/docs)
- [Pro Git: Rebasing](https://git-scm.com/book/en/v2/Git-Branching-Rebasing)
- [gitworkflows documentation](https://git-scm.com/docs/gitworkflows)
- [Back to Git commands](README.md)
- [Back to Git index](../README.md)
- [Back to root index](../../README.md)
