---
type: "Explanation"
title: "SonarQube GitHub integration"
description: "Use this page to set the right mental model for SonarQube Server and GitHub integration: repository import and binding, GitHub Actions analysis, pull request decoration, required checks, and security alert reporting."
tags: [devops, code-quality, sonarqube-github-integration]
status: draft
maturity: draft
audience: "Engineering learners and practitioners"
maintainer: "unassigned"
---

# SonarQube GitHub integration

## Purpose

Use this page to set the right mental model for SonarQube Server and GitHub integration: repository import and binding, GitHub Actions analysis, pull request decoration, required checks, and security alert reporting.

In SonarQube documentation this is usually called GitHub integration or DevOps platform integration. In team conversations, "GitHub sync" often means one of several different behaviors, so clarify which one is needed before implementation.

## What sync can mean

| Team phrase | Actual capability | Direction |
| --- | --- | --- |
| Import GitHub repositories | Create SonarQube projects from GitHub repositories. | GitHub to SonarQube. |
| Bind project to repository | Associate an existing or imported SonarQube project with a GitHub repository. | Configuration link. |
| Analyze with GitHub Actions | Run SonarScanner from a GitHub Actions workflow and send results to SonarQube. | GitHub Actions to SonarQube. |
| Pull request decoration | Show quality gate, metrics, and annotations in GitHub pull requests. | SonarQube to GitHub. |
| Required status check | Block merge when the SonarQube quality gate check fails. | GitHub branch protection. |
| Code scanning alerts | Report security issues into GitHub code scanning alerts when configured and licensed. | SonarQube to GitHub, with status synchronization for supported alerts. |
| User authentication | Let users sign in to SonarQube with GitHub. | GitHub identity to SonarQube. |

> [!IMPORTANT]
> SonarQube does not continuously mirror repository contents like a file sync tool. Code reaches SonarQube through scanner analysis. Integration metadata lets SonarQube associate analysis with the correct repository, pull request, checks, and alerts.

## Prerequisites

- Global `Administer System` permission in SonarQube Server for global GitHub integration setup.
- A reachable SonarQube Server base URL for GitHub-hosted or self-hosted runners that perform analysis.
- A GitHub App configured for the GitHub organization or GitHub Enterprise instance.
- Repository access in GitHub and `Create Projects` permission in SonarQube for importing repositories.
- `SONAR_TOKEN` stored as a GitHub secret and `SONAR_HOST_URL` stored as a GitHub variable or secret.
- Full Git checkout in CI when pull request, branch, blame, or new-code detection depends on SCM data.

## Setup sequence

1. Configure the SonarQube Server base URL.
2. Create and install the GitHub App for the target GitHub organization or instance.
3. Add the GitHub App configuration to SonarQube global DevOps platform integration settings.
4. Import GitHub repositories into SonarQube or bind existing SonarQube projects to repositories.
5. Add SonarQube analysis to GitHub Actions.
6. Run analysis on the main branch at least once.
7. Run analysis on pull requests.
8. Confirm pull request decoration appears in GitHub Checks, Conversation, and inline annotations where supported.
9. Add the SonarQube quality gate status as a required check in GitHub branch protection when the team is ready to enforce it.
10. Configure security alert reporting if the edition and GitHub security setup support it.

## GitHub Actions workflow

```yaml
name: code-quality

on:
  push:
    branches:
      - main
  pull_request:
    types:
      - opened
      - synchronize
      - reopened

permissions:
  contents: read
  pull-requests: read

jobs:
  sonarqube:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
        with:
          fetch-depth: 0

      - name: SonarQube scan
        uses: SonarSource/sonarqube-scan-action@v7
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          SONAR_HOST_URL: ${{ vars.SONAR_HOST_URL }}
```

What it does: runs analysis on pushes to `main` and on pull request updates, sends results to SonarQube Server, and gives SonarQube enough Git metadata to detect new code and pull request context.

> [!NOTE]
> Build-wrapper, Maven, Gradle, .NET, JavaScript, TypeScript, and coverage setup can require language-specific scanner configuration. Keep the workflow example minimal, then add build and coverage steps before the scan.

## Pull request decoration and merge control

For bound projects, SonarQube can report quality gate status and analysis details back to GitHub pull requests after pull request analysis is working. GitHub branch protection can then require the SonarQube status check before merge.

Recommended rollout:

1. Run the scan without blocking merges.
2. Confirm that pull request decoration appears and findings are actionable.
3. Fix false configuration issues such as missing coverage or generated-code scope.
4. Agree on quality gate policy with maintainers.
5. Add the SonarQube check to branch protection.

> [!WARNING]
> Do not make the SonarQube check required until scanner reliability is stable. A broken scanner, unreachable server, missing secret, or bad coverage path can block all merges even when the code itself is fine.

## Security alert reporting

SonarQube Server can report supported security issues into GitHub code scanning alerts when the GitHub integration and security alert reporting are configured. This is separate from normal pull request decoration.

Operational checks:

- Confirm the SonarQube edition supports the desired GitHub security alert behavior.
- Confirm the GitHub App has the permissions required by the SonarQube setup guide.
- Confirm the repository has GitHub code scanning enabled where required.
- Decide whether security alert triage status should be managed in SonarQube, GitHub, or both.
- Test status synchronization with a non-critical finding before relying on it for governance reporting.

## Troubleshooting

| Symptom | Likely cause | Next step |
| --- | --- | --- |
| Repository cannot be imported | GitHub App is not installed on the organization or lacks repository access. | Check GitHub App installation scope and SonarQube global integration settings. |
| Project is analyzed but not decorated in GitHub | Project is not bound to the GitHub repository or PR analysis is not detected. | Import or bind the project and verify pull request analysis parameters. |
| PR analysis misses changed-code context | Shallow clone, missing target branch, or modified checkout state. | Use `fetch-depth: 0` and avoid synthetic merge previews that confuse SCM data. |
| Required check never appears | No successful analysis has reported that check name yet. | Run the workflow on a branch or PR and then select the SonarQube check in branch protection. |
| GitHub-hosted runner cannot reach SonarQube | Server base URL is private or blocked by network rules. | Use a reachable URL, self-hosted runner, VPN path, or firewall allowlist. |
| Scanner cannot trust SonarQube TLS certificate | Private CA certificate is not available to the runner. | Configure the runner trust store or scanner certificate environment according to SonarQube docs. |

## Related links

- [Official SonarQube GitHub integration documentation](https://docs.sonarsource.com/sonarqube-server/2026.1/devops-platform-integration/github-integration/introduction)
- [Global GitHub integration setup](https://docs.sonarsource.com/sonarqube-server/2026.1/devops-platform-integration/github-integration/setting-up-at-global-level/introduction)
- [Importing GitHub repositories](https://docs.sonarsource.com/sonarqube-server/2026.1/devops-platform-integration/github-integration/importing-github-repositories)
- [Adding analysis to GitHub Actions workflow](https://docs.sonarsource.com/sonarqube-server/2026.1/devops-platform-integration/github-integration/adding-analysis-to-github-actions-workflow)
- [Pull request analysis setup](https://docs.sonarsource.com/sonarqube-server/2026.1/analyzing-source-code/pull-request-analysis/setting-up-the-pull-request-analysis)
- [Issues reported in GitHub](https://docs.sonarsource.com/sonarqube-server/2026.1/user-guide/issues/in-devops-platform/github)
- [SonarQube](sonarqube.md)
- [GitHub Actions](../../git/github-actions/index.md)
- [Back to code quality index](index.md)
- [Back to DevOps index](../index.md)
- [Back to root index](../../../README.md)
