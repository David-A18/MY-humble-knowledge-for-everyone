# GitHub Actions

Workflow design, CI/CD patterns, security, command references, action usage, examples, and troubleshooting notes for GitHub Actions.

## Articles

| Article | Purpose |
| --- | --- |
| [Components and concepts](components-and-concepts.md) | Trace one run from event to jobs, steps, and results before learning the YAML syntax. |
| [Workflow structure](workflow-structure.md) | Read one complete YAML file and see how triggers, permissions, jobs, and steps fit. |
| [Inspect an Actions run](commands.md) | Find a run, read its failed job and step, decide whether a fix or rerun is appropriate, and distinguish CLI commands from job files. |
| [`uses` catalog](actions-and-uses-catalog.md) | How `uses:` works, how to navigate action references, and common official, general-purpose, and third-party actions. |
| [Workflow shapes and use cases](examples-and-use-cases.md) | Choose events, jobs, permissions, and evidence for CI, publishing, deployment, maintenance, and Terraform work. |
| [Content CI/CD process](content-ci-cd-process.md) | Follow a knowledge change through `develop` validation, promotion to canonical `main`, and a conditional website update. |
| [Common solutions](common-solutions.md) | Locate the first failed handoff from event to run, job, step, permission, or deployment. |
| [Security, secrets, and permissions](security-secrets-and-permissions.md) | Decide which code a job runs, which credentials it receives, and what those credentials can change. |
| [AWS OIDC federation](aws-oidc-federation.md) | Follow one job's OIDC token through AWS role trust to temporary credentials and limited API access. |

## Recommended learning path

1. Read [Components and concepts](components-and-concepts.md).
2. Read [Workflow structure](workflow-structure.md).
3. Use the [`uses` catalog](actions-and-uses-catalog.md) to choose reusable actions safely.
4. Choose a starting shape from [Workflow shapes and use cases](examples-and-use-cases.md), then adapt its example to your repository.
5. Use [Common solutions](common-solutions.md) when a workflow fails.
6. Review [Security, secrets, and permissions](security-secrets-and-permissions.md) before adding deploys or third-party actions.

## Finding actions

Start with the [`uses` catalog](actions-and-uses-catalog.md) in this repository for general-purpose and common important actions. Then verify the action in its official repository or Marketplace listing before adding it to a workflow.

The catalog is organized by need:

- official GitHub-maintained actions,
- language and runtime setup,
- cloud authentication and deployments,
- Docker and containers,
- quality and security checks,
- release and automation helpers,
- common community actions.

## Official documentation

- [GitHub Actions documentation](https://docs.github.com/actions)
- [GitHub Actions workflow syntax](https://docs.github.com/actions/writing-workflows/workflow-syntax-for-github-actions)
- [GitHub CLI manual](https://cli.github.com/manual/gh)

[Back to Git index](../index.md) | [Back to root index](../../../README.md)
