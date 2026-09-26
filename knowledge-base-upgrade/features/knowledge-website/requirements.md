# Website requirements

## Reader and outcome

The first audience is public engineering learners and practitioners already served by the [knowledge bundle](../../../knowledge/index.md). A reader must be able to begin at the home index, browse topics, follow contextual links, search for a task, and judge a page's recorded status and sources.

## First release

1. Publish every `index.md` and concept Markdown file under `knowledge/`, including decision records, templates, and asset guidance. Do not expose any `log.md` as a website page.
2. Use `knowledge/index.md` as the home page. Provide topic navigation from index hierarchy, breadcrumbs, in-page heading navigation, and the authored cross-links. Do not infer or display backlinks in the first release.
3. Provide client-side search over published pages. Index title, description, tags, and article body when present. Search results identify the page title, summary, route, and status. Browsing and reading work without JavaScript; only search requires it.
4. Show concept `status`, `maturity`, `maintainer`, `stale_after`, recorded source links, and verification details only when present. Clearly label drafts and deprecated pages. Distinguish a passed review deadline from a claim that the content is wrong. Show the exact source commit and a source-file link on every page.
5. Preserve GitHub-flavored Markdown, tables, footnotes, fenced code, admonition callouts, and Mermaid diagrams. Make code, tables, diagrams, and navigation usable on narrow screens and with a keyboard.
6. Provide CC BY 4.0 attribution and a license link for published knowledge. Keep the website's code license separate from the source content license.

The site does not need accounts, a content editor, comments, analytics, a CMS, a content database, live GitHub reads, AI answers, or a write API for this release.

## Quality targets

| Area | Acceptance criterion |
| --- | --- |
| Coverage | Every published Markdown file has exactly one canonical route; the derived catalog covers every published concept and no reserved index. |
| Links | All site-internal links, fragments, local assets, and redirect targets resolve. Links to non-published repository files open the pinned GitHub revision. |
| Search | For every case in [retrieval-cases.yaml](../../../tests/retrieval-cases.yaml), at least one expected page appears in the first ten results; failures are fixed or explicitly reviewed before launch. |
| Trust | Draft and deprecated examples show the expected labels; missing evidence is never presented as a completed review. |
| Accessibility | Home, topic, concept, and search templates have no serious or critical automated accessibility violations; keyboard and mobile checks are recorded. |
| Reproducibility | A fixed source SHA and locked site dependencies produce the same routes, page content, and search index. Deployment-only origin values may differ by environment. |
| Release | A website content-lock pull request passes checks and is reviewed before its source revision is deployed. |

## Post-launch evidence

Run the existing [reader tasks](../../../reader-test-facilitator-guide.md) on the live site after launch. Record participant outcomes and repeated blockers without inventing or exposing personal details. Use the evidence to change navigation and search priorities.

## Related links

- [Architecture](architecture.md)
- [Content contract](content-contract.md)
- [Rollout](rollout.md)
- [Website plan](README.md)
