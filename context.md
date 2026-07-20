# AI agent context

This file is the operating map for AI agents working in `engineering-knowledge-base`. Use it before editing so routes, indexes, templates, and repository conventions stay connected.

> [!IMPORTANT]
> Keep this file updated whenever files, directories, templates, workflows, or navigation rules change.
>
> Start with [AGENTS.md](AGENTS.md) when an AI agent needs an explicit routing and deployment workflow.
>
> Read [instructions.md](instructions.md) before creating or refactoring documentation. It defines the standard page structure, table style, example placement, risk notes, and validation expectations for AI agents.

## Repository intent

`engineering-knowledge-base` is a long-term personal knowledge base for practical engineering knowledge across cloud, databases, Git, GitHub Actions, Terraform, Kubernetes, security, FinOps, DevOps, programming languages, MLOps, AI, LLMs, ML, solutions architecture, troubleshooting, and engineering best practices.

The repository is documentation-first. Changes should improve navigation, accuracy, maintainability, or practical usefulness.

## Navigation model

Readers should be able to follow this route:

1. Start at [README.md](README.md).
2. Choose a major area such as [Cloud](cloud/README.md), [Databases](databases/README.md), [Git](git/README.md), [Terraform](terraform/README.md), [Kubernetes](kubernetes/README.md), [Security](security/README.md), [AI](ai/README.md), or [Cross-topic guides](cross-topic-guides/README.md).
3. Open a subcategory `README.md`.
4. Open a focused article.
5. Use the article's bottom links to return to the parent index and root index.

High-demand topics such as APISIX, Flux/GitOps, Akamai, CloudFront, and CDN guidance should also remain reachable through root-level fast paths and topic-specific quick paths in the relevant parent indexes.

When adding or moving content, update every affected index immediately.

## Global editing rules

- Use GitHub Flavored Markdown.
- Follow [instructions.md](instructions.md) for readable documentation structure, small tables, examples outside tables, and plain-language explanations.
- Use lowercase kebab-case for documentation directories and Markdown filenames.
- Use standard uppercase filenames only for repository-level files such as [README.md](README.md), [LICENSE](LICENSE), [CONTRIBUTING.md](CONTRIBUTING.md), [CHANGELOG.md](CHANGELOG.md), [ROADMAP.md](ROADMAP.md), and [GLOSSARY.md](GLOSSARY.md).
- Use relative links for all internal repository links.
- Do not leave broken placeholder links.
- Prefer official external documentation links for technical references.
- Mark early-stage pages with `Status: Initial outline`.
- Include navigation links back to the parent index and root index in focused articles.
- Every documentation directory must contain a `README.md` index, except `.github` workflow and issue-template directories.
- Update [CHANGELOG.md](CHANGELOG.md) for meaningful structural, navigation, or content additions.
- After validation passes and only intended changes remain, commit and push completed work unless the user explicitly asks not to or a blocker prevents it.
- Update this file when repository routes or editing conventions change.

## Where to edit

| Need | Edit here |
| --- | --- |
| Change the public landing page or top-level navigation | [README.md](README.md) |
| Change AI agent routing or deployment workflow | [AGENTS.md](AGENTS.md) |
| Change contribution standards | [CONTRIBUTING.md](CONTRIBUTING.md) |
| Change AI documentation structure standards | [instructions.md](instructions.md) |
| Record notable repository changes | [CHANGELOG.md](CHANGELOG.md) |
| Update planned work | [ROADMAP.md](ROADMAP.md) |
| Define shared terms | [GLOSSARY.md](GLOSSARY.md) |
| Add reusable article structures | [templates](templates/README.md) |
| Add architecture or repository decisions | [decision-records](decision-records/README.md) |
| Add images, diagrams, or icons | [assets](assets/README.md) |
| Add raw Markdown notes for later ingestion | [sources](sources/README.md) |
| Change GitHub metadata or validation workflows | [.github](.github/PULL_REQUEST_TEMPLATE.md) |

## Route map

### Root files

| File | Purpose | Edit when |
| --- | --- | --- |
| [README.md](README.md) | Human entry point and top-level navigation. | A major area, resource, or navigation pattern changes. |
| [AGENTS.md](AGENTS.md) | AI agent router for choosing routes, templates, validation, and deployment steps. | Agent execution workflow, routing rules, or documentation improvement process changes. |
| [context.md](context.md) | AI agent operating map. | Routes, conventions, or repository automation change. |
| [instructions.md](instructions.md) | AI documentation structure and readability standard. | Documentation layout, table, example, risk-note, or validation standards change. |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contribution and documentation standards. | Review expectations or writing standards change. |
| [CHANGELOG.md](CHANGELOG.md) | Notable changes. | A meaningful content, structure, or workflow change is made. |
| [ROADMAP.md](ROADMAP.md) | Planned future work. | Priorities or planned topic areas change. |
| [GLOSSARY.md](GLOSSARY.md) | Shared terms and acronyms. | New important terminology appears in articles. |
| [LICENSE](LICENSE) | Repository license. | License ownership or terms intentionally change. |

