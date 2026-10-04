---
type: "Decision Record"
title: "ADR-0002: Source ingestion and topic taxonomy"
description: "Stage raw source notes outside the curated knowledge bundle, then classify and link each reviewed article into a growing topic taxonomy."
tags: [decision-records]
status: draft
maturity: draft
audience: "Engineering learners and practitioners"
maintainer: "unassigned"
---

# ADR-0002: Source ingestion and topic taxonomy

Decision state: Accepted. The page's OKF `status: draft` describes its
review maturity, not whether this decision was adopted.

## Context

The knowledge base needs a clear place for raw Markdown notes before they are converted into curated documentation. It also needs explicit routes for topics that are expected to grow beyond the initial Git, Terraform, Kubernetes, and AWS sections.

## Decision

Create a root-level [sources](../../sources/README.md) area with incoming and processed folders. Agents will classify raw files, transform them into the correct article structure, update indexes and links, then archive processed raw files.

Create a cloud parent route at [cloud](../cloud/index.md), move existing AWS documentation under [cloud/aws](../cloud/aws/index.md), and reserve provider routes for Azure and Google Cloud. Add initial top-level route indexes for security, FinOps, DevOps, programming languages, MLOps, AI, AI agents, LLM, ML, and solutions architect content.

## Consequences

- Raw notes have a safe staging area before becoming curated documentation.
- AWS content becomes part of a provider hierarchy instead of a standalone top-level area.
- Future agents can place new material using a consistent topic taxonomy.
- Internal links must be updated when moving provider-specific content under `cloud/`.

## How to read this decision today

Rough notes and published guidance serve different purposes. A note in
root-level [`sources/`](../../sources/README.md) is input to review;
it is not a reader-facing OKF concept. Curated pages live under
[`knowledge/`](../index.md) and appear in the nearest topic index.
This separation keeps an unreviewed paste from looking like trusted
teaching material.

The route list in the original decision records the initial taxonomy.
It has since grown to include top-level databases, migrations, and
cross-topic guides, plus Crossplane under Kubernetes. Google Cloud is
currently routed as
[`cloud/gcloud`](../cloud/gcloud/index.md). The current [source
ingestion instructions](../../sources/AGENTS.md) give the route table
and require each processed source to be recorded in the [ingestion
register](../../sources/processed/ingestion-register.md). Record the
verification status or `Unknown` when historical evidence is missing;
do not imply that an unknown ingestion date makes every verification
claim unknown.

Reconsider the taxonomy when a new subject repeatedly fits no route or
when a planned route misleads readers about available articles. Do not
create a new topic label merely to make one incoming note fit.

## Related links

- [Sources](../../sources/README.md)
- [Source ingestion instructions](../../sources/AGENTS.md)
- [Cloud](../cloud/index.md)
- [AI agent router](../../AGENTS.md)
- [Back to decision records](index.md)
- [Back to root index](../../README.md)
