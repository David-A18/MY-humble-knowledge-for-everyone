# GitHub Actions examples and use cases

## Purpose

Use this page to copy common workflow shapes and understand how each example works.

## Common use cases

| Use case | Trigger | Typical jobs |
| --- | --- | --- |
| Pull request CI | `pull_request` | lint, test, build |
| Main branch CI | `push` to `main` | test, package, publish artifact |
| Manual deployment | `workflow_dispatch` | validate input, deploy, notify |
| Scheduled maintenance | `schedule` | scan, report, open issue |
| Docker publishing | `push` tag or branch | build, scan, push image |
| Terraform plan | `pull_request` | fmt, validate, plan |
| Terraform apply | `push` to `main` or manual | plan, approval, apply |

## Pull request CI

### Node.js CI workflow

```yaml
name: Node CI

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
      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: npm
      - run: npm ci
      - run: npm test
```

How it works: pull requests and pushes to `main` start the workflow. The job checks out the repository, installs Node.js, restores npm cache when possible, installs dependencies, and runs tests.

What it does: blocks unsafe changes before merge and verifies the main branch after merge.

## Matrix testing

### Test multiple versions

```yaml
name: Matrix CI

on:
  pull_request:

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        node-version: [20, 22]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: npm
      - run: npm ci
      - run: npm test
```

How it works: GitHub expands the job into one run for Node.js 20 and one run for Node.js 22.

What it does: confirms the project works across supported runtime versions.

## Manual deployment

### Deploy with environment input

```yaml
name: Deploy

on:
  workflow_dispatch:
    inputs:
      environment:
        description: Deployment environment
        required: true
        type: choice
        options:
          - staging
          - production

permissions:
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    steps:
      - uses: actions/checkout@v4
      - run: ./deploy.sh "${{ inputs.environment }}"
```

How it works: a user starts the workflow manually and chooses an environment. GitHub attaches the selected environment to the job.

What it does: runs deployment logic with explicit human intent and can use environment protection rules.

## Docker image publishing

### Build and push to GitHub Container Registry

```yaml
name: Publish image

on:
  push:
    branches:
      - main

permissions:
  contents: read
  packages: write

jobs:
  image:
    runs-on: ubuntu-latest
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

How it works: the workflow gets package write permission, logs in to GHCR with `GITHUB_TOKEN`, sets up Buildx, and builds the image.

What it does: publishes a container image for the current commit.

## Terraform pull request plan

### Terraform validation workflow

```yaml
name: Terraform plan

on:
  pull_request:
    paths:
      - "terraform/**"
      - ".github/workflows/terraform-plan.yml"

permissions:
  contents: read

jobs:
  terraform:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: terraform
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: 1.9.8
      - run: terraform fmt -check -recursive
      - run: terraform init -backend=false
      - run: terraform validate
```

How it works: path filters run the workflow only when Terraform files or the workflow change. Terraform runs from the `terraform` directory.

What it does: checks formatting and validates Terraform configuration without touching remote state.

## AWS deployment with OIDC

### Authenticate without long-lived keys

```yaml
name: AWS deploy

on:
  workflow_dispatch:

permissions:
  id-token: write
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: eu-west-1
      - run: aws sts get-caller-identity
```

How it works: GitHub requests an OIDC token for the job. AWS validates the token against the role trust policy and returns temporary credentials.

What it does: proves the workflow can authenticate to AWS without static access keys.

## Scheduled maintenance

### Nightly dependency check

```yaml
name: Nightly checks

on:
  schedule:
    - cron: "0 3 * * *"
  workflow_dispatch:

permissions:
  contents: read

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm audit --audit-level=high
```

How it works: GitHub starts the workflow on the cron schedule and also allows manual runs.

What it does: runs a recurring dependency audit.

> [!NOTE]
> Scheduled workflows run on UTC time.

## Related links

- [GitHub Actions quickstart](https://docs.github.com/actions/get-started/quickstart)
- [Workflow syntax](https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions)
- [Configuring OpenID Connect in Amazon Web Services](https://docs.github.com/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services)
- [Back to GitHub Actions](README.md)
- [Back to Git index](../README.md)
- [Back to root index](../../README.md)
