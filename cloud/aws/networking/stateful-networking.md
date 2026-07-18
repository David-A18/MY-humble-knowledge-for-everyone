# Stateful networking

## Purpose

Use this page to understand AWS networking features where connection state changes security, routing, and troubleshooting.

## Stateful and stateless controls

| Control | Behavior | Design note |
| --- | --- | --- |
| Security group | Stateful filtering. | Return traffic for allowed connections is automatically allowed. |
| Network ACL | Stateless subnet filtering. | Inbound and outbound rules must both allow the traffic. |
| NAT Gateway | Tracks outbound flows for private subnet egress. | It is not a general inbound firewall. |
| AWS Network Firewall | Supports stateless and stateful inspection. | Symmetric routing matters for stateful inspection. |
| Gateway Load Balancer | Helps insert appliances into traffic paths. | Flow stickiness and routing symmetry are critical. |

## Troubleshooting sequence

1. Confirm the source, destination, protocol, and port.
2. Check security groups on both sides.
3. Check network ACL inbound and outbound rules, including ephemeral ports.
4. Verify route tables and appliance paths.
5. Use VPC Flow Logs when packet direction or action is unclear.

## Related links

- [Security groups](security-groups.md)
- [Stateful vs. stateless on AWS](../architecture/stateful-vs-stateless.md)
- [AWS VPC security groups documentation](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html)
- [AWS Network Firewall documentation](https://docs.aws.amazon.com/network-firewall/)
- [Back to AWS networking](README.md)
- [Back to AWS index](../README.md)
- [Back to root index](../../../README.md)
