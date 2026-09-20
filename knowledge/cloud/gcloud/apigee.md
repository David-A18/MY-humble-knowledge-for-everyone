---
type: "Explanation"
title: "Apigee API management"
description: "Use this page to understand where Google Cloud Apigee fits, how its main objects work together, and what to check before using it as an API management platform."
tags: [cloud, gcloud, apigee]
status: draft
maturity: draft
audience: "Engineering learners and practitioners"
maintainer: "unassigned"
---

# Apigee API management

## Purpose

Use this page to understand where Google Cloud Apigee fits, how its main objects work together, and what to check before using it as an API management platform.

Apigee is for managing APIs as products, not only forwarding HTTP traffic. It sits between API consumers and backend services so teams can apply security, traffic control, transformations, analytics, developer onboarding, and lifecycle controls without embedding all of that logic in each backend.

## When to use this

- You need an API gateway with product, developer, app, and credential management.
- You need API policies such as API key validation, OAuth, quotas, rate limits, mediation, and fault handling.
- You need API analytics, developer onboarding, and reusable governance across many APIs.
- You need a hybrid model where the management plane is in Google Cloud and the runtime plane runs on supported Kubernetes infrastructure that you manage.

## Core model

| Concept | Meaning | Why it matters |
| --- | --- | --- |
| Apigee organization | Top-level Apigee container mapped to a Google Cloud project for Apigee X and hybrid. | Holds API proxies, environments, products, developers, apps, and shared resources. |
| Environment | Deployment target inside an Apigee organization. | API proxies must be deployed to an environment before they can receive traffic. |
| Environment group | Routing layer that maps hostnames to one or more environments. | Determines which hostname clients use for proxies in those environments. |
| API proxy | Managed facade between clients and backend targets. | Decouples the public API contract from backend service implementation. |
| ProxyEndpoint | Client-facing side of the API proxy. | Defines how clients call the API and where policies such as authentication and quotas usually start. |
| TargetEndpoint | Backend-facing side of the API proxy. | Defines how Apigee forwards traffic to the backend service. |
| Policy | Reusable Apigee unit for security, traffic, transformation, mediation, or extension behavior. | Keeps common API behavior declarative and consistent across proxies. |
| API product | Bundle of API resources exposed to app developers as a consumable product or tier. | Connects API access, quotas, scopes, approval, and app credentials. |
| Developer app | Registered client application that receives credentials for one or more API products. | Lets Apigee identify callers and enforce product-specific access. |

## Request flow

```text
client
  -> environment group hostname
  -> API proxy ProxyEndpoint
  -> request policies and flows
  -> TargetEndpoint
  -> backend service
  -> response policies and flows
  -> client
```

What it does: separates the client contract from the backend contract. The proxy can authenticate, authorize, throttle, transform, enrich, route, observe, and format traffic without requiring every backend team to reimplement those controls.

## Design decisions

| Decision | Choose this | When it fits |
| --- | --- | --- |
| Apigee managed runtime | Apigee in Google Cloud. | You want Google-managed API runtime operations and your backend connectivity model supports it. |
| Apigee hybrid | Google-hosted management plane with self-managed Kubernetes runtime plane. | You need runtime placement near private backends or in controlled infrastructure for compliance, latency, or network ownership. |
| API product per audience or tier | Separate products such as public, partner, internal, free, and premium. | Access level, quota, monetization, or support promises differ by consumer. |
| Shared flow | Reusable policy sequence for common behavior. | Many proxies need the same authentication, headers, error handling, logging, or threat protection. |
| Direct gateway only | Cloud gateway or ingress without Apigee product features. | You only need routing and basic edge controls, not developer onboarding or API product governance. |

## Operational workflow

1. Define the API contract and backend target.
2. Create an API proxy with a `ProxyEndpoint` and `TargetEndpoint`.
3. Attach policies close to the flow they protect, such as API key verification on the client-facing request path.
4. Deploy a proxy revision to a non-production environment.
5. Test with Apigee debug tools and backend logs.
6. Bundle exposed resources into an API product.
7. Register developers or app groups, create developer apps, and issue credentials.
8. Promote the proxy revision through environments with automation and approvals.
9. Monitor traffic, errors, latency, quota use, and backend behavior.

## Example API key protected proxy flow

```xml
<PreFlow name="PreFlow">
  <Request>
    <Step>
      <Name>Verify-API-Key</Name>
    </Step>
  </Request>
  <Response/>
</PreFlow>
```

What it does: runs an API key verification policy before the request reaches the target backend. The policy must be defined in the proxy and the calling app must have an approved key for an API product that includes the requested API resource.

> [!IMPORTANT]
> Registering apps and creating API products does not protect an API by itself. The proxy still needs policies such as `VerifyAPIKey`, OAuth token verification, quota, or spike arrest attached to the correct request flow.

## Automation and lifecycle

Apigee proxies are versioned as revisions. Teams usually automate import, deployment, undeployment, promotion, and environment-specific configuration through the Apigee API, Google Cloud tooling, or CI/CD pipelines.

Useful automation checks:

- Keep proxy bundles, shared flows, and environment configuration in version control.
- Separate environment-specific values from reusable proxy logic.
- Deploy immutable proxy revisions and promote tested revisions instead of editing live behavior manually.
- Validate that the target backend, certificates, service accounts, and network path are ready before promotion.
- Use least-privilege Google Cloud IAM and Apigee roles for deployment automation.

## Common failure modes

| Symptom | Likely cause | Next step |
| --- | --- | --- |
| Client receives `401` or `403` | Missing, revoked, unapproved, or invalid app credential. | Check the developer app, API product approval, and verification policy variables. |
| Client receives quota errors | API product or operation quota is reached and enforced by a quota policy. | Confirm whether the quota is product-level or operation-level and whether the caller is on the right product tier. |
| Proxy deploys but traffic does not route | Environment group hostname, deployment target, DNS, or TLS mapping is wrong. | Check the proxy revision deployment, environment group hostname, certificate, and client URL. |
| Backend receives unexpected payload | Transformation or mediation policy changed the request. | Use debug tracing to inspect flow variables and request content at each policy step. |
| Hybrid runtime does not receive updates | Runtime plane cannot synchronize with the control plane. | Check hybrid synchronizer health, Kubernetes resources, service accounts, and network connectivity. |

## Related links

- [Official Apigee documentation](https://cloud.google.com/apigee/docs)
- [Understanding APIs and API proxies](https://cloud.google.com/apigee/docs/api-platform/fundamentals/understanding-apis-and-api-proxies)
- [Understanding Apigee organizations](https://cloud.google.com/apigee/docs/api-platform/fundamentals/organization-structure)
- [About environments and environment groups](https://cloud.google.com/apigee/docs/api-platform/fundamentals/environments-overview)
- [Managing API products](https://cloud.google.com/apigee/docs/api-platform/publish/create-api-products)
- [Apigee API reference](https://cloud.google.com/apigee/docs/reference/apis/apigee/rest)
- [What is Apigee hybrid?](https://cloud.google.com/apigee/docs/hybrid/latest/what-is-hybrid)
- [Back to Google Cloud index](index.md)
- [Back to cloud index](../index.md)
- [Back to root index](../../../README.md)