### Sources

| Route | Purpose | Edit when |
| --- | --- | --- |
| [sources/README.md](sources/README.md) | Raw Markdown source intake index. | Source intake folders or ingestion rules change. |
| [sources/AGENTS.md](sources/AGENTS.md) | Agent workflow for ingesting raw Markdown source files. | Classification, ingestion, archive, or validation behavior changes. |
| [sources/raw-topic-template.md](sources/raw-topic-template.md) | Optional metadata starter for raw topic notes. | Raw source metadata fields change. |
| [sources/incoming/README.md](sources/incoming/README.md) | Drop zone for raw `.md` files waiting for ingestion. | Incoming source rules change. |
| [sources/processed/README.md](sources/processed/README.md) | Archive for raw files already converted into curated docs. | Processed source archive rules change. |

### Assets

| Route | Purpose | Edit when |
| --- | --- | --- |
| [assets/README.md](assets/README.md) | Index for visual assets. | Asset categories change. |
| [assets/diagrams/README.md](assets/diagrams/README.md) | Diagram storage guidance. | Diagram naming or usage rules change. |
| [assets/images/README.md](assets/images/README.md) | Screenshot and image guidance. | Image standards change. |
| [assets/icons/README.md](assets/icons/README.md) | Icon storage guidance. | Icon standards change. |

### Templates

| Route | Purpose | Edit when |
| --- | --- | --- |
| [templates/README.md](templates/README.md) | Template index. | Templates are added, renamed, or removed. |
| [templates/knowledge-article-template.md](templates/knowledge-article-template.md) | General article starter. | Standard article structure changes. |
| [templates/command-reference-template.md](templates/command-reference-template.md) | Command reference starter. | Command documentation standards change. |
| [templates/troubleshooting-template.md](templates/troubleshooting-template.md) | Troubleshooting guide starter. | Diagnostic guide structure changes. |
| [templates/architecture-decision-record-template.md](templates/architecture-decision-record-template.md) | ADR starter. | Decision record format changes. |
| [templates/practical-example-template.md](templates/practical-example-template.md) | Hands-on example starter. | Example walkthrough standards change. |

### Git

| Route | Purpose | Edit when |
| --- | --- | --- |
| [git/README.md](git/README.md) | Git area index. | Git subcategories or major Git articles change. |
| [git/commands/README.md](git/commands/README.md) | Git command index. | Git command references are added or moved. |
| [git/commands/daily-commands.md](git/commands/daily-commands.md) | Common daily Git commands. | Daily workflow commands or examples change. |
| [git/commands/common-use-cases.md](git/commands/common-use-cases.md) | Scenario-based Git workflows. | Common Git workflow examples change. |
| [git/commands/solve-issues.md](git/commands/solve-issues.md) | Safe commands for undoing mistakes and recovering work. | Git issue-solving commands or safety guidance change. |
| [git/commands/troubleshooting-commands.md](git/commands/troubleshooting-commands.md) | Git diagnostic command reference. | Git troubleshooting diagnostics change. |
| [git/commands/advanced-commands.md](git/commands/advanced-commands.md) | Advanced Git command reference. | Rebase, patch, maintenance, or plumbing guidance changes. |
| [git/commands/complete-command-catalog.md](git/commands/complete-command-catalog.md) | Complete categorized Git command catalog. | Git command inventory or categorization changes. |
| [git/troubleshooting/README.md](git/troubleshooting/README.md) | Git troubleshooting index. | Git recovery guides are added or moved. |
| [git/troubleshooting/undo-and-recovery.md](git/troubleshooting/undo-and-recovery.md) | Undo and recovery guide. | Recovery procedures or safety guidance change. |
| [git/best-practices/README.md](git/best-practices/README.md) | Git best-practices index. | Branching, commits, or review practices change. |
| [git/tricks/README.md](git/tricks/README.md) | Git productivity notes. | Small Git techniques are added. |
| [git/github-actions/README.md](git/github-actions/README.md) | GitHub Actions index. | CI/CD workflow notes are added or moved. |
| [git/github-actions/components-and-concepts.md](git/github-actions/components-and-concepts.md) | GitHub Actions components and concepts. | Workflow building-block explanations change. |
| [git/github-actions/workflow-structure.md](git/github-actions/workflow-structure.md) | GitHub Actions workflow file structure. | Workflow syntax, trigger, job, step, matrix, or concurrency guidance changes. |
| [git/github-actions/commands.md](git/github-actions/commands.md) | GitHub Actions command reference. | GitHub CLI or workflow command guidance changes. |
| [git/github-actions/actions-and-uses-catalog.md](git/github-actions/actions-and-uses-catalog.md) | Common `uses:` action catalog. | Action recommendations, categories, or safety guidance change. |
| [git/github-actions/examples-and-use-cases.md](git/github-actions/examples-and-use-cases.md) | GitHub Actions examples and use cases. | CI/CD examples or workflow patterns change. |
| [git/github-actions/common-solutions.md](git/github-actions/common-solutions.md) | GitHub Actions common fixes. | Troubleshooting guidance or failure-mode solutions change. |
| [git/github-actions/security-secrets-and-permissions.md](git/github-actions/security-secrets-and-permissions.md) | GitHub Actions security, secrets, and permissions. | Token, secret, environment, OIDC, or third-party action safety guidance changes. |
| [git/github-actions/aws-oidc-federation.md](git/github-actions/aws-oidc-federation.md) | AWS OIDC federation from GitHub Actions. | GitHub-to-AWS federation guidance changes. |

