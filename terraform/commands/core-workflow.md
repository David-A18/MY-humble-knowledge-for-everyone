# Core Terraform workflow

## Purpose

Document the standard command flow for making and reviewing Terraform changes.

## Command sequence

```bash
terraform fmt -recursive
terraform init
terraform validate
terraform plan
```

Expected validation output:

```text
Success! The configuration is valid.
```

## Apply changes

```bash
terraform apply
```

> [!IMPORTANT]
> Review the plan before applying. Confirm the target workspace, backend, and account context.

## Non-interactive validation for CI

```bash
terraform fmt -recursive -check
terraform init -backend=false
terraform validate
```

## Related links

- [Terraform CLI documentation](https://developer.hashicorp.com/terraform/cli)
- [Back to Terraform commands](README.md)
- [Back to Terraform index](../README.md)
- [Back to root index](../../README.md)
