---
type: "Glossary"
title: "Glossary"
description: "Find short definitions of knowledge-base terms and follow linked concepts for examples and official sources."
tags: [glossary]
status: draft
maturity: draft
audience: "Engineering learners and practitioners"
maintainer: "unassigned"
---

# Glossary

Use this page when a word in a guide is unfamiliar. Read its short definition,
then open the linked explanation when you need an example or an official
source. A term may be more specific in one product or workflow; the linked
guide gives that context. Linked terms have a deeper route; unlinked terms
currently have only a short definition here.

## Start with common ideas

| If you are learning... | Read these terms |
| --- | --- |
| How changes are saved | [Working tree](#t-to-z), [Git index](#g-to-m), [Commit](#a-to-f), [Branch](#a-to-f) |
| How platforms keep things running | [Reconciliation](#n-to-s), [GitOps](#g-to-m), [Terraform state](#t-to-z) |
| How AI finds knowledge | [AI agent](#a-to-f), [RAG](#n-to-s), [Provenance](#n-to-s) |

## All terms

Jump to [A to F](#a-to-f), [G to M](#g-to-m), [N to S](#n-to-s), or
[T to Z](#t-to-z).

### A to F

| Term | Plain meaning |
| --- | --- |
| ADR | Architecture Decision Record; a short document that captures context, decision, and consequences. |
| Agent knowledge base | An organized collection of pages that a person or AI agent can search, read, cite, and keep up to date with clear source and review information. |
| [AI](ai/index.md) | Artificial Intelligence; systems or workflows that perform tasks associated with reasoning, generation, prediction, or automation. |
| [AI agent](ai/ai-tooling/index.md) | An AI system that can follow goals, use tools, inspect context, and take multi-step actions with feedback. |
| API gateway | A traffic entry point that routes API requests and often applies policy such as authentication, rate limits, TLS, and observability. |
| API product | Apigee bundle of API resources exposed to developers with access, quota, approval, and credential behavior. |
| Apigee | Google Cloud API management platform for API proxies, policies, products, developer apps, analytics, and hybrid API runtime patterns. |
| APISIX | Apache APISIX; an open-source API gateway that can run in Kubernetes and be configured through APISIX APIs, CRDs, or Gateway API integrations. |
| App registration | API management process where a client application is registered and receives credentials for approved API products. |
| Argo CD | Kubernetes GitOps controller that reconciles application desired state from Git or another source into target clusters. |
| Attested computation | OKF concept type that describes a sanctioned computation, its runtime, parameters, executor, receipt, and deterministic attester. |
| BackupRepository | Velero repository used by File System Backup or data movement to store volume data in object storage. |
| BackupStorageLocation | Velero custom resource that defines the object storage bucket, prefix, provider, and access mode used for backup artifacts. |
| Blue-green deployment | Release strategy that runs an old production-capable environment and a new production-capable environment at the same time, then moves traffic from the old version to the new version after validation. |
| [Bootstrap](programming-languages/bootstrap-frontend-toolkit.md) | Frontend CSS and JavaScript toolkit for responsive layouts, reusable interface components, and utility classes. |
| [Bootstrapping](programming-languages/bootstrapping-a-system.md) | Initial setup or startup work that prepares enough files, configuration, dependencies, services, or infrastructure for the next layer to run. |
| [Branch](git/git-fundamentals.md) | A movable Git name for a line of commits; it points to the latest commit on that line. |
| BSON | Binary JSON; MongoDB's binary document format for storing documents and typed values. |
| Canary deployment | Release strategy that sends a small percentage of production traffic to a new version first, then increases traffic gradually while monitoring health. |
| Capacity provider | Amazon ECS strategy that controls which infrastructure runs tasks and, for supported capacity types, how that capacity scales. |
| CD | Continuous Delivery or Continuous Deployment, depending on release process. |
| CDN | Content Delivery Network; an edge network that caches or accelerates content close to users. |
| [CI](git/github-actions/index.md) | Continuous Integration; automated validation that runs on code changes. |
| CI/CD | Continuous Integration plus Continuous Delivery or Deployment; automation that checks changes and prepares or releases them. Delivery keeps a human release decision; deployment can release automatically. |
| Claude Code | Anthropic coding agent that can use project memory, skills, commands, subagents, permissions, and MCP servers. |
| ClusterProviderConfig | Crossplane provider configuration that can be referenced across namespaces. |
| Codex | OpenAI coding agent that can use repository instructions, skills, plugins, MCP servers, and connected tools to inspect and change software projects. |
| [Commit](git/git-fundamentals.md) | A saved Git snapshot with a message and links to its parent commit or commits. |
| Composed resource | Kubernetes resource created for one Crossplane composite resource by a Composition, often a provider managed resource. |
| Composite Resource | Crossplane resource instance created from a Composite Resource Definition. |
| Composite resource claim | Legacy Crossplane user-facing request object that creates or binds to a composite resource; namespaced XRs are the default mental model in Crossplane v2 designs. |
| Composite Resource Definition | Crossplane definition that creates a custom platform API schema. |
| Composition | Crossplane implementation that maps a composite resource to composed resources through a function pipeline. |
| Composition Function | Crossplane package that supplies logic used by a Composition or Operation. |
| Composition Revision | Crossplane-generated immutable version of a Composition used for rollout and rollback control. |
| Configuration Package | Crossplane OCI package that bundles platform APIs, compositions, and package dependencies. |
| [CRD](kubernetes/core-objects/custom-resources-and-crds.md) | CustomResourceDefinition; a Kubernetes object that defines a custom API resource. |
| [Crossplane](kubernetes/crossplane/component-model.md) | Kubernetes-native control-plane framework for reconciling external infrastructure and custom platform APIs. |
| CSI snapshot | Kubernetes snapshot workflow for CSI-backed persistent volumes using VolumeSnapshot, VolumeSnapshotContent, and VolumeSnapshotClass resources. |
| DeploymentRuntimeConfig | Crossplane package-runtime configuration for provider or function pods. |
| Deterministic extraction | Parsing exact machine-readable facts from authoritative producers with code rather than asking a model to recreate them. |
| DevOps | Engineering practices that connect software delivery, automation, operations, and reliability work. |
| ECR | Amazon Elastic Container Registry; AWS managed registry for container images and OCI-compatible artifacts, including Helm charts. |
| ECS | Amazon Elastic Container Service; AWS-native container orchestration for running, managing, and scaling containerized applications. |
| ECS service | Amazon ECS resource that keeps a desired number of task definition instances running and replaces failed or unhealthy tasks. |
| EKS | Amazon Elastic Kubernetes Service; AWS managed Kubernetes service for running Kubernetes clusters on AWS and supported hybrid environments. |
| EnvironmentConfig | Crossplane composition data object that provides XR-specific in-memory environment values. |
| External name | Crossplane annotation that maps a Kubernetes managed resource to its real external resource identifier. |
| Fargate | AWS serverless container compute option for running ECS tasks or EKS pods without managing servers. |
| File System Backup | Velero volume backup method where node-agent reads mounted pod volumes and stores file data in object storage. |
| [FinOps](finops/cost-allocation-basics.md) | A cloud financial management discipline focused on cost visibility, accountability, and optimization. |
| FunctionRevision | Crossplane package revision object for a concrete installed function version. |

### G to M

| Term | Plain meaning |
| --- | --- |
| [Git index](git/git-fundamentals.md) | The staging area where Git records what the next commit should contain. |
| [GitOps](kubernetes/applications-and-tools/gitops.md) | An operating model where Git stores desired state and controllers reconcile infrastructure or workloads from that state. |
| Helm | Kubernetes package manager that installs versioned charts as tracked releases. |
| [IaC](terraform/fundamentals/terraform-fundamentals.md) | Infrastructure as Code; managing infrastructure through versioned declarative or procedural definitions. |
| IRSA | IAM Roles for Service Accounts; an EKS pattern that uses Kubernetes service account tokens and IAM OIDC trust to provide AWS credentials. |
| JWKS | JSON Web Key Set; a document containing public keys used to verify tokens signed by an identity provider. |
| K9s | Terminal UI for navigating, inspecting, and operating Kubernetes clusters through the Kubernetes API. |
| [Kafka](databases/kafka/index.md) | Distributed event streaming platform used for durable event logs, producers, consumers, and stream processing. |
| kind | Kubernetes in Docker; a local Kubernetes tool that runs cluster nodes as containers. |
| Knowledge bundle | A self-contained directory of Markdown knowledge documents, commonly used as the distribution unit for OKF. |
| Knowledge source of truth | The versioned set of knowledge pages that readers and tools treat as authoritative for this library; it can still cite upstream technical sources. |
| Kopia | Backup tool used by Velero File System Backup and data movement paths to store deduplicated volume data. |
| KRaft | Kafka's Raft-based metadata mode that replaces ZooKeeper for Kafka cluster metadata management. |
| Least privilege | Granting only the permissions needed to perform a task. |
| LLM | Large Language Model; a model trained to process and generate language and other structured content. |
| Machine-owned region | Documentation region generated from deterministic source data and protected from model-authored claims or manual drift. |
| Managed Resource | Crossplane provider-defined Kubernetes object that represents an external resource. |
| Managed Resource Activation Policy | Crossplane v2 policy that activates selected managed-resource APIs from a provider. |
| Managed Resource Definition | Crossplane v2 representation of a provider managed-resource API before or while it is activated into a Kubernetes CRD. |
| [MCP](ai/ai-tooling/index.md) | Model Context Protocol; a standard protocol for connecting AI hosts to external tools, resources, and prompt providers. |
| MCP client | The MCP connection inside an AI host that sends requests to MCP servers and receives their responses. |
| MCP host | The AI application or environment that the user interacts with, such as an agent app, IDE, or chat product. |
| MCP server | An integration process or service that exposes tools, resources, and prompts to an MCP host through an MCP client. |
| ML | Machine Learning; systems that learn patterns from data to make predictions, classifications, or decisions. |
| MLOps | Operational practices for deploying, monitoring, governing, and maintaining machine learning systems. |
| [MongoDB](databases/mongodb/index.md) | Document database that stores JSON-like BSON documents and supports flexible document modeling. |
| MSK | Amazon Managed Streaming for Apache Kafka; AWS managed service for Kafka-compatible streaming workloads. |
| MTTR | Mean Time To Recovery; a reliability metric for how quickly service is restored after failure. |
| MVP | Minimum Viable Product; the smallest useful product version that can deliver value to real users and support learning from real usage. |

### N to S

| Term | Plain meaning |
| --- | --- |
| Node-agent | Velero DaemonSet that runs file-system backup and data movement work on Kubernetes nodes. |
| [OIDC](security/identity-federation/oidc-fundamentals.md) | OpenID Connect; identity protocol built on OAuth 2.0 that issues signed identity tokens with claims. |
| OKF | Open Knowledge Format; an open Markdown and YAML-frontmatter specification for portable human- and agent-readable knowledge bundles with structured metadata. |
| Operation | Crossplane run-to-completion function pipeline for maintenance or operational tasks. |
| Pilot | Controlled real-world rollout of a more complete solution to a limited audience before wider launch. |
| PKCE | Proof Key for Code Exchange; an OAuth 2.0 extension used with authorization code flows to reduce authorization-code interception risk. |
| Platform API | Stable internal API exposed by a platform team to hide implementation details behind a product-like request shape. |
| PoC | Proof of Concept; a small, time-boxed effort used to prove whether an idea, technology, integration, architecture, or approach is feasible. |
| Prompt | Reusable instruction template that guides a model or agent for a specific interaction or workflow. |
| Prototype | Early model used to explore shape, interaction, behavior, or design before a full implementation. |
| Provenance | A record of where a page or claim came from, such as its source document, revision, and the work that produced it. |
| Provider | Crossplane OCI package that installs managed-resource APIs and controllers for an external system. |
| ProviderConfig | Crossplane provider configuration scoped to a namespace. |
| ProviderRevision | Crossplane package revision object for a concrete installed provider version. |
| [RAG](ai/ai-tooling/knowledge-bases/retrieval-and-context-efficiency.md) | Retrieval-Augmented Generation; pattern where relevant source material is retrieved and provided to a model before it answers. |
| RDF | Resource Description Framework; W3C graph data model for representing information as triples, graphs, datasets, and identifiers. |
| [Reconciliation](kubernetes/fundamentals/kubernetes-fundamentals.md) | A control loop that compares desired state with observed state and acts to reduce the difference. |
| RPO | Recovery Point Objective; acceptable data loss measured in time. |
| RTO | Recovery Time Objective; acceptable time to restore service after an outage. |
| Runbook | A repeatable operational procedure for known tasks or incidents. |
| Semantic reranking | Retrieval step that reorders lexical or candidate results by semantic similarity when measured vocabulary mismatch justifies the extra cost. |
| Service Connect | Amazon ECS capability for service discovery, service-to-service connectivity, and traffic monitoring between ECS services. |
| SHACL | Shapes Constraint Language; W3C language for validating RDF graphs against shapes. |
| Skill | Reusable AI workflow package, usually centered on `SKILL.md` plus optional references, scripts, and assets. |
| SLO | Service Level Objective; a reliability target for a service behavior. |
| [SonarQube](devops/code-quality/sonarqube.md) | Code quality and security analysis platform that uses scanners, quality profiles, quality gates, and pull request analysis to report code issues. |
| Spike | Short investigation used to learn enough to estimate, design, or make a technical decision. |

### T to Z

| Term | Plain meaning |
| --- | --- |
| Tagging strategy | A consistent scheme for metadata used in ownership, cost allocation, automation, and governance. |
| Task definition | Amazon ECS versioned blueprint that describes container images, CPU, memory, networking, IAM roles, logging, secrets, and volumes for a task. |
| Task role | IAM role associated with an ECS task that grants application containers permission to call AWS APIs. |
| [Terraform state](terraform/fundamentals/state-management.md) | Terraform’s record of the real objects it manages and their association with configuration. |
| Tool | A callable capability exposed to an AI model or agent so it can query data, perform computation, or take an action. |
| Tooling cluster | Kubernetes cluster dedicated to platform tools such as GitOps, observability, policy, CI/CD runners, or developer experience services. |
| Usage | Crossplane resource that protects a depended-on resource from deletion or controls deletion ordering. |
| Vector store | Disposable search index that stores embeddings and metadata so retrieval can find semantically similar documents or chunks. |
| Velero | Kubernetes backup, restore, disaster recovery, and cluster migration tool that stores cluster resources in object storage and can protect persistent volume data. |
| VolumeSnapshot | Kubernetes request for a point-in-time snapshot of a persistent volume claim. |
| VolumeSnapshotClass | Kubernetes object that defines snapshot behavior and CSI driver settings for VolumeSnapshot resources. |
| VolumeSnapshotLocation | Velero custom resource that defines provider-specific volume snapshot configuration. |
| [Working tree](git/git-fundamentals.md) | The files in your checked-out Git project that you can read and edit. |
| XR | Composite Resource; an instance of an XRD-defined platform API. |
| XRD | Composite Resource Definition; the Crossplane object that defines a platform API schema. |

[Back to knowledge index](index.md)