### Terraform

| Route | Purpose | Edit when |
| --- | --- | --- |
| [terraform/README.md](terraform/README.md) | Terraform area index. | Terraform subcategories or major articles change. |
| [terraform/fundamentals/README.md](terraform/fundamentals/README.md) | Fundamentals index. | Core Terraform concept pages are added. |
| [terraform/fundamentals/state-management.md](terraform/fundamentals/state-management.md) | State management guide. | State, backend, locking, or drift guidance changes. |
| [terraform/commands/README.md](terraform/commands/README.md) | Terraform command index. | CLI references are added or moved. |
| [terraform/commands/core-workflow.md](terraform/commands/core-workflow.md) | Core workflow commands. | Format, init, validate, plan, or apply guidance changes. |
| [terraform/language/README.md](terraform/language/README.md) | Terraform language index. | HCL language notes are added. |
| [terraform/project-structure/README.md](terraform/project-structure/README.md) | Project structure index. | Module, environment, or repository layout guidance changes. |
| [terraform/troubleshooting/README.md](terraform/troubleshooting/README.md) | Terraform troubleshooting index. | Diagnostic guides are added. |
| [terraform/best-practices/README.md](terraform/best-practices/README.md) | Terraform best-practices index. | Maintainability or safety guidance changes. |
| [terraform/examples/README.md](terraform/examples/README.md) | Terraform examples index. | Practical examples are added. |

### Kubernetes

