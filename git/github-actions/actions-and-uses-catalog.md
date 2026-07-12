# GitHub Actions `uses` catalog

## Purpose

Use this page to understand what the `uses:` key does and which common actions are useful in real workflows.

> [!IMPORTANT]
> This is a practical catalog, not a guarantee that every action is right for every repository. Check each action's README, permissions, maintenance, and version before using it.

## How `uses` works

| Target | Example | When to use it |
| --- | --- | --- |
| Public action repository | `actions/checkout@v4` | Use a published action from GitHub or another owner. |
| Local action | `./.github/actions/setup` | Reuse logic stored inside the same repository. |
| Reusable workflow | `org/repo/.github/workflows/deploy.yml@v1` | Reuse a complete workflow from another repository. |
| Docker image action | `docker://alpine:3.20` | Run a container image as a step. |

### Use a published action

```yaml
steps:
  - name: Check out repository
    uses: actions/checkout@v4
```

How it works: GitHub downloads the action version referenced after `@` and runs it as the step.

What it does: checks out the repository into the runner workspace so later commands can read the code.

## Official GitHub-maintained actions

| Action | Use | Notes |
| --- | --- | --- |
| `actions/checkout` | Check out repository code. | Most workflows need this before build or test commands. |
| `actions/setup-node` | Install and cache Node.js tooling. | Supports npm, Yarn, and pnpm caching. |
| `actions/setup-python` | Install Python versions. | Common for Python testing and tooling. |
| `actions/setup-java` | Install Java distributions. | Common for Maven and Gradle builds. |
| `actions/setup-go` | Install Go versions. | Common for Go testing and builds. |
| `actions/cache` | Cache dependencies or build outputs. | Use stable cache keys and restore keys. |
| `actions/upload-artifact` | Upload files from a run. | Use for test reports, build outputs, and packages. |
| `actions/download-artifact` | Download artifacts in a run. | Often paired with upload-artifact. |
| `actions/github-script` | Run GitHub API scripts in JavaScript. | Useful for labels, comments, and automation. |

### Set up Node.js

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: actions/setup-node@v4
    with:
      node-version: 22
      cache: npm
  - run: npm ci
  - run: npm test
```

How it works: checkout prepares the repository. setup-node installs Node.js and enables npm dependency caching.

What it does: creates a repeatable Node.js test job.

### Upload a test report

```yaml
steps:
  - name: Upload test report
    uses: actions/upload-artifact@v4
    with:
      name: test-report
      path: reports/
```

How it works: the action stores matching files as a workflow artifact.

What it does: lets people download reports from the workflow run page.

## Cloud authentication and deployment actions

| Action | Use | Notes |
| --- | --- | --- |
| `aws-actions/configure-aws-credentials` | Authenticate to AWS. | Prefer OIDC with `id-token: write` over long-lived keys. |
| `azure/login` | Authenticate to Azure. | Supports federated credentials and service principals. |
| `google-github-actions/auth` | Authenticate to Google Cloud. | Prefer Workload Identity Federation where possible. |
| `google-github-actions/setup-gcloud` | Install and configure Google Cloud CLI. | Often used after Google auth. |
| `hashicorp/setup-terraform` | Install Terraform CLI. | Pin Terraform versions for repeatable plans. |
| `azure/setup-kubectl` | Install kubectl. | Useful for Kubernetes deployment workflows. |
| `helm/chart-releaser-action` | Release Helm charts. | Useful for chart repositories. |

### Authenticate to AWS with OIDC

```yaml
permissions:
  id-token: write
  contents: read

steps:
  - name: Configure AWS credentials
    uses: aws-actions/configure-aws-credentials@v4
    with:
      role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
      aws-region: eu-west-1
```

How it works: GitHub issues an OIDC token for the job. AWS trusts that token and returns short-lived credentials for the role.

What it does: authenticates to AWS without storing long-lived AWS access keys in GitHub secrets.

### Install Terraform

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: hashicorp/setup-terraform@v3
    with:
      terraform_version: 1.9.8
  - run: terraform fmt -check
```

How it works: setup-terraform downloads the requested Terraform version and adds it to the runner path.

What it does: runs Terraform commands with a predictable CLI version.

## Docker and container actions

| Action | Use | Notes |
| --- | --- | --- |
| `docker/login-action` | Log in to a container registry. | Use tokens, not account passwords. |
| `docker/setup-buildx-action` | Set up Docker Buildx. | Needed for advanced and multi-platform builds. |
| `docker/build-push-action` | Build and optionally push images. | Common for Docker CI/CD. |
| `docker/metadata-action` | Generate image tags and labels. | Keeps tagging consistent. |
| `aquasecurity/trivy-action` | Scan images or filesystems. | Useful security gate before deployment. |

### Build and push a Docker image

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: docker/login-action@v3
    with:
      registry: ghcr.io
      username: ${{ github.actor }}
      password: ${{ secrets.GITHUB_TOKEN }}
  - uses: docker/setup-buildx-action@v3
  - uses: docker/build-push-action@v6
    with:
      context: .
      push: true
      tags: ghcr.io/${{ github.repository }}:${{ github.sha }}
```

How it works: GitHub checks out the code, logs in to GitHub Container Registry, configures Buildx, and runs a Docker build.

What it does: publishes an image tagged with the commit SHA.

## Quality, security, and release actions

| Action | Use | Notes |
| --- | --- | --- |
| `github/codeql-action/init` | Start CodeQL analysis. | Usually paired with `analyze`. |
| `github/codeql-action/analyze` | Upload CodeQL results. | Requires appropriate security settings. |
| `ossf/scorecard-action` | Run OpenSSF Scorecard checks. | Useful for supply-chain posture. |
| `softprops/action-gh-release` | Create GitHub releases. | Common for release automation. |
| `slackapi/slack-github-action` | Send Slack notifications. | Keep webhook tokens in secrets. |
| `peter-evans/create-pull-request` | Create pull requests from workflow changes. | Limit token permissions carefully. |

### Send a Slack notification

```yaml
steps:
  - name: Notify Slack
    uses: slackapi/slack-github-action@v1
    with:
      payload: |
        {"text":"Deployment finished for ${{ github.repository }}"}
    env:
      SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

How it works: the action sends the JSON payload to Slack using a secret webhook URL.

What it does: posts a deployment message to a Slack channel.

## Version pinning guidance

| Pin style | Example | Tradeoff |
| --- | --- | --- |
| Major version | `actions/checkout@v4` | Easy updates, accepts compatible fixes. |
| Full tag | `docker/build-push-action@v6.5.0` | More repeatable, but requires manual updates. |
| Commit SHA | `owner/action@<sha>` | Most controlled for security-sensitive workflows. |

### Pin an action

```yaml
steps:
  - uses: actions/checkout@v4
```

How it works: GitHub resolves the version after `@` and runs that action revision.

What it does: avoids running an unversioned moving target.

> [!WARNING]
> Third-party actions execute code in your workflow. Review the source, permissions, inputs, and maintenance before using them.

## Related links

- [GitHub Actions documentation](https://docs.github.com/actions)
- [actions/checkout](https://github.com/actions/checkout)
- [actions/setup-node](https://github.com/actions/setup-node)
- [aws-actions/configure-aws-credentials](https://github.com/aws-actions/configure-aws-credentials)
- [docker/login-action](https://github.com/docker/login-action)
- [hashicorp/setup-terraform](https://github.com/hashicorp/setup-terraform)
- [Back to GitHub Actions](README.md)
- [Back to Git index](../README.md)
- [Back to root index](../../README.md)
