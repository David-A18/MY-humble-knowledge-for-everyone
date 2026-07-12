# AI agent context

This file is the operating map for AI agents working in `engineering-knowledge-base`. Use it before editing so routes, indexes, templates, and repository conventions stay connected.

> [!IMPORTANT]
> Keep this file updated whenever files, directories, templates, workflows, or navigation rules change.

## Repository intent

`engineering-knowledge-base` is a long-term personal knowledge base for practical engineering knowledge across Git, GitHub Actions, Terraform, Kubernetes, AWS, FinOps, cloud architecture, troubleshooting, and engineering best practices.

The repository is documentation-first. Changes should improve navigation, accuracy, maintainability, or practical usefulness.

## Navigation model

Readers should be able to follow this route:

1. Start at [README.md](README.md).
2. Choose a major area such as [Git](git/README.md), [Terraform](terraform/README.md), [Kubernetes](kubernetes/README.md), [AWS](aws/README.md), or [Cross-topic guides](cross-topic-guides/README.md).
3. Open a subcategory `README.md`.
4. Open a focused article.
5. Use the article's bottom links to return to the parent index and root index.

When adding or moving content, update every affected index immediately.

## Global editing rules

- Use GitHub Flavored Markdown.
- Use lowercase kebab-case for documentation directories and Markdown filenames.
- Use standard uppercase filenames only for repository-level files such as [README.md](README.md), [LICENSE](LICENSE), [CONTRIBUTING.md](CONTRIBUTING.md), [CHANGELOG.md](CHANGELOG.md), [ROADMAP.md](ROADMAP.md), and [GLOSSARY.md](GLOSSARY.md).
- Use relative links for all internal repository links.
- Do not leave broken placeholder links.
- Prefer official external documentation links for technical references.
- Mark early-stage pages with `Status: Initial outline`.
- Include navigation links back to the parent index and root index in focused articles.
- Every documentation directory must contain a `README.md` index, except `.github` workflow and issue-template directories.
- Update [CHANGELOG.md](CHANGELOG.md) for meaningful structural, navigation, or content additions.
- Update this file when repository routes or editing conventions change.

## Where to edit

| Need | Edit here |
| --- | --- |
| Change the public landing page or top-level navigation | [README.md](README.md) |
| Change contribution standards | [CONTRIBUTING.md](CONTRIBUTING.md) |
| Record notable repository changes | [CHANGELOG.md](CHANGELOG.md) |
| Update planned work | [ROADMAP.md](ROADMAP.md) |
| Define shared terms | [GLOSSARY.md](GLOSSARY.md) |
| Add reusable article structures | [templates](templates/README.md) |
| Add architecture or repository decisions | [decision-records](decision-records/README.md) |
| Add images, diagrams, or icons | [assets](assets/README.md) |
| Change GitHub metadata or validation workflows | [.github](.github/PULL_REQUEST_TEMPLATE.md) |

## Route map

### Root files

| File | Purpose | Edit when |
| --- | --- | --- |
| [README.md](README.md) | Human entry point and top-level navigation. | A major area, resource, or navigation pattern changes. |
| [context.md](context.md) | AI agent operating map. | Routes, conventions, or repository automation change. |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contribution and documentation standards. | Review expectations or writing standards change. |
| [CHANGELOG.md](CHANGELOG.md) | Notable changes. | A meaningful content, structure, or workflow change is made. |
| [ROADMAP.md](ROADMAP.md) | Planned future work. | Priorities or planned topic areas change. |
| [GLOSSARY.md](GLOSSARY.md) | Shared terms and acronyms. | New important terminology appears in articles. |
| [LICENSE](LICENSE) | Repository license. | License ownership or terms intentionally change. |

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
| [git/troubleshooting/README.md](git/troubleshooting/README.md) | Git troubleshooting index. | Git recovery guides are added or moved. |
| [git/troubleshooting/undo-and-recovery.md](git/troubleshooting/undo-and-recovery.md) | Undo and recovery guide. | Recovery procedures or safety guidance change. |
| [git/best-practices/README.md](git/best-practices/README.md) | Git best-practices index. | Branching, commits, or review practices change. |
| [git/tricks/README.md](git/tricks/README.md) | Git productivity notes. | Small Git techniques are added. |
| [git/github-actions/README.md](git/github-actions/README.md) | GitHub Actions index. | CI/CD workflow notes are added or moved. |

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
| [kubernetes/commands/README.md](kubernetes/commands/README.md) | Command index. | `kubectl` references are added or moved. |
| [kubernetes/commands/kubectl-basics.md](kubernetes/commands/kubectl-basics.md) | Basic `kubectl` commands. | Common inspection commands change. |
| [kubernetes/applications-and-tools/README.md](kubernetes/applications-and-tools/README.md) | Tooling index. | Helm, Kustomize, controller, or GitOps notes are added. |
| [kubernetes/troubleshooting/README.md](kubernetes/troubleshooting/README.md) | Troubleshooting index. | Kubernetes diagnostic guides are added. |
| [kubernetes/troubleshooting/crashloopbackoff.md](kubernetes/troubleshooting/crashloopbackoff.md) | CrashLoopBackOff guide. | Pod restart diagnostics change. |
| [kubernetes/best-practices/README.md](kubernetes/best-practices/README.md) | Best-practices index. | Operational guidance changes. |
| [kubernetes/tricks/README.md](kubernetes/tricks/README.md) | Productivity notes. | Small Kubernetes techniques are added. |
| [kubernetes/examples/README.md](kubernetes/examples/README.md) | Examples index. | Practical manifests or walkthroughs are added. |

