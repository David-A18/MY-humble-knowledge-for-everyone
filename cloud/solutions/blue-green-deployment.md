# Blue-green deployment

## Purpose

Use this page to understand what blue-green deployment means, what kind of cloud solution it is, how to recognize it in real environments, and which services usually participate.

## Short definition

Blue-green deployment is a release strategy where two production-capable environments exist at the same time:

- **Blue** is the environment currently receiving production traffic.
- **Green** is the environment with the new application version.

After the green environment passes health checks, smoke tests, and monitoring checks, traffic moves from blue to green. If the new version fails, traffic can move back to blue while blue is still available.

Blue-green deployment is not one specific cloud product. It is an application delivery and reliability pattern implemented with compute, traffic routing, health checks, deployment automation, and observability.

## What kind of solution is it?

| Category | Meaning |
| --- | --- |
| Release strategy | It controls how a new application version reaches users. |
| Availability pattern | It reduces downtime by keeping the old version available during the release. |
| Rollback pattern | It keeps a previous known-good environment ready for fast fallback. |
| Traffic management pattern | It depends on a router, load balancer, gateway, service mesh, DNS record, or platform traffic-splitting feature. |

Blue-green deployment is usually part of a CI/CD and platform architecture. It is most useful when the application can run two versions side by side and production traffic can be redirected without changing clients.

## When to use it

- You need low-downtime releases for a user-facing service.
- You want to test a new version in a production-like environment before full cutover.
- You need a fast rollback path after deployment.
- The application is mostly stateless, or state changes are backward-compatible.
- The extra temporary infrastructure cost is acceptable.

Do not choose blue-green deployment just because it sounds safer. For small internal services, a rolling update may be enough. For high-risk behavior changes, a canary release with small traffic percentages may be safer than an immediate full swap.

## How it works

1. Build and publish a new artifact, such as a container image, VM image, package, or function version.
2. Deploy the artifact to the green environment without replacing blue.
3. Run readiness checks, smoke tests, synthetic checks, and dependency checks against green.
4. Shift traffic from blue to green through a controlled routing layer.
5. Watch errors, latency, saturation, business metrics, and logs during the bake period.
6. Keep blue available until the new version is accepted.
7. Remove or repurpose blue only after rollback risk is low.

## Services involved

| Layer | Common services or resources | What to look for |
| --- | --- | --- |
| Source and CI/CD | GitHub Actions, Azure DevOps, AWS CodePipeline, Google Cloud Deploy, Jenkins, Argo CD, Flux | Pipeline stages named deploy, smoke test, promote, swap, or rollback. |
| Artifact storage | Amazon ECR, Azure Container Registry, Google Artifact Registry, VM image galleries, package registries | Two deployable versions available at the same time. |
| Compute runtime | ECS services and task sets, EKS or Kubernetes Deployments, App Service slots, Azure Container Apps revisions, Cloud Run revisions, EC2 or VM scale sets, Lambda versions | Old and new runtime groups exist side by side. |
| Traffic routing | Application Load Balancer, Network Load Balancer, CodeDeploy, Route 53, Azure Front Door, Azure Traffic Manager, Application Gateway, Cloud Load Balancing, Kubernetes Service, Ingress, Gateway API, service mesh | Routing rules, target groups, weights, selectors, slots, or revision traffic split between versions. |
| Health and release gates | Load balancer health checks, readiness probes, CloudWatch alarms, Azure Monitor alerts, Cloud Monitoring metrics, synthetic tests | Automated checks decide whether to continue, stop, or roll back. |
| Configuration and secrets | Parameter Store, Secrets Manager, Azure Key Vault, Google Secret Manager, Kubernetes Secrets and ConfigMaps | Both environments can read compatible configuration without sharing unsafe mutable state. |
| Data layer | RDS, DynamoDB, Azure SQL, Cosmos DB, Cloud SQL, Spanner, MongoDB, Kafka, queues, caches | Schema and message changes are compatible with both blue and green during the transition. |

## How to know you are seeing blue-green deployment

You are probably looking at blue-green deployment when several of these signals are true:

- There are two production-sized or production-capable environments for the same application.
- The names include `blue`, `green`, `stable`, `candidate`, `active`, `inactive`, `slot`, `revision`, `task-set`, or `target-group`.
- One public endpoint, load balancer, gateway, or DNS name can route to either version.
- The release process includes a traffic switch, slot swap, selector change, traffic weight change, or target group change.
- The previous version is intentionally kept alive after the new version starts receiving traffic.
- Rollback means routing traffic back to the previous environment, not rebuilding the old application.
- Deployment dashboards show two versions during the release window.

