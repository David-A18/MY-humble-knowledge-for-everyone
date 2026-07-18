# APISIX troubleshooting

## Purpose

Diagnose Apache APISIX and APISIX Ingress Controller failures in Kubernetes.

## First checks

| Symptom | Check | Likely area |
| --- | --- | --- |
| Route returns 404 | Gateway, route, and APISIX route status. | Match rules or reconciliation. |
| Backend returns 503 | Service endpoints and upstream health. | Service discovery or workload readiness. |
| Plugin does not apply | Plugin config and route attachment. | Policy placement or controller sync. |
| TLS fails | Certificate, SNI, listener, and secret. | Gateway or certificate configuration. |

## Diagnostic commands

```bash
kubectl get gateway,httproute,ingress -A
kubectl get pods,svc,endpointslices -n <namespace>
kubectl logs -n <apisix-namespace> deployment/<apisix-ingress-controller>
```

What it does: checks routing resources, backend endpoints, and controller reconciliation logs.

## Related links

- [Apache APISIX](../applications-and-tools/apache-apisix.md)
- [Gateway API and Ingress](../applications-and-tools/gateway-api-and-ingress.md)
- [Apache APISIX Ingress Controller documentation](https://apisix.apache.org/docs/ingress-controller/)
- [Back to Kubernetes troubleshooting](README.md)
- [Back to Kubernetes index](../README.md)
- [Back to root index](../../README.md)
