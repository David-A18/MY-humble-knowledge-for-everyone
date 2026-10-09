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
guide gives that context. Unlinked terms have a short definition here and may
not yet have a dedicated explanation.

## Start with common ideas

| If you are learning... | Read these terms |
| --- | --- |
| How changes are saved | [Working tree](git/git-fundamentals.md), [Git index](git/git-fundamentals.md), [Commit](git/git-fundamentals.md), [Branch](git/git-fundamentals.md) |
| How a small program runs | [Source code](programming-languages/programming-fundamentals.md), [Interpreter](programming-languages/programming-fundamentals.md), [Variable](programming-languages/programming-fundamentals.md), [Function](programming-languages/programming-fundamentals.md) |
| How Kubernetes keeps apps running | [Desired state](kubernetes/fundamentals/kubernetes-fundamentals.md), [Current state](kubernetes/fundamentals/kubernetes-fundamentals.md), [Reconciliation](kubernetes/fundamentals/kubernetes-fundamentals.md), [Deployment](kubernetes/fundamentals/kubernetes-fundamentals.md) |
| How infrastructure changes are planned | [Terraform](terraform/fundamentals/terraform-fundamentals.md), [Plan (Terraform)](terraform/fundamentals/terraform-fundamentals.md), [Terraform state](terraform/fundamentals/state-management.md) |
| How AI models produce answers | [Model](ai/ai-fundamentals.md), [Training](ai/ai-fundamentals.md), [Inference](ai/ai-fundamentals.md), [LLM](ai/ai-fundamentals.md) |
| How AI finds knowledge | [RAG](ai/ai-tooling/knowledge-bases/retrieval-and-context-efficiency.md), [Provenance](ai/ai-tooling/knowledge-bases/provenance-trust-and-freshness.md) |
| How AI applications act | [AI agent](ai/ai-fundamentals.md), [Tool (AI agent)](ai/ai-tooling/model-context-protocol.md) |

## All terms

