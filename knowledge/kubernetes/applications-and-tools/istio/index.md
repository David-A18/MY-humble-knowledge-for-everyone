# Istio authentication and authorization

Understand identity and enforcement first, then reproduce positive and negative security tests in a disposable mesh. The lab uses sidecar mode; ambient enforcement is explained separately.

## Learning path

Read in order, or choose a task from the table.

| Guide | Use it for |
| --- | --- |
| [Fundamentals and architecture](fundamentals.md) | Understand the mesh, Istiod, proxies, and historical terminology. |
| [Workload identity and mTLS](workload-identity-and-mtls.md) | Follow certificate issuance and peer authentication. |
| [JWT authentication and authorization](jwt-and-authorization.md) | Require verified tokens and authorize workloads. |
| [Sidecar and ambient enforcement](sidecar-and-ambient.md) | Place L4 and L7 policy at the correct proxy. |
| [Security lab](security-lab.md) | Test allowed, denied, missing-token, and plaintext requests. |
| [Troubleshooting and rollout](troubleshooting-and-rollout.md) | Diagnose failures and introduce policy safely. |

## Related links

- [Runnable example files](examples/index.md)

- [Back to parent index](../index.md)
- [Back to root index](../../../../README.md)
