---
type: Explanation
title: Terraform on AWS
description: Set up Terraform for AWS so every run targets the right account and region, keeps state safe, and uses least-privilege credentials.
tags: [cross-topic-guides, terraform-on-aws, terraform, aws]
status: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
  - id: aws-provider
    resource: https://registry.terraform.io/providers/hashicorp/aws/latest/docs
    title: Terraform AWS provider documentation
  - id: s3-backend
    resource: https://developer.hashicorp.com/terraform/language/backend/s3
    title: Terraform S3 backend
  - id: tf-plan
    resource: https://developer.hashicorp.com/terraform/cli/commands/plan
    title: Terraform plan command
---

# Terraform on AWS

Terraform manages AWS through the AWS provider, a plugin that calls AWS APIs for
you. Most AWS mistakes with Terraform are not syntax errors. They are changes
made in the wrong account or region, state that two people overwrite, or
credentials with far more power than the change needs. This page shows the
setup that prevents those mistakes.

## A safe starting configuration

```hcl
terraform {
  required_version = ">= 1.10"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0" # pin to the major version you tested
    }
  }

  backend "s3" {
    bucket       = "example-terraform-state"
    key          = "network/prod/terraform.tfstate"
    region       = "eu-west-1"
    encrypt      = true
    use_lockfile = true # S3-native state locking
  }
}

provider "aws" {
  region              = "eu-west-1"
  allowed_account_ids = ["111122223333"]

  default_tags {
    tags = {
      Owner       = "platform-team"
      Environment = "prod"
      ManagedBy   = "terraform"
    }
  }
}
```

What it does:

- **Pins versions.** `required_providers` limits which AWS provider versions
  may be installed, and the dependency lock file records the exact one. See
  [providers and dependency locking](../terraform/fundamentals/providers-and-dependency-locking.md).
- **Stores state remotely, encrypted and locked.** The S3 backend keeps one
  shared state file, and `use_lockfile` stops two runs from writing it at the
  same time.[^s3-backend]
- **Refuses the wrong account.** `allowed_account_ids` makes Terraform stop if
  the credentials belong to a different AWS account.[^aws-provider]
- **Tags everything.** `default_tags` adds owner and environment tags to every
  resource that supports tags, which helps with cost reports and clean-up.

## Separate environments and blast radius

Give each environment, and usually each AWS account, its own state file and
its own credentials. A mistake in `dev` then cannot touch `prod`, and a plan
for one environment stays small enough to review. Compare the options in
[environment layouts](../terraform/project-structure/environment-layouts.md)
and [CLI workspaces](../terraform/fundamentals/cli-workspaces-and-environment-isolation.md).

## Credentials for people and automation

| Who runs Terraform | Recommended credentials |
| --- | --- |
| A person, for learning or a sandbox | Short-lived credentials from AWS IAM Identity Center, never long-lived access keys. |
| CI pull requests | An OIDC-assumed role with read-only permissions, for plans only. |
| CI after merge | A separate OIDC-assumed apply role, limited to the resources that stack manages, behind an approval. |

See [AWS governance and human access](../cloud/aws/governance-and-access/index.md)
for people's access and [GitHub Actions with Terraform](github-actions-with-terraform.md)
for the pipeline.

## Review before every apply

Read the whole plan before applying.[^tf-plan] Look hardest at:

- anything Terraform will **destroy or replace**;
- **IAM** policies, roles, and trust relationships;
- **network** paths: security groups, route tables, and public access;
- **data stores**, where replacement can mean data loss;
- changes you did not expect, which often mean drift or the wrong workspace.

> [!WARNING]
> `terraform apply` changes real AWS resources and can create costs. Start in a
> sandbox account with a budget alert, and run `terraform destroy` on practice
> resources when you finish.

## Related links

- [Terraform fundamentals](../terraform/fundamentals/terraform-fundamentals.md)
- [Terraform local state lifecycle](../terraform/local-state-lifecycle.md) - practice without an AWS account.
- [Remote backends and locking](../terraform/fundamentals/remote-backends-and-locking.md)
- [AWS FinOps](../cloud/aws/finops/index.md) - budgets and cost alerts.
- [Back to cross-topic guides](index.md)

[^aws-provider]: [Terraform AWS provider documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
[^s3-backend]: [Terraform S3 backend](https://developer.hashicorp.com/terraform/language/backend/s3)
[^tf-plan]: [Terraform plan command](https://developer.hashicorp.com/terraform/cli/commands/plan)
