# Complete Git command catalog

## Purpose

Use this catalog to recognize the Git command surface. Daily users should start with [Daily Git commands](daily-commands.md), [Common Git use cases](common-use-cases.md), and [Solve Git issues](solve-issues.md). This page includes uncommon, low-level, server, email, migration, and interface commands so readers know what exists and when it matters.

> [!IMPORTANT]
> The official Git reference is the source of truth for command behavior. Some commands listed by `git help -a` depend on platform, installed extras, or Git version.

## Main porcelain commands

| Task | Command | Example | When to use it | What it does | Risk/notes |
| --- | --- | --- | --- | --- | --- |
| Stage content | `git add` | `git add README.md` | Preparing changes for commit. | Adds file content to the index. | Run again after later edits. |
| Apply mailbox patches | `git am` | `git am -3 patch.mbox` | Email patch workflows. | Applies patches as commits. | Less common in pull-request workflows. |
| Export files from a commit | `git archive` | `git archive --format=zip --output=src.zip HEAD` | Creating source archives. | Writes tracked files from a tree to an archive. | Does not include `.git` metadata or untracked files. |
| Download partial clone objects | `git backfill` | `git backfill` | Partial clone maintenance. | Downloads missing objects in a partial clone. | Newer command; check local Git support. |
| Find bug-introducing commit | `git bisect` | `git bisect start` | Regression investigation. | Binary-searches commit history. | Requires known good/bad commits and repeatable tests. |
| Manage branches | `git branch` | `git branch --all` | Listing, creating, renaming, or deleting branches. | Manages branch refs. | Deleting branches can hide work until recovered with reflog. |
| Bundle repository data | `git bundle` | `git bundle create repo.bundle --all` | Offline transfer or backup. | Packages refs and objects into a file. | Verify bundles before relying on them. |
| Switch or restore paths | `git checkout` | `git checkout main` | Legacy branch switching or file restoration. | Switches branches or restores files. | Prefer `git switch` and `git restore` for clearer intent. |
| Apply a commit elsewhere | `git cherry-pick` | `git cherry-pick abc1234` | Backports or selective commit movement. | Replays one commit as a new commit. | Can duplicate changes if used casually. |
| Graphical commit tool | `git citool` | `git citool` | GUI-based commits. | Opens a graphical interface for committing. | Availability depends on installation. |
| Remove untracked files | `git clean` | `git clean -fdn` | Cleaning generated or untracked files. | Deletes untracked files when run without dry-run. | Use `-n` preview before destructive cleanup. |
| Clone repository | `git clone` | `git clone https://github.com/example/repo.git` | Starting from a remote repository. | Copies repository history and configures a remote. | Use trusted URLs. |
| Record staged snapshot | `git commit` | `git commit -m "Add docs"` | Saving staged changes. | Creates a commit object and advances the branch. | Review staged diff first. |
| Name an object from refs | `git describe` | `git describe --tags` | Build metadata or release labels. | Finds a human-readable name near a commit. | Output depends on available tags. |
| Compare changes | `git diff` | `git diff --staged` | Reviewing file changes. | Shows differences between working tree, index, commits, or trees. | Safe read-only unless used through tools that edit. |
| Download remote refs | `git fetch` | `git fetch --all --prune` | Updating remote-tracking refs. | Downloads objects and refs without integrating them. | Safe default before pull/rebase/merge. |
| Create patch files | `git format-patch` | `git format-patch origin/main` | Email or patch-file submission. | Writes commits as patch files. | Review patch files before sharing. |
| Optimize repository | `git gc` | `git gc` | Repository maintenance. | Cleans and packs repository data. | Avoid aggressive prune unless you understand reachability. |
| Browse repository graphically | `git gitk` | `git gitk --all` | Visual history inspection. | Opens Git's history browser. | GUI availability depends on installation. |
| Search tracked content | `git grep` | `git grep "function"` | Searching repository content. | Searches files known to Git. | Safe read-only command. |
| Graphical Git UI | `git gui` | `git gui` | GUI-based staging and commits. | Opens Git's portable GUI. | Availability depends on installation. |
| Rewrite history experimentally | `git history` | `git history` | Experimental history operations. | Provides experimental history rewrite functionality. | Experimental. Avoid in shared repositories. |
| Initialize repository | `git init` | `git init` | Starting version control in a folder. | Creates or reinitializes repository metadata. | Does not commit files automatically. |
| Show commit history | `git log` | `git log --oneline --graph` | Reviewing history. | Lists commits and metadata. | Safe read-only command. |
| Run maintenance tasks | `git maintenance` | `git maintenance run` | Keeping large repos healthy. | Runs configured optimization tasks. | Prefer defaults unless tuning is needed. |
| Join histories | `git merge` | `git merge origin/main` | Integrating branches while preserving history. | Combines histories, often with a merge commit. | Resolve conflicts carefully. |
| Move or rename tracked paths | `git mv` | `git mv old.md new.md` | Renaming tracked files. | Moves file in working tree and stages the change. | Equivalent to move plus `git add`/`git rm`. |
| Attach notes to objects | `git notes` | `git notes add -m "Reviewed"` | Adding metadata without changing commits. | Stores notes in separate refs. | Notes need explicit sharing. |
| Fetch and integrate | `git pull` | `git pull --ff-only` | Updating current branch from upstream. | Runs fetch followed by merge or rebase. | Use `--ff-only` for safer routine pulls. |
| Upload refs | `git push` | `git push -u origin HEAD` | Sharing commits or tags. | Sends objects and updates remote refs. | Avoid force pushing shared history without agreement. |
| Compare commit ranges | `git range-diff` | `git range-diff v1 v2` | Reviewing revised patch series. | Compares two commit ranges by patch identity. | Safe read-only command. |
| Reapply commits | `git rebase` | `git rebase origin/main` | Moving local commits to a new base. | Rewrites commits onto another base. | Do not rebase shared commits others may depend on. |
| Move HEAD or index | `git reset` | `git reset --soft HEAD~1` | Reworking local commits or index state. | Moves branch, index, and optionally working tree depending on mode. | `--hard` is destructive. |
| Restore files | `git restore` | `git restore --staged README.md` | Undoing file or index changes. | Restores paths from index or a commit. | Destructive when discarding unstaged edits. |
| Revert commits | `git revert` | `git revert abc1234` | Undoing shared commits. | Creates a new commit that reverses another commit. | Preferred for public history. |
| Remove tracked paths | `git rm` | `git rm --cached .env` | Stop tracking or delete files. | Removes paths from index and optionally working tree. | `--cached` keeps local file; without it deletes file. |
| Manage large repositories | `git scalar` | `git scalar register` | Large monorepo workflows. | Configures performance-oriented repository management. | Check platform and team guidance. |
| Summarize log output | `git shortlog` | `git shortlog -sn` | Release notes or contributor summaries. | Groups commits by author. | Safe read-only command. |
| Show object details | `git show` | `git show HEAD` | Inspecting commits, tags, trees, or blobs. | Displays object content and metadata. | Safe read-only command. |
| Manage sparse checkouts | `git sparse-checkout` | `git sparse-checkout set docs src` | Working with part of a large repository. | Restricts working tree paths. | Tooling may expect a full checkout. |
| Save temporary changes | `git stash` | `git stash push -m "wip"` | Context switching without committing. | Stores dirty working tree state. | Include messages; be careful with untracked files. |
| Show working tree state | `git status` | `git status --short --branch` | Before almost any Git operation. | Shows branch and file states. | Safe read-only command. |
| Manage submodules | `git submodule` | `git submodule update --init --recursive` | Repositories nested at fixed commits. | Initializes, updates, and inspects submodules. | Adds workflow complexity. |
| Measure repository scale | `git survey` | `git survey` | Experimental repository scale diagnostics. | Measures repository dimensions of scale. | Experimental; availability and output may change. |
| Switch branches | `git switch` | `git switch main` | Moving between branches. | Checks out branches with clearer intent than `checkout`. | Git blocks overwrites of local changes. |
| Manage tags | `git tag` | `git tag -a v1.0.0 -m "Release v1.0.0"` | Marking release or important points. | Creates, lists, deletes, or verifies tags. | Push tags intentionally. |
| Manage worktrees | `git worktree` | `git worktree add ../repo-hotfix hotfix` | Multiple branches at once. | Adds or manages linked working trees. | One branch should not be checked out in multiple worktrees. |

