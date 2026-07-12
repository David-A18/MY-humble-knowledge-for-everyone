# Advanced Git commands

## Purpose

Use this page for professional Git commands that are powerful, useful, and easier to misuse than daily commands.

> [!WARNING]
> Advanced Git commands often rewrite history, change many files, or operate on repository internals. Inspect first, save work, and avoid rewriting commits that other people may have based work on.

## Advanced command table

| Task | Command | Example | When to use it | What it does | Risk/notes |
| --- | --- | --- | --- | --- | --- |
| Rebase local branch | `git rebase <base>` | `git rebase origin/main` | Keeping local feature commits on top of a newer base. | Replays commits from the current branch onto the selected base. | Do not rebase shared commits that others may have based work on. |
| Edit commit series | `git rebase -i <base>` | `git rebase -i origin/main` | Squashing, rewording, reordering, or dropping local commits before review. | Opens an interactive todo list for commits after the base. | Rewrites history. Use only on local or agreed-to branches. |
| Compare two versions of a branch | `git range-diff <old> <new>` | `git range-diff origin/main..v1 origin/main..v2` | After rebasing or revising a patch series. | Compares commit ranges by patch identity. | Safe read-only command. Excellent for review. |
| Find the commit that introduced a bug | `git bisect` | `git bisect start` | A regression exists and you know a good and bad commit. | Binary-searches history by repeatedly checking out commits. | Keep test steps reliable. Finish with `git bisect reset`. |
| Show line history | `git blame <path>` | `git blame src/app.js` | Investigating why a line exists. | Shows the last commit that changed each line. | Use as context, not as a people problem. |
| Search tracked content | `git grep <pattern>` | `git grep "TODO"` | Searching repository files tracked by Git. | Searches tracked files at the current revision. | Safe read-only command. |
| Reuse recorded conflict resolutions | `git rerere` | `git config rerere.enabled true` | Repeated rebases or long-running branches hit the same conflicts. | Records and reapplies previous conflict resolutions. | Review auto-applied resolutions before committing. |
| Apply one commit elsewhere | `git cherry-pick <commit>` | `git cherry-pick abc1234` | Backporting or moving a specific commit to another branch. | Applies the changes from an existing commit as a new commit. | Can duplicate changes if used instead of merge/rebase intentionally. |
| Apply a patch file | `git apply <patch>` | `git apply fix.patch` | Applying a raw patch without creating a commit automatically. | Applies patch content to the working tree or index. | Use `git apply --check` first for safety. |
| Import mailbox patches | `git am` | `git am -3 patches/*.patch` | Email-based patch workflows. | Applies patches as commits, preserving author metadata. | Common in mailing-list workflows, less common in pull-request workflows. |
| Create patch files | `git format-patch <base>` | `git format-patch origin/main` | Sending a branch as patch files. | Creates one patch file per commit. | Check recipient workflow before using email patches. |
| Send patches by email | `git send-email` | `git send-email *.patch` | Mailing-list projects that accept patches by email. | Sends patch files with email headers preserved. | Requires email setup. Avoid sending accidental private data. |
| Maintain several working trees | `git worktree` | `git worktree add ../repo-hotfix hotfix` | Working on multiple branches without stashing. | Manages additional working directories backed by one repository. | Each worktree should use a different branch. |
| Limit checkout to selected paths | `git sparse-checkout` | `git sparse-checkout set docs src` | Large repositories where you need only part of the tree. | Configures the working tree to include selected paths. | Coordinate with tooling that expects full checkouts. |
| Manage nested repositories | `git submodule` | `git submodule update --init --recursive` | Repository depends on another repository at a fixed commit. | Initializes, updates, and inspects submodules. | Submodules add workflow complexity. Document expectations clearly. |
| Create repository bundle | `git bundle` | `git bundle create backup.bundle --all` | Offline transfer or backup of refs and objects. | Stores repository objects and refs in a single file. | Verify bundle before relying on it: `git bundle verify backup.bundle`. |
| Export a tree archive | `git archive` | `git archive --format=zip --output=release.zip HEAD` | Creating source archives without `.git` metadata. | Writes files from a tree-ish to an archive. | Does not include untracked files. |
| Add notes to objects | `git notes` | `git notes add -m "Reviewed by security"` | Adding metadata without changing commits. | Stores notes attached to objects. | Notes are separate refs and may need explicit push/fetch. |
| Inspect objects | `git cat-file` | `git cat-file -p HEAD^{tree}` | Learning or scripting against Git object data. | Prints object content, type, or size. | Plumbing command. Safe read-only when used for inspection. |
| Inspect tree contents | `git ls-tree` | `git ls-tree -r --name-only HEAD` | Listing files in a commit or tree. | Shows tree entries for a revision. | Safe read-only command. |
| Compute merge base | `git merge-base <a> <b>` | `git merge-base main feature/login` | Scripting comparisons or understanding branch divergence. | Finds a best common ancestor for commits. | Safe read-only command. |
| List commits programmatically | `git rev-list <range>` | `git rev-list --count origin/main..HEAD` | Scripts need commit IDs or counts. | Walks commit history and prints matching commits. | Safe read-only command. |
| Parse revisions safely | `git rev-parse <rev>` | `git rev-parse --show-toplevel` | Scripts need canonical object IDs or repository paths. | Parses revision names and repository metadata. | Useful in scripts; validate inputs. |
| List refs with formatting | `git for-each-ref` | `git for-each-ref --format="%(refname:short)" refs/heads` | Scripts need branch or tag metadata. | Iterates refs and prints selected fields. | Safe read-only command. |
| Update index metadata | `git update-index` | `git update-index --chmod=+x script.sh` | Advanced index changes such as file mode updates. | Registers file metadata or content changes in the index. | Do not use assume-unchanged or skip-worktree as a substitute for ignoring tracked files. |
| Validate repository objects | `git fsck` | `git fsck --full` | Diagnosing corruption or missing objects. | Verifies object database integrity. | Read-only by default. |
| Run cleanup and optimization | `git gc` | `git gc --prune=now` | After heavy repository maintenance when you understand object reachability. | Packs objects and prunes unreachable objects. | `--prune=now` is aggressive. Prefer default `git gc` or `git maintenance run`. |
| Run background-style maintenance | `git maintenance` | `git maintenance run` | Routine performance maintenance. | Runs configured maintenance tasks such as prefetch or commit-graph updates. | Safer default than custom `git gc` tuning. |
| Rewrite history with old tool | `git filter-branch` | `git filter-branch --tree-filter "rm -f secret.txt" HEAD` | Legacy scripts that still use it. | Rewrites many commits. | Official docs warn users away from this for many cases. Prefer modern tools such as `git filter-repo` when available. |
| Force push with lease | `git push --force-with-lease` | `git push --force-with-lease origin HEAD` | Updating a remote branch after an agreed history rewrite. | Force pushes only if the remote still points where your local remote-tracking ref expects. | Safer than `--force`, but still rewrites public history. |

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
