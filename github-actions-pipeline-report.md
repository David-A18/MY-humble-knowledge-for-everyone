# GitHub Actions pipeline report

## Purpose

This report records the recent GitHub Actions failures, root causes, and remediation work for `David-A18/MY-humble-knowledge-for-everyone`.

## Latest failing run set

Latest inspected commit: `da2b97d7dff00baa18891a4ac94bba402c3a30b0`

Commit title: `docs: expand okf knowledge base guidance`

Run date: 2026-08-05

| Workflow | Run ID | Result | Finding |
| --- | --- | --- | --- |
| Link check | `30994808777` | Failed | `lychee` exited with code `2`; the workflow checked raw source archives and intentional placeholder/local example URLs. |
| Markdown lint | `30994808726` | Failed | Markdown table and nested fence issues produced MD056, MD040, MD031, and MD053 failures. |
| Terraform format | `30994808745` | Passed | Formatting passed, but the workflow emitted an action runtime deprecation warning. |

## Root causes

| Area | Root cause | Fix |
| --- | --- | --- |
| Markdown table parsing | `migrations/velero/fundamentals.md` used an unescaped pipe inside an inline command in a table cell. | Escaped the pipe in `kubectl get crd \| grep velero.io`. |
| Nested Markdown examples | `ai/ai-tooling/knowledge-bases-creation-management-and-optimization.md` embedded fenced Markdown examples that contained shorter inner fences. | Changed outer fences to four backticks and added required blank lines around closing fences. |
| Link check scope | `link-check.yml` scanned `sources/incoming` and `sources/processed`, even though the repository treats those as raw intake/archive areas. | Added `lychee.toml` with `exclude_path` entries for those directories. |
| Placeholder links | Documentation examples intentionally include `example.com`, `github.com/example/...`, `localhost`, and loopback URLs. | Added explicit `lychee` exclude patterns for those non-production examples. |
| Action runtime warnings | Existing workflows used older action major versions that produced Node.js 20 deprecation warnings. | Updated workflow action refs to current releases: `actions/checkout@v7.0.1`, `DavidAnson/markdownlint-cli2-action@v24.2.0`, and `hashicorp/setup-terraform@v4.0.1`. |

## Changed files

| File | Reason |
| --- | --- |
| `.github/workflows/markdown-lint.yml` | Use current checkout and markdownlint actions; pass the repository markdownlint config explicitly. |
| `.github/workflows/link-check.yml` | Use current checkout action and run `lychee` with repository config plus root-dir handling. |
| `.github/workflows/terraform-format.yml` | Use current checkout and Terraform setup actions. |
| `lychee.toml` | Centralize link-check exclusions for raw source archives and intentional example URLs. |
| `migrations/velero/fundamentals.md` | Fix MD056 table parsing. |
| `ai/ai-tooling/knowledge-bases-creation-management-and-optimization.md` | Fix nested fence and footnote lint failures. |
| `CHANGELOG.md` | Record the CI validation hardening. |

## Validation results

| Check | Result | Notes |
| --- | --- | --- |
| `git status --short --branch` | Passed with unrelated existing changes | Confirmed intended CI/report files plus pre-existing uncommitted documentation work. |
| `git diff --check` | Passed | No whitespace errors detected. |
| Internal Markdown link resolution | Passed | Curated Markdown links resolve locally; `sources/incoming` and `sources/processed` were excluded to match repository policy. |
| Stale action reference search | Passed | No remaining `actions/checkout@v4`, `DavidAnson/markdownlint-cli2-action@v19`, or `hashicorp/setup-terraform@v3` references were found. |
| Action input verification | Passed | `markdownlint-cli2-action@v24.2.0` supports `config` and `globs`; `lychee-action@v2` supports `args`. |
| `npx markdownlint-cli2 "**/*.md"` | Not run locally | Blocked because `node` and `npx` are not installed in this environment. |
| `lychee --config lychee.toml --root-dir . --verbose --no-progress "**/*.md"` | Not run locally | Blocked because `lychee` is not installed in this environment. |
| `terraform fmt -recursive -check` | Not run locally | Blocked because `terraform` is not installed in this environment. |

## Related links

- GitHub Actions run: [Link check 30994808777](https://github.com/David-A18/MY-humble-knowledge-for-everyone/actions/runs/30994808777)
- GitHub Actions run: [Markdown lint 30994808726](https://github.com/David-A18/MY-humble-knowledge-for-everyone/actions/runs/30994808726)
- GitHub Actions run: [Terraform format 30994808745](https://github.com/David-A18/MY-humble-knowledge-for-everyone/actions/runs/30994808745)
- Back to root index: [README.md](README.md)
