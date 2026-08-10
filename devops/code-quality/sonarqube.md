# SonarQube

## Purpose

Use this page to understand SonarQube Server as a code quality and security analysis platform, how analysis reaches the server, and how teams should use quality gates in delivery workflows.

SonarQube does not replace tests, reviews, threat modeling, or dependency scanning. It provides repeatable static analysis, issue tracking, quality gates, and pull request feedback so teams can keep new code clean while improving existing code over time.

## When to use this

- You need consistent static analysis across repositories and languages.
- You want a quality gate before merging or releasing code.
- You want pull request feedback focused on new code.
- You need a central place for code smells, bugs, vulnerabilities, security hotspots, coverage, duplication, and maintainability metrics.

## Core model

| Concept | Meaning | Why it matters |
| --- | --- | --- |
| Project | SonarQube representation of one analyzed codebase or component. | Holds analysis history, issues, metrics, quality gate status, and settings. |
| SonarScanner | Build-time tool that reads source code and sends analysis results to SonarQube Server. | Analysis normally runs from CI so results match reviewed code. |
| Quality profile | Set of analysis rules for a language. | Controls which rules detect issues during analysis. |
| Quality gate | Conditions that decide whether analysis passes or fails. | Converts analysis results into an enforceable delivery signal. |
| New code | Code recently added or changed according to the configured new-code definition. | Keeps teams focused on preventing new problems instead of trying to clean all legacy code at once. |
| Issue | Finding raised by a rule. | Represents something to review, fix, accept, or mark false positive according to policy. |
| Security hotspot | Security-sensitive code that requires review. | Helps ensure risky constructs are inspected even when they are not confirmed vulnerabilities. |
| Pull request analysis | Analysis of changed code in a pull request. | Reports issues and quality gate status before merge. |

## Analysis flow

```text
developer pushes code
  -> CI checks out full repository history
  -> build and tests run
  -> SonarScanner analyzes source, coverage, and SCM data
  -> SonarQube Server stores issues and measures
  -> quality gate is computed
  -> CI and pull request receive pass or fail signal
```

What it does: makes code analysis part of the same delivery path as build and test validation.

> [!IMPORTANT]
> SonarQube analysis depends on accurate source control metadata. For GitHub Actions, use a full checkout with `fetch-depth: 0` when SonarQube needs blame, branch, or pull request context.

## Quality gate strategy

| Situation | Recommended approach | Reason |
| --- | --- | --- |
| New project | Start with the built-in recommended gate unless policy requires stricter controls. | Gives a known baseline without inventing rules too early. |
| Legacy project | Enforce the gate on new code first. | Prevents new debt while allowing planned remediation of old issues. |
| Regulated or security-sensitive service | Add explicit security, hotspot review, and coverage expectations. | Aligns merge policy with the service risk profile. |
| Monorepo | Decide whether one SonarQube project or multiple projects match ownership boundaries. | Keeps issue assignment, quality gates, and metrics meaningful. |
| Generated code | Exclude generated paths or configure analysis scope intentionally. | Avoids wasting review effort on code people do not maintain. |

## Minimal GitHub Actions scanner example

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

jobs:
  sonar:
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

What it does: checks out the repository with full history and runs the SonarQube scan action using a token stored as a secret and the server URL stored as a variable.

> [!WARNING]
> Do not hardcode SonarQube tokens in workflow files, scanner properties, Docker images, or repository scripts. Store tokens in CI secrets and scope them to the smallest practical project or organization boundary.

## Operating practices

- Run analysis on pull requests and on the main branch.
- Keep the quality gate visible in branch protection or merge rules when the team intends to enforce it.
- Treat quality profile changes like production policy changes: review them, announce impact, and avoid surprise rule churn.
- Keep coverage reports generated before the scan and pass the expected report paths to the scanner.
- Exclude vendored, generated, build-output, and dependency directories intentionally.
- Review false positives and accepted risks in SonarQube instead of hiding broad paths from analysis.
- Monitor scanner failures separately from quality gate failures; one means analysis did not complete, the other means analysis completed and failed policy.

## Common failure modes

| Symptom | Likely cause | Next step |
| --- | --- | --- |
| Analysis fails with authentication errors | Missing, expired, or incorrectly scoped `SONAR_TOKEN`. | Regenerate the token and update the CI secret. |
| Missing blame information | Shallow clone or missing `.git` metadata. | Use full checkout history and do not remove Git metadata before scanning. |
| Coverage is `0%` | Test coverage report was not generated or path is wrong. | Generate coverage before scan and configure the language-specific report property. |
| Quality gate fails only on pull requests | New-code conditions are catching changed-code issues. | Review the PR findings and gate conditions before adjusting policy. |
| Issues appear on code the team does not own | Analysis scope includes generated, vendored, or third-party paths. | Tune inclusions and exclusions carefully. |

## Related links

- [Official SonarQube Server documentation](https://docs.sonarsource.com/sonarqube-server/)
- [Project analysis setup](https://docs.sonarsource.com/sonarqube-server/analyzing-source-code/overview)
- [Quality standards and new code](https://docs.sonarsource.com/sonarqube-server/2026.1/user-guide/about-new-code)
- [Understanding quality gates](https://docs.sonarsource.com/sonarqube-server/2026.1/quality-standards-administration/managing-quality-gates/introduction-to-quality-gates)
- [SonarQube GitHub integration](sonarqube-github-integration.md)
- [GitHub Actions](../../git/github-actions/README.md)
- [Back to code quality index](README.md)
- [Back to DevOps index](../README.md)
- [Back to root index](../../README.md)
