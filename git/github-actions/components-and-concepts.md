# GitHub Actions components and concepts

## Purpose

Use this page to understand the main building blocks of GitHub Actions before writing or debugging workflow files.

## Core components

| Component | Meaning | Why it matters |
| --- | --- | --- |
| Workflow | An automated process defined in `.github/workflows/*.yml`. | It is the top-level pipeline file GitHub runs. |
| Event | The trigger that starts a workflow. | It decides when automation starts. |
| Job | A group of steps that runs on the same runner. | Jobs can run in parallel or depend on each other. |
| Step | One command or action inside a job. | Steps run in order inside the job. |
| Action | A reusable task called with `uses:`. | Actions avoid rewriting common setup or deployment logic. |
| Runner | The machine that executes jobs. | The runner controls OS, tools, network access, and cost. |
| Context | Structured data available to expressions. | Contexts expose run, repository, matrix, secret, input, and step data. |
| Expression | Dynamic syntax inside `${{ }}`. | Expressions control conditions, values, matrix logic, and outputs. |
| Secret | Encrypted sensitive value. | Secrets protect tokens, passwords, and credentials. |
| Variable | Non-secret configuration value. | Variables keep reusable values out of hardcoded YAML. |
| Artifact | File saved from a workflow run. | Artifacts share build outputs, reports, and packages. |
| Cache | Reused dependency or build data. | Caches speed up repeated workflow runs. |

## Workflow execution model

### Minimal workflow

```yaml
name: CI

on:
  pull_request:
  push:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Run tests
        run: npm test
```

How it works: GitHub watches for the configured events. When a pull request opens or code is pushed to `main`, GitHub creates a workflow run, schedules the `test` job on an Ubuntu runner, and executes each step in order.

What it does: checks out the repository, then runs the test command inside the runner workspace.

## Jobs and steps

| Concept | How it works | Common use |
| --- | --- | --- |
| Sequential steps | Steps in one job run from top to bottom. | Install dependencies, build, then test. |
| Parallel jobs | Jobs without dependencies can run at the same time. | Test Linux, macOS, and Windows together. |
| Dependent jobs | `needs:` makes one job wait for another. | Deploy only after tests pass. |
| Step output | A step can expose a value for later steps. | Reuse a computed version, path, or image tag. |
| Job output | A job can expose values to dependent jobs. | Pass build metadata to deploy jobs. |

### Dependent jobs

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: npm test

  deploy:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - run: ./deploy.sh
```

How it works: `deploy` waits for `test` to complete successfully because it declares `needs: test`.

What it does: prevents deployment when the test job fails.

## Contexts, variables, and expressions

| Item | Syntax | When to use it |
| --- | --- | --- |
| GitHub context | `${{ github.ref }}` | Repository, event, actor, SHA, and ref metadata. |
| Environment variable | `$GITHUB_SHA` or `${{ env.NAME }}` | Values available inside shell commands or workflow YAML. |
| Repository variable | `${{ vars.APP_NAME }}` | Non-secret config shared across workflows. |
| Secret | `${{ secrets.NPM_TOKEN }}` | Sensitive values that must not be printed. |
| Step output | `${{ steps.build.outputs.version }}` | Data created by an earlier step. |
| Matrix value | `${{ matrix.node }}` | Current value in a matrix job. |

### Use contexts and variables

```yaml
env:
  APP_NAME: ${{ vars.APP_NAME }}

jobs:
  print-context:
    runs-on: ubuntu-latest
    steps:
      - name: Show safe metadata
        run: |
          echo "Repository: $GITHUB_REPOSITORY"
          echo "Commit: $GITHUB_SHA"
          echo "App: $APP_NAME"
```

How it works: GitHub evaluates `${{ vars.APP_NAME }}` before the job runs, then injects `APP_NAME` as an environment variable for the shell step.

What it does: prints safe workflow metadata and a repository variable.

> [!WARNING]
> Do not print secrets or entire contexts that may contain sensitive values. Treat `secrets`, tokens, and event payloads carefully.

## Actions and `uses`

| `uses` target | Meaning | Example |
| --- | --- | --- |
| Public action | Action from another repository. | `actions/checkout@v4` |
| Local action | Action stored in the same repository. | `./.github/actions/setup` |
| Reusable workflow | Workflow called from another workflow. | `org/repo/.github/workflows/deploy.yml@v1` |
| Docker action | Action packaged as a container. | `docker://alpine:3.20` |

### Use an action

```yaml
steps:
  - name: Check out repository
    uses: actions/checkout@v4
```

How it works: GitHub downloads the referenced action version and runs the action inside the step.

What it does: checks out the repository into `$GITHUB_WORKSPACE` so later steps can access the code.

## Related links

- [Understanding GitHub Actions](https://docs.github.com/articles/getting-started-with-github-actions)
- [Contexts reference](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts)
- [Variables reference](https://docs.github.com/en/actions/reference/workflows-and-actions/variables)
- [Back to GitHub Actions](README.md)
- [Back to Git index](../README.md)
- [Back to root index](../../README.md)
