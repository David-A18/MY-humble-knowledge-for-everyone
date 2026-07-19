# Apache APISIX

## Purpose

Use this page to understand Apache APISIX as an API gateway for Kubernetes and EKS environments.

## What it does

Apache APISIX is an API gateway. It receives HTTP, HTTPS, gRPC, and selected stream traffic before backend services and applies shared gateway behavior such as routing, TLS, authentication, rate limiting, traffic splitting, transformations, metrics, logs, and tracing.

In Kubernetes, APISIX can act as the implementation behind Ingress, Gateway API, or APISIX-specific custom resources.

## Mental model

Apache APISIX is a gateway data plane and policy engine. In Kubernetes, the APISIX Ingress Controller watches Kubernetes resources such as Gateway API resources or APISIX custom resources and configures APISIX Gateway.

| Area | What it does |
| --- | --- |
| Route | Matches requests and sends them to upstream services. |
| Upstream | Defines backend targets and load balancing. |
| Plugin | Adds policy such as auth, rate limiting, traffic shaping, or observability. |
| Consumer | Represents a caller identity for API-key or credential-based plugins. |
| Ingress Controller | Reconciles Kubernetes desired state into APISIX configuration. |

## How it works

```text
Client
  -> DNS
  -> cloud load balancer
  -> APISIX gateway Pods
  -> route match
  -> plugins
  -> upstream Kubernetes Service
  -> application Pods
```

The configuration path is separate:

```text
Git or kubectl
  -> Kubernetes API
  -> APISIX Ingress Controller
  -> APISIX gateway configuration
```

This separation matters during troubleshooting because route objects can exist in Kubernetes before they are accepted, programmed, and serving traffic.

## When APISIX fits

- You need Kubernetes ingress plus API gateway policies.
- Teams need route-level plugins for authentication, rate limiting, transformations, or traffic releases.
- You want Gateway API or APISIX CRDs to manage traffic through Kubernetes-native workflows.

## Example route shape

```text
Host: api.example.com
Path: /orders/*
Authentication: OIDC or API key
Rate limit: per consumer
Upstream: orders-service:8080
Telemetry: Prometheus metrics and request logs
```

What it does: shows the common gateway contract APISIX owns for one API route before the request reaches application code.

## Related links

- [APISIX architecture and deployment](apisix-architecture-and-deployment.md)
- [APISIX security, traffic, and observability](apisix-security-traffic-and-observability.md)
- [Gateway API and Ingress](gateway-api-and-ingress.md)
- [APISIX on EKS](../../cross-topic-guides/apisix-on-eks.md)
- [APISIX troubleshooting](../troubleshooting/apisix.md)
- [Apache APISIX Ingress Controller documentation](https://apisix.apache.org/docs/ingress-controller/)
- [Back to Kubernetes applications and tools](README.md)
- [Back to Kubernetes index](../README.md)
- [Back to root index](../../README.md)
