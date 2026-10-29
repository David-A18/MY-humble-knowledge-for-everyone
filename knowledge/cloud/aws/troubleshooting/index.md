# AWS troubleshooting

Status: Initial outline

Diagnostic runbooks for AWS service and architecture issues.

## Expected content

- EC2 connectivity failures.
- Load balancer health check failures.
- IAM access denied errors.
- VPC routing problems.
- Unexpected cost spikes.

## Available focused route

- [AWS network connectivity](../networking/network-connectivity-troubleshooting.md) — separate DNS, routes, filtering, TLS, and API authorization, then choose the relevant evidence tool.

## First checks

- [ ] Confirm account, region, and resource identifiers.
- [ ] Check recent changes.
- [ ] Review CloudTrail or service logs where available.
- [ ] Capture exact error messages.

[Back to AWS index](../index.md) | [Back to root index](../../../../README.md)
