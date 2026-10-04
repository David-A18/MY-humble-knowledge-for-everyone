---
type: Decision Record
title: "ADR-0005: Publish a Git-backed reading site"
description: "Present the canonical OKF bundle through a separate static website built from a reviewed, pinned knowledge-base revision."
tags: [decision-records, okf, publishing, website]
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
---

# ADR-0005: Publish a Git-backed reading site

## Decision state

Accepted. Supersedes the wait-for-reader-testing decision in [ADR-0003](adr-0003-searchable-site-decision.md) and the site deferral in [ADR-0004](adr-0004-machine-readable-discovery.md). The canonical-content and derived-catalog decisions in ADR-0004 remain in force.

## Context

The repository provides an OKF v0.2 bundle, validated relative links, a derived concept catalog, and a reader-test protocol. The owner wants a public, linked reading site in a separate repository. Independent reader sessions had not been recorded when this decision was made; it reflects owner direction rather than claimed reader evidence.

## Decision

Publish a static presentation of the full reader-facing `knowledge/` bundle from an exact commit on this repository's `main` branch. Keep Markdown and its frontmatter authoritative. The website repository owns rendering, derived search files, redirects, build validation, and deployment; it must not maintain a second content database or a hand-edited copy of the corpus.

Each source update is proposed as a pinned-commit pull request in the website repository and reviewed before deployment. The first release includes browsable topic indexes, readable concepts, internal links, search, and visible trust and attribution information. Reader testing follows the first public release using the existing task protocol.

## Options considered

| Option | Benefit | Cost or risk |
| --- | --- | --- |
| Static build from a pinned Git commit | Reviewable releases, reliable browsing, and rebuildable search without a runtime content service. | Site updates require a build and a reviewed pull request. |
| Read GitHub at request time | Content could appear without rebuilding. | GitHub availability, API limits, runtime complexity, and harder release validation affect readers. |
| Keep GitHub Markdown as the only reading surface | No website maintenance. | Does not provide the requested reading and search experience. |

## Consequences

- Site content can lag behind source `main` until an update pull request is merged; the displayed source commit makes that visible.
- A moved source path changes its website route and requires a redirect.
- The existing catalog remains derived and covers concepts; website indexes are resolved from the bundle's `index.md` files.
- Site launch has a host-selection gate. Reader tests run after launch and may change navigation priorities, without being represented as prelaunch evidence.

## What this means for a reader and maintainer

Imagine a contributor improves one concept in `knowledge/` and merges
it to the source `main` branch. Under this design, a site release keeps
showing its previous, reviewable version until a website update pins
the new full commit SHA and passes the site build. That pin tells a
reader exactly which source revision produced the page. It also lets
a maintainer rebuild that release from the same source and dependencies.

The website build is designed to read the generated catalog for concept discovery and the
bundle's `index.md` files for topic routes. Search files are built from
the rendered static pages. Both catalog and search output are derived
from Markdown; neither is an independent place to edit knowledge.

Reconsider the site design after the first reader-task sessions if
people cannot find or understand pages, or if a host cannot meet the
documented accessibility and release checks. Record observed problems
and a new decision before changing the canonical-source boundary.

## Related links

- [Website upgrade plan](../../knowledge-base-upgrade/features/knowledge-website/README.md)
- [Reader test facilitator guide](../../reader-test-facilitator-guide.md)
- [Decision records](index.md)
- [Knowledge index](../index.md)