## Ancillary commands

| Task | Command | Example | When to use it | What it does | Risk/notes |
| --- | --- | --- | --- | --- | --- |
| Read or set configuration | `git config` | `git config --global user.email "alex@example.com"` | Configuring identity, behavior, aliases, or tools. | Gets and sets Git config values. | Know whether you are editing local, global, or system config. |
| Export Git data stream | `git fast-export` | `git fast-export --all` | Migration or conversion tooling. | Exports repository history in a fast-import stream. | Usually for tools and migrations. |
| Import Git data stream | `git fast-import` | `git fast-import < stream.txt` | Migration or conversion tooling. | Imports fast-import formatted repository data. | Can create many refs and objects. Test first. |
| Rewrite branches with legacy tool | `git filter-branch` | `git filter-branch --index-filter "git rm --cached secret.txt" HEAD` | Legacy history rewriting scripts. | Rewrites commits across history. | Use modern alternatives where possible; high risk. |
| Resolve conflicts with a tool | `git mergetool` | `git mergetool` | Visual conflict resolution. | Launches a configured merge tool. | Review results before staging. |
| Pack refs | `git pack-refs` | `git pack-refs --all` | Repository maintenance or server optimization. | Packs loose refs into a single file. | Mostly administrative. |
| Prune unreachable objects | `git prune` | `git prune --dry-run` | Low-level cleanup after object reachability changes. | Removes unreachable loose objects. | Prefer `git gc`; pruning can remove recovery options. |
| Inspect reflogs | `git reflog` | `git reflog --date=local` | Recovering moved branch tips or lost commits. | Shows recent ref updates. | Read-only unless expiring or deleting entries. |
| Manage refs namespace | `git refs` | `git refs verify` | Low-level ref maintenance. | Provides low-level access to refs. | Advanced and version-dependent. |
| Manage remotes | `git remote` | `git remote -v` | Viewing or changing remote repositories. | Lists, adds, removes, or edits remotes. | Verify URLs before pushing. |
| Repack object database | `git repack` | `git repack -Ad` | Repository/server maintenance. | Packs loose objects into packfiles. | Prefer `git gc` unless administering repositories. |
| Replace objects | `git replace` | `git replace <old> <new>` | Temporary history repair or investigation. | Creates replacement refs for objects. | Can make history look different locally. |
| Annotate lines | `git annotate` | `git annotate README.md` | Similar to blame in older workflows. | Shows commit attribution per line. | Prefer `git blame` for common use. |
| Show line attribution | `git blame` | `git blame README.md` | Investigating line history. | Shows the last commit for each line. | Use for context, not personal blame. |
| Collect Git bug info | `git bugreport` | `git bugreport` | Filing Git bugs. | Creates a diagnostic bug report template. | Review before sharing. |
| Count object storage | `git count-objects` | `git count-objects -vH` | Diagnosing repository size. | Shows loose object and pack statistics. | Safe read-only command. |
| Generate diagnostics | `git diagnose` | `git diagnose` | Support or deep troubleshooting. | Creates diagnostic archive. | Review archive before sharing. |
| Use external diff tool | `git difftool` | `git difftool HEAD~1` | Visual diff inspection. | Opens configured diff tool. | Tool may create temp files. |
| Verify object database | `git fsck` | `git fsck --full` | Suspected corruption. | Checks object connectivity and validity. | Read-only by default. |
| Browse with gitweb | `git gitweb` | `git gitweb` | Web frontend administration. | Supports Git web browsing. | Server/admin use. |
| Show help | `git help` | `git help commit` | Learning command options. | Opens manual pages or help text. | Safe read-only command. |
| Serve repository in browser | `git instaweb` | `git instaweb` | Temporary local web browsing of a repository. | Starts a gitweb instance. | Opens local service; stop when done. |
| Test merges without checkout | `git merge-tree` | `git merge-tree HEAD origin/main` | Predicting merge results. | Performs a merge calculation without touching index or worktree. | Safe for analysis. |
| Reuse conflict resolution | `git rerere` | `git config rerere.enabled true` | Repeated conflicts. | Records and reapplies resolutions. | Review reused resolutions. |
| Compare branches | `git show-branch` | `git show-branch main feature` | Inspecting branch relationships. | Shows commits and branch ancestry. | Safe read-only command. |
| Verify signed commit | `git verify-commit` | `git verify-commit HEAD` | Checking commit signatures. | Validates GPG/SSH signatures on commits. | Requires trust configuration. |
| Verify signed tag | `git verify-tag` | `git verify-tag v1.0.0` | Checking release tag signatures. | Validates tag signatures. | Requires trust configuration. |
| Show Git version | `git version` | `git version` | Reporting local Git version. | Prints installed Git version. | Safe read-only command. |
| Show old-style changed commits | `git whatchanged` | `git whatchanged -p` | Legacy history inspection. | Shows logs with diffs. | Prefer `git log` for most use. |