You are probably not looking at blue-green deployment when a single Deployment, service, or VM group is updated in place and old instances are removed gradually as new instances become ready. That is usually a rolling deployment.

## Provider examples

| Platform | Common implementation |
| --- | --- |
| AWS ECS | ECS service with blue-green deployment through CodeDeploy, task sets, a load balancer, and traffic shifting. |
| AWS EC2 | Two Auto Scaling groups or instance fleets behind a load balancer, with traffic moved between target groups or DNS records. |
| AWS Lambda | Function versions and aliases with traffic shifting, usually managed by CodeDeploy or deployment tooling. |
| Azure App Service | Production and staging deployment slots, then a slot swap when the new version is ready. |
| Azure Container Apps | Revisions, revision labels, and traffic weights representing blue and green versions. |
| Google Cloud Run | Immutable revisions with traffic split or full traffic migration between old and new revisions. |
| Google Kubernetes Engine or Kubernetes | Separate blue and green Deployments or clusters, with traffic controlled by a Service selector, Ingress, Gateway API, service mesh, or load balancer. |

## Common designs

### Load balancer with two target groups

```text
users -> dns -> load balancer -> blue target group -> current version
                          \-> green target group -> new version
```

What it shows: the public endpoint stays stable while the routing layer changes which backend group receives production traffic.

### Kubernetes service switch

```yaml
apiVersion: v1
kind: Service
metadata:
  name: checkout
spec:
  selector:
    app: checkout
    release: blue
  ports:
    - port: 80
      targetPort: 8080
```

What it does: routes service traffic only to Pods labeled `release: blue`. A blue-green switch can point the selector, gateway route, or mesh route to green after validation.

> [!IMPORTANT]
> In production Kubernetes systems, prefer a release controller, GitOps workflow, service mesh, Gateway API implementation, or ingress controller that can make the traffic change auditable and reversible. Manual selector edits are easy to understand but risky in shared environments.

### Revision traffic split

```text
checkout-v1: 100%
checkout-v2:   0%

after validation:
checkout-v1:   0%
checkout-v2: 100%
```

What it shows: platforms such as Cloud Run or Azure Container Apps can keep immutable revisions and move traffic by changing revision weights.

## Decision checklist

Use blue-green deployment when all of these are true:

- Users can reach the application through a stable routing layer.
- The old and new versions can run at the same time.
- Database schema changes are backward-compatible.
- Background workers, queues, scheduled jobs, and consumers will not double-process work.
- Health checks validate real dependencies, not only process liveness.
- Logs, metrics, and traces include version or environment labels.
- Rollback is tested and documented.
- The team accepts temporary duplicate capacity cost.

## Common failure modes

| Symptom | Likely cause | Next step |
| --- | --- | --- |
| Green passes health checks but fails real traffic | Health checks are too shallow. | Add synthetic checks that hit dependencies and critical user paths. |
| Rollback fails after a database migration | Schema change is not backward-compatible. | Use expand-and-contract migrations so both versions can run together. |
| Some users stay on the old version unexpectedly | Session affinity, DNS caching, client caching, or long-lived connections. | Check routing method, TTLs, sticky sessions, and connection draining. |
| Both versions process the same queue messages or scheduled jobs | Worker ownership is not part of the release plan. | Gate worker startup, isolate queues, or use idempotency and leader election. |
| Costs spike during release windows | Blue and green both run full capacity. | Plan temporary capacity, autoscaling limits, and cleanup timing. |

## Official references

- [AWS CodeDeploy blue-green deployments](https://docs.aws.amazon.com/codedeploy/latest/userguide/welcome.html)
- [Amazon ECS blue-green deployments](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-type-blue-green.html)
- [Azure Container Apps blue-green deployment](https://learn.microsoft.com/en-us/azure/container-apps/blue-green-deployment)
- [Azure App Service deployment best practices](https://learn.microsoft.com/en-us/azure/app-service/deploy-best-practices)
- [Cloud Run rollbacks, gradual rollouts, and traffic migration](https://cloud.google.com/run/docs/rollouts-rollbacks-traffic-migration)
- [Kubernetes Service](https://kubernetes.io/docs/concepts/services-networking/service/)
- [Kubernetes Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/)

## Related links

- [Cloud solutions](README.md)
- [Cloud index](../README.md)
- [End-to-end deployment](../../cross-topic-guides/end-to-end-deployment.md)
- [GitHub Actions with Kubernetes](../../cross-topic-guides/github-actions-with-kubernetes.md)
- [Back to root index](../../README.md)
