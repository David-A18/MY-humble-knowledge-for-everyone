# Kubernetes on AWS

Status: Initial outline

## Purpose

Collect guidance for running Kubernetes workloads on AWS infrastructure.

## Expected content

- EKS cluster considerations.
- AWS load balancer integration.
- IAM and workload identity.
- Networking and private cluster access.
- Storage integrations.

## Operational questions

- Which workloads require public ingress?
- Which AWS services does the workload need to access?
- How are cluster upgrades planned and tested?
- Which logs and metrics are required for operations?

## Related links

- [Amazon EKS documentation](https://docs.aws.amazon.com/eks/)
- [Kubernetes index](../kubernetes/README.md)
- [AWS index](../aws/README.md)
- [Back to cross-topic guides](README.md)
- [Back to root index](../README.md)
