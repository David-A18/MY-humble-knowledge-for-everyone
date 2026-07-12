# GitHub Actions common solutions

## Purpose

Use this page when a workflow fails or behaves unexpectedly. Start with inspection, then apply the smallest safe fix.

## First checks

| Symptom | Check | Likely cause |
| --- | --- | --- |
| Workflow did not start | `on` trigger and branch/path filters | Event does not match workflow filters. |
| Step cannot find files | `actions/checkout` exists before commands | Repository was not checked out. |
| Push or release fails | `permissions` block | `GITHUB_TOKEN` lacks required write permission. |
| Secret is empty | Secret scope and event type | Secret is unavailable for fork or environment. |
| Deployment waits | Environment protection rules | Required reviewers or wait timer. |
| Job is slow | Cache and matrix strategy | Dependencies reinstall every run or too many jobs. |
| Workflow cancels | `concurrency` group | Newer run canceled older run. |

### Inspect a failed run

```bash
gh run list --limit 10
gh run view 1234567890 --log-failed
```

How it works: GitHub CLI lists recent runs, then fetches failed logs for one run.

What it does: gives you the error context before changing YAML.

## Workflow did not start

### Check event filters

```yaml
on:
  push:
    branches:
      - main
    paths:
      - "src/**"
```

How it works: both the branch filter and path filter must match for this workflow to run.

What it does: prevents runs for pushes outside `main` or changes outside `src/**`.

Common fix: loosen filters while debugging, then add the narrow filters back intentionally.

## Repository files are missing

### Add checkout before commands

```yaml
steps:
  - uses: actions/checkout@v4
  - run: ls
  - run: npm test
```

How it works: hosted runners start with an empty workspace. `actions/checkout` fetches repository content into `$GITHUB_WORKSPACE`.

What it does: makes project files available to later shell commands.

## Token permission failures

### Grant least required permission

```yaml
permissions:
  contents: read
  packages: write
```

How it works: the workflow's `GITHUB_TOKEN` receives only the permissions listed.

What it does: allows package publishing while keeping repository contents read-only.

> [!TIP]
> Start from least privilege. Add write permissions only when a step actually needs them.

## Secret is empty or unavailable

### Use repository or environment secrets

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - run: ./deploy.sh
        env:
          API_TOKEN: ${{ secrets.API_TOKEN }}
```

How it works: GitHub injects the secret into the step environment if the event and environment allow access.

What it does: makes the secret available to `deploy.sh` without hardcoding it in the repository.

> [!WARNING]
> Secrets are not passed to workflows from forks in the same way as trusted repository workflows. Be careful with pull request automation that needs credentials.

## OIDC authentication fails

### Add OIDC permission

```yaml
permissions:
  id-token: write
  contents: read
```

How it works: `id-token: write` allows the job to request an OIDC token from GitHub.

What it does: enables cloud login actions such as `aws-actions/configure-aws-credentials` to exchange the token for short-lived credentials.

Common fix: verify the cloud trust policy also matches the repository, branch, environment, or subject claim you expect.

## Cache does not restore

### Use stable cache keys

```yaml
steps:
  - uses: actions/setup-node@v4
    with:
      node-version: 22
      cache: npm
```

How it works: setup-node can cache npm dependencies based on lockfile data.

What it does: reduces dependency install time when the lockfile has not changed.

Common fix: make sure the lockfile exists and is committed.

## Matrix jobs are too noisy

### Disable fail-fast

```yaml
strategy:
  fail-fast: false
  matrix:
    node-version: [20, 22]
```

How it works: `fail-fast: false` lets all matrix jobs finish even if one fails.

What it does: gives you the full compatibility picture instead of stopping at the first failure.

## Deployments overlap

### Add deployment concurrency

```yaml
concurrency:
  group: deploy-${{ github.ref }}
  cancel-in-progress: false
```

How it works: GitHub allows only one run in the same concurrency group at a time.

What it does: prevents overlapping deploys for the same branch.

## Debug expression values

### Print safe context values

```yaml
steps:
  - run: |
      echo "ref=${{ github.ref }}"
      echo "event=${{ github.event_name }}"
      echo "runner_os=${{ runner.os }}"
```

How it works: GitHub evaluates expressions before the shell command runs.

What it does: prints safe metadata that helps debug conditions and triggers.

> [!WARNING]
> Do not print `secrets` or full event payloads unless you understand what they contain.

## Related links

- [GitHub Actions workflow syntax](https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions)
- [Using secrets in GitHub Actions](https://docs.github.com/actions/security-guides/using-secrets-in-github-actions)
- [Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use)
- [Back to GitHub Actions](README.md)
- [Back to Git index](../README.md)
- [Back to root index](../../README.md)
