---
type: How-to Guide
title: Inspect a GitHub Actions run from the terminal
description: Find a workflow run, locate its first failed job and step, and decide whether to fix the revision or rerun it.
tags: [git, github-actions, commands, troubleshooting]
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
  - id: gh-run-list
    resource: https://cli.github.com/manual/gh_run_list
    title: gh run list
  - id: gh-run-view
    resource: https://cli.github.com/manual/gh_run_view
    title: gh run view
  - id: gh-run-rerun
    resource: https://cli.github.com/manual/gh_run_rerun
    title: gh run rerun
  - id: github-rerun
    resource: https://docs.github.com/en/actions/how-tos/manage-workflow-runs/re-run-workflows-and-jobs
    title: Re-running workflows and jobs
  - id: gh-workflow-run
    resource: https://cli.github.com/manual/gh_workflow_run
    title: gh workflow run
  - id: github-workflow-commands
    resource: https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-commands
    title: Workflow commands for GitHub Actions
  - id: gh-pr-checks
    resource: https://cli.github.com/manual/gh_pr_checks
    title: gh pr checks
  - id: github-rerun-api
    resource: https://docs.github.com/en/rest/actions/workflow-runs
    title: REST API endpoints for workflow runs
  - id: github-manual-run
    resource: https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow
    title: Manually running a workflow
  - id: github-workflow-syntax
    resource: https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax
    title: Workflow syntax for GitHub Actions
---

# Inspect a GitHub Actions run from the terminal

## The simple idea

The GitHub CLI command `gh run` reads or manages a workflow run **from your
terminal**. A workflow command such as writing to `$GITHUB_OUTPUT` happens
**inside a running job**. They serve different people and times: the first
helps you inspect a result; the second lets a step pass information to later
steps.[^gh-run-view][^github-workflow-commands]

Think of `gh run view` as a status board and a job's output file as a note
the worker leaves for the next step. The comparison ends there: the board
can also offer controls that change a run, and the output file is parsed by
the runner rather than sent to another person.

This guide's outcome is to locate a failed run, find the first useful failure
signal, and choose a next action. The run and repository names below are
placeholders; no example workflow was triggered for this guide.

## Before you start

- Install GitHub CLI and sign in with an account allowed to view the target
  repository. `gh auth status` checks the current sign-in.
- Know the repository as `OWNER/REPO`. Using `--repo OWNER/REPO` makes the
  target explicit even when your current directory belongs to another
  repository.
- If the run publishes or deploys, know what a rerun would change before
  asking GitHub to start it again.

The read commands below do not alter a workflow run. A rerun does.[^github-rerun]

## Find and read one run

Imagine a proposed change to a lesson site whose CI check failed.

For a pull request, you can first list its checks with
`gh pr checks PR_NUMBER --repo OWNER/REPO`. A failing check links to its
run. A required check that never reported may be absent from this list;
compare it with the PR's merge box and the repository's required-check rules.
An approval wait needs a different first question than a failed test. The
command only reads check status.
[^gh-pr-checks]

1. List recent runs for the intended repository:

   ```bash
   gh run list --repo OWNER/REPO --limit 10
   ```

   Choose the run that matches the workflow, event, branch, and commit of the
   proposed change. Copy its run ID; do not assume that the newest run belongs
   to your change. `gh run list --repo OWNER/REPO --commit SHA` can narrow the
   list when you know the commit GitHub associates with the run.[^gh-run-list]

2. Read that run's summary and failed-step logs:

   ```bash
   gh run view RUN_ID --repo OWNER/REPO
   gh run view RUN_ID --repo OWNER/REPO --log-failed
   ```

   If the run is still active, `gh run watch RUN_ID --repo OWNER/REPO` shows
   its progress. The summary identifies the run and jobs. `--log-failed` shows failed-step
   logs when GitHub can provide them; it can include more than one failed
   step, so it does not identify the root cause for you. If logs are missing or
   hard to associate with a step, open the run in GitHub and inspect its
   jobs there; the CLI manual documents log association limits.
   [^gh-run-view]

3. Read the **first failing handoff**, not only the final red badge.

   | Signal | First question |
   | --- | --- |
   | No run matching the change | Did the workflow event, branch, path, or activity filter include it? |
   | PR check is awaiting approval | Does the repository's fork policy require a maintainer to inspect and approve this run? |
   | Required check says expected or pending | Did its workflow start, or did a trigger filter prevent the check from being reported? |
   | Run exists, job skipped or waiting | Did a job condition, dependency, or environment protection rule stop progress? |
   | Job is queued without starting | Is a matching runner available for its `runs-on` labels? |
   | Job ran, command failed | Which step and command failed first, and was the input revision the one expected? |
   | Job passed, service still fails | What deployment artifact and user path need checking outside this test job? |

   In a failed job, look for the first causal error in a step's log. A final
   “exit code 1” line reports failure but rarely explains it; canceled matrix
   siblings or later cleanup steps may be consequences of an earlier error.
   Compare the run graph and individual job logs when several jobs fail.

   The [common-solutions guide](common-solutions.md) follows each boundary
   in more detail.

4. Choose a next action from the evidence. A wrong path, broken test, or
   missing permission usually needs a reviewed change to the workflow or
   repository. A temporary service failure may justify a rerun after you
   confirm its effects. Do not use a rerun as evidence that the underlying
   defect is fixed.

## Rerun only when the same revision should run again

If you are authorized to rerun the workflow and have checked its side
effects, this asks GitHub to rerun failed jobs and jobs that depend on them:

```bash
gh run rerun RUN_ID --repo OWNER/REPO --failed
```

