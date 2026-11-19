---
type: Reference
title: Common GitHub Actions by category
description: Find widely used GitHub Actions for setup, cloud authentication, containers, quality and security, releases, and community tasks.
tags: [git, github-actions, actions-and-uses-catalog]
status: draft
audience: Engineering learners and practitioners
maintainer: unassigned
---

# Common GitHub Actions by category

This catalog groups commonly used actions by the job they do, so you can find a starting point and then check its documentation. It is part of [GitHub Actions `uses` catalog](actions-and-uses-catalog.md).

## Official GitHub-maintained actions

| Action | Use | Notes |
| --- | --- | --- |
| `actions/checkout` | Check out repository code. | Most workflows need this before build or test commands. |
| `actions/cache` | Cache dependencies or build outputs. | Use stable cache keys and restore keys. |
| `actions/upload-artifact` | Upload files from a run. | Use for test reports, build outputs, and packages. |
| `actions/download-artifact` | Download artifacts in a run. | Often paired with upload-artifact. |
| `actions/github-script` | Run GitHub API scripts in JavaScript. | Useful for labels, comments, issues, and pull requests. |
| `actions/create-github-app-token` | Create GitHub App installation tokens. | Useful when `GITHUB_TOKEN` is not the right identity. |
| `actions/dependency-review-action` | Review dependency changes in pull requests. | Useful security control for dependency updates. |
| `actions/attest-build-provenance` | Generate build provenance attestations. | Useful for supply-chain integrity. |
| `actions/configure-pages` | Configure GitHub Pages. | Common in Pages deploy workflows. |
| `actions/upload-pages-artifact` | Upload Pages artifact. | Usually paired with deploy-pages. |
| `actions/deploy-pages` | Deploy to GitHub Pages. | Requires Pages permissions and configuration. |

### General CI setup

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: actions/cache@v4
    with:
      path: ~/.npm
      key: npm-${{ runner.os }}-${{ hashFiles('package-lock.json') }}
      restore-keys: npm-${{ runner.os }}-
```

How it works: checkout downloads the repository, then cache restores previously saved dependency data using the cache key.

What it does: prepares source files and speeds up repeated dependency installation.

### Pull request dependency review

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: actions/dependency-review-action@v4
```

How it works: the dependency review action checks dependency changes introduced by a pull request.

What it does: helps catch risky dependency updates before merge.

### GitHub Pages deployment

```yaml
steps:
  - uses: actions/configure-pages@v5
  - uses: actions/upload-pages-artifact@v3
    with:
      path: ./site
  - uses: actions/deploy-pages@v4
```

How it works: the actions configure Pages, upload a static site artifact, and deploy that artifact.

What it does: publishes static content through GitHub Pages.

## Language and runtime setup actions

| Action | Use | Notes |
| --- | --- | --- |
| `actions/setup-node` | Install Node.js. | Supports dependency caching for npm, Yarn, and pnpm. |
| `actions/setup-python` | Install Python. | Supports Python version selection and pip cache. |
| `actions/setup-java` | Install Java. | Supports distributions and Maven/Gradle caches. |
| `actions/setup-go` | Install Go. | Supports Go version files and cache. |
| `actions/setup-dotnet` | Install .NET SDK. | Useful for .NET build and test workflows. |
| `ruby/setup-ruby` | Install Ruby and Bundler dependencies. | Common community-maintained Ruby setup action. |
| `pnpm/action-setup` | Install pnpm. | Often used with setup-node for pnpm projects. |
| `oven-sh/setup-bun` | Install Bun. | Useful for Bun-based JavaScript projects. |

### Node.js with pnpm

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: pnpm/action-setup@v4
    with:
      version: 9
  - uses: actions/setup-node@v4
    with:
      node-version: 22
      cache: pnpm
  - run: pnpm install --frozen-lockfile
  - run: pnpm test
```

How it works: pnpm is installed first, then setup-node installs Node.js and configures pnpm cache support.

What it does: creates a repeatable pnpm CI workflow.

### Python setup

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: actions/setup-python@v5
    with:
      python-version: "3.12"
      cache: pip
  - run: pip install -r requirements.txt
  - run: pytest
```

How it works: setup-python installs Python 3.12 and configures pip dependency caching.

What it does: runs Python tests with a known interpreter version.

## Cloud authentication and deployment actions

| Action | Use | Notes |
| --- | --- | --- |
| `aws-actions/configure-aws-credentials` | Authenticate to AWS. | Prefer OIDC with `id-token: write` over long-lived keys. |
| `azure/login` | Authenticate to Azure. | Supports federated credentials and service principals. |
| `google-github-actions/auth` | Authenticate to Google Cloud. | Prefer Workload Identity Federation where possible. |
| `google-github-actions/setup-gcloud` | Install and configure Google Cloud CLI. | Often used after Google auth. |
| `hashicorp/setup-terraform` | Install Terraform CLI. | Pin Terraform versions for repeatable plans. |
| `azure/setup-kubectl` | Install kubectl. | Useful for Kubernetes deployment workflows. |
| `azure/k8s-deploy` | Deploy manifests to Kubernetes. | Common in Azure/Kubernetes workflows. |
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
| `docker/setup-qemu-action` | Set up QEMU for multi-platform builds. | Needed for some cross-platform images. |
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
  - uses: docker/metadata-action@v5
    id: meta
    with:
      images: ghcr.io/${{ github.repository }}
  - uses: docker/setup-buildx-action@v3
  - uses: docker/build-push-action@v6
    with:
      context: .
      push: true
      tags: ${{ steps.meta.outputs.tags }}
      labels: ${{ steps.meta.outputs.labels }}