## Interacting with other systems

| Task | Command | Example | When to use it | What it does | Risk/notes |
| --- | --- | --- | --- | --- | --- |
| Import GNU Arch repository | `git archimport` | `git archimport archive/project` | Migrating from GNU Arch. | Imports Arch history into Git. | Niche migration command. |
| Export commit to CVS checkout | `git cvsexportcommit` | `git cvsexportcommit HEAD` | CVS interoperability. | Applies one Git commit to a CVS checkout. | Legacy system support. |
| Import CVS repository | `git cvsimport` | `git cvsimport project` | Migrating from CVS. | Imports CVS history into Git. | Legacy migration command. |
| Serve CVS protocol from Git | `git cvsserver` | `git cvsserver` | Supporting CVS clients against Git. | Emulates a CVS server. | Legacy interoperability. |
| Send patches to IMAP | `git imap-send` | `git imap-send < patches.mbox` | Email patch workflows. | Uploads patches to an IMAP folder. | Requires mail configuration. |
| Interoperate with Perforce | `git p4` | `git p4 clone //depot/project` | Perforce migration or bridge workflows. | Imports from and submits to Perforce. | Niche external SCM workflow. |
| Import Quilt patches | `git quiltimport` | `git quiltimport` | Quilt patch stack migration. | Applies a quilt patchset to a branch. | Legacy/niche patch workflow. |
| Generate pull request text | `git request-pull` | `git request-pull v1.0 origin main` | Mailing-list or distributed workflows. | Summarizes pending changes for upstream. | Not the same as a GitHub pull request object. |
| Send patch emails | `git send-email` | `git send-email *.patch` | Email-based contribution workflows. | Sends patches as email. | Requires careful email setup. |
| Interoperate with Subversion | `git svn` | `git svn clone https://svn.example.org/project` | SVN migration or bridge workflows. | Provides bidirectional Git/SVN operations. | Can be slow and workflow-sensitive. |

