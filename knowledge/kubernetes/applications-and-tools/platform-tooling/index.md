# Kubernetes platform tooling

A practical catalog of commonly encountered tools, organized by responsibility. This is a selection guide, not a measured popularity ranking. Each controller adds permissions, upgrades, and failure modes.

## Learning path

Read in order, or choose a task from the table.

| Guide | Use it for |
| --- | --- |
| [Choose Kubernetes platform tools](tool-selection.md) | Map operational needs to components and ownership. |
| [Helm and Kustomize](helm-and-kustomize.md) | Package applications and render environment overlays. |
| [Secret-management patterns](secret-management.md) | Choose a store, delivery mechanism, and rotation contract. |
| [External Secrets Operator](external-secrets-operator.md) | Reconcile external values into Kubernetes Secrets. |
| [Secrets Store CSI Driver](secrets-store-csi-driver.md) | Mount external secrets as files. |
| [Vault on Kubernetes](vault.md) | Use authentication, policies, leases, and dynamic credentials. |
| [SOPS and Sealed Secrets](gitops-secrets.md) | Keep encrypted configuration in Git. |
| [cert-manager](cert-manager.md) | Issue, renew, inspect, and troubleshoot certificates. |
| [Storage and snapshots](storage-and-snapshots.md) | Choose CSI drivers, persistent storage, and recovery mechanisms. |
| [DNS and gateways](dns-and-gateways.md) | Separate DNS records, ingress routing, and service meshes. |
| [Policy, security, and scaling](policy-security-and-scaling.md) | Choose admission, scanning, runtime detection, and scaling tools. |

## Related links

- [Back to parent index](../index.md)
- [Back to root index](../../../../README.md)