| Route | Purpose | Edit when |
| --- | --- | --- |
| [kubernetes/README.md](kubernetes/README.md) | Kubernetes area index. | Kubernetes subcategories or major articles change. |
| [kubernetes/fundamentals/README.md](kubernetes/fundamentals/README.md) | Fundamentals index. | Core Kubernetes concept pages are added. |
| [kubernetes/core-objects/README.md](kubernetes/core-objects/README.md) | Core objects index. | Object-specific pages are added. |
| [kubernetes/core-objects/stateful-workloads.md](kubernetes/core-objects/stateful-workloads.md) | Stateful workload objects and storage guidance. | StatefulSet, PVC, StorageClass, or stateful design guidance changes. |
| [kubernetes/core-objects/custom-resources-and-crds.md](kubernetes/core-objects/custom-resources-and-crds.md) | Custom resources, CRDs, and operator concepts. | Kubernetes API extension guidance changes. |
| [kubernetes/commands/README.md](kubernetes/commands/README.md) | Command index. | `kubectl` references are added or moved. |
| [kubernetes/commands/daily-usage.md](kubernetes/commands/daily-usage.md) | Daily `kubectl` usage. | Context, namespace, inspection, logs, events, exec, or port-forward guidance changes. |
| [kubernetes/commands/common-commands.md](kubernetes/commands/common-commands.md) | Common `kubectl` command reference. | Apply, diff, rollout, scale, delete, selector, or output-format guidance changes. |
| [kubernetes/commands/advanced-commands.md](kubernetes/commands/advanced-commands.md) | Advanced `kubectl` command reference. | JSONPath, dry-run, server-side apply, debug, node maintenance, or authorization guidance changes. |
| [kubernetes/commands/workflows.md](kubernetes/commands/workflows.md) | Kubernetes operational command workflows. | Deployment, rollback, service debugging, or resource-pressure workflows change. |
| [kubernetes/commands/eksctl-commands.md](kubernetes/commands/eksctl-commands.md) | AWS-native `eksctl` command reference for EKS. | EKS cluster, node group, add-on, access, Pod Identity, Fargate, endpoint, logging, or upgrade commands change. |
| [kubernetes/commands/kubectl-basics.md](kubernetes/commands/kubectl-basics.md) | Basic `kubectl` commands. | Common inspection commands change. |
| [kubernetes/crossplane/README.md](kubernetes/crossplane/README.md) | Crossplane concept guide and section index. | Crossplane core guidance or section navigation changes. |
| [kubernetes/crossplane/component-model.md](kubernetes/crossplane/component-model.md) | Crossplane component model guide. | Crossplane-specific component definitions, package objects, XRD/XR/Composition/Function relationships, Operations, Usages, MRDs, or MRAP guidance changes. |
| [kubernetes/crossplane/managed-resources-and-lifecycle.md](kubernetes/crossplane/managed-resources-and-lifecycle.md) | Crossplane managed-resource lifecycle guide. | Direct managed resources, reconciliation fields, references, import, pause, or deletion behavior changes. |
| [kubernetes/crossplane/providers-and-authentication.md](kubernetes/crossplane/providers-and-authentication.md) | Crossplane provider and authentication guide. | Provider package, ProviderConfig, authentication, activation policy, or schema-validation guidance changes. |
| [kubernetes/crossplane/compositions.md](kubernetes/crossplane/compositions.md) | Crossplane composition design. | Composition, XRD, XR, function pipeline, revision, render, or platform API guidance changes. |
| [kubernetes/crossplane/deployment-patterns-and-references.md](kubernetes/crossplane/deployment-patterns-and-references.md) | Crossplane multi-resource deployment and reference guide. | Terraform-style loop equivalents, multi-document YAML, dynamic function loops, resource references, selectors, or XR status patching changes. |
| [kubernetes/crossplane/professional-operating-model.md](kubernetes/crossplane/professional-operating-model.md) | Crossplane professional operating model guide. | Platform-team workflow, GitOps review, ownership, control-plane, or professional practice guidance changes. |
| [kubernetes/crossplane/aws-resource-workflow.md](kubernetes/crossplane/aws-resource-workflow.md) | Crossplane AWS resource workflow guide. | Install-to-AWS-resource workflow, component interaction, managed-resource deployment, or AWS management procedure changes. |
| [kubernetes/crossplane/local-aws-s3-lab.md](kubernetes/crossplane/local-aws-s3-lab.md) | Crossplane local AWS S3 hands-on lab. | Local lab, temporary AWS credential, S3 provider, drift test, or cleanup workflow changes. |
| [kubernetes/crossplane/production-gitops-and-operations.md](kubernetes/crossplane/production-gitops-and-operations.md) | Crossplane production, GitOps, observability, backup, upgrade, and operations guide. | Crossplane production operations, GitOps layering, metrics, backups, upgrades, or operational workflows change. |
| [kubernetes/crossplane/troubleshooting.md](kubernetes/crossplane/troubleshooting.md) | Crossplane troubleshooting guide. | Crossplane diagnostic guidance changes. |
| [kubernetes/crossplane/references.md](kubernetes/crossplane/references.md) | Crossplane official and supporting reference list. | Crossplane source references or research bibliography changes. |
| [kubernetes/applications-and-tools/README.md](kubernetes/applications-and-tools/README.md) | Tooling index. | Helm, Kustomize, controller, or GitOps notes are added. |
| [kubernetes/applications-and-tools/apache-apisix.md](kubernetes/applications-and-tools/apache-apisix.md) | Apache APISIX gateway guidance. | APISIX concepts or Kubernetes gateway guidance changes. |
| [kubernetes/applications-and-tools/apisix-architecture-and-deployment.md](kubernetes/applications-and-tools/apisix-architecture-and-deployment.md) | APISIX architecture and deployment guide. | APISIX data-plane, controller, Gateway API, deployment mode, EKS exposure, or troubleshooting flow guidance changes. |
| [kubernetes/applications-and-tools/apisix-security-traffic-and-observability.md](kubernetes/applications-and-tools/apisix-security-traffic-and-observability.md) | APISIX security, traffic, and observability guide. | APISIX authentication, rate limiting, traffic release, telemetry, or policy-placement guidance changes. |
| [kubernetes/applications-and-tools/gateway-api-and-ingress.md](kubernetes/applications-and-tools/gateway-api-and-ingress.md) | Gateway API and Ingress comparison. | Kubernetes traffic API guidance changes. |
| [kubernetes/applications-and-tools/gitops.md](kubernetes/applications-and-tools/gitops.md) | GitOps operating model. | GitOps reconciliation guidance changes. |
| [kubernetes/applications-and-tools/argo-cd-vs-flux.md](kubernetes/applications-and-tools/argo-cd-vs-flux.md) | Argo CD and Flux comparison. | GitOps controller comparison changes. |
| [kubernetes/applications-and-tools/flux.md](kubernetes/applications-and-tools/flux.md) | Flux controller and repository guidance. | Flux guidance changes. |
| [kubernetes/applications-and-tools/flux-reconciliation-and-helm.md](kubernetes/applications-and-tools/flux-reconciliation-and-helm.md) | Flux reconciliation and Helm release guide. | Flux source-controller, Kustomization, HelmRelease, dependency, or reconciliation troubleshooting guidance changes. |
| [kubernetes/applications-and-tools/gitops-security-and-multitenancy.md](kubernetes/applications-and-tools/gitops-security-and-multitenancy.md) | GitOps security and multi-tenancy guide. | GitOps ownership, Argo CD Projects, Flux tenancy, secrets, or controller-permission guidance changes. |
| [kubernetes/applications-and-tools/tooling-clusters.md](kubernetes/applications-and-tools/tooling-clusters.md) | Tooling cluster design. | Platform tooling cluster guidance changes. |
| [kubernetes/applications-and-tools/tooling-cluster-architecture.md](kubernetes/applications-and-tools/tooling-cluster-architecture.md) | Tooling cluster architecture guide. | Tooling-cluster patterns, failure behavior, security, or EKS account-boundary guidance changes. |
| [kubernetes/applications-and-tools/kind-custom-clusters.md](kubernetes/applications-and-tools/kind-custom-clusters.md) | Custom `kind` cluster guidance. | Local cluster lab or kind configuration guidance changes. |
| [kubernetes/applications-and-tools/kind-images-and-local-registries.md](kubernetes/applications-and-tools/kind-images-and-local-registries.md) | kind image and local-registry guide. | Loading local images, named kind clusters, local registries, or private-registry troubleshooting changes. |
| [kubernetes/troubleshooting/README.md](kubernetes/troubleshooting/README.md) | Troubleshooting index. | Kubernetes diagnostic guides are added. |
| [kubernetes/troubleshooting/crashloopbackoff.md](kubernetes/troubleshooting/crashloopbackoff.md) | CrashLoopBackOff guide. | Pod restart diagnostics change. |
| [kubernetes/troubleshooting/common-solutions.md](kubernetes/troubleshooting/common-solutions.md) | Common Kubernetes troubleshooting solutions. | Pending pod, image pull, service/DNS, rollout, or permission diagnostics change. |
| [kubernetes/troubleshooting/apisix.md](kubernetes/troubleshooting/apisix.md) | APISIX troubleshooting guide. | APISIX diagnostic guidance changes. |
| [kubernetes/troubleshooting/kind.md](kubernetes/troubleshooting/kind.md) | `kind` troubleshooting guide. | Local cluster diagnostic guidance changes. |
| [kubernetes/best-practices/README.md](kubernetes/best-practices/README.md) | Best-practices index. | Operational guidance changes. |
| [kubernetes/tricks/README.md](kubernetes/tricks/README.md) | Productivity notes. | Small Kubernetes techniques are added. |
| [kubernetes/examples/README.md](kubernetes/examples/README.md) | Examples index. | Practical manifests or walkthroughs are added. |