Jump to [A to F](#a-to-f), [G to M](#g-to-m), [N to S](#n-to-s), or
[T to Z](#t-to-z).

### A to F

| Term | Plain meaning |
| --- | --- |
| [ADR](decision-records/index.md) | Architecture Decision Record; a short document that captures context, decision, and consequences. |
| [Agent knowledge base](ai/ai-tooling/knowledge-bases/reference-architecture.md) | An organized collection of pages that a person or AI agent can search, read, cite, and keep up to date with clear source and review information. |
| [AI](ai/ai-fundamentals.md) | Artificial Intelligence; systems that use inputs to produce predictions, recommendations, decisions, or content for a goal. |
| [AI agent](ai/ai-fundamentals.md) | In one common meaning, an application where a model chooses its next steps and tool calls within the tools and permissions it is given. |
| API | Application Programming Interface; a defined way for one program to request information or actions from another. |
| [API gateway](kubernetes/applications-and-tools/apache-apisix.md) | A traffic entry point that routes API requests and can apply configured policies such as authentication or rate limits. |
| API product | Apigee bundle of API resources exposed to developers with access, quota, approval, and credential behavior. |
| [Apigee](cloud/gcloud/apigee.md) | Google Cloud API management platform for API proxies, policies, products, developer apps, analytics, and hybrid API runtime patterns. |
| [APISIX](kubernetes/applications-and-tools/apache-apisix.md) | Apache APISIX; an open-source API gateway whose route and policy configuration can come from its own APIs or a Kubernetes controller. |
| App registration | API management process where a client application is registered and receives credentials for approved API products. |
| [Apply (Terraform)](terraform/fundamentals/terraform-fundamentals.md) | The step that carries out a Terraform plan and records completed changes in state. |
| [Argo CD](kubernetes/applications-and-tools/argo-cd-vs-flux.md) | Kubernetes GitOps controller that reconciles application desired state from Git or another source into target clusters. |
| [Assistant (AI)](ai/ai-fundamentals.md) | An application that presents a model through a conversation interface and may add instructions, information, or tools. |
| [Attested computation](ai/ai-tooling/knowledge-bases/okf-v0.2.md) | In OKF, a concept type describing a specified computation, its inputs, executor, receipt, and evidence check. |
| BackupRepository | Velero repository used by File System Backup or data movement to store volume data in object storage. |
| BackupStorageLocation | Velero custom resource that defines the object storage bucket, prefix, provider, and access mode used for backup artifacts. |
| Blue-green deployment | Release strategy that runs an old production-capable environment and a new production-capable environment at the same time, then moves traffic from the old version to the new version after validation. |
| [Bootstrap](programming-languages/bootstrap-frontend-toolkit.md) | Frontend CSS and JavaScript toolkit for responsive layouts, reusable interface components, and utility classes. |
| [Bootstrapping](programming-languages/bootstrapping-a-system.md) | Initial setup or startup work that prepares enough files, configuration, dependencies, services, or infrastructure for the next layer to run. |
| [Branch](git/git-fundamentals.md) | A movable Git name that points at one commit; it is not a separate copy of your files. |
| BSON | Binary JSON; MongoDB's binary document format for storing documents and typed values. |
| Canary deployment | Release strategy that sends a small percentage of production traffic to a new version first, then increases traffic gradually while monitoring health. |
| Capacity provider | Amazon ECS strategy that controls which infrastructure runs tasks and, for supported capacity types, how that capacity scales. |
| CD | Continuous Delivery means keeping checked software ready for a release decision; Continuous Deployment also releases qualifying changes automatically. |
| CDN | Content Delivery Network; an edge network that caches or accelerates content close to users. |
| [CI](git/github-actions/index.md) | Continuous Integration; integrating changes into a shared codebase frequently and checking each integration with automated validation. |
| CI/CD | The combined practices of Continuous Integration and Continuous Delivery or Deployment. |
| Claude Code | Anthropic coding agent that can use project memory, skills, commands, subagents, permissions, and MCP servers. |
| [Cluster](kubernetes/fundamentals/kubernetes-fundamentals.md) | A Kubernetes control plane and worker nodes that together store desired state and run workloads. |
| [ClusterIP](kubernetes/core-objects/how-a-service-selects-pods.md) | The virtual address inside a Kubernetes cluster assigned to an ordinary Service so clients can reach its eligible Pods. |
| [ClusterProviderConfig](kubernetes/crossplane/providers-and-authentication.md) | Cluster-scoped Crossplane provider configuration that namespaced managed resources can reference across namespaces. |
| Codex | OpenAI coding agent that can use repository instructions, skills, plugins, MCP servers, and connected tools to inspect and change software projects. |
| [Commit](git/git-fundamentals.md) | A saved Git snapshot with a message and links to its parent commits; it remains local until you push it. |
| Composed resource | Kubernetes resource created for one Crossplane composite resource by a Composition, often a provider managed resource. |
| Composite Resource | Crossplane resource instance created from a Composite Resource Definition. |
| Composite resource claim | Legacy Crossplane user-facing request object that creates or binds to a composite resource; namespaced XRs are the default mental model in Crossplane v2 designs. |
| Composite Resource Definition | Crossplane definition that creates a custom platform API schema. |
| Composition | Crossplane implementation that maps a composite resource to composed resources through a function pipeline. |
| Composition Function | Crossplane package that supplies logic used by a Composition or Operation. |
| Composition Revision | Crossplane-generated immutable version of a Composition used for rollout and rollback control. |
| [Condition (programming)](programming-languages/programming-fundamentals.md) | An expression used to choose which instructions run next. |
| [Confabulation (AI)](ai/ai-fundamentals.md) | A generated answer that presents false or made-up information as if it were true. |
| [Configuration (Terraform)](terraform/fundamentals/terraform-fundamentals.md) | The `.tf` files that describe the managed objects and values you want Terraform to use. |
| Configuration Package | Crossplane OCI package that bundles platform APIs, compositions, and package dependencies. |
| Container | A running, isolated process with packaged dependencies; a container image supplies the files used to start it. |
| Container image | A packaged, versioned set of files and metadata used to start a container. |
| [Controller](kubernetes/fundamentals/kubernetes-fundamentals.md) | A program that repeatedly observes a system and acts to move it toward a declared state. |
| [CRD](kubernetes/core-objects/custom-resources-and-crds.md) | CustomResourceDefinition; a Kubernetes object that defines a custom API resource. |
| [Crossplane](kubernetes/crossplane/component-model.md) | Kubernetes-native control-plane framework for reconciling external infrastructure and custom platform APIs. |
| CSI snapshot | Kubernetes snapshot workflow for CSI-backed persistent volumes using VolumeSnapshot, VolumeSnapshotContent, and VolumeSnapshotClass resources. |
| [Current state (observed state)](kubernetes/fundamentals/kubernetes-fundamentals.md) | What is actually present or running in a system, which a controller compares with desired state. |
| Data source (Terraform) | A Terraform request to read information from a provider without managing the object it describes. |
| [Deployment (Kubernetes)](kubernetes/fundamentals/kubernetes-fundamentals.md) | A record of which Pod template to run and how many copies, managed through ReplicaSets. |
| DeploymentRuntimeConfig | Crossplane package-runtime configuration for provider or function pods. |
| [Desired state](kubernetes/fundamentals/kubernetes-fundamentals.md) | The result declared for a system to maintain, such as two copies of an application. |
| [Deterministic extraction](ai/ai-tooling/knowledge-bases/reference-architecture.md) | In this knowledge base's workflow, parsing exact machine-readable facts from authoritative sources with code rather than asking a model to recreate them. |
| DevOps | Engineering practices that connect software delivery, automation, operations, and reliability work. |
| ECR | Amazon Elastic Container Registry; AWS managed registry for container images and OCI-compatible artifacts, including Helm charts. |
| ECS | Amazon Elastic Container Service; AWS-native container orchestration for running, managing, and scaling containerized applications. |
| ECS service | Amazon ECS resource that keeps a desired number of task definition instances running and replaces failed or unhealthy tasks. |
| EKS | Amazon Elastic Kubernetes Service; AWS managed Kubernetes service for running Kubernetes clusters on AWS and supported hybrid environments. |
| Embedding | A numerical representation of content that a retrieval system can compare with other representations. |
| [EndpointSlice](kubernetes/core-objects/how-a-service-selects-pods.md) | A Kubernetes record of backend addresses and readiness conditions for a Service. |
| [EnvironmentConfig](kubernetes/crossplane/compositions.md) | Cluster-scoped Crossplane resource containing reusable data that a Composition function can select for a composite resource's in-memory environment. |
| External name | Crossplane annotation that maps a Kubernetes managed resource to its real external resource identifier. |
| Fargate | AWS serverless container compute option for running ECS tasks or EKS pods without managing servers. |
| [Fetch (Git)](git/git-fundamentals.md) | Download commits and update your local record of remote branches without changing your current branch or working files. |
| File System Backup | Velero volume backup method where node-agent reads mounted pod volumes and stores file data in object storage. |
| [FinOps](finops/cost-allocation-basics.md) | A cloud financial management discipline focused on cost visibility, accountability, and optimization. |
| [Function (programming)](programming-languages/programming-fundamentals.md) | A named block of instructions that runs when called and can return a value. |
| FunctionRevision | Crossplane package revision object for a concrete installed function version. |

### G to M

| Term | Plain meaning |
| --- | --- |
| [Generative AI](ai/ai-fundamentals.md) | AI models that produce new content such as text, images, audio, or video. |
| [Git index](git/git-fundamentals.md) | The staging area: a complete proposed snapshot for the next commit, updated when you stage file contents. |
| [GitOps](kubernetes/applications-and-tools/gitops.md) | An operating model where Git stores desired state and controllers reconcile infrastructure or workloads from that state. |
| [HEAD (Git)](git/git-fundamentals.md) | Git's marker for where you are now; it normally points at your current branch. |
| [Helm](kubernetes/applications-and-tools/helm.md) | Kubernetes package manager that installs versioned charts as tracked releases. |
| [IaC](terraform/fundamentals/terraform-fundamentals.md) | Infrastructure as Code; describing infrastructure in versioned files so changes can be reviewed and repeated. |
| IAM | Identity and Access Management; AWS's system for defining who or what may perform actions on AWS resources. |
| [ID token](security/identity-federation/oidc-fundamentals.md) | A token issued in OpenID Connect that carries identity claims about an authenticated user to a client. |
| [Inference (AI)](ai/ai-fundamentals.md) | Using a trained model on new input to produce a result; one request normally does not retrain it. |
| [Input (programming)](programming-languages/programming-fundamentals.md) | Data given to a running program, such as text typed at a prompt. |
| [Interpreter](programming-languages/programming-fundamentals.md) | A program that reads and runs instructions written in a language such as Python. |
| [IRSA](cloud/aws/security/iam-oidc-provider-and-sts-web-identity.md) | IAM Roles for Service Accounts; an EKS workload-identity pattern using a Kubernetes service-account token and IAM OIDC trust to obtain AWS credentials. |
| JWKS | JSON Web Key Set; a document containing public keys used to verify tokens signed by an identity provider. |
| [JWT](security/identity-federation/oidc-token-validation.md) | JSON Web Token; a compact token format whose claims and signature must be checked for the intended use. |
| [K9s](kubernetes/applications-and-tools/k9s.md) | Terminal UI for navigating, inspecting, and operating Kubernetes clusters through the Kubernetes API. |
| [Kafka](databases/kafka/index.md) | Distributed event streaming platform used for durable event logs, producers, consumers, and stream processing. |
| [kind](kubernetes/applications-and-tools/kind-custom-clusters.md) | Kubernetes in Docker; a local Kubernetes tool that runs cluster nodes as containers. |
| [Knowledge bundle](ai/ai-tooling/knowledge-bases/okf-v0.2.md) | A self-contained directory of Markdown knowledge documents, commonly used as the distribution unit for OKF. |
| Knowledge source of truth | The versioned set of knowledge pages that readers and tools treat as authoritative for this library; it can still cite upstream technical sources. |
| Kopia | Backup tool used by Velero File System Backup and data movement paths to store deduplicated volume data. |
| KRaft | Kafka's Raft-based metadata mode that replaces ZooKeeper for Kafka cluster metadata management. |
| [Kubernetes](kubernetes/fundamentals/kubernetes-fundamentals.md) | A system for running containerized applications across a cluster and reconciling them toward declared state. |
| [Label (Kubernetes)](kubernetes/core-objects/how-a-service-selects-pods.md) | A key-value tag on an object; many objects can share the same label. |
| Least privilege | Granting only the permissions needed to perform a task. |
| [LLM](ai/ai-fundamentals.md) | Large Language Model; a model trained at large scale on language data, commonly used to read input as tokens and produce a response as tokens. |
| Machine-owned region | In this knowledge base's workflow, a page region generated from a structured source and protected from manual changes. |
| Managed Resource | Crossplane provider-defined Kubernetes object that represents an external resource. |
| Managed Resource Activation Policy | Crossplane v2 policy that activates selected managed-resource APIs from a provider. |
| Managed Resource Definition | Crossplane v2 representation of a provider managed-resource API before or while it is activated into a Kubernetes CRD. |
| [MCP](ai/ai-tooling/model-context-protocol.md) | Model Context Protocol; a standard protocol for connecting AI hosts to external tools, resources, and prompt providers. |
| [MCP client](ai/ai-tooling/model-context-protocol.md) | The MCP connection inside an AI host that sends requests to MCP servers and receives their responses. |
| [MCP host](ai/ai-tooling/model-context-protocol.md) | The AI application or environment that the user interacts with, such as an agent app, IDE, or chat product. |
| [MCP server](ai/ai-tooling/model-context-protocol.md) | An integration process or service that exposes tools, resources, and prompts to an MCP host through an MCP client. |
| [ML](ai/ai-fundamentals.md) | Machine Learning; methods that train models from data to make predictions or generate content. |
| MLOps | Operational practices for deploying, monitoring, governing, and maintaining machine learning systems. |
| [Model (AI)](ai/ai-fundamentals.md) | Learned patterns that an AI system uses to make predictions or generate content from new input. |
| [Model parameters (weights)](ai/ai-fundamentals.md) | Values adjusted during training that a model uses during inference; a normal request usually does not change them. |
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
| OCI artifact | A packaged item distributed through a registry using Open Container Initiative conventions, such as a container image or Helm chart. |
| [OIDC](security/identity-federation/oidc-fundamentals.md) | OpenID Connect; identity protocol built on OAuth 2.0 that issues signed identity tokens with claims. |
| [OKF](ai/ai-tooling/knowledge-bases/okf-v0.2.md) | Open Knowledge Format; a Markdown and YAML-frontmatter format for portable human- and agent-readable knowledge bundles with structured metadata. |
| [Operation (Crossplane)](kubernetes/crossplane/component-model.md) | A Crossplane function pipeline for a bounded operational task, separate from continuous resource reconciliation. |
| [Output (programming)](programming-languages/programming-fundamentals.md) | Data a running program produces, such as text printed to a terminal. |
| Pilot (delivery) | Controlled real-world rollout of a more complete solution to a limited audience before wider launch. |
| PKCE | Proof Key for Code Exchange; an OAuth 2.0 extension used with authorization code flows to reduce authorization-code interception risk. |
| [Plan (Terraform)](terraform/fundamentals/terraform-fundamentals.md) | A proposal showing what Terraform would create, change, replace, or destroy; planning does not apply those actions. |
| Platform API | Stable internal API exposed by a platform team to hide implementation details behind a product-like request shape. |
| PoC | Proof of Concept; a small, time-boxed effort used to prove whether an idea, technology, integration, architecture, or approach is feasible. |
| [Pod](kubernetes/fundamentals/kubernetes-fundamentals.md) | The smallest Kubernetes unit that runs one or more containers sharing networking and any volumes declared for them. |
| [Program](programming-languages/programming-fundamentals.md) | Instructions that a computer runs to process input and produce an outcome. |
| Prompt | Input text, and sometimes other content, given to a model for one interaction; a prompt template is saved for repeated use. |
| Prototype | Early model used to explore shape, interaction, behavior, or design before a full implementation. |
| [Provenance](ai/ai-tooling/knowledge-bases/provenance-trust-and-freshness.md) | A record of where a page or claim came from, such as its source document, revision, and the work that produced it. |
| [Provider (Crossplane)](kubernetes/crossplane/providers-and-authentication.md) | Crossplane package that installs managed-resource APIs and controllers for an external system. |
| [Provider (Terraform)](terraform/fundamentals/terraform-fundamentals.md) | Terraform plugin that supplies resource and data-source types and talks to a platform's API. |
| [ProviderConfig (Crossplane)](kubernetes/crossplane/providers-and-authentication.md) | Provider-specific credentials and settings; namespace-scoped for a v2 namespaced managed resource, while legacy provider APIs can use a cluster-scoped ProviderConfig. |
| ProviderRevision | Crossplane package revision object for a concrete installed provider version. |
| Pull request | A request on a Git hosting platform, such as GitHub, to review and merge commits from one branch into another. |
| [Push (Git)](git/git-fundamentals.md) | Send your local commits to a branch in a remote repository so others can fetch them. |
| [RAG](ai/ai-tooling/knowledge-bases/retrieval-and-context-efficiency.md) | Retrieval-Augmented Generation; pattern where relevant source material is retrieved and provided to a model before it answers. |
| RDF | Resource Description Framework; W3C graph data model for representing information as triples, graphs, datasets, and identifiers. |
| [Readiness (Pod)](kubernetes/core-objects/how-a-service-selects-pods.md) | A signal of whether a Pod can normally receive Service traffic; a readiness probe can help determine it. |
| [Reconciliation](kubernetes/fundamentals/kubernetes-fundamentals.md) | A controller repeatedly compares desired state with current state and acts to reduce the difference. |
| [Remote (Git)](git/git-fundamentals.md) | Another Git repository you exchange commits with by fetching or pushing. |
| [Remote-tracking branch](git/git-fundamentals.md) | Your local, possibly stale record of where a branch on a remote stood at your last relevant contact. |
| [ReplicaSet](kubernetes/fundamentals/kubernetes-fundamentals.md) | A Kubernetes object that requests a number of matching Pods; its controller keeps that many running, usually for a Deployment. |
| [Repository (Git)](git/git-fundamentals.md) | A project with Git metadata that records tracked files, commit history, and branches. |
| [Resource (Terraform)](terraform/fundamentals/terraform-fundamentals.md) | One object declared in configuration whose identity Terraform tracks in state. |
| RPO | Recovery Point Objective; acceptable data loss measured in time. |
| RTO | Recovery Time Objective; acceptable time to restore service after an outage. |
| Runbook | A repeatable operational procedure for known tasks or incidents. |
| [Runtime (programming)](programming-languages/programming-fundamentals.md) | The period while a program is running; an error at runtime appears during execution. |
| [Selector (Kubernetes)](kubernetes/core-objects/how-a-service-selects-pods.md) | A rule that chooses objects by matching their labels; a Service selector chooses candidate Pods in its Namespace. |
| [Semantic reranking](ai/ai-tooling/knowledge-bases/retrieval-and-context-efficiency.md) | A retrieval step that reorders candidate results by their likely relevance to a query. |
| [Service (Kubernetes)](kubernetes/core-objects/how-a-service-selects-pods.md) | A Kubernetes object that gives clients a stable name for changing Pods and normally routes to ready ones; the common ClusterIP type adds an in-cluster virtual IP. |
| Service Connect | Amazon ECS capability for service discovery, service-to-service connectivity, and traffic monitoring between ECS services. |
| SHACL | Shapes Constraint Language; W3C language for validating RDF graphs against shapes. |
| [Skill (AI agent)](ai/ai-tooling/create-ai-tools-for-claude-and-codex.md) | Reusable agent workflow package, often centered on `SKILL.md` plus optional references, scripts, and assets. |
| SLA | Service Level Agreement; a commitment about service behavior that may include remedies when it is not met. |
| SLI | Service Level Indicator; a measured aspect of service behavior, such as the fraction of requests that succeed. |
| SLO | Service Level Objective; a reliability target for a service behavior. |
| [SonarQube](devops/code-quality/sonarqube.md) | Code quality and security analysis platform that uses scanners, quality profiles, quality gates, and pull request analysis to report code issues. |
| [Source code](programming-languages/programming-fundamentals.md) | The human-readable instructions written in a programming language. |
| Spike | Short investigation used to learn enough to estimate, design, or make a technical decision. |

### T to Z

| Term | Plain meaning |
| --- | --- |
| Tagging strategy | A consistent scheme for metadata used in ownership, cost allocation, automation, and governance. |
| Task definition | Amazon ECS versioned blueprint that describes container images, CPU, memory, networking, IAM roles, logging, secrets, and volumes for a task. |
| Task role | IAM role associated with an ECS task that grants application containers permission to call AWS APIs. |
| [Terraform](terraform/fundamentals/terraform-fundamentals.md) | An Infrastructure as Code tool that uses state to find managed objects, compares their current condition with configuration, and can apply approved changes. |
| [Terraform state](terraform/fundamentals/state-management.md) | A record mapping resource addresses to managed object identities and attributes; it may contain secrets. |
| [Token (AI)](ai/ai-fundamentals.md) | A small piece of text, or other encoded content, that a language model reads or produces. |
| [Tool (AI agent)](ai/ai-tooling/model-context-protocol.md) | A callable capability exposed to an AI model or agent so it can query data, perform computation, or take an action. |
| [Tooling cluster](kubernetes/applications-and-tools/tooling-clusters.md) | A Kubernetes cluster chosen to host shared platform services; target clusters still keep their own control planes and local requirements. |
| [Training (AI)](ai/ai-fundamentals.md) | A process that uses data to build or adjust a model before it is used on new input. |
| [Usage (Crossplane)](kubernetes/crossplane/managed-resources-and-lifecycle.md) | Crossplane resource that protects a depended-on resource from deletion or controls deletion ordering. |
| [Variable (programming)](programming-languages/programming-fundamentals.md) | A name used to refer to a value while a program runs. |
| Vector store | A search system that stores numerical representations of content with identifiers and metadata for similarity retrieval; this knowledge base treats its indexes as rebuildable. |
| [Velero](migrations/velero/fundamentals.md) | Kubernetes backup and restore tool that stores backed-up resource definitions in object storage and can also protect selected volume data. |
| VolumeSnapshot | Kubernetes request for a point-in-time snapshot of a persistent volume claim. |
| VolumeSnapshotClass | Kubernetes object that defines snapshot behavior and CSI driver settings for VolumeSnapshot resources. |
| VolumeSnapshotLocation | Velero custom resource that defines provider-specific volume snapshot configuration. |
| [Workflow (AI)](ai/ai-fundamentals.md) | An application path where code decides the steps and when a model or tool is called. |
| [Working tree](git/git-fundamentals.md) | The files in your checked-out Git project that you can read and edit. |
| XR | See Composite Resource: an instance of an XRD-defined platform API. |
| XRD | See Composite Resource Definition: the Crossplane object that defines a platform API schema. |

[Back to knowledge index](index.md)
