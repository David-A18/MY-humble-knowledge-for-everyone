---
type: Reference
title: Choose a GitHub Actions action
description: Read a uses reference, find a maintained action for a job, and check its code, version, inputs, and authority before adoption.
tags: [git, github-actions, actions-and-uses-catalog, reference]
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
  - id: github-workflow-syntax
    resource: https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax
    title: Workflow syntax for GitHub Actions
  - id: github-secure-use
    resource: https://docs.github.com/en/actions/reference/security/secure-use
    title: Secure use reference
  - id: github-reusable-workflows
    resource: https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows
    title: Reuse workflows
  - id: github-token
    resource: https://docs.github.com/en/actions/tutorials/authenticate-with-github_token
    title: Use GITHUB_TOKEN for authentication
  - id: github-checkout
    resource: https://github.com/actions/checkout
    title: actions/checkout
  - id: github-setup-node
    resource: https://github.com/actions/setup-node
    title: actions/setup-node
---

# Choose a GitHub Actions action

## The simple idea

An **action** is reusable code that a workflow step runs. The `uses` key
names that code. It may come from a public repository, a path in your own
repository, or a container image. A **reusable workflow** is a larger unit
called by a job, also with `uses`. These two placements have different
inputs and security boundaries.[^github-syntax][^github-reuse]

Treat an action like a program you add to a build: its owner, code revision,
inputs, and access to the job all matter. The analogy has a limit: unlike a
library imported by your application, an action executes during automation
and can reach any credentials or files the job exposes to it.
[^github-secure]

This page helps you find a candidate and check it. The listed actions are
starting points, not endorsements or complete workflow recipes. Read
[workflow structure](workflow-structure.md) first if a step or job is new.

## Read the reference before copying it

| Location | Shape | What GitHub runs |
| --- | --- | --- |
| Step in a job | `owner/repository@ref` | An action from another repository at the chosen ref. |
| Step in a job | `./path/to/action` | An action checked out from this repository; its files must be present on the runner. |
| Step in a job | `docker://image:tag` | A container image as an action step; verify the image source and tag. |
| Whole job | `owner/repository/.github/workflows/file.yml@ref` | A reusable workflow with its own jobs and declared inputs. |

For example, this step uses the official checkout action at the `v7`
major-version tag shown in its current README:

```yaml
steps:
  - name: Get repository files
    uses: actions/checkout@v7
```

The `actions` owner is the GitHub organization that maintains the action;
`checkout` is the repository; `v7` is a ref GitHub resolves. The action
gets source files onto the runner for later steps. The snippet is only a
step list, not a runnable workflow. Check the action's current README and
the runner it supports before adding it.[^github-checkout][^github-syntax]

`with:` passes inputs defined by an action; `env:` sets environment values
for a step. The action's `action.yml` or `action.yaml` and README tell you
which inputs exist. Neither key automatically grants permission: token
scopes, repository access, external credentials, and event trust still
determine what the code can do.[^github-syntax][^github-token]

### A reusable workflow is a job call

Put the reusable workflow's `uses` at the **job** level, not inside
`steps`. The called workflow must declare `workflow_call`. Its `with:`
inputs follow the called workflow's contract. Pass only the named secrets
it needs; `secrets: inherit` passes every secret available to the caller
to the called workflow.[^github-reuse][^github-syntax]

