# Glossary

Common terms used across the knowledge base.

| Term | Meaning |
| --- | --- |
| ADR | Architecture Decision Record; a short document that captures context, decision, and consequences. |
| AI | Artificial Intelligence; systems or workflows that perform tasks associated with reasoning, generation, prediction, or automation. |
| AI agent | An AI system that can follow goals, use tools, inspect context, and take multi-step actions with feedback. |
| API gateway | A traffic entry point that routes API requests and often applies policy such as authentication, rate limits, TLS, and observability. |
| APISIX | Apache APISIX; an open-source API gateway that can run in Kubernetes and be configured through APISIX APIs, CRDs, or Gateway API integrations. |
| Argo CD | Kubernetes GitOps controller that reconciles application desired state from Git or another source into target clusters. |
| BackupRepository | Velero repository used by File System Backup or data movement to store volume data in object storage. |
| BackupStorageLocation | Velero custom resource that defines the object storage bucket, prefix, provider, and access mode used for backup artifacts. |
| BSON | Binary JSON; MongoDB's binary document format for storing documents and typed values. |
| CDN | Content Delivery Network; an edge network that caches or accelerates content close to users. |
| CI | Continuous Integration; automated validation that runs on code changes. |
| CD | Continuous Delivery or Continuous Deployment, depending on release process. |
| ClusterProviderConfig | Crossplane provider configuration that can be referenced across namespaces. |
| Composition | Crossplane implementation that maps a composite resource to composed resources through a function pipeline. |
| Composition Function | Crossplane package that supplies logic used by a Composition or Operation. |
| Composition Revision | Crossplane-generated immutable version of a Composition used for rollout and rollback control. |
| Configuration Package | Crossplane OCI package that bundles platform APIs, compositions, and package dependencies. |
| Composite Resource | Crossplane resource instance created from a Composite Resource Definition. |
| Composite Resource Definition | Crossplane definition that creates a custom platform API schema. |
| CRD | CustomResourceDefinition; a Kubernetes object that defines a custom API resource. |
| Crossplane | Kubernetes-native control-plane framework for reconciling external infrastructure and custom platform APIs. |
| CSI snapshot | Kubernetes snapshot workflow for CSI-backed persistent volumes using VolumeSnapshot, VolumeSnapshotContent, and VolumeSnapshotClass resources. |
| DeploymentRuntimeConfig | Crossplane package-runtime configuration for provider or function pods. |
| DevOps | Engineering practices that connect software delivery, automation, operations, and reliability work. |
| EnvironmentConfig | Crossplane composition data object that provides XR-specific in-memory environment values. |
| External name | Crossplane annotation that maps a Kubernetes managed resource to its real external resource identifier. |
| FinOps | A cloud financial management discipline focused on cost visibility, accountability, and optimization. |
| File System Backup | Velero volume backup method where node-agent reads mounted pod volumes and stores file data in object storage. |
| FunctionRevision | Crossplane package revision object for a concrete installed function version. |
| GitOps | An operating model where Git stores desired state and controllers reconcile infrastructure or workloads from that state. |
| IaC | Infrastructure as Code; managing infrastructure through versioned declarative or procedural definitions. |
| IRSA | IAM Roles for Service Accounts; an EKS pattern that uses Kubernetes service account tokens and IAM OIDC trust to provide AWS credentials. |
| JWKS | JSON Web Key Set; a document containing public keys used to verify tokens signed by an identity provider. |
| Kafka | Distributed event streaming platform used for durable event logs, producers, consumers, and stream processing. |
| kind | Kubernetes in Docker; a local Kubernetes tool that runs cluster nodes as containers. |
| Kopia | Backup tool used by Velero File System Backup and data movement paths to store deduplicated volume data. |
| KRaft | Kafka's Raft-based metadata mode that replaces ZooKeeper for Kafka cluster metadata management. |
| Least privilege | Granting only the permissions needed to perform a task. |
| LLM | Large Language Model; a model trained to process and generate language and other structured content. |
| Managed Resource | Crossplane provider-defined Kubernetes object that represents an external resource. |
| Managed Resource Activation Policy | Crossplane v2 policy that activates selected managed-resource APIs from a provider. |
| Managed Resource Definition | Crossplane v2 representation of a provider managed-resource API before or while it is activated into a Kubernetes CRD. |
| ML | Machine Learning; systems that learn patterns from data to make predictions, classifications, or decisions. |
| MLOps | Operational practices for deploying, monitoring, governing, and maintaining machine learning systems. |
| MongoDB | Document database that stores JSON-like BSON documents and supports flexible document modeling. |
| MSK | Amazon Managed Streaming for Apache Kafka; AWS managed service for Kafka-compatible streaming workloads. |
| MTTR | Mean Time To Recovery; a reliability metric for how quickly service is restored after failure. |
| OIDC | OpenID Connect; identity protocol built on OAuth 2.0 that issues signed identity tokens with claims. |
| Node-agent | Velero DaemonSet that runs file-system backup and data movement work on Kubernetes nodes. |
| Operation | Crossplane run-to-completion function pipeline for maintenance or operational tasks. |
| PKCE | Proof Key for Code Exchange; an OAuth 2.0 extension used with authorization code flows to reduce authorization-code interception risk. |
| Platform API | Stable internal API exposed by a platform team to hide implementation details behind a product-like request shape. |
| ProviderConfig | Crossplane provider configuration scoped to a namespace. |
| ProviderRevision | Crossplane package revision object for a concrete installed provider version. |
| RPO | Recovery Point Objective; acceptable data loss measured in time. |
| RTO | Recovery Time Objective; acceptable time to restore service after an outage. |
| Runbook | A repeatable operational procedure for known tasks or incidents. |
| SLO | Service Level Objective; a reliability target for a service behavior. |
| Tagging strategy | A consistent scheme for metadata used in ownership, cost allocation, automation, and governance. |
| Tooling cluster | Kubernetes cluster dedicated to platform tools such as GitOps, observability, policy, CI/CD runners, or developer experience services. |
| Usage | Crossplane resource that protects a depended-on resource from deletion or controls deletion ordering. |
| Velero | Kubernetes backup, restore, disaster recovery, and cluster migration tool that stores cluster resources in object storage and can protect persistent volume data. |
| VolumeSnapshot | Kubernetes request for a point-in-time snapshot of a persistent volume claim. |
| VolumeSnapshotClass | Kubernetes object that defines snapshot behavior and CSI driver settings for VolumeSnapshot resources. |
| VolumeSnapshotLocation | Velero custom resource that defines provider-specific volume snapshot configuration. |
| XR | Composite Resource; an instance of an XRD-defined platform API. |
| XRD | Composite Resource Definition; the Crossplane object that defines a platform API schema. |

[Back to root index](README.md)
