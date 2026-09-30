---
type: "Explanation"
title: "GitHub Actions workflow structure"
description: "Read a workflow file from its trigger through jobs and steps, and understand how permissions, dependencies, and conditions change what runs."
tags: [git, github-actions, workflow-structure]
status: draft
maturity: draft
audience: "Engineering learners and practitioners"
maintainer: "unassigned"
sources:
  - id: github-workflow-syntax
    resource: https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax
    title: GitHub Docs - Workflow syntax for GitHub Actions
  - id: github-triggering
    resource: https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow
    title: GitHub Docs - Triggering a workflow
  - id: github-token
    resource: https://docs.github.com/en/actions/tutorials/authenticate-with-github_token
    title: GitHub Docs - Use GITHUB_TOKEN for authentication in workflows
  - id: github-checkout
    resource: https://github.com/actions/checkout
    title: actions/checkout - official action repository
  - id: github-setup-node
    resource: https://github.com/actions/setup-node
    title: actions/setup-node - official action repository
---

# GitHub Actions workflow structure

## The idea in plain language

A workflow file tells GitHub **when to start**, **what jobs exist**, and
**what each job does**. Put it under `.github/workflows/` with a `.yml` or
`.yaml` extension. GitHub reads the YAML as nested settings: a step belongs
to a job, and a job belongs to the workflow.[^github-workflow-syntax]

If YAML is new to you, picture labeled boxes inside other boxes. The amount
of indentation tells you which box owns a setting. The label `run` under a
step means “execute this shell command”; `runs-on` under a job means “choose
this runner.” Putting either key at the wrong level changes or invalidates
the workflow.

Read [components and concepts](components-and-concepts.md) first if event,
job, step, or runner is unfamiliar.

## Read one complete file

This is an illustrative workflow for a repository with a Node project at its
root and an `npm test` script. It has not been run in this knowledge-base
repository. A real project should check its Node version, lockfile, script,
and action revisions before copying it.

```yaml
name: Test a proposed change

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
      - name: Check out code
        uses: actions/checkout@v7
      - name: Set up Node
        uses: actions/setup-node@v7
        with:
          node-version: '22'
      - name: Install locked dependencies
        run: npm ci
      - name: Run tests
        run: npm test
```

The top-level `on` field starts a run for pull requests and pushes to
`main`. `permissions` gives the workflow's `GITHUB_TOKEN` read access to
repository contents. The single `test` job uses an Ubuntu runner and runs
four steps in order: fetch code, set up Node, install from the lockfile, and
run the project test script.[^github-workflow-syntax][^github-token]

The checkout action is needed because a runner does not automatically have
your repository files. The official action READMEs currently show
`actions/checkout@v7` and `actions/setup-node@v7`. Their versions and runner
requirements can change, so check those repositories before adopting the
example.[^github-checkout][^github-setup-node]

## The nesting map

```text
.github/workflows/test.yml
  name                    label in the Actions view
  on                      events that can start a run
  permissions             default GITHUB_TOKEN scope
  jobs
    test                  job identifier
      runs-on             runner choice
      steps               ordered list within this job
        uses              reusable action step
        with              inputs to that action
        run               shell command step
```

Text alternative: workflow settings sit at the top of the file; each entry
under `jobs` defines a job; each entry under a job's `steps` is an ordered
action or shell command. GitHub's workflow syntax reference is the source
for valid keys and levels.[^github-workflow-syntax]

## Change the run deliberately

| If you need... | Add or change | Effect |
| --- | --- | --- |
| A manual start | `workflow_dispatch` under `on` | An eligible user can request a run from GitHub or the CLI.[^github-triggering] |
| Another operating system or runtime | `runs-on` or a setup action | Changes the environment in which a job runs. |
| A second independent check | A sibling entry under `jobs` | GitHub can schedule it independently of `test`. |
| A job only after tests pass | `needs: test` on that job | Waits for the named job and normally skips if it fails.[^github-workflow-syntax] |
| A conditional job or step | `if:` at that level | Runs only when the expression matches.[^github-workflow-syntax] |
| A smaller token permission set | `permissions` at workflow or job level | Limits what `GITHUB_TOKEN` can do; choose the scopes the job needs.[^github-token] |

This table shows where to look, not complete syntax for every feature. In
particular, adding a deploy job changes external state. Its credentials,
environment, and approval rules need a separate design; a successful test
job alone does not make deployment safe.

## A common two-job mistake

Suppose a `build` job creates `dist/app.zip`, and `deploy` declares
`needs: build`. The dependency orders the jobs; it does not move the ZIP.
Each job has its own runner. Upload the build result as an artifact and
download it in the later job, or build it again there. See
[components and concepts](components-and-concepts.md) for the artifact and
cache distinction.

Another common mistake is a trigger filter that excludes the change you
care about. If a workflow does not start, inspect `on` before debugging
steps that never ran. A failing step, by contrast, means a run started and
reached that job. GitHub's [trigger guide](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow)
shows event and filter behavior.[^github-triggering]

## Check your understanding

- Which top-level key decides whether a push to `main` starts this file?
- Why does `npm ci` need checkout and a matching lockfile first?
- What changes when a second job adds `needs: test`?
- Where would you narrow `GITHUB_TOKEN` permissions for one job?

## Official documentation for deeper study

- [Workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) lists every supported key, level, and condition.
- [Triggering a workflow](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow) explains event choices and manual starts.
- [Using `GITHUB_TOKEN`](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token) explains token permissions.
- [Official checkout action](https://github.com/actions/checkout) documents action behavior and current examples.
- [Official Node setup action](https://github.com/actions/setup-node) documents supported Node versions and inputs.

See the [GitHub Actions index](index.md) and [examples and use cases](examples-and-use-cases.md).

[^github-workflow-syntax]: [Workflow syntax for GitHub Actions](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax).
[^github-triggering]: [Triggering a workflow](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow).
[^github-token]: [Use `GITHUB_TOKEN` for authentication](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token).
[^github-checkout]: [Official `actions/checkout` repository](https://github.com/actions/checkout).
[^github-setup-node]: [Official `actions/setup-node` repository](https://github.com/actions/setup-node).