### Cloud

| Route | Purpose | Edit when |
| --- | --- | --- |
| [cloud/README.md](cloud/README.md) | Cloud provider and provider-neutral index. | Cloud provider routes or provider-neutral cloud topics change. |
| [cloud/edge/README.md](cloud/edge/README.md) | Edge and CDN index. | CDN or edge delivery articles are added. |
| [cloud/edge/cdn-and-edge-fundamentals.md](cloud/edge/cdn-and-edge-fundamentals.md) | CDN and edge fundamentals. | CDN terminology or edge design guidance changes. |
| [cloud/edge/cdn-caching-and-origin-protection.md](cloud/edge/cdn-caching-and-origin-protection.md) | CDN caching and origin-protection guide. | Cache keys, TTLs, purges, origin shielding, private origins, or direct-origin bypass guidance changes. |
| [cloud/edge/akamai-vs-cloudfront.md](cloud/edge/akamai-vs-cloudfront.md) | Akamai and CloudFront comparison. | CDN comparison or decision guidance changes. |
| [cloud/edge/multi-cdn-operations.md](cloud/edge/multi-cdn-operations.md) | Multi-CDN operations guide. | DNS, traffic steering, cache parity, logging, purge, or rollback guidance for multiple CDN providers changes. |
| [cloud/aws/README.md](cloud/aws/README.md) | AWS area index. | AWS subcategories or major articles change. |
| [cloud/aws/fundamentals/README.md](cloud/aws/fundamentals/README.md) | Fundamentals index. | Core AWS concept pages are added. |
| [cloud/aws/networking/README.md](cloud/aws/networking/README.md) | Networking index. | VPC, routing, or connectivity guides are added. |
| [cloud/aws/networking/security-groups.md](cloud/aws/networking/security-groups.md) | Security groups guide. | Security group behavior or troubleshooting guidance changes. |
| [cloud/aws/networking/cloudfront.md](cloud/aws/networking/cloudfront.md) | CloudFront guide. | CloudFront distribution, origin, or cache guidance changes. |
| [cloud/aws/networking/stateful-networking.md](cloud/aws/networking/stateful-networking.md) | Stateful AWS networking guide. | Security group, NACL, NAT, firewall, or appliance routing guidance changes. |
| [cloud/aws/compute/README.md](cloud/aws/compute/README.md) | Compute index. | EC2, scaling, containers, or serverless notes are added. |
| [cloud/aws/storage/README.md](cloud/aws/storage/README.md) | Storage index. | S3, EBS, EFS, backup, or lifecycle notes are added. |
| [cloud/aws/databases/README.md](cloud/aws/databases/README.md) | Databases index. | RDS, DynamoDB, cache, or data notes are added. |
| [cloud/aws/databases/amazon-msk.md](cloud/aws/databases/amazon-msk.md) | Amazon MSK guide. | AWS Kafka or MSK guidance changes. |
| [cloud/aws/databases/mongodb-on-aws.md](cloud/aws/databases/mongodb-on-aws.md) | MongoDB on AWS guide. | MongoDB deployment choices on AWS change. |
| [cloud/aws/databases/documentdb-vs-mongodb-atlas.md](cloud/aws/databases/documentdb-vs-mongodb-atlas.md) | DocumentDB and MongoDB Atlas comparison. | AWS document database comparison guidance changes. |
| [cloud/aws/security/README.md](cloud/aws/security/README.md) | Security index. | Encryption, detection, or incident notes are added. |
| [cloud/aws/security/iam-oidc-provider-and-sts-web-identity.md](cloud/aws/security/iam-oidc-provider-and-sts-web-identity.md) | IAM OIDC provider and STS web identity guide. | AWS OIDC federation guidance changes. |
| [cloud/aws/governance-and-access/README.md](cloud/aws/governance-and-access/README.md) | Governance and access index. | IAM, Organizations, SCP, or account guidance changes. |
| [cloud/aws/finops/README.md](cloud/aws/finops/README.md) | FinOps index. | Cost management guides are added. |
| [cloud/aws/finops/cost-allocation-tags.md](cloud/aws/finops/cost-allocation-tags.md) | Cost allocation tag guide. | Tagging standards or reporting guidance changes. |
| [cloud/aws/architecture/README.md](cloud/aws/architecture/README.md) | Architecture index. | Reference architecture or design review notes are added. |
| [cloud/aws/architecture/stateful-vs-stateless.md](cloud/aws/architecture/stateful-vs-stateless.md) | Stateful vs. stateless AWS design guide. | AWS state, scaling, or recovery design guidance changes. |
| [cloud/aws/architecture/stateless-application-patterns.md](cloud/aws/architecture/stateless-application-patterns.md) | Stateless AWS application pattern guide. | Externalizing application state, replaceable compute, or safe replica-replacement guidance changes. |
| [cloud/aws/architecture/stateful-design-decision-checklist.md](cloud/aws/architecture/stateful-design-decision-checklist.md) | Stateful AWS design checklist. | State ownership, backups, RPO/RTO, stateful networking, or Kubernetes stateful workload review guidance changes. |
| [cloud/aws/troubleshooting/README.md](cloud/aws/troubleshooting/README.md) | AWS troubleshooting index. | AWS diagnostic runbooks are added. |
| [cloud/aws/solutions-architect/README.md](cloud/aws/solutions-architect/README.md) | Solutions architect notes. | Certification or architecture review notes are added. |
| [cloud/azure/README.md](cloud/azure/README.md) | Azure area index. | Azure service, architecture, governance, or operations notes are added. |
| [cloud/gcloud/README.md](cloud/gcloud/README.md) | Google Cloud area index. | Google Cloud service, architecture, governance, or operations notes are added. |

