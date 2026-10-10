# GitHub Actions

Workflow design, CI/CD patterns, security, command references, action usage, examples, and troubleshooting notes for GitHub Actions.

## Articles

| Article | Purpose |
| --- | --- |
| [Components and concepts](components-and-concepts.md) | Trace one run from event to jobs, steps, and results before learning the YAML syntax. |
| [Workflow structure](workflow-structure.md) | Read one complete YAML file and see how triggers, permissions, jobs, and steps fit. |
| [Inspect an Actions run](commands.md) | Find a run, read its failed job and step, decide whether a fix or rerun is appropriate, and distinguish CLI commands from job files. |
| [Choose an action](actions-and-uses-catalog.md) | Read `uses`, find a candidate source, and check its revision, inputs, runner, and authority before adding it. |
| [Workflow shapes and use cases](examples-and-use-cases.md) | Choose events, jobs, permissions, and evidence for CI, publishing, deployment, maintenance, and Terraform work. |
| [Content CI/CD process](content-ci-cd-process.md) | Follow a knowledge change through `develop` validation, promotion to canonical `main`, and a conditional website update. |
| [Common solutions](common-solutions.md) | Locate the first failed handoff from event to run, job, step, permission, or deployment. |
| [Security, secrets, and permissions](security-secrets-and-permissions.md) | Decide which code a job runs, which credentials it receives, and what those credentials can change. |
| [AWS OIDC federation](aws-oidc-federation.md) | Follow one job's OIDC token through AWS role trust to temporary credentials and limited API access. |

## Recommended learning path

1. Read [Components and concepts](components-and-concepts.md).
2. Read [Workflow structure](workflow-structure.md).
3. Read [Security, secrets, and permissions](security-secrets-and-permissions.md) before adding credentials, deploys, or third-party actions.
4. Use [Choose an action](actions-and-uses-catalog.md) to check a reusable dependency before adding it.
5. Choose a starting shape from [Workflow shapes and use cases](examples-and-use-cases.md), then adapt its example to your repository.
6. Use [Common solutions](common-solutions.md) when a workflow fails.

## Finding actions

Start with [Choose an action](actions-and-uses-catalog.md) for common source repositories. Then verify the code, current release, inputs, and permissions in that action's own documentation before adding it to a workflow.

The source map is organized by need:

- repository files, language setup, and dependency review,
- caching and artifacts,
- cloud authentication and infrastructure tooling,
- container registry and image work.

## Official documentation

- [GitHub Actions documentation](https://docs.github.com/actions)
- [GitHub Actions workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
- [GitHub CLI manual](https://cli.github.com/manual/gh)

[Back to Git index](../index.md) | [Back to knowledge index](../../index.md)
