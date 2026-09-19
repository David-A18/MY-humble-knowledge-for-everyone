# Changelog

All notable changes to this repository are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this repository uses calendar-aware, human-readable release notes rather than package versioning.

## Unreleased

### Added

- Added GitHub tracking issues for the remaining KB-04 AWS sandbox validation and KB-14 reader-test evidence blockers.
- Added an external evidence request checklist for the remaining KB-04 AWS sandbox and KB-14 reader-test blockers.
- Added a reader test facilitator guide for KB-14 sessions, with a standard prompt, expected routes, scoring rules, hint guidance, and follow-up workflow.
- Added maintained issue-template validation with a local Python checker and GitHub Actions workflow.
- Added GitHub issue forms for KB-14 reader-test results and KB-04 Crossplane AWS S3 sandbox validation runs.
- Added a Crossplane AWS S3 lab validation template for future authorized sandbox runs, with version capture, identity checks, execution evidence, failure handling, cleanup proof, and publication-update guidance.
- Added a reader-test results template for KB-14 sessions, including task outcomes, blocker tracking, terminology feedback, privacy guidance, and follow-up actions.
- Completed the local Kubernetes beginner path author run with rootless Docker, kind, and kubectl; fixed the failing-image manifest so the exercise produces the intended `ErrImagePull` diagnosis and rollback flow.
- Added ADR-0003, deciding to keep repository Markdown navigation as the canonical publishing surface until reader testing shows a measured need for a searchable static site.
- Added a maintenance review queue with priority guide review dates, blocked validation follow-ups, a reader-task testing protocol, and contributor navigation links.
- Added the first local beginner route with `start-here.md`, a local Kubernetes deployment learning path, exact Kubernetes exercise manifests, and a Terraform local-state lifecycle exercise.
- Added review-information blocks to ten priority operational guides covering Git recovery, Crossplane, Terraform, Kafka, Velero, and EKS deployment, with current source-review evidence and explicit integration-test limits.
- Added a processed-source ingestion register and contents navigation for long Git, K9s, and Crossplane reference pages.
- Added maintained local-link validation scripts, validator fixtures, CI wiring, manual workflow triggers, and explicit workflow permissions for documentation validation.
- Added visible article review-information standards to the writing instructions, templates, and contributor checklist.
- Corrected Git restore guidance, Kafka manual-commit example behavior, Crossplane temporary AWS credential examples, and the Markdown lint baseline.
- Added an actionable knowledge-base improvement plan with 15 work packages, dependencies, contributor instructions, quality criteria, evidence tracking, and maintenance targets; linked it from the roadmap and repository routing guides.
- Added a dated knowledge-base review covering structure, learning paths, technical spot checks, validation, maintenance, and prioritized improvements, with links from the root index and context map.
- Added Crossplane provider, managed-resource, Composition, Function, and Configuration package guidance; an ECR-backed application delivery platform API; Helm installation and lifecycle guidance; and Amazon ECR OCI/Helm operational guidance.
- Initial professional documentation scaffold for Git, Terraform, Kubernetes, AWS, cross-topic guides, templates, decision records, and repository maintenance files.
- MIT license.
- GitHub issue templates, pull request template, CODEOWNERS, and documentation validation workflows.
- AI agent context map with repository routes, editing rules, and validation expectations.
- Expanded Git command documentation with daily commands, common use cases, issue-solving commands, troubleshooting diagnostics, advanced commands, and a complete command catalog.
- Refactored Git command documentation for easier reading with smaller tables and examples outside table cells.
- Added AI documentation instructions for readable page structure, small tables, examples outside tables, explanations, risk notes, and validation expectations.
- Added GitHub Actions documentation covering concepts, workflow structure, commands, `uses:` actions, examples, common solutions, and security guidance.
- Expanded GitHub Actions `uses:` guidance with reference syntax, catalog navigation, action selection checks, and broader common-action coverage.
- Expanded Kubernetes and EKS documentation with daily `kubectl` commands, common and advanced command references, operational workflows, troubleshooting solutions, tricks, best practices, EKS operations, and AWS-focused deployment guidance.
- Added an agent instruction to commit and push completed documentation work after successful validation.
- Added an `eksctl` command reference for AWS-native EKS cluster, node group, add-on, access, Pod Identity, Fargate, networking, logging, and upgrade operations.
- Added an AI agent router with route selection, template choice, improvement workflow, link rules, validation, and deployment guidance.
- Added a raw Markdown source intake area with incoming and processed folders, ingestion instructions, and a raw topic template.
- Added a cloud provider hierarchy, moved AWS documentation under `cloud/aws`, and added initial Azure and Google Cloud indexes.
- Added initial topic indexes for security, FinOps, DevOps, programming languages, MLOps, AI, AI agents, LLM, ML, and solutions architect content.
- Added ADR-0002 for source ingestion and expanded topic taxonomy.
- Ingested raw source guides into curated articles for CDN and edge delivery, APISIX, Kafka, stateful AWS design, Crossplane, GitOps, MongoDB, OIDC, EKS workload identity, tooling clusters, `kind`, and CRDs.
- Added a top-level databases section for Kafka, MongoDB, and database model decision guidance.
- Improved the root README knowledge-area table to show principal areas with their current subtopics.
- Promoted Crossplane into its own Kubernetes subtopic and updated canonical links.
- Expanded the Crossplane section with managed-resource lifecycle, provider authentication, composition, local AWS S3 lab, production GitOps and operations, troubleshooting, and AWS architecture guidance.
- Added deeper Crossplane professional-practice guidance, an end-to-end AWS resource workflow, and a dedicated Crossplane references page.
- Added Crossplane deployment-pattern guidance for multi-resource YAML, Terraform-style loop equivalents, resource references, selectors, and XR status patching.
- Added a Crossplane component-model guide defining XRDs, XRs, Compositions, Functions, Configuration packages, MRDs, MRAPs, Operations, Usages, EnvironmentConfigs, package revisions, and package runtime controls.
- Added a Terraform modules versus Crossplane reusable platform APIs comparison with Configuration package examples.
- Ingested additional processed source guidance into focused articles for CDN caching and multi-CDN operations, APISIX architecture and policy, Kafka lag/replay and delivery guarantees, AWS stateful design, Flux/GitOps operations, MongoDB validation and scaling, OIDC/EKS identity, and tooling/kind workflows.
- Expanded the ingested topic set with deeper explanations, component maps, request and reconciliation flows, examples, troubleshooting checks, and official reference links across edge/CDN, APISIX, Kafka, AWS state design, GitOps, MongoDB, OIDC/EKS identity, tooling clusters, and `kind`.
- Improved navigation for APISIX, Flux, GitOps, Akamai, CloudFront, and CDN content with root-level fast paths, topic-specific index paths, and cross-topic guide navigation routes.
- Added a top-level migrations section with a Velero guide covering Kubernetes backup, restore, S3-compatible storage, EBS and CSI snapshots, File System Backup, cluster migration, disaster recovery, runbooks, and troubleshooting.
- Expanded Velero fundamentals, architecture, storage, installation, backup and restore workflows, migration planning, runbooks, and troubleshooting with beginner-to-operations explanations, concrete YAML examples, EKS/S3/EBS configuration, volume backup trade-offs, GitOps migration guidance, and AKS-to-EKS cross-cloud migration guidance.
- Added a Velero possible integrations guide with a GitHub Actions pipeline pattern, operation instruction file, OIDC and EKS access requirements, backup and migration modes, full-cluster resource backup option, and supporting Velero configuration examples.
- Added Crossplane knowledge-base coverage under the canonical Kubernetes Crossplane section, including fundamentals, deployment workflows, examples, XRDs, Compositions, and Terraform comparison guidance.
- Consolidated the requested Crossplane VPC example into the canonical `kubernetes/crossplane` section and cleaned up duplicate top-level Crossplane navigation.
- Split Crossplane XRD/XR and Composition guidance into separate AWS-focused sections.
- Added an AWS VPC Crossplane example with a `PlatformNetwork` XRD, XR call, and multi-resource Composition.
- Added a dedicated Terraform vs Crossplane comparison explaining what Crossplane solves beyond Terraform's run-based workflow.
- Added AWS compute coverage for Amazon ECS fundamentals, ECS versus EKS decision guidance, and full-platform EKS-to-ECS migration planning.
- Added AI guidance for MCP, custom tools, Markdown knowledge-base management, skills, retrieval, and OKF v0.2 bundles.
- Split AI tooling into a dedicated section with focused guides for MCP, Claude and Codex tools, and agent knowledge-base management.
- Expanded OKF guidance with clearer purpose, consumption model, field details, attestation behavior, and a platform-operations bundle scenario.
- Added a provider-neutral cloud solutions section with blue-green deployment guidance, recognition signals, service maps, risks, and official references.
- Added a K9s guide for Kubernetes terminal UI navigation, common views, inspection workflows, filters, aliases, hotkeys, plugins, and safe read-only use.
- Added a Crossplane beginner guide explaining XRDs, Compositions, XRs, composition selection, naming rules, and the Terraform module-call analogy.
- Added a beginner Bootstrap and bootstrapping concept guide covering the frontend toolkit, class meanings, startup processes, project setup, and infrastructure bootstrapping.
- Added a Proof of Concept guide under solutions architect with vocabulary, scope, success criteria, deliverables, examples, risks, and review guidance.
- Added a GitHub Actions pipeline failure report and validation hardening for Markdown lint, link checking, and action runtime warnings.
- Added an agent-first knowledge-base reference architecture under AI tooling, covering OKF v0.2, knowledge standards, Git-backed corpus design, retrieval budgets, provenance, freshness, security, governance, evaluation, and a conformant public-safe OKF example bundle.
- Added Apigee API management coverage under Google Cloud and SonarQube code quality plus GitHub integration coverage under DevOps, with root fast paths and glossary entries.
- Added a content-only CI/CD process guide requiring documentation changes to land in `main`, with validation-focused checks, no required human review for normal content changes, and branch cleanup guidance.
