# Cross-topic guides

Guides that connect multiple engineering areas into practical workflows.

## Quick paths

| Topic | Start here | Related foundations |
| --- | --- | --- |
| APISIX on EKS | [APISIX on EKS](apisix-on-eks.md) | [What Apache APISIX does for an API](../kubernetes/applications-and-tools/apache-apisix.md), [How the gateway and controller fit together](../kubernetes/applications-and-tools/apisix-architecture-and-deployment.md), [How APISIX policies shape one request](../kubernetes/applications-and-tools/apisix-security-traffic-and-observability.md). |
| Flux or GitOps on EKS | [GitOps on EKS](gitops-on-eks.md) | [GitOps](../kubernetes/applications-and-tools/gitops.md), [Flux](../kubernetes/applications-and-tools/flux.md), [How Flux applies a HelmRelease from Git](../kubernetes/applications-and-tools/flux-reconciliation-and-helm.md). |
| Akamai, CloudFront, or CDN in front of EKS | [CDN in front of EKS](cdn-in-front-of-eks.md) | [Akamai vs. CloudFront](../cloud/edge/akamai-vs-cloudfront.md), [CDN caching and origin protection](../cloud/edge/cdn-caching-and-origin-protection.md), [Multi-CDN operations](../cloud/edge/multi-cdn-operations.md). |
| First local learning route | [Local deployment learning path](local-deployment-learning-path.md) | [Start here](../start-here.md), [Kubernetes fundamentals](../kubernetes/fundamentals/index.md), [Git undo and recovery](../git/troubleshooting/undo-and-recovery.md). |

| Guide | Coverage | Focus |
| --- | --- | --- |
| [Terraform on AWS](terraform-on-aws.md) | Draft | Understand the boundaries between the AWS provider, identity with its account and region, resources, and backend state. |
| [Local deployment learning path](local-deployment-learning-path.md) | Draft | Learn how a local Deployment and Service work, diagnose a failed image rollout, and recover. |
| [Kubernetes on AWS](kubernetes-on-aws.md) | Draft | Map Kubernetes objects to AWS compute, networking, identity, and storage. |
| [GitHub Actions with Terraform](github-actions-with-terraform.md) | Draft | Tell pull request validation, plan, and gated apply apart, and see why plan files are sensitive. |
| [GitHub Actions with Kubernetes](github-actions-with-kubernetes.md) | Draft | Understand what a deployment job does, what Kubernetes controllers do afterwards, and what a green run does not prove. |
| [Deploying to EKS](deploying-to-eks.md) | Draft | Follow deployer access, image pull, rollout, and user-path checks. |
| [EKS operations](eks-operations.md) | Draft | Locate the first failed boundary across AWS, Kubernetes, workload IAM, and the user path. |
| [CDN in front of EKS](cdn-in-front-of-eks.md) | Draft | Follow cache hits and misses through CloudFront, an ALB, and the EKS application's target mode. |
| [APISIX on EKS](apisix-on-eks.md) | Draft | Follow AWS entry, APISIX route configuration, gateway traffic, and backend health. |
| [EKS to MSK applications](eks-to-msk-applications.md) | Draft | See the network, identity, and processing gates from an EKS Pod to MSK. |
| [Crossplane on AWS](crossplane-on-aws.md) | Draft | Follow a resource request through Crossplane into AWS, including identity, ownership, and recovery boundaries. |
| [GitOps on EKS](gitops-on-eks.md) | Draft | Follow a Git change through GitOps, Kubernetes, and AWS controllers on EKS. |
| [EKS workload identity](eks-workload-identity.md) | Draft | Understand how Pods get temporary AWS credentials through a service account, and choose IRSA or EKS Pod Identity from a workload's conditions. |
| [EKS tooling cluster architecture](eks-tooling-cluster-architecture.md) | Draft | Decide when central GitOps helps and how target access and recovery work. |
| [Observability stack](observability-stack.md) | Draft | Understand which questions metrics, logs, and traces answer, and how an SLO and alert turn signals into a decision. |
| [End-to-end deployment](end-to-end-deployment.md) | Draft | Follow the delivery chain from reviewed change to user check and recovery, and what each gate does and does not prove. |

[Back to root index](../../README.md)
