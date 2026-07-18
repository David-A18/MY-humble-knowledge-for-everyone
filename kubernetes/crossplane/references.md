# Crossplane references

## Purpose

Use this page as the reference list for the Crossplane section. Prefer these official sources when verifying examples, provider schemas, authentication behavior, operations, and production guidance.

## Crossplane official documentation

| Reference | Use it for |
| --- | --- |
| [Crossplane documentation](https://docs.crossplane.io/latest/) | Current Crossplane documentation entry point. |
| [What is new in Crossplane v2](https://docs.crossplane.io/latest/whats-new/) | Namespaced resources, v2 behavior, and upgrade context. |
| [Install Crossplane](https://docs.crossplane.io/latest/get-started/install/) | Helm installation and prerequisites. |
| [Get started with managed resources](https://docs.crossplane.io/latest/get-started/get-started-with-managed-resources/) | First managed-resource workflow. |
| [Managed resources](https://docs.crossplane.io/latest/managed-resources/managed-resources/) | Managed-resource fields, conditions, annotations, references, finalizers, provider configs, and management policies. |
| [Managed Resource Activation Policies](https://docs.crossplane.io/latest/managed-resources/managed-resource-activation-policies/) | Selectively activating provider resource APIs. |
| [Disabling unused managed resources](https://docs.crossplane.io/latest/guides/disabling-unused-managed-resources/) | Safe-start and activation-policy workflow. |
| [Providers](https://docs.crossplane.io/latest/packages/providers/) | Provider package installation, revisions, health, runtime configuration, and provider config types. |
| [Compositions](https://docs.crossplane.io/latest/composition/compositions/) | Composition model and composed-resource behavior. |
| [Composite Resource Definitions](https://docs.crossplane.io/latest/composition/composite-resource-definitions/) | XRD schema, API group, names, scope, and versions. |
| [Composition revisions](https://docs.crossplane.io/latest/composition/composition-revisions/) | How composition changes are versioned and rolled out. |
| [Function Patch and Transform](https://docs.crossplane.io/latest/guides/function-patch-and-transform/) | Patch-and-transform function input schema and examples. |
| [Crossplane CLI command reference](https://docs.crossplane.io/cli/latest/command-reference/) | `crossplane composition render`, project, dependency, and package commands. |
| [Crossplane with Argo CD](https://docs.crossplane.io/latest/guides/crossplane-with-argo-cd/) | GitOps integration, tracking, sync waves, health, and exclusions. |
| [Metrics](https://docs.crossplane.io/latest/guides/metrics/) | Prometheus-style metrics for Crossplane core, providers, and Upjet providers. |
| [Operations](https://docs.crossplane.io/latest/operations/operation/) | Run-to-completion function pipelines for maintenance and operational tasks. |
| [Troubleshoot Crossplane](https://docs.crossplane.io/latest/guides/troubleshoot-crossplane/) | Official diagnostic workflow. |
| [Import existing resources](https://docs.crossplane.io/latest/guides/import-existing-resources/) | Bringing existing external resources under Crossplane observation or management. |
| [Change logs](https://docs.crossplane.io/latest/guides/change-logs/) | Provider change-log feature and audit support. |
| [Upgrade Crossplane](https://docs.crossplane.io/latest/guides/upgrade-crossplane/) | Upgrade planning and supported procedures. |

## Upbound and provider references

| Reference | Use it for |
| --- | --- |
| [Upbound documentation](https://docs.upbound.io/) | Upbound platform and package documentation. |
| [Provider authentication](https://docs.upbound.io/manuals/packages/providers/authentication/) | Upbound OIDC, provider config examples, and provider authentication models. |
| [AWS access-key authentication](https://docs.upbound.io/manuals/packages/providers/aws-auth/aws-access-keys/) | Static access-key configuration for labs or specific controlled cases. |
| [AWS IRSA authentication](https://docs.upbound.io/manuals/packages/providers/aws-auth/aws-irsa/) | IRSA setup for EKS-hosted Crossplane providers. |
| [Upbound Marketplace](https://marketplace.upbound.io/) | Current provider, function, configuration package, and resource schema discovery. |
| [Upbound AWS S3 provider](https://marketplace.upbound.io/providers/upbound/provider-aws-s3) | S3 provider package, versions, and resource schemas. |
| [Upbound AWS provider family](https://marketplace.upbound.io/providers/upbound/provider-family-aws) | Shared AWS provider family and authentication APIs. |
| [Upjet repository](https://github.com/crossplane/upjet) | Provider-generation framework and implementation context. |
| [provider-upjet-aws authentication](https://github.com/crossplane-contrib/provider-upjet-aws/blob/main/AUTHENTICATION.md) | Provider AWS authentication behavior and supported credential sources. |

## AWS references

| Reference | Use it for |
| --- | --- |
| [EKS Pod Identity](https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html) | AWS-recommended EKS-native workload identity model, setup steps, benefits, and limitations. |
| [IAM Roles for Service Accounts](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html) | IRSA behavior, OIDC provider requirements, and service-account role mapping. |
| [EKS workload IAM overview](https://docs.aws.amazon.com/eks/latest/userguide/service-accounts.html) | Choosing workload identity mechanisms for Pods. |
| [EKS Pod Identity Agent](https://docs.aws.amazon.com/eks/latest/userguide/pod-id-agent-setup.html) | Pod Identity Agent installation and requirements. |
| [AWS CloudTrail](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html) | Auditing provider assume-role and resource API calls. |
| [AWS Organizations service control policies](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html) | Defense-in-depth guardrails outside Crossplane. |
| [AWS Config](https://docs.aws.amazon.com/config/latest/developerguide/WhatIsConfig.html) | Independent configuration recording and compliance checks. |

## Professional practice signals

These sources are useful for understanding how teams combine Crossplane with platform engineering and GitOps. Verify commands and APIs against official docs before copying examples.

| Reference | Use it for |
| --- | --- |
| [Platform engineering with Crossplane and Argo CD](https://platformengineering.org/blog/platform-engineering-with-crossplane-and-argocd) | Practice-oriented discussion of GitOps plus Crossplane workflows. |
| [Upbound GitOps with Flux and Crossplane](https://www.upbound.io/blog/gitopsify-infrastructure-xp) | GitOps infrastructure pattern with Crossplane and Flux. |
| [Crossplane provider security practices](https://blog.crossplane.io/enhancing-security-practices-with-crossplane-providers/) | Security model, provider credentials, and identity considerations. |

## Repository source notes

| Reference | Use it for |
| --- | --- |
| [Crossplane complete study guide source](../../sources/processed/crossplane-complete-study-guide.md) | Original processed source notes for Crossplane, Upbound, Upjet, AWS labs, GitOps, security, and troubleshooting. |

## Related links

- [Crossplane](README.md)
- [Professional operating model](professional-operating-model.md)
- [AWS resource workflow](aws-resource-workflow.md)
- [Back to Kubernetes index](../README.md)
- [Back to root index](../../README.md)
