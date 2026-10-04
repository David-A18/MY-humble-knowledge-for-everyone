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
| How changes are saved | [Working tree](git/git-fundamentals.md), [Git index](git/git-fundamentals.md), [Commit](git/git-fundamentals.md), [Branch](git/git-fundamentals.md) |
| How platforms keep things running | [Reconciliation](kubernetes/fundamentals/kubernetes-fundamentals.md), [GitOps](kubernetes/applications-and-tools/gitops.md), [Terraform state](terraform/fundamentals/state-management.md) |
| How AI finds knowledge | [AI agent](ai/ai-tooling/index.md), [RAG](ai/ai-tooling/knowledge-bases/retrieval-and-context-efficiency.md), [Provenance](ai/ai-tooling/knowledge-bases/provenance-trust-and-freshness.md) |

## All terms

Jump to [A to F](#a-to-f), [G to M](#g-to-m), [N to S](#n-to-s), or
[T to Z](#t-to-z).

### A to F

| Term | Plain meaning |
| --- | --- |
| [ADR](decision-records/index.md) | Architecture Decision Record; a short document that captures context, decision, and consequences. |
| Agent knowledge base | An organized collection of pages that a person or AI agent can search, read, cite, and keep up to date with clear source and review information. |
| [AI](ai/index.md) | Artificial Intelligence; systems or workflows that perform tasks associated with reasoning, generation, prediction, or automation. |
| [AI agent](ai/ai-tooling/index.md) | An AI system that can follow goals, use tools, inspect context, and take multi-step actions with feedback. |
| API | Application Programming Interface; a defined way for one program to request information or actions from another. |
| [API gateway](kubernetes/applications-and-tools/apache-apisix.md) | A traffic entry point that routes API requests and can apply configured policies such as authentication or rate limits. |
| API product | Apigee bundle of API resources exposed to developers with access, quota, approval, and credential behavior. |
| [Apigee](cloud/gcloud/apigee.md) | Google Cloud API management platform for API proxies, policies, products, developer apps, analytics, and hybrid API runtime patterns. |
| [APISIX](kubernetes/applications-and-tools/apache-apisix.md) | Apache APISIX; an open-source API gateway whose route and policy configuration can come from its own APIs or a Kubernetes controller. |
| App registration | API management process where a client application is registered and receives credentials for approved API products. |
| [Argo CD](kubernetes/applications-and-tools/argo-cd-vs-flux.md) | Kubernetes GitOps controller that reconciles application desired state from Git or another source into target clusters. |
| [Attested computation](ai/ai-tooling/knowledge-bases/okf-v0.2.md) | In OKF, a concept type describing a specified computation, its inputs, executor, receipt, and evidence check. |
| BackupRepository | Velero repository used by File System Backup or data movement to store volume data in object storage. |
| BackupStorageLocation | Velero custom resource that defines the object storage bucket, prefix, provider, and access mode used for backup artifacts. |
| Blue-green deployment | Release strategy that runs an old production-capable environment and a new production-capable environment at the same time, then moves traffic from the old version to the new version after validation. |
| [Bootstrap](programming-languages/bootstrap-frontend-toolkit.md) | Frontend CSS and JavaScript toolkit for responsive layouts, reusable interface components, and utility classes. |
| [Bootstrapping](programming-languages/bootstrapping-a-system.md) | Initial setup or startup work that prepares enough files, configuration, dependencies, services, or infrastructure for the next layer to run. |
| [Branch](git/git-fundamentals.md) | A movable Git name for a line of commits; it points to the latest commit on that line. |
| BSON | Binary JSON; MongoDB's binary document format for storing documents and typed values. |
| Canary deployment | Release strategy that sends a small percentage of production traffic to a new version first, then increases traffic gradually while monitoring health. |
| Capacity provider | Amazon ECS strategy that controls which infrastructure runs tasks and, for supported capacity types, how that capacity scales. |
| CD | Continuous Delivery means keeping checked software ready for a release decision; Continuous Deployment also releases qualifying changes automatically. |
| CDN | Content Delivery Network; an edge network that caches or accelerates content close to users. |
| [CI](git/github-actions/index.md) | Continuous Integration; integrating changes into a shared codebase frequently and checking each integration with automated validation. |
| CI/CD | The combined practices of Continuous Integration and Continuous Delivery or Deployment. |
| Claude Code | Anthropic coding agent that can use project memory, skills, commands, subagents, permissions, and MCP servers. |
| [Cluster](kubernetes/fundamentals/kubernetes-fundamentals.md) | A Kubernetes control plane and worker nodes that together store desired state and run workloads. |
| [ClusterProviderConfig](kubernetes/crossplane/providers-and-authentication.md) | Cluster-scoped Crossplane provider configuration that namespaced managed resources can reference across namespaces. |
| Codex | OpenAI coding agent that can use repository instructions, skills, plugins, MCP servers, and connected tools to inspect and change software projects. |
| [Commit](git/git-fundamentals.md) | A saved Git snapshot with a message and links to its parent commit or commits. |
| Container | A running, isolated process with packaged dependencies; a container image supplies the files used to start it. |
| Container image | A packaged, versioned set of files and metadata used to start a container. |
| Composed resource | Kubernetes resource created for one Crossplane composite resource by a Composition, often a provider managed resource. |
| Composite Resource | Crossplane resource instance created from a Composite Resource Definition. |
| Composite resource claim | Legacy Crossplane user-facing request object that creates or binds to a composite resource; namespaced XRs are the default mental model in Crossplane v2 designs. |
| Composite Resource Definition | Crossplane definition that creates a custom platform API schema. |
| Composition | Crossplane implementation that maps a composite resource to composed resources through a function pipeline. |
| Composition Function | Crossplane package that supplies logic used by a Composition or Operation. |
| Composition Revision | Crossplane-generated immutable version of a Composition used for rollout and rollback control. |
| Configuration Package | Crossplane OCI package that bundles platform APIs, compositions, and package dependencies. |
| [Controller](kubernetes/fundamentals/kubernetes-fundamentals.md) | A program that repeatedly observes a system and acts to move it toward a declared state. |
| [CRD](kubernetes/core-objects/custom-resources-and-crds.md) | CustomResourceDefinition; a Kubernetes object that defines a custom API resource. |
| [Crossplane](kubernetes/crossplane/component-model.md) | Kubernetes-native control-plane framework for reconciling external infrastructure and custom platform APIs. |
| CSI snapshot | Kubernetes snapshot workflow for CSI-backed persistent volumes using VolumeSnapshot, VolumeSnapshotContent, and VolumeSnapshotClass resources. |
| DeploymentRuntimeConfig | Crossplane package-runtime configuration for provider or function pods. |
| [Desired state](kubernetes/fundamentals/kubernetes-fundamentals.md) | The result declared for a system to maintain, such as two copies of an application. |
| [Deterministic extraction](ai/ai-tooling/knowledge-bases/reference-architecture.md) | In this knowledge base's workflow, parsing exact machine-readable facts from authoritative sources with code rather than asking a model to recreate them. |
| DevOps | Engineering practices that connect software delivery, automation, operations, and reliability work. |
| ECR | Amazon Elastic Container Registry; AWS managed registry for container images and OCI-compatible artifacts, including Helm charts. |
| ECS | Amazon Elastic Container Service; AWS-native container orchestration for running, managing, and scaling containerized applications. |
| ECS service | Amazon ECS resource that keeps a desired number of task definition instances running and replaces failed or unhealthy tasks. |
| EKS | Amazon Elastic Kubernetes Service; AWS managed Kubernetes service for running Kubernetes clusters on AWS and supported hybrid environments. |
| Embedding | A numerical representation of content that a retrieval system can compare with other representations. |
| [EnvironmentConfig](kubernetes/crossplane/compositions.md) | Cluster-scoped Crossplane resource containing reusable data that a Composition function can select for a composite resource's in-memory environment. |
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
| [Helm](kubernetes/applications-and-tools/helm.md) | Kubernetes package manager that installs versioned charts as tracked releases. |
| [ID token](security/identity-federation/oidc-fundamentals.md) | A token issued in OpenID Connect that carries identity claims about an authenticated user to a client. |
| [IaC](terraform/fundamentals/terraform-fundamentals.md) | Infrastructure as Code; managing infrastructure through versioned declarative or procedural definitions. |
| IAM | Identity and Access Management; AWS's system for defining who or what may perform actions on AWS resources. |
| [IRSA](cloud/aws/security/iam-oidc-provider-and-sts-web-identity.md) | IAM Roles for Service Accounts; an EKS workload-identity pattern using a Kubernetes service-account token and IAM OIDC trust to obtain AWS credentials. |
| JWKS | JSON Web Key Set; a document containing public keys used to verify tokens signed by an identity provider. |
| [JWT](security/identity-federation/oidc-token-validation.md) | JSON Web Token; a compact token format whose claims and signature must be checked for the intended use. |
| [K9s](kubernetes/applications-and-tools/k9s.md) | Terminal UI for navigating, inspecting, and operating Kubernetes clusters through the Kubernetes API. |
| [Kafka](databases/kafka/index.md) | Distributed event streaming platform used for durable event logs, producers, consumers, and stream processing. |
| [kind](kubernetes/applications-and-tools/kind-custom-clusters.md) | Kubernetes in Docker; a local Kubernetes tool that runs cluster nodes as containers. |
| Knowledge bundle | A self-contained directory of Markdown knowledge documents, commonly used as the distribution unit for OKF. |
| Knowledge source of truth | The versioned set of knowledge pages that readers and tools treat as authoritative for this library; it can still cite upstream technical sources. |
| [Kubernetes](kubernetes/fundamentals/kubernetes-fundamentals.md) | A system for running containerized applications across a cluster and reconciling them toward declared state. |
| Kopia | Backup tool used by Velero File System Backup and data movement paths to store deduplicated volume data. |
| KRaft | Kafka's Raft-based metadata mode that replaces ZooKeeper for Kafka cluster metadata management. |
| Least privilege | Granting only the permissions needed to perform a task. |
| LLM | Large Language Model; a model trained to process and generate language and other structured content. |
| Machine-owned region | In this knowledge base's workflow, a page region generated from a structured source and protected from manual changes. |
| Managed Resource | Crossplane provider-defined Kubernetes object that represents an external resource. |
| Managed Resource Activation Policy | Crossplane v2 policy that activates selected managed-resource APIs from a provider. |
| Managed Resource Definition | Crossplane v2 representation of a provider managed-resource API before or while it is activated into a Kubernetes CRD. |
| [MCP](ai/ai-tooling/model-context-protocol.md) | Model Context Protocol; a standard protocol for connecting AI hosts to external tools, resources, and prompt providers. |
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
| [Namespace](kubernetes/fundamentals/kubernetes-fundamentals.md) | A named scope inside a Kubernetes cluster that helps organize namespaced objects. |
| [Node](kubernetes/fundamentals/kubernetes-fundamentals.md) | A worker machine in a Kubernetes cluster that runs Pods. |
| Node-agent | Velero DaemonSet that runs file-system backup and data movement work on Kubernetes nodes. |
| OAuth 2.0 | An authorization framework in which a client obtains a scoped access token to call a resource server. |
| Object storage | Storage that keeps data as named objects in buckets rather than as a mounted file system. |
| [Observed state](kubernetes/fundamentals/kubernetes-fundamentals.md) | What a controller currently sees in the system, which it compares with desired state. |
| OCI artifact | A packaged item distributed through a registry using Open Container Initiative conventions, such as a container image or Helm chart. |
| [OIDC](security/identity-federation/oidc-fundamentals.md) | OpenID Connect; identity protocol built on OAuth 2.0 that issues signed identity tokens with claims. |
| [OKF](ai/ai-tooling/knowledge-bases/okf-v0.2.md) | Open Knowledge Format; a Markdown and YAML-frontmatter format for portable human- and agent-readable knowledge bundles with structured metadata. |
| [Operation (Crossplane)](kubernetes/crossplane/component-model.md) | A Crossplane function pipeline for a bounded operational task, separate from continuous resource reconciliation. |
| Pilot (delivery) | Controlled real-world rollout of a more complete solution to a limited audience before wider launch. |
| PKCE | Proof Key for Code Exchange; an OAuth 2.0 extension used with authorization code flows to reduce authorization-code interception risk. |
| Platform API | Stable internal API exposed by a platform team to hide implementation details behind a product-like request shape. |
| [Pod](kubernetes/fundamentals/kubernetes-fundamentals.md) | The smallest Kubernetes unit that runs one or more containers sharing networking and storage. |
| PoC | Proof of Concept; a small, time-boxed effort used to prove whether an idea, technology, integration, architecture, or approach is feasible. |
| Prompt | Input text, and sometimes other content, given to a model for one interaction; a prompt template is saved for repeated use. |
| Prototype | Early model used to explore shape, interaction, behavior, or design before a full implementation. |
| Provenance | A record of where a page or claim came from, such as its source document, revision, and the work that produced it. |
| [Provider (Crossplane)](kubernetes/crossplane/providers-and-authentication.md) | Crossplane package that installs managed-resource APIs and controllers for an external system. |
| [Provider (Terraform)](terraform/fundamentals/terraform-fundamentals.md) | Terraform plugin that supplies resource and data-source types and talks to an external API. |
| [ProviderConfig (Crossplane)](kubernetes/crossplane/providers-and-authentication.md) | Provider-specific credentials and settings; namespace-scoped for a v2 namespaced managed resource, while legacy provider APIs can use a cluster-scoped ProviderConfig. |
| ProviderRevision | Crossplane package revision object for a concrete installed provider version. |
| [Pull request](git/git-fundamentals.md) | A proposed set of Git changes submitted for review before merging into a target branch. |
| [RAG](ai/ai-tooling/knowledge-bases/retrieval-and-context-efficiency.md) | Retrieval-Augmented Generation; pattern where relevant source material is retrieved and provided to a model before it answers. |
| RDF | Resource Description Framework; W3C graph data model for representing information as triples, graphs, datasets, and identifiers. |
| [Reconciliation](kubernetes/fundamentals/kubernetes-fundamentals.md) | A control loop that compares desired state with observed state and acts to reduce the difference. |
| Repository | A Git project containing files, commit history, and branches. |
| RPO | Recovery Point Objective; acceptable data loss measured in time. |
| RTO | Recovery Time Objective; acceptable time to restore service after an outage. |
| Runbook | A repeatable operational procedure for known tasks or incidents. |
| [Semantic reranking](ai/ai-tooling/knowledge-bases/retrieval-and-context-efficiency.md) | A retrieval step that reorders candidate results by their likely relevance to a query. |
| [Service](kubernetes/fundamentals/kubernetes-fundamentals.md) | A Kubernetes object that gives a changing set of selected Pods a stable network name and, for the common ClusterIP type, a virtual IP. |
| Service Connect | Amazon ECS capability for service discovery, service-to-service connectivity, and traffic monitoring between ECS services. |
| SHACL | Shapes Constraint Language; W3C language for validating RDF graphs against shapes. |
| Skill (AI agent) | Reusable agent workflow package, often centered on `SKILL.md` plus optional references, scripts, and assets. |
| SLA | Service Level Agreement; a commitment about service behavior that may include remedies when it is not met. |
| SLI | Service Level Indicator; a measured aspect of service behavior, such as the fraction of requests that succeed. |
| SLO | Service Level Objective; a reliability target for a service behavior. |
| [SonarQube](devops/code-quality/sonarqube.md) | Code quality and security analysis platform that uses scanners, quality profiles, quality gates, and pull request analysis to report code issues. |
| Spike | Short investigation used to learn enough to estimate, design, or make a technical decision. |

### T to Z

| Term | Plain meaning |
| --- | --- |
| Tagging strategy | A consistent scheme for metadata used in ownership, cost allocation, automation, and governance. |
| Task definition | Amazon ECS versioned blueprint that describes container images, CPU, memory, networking, IAM roles, logging, secrets, and volumes for a task. |
| Task role | IAM role associated with an ECS task that grants application containers permission to call AWS APIs. |
| [Terraform](terraform/fundamentals/terraform-fundamentals.md) | An Infrastructure as Code tool that compares configuration with state and plans changes to managed resources. |
| [Terraform state](terraform/fundamentals/state-management.md) | Terraform’s record of the real objects it manages and their association with configuration. |
| Tool (AI agent) | A callable capability exposed to an AI model or agent so it can query data, perform computation, or take an action. |
| [Tooling cluster](kubernetes/applications-and-tools/tooling-clusters.md) | A Kubernetes cluster chosen to host shared platform services; target clusters still keep their own control planes and local requirements. |
| [Usage (Crossplane)](kubernetes/crossplane/managed-resources-and-lifecycle.md) | Crossplane resource that protects a depended-on resource from deletion or controls deletion ordering. |
| Vector store | A search system that stores numerical representations of content with identifiers and metadata for similarity retrieval; this knowledge base treats its indexes as rebuildable. |
| [Velero](migrations/velero/fundamentals.md) | Kubernetes backup and restore tool that stores backed-up resource definitions in object storage and can also protect selected volume data. |
| VolumeSnapshot | Kubernetes request for a point-in-time snapshot of a persistent volume claim. |
| VolumeSnapshotClass | Kubernetes object that defines snapshot behavior and CSI driver settings for VolumeSnapshot resources. |
| VolumeSnapshotLocation | Velero custom resource that defines provider-specific volume snapshot configuration. |
| [Working tree](git/git-fundamentals.md) | The files in your checked-out Git project that you can read and edit. |
| XR | See Composite Resource: an instance of an XRD-defined platform API. |
| XRD | See Composite Resource Definition: the Crossplane object that defines a platform API schema. |

[Back to knowledge index](index.md)