### Databases

| Route | Purpose | Edit when |
| --- | --- | --- |
| [databases/README.md](databases/README.md) | Database and data-platform index. | Database categories or major database articles change. |
| [databases/kafka/README.md](databases/kafka/README.md) | Kafka index. | Kafka articles are added or moved. |
| [databases/kafka/fundamentals.md](databases/kafka/fundamentals.md) | Kafka fundamentals. | Kafka architecture or concept guidance changes. |
| [databases/kafka/topic-and-event-design.md](databases/kafka/topic-and-event-design.md) | Kafka topic and event design. | Topic, schema, retention, or event contract guidance changes. |
| [databases/kafka/consumer-groups-lag-and-replay.md](databases/kafka/consumer-groups-lag-and-replay.md) | Kafka consumer group, lag, and replay guide. | Consumer assignment, offset commits, lag diagnostics, replay, or offset-reset guidance changes. |
| [databases/kafka/delivery-guarantees-and-failure-handling.md](databases/kafka/delivery-guarantees-and-failure-handling.md) | Kafka delivery guarantees and failure-handling guide. | Producer safety, consumer idempotency, retry topics, dead-letter topics, or outbox guidance changes. |
| [databases/kafka/operations.md](databases/kafka/operations.md) | Kafka operations. | Kafka monitoring, lag, replication, or recovery guidance changes. |
| [databases/mongodb/README.md](databases/mongodb/README.md) | MongoDB index. | MongoDB articles are added or moved. |
| [databases/mongodb/fundamentals.md](databases/mongodb/fundamentals.md) | MongoDB fundamentals. | MongoDB concept guidance changes. |
| [databases/mongodb/data-modeling.md](databases/mongodb/data-modeling.md) | MongoDB data modeling. | Document modeling guidance changes. |
| [databases/mongodb/schema-validation-and-indexing.md](databases/mongodb/schema-validation-and-indexing.md) | MongoDB schema validation and indexing guide. | JSON Schema validation, schema versioning, index design, TTL indexes, or explain-plan checks change. |
| [databases/mongodb/replication-sharding-and-consistency.md](databases/mongodb/replication-sharding-and-consistency.md) | MongoDB replication, sharding, and consistency guide. | Replica set, write concern, read concern, shard key, backup, restore, or consistency guidance changes. |
| [databases/mongodb/operations.md](databases/mongodb/operations.md) | MongoDB operations. | MongoDB performance, backup, replication, or sharding guidance changes. |
| [databases/relational-vs-document-databases.md](databases/relational-vs-document-databases.md) | Relational and document database comparison. | Database model decision guidance changes. |

### Principal topic indexes