For example, if `test` failed and `publish` needs `test`, the failed-jobs
rerun includes `test` and its dependent `publish` job; an earlier successful
setup job is not rerun by this option. If `test` passes this time, `publish`
may now execute, so inspect its side effects first. This is a new **attempt**
of the original run, not a run of your latest
commit.[^gh-run-rerun][^github-rerun-api]

GitHub permits this rerun for up to 30 days after the initial run. The rerun
uses the original event's commit SHA and ref, so a code or workflow
fix committed afterward is absent. Repository configuration may have changed;
inspect current secrets, variables, and settings before assuming the attempt
repeats the same environment. GitHub also uses the original actor's
privileges for the rerun. Use `gh run view RUN_ID --repo OWNER/REPO --attempt N`
to compare a particular attempt with the latest one; a green rerun alone
cannot explain why the earlier attempt failed.[^gh-run-view][^github-rerun]

Stop before rerunning a publish, deployment, or other job that changes an
external system unless its owner has confirmed that repeating it is
appropriate. For a code or workflow fix, start a new run on the corrected
revision through the repository's normal review path.

## Other commands have different effects

| Need | Start with | Boundary |
| --- | --- | --- |
| Find a workflow file or its state | [`gh workflow list --all`](https://cli.github.com/manual/gh_workflow_list) or [`gh workflow view`](https://cli.github.com/manual/gh_workflow_view) | `--all` includes disabled workflows; these commands inspect definitions, not the steps of one run. |
| Start a manual workflow | [`gh workflow run`](https://cli.github.com/manual/gh_workflow_run) | The file must support `workflow_dispatch` and exist on the default branch; `--ref` selects the branch or tag to run. Its jobs may publish or deploy.[^gh-workflow-run][^github-manual-run] |
| Watch or download a run result | [`gh run watch`](https://cli.github.com/manual/gh_run_watch) or [`gh run download`](https://cli.github.com/manual/gh_run_download) | A downloaded artifact is only a run output; inspect its identity and contents before using it. |
| Disable or enable a workflow | [`gh workflow disable`](https://cli.github.com/manual/gh_workflow_disable) or [`gh workflow enable`](https://cli.github.com/manual/gh_workflow_enable) | These change whether the workflow can run; coordinate with its owner. |
| Set a secret or variable | [`gh secret`](https://cli.github.com/manual/gh_secret) or [`gh variable`](https://cli.github.com/manual/gh_variable) | These change repository or environment configuration; use secrets for sensitive values. |

Inside a running job, GitHub provides files for communication between
steps. These are **not** `gh` terminal commands:

| Job file | What a step writes | Scope |
| --- | --- | --- |
| `$GITHUB_ENV` | A name and value for later steps. | Subsequent steps in the same job; the writing step does not receive the new value. |
| `$GITHUB_OUTPUT` | A named output for the current step. | Give the writing step an `id:`. Later steps in the job use `steps.<id>.outputs.<name>`; another job needs an explicit job output, a `needs:` dependency, and `needs.<job>.outputs.<name>`.[^github-workflow-syntax] |
| `$GITHUB_STEP_SUMMARY` | Markdown to show on the run page. | Readers of the job summary after the step completes. |
| `$GITHUB_PATH` | A directory to add to `PATH`. | Subsequent steps in the same job. |

See GitHub's [workflow command reference](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-commands)
for exact syntax and limits. Do not put secrets or untrusted data in a
summary merely because it is easier to read than raw logs.
[^github-workflow-commands]

These files communicate within one job or its result; they do not give another
job the same runner workspace.

## Check your understanding

- If no run appears for a pull request, should you inspect job logs or the
  workflow trigger first?
- Why can a rerun pass without including a fix committed after the original
  attempt?
- If job B needs job A and only B fails, which job does a failed-jobs rerun
  start again?
- Which tool reads a run from your terminal, and which file lets one job
  step expose a named output to a later step?
- What would you check outside Actions after a deployment job is green?

## Official documentation and next routes

- [List runs](https://cli.github.com/manual/gh_run_list),
  [view a run](https://cli.github.com/manual/gh_run_view), and
  [rerun jobs](https://cli.github.com/manual/gh_run_rerun).
- [Pull request checks](https://cli.github.com/manual/gh_pr_checks) help you
  find the run associated with a proposed change.
- [GitHub's rerun behavior](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/re-run-workflows-and-jobs)
  and [workflow command files](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-commands).
- Read [workflow structure](workflow-structure.md) to understand the file
  that produced a run, [workflow shapes](examples-and-use-cases.md) to
  choose events and outcomes, and [GitHub Actions](index.md) for the topic.

[^gh-run-list]: [GitHub CLI `gh run list`](https://cli.github.com/manual/gh_run_list).
[^gh-run-view]: [GitHub CLI `gh run view`](https://cli.github.com/manual/gh_run_view).
[^gh-run-rerun]: [GitHub CLI `gh run rerun`](https://cli.github.com/manual/gh_run_rerun).
[^github-rerun]: [GitHub Docs, rerunning workflows and jobs](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/re-run-workflows-and-jobs).
[^gh-workflow-run]: [GitHub CLI `gh workflow run`](https://cli.github.com/manual/gh_workflow_run).
[^github-workflow-commands]: [GitHub Docs, workflow commands](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-commands).
[^gh-pr-checks]: [GitHub CLI `gh pr checks`](https://cli.github.com/manual/gh_pr_checks).
[^github-rerun-api]: [REST API endpoints for workflow runs](https://docs.github.com/en/rest/actions/workflow-runs).
[^github-manual-run]: [Manually running a workflow](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow).
[^github-workflow-syntax]: [Workflow syntax for GitHub Actions](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax).
