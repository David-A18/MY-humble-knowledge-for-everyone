# GitHub Actions pipeline report

## Purpose

This report records the recent GitHub Actions failures, root causes, and remediation work for `David-A18/MY-humble-knowledge-for-everyone`.

## Latest failing run set

Latest inspected commit: `da2b97d7dff00baa18891a4ac94bba402c3a30b0`

Commit title: `docs: expand okf knowledge base guidance`

Run date: 2026-08-05

| Workflow | Run ID | Result | Finding |
| --- | --- | --- | --- |
| Link check | `30994808777` | Failed | `lychee` exited with code `2`; the workflow checked raw source archives and intentional placeholder/local example URLs. A follow-up run on commit `119d4771764bbd3c1bea444b0ee897c4cc4b885c` also exposed two stale curated external documentation links. |
| Markdown lint | `30994808726` | Failed | Markdown table and nested fence issues produced MD056, MD040, MD031, and MD053 failures. |
| Terraform format | `30994808745` | Passed | Formatting passed, but the workflow emitted an action runtime deprecation warning. |

## Root causes

| Area | Root cause | Fix |
| --- | --- | --- |
| Markdown table parsing | `migrations/velero/fundamentals.md` used an unescaped pipe inside an inline command in a table cell. | Escaped the pipe in `kubectl get crd \| grep velero.io`. |
| Nested Markdown examples | `ai/ai-tooling/knowledge-bases-creation-management-and-optimization.md` embedded fenced Markdown examples that contained shorter inner fences. | Changed outer fences to four backticks and added required blank lines around closing fences. |
| Link check scope | `link-check.yml` scanned `sources/incoming` and `sources/processed`, even though the repository treats those as raw intake/archive areas. | Added `lychee.toml` with `exclude_path` entries for those directories. |
| Placeholder links | Documentation examples intentionally include `example.com`, `github.com/example/...`, `localhost`, and loopback URLs. | Added explicit `lychee` exclude patterns for those non-production examples. |
| CI evidence links | The report links to GitHub Actions run pages for auditability, but those pages are CI evidence rather than documentation dependencies and can vary by GitHub execution context. | Excluded repository GitHub Actions run-page URLs from lychee while keeping them visible in the report. |
| Stale official links | Local reproduction with `lychee-v0.24.2` found 404s for the AWS CLI v2 `update-kubeconfig` path and the removed Velero `troubleshoot-restore` page. | Replaced them with the current AWS CLI `latest` command reference and the Velero `restore-reference` page. |
| Action runtime warnings | Existing workflows used older action major versions that produced Node.js 20 deprecation warnings. | Updated workflow action refs to current releases: `actions/checkout@v7.0.1`, `DavidAnson/markdownlint-cli2-action@v24.2.0`, and `hashicorp/setup-terraform@v4.0.1`. |

## Changed files

| File | Reason |
| --- | --- |
| `.github/workflows/markdown-lint.yml` | Use current checkout and markdownlint actions; pass the repository markdownlint config explicitly. |
| `.github/workflows/link-check.yml` | Use current checkout action, run `lychee` with repository config plus absolute root-dir handling, and expose lychee output when failures occur. |
| `.github/workflows/terraform-format.yml` | Use current checkout and Terraform setup actions. |
| `lychee.toml` | Centralize link-check exclusions for raw source archives, intentional example URLs, and GitHub Actions evidence links. |
| `migrations/velero/fundamentals.md` | Fix MD056 table parsing. |
| `migrations/velero/possible-integrations.md` | Replace a stale AWS CLI command reference URL. |
| `migrations/velero/troubleshooting-and-operations.md` | Replace a removed Velero restore troubleshooting URL. |
| `ai/ai-tooling/knowledge-bases-creation-management-and-optimization.md` | Fix nested fence and footnote lint failures. |
| `CHANGELOG.md` | Record the CI validation hardening. |

## Validation results

Remote validation commit: `bb2c4bd`

Run date: 2026-08-07

| Workflow | Run ID | Result | Notes |
| --- | --- | --- | --- |
| Link check | `31175695827` | Passed | Confirmed `lychee` succeeds after excluding raw source archives, excluding intentional examples, using an absolute root dir, and replacing two stale external links. |
| Markdown lint | `31175695736` | Passed | Confirmed the Velero table escape and OKF nested fence fixes. |
| Terraform format | `31175695734` | Passed | Confirmed Terraform formatting workflow succeeds after action upgrades. |

| Check | Result | Notes |
| --- | --- | --- |
| `git status --short --branch` | Passed with unrelated existing changes | Confirmed intended CI/report files plus pre-existing uncommitted documentation work. |
| `git diff --check` | Passed | No whitespace errors detected. |
| Internal Markdown link resolution | Passed | Curated Markdown links resolve locally; `sources/incoming` and `sources/processed` were excluded to match repository policy. |
| Stale action reference search | Passed | No remaining `actions/checkout@v4`, `DavidAnson/markdownlint-cli2-action@v19`, or `hashicorp/setup-terraform@v3` references were found. |
| Action input verification | Passed | `markdownlint-cli2-action@v24.2.0` supports `config` and `globs`; `lychee-action@v2` supports `args`. |
| `npx markdownlint-cli2 "**/*.md"` | Not run locally | Blocked because `node` and `npx` are not installed in this environment. |
| `lychee-v0.24.2 --config lychee.toml --root-dir <repo> --verbose --no-progress "**/*.md"` | Passed | Downloaded the same lychee release used by `lychee-action@v2` to a temporary directory, reproduced the two stale links, fixed them, and reran successfully. |
| `terraform fmt -recursive -check` | Not run locally | Blocked because `terraform` is not installed in this environment. |

## Related links

- GitHub Actions run: [Link check 30994808777](https://github.com/David-A18/MY-humble-knowledge-for-everyone/actions/runs/30994808777)
- GitHub Actions run: [Markdown lint 30994808726](https://github.com/David-A18/MY-humble-knowledge-for-everyone/actions/runs/30994808726)
- GitHub Actions run: [Terraform format 30994808745](https://github.com/David-A18/MY-humble-knowledge-for-everyone/actions/runs/30994808745)
- Back to root index: [README.md](README.md)
