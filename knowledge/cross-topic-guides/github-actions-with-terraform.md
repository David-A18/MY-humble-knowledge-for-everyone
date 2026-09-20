---
type: "Explanation"
title: "GitHub Actions with Terraform"
description: "Define a safe CI workflow for formatting, validating, and reviewing Terraform changes with GitHub Actions."
tags: [cross-topic-guides, github-actions-with-terraform]
status: draft
maturity: initial-outline
audience: "Engineering learners and practitioners"
maintainer: "unassigned"
---

# GitHub Actions with Terraform

Status: Initial outline

## Purpose

Define a safe CI workflow for formatting, validating, and reviewing Terraform changes with GitHub Actions.

## Expected content

- Pull request validation.
- Provider setup.
- Backend access model.
- Plan artifacts and review comments.
- Apply approval flow.

## Starter workflow sequence

1. Check out the repository.
2. Install Terraform.
3. Run `terraform fmt -recursive -check`.
4. Run `terraform init`.
5. Run `terraform validate`.
6. Run `terraform plan` for reviewed environments.

## Related links

- [GitHub Actions documentation](https://docs.github.com/actions)
- [Terraform CLI documentation](https://developer.hashicorp.com/terraform/cli)
- [Back to cross-topic guides](index.md)
- [Back to root index](../../README.md)