A same-repository action and a same-repository reusable workflow use
different paths. The [workflow syntax reference](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
has the supported forms, including GitHub Enterprise Server differences.

## Find a candidate by the job you need

Each link below goes to the action's source repository. Check its README,
release or commit, metadata, permissions, and runner requirements before
using it. A current link is not evidence that a particular version works
in your repository.

| Need | Candidate source | First boundary to check |
| --- | --- | --- |
| Get repository files | [actions/checkout](https://github.com/actions/checkout) | Which ref and repository does it check out? |
| Choose a Node version | [actions/setup-node](https://github.com/actions/setup-node) | Which Node version and package cache settings fit the project? |
| Choose a Python version | [actions/setup-python](https://github.com/actions/setup-python) | Which Python version and dependency file are used? |
| Cache dependencies | [actions/cache](https://github.com/actions/cache) | Can an untrusted ref write or restore this cache? |
| Move files between jobs | [actions/upload-artifact](https://github.com/actions/upload-artifact) and [actions/download-artifact](https://github.com/actions/download-artifact) | Which run and artifact produced the files? |
| Review dependency changes | [actions/dependency-review-action](https://github.com/actions/dependency-review-action) | Does the event provide a meaningful PR comparison and required permission? |
| Authenticate to AWS | [aws-actions/configure-aws-credentials](https://github.com/aws-actions/configure-aws-credentials) | Does OIDC trust restrict repository, ref or environment, and role permissions? |
| Authenticate to Azure | [azure/login](https://github.com/Azure/login) | Which federated identity and subscription will the job use? |
| Authenticate to Google Cloud | [google-github-actions/auth](https://github.com/google-github-actions/auth) | Which workload identity provider and service account are trusted? |
| Install Terraform | [hashicorp/setup-terraform](https://github.com/hashicorp/setup-terraform) | Which CLI version, backend, and cloud identity does the job need? |
| Log in to a container registry | [docker/login-action](https://github.com/docker/login-action) | Which registry and least-privilege credential will be used? |
| Build or publish an image | [docker/build-push-action](https://github.com/docker/build-push-action) | Is pushing intended, and how will the digest be verified? |

These are common examples, not a list of every useful action. Some
tasks need only `run:` with tools already on a runner; using an action
adds code you must maintain and review. For an OIDC walkthrough, read
[AWS OIDC federation](aws-oidc-federation.md). For the event and result
shape around publishing, read [workflow shapes](examples-and-use-cases.md).

## Review the dependency before running it

1. **Name the outcome.** Decide what the job must produce and whether this
   action is necessary for that step.
2. **Verify the owner and source.** Open the repository linked above or the
   candidate's own source, then read its README and action metadata. Check
   that the stated inputs, outputs, runner, and release apply to your use.
3. **Choose a reviewed ref.** A branch or major tag can move. GitHub's
   secure-use guidance says a full-length commit SHA is the way to make
   an action reference immutable; verify that SHA belongs to the intended
   action repository. Update a pinned SHA deliberately when reviewing a
   new release.[^github-secure]
4. **Map its authority.** Record the event, repository-token permissions,
   passed secrets, OIDC trust, and files the action can read. Check this
   especially for code from a pull request or a third-party owner.
   [^github-token][^github-secure]
5. **Test the actual outcome.** Run it on a reviewed change and inspect
   the resulting job, artifact, or target service. A passing action step
   alone does not prove that users can use the published result.

| Ref style | What stays fixed? | Review implication |
| --- | --- | --- |
| Full-length commit SHA | The referenced Git commit. | Strongest revision control; check origin and update intentionally. |
| Major or full version tag | A name that the owner can move. | Easier updates, but recheck what the tag resolves to. |
| Branch name | A moving branch tip. | Avoid for privileged jobs unless that movement is part of the design. |

These choices apply to external actions and reusable workflows. A local
action follows the calling repository's checked-out revision, so check
which code the workflow event supplies. GitHub's
[secure-use reference](https://docs.github.com/en/actions/reference/security/secure-use)
explains why untrusted pull-request code and powerful credentials need
separate treatment.[^github-secure]

## Check your understanding

- Why is `uses: actions/checkout@v7` not an entire workflow?
- Where does `uses` go when calling a reusable workflow?
- Why does a full-length SHA still require checking the source repository?
- What else must be reviewed before an AWS login action can call AWS APIs?
- What could `secrets: inherit` expose to a called workflow?

## Official documentation and next routes

- [Workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
  for step actions, local actions, container actions, and reusable workflows.
- [Secure use](https://docs.github.com/en/actions/reference/security/secure-use)
  for pinning and trust boundaries; [reuse workflows](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows)
  for called-job inputs and secrets.
- [GITHUB_TOKEN permissions](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token)
  and the [official checkout](https://github.com/actions/checkout) and
  [Node setup](https://github.com/actions/setup-node) source repositories.
- Return to [GitHub Actions](index.md), [workflow shapes](examples-and-use-cases.md),
  or the [knowledge index](../../index.md).

[^github-syntax]: [GitHub Actions workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax).
[^github-secure]: [GitHub Actions secure-use reference](https://docs.github.com/en/actions/reference/security/secure-use).
[^github-reuse]: [GitHub Docs, reuse workflows](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows).
[^github-token]: [GitHub Docs, use GITHUB_TOKEN](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token).
[^github-checkout]: [Official actions/checkout repository](https://github.com/actions/checkout).
