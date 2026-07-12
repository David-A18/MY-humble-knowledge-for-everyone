# GitHub Actions security, secrets, and permissions

## Purpose

Use this page to design safer workflows: least-privilege tokens, protected environments, secret handling, dependency trust, and OIDC authentication.

## Security building blocks

| Building block | Use | Why it matters |
| --- | --- | --- |
| `permissions` | Restrict `GITHUB_TOKEN`. | Limits what workflow code can change. |
| Secrets | Store sensitive values. | Prevents committing tokens and passwords. |
| Variables | Store non-secret config. | Keeps workflow files reusable. |
| Environments | Protect deployments. | Adds approvals, wait timers, and environment-scoped secrets. |
| OIDC | Authenticate to cloud providers. | Replaces long-lived cloud keys with short-lived tokens. |
| Version pinning | Control action versions. | Reduces supply-chain surprise. |
| Fork restrictions | Limit untrusted code access. | Protects secrets from untrusted pull requests. |

## Token permissions

### Read-only default permissions

```yaml
permissions:
  contents: read
```

How it works: GitHub grants the workflow token only read access to repository contents unless a job overrides it.

What it does: reduces the damage possible if a dependency, action, or script behaves unexpectedly.

### Job-level write permission

```yaml
jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - run: echo "publish package"
```

How it works: the `publish` job receives package write permission, while other jobs can keep stricter defaults.

What it does: limits write access to the job that actually needs it.

## Secrets and variables

| Data type | Access syntax | Use for |
| --- | --- | --- |
| Repository secret | `${{ secrets.NAME }}` | Sensitive values used across repository workflows. |
| Environment secret | `${{ secrets.NAME }}` with `environment:` | Sensitive values tied to deployment environments. |
| Organization secret | `${{ secrets.NAME }}` | Shared sensitive values across repositories. |
| Repository variable | `${{ vars.NAME }}` | Non-secret values such as app name or region. |
| Environment variable | `$NAME` in shell | Values injected into a running step. |

### Use a secret in one step

```yaml
steps:
  - name: Publish package
    run: npm publish
    env:
      NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

How it works: GitHub injects the secret as an environment variable only for this step.

What it does: gives the publish command access to the token without writing the token into the repository.

> [!WARNING]
> Never echo secrets, pass them in URLs, or print full environments in logs.

### Use variables for safe config

```yaml
env:
  AWS_REGION: ${{ vars.AWS_REGION }}
```

How it works: GitHub resolves the repository or environment variable before the job runs.

What it does: keeps non-secret configuration outside repeated YAML blocks.

## Environments

### Protected production deployment

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - run: ./deploy.sh
```

How it works: GitHub connects the job to the `production` environment. Environment rules can require reviewers, wait timers, or environment-specific secrets.

What it does: adds a control point before production deployment.

## OpenID Connect

### Cloud authentication with OIDC

```yaml
permissions:
  id-token: write
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: eu-west-1
```

How it works: GitHub issues a signed identity token for the job. AWS validates the token and exchanges it for short-lived role credentials.

What it does: removes the need for long-lived AWS access keys in GitHub secrets.

> [!IMPORTANT]
> OIDC also requires cloud-side trust configuration. The workflow permission is necessary but not enough by itself.

## Third-party action safety

| Check | Why it matters |
| --- | --- |
| Maintainer and repository ownership | Confirms who controls the action code. |
| Version pinning | Prevents accidental major upgrades. |
| Permissions needed | Reveals whether the action needs write access. |
| Inputs and secrets | Shows what data the action receives. |
| Release activity | Helps identify abandoned actions. |
| Source code | Lets you inspect what runs in your workflow. |

### Pin action versions

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: docker/build-push-action@v6
```

How it works: GitHub resolves the referenced major version instead of running an unversioned default branch.

What it does: gives you controlled updates while avoiding unpinned action references.

For high-risk workflows, pin to a full commit SHA after reviewing the source.

## Pull request safety

| Event | Trust level | Notes |
| --- | --- | --- |
| `pull_request` | Safer default for untrusted changes. | Runs in the context of the merge commit and has restricted secret access for forks. |
| `pull_request_target` | Higher risk. | Runs in the base repository context and can access more privileges. |
| `workflow_dispatch` | Human-triggered. | Use inputs and environments for controlled operations. |
| `push` to protected branch | Trusted after merge. | Good for publishing or deployment after review. |

### Avoid privileged fork execution

```yaml
on:
  pull_request:

permissions:
  contents: read
```

How it works: pull request workflows validate proposed changes with limited token permissions.

What it does: lets contributors get CI feedback without giving untrusted code write access.

> [!WARNING]
> Be extremely careful with `pull_request_target`. Do not check out and run untrusted pull request code with privileged secrets.

## Related links

- [Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use)
- [Using secrets in GitHub Actions](https://docs.github.com/actions/security-guides/using-secrets-in-github-actions)
- [OpenID Connect](https://docs.github.com/en/actions/concepts/security/openid-connect)
- [Configuring OpenID Connect in cloud providers](https://docs.github.com/actions/security-for-github-actions/security-hardening-your-deployments/configuring-openid-connect-in-cloud-providers)
- [Back to GitHub Actions](README.md)
- [Back to Git index](../README.md)
- [Back to root index](../../README.md)
