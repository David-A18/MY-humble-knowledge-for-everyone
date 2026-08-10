# Content CI/CD process

## Purpose

This page defines the repository CI/CD process for documentation-only changes. The goal is to keep `main` as the single published source of truth while keeping content updates lightweight.

## Policy

| Rule | Repository standard |
| --- | --- |
| Merge target | Always merge documentation changes into `main`. |
| Review requirement | No required human review for normal content changes. |
| Validation requirement | Run Markdown and link validation before pushing or merging when tooling is available. |
| Branch cleanup | Delete topic branches after their useful content is merged or already covered by `main`. |
| Source of truth | Treat `main` as the canonical branch for readers and future agents. |

> [!IMPORTANT]
> This repository is a content knowledge base, not an application release repository. CI/CD means validating and publishing documentation changes through `main`, not deploying runtime services.

## Branch flow

1. Start from the latest `main`.
2. Make focused content changes on a short-lived branch when useful.
3. Run local validation.
4. Merge the branch into `main` after validation passes.
5. Push `main`.
6. Delete the branch if `main` already contains the useful content.

### Update main before work

```bash
git fetch --all --prune
git switch main
git pull --ff-only
```

What it does: refreshes remote branch knowledge, moves to `main`, and fast-forwards the local branch without creating a merge commit.

### Validate content

```bash
npx markdownlint-cli2 "**/*.md"
```

What it does: runs the repository Markdown lint check against every Markdown file.

If Node tooling is unavailable, inspect the changed Markdown manually and record the missing tool in the handoff.

### Merge a content branch into main

```bash
git switch main
git merge --no-ff <branch-name>
```

What it does: merges the topic branch into `main` while preserving an explicit merge point for the content batch.

> [!WARNING]
> Resolve conflicts by preserving the newest useful documentation, indexes, and changelog entries. Do not accept deletions from older branches when `main` already contains newer expanded content.

### Delete a covered branch

```bash
git branch -d <branch-name>
git push origin --delete <branch-name>
```

What it does: removes a local branch and then removes the remote branch after `main` already contains the useful content.

## Pull request handling

Pull requests are allowed as a packaging mechanism, but they should target `main`. For normal content-only changes, do not require approving reviews. The author or agent is responsible for self-checking the diff, validating links, and confirming parent indexes are updated.

Use reviews only when a change introduces sensitive security guidance, high-risk commands, external product claims that need domain verification, or broad repository workflow changes.

## GitHub settings

If branch protection or repository rules are configured for `main`, use them to require validation checks instead of human approval for normal content changes.

Recommended settings:

- Require status checks for Markdown lint and link validation when those workflows are active.
- Leave required approving reviews disabled for normal documentation changes.
- Keep force pushes disabled on `main`.
- Keep branch deletion disabled for `main`.
- Allow topic branch deletion after merge.

## CI triggers

Documentation validation workflows should run on:

- `pull_request` targeting `main`, when a pull request is used;
- `push` to `main`, after direct or merged content changes land;
- `workflow_dispatch`, for manual validation reruns.

## Related links

- Official documentation: [GitHub Actions events that trigger workflows](https://docs.github.com/actions/reference/workflows-and-actions/events-that-trigger-workflows)
- Official documentation: [GitHub protected branches](https://docs.github.com/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [GitHub Actions examples and use cases](examples-and-use-cases.md)
- [GitHub Actions security, secrets, and permissions](security-secrets-and-permissions.md)
- [Back to GitHub Actions](README.md)
- [Back to Git index](../README.md)
- [Back to root index](../../README.md)
