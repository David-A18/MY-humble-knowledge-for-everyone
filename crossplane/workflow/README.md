# Crossplane workflow

## Purpose

Show the graphical workflow Crossplane follows when deploying infrastructure directly through managed resources or indirectly through a custom platform API.

## Direct managed resource workflow

```mermaid
flowchart TD
    user["User or GitOps controller"]
    api["Kubernetes API server"]
    mr["Managed resource\nBucket.s3.aws.m.upbound.io"]
    provider["Crossplane provider controller"]
    external["External API\nAWS S3"]
    status["Resource status\nReady and Synced conditions"]

    user -->|"kubectl apply"| api
    api -->|"stores desired state"| mr
    provider -->|"watches managed resources"| mr
    provider -->|"create, observe, update, delete"| external
    external -->|"actual state and errors"| provider
    provider -->|"updates status and events"| status
    status --> api
```

What happens:

1. A user applies a provider-specific managed resource.
2. Kubernetes stores the object like any other custom resource.
3. The provider controller watches that object.
4. The provider calls the external API.
5. Crossplane updates status, conditions, events, and connection details where supported.

This workflow is close to using a cloud-provider SDK through Kubernetes objects.

## Composition workflow

```mermaid
flowchart TD
    platform["Platform team"]
    xrd["XRD\nDefines custom API schema"]
    comp["Composition\nDefines implementation"]
    function["Composition Function\nGenerates desired resources"]
    developer["Developer or service team"]
    xr["XR\nAppBucket instance"]
    composed["Composed resources\nBucket, Secret, IAM, Deployment"]
    providers["Provider controllers"]
    cloud["External infrastructure"]
    ready["XR Ready condition"]

    platform --> xrd
    platform --> comp
    comp --> function
    developer -->|"creates platform API object"| xr
    xrd -. "defines schema for" .-> xr
    comp -. "matches kind and API version" .-> xr
    xr -->|"observed by Crossplane"| function
    function -->|"returns desired resources"| composed
    providers -->|"reconcile managed resources"| composed
    providers -->|"call external APIs"| cloud
    cloud -->|"observed state"| providers
    composed -->|"readiness feeds"| ready
```

What happens:

1. The platform team defines an XRD and at least one matching Composition.
2. A developer creates an XR using the custom API from the XRD.
3. Crossplane selects a matching Composition.
4. Crossplane runs the Composition function pipeline.
5. The pipeline returns desired composed resources.
6. Crossplane applies those resources to the Kubernetes API.
7. Provider controllers reconcile managed resources into external infrastructure.
8. Crossplane reports status through the XR.

This workflow is the main platform self-service pattern.

## Terraform plan/apply compared with Crossplane reconciliation

```mermaid
flowchart LR
    subgraph terraform["Terraform workflow"]
        tfcode["HCL configuration"]
        tfplan["terraform plan"]
        tfstate["Terraform state"]
        tfapply["terraform apply"]
        tfcloud["Cloud APIs"]
        tfcode --> tfplan
        tfstate --> tfplan
        tfplan --> tfapply
        tfapply --> tfcloud
        tfapply --> tfstate
    end

    subgraph crossplane["Crossplane workflow"]
        yaml["Kubernetes YAML"]
        k8sapi["Kubernetes API"]
        controller["Continuous controllers"]
        cpcloud["Cloud APIs"]
        cpstatus["Status and events"]
        yaml --> k8sapi
        k8sapi --> controller
        controller --> cpcloud
        cpcloud --> controller
        controller --> cpstatus
    end
```

The key difference is timing. Terraform calculates and applies a change when the workflow runs. Crossplane keeps watching resources and reconciling them after the initial request.

## Failure workflow

```mermaid
flowchart TD
    xr["XR or managed resource"]
    controller["Crossplane/provider controller"]
    api["External API"]
    condition["Synced=False or Ready=False"]
    events["Kubernetes events"]
    logs["Controller logs"]
    fix["Fix spec, credentials, quota, policy, or external conflict"]

    xr --> controller
    controller --> api
    api -->|"error"| controller
    controller --> condition
    controller --> events
    controller --> logs
    condition --> fix
    events --> fix
    logs --> fix
    fix --> xr
```

Useful checks:

```bash
kubectl get managed
kubectl describe <kind> <name> -n <namespace>
kubectl get events -n <namespace> --sort-by=.lastTimestamp
kubectl -n crossplane-system logs deploy/crossplane
kubectl -n crossplane-system get pods
```

What it does: starts from resource health, then uses describe output, events, and controller logs to find provider errors.

## Related links

- [Crossplane fundamentals](../fundamentals/README.md)
- [Crossplane examples](../examples/README.md)
- [XRDs and Compositions](../xrd-and-compositions/README.md)
- [Terraform vs Crossplane](../comparison/terraform-vs-crossplane.md)
- [Crossplane composition documentation](https://docs.crossplane.io/latest/composition/)
- [Back to Crossplane index](../README.md)
- [Back to root index](../../README.md)
