# Processed source ingestion register

Status: Draft
Audience: Contributors and maintainers
Page type: Reference
Maintainer: Unassigned
Last substantive review: 2026-09-19
Applicable versions: Repository state at commit `1079a0d`
Validation evidence: Source archive filenames and curated destinations checked against current repository paths; historical ingestion details reconstructed from current files and changelog, not from original handoff notes
Known limitations: Older ingestion dates, exact source verification steps, and unresolved questions are unknown unless stated in the curated articles
Next review: During the next source-ingestion maintenance pass

## Purpose

Track how archived raw Markdown files under `sources/processed` relate to curated knowledge-base destinations. This register prevents archived notes from becoming a second, untraceable documentation corpus.

For older processed sources, the mappings below are reconstructed from current repository paths and changelog summaries. Use `Unknown` rather than inventing missing ingestion details.

## Register

| Processed source | Principal topic | Curated destinations | Ingestion date | Verification status | Open questions |
| --- | --- | --- | --- | --- | --- |
| [akamai-vs-amazon-cloudfront-complete-guide.md](akamai-vs-amazon-cloudfront-complete-guide.md) | Cloud edge | [Akamai vs. CloudFront](../../knowledge/cloud/edge/akamai-vs-cloudfront.md), [CDN fundamentals](../../knowledge/cloud/edge/cdn-and-edge-fundamentals.md), [CDN caching and origin protection](../../knowledge/cloud/edge/cdn-caching-and-origin-protection.md), [multi-CDN operations](../../knowledge/cloud/edge/multi-cdn-operations.md), [CDN in front of EKS](../../knowledge/cross-topic-guides/cdn-in-front-of-eks.md) | Unknown | Curated before this register; current paths verified | Original source-review evidence unknown. |
| [apache-apisix-kubernetes-eks-complete-guide.md](apache-apisix-kubernetes-eks-complete-guide.md) | Kubernetes and cross-topic | [Apache APISIX](../../knowledge/kubernetes/applications-and-tools/apache-apisix.md), [APISIX architecture and deployment](../../knowledge/kubernetes/applications-and-tools/apisix-architecture-and-deployment.md), [APISIX security, traffic, and observability](../../knowledge/kubernetes/applications-and-tools/apisix-security-traffic-and-observability.md), [APISIX troubleshooting](../../knowledge/kubernetes/troubleshooting/apisix.md), [APISIX on EKS](../../knowledge/cross-topic-guides/apisix-on-eks.md) | Unknown | Curated before this register; current paths verified | Original source-review evidence unknown. |
| [apache-kafka-aws-complete-guide.md](apache-kafka-aws-complete-guide.md) | Databases and AWS | [Kafka fundamentals](../../knowledge/databases/kafka/fundamentals.md), [topic and event design](../../knowledge/databases/kafka/topic-and-event-design.md), [consumer lag and replay](../../knowledge/databases/kafka/consumer-groups-lag-and-replay.md), [delivery guarantees](../../knowledge/databases/kafka/delivery-guarantees-and-failure-handling.md), [Kafka operations](../../knowledge/databases/kafka/operations.md), [Amazon MSK](../../knowledge/cloud/aws/databases/amazon-msk.md), [EKS to MSK applications](../../knowledge/cross-topic-guides/eks-to-msk-applications.md) | Unknown | Curated before this register; current paths verified | Broker integration evidence should be added when examples are expanded. |
| [aws-stateful-vs-stateless-complete-guide.md](aws-stateful-vs-stateless-complete-guide.md) | AWS architecture | [Stateful vs. stateless](../../knowledge/cloud/aws/architecture/stateful-vs-stateless.md), [stateless application patterns](../../knowledge/cloud/aws/architecture/stateless-application-patterns.md), [stateful design decision checklist](../../knowledge/cloud/aws/architecture/stateful-design-decision-checklist.md), [stateful networking](../../knowledge/cloud/aws/networking/stateful-networking.md) | Unknown | Curated before this register; current paths verified | Original source-review evidence unknown. |
| [crossplane-complete-study-guide.md](crossplane-complete-study-guide.md) | Kubernetes Crossplane | [Crossplane](../../knowledge/kubernetes/crossplane/index.md), [component model](../../knowledge/kubernetes/crossplane/component-model.md), [managed resources and lifecycle](../../knowledge/kubernetes/crossplane/managed-resources-and-lifecycle.md), [providers and authentication](../../knowledge/kubernetes/crossplane/providers-and-authentication.md), [compositions](../../knowledge/kubernetes/crossplane/compositions.md), [deployment patterns and references](../../knowledge/kubernetes/crossplane/deployment-patterns-and-references.md), [Crossplane on AWS](../../knowledge/cross-topic-guides/crossplane-on-aws.md) | Unknown | Curated before this register; current paths verified | AWS sandbox execution evidence remains separate from source ingestion. |
| [gitops-argo-cd-vs-flux-detailed-guide.md](gitops-argo-cd-vs-flux-detailed-guide.md) | Kubernetes GitOps | [GitOps](../../knowledge/kubernetes/applications-and-tools/gitops.md), [Argo CD vs. Flux](../../knowledge/kubernetes/applications-and-tools/argo-cd-vs-flux.md), [Flux](../../knowledge/kubernetes/applications-and-tools/flux.md), [Flux reconciliation and Helm releases](../../knowledge/kubernetes/applications-and-tools/flux-reconciliation-and-helm.md), [GitOps security and multi-tenancy](../../knowledge/kubernetes/applications-and-tools/gitops-security-and-multitenancy.md), [GitOps on EKS](../../knowledge/cross-topic-guides/gitops-on-eks.md) | Unknown | Curated before this register; current paths verified | Original source-review evidence unknown. |
| [mongodb_complete_guide.md](mongodb_complete_guide.md) | Databases and AWS | [MongoDB fundamentals](../../knowledge/databases/mongodb/fundamentals.md), [data modeling](../../knowledge/databases/mongodb/data-modeling.md), [schema validation and indexing](../../knowledge/databases/mongodb/schema-validation-and-indexing.md), [replication, sharding, and consistency](../../knowledge/databases/mongodb/replication-sharding-and-consistency.md), [MongoDB operations](../../knowledge/databases/mongodb/operations.md), [MongoDB on AWS](../../knowledge/cloud/aws/databases/mongodb-on-aws.md), [DocumentDB vs. MongoDB Atlas](../../knowledge/cloud/aws/databases/documentdb-vs-mongodb-atlas.md) | Unknown | Curated before this register; current paths verified | Original source-review evidence unknown. |
| [oidc_aws_eks_complete_guide.md](oidc_aws_eks_complete_guide.md) | Security and AWS/EKS | [OIDC fundamentals](../../knowledge/security/identity-federation/oidc-fundamentals.md), [OIDC token validation](../../knowledge/security/identity-federation/oidc-token-validation.md), [EKS human identity and RBAC](../../knowledge/security/identity-federation/eks-human-identity-and-rbac.md), [IAM OIDC provider and STS web identity](../../knowledge/cloud/aws/security/iam-oidc-provider-and-sts-web-identity.md), [EKS workload identity](../../knowledge/cross-topic-guides/eks-workload-identity.md) | Unknown | Curated before this register; current paths verified | Original source-review evidence unknown. |
| [tooling-clusters-and-kind-custom-guide.md](tooling-clusters-and-kind-custom-guide.md) | Kubernetes tooling | [Tooling clusters](../../knowledge/kubernetes/applications-and-tools/tooling-clusters.md), [tooling cluster architecture](../../knowledge/kubernetes/applications-and-tools/tooling-cluster-architecture.md), [kind custom clusters](../../knowledge/kubernetes/applications-and-tools/kind-custom-clusters.md), [kind images and local registries](../../knowledge/kubernetes/applications-and-tools/kind-images-and-local-registries.md), [kind troubleshooting](../../knowledge/kubernetes/troubleshooting/kind.md), [EKS tooling cluster architecture](../../knowledge/cross-topic-guides/eks-tooling-cluster-architecture.md) | Unknown | Curated before this register; current paths verified | Local kind execution evidence for the current beginner path is recorded in the improvement plan; this archived source remains historical. |

## Register rules

- Add a row when raw source material moves from `sources/incoming` to `sources/processed`.
- Link every curated destination that received material from the source.
- Use `Unknown` for historical ingestion details that cannot be proven.
- Keep verification status separate from article maturity and execution evidence.
- Do not treat archived source files as curated reader-facing documentation.

## Related links

- [Processed sources](README.md)
- [Source ingestion instructions](../AGENTS.md)
- [Back to sources index](../README.md)
- [Back to root index](../../README.md)
