# Terraform on AWS

Status: Initial outline

## Purpose

Capture practical patterns for managing AWS infrastructure with Terraform.

## Expected content

- AWS provider configuration.
- Remote state backend patterns.
- IAM permissions for Terraform automation.
- Account and region targeting.
- Plan review and apply safety.

## Starter checklist

- [ ] Confirm AWS account and region.
- [ ] Use a remote backend for shared infrastructure.
- [ ] Lock provider versions.
- [ ] Run `terraform fmt`, `terraform validate`, and `terraform plan` before apply.
- [ ] Review IAM and networking changes carefully.

## Related links

- [Terraform AWS provider documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Terraform index](../terraform/README.md)
- [AWS index](../aws/README.md)
- [Back to cross-topic guides](README.md)
- [Back to root index](../README.md)
