# GitHub Actions

Workflow design, CI/CD patterns, security, command references, action usage, examples, and troubleshooting notes for GitHub Actions.

## Articles

| Article | Purpose |
| --- | --- |
| [Components and concepts](components-and-concepts.md) | Workflows, events, jobs, steps, runners, contexts, expressions, secrets, variables, artifacts, and actions. |
| [Workflow structure](workflow-structure.md) | Workflow file layout, top-level keys, triggers, jobs, steps, matrix jobs, and concurrency. |
| [Commands](commands.md) | GitHub CLI workflow/run commands and workflow command files such as `$GITHUB_ENV` and `$GITHUB_OUTPUT`. |
| [`uses` catalog](actions-and-uses-catalog.md) | Common official and third-party actions used with the `uses:` argument. |
| [Examples and use cases](examples-and-use-cases.md) | CI, matrix testing, manual deploys, Docker publishing, Terraform checks, AWS OIDC, and scheduled jobs. |
| [Common solutions](common-solutions.md) | Fixes for trigger, checkout, token, secret, OIDC, cache, matrix, concurrency, and debugging problems. |
| [Security, secrets, and permissions](security-secrets-and-permissions.md) | Least-privilege tokens, secrets, variables, environments, OIDC, action pinning, and pull request safety. |

## Recommended learning path

1. Read [Components and concepts](components-and-concepts.md).
2. Read [Workflow structure](workflow-structure.md).
3. Copy a starting point from [Examples and use cases](examples-and-use-cases.md).
4. Use [Common solutions](common-solutions.md) when a workflow fails.
5. Review [Security, secrets, and permissions](security-secrets-and-permissions.md) before adding deploys or third-party actions.

## Official documentation

- [GitHub Actions documentation](https://docs.github.com/actions)
- [GitHub Actions workflow syntax](https://docs.github.com/actions/writing-workflows/workflow-syntax-for-github-actions)
- [GitHub CLI manual](https://cli.github.com/manual/gh)

[Back to Git index](../README.md) | [Back to root index](../../README.md)
