# GitHub Actions workflow structure

## Purpose

Use this page to understand the structure of workflow YAML files and where each key belongs.

## Workflow file location

| Item | Standard |
| --- | --- |
| Directory | `.github/workflows/` |
| File extension | `.yml` or `.yaml` |
| File purpose | One automated workflow per file |
| Common naming | `ci.yml`, `deploy.yml`, `release.yml`, `terraform-plan.yml` |

### Workflow file path

```text
.github/
  workflows/
    ci.yml
    deploy.yml
```

How it works: GitHub scans `.github/workflows/` for workflow files. Each valid YAML file can define a separate automation.

What it does: keeps CI, deployment, release, and maintenance automation close to the repository.

## Common top-level keys

| Key | Use | Notes |
| --- | --- | --- |
| `name` | Human-readable workflow name. | Shows in the Actions tab. |
| `on` | Events that trigger the workflow. | Can be simple or deeply filtered. |
| `permissions` | Default `GITHUB_TOKEN` permissions. | Prefer least privilege. |
| `env` | Environment variables shared by jobs. | Do not store secrets here directly. |
| `defaults` | Default shell or working directory. | Useful for monorepos. |
| `concurrency` | Prevent overlapping runs. | Good for deploy workflows. |
| `jobs` | Job definitions. | Required for useful workflows. |

### Minimal top-level structure

```yaml
name: CI

on:
  pull_request:
  push:
    branches:
      - main

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm test
```

How it works: `on` defines triggers, `permissions` limits token access, and `jobs` defines the work GitHub schedules.

What it does: runs tests for pull requests and pushes to `main` with read-only repository access.

## Triggers

| Trigger | When it runs | Common use |
| --- | --- | --- |
| `push` | Code is pushed to matching refs. | CI on `main` or release branches. |
| `pull_request` | Pull request activity happens. | Validate proposed changes. |
| `workflow_dispatch` | User or CLI manually starts a workflow. | Manual deploys, maintenance, one-off jobs. |
| `schedule` | Cron schedule is reached. | Nightly scans, dependency checks. |
| `workflow_call` | Another workflow calls this workflow. | Reusable workflows. |
| `workflow_run` | Another workflow completes or is requested. | Follow-up automation. |

### Filter events

```yaml
on:
  push:
    branches:
      - main
    paths:
      - "src/**"
      - ".github/workflows/ci.yml"
```

How it works: GitHub only starts this workflow for pushes to `main` that touch one of the listed paths.

What it does: avoids running CI when unrelated files change.

## Jobs

| Key | Use | Notes |
| --- | --- | --- |
| `runs-on` | Select runner type. | Example: `ubuntu-latest`. |
| `needs` | Wait for other jobs. | Use for build-then-deploy flow. |
| `if` | Conditionally run a job. | Uses expression syntax. |
| `strategy.matrix` | Run job with multiple values. | Common for versions or operating systems. |
| `timeout-minutes` | Stop stuck jobs. | Helps control cost and noise. |
| `environment` | Use protected deployment environment. | Can require approvals. |
| `permissions` | Override token permissions for one job. | Use least privilege per job. |
| `outputs` | Expose values to downstream jobs. | Requires step outputs. |

### Matrix job

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [20, 22]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
      - run: npm ci
      - run: npm test
```

How it works: GitHub expands the job into one run for each matrix value.

What it does: tests the project against Node.js 20 and 22.

## Steps

| Step key | Use | Notes |
| --- | --- | --- |
| `name` | Human-readable step label. | Helps logs stay readable. |
| `uses` | Run an action. | Pin to a version or SHA. |
| `run` | Run shell commands. | Uses the runner shell. |
| `with` | Pass inputs to an action. | Input names depend on the action. |
| `env` | Set environment variables for the step. | Step-scoped values. |
| `id` | Name a step for outputs. | Required for `steps.<id>.outputs`. |
| `if` | Conditionally run a step. | Useful for branch or result logic. |
| `working-directory` | Run command from a directory. | Useful for monorepos. |

### Action step and shell step

```yaml
steps:
  - name: Check out repository
    uses: actions/checkout@v4

  - name: Run tests
    run: npm test
```

How it works: the first step runs a reusable action. The second step runs a shell command on the runner.

What it does: prepares the code, then runs the test script.

## Concurrency

### Cancel old runs for the same branch

```yaml
concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true
```

How it works: GitHub groups runs by branch ref. When a newer run starts in the same group, GitHub cancels the older in-progress run.

What it does: reduces wasted CI time when developers push several commits quickly.

## Related links

- [Workflow syntax for GitHub Actions](https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions)
- [Expressions](https://docs.github.com/en/actions/concepts/workflows-and-actions/expressions)
- [Back to GitHub Actions](README.md)
- [Back to Git index](../README.md)
- [Back to root index](../../README.md)