| Route | Purpose | Edit when |
| --- | --- | --- |
| [security/README.md](security/README.md) | Security index. | Cross-platform security content is added. |
| [security/identity-federation/README.md](security/identity-federation/README.md) | Identity federation index. | Federation or OIDC articles are added. |
| [security/identity-federation/oidc-fundamentals.md](security/identity-federation/oidc-fundamentals.md) | OIDC fundamentals. | OIDC concept or token validation guidance changes. |
| [security/identity-federation/oidc-token-validation.md](security/identity-federation/oidc-token-validation.md) | OIDC token validation guide. | JWT signature, issuer, audience, JWKS, time claim, nonce, or token-purpose validation guidance changes. |
| [security/identity-federation/eks-human-identity-and-rbac.md](security/identity-federation/eks-human-identity-and-rbac.md) | EKS human identity and Kubernetes RBAC guide. | Human EKS authentication, access entries, OIDC group claims, or RBAC binding guidance changes. |
| [finops/README.md](finops/README.md) | FinOps index. | Provider-neutral cost-management content is added. |
| [devops/README.md](devops/README.md) | DevOps index. | Delivery, automation, platform, or operations content is added. |
| [programming-languages/README.md](programming-languages/README.md) | Programming languages index. | Language-specific notes or examples are added. |
| [mlops/README.md](mlops/README.md) | MLOps index. | ML operations, deployment, monitoring, or governance content is added. |
| [ai/README.md](ai/README.md) | AI index. | General AI system, workflow, or safety content is added. |
| [ai-agents/README.md](ai-agents/README.md) | AI agents index. | Agent workflow, routing, tool-use, or evaluation content is added. |
| [llm/README.md](llm/README.md) | LLM index. | LLM prompting, retrieval, evaluation, deployment, or operations content is added. |
| [ml/README.md](ml/README.md) | ML index. | Machine learning concepts, datasets, training, or evaluation content is added. |
| [solutions-architect/README.md](solutions-architect/README.md) | Solutions architect index. | Architecture trade-off, review, or study content is added. |

### Cross-topic guides

| Route | Purpose | Edit when |
| --- | --- | --- |
| [cross-topic-guides/README.md](cross-topic-guides/README.md) | Cross-topic guide index. | Multi-technology guides are added or moved. |
| [cross-topic-guides/terraform-on-aws.md](cross-topic-guides/terraform-on-aws.md) | Terraform and AWS integration. | AWS IaC patterns change. |
| [cross-topic-guides/kubernetes-on-aws.md](cross-topic-guides/kubernetes-on-aws.md) | Kubernetes on AWS guidance. | EKS or AWS integration notes change. |
| [cross-topic-guides/github-actions-with-terraform.md](cross-topic-guides/github-actions-with-terraform.md) | GitHub Actions and Terraform CI. | Terraform CI/CD patterns change. |
| [cross-topic-guides/github-actions-with-kubernetes.md](cross-topic-guides/github-actions-with-kubernetes.md) | GitHub Actions and Kubernetes CI/CD. | Kubernetes deployment automation changes. |
| [cross-topic-guides/deploying-to-eks.md](cross-topic-guides/deploying-to-eks.md) | EKS deployment planning. | EKS deployment procedures change. |
| [cross-topic-guides/eks-operations.md](cross-topic-guides/eks-operations.md) | Day-to-day EKS operations with AWS CLI and kubectl. | EKS operational commands, access, add-ons, or diagnostics change. |
| [cross-topic-guides/cdn-in-front-of-eks.md](cross-topic-guides/cdn-in-front-of-eks.md) | CDN fronting EKS workloads. | CDN, ingress, or EKS edge routing guidance changes. |
| [cross-topic-guides/apisix-on-eks.md](cross-topic-guides/apisix-on-eks.md) | APISIX on EKS guide. | APISIX and EKS architecture guidance changes. |
| [cross-topic-guides/eks-to-msk-applications.md](cross-topic-guides/eks-to-msk-applications.md) | EKS applications connecting to MSK. | Kafka client, networking, or MSK guidance changes. |
| [cross-topic-guides/crossplane-on-aws.md](cross-topic-guides/crossplane-on-aws.md) | Crossplane on AWS guide. | Crossplane AWS platform guidance changes. |
| [cross-topic-guides/gitops-on-eks.md](cross-topic-guides/gitops-on-eks.md) | GitOps on EKS guide. | Argo CD, Flux, or EKS GitOps guidance changes. |
| [cross-topic-guides/eks-workload-identity.md](cross-topic-guides/eks-workload-identity.md) | EKS workload identity guide. | IRSA or EKS Pod Identity guidance changes. |
| [cross-topic-guides/eks-tooling-cluster-architecture.md](cross-topic-guides/eks-tooling-cluster-architecture.md) | EKS tooling cluster architecture. | Platform tooling cluster guidance changes. |
| [cross-topic-guides/observability-stack.md](cross-topic-guides/observability-stack.md) | Observability planning. | Monitoring, logging, tracing, or alerting guidance changes. |
| [cross-topic-guides/end-to-end-deployment.md](cross-topic-guides/end-to-end-deployment.md) | Full delivery flow. | Source-to-production workflow guidance changes. |