## Low-level commands

| Task | Command | Example | When to use it | What it does | Risk/notes |
| --- | --- | --- | --- | --- | --- |
| Apply patch | `git apply` | `git apply --check fix.patch` | Applying or validating raw patches. | Applies patch files to worktree or index. | Use `--check` before applying. |
| Copy index files out | `git checkout-index` | `git checkout-index -a --prefix=/tmp/export/` | Scripts exporting index content. | Copies files from index to working tree path. | Plumbing command. |
| Manage commit graph | `git commit-graph` | `git commit-graph write --reachable` | Performance maintenance. | Writes or verifies commit-graph data. | Usually handled by maintenance. |
| Create commit object | `git commit-tree` | `git commit-tree HEAD^{tree} -p HEAD` | Low-level scripting. | Creates a commit object from a tree. | Does not update branch refs by itself. |
| Compute object ID | `git hash-object` | `git hash-object README.md` | Object model learning or scripting. | Computes and optionally writes object IDs. | `-w` writes objects. |
| Build pack index | `git index-pack` | `git index-pack packfile.pack` | Packfile maintenance. | Builds index for a packfile. | Administrative/plumbing use. |
| Three-way merge files | `git merge-file` | `git merge-file current base other` | Scripted conflict handling. | Merges three file versions. | Can modify files. |
| Merge index entries | `git merge-index` | `git merge-index git-merge-one-file -a` | Low-level merge machinery. | Runs merge program for unmerged index entries. | Plumbing command. |
| Create validated tag object | `git mktag` | `git mktag < tag-object.txt` | Low-level tag creation. | Creates a tag object with validation. | Porcelain `git tag` is safer. |
| Create tree object | `git mktree` | `git mktree < tree.txt` | Low-level object construction. | Builds a tree from ls-tree formatted input. | Plumbing command. |
| Manage multi-pack index | `git multi-pack-index` | `git multi-pack-index write` | Repository performance maintenance. | Writes or verifies multi-pack-index data. | Usually handled by maintenance. |
| Create packfile | `git pack-objects` | `git pack-objects pack` | Server/admin object packing. | Creates packed object archives. | Plumbing/admin command. |
| Remove duplicate packed objects | `git prune-packed` | `git prune-packed` | Cleanup after packing. | Removes loose objects already in packs. | Usually handled by `git gc`. |
| Read tree into index | `git read-tree` | `git read-tree HEAD` | Low-level index manipulation. | Reads tree data into the index. | Can replace index contents. |
| Replay commits experimentally | `git replay` | `git replay --onto main topic` | Experimental commit replay. | Replays commits on another base, including bare repo flows. | Experimental; prefer `git rebase` unless needed. |
| Manage symbolic refs | `git symbolic-ref` | `git symbolic-ref --short HEAD` | Inspecting or setting symbolic refs. | Reads, modifies, or deletes symbolic refs. | Updating refs manually is advanced. |
| Unpack objects | `git unpack-objects` | `git unpack-objects < packfile.pack` | Repository transfer internals. | Unpacks objects from a pack. | Plumbing/admin command. |
| Update index | `git update-index` | `git update-index --chmod=+x script.sh` | Advanced index edits. | Registers content and metadata in the index. | Do not use as a substitute for `.gitignore`. |
| Update refs safely | `git update-ref` | `git update-ref refs/heads/test HEAD` | Scripts that move refs. | Updates ref values with safety checks. | Can move branch pointers. |
| Write tree object | `git write-tree` | `git write-tree` | Low-level commit construction. | Creates a tree object from the index. | Plumbing command. |
| Inspect object content | `git cat-file` | `git cat-file -p HEAD` | Object model inspection. | Prints object content, type, or size. | Safe read-only command. |
| Find unapplied commits | `git cherry` | `git cherry -v origin/main` | Comparing patch equivalence with upstream. | Shows commits not yet applied upstream. | Safe read-only command. |
| Compare worktree and index | `git diff-files` | `git diff-files` | Low-level diff scripts. | Compares working tree files to index. | Safe read-only command. |
| Compare tree and index/worktree | `git diff-index` | `git diff-index HEAD` | Scripting changed-file detection. | Compares a tree to index or working tree. | Safe read-only command. |
| Compare blob pairs | `git diff-pairs` | `git diff-pairs` | Low-level diff internals. | Compares provided blob pairs. | Internal/advanced. |
| Compare tree objects | `git diff-tree` | `git diff-tree --stat HEAD~1 HEAD` | Scripted commit diffing. | Compares tree objects. | Safe read-only command. |
| Iterate refs | `git for-each-ref` | `git for-each-ref refs/heads` | Scripting branch/tag reports. | Prints refs with formatting. | Safe read-only command. |
| Run command across repositories | `git for-each-repo` | `git for-each-repo --config=maintenance.repo maintenance run` | Multi-repo maintenance. | Runs a Git command for repositories listed in config. | Validate config list first. |
| Extract archive commit ID | `git get-tar-commit-id` | `git get-tar-commit-id < archive.tar` | Inspecting archives made by `git archive`. | Reads embedded commit ID. | Safe read-only command. |
| Show last modified commits | `git last-modified` | `git last-modified README.md` | Experimental file-history queries. | Shows when files were last modified. | Experimental; availability varies. |
| List index files | `git ls-files` | `git ls-files` | Inspecting tracked, staged, or ignored files. | Shows index and working tree file info. | Safe read-only command. |
| List remote refs | `git ls-remote` | `git ls-remote origin` | Checking remote branch/tag names. | Lists refs advertised by a remote. | Safe read-only command. |
| List tree contents | `git ls-tree` | `git ls-tree -r --name-only HEAD` | Inspecting files in a commit. | Lists entries in a tree object. | Safe read-only command. |
| Find merge base | `git merge-base` | `git merge-base main feature` | Comparing branch ancestry. | Finds best common ancestors. | Safe read-only command. |
| Find symbolic names | `git name-rev` | `git name-rev HEAD~3` | Making object IDs human-readable. | Finds ref-based names for revisions. | Safe read-only command. |
| Find redundant packs | `git pack-redundant` | `git pack-redundant --all` | Pack maintenance. | Finds redundant pack files. | Rare admin command. |
| Show repository info | `git repo` | `git repo info` | Repository metadata inspection when available. | Retrieves repository information. | Version-dependent. |
| List commits | `git rev-list` | `git rev-list --count HEAD` | Scripting history traversal. | Lists commit objects matching criteria. | Safe read-only command. |
| Parse revisions | `git rev-parse` | `git rev-parse --show-toplevel` | Scripts needing repository paths or object IDs. | Parses revisions and repository metadata. | Validate user input in scripts. |
| Show pack index | `git show-index` | `git show-index < pack.idx` | Packfile diagnostics. | Shows contents of a pack index. | Low-level read-only command. |
| Show refs | `git show-ref` | `git show-ref --heads` | Inspecting local refs. | Lists refs and object IDs. | Safe read-only command. |
| Unpack blob to temp file | `git unpack-file` | `git unpack-file HEAD:README.md` | Low-level blob extraction. | Creates temporary file with blob content. | Mostly internal. |
| Show logical variable | `git var` | `git var GIT_AUTHOR_IDENT` | Scripting identity or editor info. | Prints Git logical variables. | Safe read-only command. |
| Verify packfile | `git verify-pack` | `git verify-pack -v pack.idx` | Pack diagnostics. | Validates packed object files. | Low-level read-only command. |

