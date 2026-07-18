# Cost allocation tags

## Purpose

Use consistent tags to support AWS cost allocation, ownership, and operational reporting.

## Common tag dimensions

| Tag | Purpose |
| --- | --- |
| `owner` | Team or person responsible for the resource. |
| `environment` | Environment such as development, staging, or production. |
| `application` | Product, service, or workload name. |
| `cost-center` | Finance allocation target. |
| `managed-by` | Tool or process that manages the resource, such as Terraform. |

> [!IMPORTANT]
> Tag names and required values should be documented and enforced consistently. Cost allocation is only useful when the tagging standard is followed.

## Starter checklist

- [ ] Define required tags.
- [ ] Apply tags through infrastructure as code where possible.
- [ ] Review untagged spend regularly.
- [ ] Align tags with reporting needs before dashboards are built.

## Related links

- [AWS cost allocation tags documentation](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html)
- [Back to AWS FinOps](README.md)
- [Back to AWS index](../README.md)
- [Back to root index](../../../README.md)
