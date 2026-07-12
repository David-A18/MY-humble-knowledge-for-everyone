# GitHub Actions commands

## Purpose

Use this page for commands that operate GitHub Actions from the terminal and workflow commands used inside running jobs.

## GitHub CLI workflow commands

| Task | Command | When to use it |
| --- | --- | --- |
| List workflows | `gh workflow list` | You need workflow names, IDs, or status. |
| View workflow details | `gh workflow view <workflow>` | You need file path, state, or recent runs. |
| Run a manual workflow | `gh workflow run <workflow>` | The workflow supports `workflow_dispatch`. |
| Disable a workflow | `gh workflow disable <workflow>` | You need to stop a workflow temporarily. |
| Enable a workflow | `gh workflow enable <workflow>` | You need to restore a disabled workflow. |

### List workflows

```bash
gh workflow list
```

How it works: GitHub CLI calls the GitHub API for the current repository and lists Actions workflows.

What it does: shows workflow names, IDs, and active/disabled state.

### Run a workflow manually

```bash
gh workflow run deploy.yml -f environment=staging
```

How it works: GitHub CLI creates a `workflow_dispatch` event for the selected workflow and passes input values.

What it does: starts a manual deployment workflow with the `environment` input set to `staging`.

> [!IMPORTANT]
> A workflow can only be started with `gh workflow run` if the workflow defines `on: workflow_dispatch`.

## GitHub CLI run commands

| Task | Command | When to use it |
| --- | --- | --- |
| List runs | `gh run list` | You need recent workflow runs. |
| View a run | `gh run view <run-id>` | You need status, jobs, logs, or failure context. |
| Watch a run | `gh run watch <run-id>` | You want live status in the terminal. |
| Download artifacts | `gh run download <run-id>` | You need files produced by a run. |
| Rerun failed jobs | `gh run rerun <run-id> --failed` | You want to retry only failed jobs. |
| Cancel a run | `gh run cancel <run-id>` | A run is stale, wrong, or wasting minutes. |

### Inspect recent runs

```bash
gh run list --limit 10
gh run view 1234567890 --log-failed
```

How it works: GitHub CLI fetches workflow run metadata and logs from GitHub.

What it does: lists recent runs, then shows logs for failed jobs in one run.

### Rerun or cancel a run

```bash
gh run rerun 1234567890 --failed
gh run cancel 1234567890
```

How it works: GitHub CLI sends rerun or cancel requests to the workflow run API.

What it does: retries failed jobs or stops a run that should not continue.

## Secret and variable commands

| Task | Command | When to use it |
| --- | --- | --- |
| Set a repository secret | `gh secret set <name>` | You need an encrypted value for workflows. |
| Set an environment secret | `gh secret set <name> --env <environment>` | A secret should only be available to one deployment environment. |
| List repository secrets | `gh secret list` | You need to audit configured secret names. |
| Set a repository variable | `gh variable set <name> --body <value>` | You need non-secret configuration. |
| List repository variables | `gh variable list` | You need to inspect configured variable names and values. |

### Set secrets

```bash
gh secret set NPM_TOKEN
gh secret set AWS_ROLE_ARN --env production
```

How it works: GitHub CLI encrypts secret values locally before sending them to GitHub.

What it does: creates encrypted repository or environment secrets that workflows can read through the `secrets` context.

> [!WARNING]
> Do not pass secret values directly in shell history. Prefer interactive input or safe standard input.

### Set variables

```bash
gh variable set APP_NAME --body "payments-api"
gh variable list
```

How it works: GitHub stores variables as non-secret configuration values.

What it does: makes reusable values available through the `vars` context.

## Workflow command files

| Task | File | When to use it |
| --- | --- | --- |
| Add environment variable | `$GITHUB_ENV` | Later steps in the same job need a value. |
| Add step output | `$GITHUB_OUTPUT` | Later steps or jobs need a computed value. |
| Add Markdown summary | `$GITHUB_STEP_SUMMARY` | You want readable run output in the Actions UI. |
| Add a PATH entry | `$GITHUB_PATH` | Later steps need a tool directory in `PATH`. |

### Set an environment variable for later steps

```bash
echo "APP_VERSION=1.2.3" >> "$GITHUB_ENV"
```

How it works: the runner reads `$GITHUB_ENV` after the step completes and adds the variable to later steps in the same job.

What it does: makes `APP_VERSION` available as an environment variable after the current step.

### Set a step output

```bash
echo "image_tag=app-${GITHUB_SHA}" >> "$GITHUB_OUTPUT"
```

How it works: the runner records the value as an output for the current step. The step must have an `id` to be referenced later.

What it does: creates a reusable value such as `${{ steps.meta.outputs.image_tag }}`.

### Add a run summary

```bash
{
  echo "## Test summary"
  echo "- Status: passed"
  echo "- Commit: $GITHUB_SHA"
} >> "$GITHUB_STEP_SUMMARY"
```

How it works: GitHub renders Markdown written to `$GITHUB_STEP_SUMMARY` on the workflow run page.

What it does: gives readers a quick summary without opening raw logs.

## Related links

- [GitHub CLI manual](https://cli.github.com/manual/gh)
- [gh workflow run](https://cli.github.com/manual/gh_workflow_run)
- [gh run list](https://cli.github.com/manual/gh_run_list)
- [Workflow commands for GitHub Actions](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-commands)
- [Back to GitHub Actions](README.md)
- [Back to Git index](../README.md)
- [Back to root index](../../README.md)