## Server and protocol commands

| Task | Command | Example | When to use it | What it does | Risk/notes |
| --- | --- | --- | --- | --- | --- |
| Serve Git protocol | `git daemon` | `git daemon --base-path=/srv/git` | Hosting repositories over the Git protocol. | Starts a simple Git server. | Server administration command. |
| Fetch missing objects | `git fetch-pack` | `git fetch-pack origin` | Protocol-level fetch operations. | Receives missing objects from another repository. | Usually invoked by porcelain commands. |
| Serve Git over HTTP | `git http-backend` | `git http-backend` | Smart HTTP server setup. | Implements server-side HTTP Git protocol. | Web server configuration required. |
| Push objects at protocol level | `git send-pack` | `git send-pack origin refs/heads/main` | Protocol-level push operations. | Sends objects over Git protocol. | Usually invoked by `git push`. |
| Support dumb HTTP transports | `git update-server-info` | `git update-server-info` | Static HTTP repository hosting. | Updates auxiliary info files. | Server/admin use. |

## Internal helpers and repository interfaces

| Task | Command | Example | When to use it | What it does | Risk/notes |
| --- | --- | --- | --- | --- | --- |
| Check attributes | `git check-attr` | `git check-attr --all README.md` | Debugging `.gitattributes`. | Shows attributes that apply to paths. | Safe read-only command. |
| Check ignore rules | `git check-ignore` | `git check-ignore -v .env` | Debugging `.gitignore`. | Shows which ignore rule matches a path. | Safe read-only command. |
| Check mailmap names | `git check-mailmap` | `git check-mailmap "A <a@example.com>"` | Verifying canonical author mapping. | Resolves names through mailmap rules. | Safe read-only command. |
| Validate ref names | `git check-ref-format` | `git check-ref-format refs/heads/feature/a` | Scripts creating refs. | Checks whether a ref name is valid. | Safe read-only command. |
| Format columns | `git column` | `git column --mode=column` | Script/user interface formatting. | Displays text in columns. | Helper command. |
| Handle credentials | `git credential` | `git credential fill` | Credential-helper debugging. | Reads/writes credential protocol records. | Avoid exposing tokens. |
| Cache credentials | `git credential-cache` | `git credential-cache exit` | Temporary in-memory credential storage. | Implements cache credential helper. | Stores secrets temporarily. |
| Store credentials | `git credential-store` | `git credential-store --file ~/.git-credentials store` | Plain-text credential helper workflows. | Stores credentials on disk. | Plain text; use OS credential manager when possible. |
| Format merge message | `git fmt-merge-msg` | `git fmt-merge-msg < .git/FETCH_HEAD` | Merge internals or scripts. | Produces merge commit messages. | Usually invoked by merge. |
| Run hooks | `git hook` | `git hook run --ignore-missing pre-commit` | Testing or running configured hooks. | Runs hook commands. | Hook support varies by version. |
| Parse trailers | `git interpret-trailers` | `git interpret-trailers --parse < commit.txt` | Commit metadata automation. | Adds or parses structured trailers. | Useful for signoffs and review metadata. |
| Extract patch mail info | `git mailinfo` | `git mailinfo msg patch < mail.txt` | Email patch internals. | Extracts patch and authorship from email. | Usually used by `git am`. |
| Split mailbox | `git mailsplit` | `git mailsplit mailbox` | Email patch internals. | Splits mbox into individual messages. | Usually used by `git am`. |
| Merge one conflicted file | `git merge-one-file` | `git merge-one-file` | Merge internals. | Helper used by `git merge-index`. | Internal helper. |
| Compute patch identity | `git patch-id` | `git patch-id < change.patch` | Comparing equivalent patches. | Computes stable patch IDs. | Safe read-only command. |
| Shell i18n helper | `git sh-i18n` | `git sh-i18n` | Git script internals. | Provides translation setup for shell scripts. | Internal helper. |
| Shell setup helper | `git sh-setup` | `git sh-setup` | Git script internals. | Provides common shell script setup. | Internal helper. |
| Strip whitespace | `git stripspace` | `git stripspace < message.txt` | Cleaning commit messages or mail input. | Removes unnecessary whitespace. | Helper command. |
| Define path attributes | `gitattributes` | `.gitattributes` | Line endings, diffs, merge drivers, linguist metadata. | Repository interface file for per-path attributes. | Commit changes intentionally; can affect many files. |
| Understand CLI conventions | `gitcli` | `git help gitcli` | Learning Git command syntax. | Documents command-line conventions. | Documentation interface, not a normal subcommand. |
| Define hooks | `githooks` | `.git/hooks/pre-commit` | Automating local or server checks. | Documents hook names and behavior. | Local hooks are not cloned by default. |
| Ignore untracked files | `gitignore` | `.gitignore` | Keeping build outputs and local config untracked. | Defines ignore patterns. | Does not untrack files already committed. |
| Canonicalize identities | `gitmailmap` | `.mailmap` | Cleaning author names in history views. | Maps names/emails for display. | Does not rewrite commits. |
| Configure submodules | `gitmodules` | `.gitmodules` | Documenting submodule URLs and paths. | Defines submodule configuration stored in the repo. | Keep URLs reviewed and trusted. |
| Understand repository layout | `gitrepository-layout` | `git help repository-layout` | Learning Git internals. | Documents `.git` directory layout. | Documentation interface. |
| Specify revisions | `gitrevisions` | `git help revisions` | Learning revision syntax. | Documents names and ranges such as `HEAD~1` and `main..topic`. | Essential for safe advanced usage. |