### Decision records

| Route | Purpose | Edit when |
| --- | --- | --- |
| [decision-records/README.md](decision-records/README.md) | ADR index. | ADRs are added, renamed, or superseded. |
| [decision-records/ADR-0001-knowledge-base-structure.md](decision-records/ADR-0001-knowledge-base-structure.md) | Initial structure decision. | Only edit to correct history or add clearly marked amendments. |
| [decision-records/ADR-0002-source-ingestion-and-topic-taxonomy.md](decision-records/ADR-0002-source-ingestion-and-topic-taxonomy.md) | Source ingestion and expanded topic taxonomy decision. | Only edit to correct history or add clearly marked amendments. |

### GitHub metadata and workflows

| Route | Purpose | Edit when |
| --- | --- | --- |
| [.github/CODEOWNERS](.github/CODEOWNERS) | Default repository ownership. | Ownership or review routing changes. |
| [.github/PULL_REQUEST_TEMPLATE.md](.github/PULL_REQUEST_TEMPLATE.md) | Pull request checklist. | Review expectations change. |
| [.github/ISSUE_TEMPLATE/documentation-error.yml](.github/ISSUE_TEMPLATE/documentation-error.yml) | Documentation error issue form. | Error reporting fields change. |
| [.github/ISSUE_TEMPLATE/new-topic.yml](.github/ISSUE_TEMPLATE/new-topic.yml) | New topic issue form. | Topic proposal fields change. |
| [.github/ISSUE_TEMPLATE/improvement.yml](.github/ISSUE_TEMPLATE/improvement.yml) | Improvement issue form. | Improvement request fields change. |
| [.github/workflows/markdown-lint.yml](.github/workflows/markdown-lint.yml) | Markdown lint workflow. | Markdown lint behavior changes. |
| [.github/workflows/link-check.yml](.github/workflows/link-check.yml) | Link check workflow. | Link validation behavior changes. |
| [.github/workflows/terraform-format.yml](.github/workflows/terraform-format.yml) | Terraform format workflow. | Terraform validation behavior changes. |
| [.markdownlint-cli2.jsonc](.markdownlint-cli2.jsonc) | Markdown lint configuration. | Local or CI lint rules change. |
| [.gitattributes](.gitattributes) | Line-ending and binary file handling. | File normalization rules change. |

## How to add a new article

1. Choose the correct major area and subcategory.
2. Copy the closest template from [templates](templates/README.md).
3. Name the file in lowercase kebab-case.
4. Follow [instructions.md](instructions.md) for readable structure, examples, explanations, and risk notes.
5. Add a clear title, purpose, practical content, and navigation links.
6. Add the article to the parent `README.md` index.
7. If it creates a new concept, update [GLOSSARY.md](GLOSSARY.md).
8. If it changes repository structure or standards, update this file.
9. Add a short note to [CHANGELOG.md](CHANGELOG.md).

## How to add a new directory

1. Create the directory using lowercase kebab-case.
2. Add a `README.md` index immediately.
3. Link the new directory from its parent index.
4. Add the route to this file.
5. Update [README.md](README.md) if it is a new top-level area or resource.
6. Validate internal links before committing.

## How to ingest raw source files

1. Place raw `.md` files in [sources/incoming](sources/incoming/README.md).
2. Follow [sources/AGENTS.md](sources/AGENTS.md) to classify each source by topic, provider, and destination.
3. Convert the raw material into the closest existing article or a new focused article.
4. Update parent indexes, related links, [GLOSSARY.md](GLOSSARY.md), and [CHANGELOG.md](CHANGELOG.md) when needed.
5. Move processed raw files to [sources/processed](sources/processed/README.md).

## How to modify existing files

- Keep edits scoped to the page's purpose.
- Preserve existing navigation links unless the route changes.
- Update parent indexes when article titles, filenames, or locations change.
- Prefer small scan-friendly tables for comparisons and checklists for operational procedures.
- Put command examples outside tables and explain them with `What it does:` text below the example.
- Use fenced code blocks with language identifiers.
- Include expected command output where it helps readers verify success.
- Use GitHub alerts for operational risk, useful tips, or important caveats.

## Validation checklist for agents

- [ ] `git status --short --branch` shows only intended changes before staging.
- [ ] Every new documentation directory has a `README.md`.
- [ ] Every new article is linked from its parent index.
- [ ] Internal links are relative and resolve locally.
- [ ] Markdown lint passes when tooling is available.
- [ ] [CHANGELOG.md](CHANGELOG.md) is updated for meaningful changes.
- [ ] [AGENTS.md](AGENTS.md) is updated when routing or deployment workflow changes.
- [ ] [context.md](context.md) is updated when routes or conventions change.
- [ ] Processed raw source files are archived under [sources/processed](sources/processed/README.md).
- [ ] Completed work is committed and pushed after successful validation, unless explicitly blocked.

[Back to root index](README.md)