### AWS

| Route | Purpose | Edit when |
| --- | --- | --- |
| [aws/README.md](aws/README.md) | AWS area index. | AWS subcategories or major articles change. |
| [aws/fundamentals/README.md](aws/fundamentals/README.md) | Fundamentals index. | Core AWS concept pages are added. |
| [aws/networking/README.md](aws/networking/README.md) | Networking index. | VPC, routing, or connectivity guides are added. |
| [aws/networking/security-groups.md](aws/networking/security-groups.md) | Security groups guide. | Security group behavior or troubleshooting guidance changes. |
| [aws/compute/README.md](aws/compute/README.md) | Compute index. | EC2, scaling, containers, or serverless notes are added. |
| [aws/storage/README.md](aws/storage/README.md) | Storage index. | S3, EBS, EFS, backup, or lifecycle notes are added. |
| [aws/databases/README.md](aws/databases/README.md) | Databases index. | RDS, DynamoDB, cache, or data notes are added. |
| [aws/security/README.md](aws/security/README.md) | Security index. | Encryption, detection, or incident notes are added. |
| [aws/governance-and-access/README.md](aws/governance-and-access/README.md) | Governance and access index. | IAM, Organizations, SCP, or account guidance changes. |
| [aws/finops/README.md](aws/finops/README.md) | FinOps index. | Cost management guides are added. |
| [aws/finops/cost-allocation-tags.md](aws/finops/cost-allocation-tags.md) | Cost allocation tag guide. | Tagging standards or reporting guidance changes. |
| [aws/architecture/README.md](aws/architecture/README.md) | Architecture index. | Reference architecture or design review notes are added. |
| [aws/troubleshooting/README.md](aws/troubleshooting/README.md) | AWS troubleshooting index. | AWS diagnostic runbooks are added. |
| [aws/solutions-architect/README.md](aws/solutions-architect/README.md) | Solutions architect notes. | Certification or architecture review notes are added. |

### Cross-topic guides

| Route | Purpose | Edit when |
| --- | --- | --- |
| [cross-topic-guides/README.md](cross-topic-guides/README.md) | Cross-topic guide index. | Multi-technology guides are added or moved. |
| [cross-topic-guides/terraform-on-aws.md](cross-topic-guides/terraform-on-aws.md) | Terraform and AWS integration. | AWS IaC patterns change. |
| [cross-topic-guides/kubernetes-on-aws.md](cross-topic-guides/kubernetes-on-aws.md) | Kubernetes on AWS guidance. | EKS or AWS integration notes change. |
| [cross-topic-guides/github-actions-with-terraform.md](cross-topic-guides/github-actions-with-terraform.md) | GitHub Actions and Terraform CI. | Terraform CI/CD patterns change. |
| [cross-topic-guides/github-actions-with-kubernetes.md](cross-topic-guides/github-actions-with-kubernetes.md) | GitHub Actions and Kubernetes CI/CD. | Kubernetes deployment automation changes. |
| [cross-topic-guides/deploying-to-eks.md](cross-topic-guides/deploying-to-eks.md) | EKS deployment planning. | EKS deployment procedures change. |
| [cross-topic-guides/observability-stack.md](cross-topic-guides/observability-stack.md) | Observability planning. | Monitoring, logging, tracing, or alerting guidance changes. |
| [cross-topic-guides/end-to-end-deployment.md](cross-topic-guides/end-to-end-deployment.md) | Full delivery flow. | Source-to-production workflow guidance changes. |

### Decision records

| Route | Purpose | Edit when |
| --- | --- | --- |
| [decision-records/README.md](decision-records/README.md) | ADR index. | ADRs are added, renamed, or superseded. |
| [decision-records/ADR-0001-knowledge-base-structure.md](decision-records/ADR-0001-knowledge-base-structure.md) | Initial structure decision. | Only edit to correct history or add clearly marked amendments. |

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
4. Add a clear title, purpose, practical content, and navigation links.
5. Add the article to the parent `README.md` index.
6. If it creates a new concept, update [GLOSSARY.md](GLOSSARY.md).
7. If it changes repository structure or standards, update this file.
8. Add a short note to [CHANGELOG.md](CHANGELOG.md).

## How to add a new directory

1. Create the directory using lowercase kebab-case.
2. Add a `README.md` index immediately.
3. Link the new directory from its parent index.
4. Add the route to this file.
5. Update [README.md](README.md) if it is a new top-level area or resource.
6. Validate internal links before committing.

## How to modify existing files

- Keep edits scoped to the page's purpose.
- Preserve existing navigation links unless the route changes.
- Update parent indexes when article titles, filenames, or locations change.
- Prefer tables for comparisons and checklists for operational procedures.
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
- [ ] [context.md](context.md) is updated when routes or conventions change.

[Back to root index](README.md)