## Developer-facing formats and protocols

| Task | Command | Example | When to use it | What it does | Risk/notes |
| --- | --- | --- | --- | --- | --- |
| Understand bundle format | `gitformat-bundle` | `git help format-bundle` | Tooling around bundle files. | Documents Git bundle file format. | Documentation interface. |
| Understand chunk format | `gitformat-chunk` | `git help format-chunk` | Implementing Git-compatible tooling. | Documents chunk-based file formats. | Developer-facing docs. |
| Understand commit-graph format | `gitformat-commit-graph` | `git help format-commit-graph` | Tooling or diagnostics for commit graphs. | Documents commit-graph file format. | Developer-facing docs. |
| Understand index format | `gitformat-index` | `git help format-index` | Tooling around the index. | Documents Git index file format. | Developer-facing docs. |
| Understand pack format | `gitformat-pack` | `git help format-pack` | Packfile tooling or diagnostics. | Documents pack file format. | Developer-facing docs. |
| Understand signature format | `gitformat-signature` | `git help format-signature` | Signature tooling. | Documents Git cryptographic signature formats. | Developer-facing docs. |
| Understand protocol capabilities | `gitprotocol-capabilities` | `git help protocol-capabilities` | Server/client implementation. | Documents protocol v0 and v1 capabilities. | Developer-facing docs. |
| Understand common protocol rules | `gitprotocol-common` | `git help protocol-common` | Protocol implementation. | Documents shared protocol concepts. | Developer-facing docs. |
| Understand HTTP protocol | `gitprotocol-http` | `git help protocol-http` | Git HTTP server/client work. | Documents Git HTTP protocols. | Developer-facing docs. |
| Understand pack protocol | `gitprotocol-pack` | `git help protocol-pack` | Transfer protocol implementation. | Documents pack transfer protocol. | Developer-facing docs. |
| Understand protocol v2 | `gitprotocol-v2` | `git help protocol-v2` | Modern Git protocol implementation. | Documents Git wire protocol v2. | Developer-facing docs. |