```

How it works: GitHub checks out the code, logs in to GitHub Container Registry, calculates tags and labels, configures Buildx, and runs a Docker build.

What it does: publishes a container image with consistent metadata.

## Quality and security actions

| Action | Use | Notes |
| --- | --- | --- |
| `github/codeql-action/init` | Start CodeQL analysis. | Usually paired with `analyze`. |
| `github/codeql-action/analyze` | Upload CodeQL results. | Requires appropriate security settings. |
| `ossf/scorecard-action` | Run OpenSSF Scorecard checks. | Useful for supply-chain posture. |
| `aquasecurity/trivy-action` | Scan containers, filesystems, or IaC. | Common security gate. |
| `step-security/harden-runner` | Monitor and restrict runner network behavior. | Useful for higher-security workflows. |
| `reviewdog/action-actionlint` | Run actionlint and report workflow issues. | Useful for workflow YAML review. |

### CodeQL analysis

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: github/codeql-action/init@v3
    with:
      languages: javascript-typescript
  - uses: github/codeql-action/analyze@v3
```

How it works: CodeQL initializes a language database and analyzes source code for security issues.

What it does: uploads code scanning results to GitHub security features.

### Scan a container image

```yaml
steps:
  - uses: aquasecurity/trivy-action@master
    with:
      image-ref: ghcr.io/example/app:${{ github.sha }}
      severity: HIGH,CRITICAL
```

How it works: Trivy checks the image for known vulnerabilities and reports matching findings.

What it does: adds a security gate before release or deployment.

> [!WARNING]
> Some community actions publish examples using a branch such as `@master`. For stricter repeatability, pin to a release tag or commit SHA when the project provides one.

## Release and automation actions

| Action | Use | Notes |
| --- | --- | --- |
| `softprops/action-gh-release` | Create GitHub releases. | Common for release automation. |
| `peter-evans/create-pull-request` | Create pull requests from workflow changes. | Limit token permissions carefully. |
| `peter-evans/slash-command-dispatch` | Dispatch workflows from issue or PR comments. | Useful for ChatOps-style automation. |
| `actions/github-script` | Run GitHub API scripts. | Good for small automations without a full app. |
| `peaceiris/actions-gh-pages` | Publish static files to GitHub Pages branch. | Common community alternative for Pages workflows. |
| `slackapi/slack-github-action` | Send Slack notifications. | Keep webhook tokens in secrets. |

### Create a GitHub release

```yaml
steps:
  - name: Create release
    uses: softprops/action-gh-release@v2
    with:
      files: dist/*
```

How it works: the action uses the GitHub API to create or update a release and attach files.

What it does: publishes release assets from the workflow.

### Create an automated pull request

```yaml
steps:
  - uses: actions/checkout@v4
  - run: ./scripts/update-generated-docs.sh
  - uses: peter-evans/create-pull-request@v7
    with:
      title: Update generated docs
      branch: automation/update-generated-docs
```

How it works: the action commits workflow-generated changes to a branch and opens or updates a pull request.

What it does: turns automated repository changes into a reviewable pull request instead of pushing directly to `main`.

## Common community actions

| Action | Use | Notes |
| --- | --- | --- |
| `dorny/paths-filter` | Detect which paths changed. | Useful for monorepos and conditional jobs. |
| `tj-actions/changed-files` | List changed files. | Useful for targeted linting or selective deploys. |
| `amannn/action-semantic-pull-request` | Validate pull request titles. | Useful with conventional commit release workflows. |
| `lycheeverse/lychee-action` | Check links. | Useful for documentation repositories. |
| `DavidAnson/markdownlint-cli2-action` | Run markdownlint-cli2. | Useful for Markdown style checks. |
| `reviewdog/action-eslint` | Run ESLint with review comments. | Useful for JavaScript/TypeScript reviews. |
| `actions-cool/issues-helper` | Automate issue operations. | Useful for issue triage workflows. |

### Run path-based logic

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: dorny/paths-filter@v3
    id: changes
    with:
      filters: |
        docs:
          - "**/*.md"
        app:
          - "src/**"
```

How it works: the action compares changed files against named path filters and exposes outputs.

What it does: lets later steps or jobs decide whether docs or application code changed.

### Check Markdown and links

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: DavidAnson/markdownlint-cli2-action@v19
  - uses: lycheeverse/lychee-action@v2
```

How it works: the first action lints Markdown files, and the second checks links.

What it does: catches documentation formatting and broken links before merge.

## Related links

- [GitHub Actions `uses` catalog](actions-and-uses-catalog.md)
- [Back to index](index.md)
