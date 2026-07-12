# GitHub Actions `uses` catalog

## Purpose

Use this page to understand the `uses:` parameter and find common, general-purpose, and important actions for real workflows.

This page is a practical catalog. It explains how to read action references, how to choose a safe action, how to navigate the catalog, and where to find the official source for each action.

> [!IMPORTANT]
> A `uses:` step runs code from an action or calls a reusable workflow. Treat every third-party action like a dependency: read its README, check inputs, review permissions, pin a version, and confirm it is maintained.

## How to navigate this catalog

| Need | Start here | Then check |
| --- | --- | --- |
| Understand `uses:` syntax | [Anatomy of `uses`](#anatomy-of-uses) | [Reference formats](#reference-formats) |
| Pick a normal setup action | [Official GitHub-maintained actions](#official-github-maintained-actions) | The action README and version tags |
| Add language tooling | [Language and runtime setup actions](#language-and-runtime-setup-actions) | Cache support and version inputs |
| Add Docker builds | [Docker and container actions](#docker-and-container-actions) | Registry auth and token permissions |
| Deploy to cloud | [Cloud authentication and deployment actions](#cloud-authentication-and-deployment-actions) | OIDC setup and environment protection |
| Add security checks | [Quality and security actions](#quality-and-security-actions) | Required permissions and report output |
| Add release automation | [Release and automation actions](#release-and-automation-actions) | Tag strategy and write permissions |
| Use community actions | [Common community actions](#common-community-actions) | Maintainer trust, inputs, and source code |
| Decide if an action is safe | [Selection checklist](#selection-checklist) | [Version pinning guidance](#version-pinning-guidance) |

## Anatomy of `uses`

| Part | Example | Meaning |
| --- | --- | --- |
| Owner | `actions` | GitHub organization or user that owns the action repository. |
| Repository | `checkout` | Repository that contains the action. |
| Path | `.github/workflows/deploy.yml` | Optional path for reusable workflows or actions in subdirectories. |
| Version reference | `@v4` | Branch, tag, or commit SHA to run. |
| Inputs | `with:` | Values passed to the action. |
| Secrets/env | `env:` or `secrets:` | Sensitive or runtime values passed to the step or reusable workflow. |

### Read a normal action reference

```yaml
steps:
  - name: Check out repository
    uses: actions/checkout@v4
```

How it works: `actions` is the owner, `checkout` is the repository, and `v4` is the version reference GitHub resolves.

What it does: downloads and runs the checkout action so later steps can access repository files.

### Pass inputs to an action

```yaml
steps:
  - uses: actions/setup-node@v4
    with:
      node-version: 22
      cache: npm
```

How it works: the `with:` block passes action-specific inputs. Input names and accepted values are defined by the action's `action.yml` and README.

What it does: installs Node.js 22 and enables npm dependency caching.

## Reference formats

| Format | Example | When to use it |
| --- | --- | --- |
| Public action | `owner/repository@version` | Most marketplace and open-source actions. |
| Public action in subdirectory | `owner/repository/path@version` | Monorepos that publish several actions. |
| Same-repository local action | `./.github/actions/setup` | Internal shared logic in the same repository. |
| Reusable workflow | `owner/repository/.github/workflows/file.yml@version` | Reuse a complete workflow as a job. |
| Docker image action | `docker://image:tag` | Run a published container image as an action step. |

### Use a local action

```yaml
steps:
  - name: Run local setup action
    uses: ./.github/actions/setup
```

How it works: GitHub looks for action metadata such as `action.yml` in the local path after the repository is checked out.

What it does: runs reusable automation stored inside the same repository.

> [!IMPORTANT]
> Local actions usually need `actions/checkout` before the local `uses:` step because the runner must have the repository files available.

### Call a reusable workflow

```yaml
jobs:
  deploy:
    uses: organization/platform/.github/workflows/deploy.yml@v1
    with:
      environment: staging
    secrets: inherit
```

How it works: reusable workflows are called at the job level, not inside `steps`. The caller passes inputs and secrets to the called workflow.

What it does: lets teams centralize a full deployment workflow instead of copying jobs into many repositories.

### Run a Docker image as an action

```yaml
steps:
  - name: Run shell in Alpine
    uses: docker://alpine:3.20
    with:
      args: sh -c "echo hello"
```

How it works: GitHub starts the referenced container image for the step.

What it does: runs a command inside a known container image.

## Selection checklist

| Check | Why it matters |
| --- | --- |
| Is the owner trusted? | The action code runs in your workflow. |
| Is the action maintained? | Old actions may use deprecated runtimes or APIs. |
| Does the README explain inputs and outputs? | You need to know what values the action accepts and returns. |
| Does it need secrets? | Secrets increase risk, especially for third-party actions. |
| What permissions does it need? | Prefer actions that work with least privilege. |
| Is it pinned to a version? | Unpinned actions are unstable and unsafe. |
| Does it support your runner OS? | Some actions assume Linux, Docker, or specific tooling. |
| Is there an official alternative? | Official or vendor-maintained actions are usually easier to justify. |

### Evaluate an action before using it

```text
1. Open the action repository or Marketplace page.
2. Read the README inputs, outputs, and examples.
3. Check the latest release or tags.
4. Review requested permissions and required secrets.
5. Pin the action to a version.
6. Add only the minimum token permissions needed by the workflow.
```

How it works: this turns action selection into a dependency review instead of a copy-paste exercise.

What it does: reduces the chance of giving untrusted code unnecessary access.

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

## Version pinning guidance

| Pin style | Example | Tradeoff |
| --- | --- | --- |
| Major version tag | `actions/checkout@v4` | Convenient and common; receives compatible updates. |
| Full version tag | `docker/build-push-action@v6.5.0` | More repeatable; requires manual updates. |
| Commit SHA | `owner/action@<sha>` | Strongest control for security-sensitive workflows. |
| Branch name | `owner/action@main` | Convenient but risky because it moves. |
| No version | `owner/action` | Do not use; workflow syntax requires a reference for repository actions. |

### Pin an action

```yaml
steps:
  - uses: actions/checkout@v4
```

How it works: GitHub resolves the version after `@` and runs that action revision.

What it does: avoids running an unversioned moving target.

> [!WARNING]
> Third-party actions execute code in your workflow. Review the source, permissions, inputs, and maintenance before using them.

## Where to find action documentation

| Source | Use it for |
| --- | --- |
| GitHub Marketplace listing | Quick install snippet, summary, and owner details. |
| Action repository README | Inputs, outputs, permissions, examples, and version guidance. |
| Releases or tags page | Available versions to pin. |
| `action.yml` or `action.yaml` | The exact inputs, outputs, branding, and runtime. |
| Security tab and issues | Maintenance and vulnerability signals. |
| Dependency graph | Visibility into actions referenced by workflows. |

### Inspect an action before adding it

```text
Repository page:
  README.md
  action.yml
  releases/tags
  issues
  security
```

How it works: the README explains intended use, while `action.yml` defines the action contract GitHub reads.

What it does: helps you confirm the action does what the catalog says before you give it access to your workflow.

## Related links

- [GitHub Actions documentation](https://docs.github.com/actions)
- [Workflow syntax: `jobs.<job_id>.steps[*].uses`](https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions#jobsjob_idstepsuses)
- [Using pre-written building blocks in your workflow](https://docs.github.com/actions/writing-workflows/choosing-what-your-workflow-does/using-pre-written-building-blocks-in-your-workflow)
- [About custom actions](https://docs.github.com/actions/creating-actions/about-custom-actions)
- [Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use)
- [GitHub Marketplace actions](https://github.com/marketplace?type=actions)
- [actions/checkout](https://github.com/actions/checkout)
- [actions/setup-node](https://github.com/actions/setup-node)
- [actions/setup-python](https://github.com/actions/setup-python)
- [actions/cache](https://github.com/actions/cache)
- [aws-actions/configure-aws-credentials](https://github.com/aws-actions/configure-aws-credentials)
- [docker/build-push-action](https://github.com/docker/build-push-action)
- [hashicorp/setup-terraform](https://github.com/hashicorp/setup-terraform)
- [Back to GitHub Actions](README.md)
- [Back to Git index](../README.md)
- [Back to root index](../../README.md)