## Local external helpers shown by this workstation

| Task | Command | Example | When to use it | What it does | Risk/notes |
| --- | --- | --- | --- | --- | --- |
| Prompt for passwords | `git askpass` | `git askpass` | Credential prompting internals. | External helper for credential prompts. | Usually invoked by Git or GUI tools. |
| Prompt yes/no | `git askyesno` | `git askyesno` | Git for Windows helper prompts. | External helper for yes/no prompts. | Usually invoked by Git tooling. |
| Select credential helper | `git credential-helper-selector` | `git credential-helper-selector` | Git for Windows credential setup. | Helps choose a credential manager. | Platform-specific external helper. |
| Manage credentials | `git credential-manager` | `git credential-manager version` | Git Credential Manager operations. | Manages secure credential storage. | Prefer over plain-text credential storage. |
| Manage large files | `git lfs` | `git lfs track "*.zip"` | Repositories using Git Large File Storage. | Handles large file pointers and LFS transfers. | Requires server/project LFS support. |
| Update Git for Windows | `git update-git-for-windows` | `git update-git-for-windows` | Updating Git for Windows. | Launches Git for Windows updater. | Platform-specific external command. |

## Related links

- [Git reference documentation](https://git-scm.com/docs)
- [git command documentation](https://git-scm.com/docs/git)
- [Everyday Git](https://git-scm.com/docs/giteveryday)
- [Back to Git commands](README.md)
- [Back to Git index](../README.md)
- [Back to root index](../../README.md)
