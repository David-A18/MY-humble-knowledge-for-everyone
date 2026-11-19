---
type: "Reference"
title: "GitHub Actions `uses` catalog"
description: "Use this page to understand the uses: parameter and find common, general-purpose, and important actions for real workflows."
tags: [git, github-actions, actions-and-uses-catalog]
status: draft
audience: "Engineering learners and practitioners"
maintainer: "unassigned"
---

# GitHub Actions `uses` catalog

## Purpose

Use this page to understand the `uses:` parameter and find common, general-purpose, and important actions for real workflows.

This page is a practical catalog. It explains how to read action references, how to choose a safe action, how to navigate the catalog, and where to find the official source for each action.

> [!IMPORTANT]
> A `uses:` step runs code from an action or calls a reusable workflow. Treat every third-party action like a dependency: read its README, check inputs, review permissions, pin a version, and confirm it is maintained.

## How to navigate this catalog

| Need | Start here | Then check |
| --- | --- | --- |
| Understand `uses:` syntax | [Anatomy of `uses`](#anatomy-of-uses) | [Reference formats](#reference-formats) |
| Pick a normal setup action | [Official GitHub-maintained actions](common-actions-by-category.md#official-github-maintained-actions) | The action README and version tags |
| Add language tooling | [Language and runtime setup actions](common-actions-by-category.md#language-and-runtime-setup-actions) | Cache support and version inputs |
| Add Docker builds | [Docker and container actions](common-actions-by-category.md#docker-and-container-actions) | Registry auth and token permissions |
| Deploy to cloud | [Cloud authentication and deployment actions](common-actions-by-category.md#cloud-authentication-and-deployment-actions) | OIDC setup and environment protection |
| Add security checks | [Quality and security actions](common-actions-by-category.md#quality-and-security-actions) | Required permissions and report output |
| Add release automation | [Release and automation actions](common-actions-by-category.md#release-and-automation-actions) | Tag strategy and write permissions |
| Use community actions | [Common community actions](common-actions-by-category.md#common-community-actions) | Maintainer trust, inputs, and source code |
| Decide if an action is safe | [Selection checklist](#selection-checklist) | [Version pinning guidance](#version-pinning-guidance) |

## Anatomy of `uses`

| Part | Example | Meaning |
| --- | --- | --- |
| Owner | `actions` | GitHub organization or user that owns the action repository. |
| Repository | `checkout` | Repository that contains the action. |
| Path | `.github/workflows/deploy.yml` | Optional path for reusable workflows or actions in subdirectories. |
| Version reference | `@v4` | Branch, tag, or commit SHA to run. |
| Inputs | `with:` | Values passed to the action. |
| Secrets/env | `env:` or `secrets:` | Sensitive or runtime values passed to the step or reusable workflow. |

### Read a normal action reference

```yaml
steps:
  - name: Check out repository
    uses: actions/checkout@v4
```

How it works: `actions` is the owner, `checkout` is the repository, and `v4` is the version reference GitHub resolves.

What it does: downloads and runs the checkout action so later steps can access repository files.

### Pass inputs to an action

```yaml
steps:
  - uses: actions/setup-node@v4
    with:
      node-version: 22
      cache: npm
```

How it works: the `with:` block passes action-specific inputs. Input names and accepted values are defined by the action's `action.yml` and README.

What it does: installs Node.js 22 and enables npm dependency caching.

## Reference formats

| Format | Example | When to use it |
| --- | --- | --- |
| Public action | `owner/repository@version` | Most marketplace and open-source actions. |
| Public action in subdirectory | `owner/repository/path@version` | Monorepos that publish several actions. |
| Same-repository local action | `./.github/actions/setup` | Internal shared logic in the same repository. |
| Reusable workflow | `owner/repository/.github/workflows/file.yml@version` | Reuse a complete workflow as a job. |
| Docker image action | `docker://image:tag` | Run a published container image as an action step. |

### Use a local action

```yaml
steps:
  - name: Run local setup action
    uses: ./.github/actions/setup
```

How it works: GitHub looks for action metadata such as `action.yml` in the local path after the repository is checked out.

What it does: runs reusable automation stored inside the same repository.

> [!IMPORTANT]
> Local actions usually need `actions/checkout` before the local `uses:` step because the runner must have the repository files available.

### Call a reusable workflow

```yaml
jobs:
  deploy:
    uses: organization/platform/.github/workflows/deploy.yml@v1
    with:
      environment: staging
    secrets: inherit
```

How it works: reusable workflows are called at the job level, not inside `steps`. The caller passes inputs and secrets to the called workflow.

What it does: lets teams centralize a full deployment workflow instead of copying jobs into many repositories.

### Run a Docker image as an action

```yaml
steps:
  - name: Run shell in Alpine
    uses: docker://alpine:3.20
    with:
      args: sh -c "echo hello"
```

How it works: GitHub starts the referenced container image for the step.

What it does: runs a command inside a known container image.

## Selection checklist

| Check | Why it matters |
| --- | --- |
| Is the owner trusted? | The action code runs in your workflow. |
| Is the action maintained? | Old actions may use deprecated runtimes or APIs. |
| Does the README explain inputs and outputs? | You need to know what values the action accepts and returns. |
| Does it need secrets? | Secrets increase risk, especially for third-party actions. |
| What permissions does it need? | Prefer actions that work with least privilege. |
| Is it pinned to a version? | Unpinned actions are unstable and unsafe. |
| Does it support your runner OS? | Some actions assume Linux, Docker, or specific tooling. |
| Is there an official alternative? | Official or vendor-maintained actions are usually easier to justify. |

### Evaluate an action before using it

```text
1. Open the action repository or Marketplace page.
2. Read the README inputs, outputs, and examples.
3. Check the latest release or tags.
4. Review requested permissions and required secrets.
5. Pin the action to a version.
6. Add only the minimum token permissions needed by the workflow.
```

How it works: this turns action selection into a dependency review instead of a copy-paste exercise.

What it does: reduces the chance of giving untrusted code unnecessary access.

## Version pinning guidance

| Pin style | Example | Tradeoff |
| --- | --- | --- |
| Major version tag | `actions/checkout@v4` | Convenient and common; receives compatible updates. |
| Full version tag | `docker/build-push-action@v6.5.0` | More repeatable; requires manual updates. |
| Commit SHA | `owner/action@<sha>` | Strongest control for security-sensitive workflows. |
| Branch name | `owner/action@main` | Convenient but risky because it moves. |
| No version | `owner/action` | Do not use; workflow syntax requires a reference for repository actions. |

### Pin an action

```yaml
steps:
  - uses: actions/checkout@v4
```

How it works: GitHub resolves the version after `@` and runs that action revision.

What it does: avoids running an unversioned moving target.

> [!WARNING]
> Third-party actions execute code in your workflow. Review the source, permissions, inputs, and maintenance before using them.

## Where to find action documentation

| Source | Use it for |
| --- | --- |
| GitHub Marketplace listing | Quick install snippet, summary, and owner details. |
| Action repository README | Inputs, outputs, permissions, examples, and version guidance. |
| Releases or tags page | Available versions to pin. |
| `action.yml` or `action.yaml` | The exact inputs, outputs, branding, and runtime. |
| Security tab and issues | Maintenance and vulnerability signals. |
| Dependency graph | Visibility into actions referenced by workflows. |

### Inspect an action before adding it

```text
Repository page:
  README.md
  action.yml
  releases/tags
  issues
  security
```

How it works: the README explains intended use, while `action.yml` defines the action contract GitHub reads.

What it does: helps you confirm the action does what the catalog says before you give it access to your workflow.

## Related pages

The catalog of common actions, grouped by job, has its own page:

- [Common GitHub Actions by category](common-actions-by-category.md) - Find widely used GitHub Actions for setup, cloud authentication, containers, quality and security, releases, and community tasks.

## Related links

- [GitHub Actions documentation](https://docs.github.com/actions)
- [Workflow syntax: `jobs.<job_id>.steps[*].uses`](https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions#jobsjob_idstepsuses)
- [Using pre-written building blocks in your workflow](https://docs.github.com/actions/writing-workflows/choosing-what-your-workflow-does/using-pre-written-building-blocks-in-your-workflow)
- [About custom actions](https://docs.github.com/actions/creating-actions/about-custom-actions)
- [Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use)
- [GitHub Marketplace actions](https://github.com/marketplace?type=actions)
- [actions/checkout](https://github.com/actions/checkout)
- [actions/setup-node](https://github.com/actions/setup-node)
- [actions/setup-python](https://github.com/actions/setup-python)
- [actions/cache](https://github.com/actions/cache)
- [aws-actions/configure-aws-credentials](https://github.com/aws-actions/configure-aws-credentials)
- [docker/build-push-action](https://github.com/docker/build-push-action)
- [hashicorp/setup-terraform](https://github.com/hashicorp/setup-terraform)
- [Back to GitHub Actions](index.md)
- [Back to Git index](../index.md)
- [Back to root index](../../../README.md)
