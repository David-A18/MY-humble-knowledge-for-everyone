# Website rollout and operations

## 1. Publish the source-side specification

Review the [requirements](requirements.md), [architecture](architecture.md), [content contract](content-contract.md), and [ADR-0005](../../../knowledge/decision-records/adr-0005-git-backed-reading-site.md) on `develop`. Run the repository's required checks, wait for CI, and merge to `main` after they pass. Preserve unrelated working-tree changes.

## 2. Publish the website project as a repository

The separate website project has been scaffolded locally. The owner creates a public GitHub repository and supplies its URL, then publishes the reviewed project. Before publishing, confirm it contains `README.md`, `docs/README.md`, `docs/deployment.md`, `docs/operations.md`, source, tests, `content-lock.json`, `redirects.json`, and Actions workflows. Link its README to this specification at the pinned source commit. License site code separately from the CC BY 4.0 knowledge content.

Before publication, confirm `content-lock.json` pins a validated source `main` SHA and the build checks that snapshot. Verify source checkout, OKF/catalog checks, route and link conversion, Markdown rendering, navigation, trust display, Pagefind, and redirect stubs. Keep source Markdown out of website Git history.

## 3. Validate the site locally and in CI

Build the same lock twice and compare normalized output. Test home, topic, concept, decision-record, draft, deprecated, callout, Mermaid, fragment, asset, and root-repository links. Confirm all published paths have one route and all removed paths have redirects. Run the [retrieval cases](../../../tests/retrieval-cases.yaml) against the built search index and meet the [requirements](requirements.md) threshold. Test keyboard, mobile, and automated accessibility on representative page types.

## 4. Connect repository updates

Add the source-side dispatch job only after the website repository and its sync workflow exist. Create a fine-grained token scoped to the website repository with Contents write permission and store it as a GitHub Actions secret in the knowledge repository. Never commit the token. Enable website Actions pull-request creation, branch protection, and required CI checks. Verify a source `main` update opens a single lock-update PR; verify duplicate, out-of-order, missed-event, and failed-validation behavior. Document token owner and rotation in website `docs/operations.md`.

## 5. Select host and release

The owner chooses the static host and domain. Set origin and base path, add the matching deployment adapter, and record rollback steps in website `docs/deployment.md`. A reviewed website `main` commit deploys its already-validated lock. Check live routes, search, source links, redirects, and license attribution before announcing the site.

After release, run the [reader-task protocol](../../../reader-test-facilitator-guide.md) with actual readers and log observed results in the existing templates or issue form. Change the site or knowledge navigation based on repeated blockers.

## Failure and rollback

- A source validation failure or missing dispatch credential stops sync without changing the deployed site. Repair the cause, then run manual reconciliation.
- A broken website PR stays unmerged. Fix rendering, source content, or redirects in the appropriate repository and rerun checks.
- A production failure is rolled back by redeploying the prior website commit and its pinned source SHA; do not read mutable source `main` during rollback.

## Related links

- [Website plan](README.md)
- [Architecture](architecture.md)
- [Content contract](content-contract.md)
- [Upgrade workflow](../../instructions/upgrade-workflow.md)
