---
type: Decision Record
title: "ADR-0004: Keep Markdown canonical and generate discovery artifacts"
description: "Keep OKF Markdown as the single curated source of truth while generating a deterministic catalog and testing navigation, command paths, and retrieval cases in CI."
tags: [decision-records, okf, retrieval, quality]
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
  - id: okf-v02
    resource: https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md
    title: Open Knowledge Format v0.2 specification
  - id: diataxis
    resource: https://diataxis.fr/
    title: Diátaxis documentation framework
  - id: mkdocs-navigation
    resource: https://www.mkdocs.org/user-guide/writing-your-docs/
    title: MkDocs writing and navigation guide
  - id: backstage-techdocs
    resource: https://backstage.io/docs/features/techdocs/
    title: Backstage TechDocs documentation
stale_after: 2027-03-20
---

# ADR-0004: Keep Markdown canonical and generate discovery artifacts

## Decision state

Accepted. Its site-deferral sentence was superseded by [ADR-0005](adr-0005-git-backed-reading-site.md); the canonical Markdown, catalog, and quality-gate decisions remain active.

## Context

The knowledge base is an OKF v0.2 bundle intended for both people and AI agents. Markdown indexes are reliable for browsing, but an agent or future search tool should not need to reparse every document merely to discover titles, types, lifecycle state, owners, review deadlines, and source identifiers.

A review also found that Markdown-link validation cannot detect paths embedded in fenced command examples. A successful CI run had skipped the Terraform examples after the OKF move because the workflow still searched the former root path.

Public documentation systems provide a useful pattern: keep human-authored Markdown as the source of truth, then generate navigation or search artifacts and validate them in CI. The applicable principles are portable Markdown from OKF, one reader outcome per Diátaxis concept, explicit navigation from MkDocs, and documentation-as-code publication from Backstage TechDocs.
[^okf-v02][^diataxis][^mkdocs-navigation][^backstage-techdocs]

## Decision

Keep `knowledge/` as the only canonical curated corpus. Generate
`generated/knowledge-catalog.json` deterministically from OKF frontmatter and
commit it as a derived artifact for retrieval, filtering, and maintenance tools.

Maintain a small golden set in `tests/retrieval-cases.yaml`: a set of
reference reader questions with expected concepts and source IDs.
Validate it against the generated catalog in CI.

Treat fenced command paths as documentation behavior. Validate that they do not reference the pre-OKF root layout. Keep the local-link validator as the authority for Markdown targets and fragments.

The original site clause said: "Do not add a static site yet. Revisit
ADR-0003 after reader testing shows that repository navigation cannot
meet measured discovery or readability needs." [ADR-0005](adr-0005-git-backed-reading-site.md)
superseded that timing choice. The remaining requirement for any site
to consume canonical Markdown and the derived catalog, without
creating a second content source, remains active.

## Options considered

| Option | Benefits | Costs and risks |
| --- | --- | --- |
| Canonical Markdown plus generated catalog and tests | Preserves portable human-readable sources, makes AI discovery fast, and keeps derived data reproducible. | Requires contributors to rebuild the catalog and maintain a small test set. |
| Parse Markdown at every retrieval request | Has no derived artifact to maintain. | Repeats work, makes filtering slower, and complicates reliable tooling. |
| Build a static site immediately | Could add site search and a polished reader interface. | Adds a publishing surface before reader evidence identifies the need. |
| Hand-maintain an external catalog | Can support customized tooling. | Creates drift and a second source of truth. |

## Consequences

- Metadata changes require `python3 scripts/build-knowledge-catalog.py` before commit.
- CI rejects a stale catalog, invalid retrieval cases, invalid command paths, or invalid OKF metadata.
- A catalog is a discovery aid, not a trust substitute; `draft`, `stable`, source, review, and freshness data remain visible to consumers.
- The initial golden set is structural. A future retrieval service must measure ranking, grounding, citations, and context cost against the same cases.

## How to read this decision today

A concept's Markdown frontmatter is the authored record. For example,
if a contributor changes its title or source IDs, they rebuild
`generated/knowledge-catalog.json`; they do not edit the catalog as a
separate source. CI checks that the derived catalog and retrieval cases
still match the bundle. The website design uses that catalog to discover
concepts, reads `index.md` files for topic routes, and builds its own
search files from the rendered pages. Those search files are another
derived output, not a second knowledge base.

Reconsider the catalog shape when an OKF version changes the metadata
contract or measured retrieval tasks show missing fields. Review this
decision by its recorded `stale_after` date; do not treat that deadline
as evidence that a review already happened.

## Related links

- [Generated knowledge artifacts](../../generated/README.md)
- [Knowledge-quality test data](../../tests/README.md)
- [Knowledge-base readiness review](../../knowledge-base-review.md)
- [ADR-0003: searchable site decision](adr-0003-searchable-site-decision.md)
- [ADR-0005: Git-backed reading site](adr-0005-git-backed-reading-site.md)
- [Decision records](index.md)
- [Back to knowledge index](../index.md)

[^okf-v02]: [Open Knowledge Format v0.2 specification](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md).
[^diataxis]: [Diátaxis documentation framework](https://diataxis.fr/).
[^mkdocs-navigation]: [MkDocs writing and navigation guide](https://www.mkdocs.org/user-guide/writing-your-docs/).
[^backstage-techdocs]: [Backstage TechDocs documentation](https://backstage.io/docs/features/techdocs/).
