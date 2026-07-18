# Apache APISIX in Kubernetes and AWS EKS

> A detailed study guide to API gateways, Apache APISIX, Kubernetes Ingress and Gateway API, traffic management, security, observability, GitOps, AWS integration, production design, and troubleshooting.

**Research snapshot:** 18 July 2026  
**Documentation versions reviewed:** Apache APISIX **3.17** and APISIX Ingress Controller **2.1.0**  
**Audience:** Cloud engineers, Kubernetes administrators, platform engineers, DevOps engineers, and solution architects.

---

## Table of contents

1. [The correct term: APISIX, “API-six,” APIG and API Gateway](#1-the-correct-term-apisix-api-six-apig-and-api-gateway)
2. [What problem does an API gateway solve?](#2-what-problem-does-an-api-gateway-solve)
3. [What Apache APISIX is](#3-what-apache-apisix-is)
4. [The essential mental model](#4-the-essential-mental-model)
5. [How APISIX is built](#5-how-apisix-is-built)
6. [Control plane, data plane and configuration flow](#6-control-plane-data-plane-and-configuration-flow)
7. [APISIX deployment modes](#7-apisix-deployment-modes)
8. [Core APISIX objects](#8-core-apisix-objects)
9. [How an incoming request is processed](#9-how-an-incoming-request-is-processed)
10. [APISIX and Kubernetes](#10-apisix-and-kubernetes)
11. [Ingress API, Gateway API and APISIX CRDs](#11-ingress-api-gateway-api-and-apisix-crds)
12. [Gateway API resource model and organizational roles](#12-gateway-api-resource-model-and-organizational-roles)
13. [APISIX Ingress Controller resources](#13-apisix-ingress-controller-resources)
14. [Service discovery and load balancing](#14-service-discovery-and-load-balancing)
15. [Plugins and policy enforcement](#15-plugins-and-policy-enforcement)
16. [Authentication, authorization and consumers](#16-authentication-authorization-and-consumers)
17. [Rate limiting and protection against overload](#17-rate-limiting-and-protection-against-overload)
18. [TLS, HTTPS, SNI and mTLS](#18-tls-https-sni-and-mtls)
19. [Traffic management and release strategies](#19-traffic-management-and-release-strategies)
20. [Observability: metrics, logs and traces](#20-observability-metrics-logs-and-traces)
21. [APISIX on Amazon EKS](#21-apisix-on-amazon-eks)
22. [A complete EKS reference architecture](#22-a-complete-eks-reference-architecture)
23. [Local Kubernetes lab](#23-local-kubernetes-lab)
24. [Practical application example](#24-practical-application-example)
25. [Gateway API manifests](#25-gateway-api-manifests)
26. [Adding rate limiting](#26-adding-rate-limiting)
27. [Adding API-key authentication](#27-adding-api-key-authentication)
28. [Adding HTTPS](#28-adding-https)
29. [Adding a canary release](#29-adding-a-canary-release)
30. [Exposing APISIX through an AWS NLB](#30-exposing-apisix-through-an-aws-nlb)
31. [GitOps with Flux or Argo CD](#31-gitops-with-flux-or-argo-cd)
32. [Production security recommendations](#32-production-security-recommendations)
33. [High availability and scalability](#33-high-availability-and-scalability)
34. [Operations, upgrades and disaster recovery](#34-operations-upgrades-and-disaster-recovery)
35. [Troubleshooting methodology](#35-troubleshooting-methodology)
36. [Common failure scenarios](#36-common-failure-scenarios)
37. [APISIX compared with related technologies](#37-apisix-compared-with-related-technologies)
38. [When APISIX is a good choice](#38-when-apisix-is-a-good-choice)
39. [When APISIX may be unnecessary](#39-when-apisix-may-be-unnecessary)
40. [Suggested learning path](#40-suggested-learning-path)
41. [Glossary](#41-glossary)
42. [Official references](#42-official-references)

---

# 1. The correct term: APISIX, “API-six,” APIG and API Gateway

The term you heard was most likely **Apache APISIX**, pronounced approximately **“API-six.”**

Several names in this area sound similar:

| Term | What it means |
|---|---|
| **API** | An Application Programming Interface: a contract through which one application communicates with another. |
| **API Gateway** | An architectural component that receives API traffic and applies routing, security, traffic and observability policies. |
| **APIG** | An informal abbreviation for “API Gateway.” In an AWS conversation it can also refer to Amazon API Gateway. |
| **Apache APISIX** | A specific open-source, cloud-native API gateway. |
| **API7** | A commercial company and product ecosystem closely associated with Apache APISIX. It is not the name of the Apache project. |
| **Kubernetes Ingress** | A Kubernetes API for basic external HTTP/HTTPS routing. It requires an implementation called an Ingress Controller. |
| **Kubernetes Gateway API** | A newer family of Kubernetes networking APIs such as `GatewayClass`, `Gateway` and `HTTPRoute`. |
| **Kubernetes API server** | The Kubernetes control-plane endpoint used by `kubectl`, controllers and operators. It is unrelated to the API-gateway role. |

The most important correction is:

> **APISIX is not an individual business API. It is gateway software that manages access to many APIs and services.**

For example, `orders-service` exposes an API. APISIX stands in front of that API and decides whether, where and how a request is forwarded.

---

# 2. What problem does an API gateway solve?

Imagine a Kubernetes cluster containing these microservices:

```text
users-service
catalog-service
orders-service
payments-service
shipping-service
```

Without an API gateway, a client might need to know multiple endpoints:

```text
users.example.com
catalog.example.com
orders.example.com
payments.example.com
shipping.example.com
```

Each service might independently implement:

- TLS handling
- JWT validation
- API-key validation
- CORS rules
- rate limiting
- request logging
- trace propagation
- IP restrictions
- retry behavior
- request and response transformations

That leads to duplicated code and inconsistent policies.

An API gateway provides a shared entry point:

```text
https://api.example.com
```

It then maps requests to backends:

```text
/api/users/*      -> users-service
/api/catalog/*    -> catalog-service
/api/orders/*     -> orders-service
/api/payments/*   -> payments-service
/api/shipping/*   -> shipping-service
```

The gateway centralizes cross-cutting concerns that apply to many services.

## 2.1 Typical API-gateway responsibilities

An API gateway commonly provides:

- Host and path routing
- HTTP method and header matching
- TLS termination
- API-key, JWT and OIDC authentication
- Consumer identification
- Rate limiting and quotas
- IP allowlists and denylists
- CORS
- Request validation
- Request and response rewriting
- Load balancing
- Health-aware backend selection
- Retries and timeouts
- Canary and weighted routing
- Metrics, logs and distributed tracing
- Correlation/request IDs
- Protocol translation in selected cases
- A stable external API while internal services change

## 2.2 North-south and east-west traffic

Two useful networking terms are:

- **North-south traffic:** traffic entering or leaving the cluster, such as a mobile application calling a public API.
- **East-west traffic:** traffic between internal workloads, such as `orders-service` calling `payments-service`.

API gateways are primarily associated with north-south traffic. A service mesh is primarily associated with east-west traffic. They can coexist.

```text
Internet
   |
   v
API Gateway / APISIX        north-south boundary
   |
   v
frontend-service
   |
   v
service mesh                east-west communication
   |
   +--> orders-service
   +--> payments-service
   +--> inventory-service
```

This is a common distinction, not an absolute technical restriction. APISIX can also be used for internal APIs.

---

# 3. What Apache APISIX is

**Apache APISIX is an open-source, dynamic, cloud-native API gateway.**

It can be deployed:

- in Kubernetes
- on Amazon EKS
- on another managed Kubernetes platform
- on virtual machines
- on bare metal
- in a private data center
- in a hybrid or multi-cloud design

APISIX can process HTTP, HTTPS and gRPC traffic, and it also has capabilities for stream-oriented TCP and UDP use cases. WebSocket traffic can pass through HTTP routes when configured appropriately.

The project is designed to be:

- dynamically configurable
- extensible through plugins
- suitable for distributed deployments
- independent of a specific cloud provider
- usable as a Kubernetes ingress and Gateway API implementation

## 3.1 APISIX is both a proxy and a policy engine

A reverse proxy accepts a client request and forwards it to a backend.

APISIX does this, but it also runs policies before and after proxying:

```text
Client request
     |
     v
Route match
     |
     v
Authentication
     |
     v
Authorization / restrictions
     |
     v
Rate limiting
     |
     v
Request transformation
     |
     v
Load balancing
     |
     v
Backend service
     |
     v
Response transformation and logging
```

This combination is what makes it an API gateway rather than only a basic proxy.

---

# 4. The essential mental model

Keep these definitions separate:

```text
API Gateway
    = the architectural role

Apache APISIX
    = software that performs that role

Gateway API
    = Kubernetes resources used to describe gateway infrastructure
      and routing

APISIX Ingress Controller
    = a Kubernetes controller that reads Kubernetes resources
      and converts them into APISIX configuration

APISIX Gateway Pods
    = the data-plane processes that receive real client traffic
```

There are two different flows.

## 4.1 Configuration flow

```text
Git / kubectl
     |
     v
Kubernetes API server
     |
     v
APISIX Ingress Controller
     |
     v
APISIX configuration
```

## 4.2 Request flow

```text
Client
  |
  v
DNS
  |
  v
Cloud load balancer
  |
  v
APISIX Gateway Pod
  |
  v
Authentication, routing and plugins
  |
  v
Application Pod
```

The Ingress Controller is normally **not** in the client request path. Its job is to reconcile configuration.

---

# 5. How APISIX is built

The official APISIX architecture documentation describes APISIX as being built on NGINX, `ngx_lua` and LuaJIT.

A simplified software stack is:

```text
+--------------------------------------------------+
| APISIX routes, plugins and gateway abstractions  |
+--------------------------------------------------+
| Lua and optional external plugin runtimes        |
+--------------------------------------------------+
| OpenResty / ngx_lua / LuaJIT                     |
+--------------------------------------------------+
| NGINX event-driven networking                    |
+--------------------------------------------------+
| Linux networking                                 |
+--------------------------------------------------+
```

## 5.1 APISIX core

The APISIX core is responsible for functions including:

- route matching
- plugin execution
- load balancing
- service discovery
- configuration handling
- gateway APIs
- request lifecycle integration

## 5.2 Plugin system

Plugins extend the core with functionality such as:

- authentication
- traffic control
- security
- transformations
- logging
- metrics
- tracing
- serverless functions
- integrations with external systems

Most built-in plugins are implemented in Lua. APISIX also supports external plugin runtimes for languages such as Go, Java and Python. The official architecture documentation also describes a WebAssembly plugin runtime as experimental.

## 5.3 Request-processing phases

Plugins can participate in different request lifecycle phases. Common phases include:

- `rewrite`
- `access`
- `before_proxy`
- `header_filter`
- `body_filter`
- `log`

This matters because plugin order and phase affect behavior. For example:

- authentication must happen before an unauthorized request reaches the upstream
- a response-header plugin runs after the upstream response begins
- logging occurs after enough request and response information is available

---

# 6. Control plane, data plane and configuration flow

## 6.1 Data plane

The **data plane** handles real application traffic.

It:

- listens on gateway ports
- terminates or passes TLS according to configuration
- matches routes
- runs plugins
- selects upstream nodes
- proxies requests
- returns responses
- emits telemetry

When users say “APISIX is handling traffic,” they usually mean the data plane.

## 6.2 Control plane

The **control plane** manages configuration.

Depending on deployment mode, it can include:

- the APISIX Admin API
- etcd
- APISIX control-plane instances
- the APISIX Ingress Controller
- Kubernetes resources
- a GitOps controller
- a management product or automation tool

The control plane should be protected much more strictly than the public data-plane endpoint.

## 6.3 Desired state and reconciliation

In Kubernetes, the APISIX Ingress Controller follows the controller pattern:

1. Watch Kubernetes resources.
2. Read the desired state.
3. Compare it with the state currently programmed into APISIX.
4. Create, update or delete APISIX configuration.
5. Update Kubernetes status where appropriate.
6. Repeat continuously.

This is reconciliation, not a one-time script.

For example:

```yaml
path: /orders
backend: orders-service
```

means:

> Continue ensuring that `/orders` traffic is routed to the current healthy endpoints behind `orders-service`.

When Pods are recreated and their IP addresses change, the controller can update APISIX without the application developer manually changing gateway nodes.

---

# 7. APISIX deployment modes

Current APISIX documentation describes three broad deployment modes:

1. Traditional
2. Decoupled
3. Standalone

The correct mode depends on scale, operations, failure-domain and configuration-management requirements.

## 7.1 Traditional mode

In traditional mode, an APISIX instance can serve both data-plane and control-plane responsibilities.

Conceptually:

```text
Administrator / controller
          |
          v
       Admin API
          |
          v
         etcd
          |
          v
APISIX instance handles traffic
```

Characteristics:

- configuration is stored in etcd
- the Admin API writes configuration
- APISIX watches for changes
- configuration updates can be applied dynamically
- the same deployment role can expose gateway and management capabilities

Advantages:

- straightforward architecture
- mature, dynamic configuration model
- familiar Admin API workflow

Risks and considerations:

- the Admin API must not be publicly exposed
- etcd must be highly available and securely operated
- management and traffic responsibilities need network isolation even when logically combined

## 7.2 Decoupled control and data planes

In decoupled mode, control-plane and data-plane instances are separated.

```text
Management network
    |
    v
APISIX control plane
    |
    v
etcd cluster
    ^
    |
APISIX data-plane replicas
    |
    v
Application traffic
```

Advantages:

- smaller attack surface on data-plane instances
- clearer separation of responsibilities
- independent scaling
- better isolation of public traffic from management interfaces

This is useful in larger or security-sensitive deployments.

## 7.3 Standalone file-driven mode

In standalone file-driven mode, APISIX reads the complete declarative configuration from a local YAML or JSON file instead of using etcd as its configuration center.

```text
Configuration file
       |
       v
APISIX loads configuration into memory
       |
       v
Traffic handling
```

The file is checked for changes and rules are hot-updated in memory.

This model works well when another system generates the full APISIX configuration and distributes it safely.

## 7.4 Standalone API-driven mode

The current APISIX documentation describes an API-driven standalone mode designed especially for integration with the APISIX Ingress Controller and APISIX declarative configuration tooling.

Conceptually:

```text
Kubernetes resources
        |
        v
APISIX Ingress Controller
        |
        v
Standalone configuration API
        |
        v
Full configuration held in APISIX memory
```

It does not require etcd for gateway configuration.

Important operational points:

- updates use full or versioned configuration operations
- configuration is held in memory
- gateway Pods need a reliable way to be reprogrammed after restart
- the APISIX Ingress Controller documentation continues to mark standalone mode as experimental
- version compatibility between APISIX and the Ingress Controller is especially important

## 7.5 Choosing a mode

| Requirement | Likely direction |
|---|---|
| Simple learning lab | Standalone API-driven mode from the official quick-start |
| Existing APISIX Admin API and etcd operations | Traditional |
| Large platform with strict management/traffic separation | Decoupled |
| Fully declarative generated configuration | Standalone file-driven |
| Kubernetes-native controller without etcd | Standalone API-driven, after assessing maturity and compatibility |

Do not choose only on the basis of “fewer components.” Consider:

- recovery after Pod restart
- upgrade compatibility
- configuration durability
- management security
- number of gateways
- multi-cluster design
- operational familiarity with etcd
- support and maturity requirements

---

# 8. Core APISIX objects

Understanding the internal APISIX object model makes Kubernetes resources much easier to understand.

## 8.1 Route

A **Route** determines which requests match and what should happen to them.

A route can match using information such as:

- URI or path
- hostname
- HTTP method
- headers
- query parameters
- source address
- other request variables

It can then:

- execute plugins
- reference a Service
- reference an Upstream
- directly contain upstream configuration

Example concept:

```text
Host: api.example.com
Path prefix: /orders
Methods: GET, POST
Plugins: OIDC, rate limit, request ID
Upstream: orders application
```

A Route answers:

> “Which requests does this rule apply to?”

## 8.2 Router

The **Router** is the route-matching engine.

Current APISIX documentation describes radix-tree-based router options, including matching by URI and by host plus URI.

You normally do not manage the router for every application route. It is a gateway-level implementation choice.

## 8.3 Upstream

An **Upstream** represents one or more backend nodes and the rules used to select among them.

```text
orders upstream
  |- 10.0.10.21:8080 weight 1
  |- 10.0.11.35:8080 weight 1
  `- 10.0.12.17:8080 weight 1
```

An Upstream can describe:

- nodes
- weights
- load-balancing algorithm
- health checks
- retries
- timeout behavior
- upstream scheme
- host-header behavior
- service-discovery integration

An Upstream answers:

> “Where can this request be sent, and how should a target be selected?”

## 8.4 Service

An APISIX **Service** is a reusable abstraction for shared API behavior.

Multiple Routes can reference one Service:

```text
GET /orders/*  ----\
POST /orders   -----+--> orders Service --> orders Upstream
GET /history/* ----/
```

The Service can hold common:

- plugins
- upstream references
- upstream configuration

This avoids repeating the same settings in many Routes.

Do not confuse:

- **APISIX Service**: an APISIX configuration abstraction
- **Kubernetes Service**: a Kubernetes networking abstraction that selects Pods

The APISIX Ingress Controller maps Kubernetes concepts into APISIX concepts, but the objects are not identical.

## 8.5 Consumer

A **Consumer** represents a known caller of the API.

Examples:

- a mobile application
- a business partner
- an internal batch process
- a customer tenant
- another microservice
- a developer account

After authentication, APISIX can associate a request with a Consumer and apply consumer-specific policies.

Example:

```text
free-plan consumer:
  100 requests/hour

premium-plan consumer:
  10,000 requests/hour

internal-reporting consumer:
  allowed only from private network
```

## 8.6 Credential

A credential contains authentication material associated with a Consumer, such as:

- API key
- JWT settings
- basic-auth credentials
- HMAC credentials

Credentials should be stored and distributed as secrets, not committed to Git in plaintext.

## 8.7 Plugin

A Plugin implements a gateway capability.

A plugin can be associated with:

- a Route
- a Service
- a Consumer
- a reusable Plugin Config
- global rules, depending on the feature

## 8.8 Plugin Config

A Plugin Config groups reusable plugin settings.

Instead of repeating authentication, CORS and rate-limit configuration in ten routes, the routes can reference a shared policy.

This improves:

- consistency
- reviewability
- reuse
- change management

It also increases blast radius: changing a shared policy can affect many routes. Treat shared policy changes as production changes.

## 8.9 SSL object

An SSL configuration associates certificates and keys with hostnames through SNI. It can also support mutual TLS configurations.

## 8.10 Global rule

A global rule applies plugin behavior broadly rather than only to one route. Use global policies carefully, because an error can affect all traffic.

---

# 9. How an incoming request is processed

Suppose a client sends:

```http
GET /orders/123 HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJ...
```

A simplified request lifecycle is:

## Step 1: DNS

`api.example.com` resolves to a public or private load-balancer address.

## Step 2: Cloud load balancer

An AWS NLB, ALB or other load balancer sends the request to an APISIX gateway endpoint.

In the common EKS design covered later, an NLB sends traffic to APISIX gateway Pods.

## Step 3: Connection and TLS

APISIX accepts the connection.

For HTTPS:

1. The TLS ClientHello includes the SNI hostname.
2. APISIX selects the matching certificate.
3. APISIX and the client negotiate TLS.
4. APISIX decrypts the HTTP request if TLS terminates at APISIX.

TLS can alternatively terminate at the AWS load balancer, but that changes certificate ownership, source protocol and trust-boundary design.

## Step 4: Route match

APISIX evaluates route rules:

```text
host == api.example.com
path starts with /orders
method == GET
```

## Step 5: Plugin execution

The matched route may run:

1. request ID generation
2. IP restriction
3. OIDC/JWT authentication
4. authorization integration
5. rate limiting
6. request validation
7. header/path rewriting

The exact order depends on plugin priorities and request phases.

## Step 6: Consumer identification

If authentication maps the request to a Consumer, consumer-level policy can be applied.

## Step 7: Upstream selection

APISIX chooses a healthy backend endpoint based on:

- current endpoint list
- weights
- load-balancing algorithm
- health status
- consistent-hash key, when configured
- traffic-split policy, when configured

## Step 8: Proxying

APISIX opens or reuses an upstream connection and forwards the request.

## Step 9: Response handling

APISIX receives the backend response and may:

- add or remove headers
- rewrite response status/body
- apply CORS response headers
- export metrics
- write logs
- complete a trace span

## Step 10: Client response

The response returns through the load balancer to the client.

---

# 10. APISIX and Kubernetes

APISIX has two principal Kubernetes components:

1. APISIX Gateway
2. APISIX Ingress Controller

## 10.1 APISIX Gateway

The gateway Deployment runs the data plane.

Typical Kubernetes resources include:

- `Deployment`
- `Service`
- `ConfigMap`
- `Secret`
- `ServiceAccount`
- optional `HorizontalPodAutoscaler`
- optional `PodDisruptionBudget`

## 10.2 APISIX Ingress Controller

The controller watches Kubernetes objects and configures APISIX.

It can read:

- Kubernetes `Ingress`
- Gateway API objects
- APISIX CRDs
- `Service`
- `EndpointSlice`
- `Secret`
- related policy objects

The official controller documentation states that it supports:

- native Kubernetes Ingress
- Gateway API
- APISIX custom resources
- Kubernetes Service discovery
- Pod-based upstream load balancing
- APISIX plugins and custom plugins

## 10.3 Why `EndpointSlice` matters

A Kubernetes Service is a stable logical name. Pods are ephemeral.

For example:

```text
orders-service
```

may currently select:

```text
10.0.10.14:8080
10.0.11.25:8080
10.0.12.37:8080
```

After a rollout, the Pod IPs may become:

```text
10.0.10.88:8080
10.0.11.91:8080
10.0.12.63:8080
```

`EndpointSlice` objects represent the current backend endpoints. Controllers can watch them and update data-plane targets.

That is why an APISIX route can continue referencing `orders-service` even though Pod IPs change.

---

# 11. Ingress API, Gateway API and APISIX CRDs

APISIX can be configured through several Kubernetes API styles.

## 11.1 Kubernetes Ingress

`Ingress` is the older standard HTTP/HTTPS routing API.

Example:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: orders
spec:
  rules:
    - host: api.example.com
      http:
        paths:
          - path: /orders
            pathType: Prefix
            backend:
              service:
                name: orders-service
                port:
                  number: 8080
```

Strengths:

- widely understood
- simple
- supported by many controllers

Limitations:

- relatively small core API
- advanced features often require controller-specific annotations
- weak separation between infrastructure and application ownership
- less expressive for non-HTTP protocols and advanced policies

The Kubernetes documentation now describes Gateway API as the successor to Ingress. Ingress remains a stable API, but new platform designs should evaluate Gateway API.

## 11.2 Kubernetes Gateway API

Gateway API separates concerns into resources including:

- `GatewayClass`
- `Gateway`
- `HTTPRoute`
- `GRPCRoute`
- and other route types depending on installed CRDs and channel

It offers:

- clearer role separation
- multiple listeners
- richer route attachment
- cross-namespace delegation
- standard filters
- explicit status
- a more extensible policy model

## 11.3 APISIX CRDs

APISIX-specific CRDs expose features that may not be represented in the standard API.

Examples include:

- `ApisixRoute`
- `ApisixUpstream`
- `ApisixConsumer`
- `ApisixPluginConfig`
- `ApisixTls`

The APISIX Ingress Controller 2.1.0 documentation also defines Gateway API extension resources such as:

- `GatewayProxy`
- `BackendTrafficPolicy`
- `Consumer`
- `PluginConfig`
- `HTTPRoutePolicy`

## 11.4 Which API style should you choose?

A practical strategy is:

- Prefer **Gateway API** for standard routing and organizational boundaries.
- Use **APISIX extensions** for APISIX-specific policy not represented by standard resources.
- Keep existing **Ingress** during migration if rewriting everything immediately is too risky.
- Avoid creating a design that uses every configuration style for the same responsibility.

For a new platform:

```text
Gateway API for:
  listeners, hostnames, paths, backends, weighted routing

APISIX extensions for:
  reusable plugins, consumers, advanced backend traffic policy

Kubernetes Secrets / external secret system for:
  credentials and certificates
```

---

# 12. Gateway API resource model and organizational roles

Gateway API has three central resources.

## 12.1 GatewayClass

`GatewayClass` defines a category of gateways managed by a particular controller.

```text
GatewayClass: apisix
controller: apisix.apache.org/apisix-ingress-controller
```

It is cluster-scoped and usually managed by a platform or infrastructure team.

## 12.2 Gateway

`Gateway` requests a gateway instance or gateway configuration.

It defines listeners such as:

```text
HTTP  port 80
HTTPS port 443 for api.example.com
```

A cluster/platform operator commonly owns it.

## 12.3 HTTPRoute

`HTTPRoute` defines how HTTP traffic is matched and sent to Services.

An application team can own routes in its namespace.

## 12.4 Separation of roles

Gateway API documentation uses three example personas:

- infrastructure provider
- cluster operator
- application developer

A practical enterprise mapping is:

| Role | Typical ownership |
|---|---|
| Cloud/platform infrastructure team | Gateway controller installation, `GatewayClass`, load balancer integration |
| Kubernetes platform team | shared `Gateway`, listeners, certificates, policies, namespace permissions |
| Application team | `HTTPRoute`, application `Service`, Deployment |
| Security team | approved authentication, TLS, WAF and policy patterns |
| SRE/operations team | SLOs, dashboards, alerting, capacity and incident response |

This model prevents every application team from creating unmanaged public entry points.

## 12.5 Cross-namespace routing

Gateway API supports controlled cross-namespace routing.

A shared Gateway can exist in a platform namespace while application routes exist in team namespaces.

```text
gateway-system/public-gateway
    |
    +--> team-a/orders-route
    +--> team-b/catalog-route
    `--> team-c/users-route
```

The Gateway listener must allow the namespaces, and cross-namespace backend references may require `ReferenceGrant`.

This model is powerful, but RBAC and route-attachment policies must be designed deliberately.

---

# 13. APISIX Ingress Controller resources

The current APISIX Ingress Controller documentation groups resources into standard Kubernetes/Gateway API resources and APISIX extensions.

## 13.1 GatewayProxy

`GatewayProxy` defines how the controller connects to APISIX, including:

- provider type
- control-plane or standalone endpoint
- authentication
- gateway-wide settings
- selected global plugin behavior

It can be referenced through `parametersRef`.

Treat this as platform configuration, not normal application configuration.

## 13.2 BackendTrafficPolicy

`BackendTrafficPolicy` applies advanced backend behavior, potentially including:

- load-balancing strategy
- timeouts
- retries
- host-header handling
- failover behavior

This separates backend traffic behavior from the `HTTPRoute`.

## 13.3 Consumer

The v1alpha1 `Consumer` resource represents a caller and credentials in the Gateway API extension model.

## 13.4 PluginConfig

`PluginConfig` defines reusable APISIX plugin settings and can be referenced by an `HTTPRoute` through an `ExtensionRef`.

Example use:

```text
PluginConfig: authenticated-api-policy
  - openid-connect
  - limit-count
  - request-id
  - prometheus
```

Multiple routes can reference it.

## 13.5 HTTPRoutePolicy

`HTTPRoutePolicy` extends route behavior without directly modifying the standard `HTTPRoute`.

## 13.6 ApisixRoute

`ApisixRoute` is the APISIX-native routing CRD. It supports advanced HTTP, TCP and UDP route definitions.

Use it when you need APISIX-native capabilities and Gateway API plus extensions do not cover the requirement.

## 13.7 ApisixUpstream

`ApisixUpstream` extends a Kubernetes Service with:

- health checks
- advanced load balancing
- retries
- timeouts
- subsets
- external nodes

## 13.8 ApisixConsumer

`ApisixConsumer` defines consumers and authentication settings in the v2 CRD model.

## 13.9 ApisixTls

`ApisixTls` manages:

- TLS certificates
- SNI hostname binding
- mTLS settings

## 13.10 Avoid mixing generations accidentally

The documentation contains both:

- Gateway API extension resources under `apisix.apache.org/v1alpha1`
- older/native APISIX resources under `apisix.apache.org/v2`

This is not simply “v2 is newer than v1alpha1” for one identical resource family. They serve different models.

Before applying an example:

```bash
kubectl api-resources | grep -i apisix
kubectl explain pluginconfig.apisix.apache.org
kubectl explain apisixroute.apisix.apache.org
```

Always compare examples with the CRDs installed by your chart version.

---

# 14. Service discovery and load balancing

## 14.1 Pod endpoint discovery

The controller can convert Kubernetes Service endpoints into APISIX upstream nodes.

Conceptually:

```text
HTTPRoute backendRef
       |
       v
Kubernetes Service
       |
       v
EndpointSlices
       |
       v
Pod IPs
       |
       v
APISIX Upstream nodes
```

This can allow APISIX to route directly to Pod IP addresses instead of adding another kube-proxy hop.

## 14.2 Load-balancing algorithms

APISIX supports multiple load-balancing strategies. Available choices depend on the context, but common APISIX algorithms include:

- weighted round robin
- consistent hashing
- EWMA
- least connections

### Weighted round robin

Each node receives traffic according to weight.

```text
pod-a weight 1
pod-b weight 1
pod-c weight 2
```

`pod-c` should receive approximately twice as many selections.

### Consistent hashing

A key such as a header, cookie or client attribute determines backend selection.

Useful for:

- session affinity
- cache locality
- tenant sharding

Do not use sticky routing as a substitute for correct state management unless the application genuinely requires affinity.

### Least connections

Traffic is directed toward the target with fewer active connections.

Useful when request duration varies significantly.

### EWMA

An exponentially weighted moving average can account for observed latency and favor faster upstreams.

## 14.3 Active and passive health checks

An active health check periodically probes backends.

Example:

```text
GET /health/ready
```

A passive health check evaluates real traffic outcomes.

Production readiness requires alignment between:

- Kubernetes readiness probes
- APISIX upstream health checks
- AWS load-balancer health checks
- application dependency behavior

A backend can be “healthy” at one layer and unusable at another. Define what health means at each layer.

## 14.4 Timeouts

Important timeout classes include:

- client-to-gateway connection timeout
- gateway upstream connect timeout
- upstream send timeout
- upstream read timeout
- AWS load-balancer idle timeout, depending on load-balancer type and protocol

A timeout should reflect the API contract. Simply setting every timeout very high can convert failures into resource exhaustion.

## 14.5 Retries

Retries can improve resilience for transient failures, but they can also multiply traffic.

Avoid automatic retries for non-idempotent requests unless you have an idempotency design.

Safer retry candidates:

- `GET`
- selected `HEAD`
- operations using an idempotency key
- connection failure before the request is processed

Risky retry candidates:

- payment creation
- order creation
- any mutation without deduplication

---

# 15. Plugins and policy enforcement

APISIX plugins are one of its main differentiators.

## 15.1 Plugin categories

### Authentication and authorization

- `key-auth`
- `jwt-auth`
- `openid-connect`
- `basic-auth`
- HMAC authentication
- LDAP authentication
- OPA integration
- external authorization integrations

### Security

- `ip-restriction`
- CORS
- URI restrictions
- user-agent restrictions
- CSRF protection
- WAF integrations
- data masking

### Traffic management

- `limit-count`
- `limit-req`
- `limit-conn`
- `traffic-split`
- circuit breaking
- request validation
- caching
- request mirroring
- request IDs

### Transformation

- `proxy-rewrite`
- response rewriting
- body transformation
- gRPC transcoding
- gRPC-Web support
- fault injection
- mocking

### Observability

- Prometheus
- OpenTelemetry
- Zipkin
- external log sinks
- Kafka logging
- HTTP logging
- tracing integrations

## 15.2 Route-level policy

Apply when a policy is specific to one API operation.

Example:

```text
POST /payments
  - OIDC
  - strict rate limit
  - request validation
  - audit log
```

## 15.3 Service-level policy

Apply when multiple routes share the same policy and backend.

Example:

```text
/orders/*
/order-history/*
/order-search/*
```

all use the same orders API policy.

## 15.4 Consumer-level policy

Apply when behavior depends on caller identity.

Example:

```text
partner-a:
  quota 10,000/hour

partner-b:
  quota 1,000/hour
```

## 15.5 Global policy

Use for truly universal behavior, such as a request ID or baseline telemetry.

Global policies have a broad blast radius. Test them carefully.

## 15.6 Plugin precedence

Plugin configuration can exist at several levels, and APISIX defines precedence behavior. The official Consumer documentation notes a high-priority relationship beginning with Consumer over route and shared configuration levels.

Do not depend on memory for complex precedence. Test the effective policy with the exact APISIX version, because mixing Route plugins, Service plugins, Consumer plugins and Plugin Config references can be difficult to reason about.

## 15.7 Request rewriting

The `proxy-rewrite` plugin can change:

- upstream URI
- HTTP method
- Host header
- request headers

Example use case:

```text
Public API:
  /api/v1/orders/123

Internal service:
  /orders/123
```

The gateway can remove `/api/v1` before forwarding.

Avoid excessive rewriting that makes production behavior impossible to understand. Keep a documented external-to-internal mapping.

---

# 16. Authentication, authorization and consumers

Authentication answers:

> Who is calling?

Authorization answers:

> Is this caller allowed to perform this action?

They are related but not the same.

## 16.1 API-key authentication

API keys are useful for:

- partner integrations
- simple machine clients
- development environments
- metering by client

They are not ideal for rich end-user identity and delegated authorization.

A client sends:

```http
apikey: client-secret-value
```

APISIX:

1. extracts the key
2. finds the credential
3. identifies the Consumer
4. applies policy
5. allows or rejects the request

Protect API keys:

- store them as secrets
- rotate them
- do not put them in URLs
- avoid logging them
- use TLS
- scope them
- support multiple active credentials during rotation

## 16.2 JWT authentication

JWT authentication allows clients to carry a signed token.

APISIX can verify:

- signature
- algorithm
- credential identity
- expiration
- token location

JWTs can be sent in:

- an HTTP header
- a cookie
- in some configurations, a query parameter

Headers are normally preferable to query parameters because URLs are often logged.

## 16.3 OpenID Connect

The `openid-connect` plugin integrates APISIX with OIDC identity providers such as:

- Keycloak
- Auth0
- Microsoft Entra ID
- Okta
- Google identity services
- other standards-compliant providers

Two common API patterns are:

### Bearer-token validation

```text
Client gets token from identity provider
       |
       v
Client calls APISIX with Bearer token
       |
       v
APISIX validates token
       |
       v
Backend receives authenticated identity context
```

### Browser authorization-code flow

```text
Browser -> APISIX -> identity provider login
                    |
                    v
               authorization code
                    |
                    v
             tokens / user session
```

The appropriate mode depends on whether the client is:

- a browser application
- a mobile app
- a machine client
- another service

## 16.4 Gateway authentication versus application authorization

A strong architecture usually divides responsibilities.

APISIX can enforce:

- token validity
- issuer and audience
- required scopes or claims
- coarse role checks
- client quota
- source-network restriction

The application should still enforce business authorization:

- Can this user read order `123`?
- Does this tenant own this resource?
- Is this payment operation permitted in the current state?
- Is the amount within a business limit?

Do not assume that “valid token” means “allowed to do everything.”

## 16.5 Forwarded identity headers

After authentication, APISIX can add identity-related headers to the upstream request.

Only trust these headers if:

- clients cannot bypass APISIX
- APISIX removes spoofed incoming copies
- the backend network permits only trusted gateway traffic
- header names and semantics are documented

Otherwise a client might call the backend directly and forge identity headers.

---

# 17. Rate limiting and protection against overload

Rate limiting protects:

- gateway capacity
- backend capacity
- fair usage
- commercial quotas
- authentication endpoints
- expensive operations
- third-party dependencies

## 17.1 Fixed-window count limiting

The APISIX `limit-count` plugin uses a fixed-window request-count model.

Example:

```text
100 requests in 60 seconds per client
```

After the quota is exceeded, APISIX rejects requests, commonly with:

```http
HTTP/1.1 429 Too Many Requests
```

The plugin can emit rate-limit headers describing:

- total quota
- remaining quota
- reset time

## 17.2 Choosing the key

A rate limit needs a key.

Possible keys:

- client IP
- Consumer name
- API key identity
- JWT subject
- tenant ID
- route ID
- combination of attributes

### IP-based limiting

Simple, but imperfect:

- many users can share one NAT address
- one user can change addresses
- proxies can hide the original address
- IPv6 creates additional considerations

### Consumer-based limiting

Better for authenticated APIs:

```text
key = consumer_name
```

### Tenant-based limiting

Useful for SaaS:

```text
key = tenant claim
```

Ensure the tenant attribute is trusted and validated.

## 17.3 Local versus distributed counters

The `limit-count` plugin supports counter policies including:

- local memory
- Redis
- Redis cluster

A local counter is maintained independently by each gateway instance.

With three replicas, a nominal limit of 100 may effectively allow more than 100 across the deployment.

Use a distributed store when the quota must be enforced consistently across replicas.

Trade-off:

```text
Local counter:
  faster, simpler, approximate cluster-wide quota

Redis counter:
  coordinated quota, extra dependency and network latency
```

## 17.4 Rate limit versus concurrency limit

Request rate controls how many requests arrive over time.

Concurrency limit controls how many are active simultaneously.

A backend can be overloaded by:

- too many requests per second
- too many slow requests
- too many open connections

Use the correct control for the failure mode.

## 17.5 Protect sensitive endpoints

Authentication and password-reset endpoints often need stricter controls than read-only catalog endpoints.

Example:

```text
/login:
  low per-IP burst
  per-account protection
  bot/WAF controls
  detailed security telemetry

/catalog:
  higher request rate
  caching
  public access
```

---

# 18. TLS, HTTPS, SNI and mTLS

## 18.1 TLS termination

TLS can terminate at:

1. AWS load balancer
2. APISIX
3. the backend
4. multiple layers through re-encryption

### TLS at APISIX

```text
Client --HTTPS--> APISIX --HTTP/HTTPS--> backend
```

Advantages:

- APISIX selects certificates by SNI
- gateway has full HTTP context
- consistent multi-cloud design

### TLS at AWS load balancer

```text
Client --HTTPS--> NLB/ALB --HTTP/HTTPS--> APISIX
```

Advantages:

- certificates can be managed in AWS Certificate Manager
- TLS offload can be centralized in AWS

Considerations:

- trust boundary moves outward
- APISIX sees decrypted traffic unless re-encrypted
- client certificate and source details need explicit design
- health checks and listener configuration become more complex

## 18.2 SNI

Server Name Indication lets one IP address serve multiple TLS hostnames.

```text
api.example.com
partner.example.com
internal-api.example.com
```

APISIX selects the certificate based on the requested SNI hostname.

## 18.3 Mutual TLS

Normal TLS authenticates the server to the client.

mTLS also authenticates the client with a certificate.

Useful for:

- B2B APIs
- device identity
- high-trust service integrations
- private administrative APIs

mTLS does not replace application authorization. A valid client certificate proves possession of a trusted key, but the system still needs to decide what that identity may do.

## 18.4 Certificate sources

Certificates can come from:

- Kubernetes Secrets
- cert-manager
- AWS Certificate Manager at the load-balancer layer
- an external secret/certificate management system
- an enterprise PKI

Never store private keys in a public repository.

## 18.5 Backend TLS

For gateway-to-backend encryption:

```text
Client --HTTPS--> APISIX --HTTPS--> service
```

Consider:

- backend certificate hostname
- trusted CA
- certificate rotation
- strict verification
- mTLS to backend when required

Disabling certificate verification may make a test work, but it removes server-authentication guarantees.

---

# 19. Traffic management and release strategies

## 19.1 Weighted canary

Suppose:

```text
orders-v1 weight 90
orders-v2 weight 10
```

APISIX sends approximately:

```text
90% -> v1
10% -> v2
```

Use this to:

1. release a small percentage
2. observe errors and latency
3. increase traffic gradually
4. roll back by changing weights

Weighted traffic is probabilistic. Small samples will not always match the exact percentage.

## 19.2 Header-based canary

Route selected users to a new version:

```http
X-Canary: true
```

Useful for:

- internal testers
- QA
- specific partners
- synthetic tests

Do not allow an untrusted public header to bypass security or access unreleased functionality accidentally.

## 19.3 Cookie-based canary

A cookie can keep a browser on one version.

Useful when user experience needs session consistency.

## 19.4 Traffic mirroring

Mirroring copies production requests to another backend while the original backend remains authoritative.

Uses:

- testing a new implementation
- validating migration behavior
- performance observation

Risks:

- duplicate side effects
- sensitive data exposure
- doubled downstream traffic
- response from mirror is normally ignored

Mirror only safe requests or use a backend that cannot perform real side effects.

## 19.5 Blue/green deployment

```text
Blue = current production
Green = new production candidate
```

The route changes from blue to green after validation.

The rollback is a route switch, provided database and state changes remain compatible.

## 19.6 Circuit breaking

A circuit breaker stops sending traffic to a failing backend for a period or under defined conditions.

It prevents repeated work against a dependency that is already unhealthy.

A circuit breaker needs:

- meaningful failure thresholds
- recovery logic
- observability
- fallback behavior
- avoidance of false positives

---

# 20. Observability: metrics, logs and traces

An API gateway is a strategic observation point because almost every external API request crosses it.

## 20.1 Metrics

The Prometheus plugin can collect gateway and API metrics such as request counts and latency.

Useful dimensions include:

- route
- service
- upstream
- consumer, where safe
- response status
- latency bucket
- gateway instance

Avoid high-cardinality labels such as raw user ID or full URL with arbitrary identifiers.

### Golden signals

Monitor:

- traffic
- errors
- latency
- saturation

Example alerts:

- 5xx ratio above threshold
- p95/p99 latency increase
- no healthy upstreams
- gateway Pod restart loop
- APISIX controller reconciliation errors
- NLB unhealthy target count
- Redis rate-limit dependency failures
- certificate expiry approaching

## 20.2 Logs

Logs may include:

- request timestamp
- request ID
- trace ID
- route
- upstream
- status
- latency
- client address
- authenticated consumer
- selected backend
- retry count

Do not log:

- passwords
- tokens
- API keys
- session cookies
- full payment data
- sensitive request bodies

Use structured JSON logs and centralized storage.

## 20.3 Distributed tracing

The OpenTelemetry plugin can export traces to an OpenTelemetry Collector.

```text
Client
  |
  v
APISIX span
  |
  v
orders-service span
  |
  v
database span
```

A complete trace helps answer:

- Was latency in the gateway or backend?
- Which upstream Pod was selected?
- Did the request retry?
- Which dependency failed?
- Was the request rejected before reaching the application?

Sampling must balance visibility and overhead.

The APISIX documentation warns that comprehensive request-lifecycle tracing adds processing and export overhead.

## 20.4 Correlation IDs

Generate or validate a request ID at the edge.

Propagate it to:

- upstream headers
- application logs
- trace attributes
- error responses where appropriate

Reject or sanitize unbounded client-provided IDs to avoid log injection and excessive cardinality.

## 20.5 SLO example

For a public orders API:

```text
Availability SLO:
  99.9% successful eligible requests over 30 days

Latency SLO:
  95% of eligible requests below 300 ms

Gateway indicators:
  APISIX 5xx
  upstream 5xx
  timeout rate
  no-healthy-upstream rate
  route-not-found rate
```

Separate:

- client errors
- gateway-generated errors
- upstream-generated errors
- intentional rate-limit responses

---

# 21. APISIX on Amazon EKS

A common AWS design is:

```text
Route 53
   |
   v
AWS Network Load Balancer
   |
   v
APISIX Gateway Service
   |
   v
APISIX Gateway Pods
   |
   v
Application Pod IPs
```

## 21.1 Why use an NLB in front of APISIX?

An NLB operates at Layer 4 and can provide:

- a managed AWS entry point
- high network throughput
- TCP/TLS listeners
- source-IP preservation characteristics
- static addresses for the lifetime of the NLB
- direct IP targets

APISIX then performs Layer-7 API routing and policy.

This keeps responsibilities clear:

| NLB | APISIX |
|---|---|
| AWS network entry | API routing |
| Listener and target groups | Host/path/method matching |
| Layer-4 load balancing | Authentication |
| AWS health checks | Rate limiting |
| Optional AWS TLS termination | Request transformations |
| AWS network integration | Consumers and API policy |

## 21.2 AWS Load Balancer Controller

AWS recommends the AWS Load Balancer Controller for EKS load balancers.

For a Kubernetes `Service` of type `LoadBalancer`, it can provision an NLB.

For Kubernetes `Ingress`, it can provision an ALB.

With APISIX, the usual pattern is:

- NLB created from the APISIX gateway `Service`
- APISIX provides the HTTP API gateway layer

## 21.3 IP targets versus instance targets

### IP targets

```text
NLB target group -> APISIX Pod IPs
```

Advantages:

- direct Pod routing
- supported for EC2 nodes and Fargate
- avoids NodePort as the final target

### Instance targets

```text
NLB target group -> worker node -> NodePort -> APISIX Pod
```

Advantages:

- familiar, broadly used

Considerations:

- extra network hop
- only applicable where node targeting is supported
- traffic distribution interacts with Kubernetes Service behavior

## 21.4 ALB in front of APISIX?

It is possible, but often duplicates Layer-7 functions:

```text
ALB L7 routing -> APISIX L7 routing
```

Use it only for a deliberate reason, such as a required AWS-specific feature at the outer layer.

For a generic APISIX gateway, NLB is often the cleaner pairing.

## 21.5 Route 53 and DNS

A Route 53 alias or DNS record maps the API hostname to the AWS load balancer.

```text
api.example.com -> NLB DNS name
```

DNS is separate from the Kubernetes route. Both must be correct:

- DNS must reach the load balancer.
- Gateway/HTTPRoute must accept the hostname.
- TLS must include the hostname.
- APISIX must have a matching route.

## 21.6 AWS WAF and CloudFront

Depending on requirements:

```text
Client
  |
CloudFront
  |
AWS WAF
  |
ALB or another supported origin path
  |
APISIX
```

or a different supported architecture may be used.

Do not assume every AWS edge/security service attaches directly to every load-balancer type. Validate the exact AWS integration.

APISIX can also integrate with WAF products through its plugin ecosystem, but gateway plugins and AWS perimeter controls protect different layers.

---

# 22. A complete EKS reference architecture

```text
                            INTERNET
                                |
                                v
                        Route 53 DNS record
                                |
                                v
                  AWS Network Load Balancer (multi-AZ)
                                |
                 +--------------+--------------+
                 |                             |
                 v                             v
          APISIX Gateway Pod A          APISIX Gateway Pod B
             AZ-a / node-a                 AZ-b / node-b
                 |                             |
                 +--------------+--------------+
                                |
              +-----------------+------------------+
              |                 |                  |
              v                 v                  v
        users-service      orders-service    payments-service
          Pod endpoints      Pod endpoints      Pod endpoints

Configuration path:

Git repository
     |
     v
Flux or Argo CD
     |
     v
Kubernetes API server
     |
     v
APISIX Ingress Controller replicas
     |
     v
APISIX gateway configuration

Observability:

APISIX -> Prometheus / managed metrics
APISIX -> OpenTelemetry Collector -> tracing backend
APISIX -> log collector -> centralized logs
AWS NLB -> CloudWatch metrics
```

## 22.1 Suggested namespace model

```text
gateway-system
  APISIX
  APISIX Ingress Controller
  Gateway
  platform policies

observability
  Prometheus
  OpenTelemetry Collector
  logging agents

orders
  orders Deployment
  orders Service
  orders HTTPRoute

catalog
  catalog Deployment
  catalog Service
  catalog HTTPRoute
```

## 22.2 Shared versus dedicated gateways

### Shared gateway

One gateway serves many teams.

Advantages:

- lower cost
- centralized operations
- fewer public load balancers
- consistent policy

Risks:

- larger blast radius
- noisy-neighbor effects
- more complex ownership

### Dedicated gateway

Each environment, tenant or security domain has its own gateway.

Advantages:

- isolation
- independent scaling
- smaller blast radius
- simpler chargeback in some models

Risks:

- more infrastructure
- more upgrades
- more load balancers
- duplicated policy

A common compromise:

```text
one gateway per environment and trust boundary
not one gateway per individual microservice
```

---

# 23. Local Kubernetes lab

The official APISIX Ingress Controller 2.1.0 getting-started documentation uses:

- Kubernetes 1.26 or newer
- Helm 3.8 or newer
- `kubectl`
- `kind` for a local cluster

The following command mirrors the official standalone API-driven quick-start pattern at the research date.

> Verify the current official installation page before using it in a production cluster. Helm value names and compatibility can change.

```bash
kind create cluster

kubectl create namespace ingress-apisix

helm repo add apisix https://apache.github.io/apisix-helm-chart
helm repo update

helm install apisix \
  --namespace ingress-apisix \
  --create-namespace \
  --set apisix.deployment.role=traditional \
  --set apisix.deployment.role_traditional.config_provider=yaml \
  --set etcd.enabled=false \
  --set ingress-controller.enabled=true \
  --set ingress-controller.config.provider.type=apisix-standalone \
  --set ingress-controller.apisix.adminService.namespace=ingress-apisix \
  --set ingress-controller.gatewayProxy.createDefault=true \
  apisix/apisix
```

Check the installation:

```bash
kubectl get all -n ingress-apisix
kubectl get gatewayclass
kubectl get crd | grep -E 'gateway|apisix'
```

Port-forward the gateway:

```bash
kubectl port-forward \
  -n ingress-apisix \
  svc/apisix-gateway \
  9080:80
```

Verify:

```bash
curl -i http://127.0.0.1:9080/
```

A 404 can be a healthy result when no route matches. It proves the gateway is reachable.

## 23.1 Verify version compatibility

```bash
helm list -n ingress-apisix
helm get values apisix -n ingress-apisix
kubectl get deployment -n ingress-apisix -o wide
kubectl describe pod -n ingress-apisix
```

Check image tags:

```bash
kubectl get pods -n ingress-apisix \
  -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{range .spec.containers[*]}{.image}{" "}{end}{"\n"}{end}'
```

Do not upgrade the gateway and controller independently without reading the compatibility and upgrade documentation.

---

# 24. Practical application example

We will expose an orders API.

## 24.1 Application Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: orders-v1
  namespace: orders
spec:
  replicas: 3
  selector:
    matchLabels:
      app: orders
      version: v1
  template:
    metadata:
      labels:
        app: orders
        version: v1
    spec:
      containers:
        - name: orders
          image: kennethreitz/httpbin
          ports:
            - name: http
              containerPort: 80
          readinessProbe:
            httpGet:
              path: /status/200
              port: http
            initialDelaySeconds: 3
            periodSeconds: 5
          livenessProbe:
            httpGet:
              path: /status/200
              port: http
            initialDelaySeconds: 10
            periodSeconds: 10
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              memory: 256Mi
```

## 24.2 Application Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: orders-service
  namespace: orders
spec:
  selector:
    app: orders
    version: v1
  ports:
    - name: http
      port: 8080
      targetPort: http
```

Apply:

```bash
kubectl create namespace orders
kubectl apply -f orders-deployment.yaml
kubectl apply -f orders-service.yaml
kubectl get pods,svc,endpointslice -n orders
```

The Service listens on port `8080` but forwards to container port `80`.

---

# 25. Gateway API manifests

The exact `GatewayProxy` reference can depend on how the chart installed the default gateway configuration. The following example shows the standard resource relationship.

## 25.1 GatewayClass

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: GatewayClass
metadata:
  name: apisix
spec:
  controllerName: apisix.apache.org/apisix-ingress-controller
```

## 25.2 Gateway

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: public-api
  namespace: gateway-system
spec:
  gatewayClassName: apisix
  listeners:
    - name: http
      protocol: HTTP
      port: 80
      allowedRoutes:
        namespaces:
          from: All
```

For a real platform, `from: All` may be too broad. Prefer a namespace selector or another controlled attachment strategy.

## 25.3 HTTPRoute

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: orders
  namespace: orders
spec:
  parentRefs:
    - name: public-api
      namespace: gateway-system
      sectionName: http
  hostnames:
    - api.example.com
  rules:
    - matches:
        - path:
            type: PathPrefix
            value: /orders
      backendRefs:
        - name: orders-service
          port: 8080
```

Apply:

```bash
kubectl create namespace gateway-system
kubectl apply -f gatewayclass.yaml
kubectl apply -f gateway.yaml
kubectl apply -f orders-route.yaml
```

Inspect status:

```bash
kubectl get gatewayclass
kubectl describe gateway public-api -n gateway-system
kubectl describe httproute orders -n orders
```

Test through port-forward:

```bash
curl -i \
  -H 'Host: api.example.com' \
  http://127.0.0.1:9080/orders/get
```

The Host header is required because the route declares `api.example.com`.

---

# 26. Adding rate limiting

Create a reusable `PluginConfig`.

```yaml
apiVersion: apisix.apache.org/v1alpha1
kind: PluginConfig
metadata:
  name: orders-rate-limit
  namespace: orders
spec:
  plugins:
    - name: limit-count
      config:
        count: 100
        time_window: 60
        rejected_code: 429
        key_type: var
        key: remote_addr
        policy: local
```

Reference it from the route:

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: orders
  namespace: orders
spec:
  parentRefs:
    - name: public-api
      namespace: gateway-system
      sectionName: http
  hostnames:
    - api.example.com
  rules:
    - matches:
        - path:
            type: PathPrefix
            value: /orders
      filters:
        - type: ExtensionRef
          extensionRef:
            group: apisix.apache.org
            kind: PluginConfig
            name: orders-rate-limit
      backendRefs:
        - name: orders-service
          port: 8080
```

Apply and inspect:

```bash
kubectl apply -f orders-rate-limit.yaml
kubectl apply -f orders-route.yaml
kubectl describe pluginconfig orders-rate-limit -n orders
kubectl describe httproute orders -n orders
```

## 26.1 Production caution: `policy: local`

A local policy counts independently on each APISIX replica.

For a strict, shared production quota, evaluate Redis or Redis Cluster.

The external rate-limit store becomes a production dependency. Configure:

- authentication
- TLS
- high availability
- timeout
- connection pools
- failure behavior
- monitoring

---

# 27. Adding API-key authentication

The APISIX Ingress Controller documentation provides a Gateway API extension `Consumer` resource.

The exact credential schema must match the installed CRD. A 2.1.0-style example is:

```yaml
apiVersion: apisix.apache.org/v1alpha1
kind: Consumer
metadata:
  name: partner-a
  namespace: orders
spec:
  gatewayRef:
    name: public-api
    namespace: gateway-system
  credentials:
    - type: key-auth
      name: primary-key
      config:
        key: REPLACE_ME
```

Create a PluginConfig that enables `key-auth`:

```yaml
apiVersion: apisix.apache.org/v1alpha1
kind: PluginConfig
metadata:
  name: orders-auth-policy
  namespace: orders
spec:
  plugins:
    - name: key-auth
      config:
        _meta:
          disable: false
    - name: limit-count
      config:
        count: 1000
        time_window: 3600
        rejected_code: 429
        key_type: var
        key: consumer_name
        policy: local
```

Attach it to the `HTTPRoute` using `ExtensionRef`.

Test:

```bash
curl -i \
  -H 'Host: api.example.com' \
  http://127.0.0.1:9080/orders/get
```

Expected: authentication rejection.

Then:

```bash
curl -i \
  -H 'Host: api.example.com' \
  -H 'apikey: REPLACE_ME' \
  http://127.0.0.1:9080/orders/get
```

Expected: request reaches the backend.

## 27.1 Secret-management warning

The plaintext key above is only for understanding the object shape.

Production options include:

- Kubernetes Secret references where supported
- External Secrets Operator
- Secrets Store CSI Driver
- AWS Secrets Manager
- a Git encryption workflow such as SOPS
- APISIX secret-manager integrations

Never commit a real API key in plaintext.

---

# 28. Adding HTTPS

Create a TLS Secret:

```bash
kubectl create secret tls api-example-com \
  --cert=tls.crt \
  --key=tls.key \
  -n gateway-system
```

Add an HTTPS listener:

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: public-api
  namespace: gateway-system
spec:
  gatewayClassName: apisix
  listeners:
    - name: https
      hostname: api.example.com
      protocol: HTTPS
      port: 443
      tls:
        mode: Terminate
        certificateRefs:
          - kind: Secret
            name: api-example-com
      allowedRoutes:
        namespaces:
          from: All
```

Update the route:

```yaml
parentRefs:
  - name: public-api
    namespace: gateway-system
    sectionName: https
```

Test with a real DNS name and trusted certificate in production.

For a local self-signed lab:

```bash
curl -k -i https://api.example.com/orders/get
```

`-k` disables certificate verification and should not be used as a production solution.

## 28.1 cert-manager pattern

```text
Certificate resource
      |
      v
cert-manager
      |
      v
Kubernetes TLS Secret
      |
      v
Gateway certificateRef
      |
      v
APISIX SNI certificate
```

Monitor certificate renewal and expiry.

---

# 29. Adding a canary release

Create version 2.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: orders-v2
  namespace: orders
spec:
  replicas: 1
  selector:
    matchLabels:
      app: orders
      version: v2
  template:
    metadata:
      labels:
        app: orders
        version: v2
    spec:
      containers:
        - name: orders
          image: kennethreitz/httpbin
          ports:
            - name: http
              containerPort: 80
```

Create a Service:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: orders-v2-service
  namespace: orders
spec:
  selector:
    app: orders
    version: v2
  ports:
    - name: http
      port: 8080
      targetPort: http
```

Weighted Gateway API route:

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: orders
  namespace: orders
spec:
  parentRefs:
    - name: public-api
      namespace: gateway-system
  hostnames:
    - api.example.com
  rules:
    - matches:
        - path:
            type: PathPrefix
            value: /orders
      backendRefs:
        - name: orders-service
          port: 8080
          weight: 90
        - name: orders-v2-service
          port: 8080
          weight: 10
```

Before increasing the v2 weight, compare:

- error rate
- latency
- saturation
- business metrics
- logs
- trace failures
- compatibility with current data

A rollout is not successful only because Pods are `Running`.

---

# 30. Exposing APISIX through an AWS NLB

AWS documentation recommends the AWS Load Balancer Controller for new EKS load balancers.

Assuming the APISIX gateway Service is named `apisix-gateway`, its essential shape is:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: apisix-gateway
  namespace: ingress-apisix
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: external
    service.beta.kubernetes.io/aws-load-balancer-nlb-target-type: ip
    service.beta.kubernetes.io/aws-load-balancer-scheme: internet-facing
    service.beta.kubernetes.io/aws-load-balancer-healthcheck-protocol: TCP
spec:
  type: LoadBalancer
  ports:
    - name: http
      port: 80
      targetPort: 9080
    - name: https
      port: 443
      targetPort: 9443
  selector:
    app.kubernetes.io/name: apisix
```

The actual target ports and selector labels must match the Helm release. Do not replace the chart-created Service blindly.

Inspect it first:

```bash
kubectl get svc apisix-gateway -n ingress-apisix -o yaml
kubectl get pods -n ingress-apisix --show-labels
```

A safer workflow is to set Service values in the Helm release so that Git/Helm remains the source of truth.

## 30.1 Important AWS annotations

For AWS Load Balancer Controller:

```yaml
service.beta.kubernetes.io/aws-load-balancer-type: "external"
service.beta.kubernetes.io/aws-load-balancer-nlb-target-type: "ip"
service.beta.kubernetes.io/aws-load-balancer-scheme: "internet-facing"
```

AWS notes that NLBs are internal by default unless the internet-facing scheme is specified.

For private APIs:

```yaml
service.beta.kubernetes.io/aws-load-balancer-scheme: "internal"
```

## 30.2 Do not change ownership annotations casually

AWS documentation warns that some load-balancer ownership annotations should not be edited in place after Service creation. A replacement may be required.

Plan changes to:

- target type
- scheme
- load-balancer class
- subnet selection

as controlled infrastructure migrations.

## 30.3 Health checks

Possible designs:

### TCP health check

Checks that the APISIX listener accepts a connection.

Pros:

- simple
- independent of a particular route

Cons:

- does not prove that APISIX can process an HTTP request

### HTTP health check

Checks a dedicated gateway health endpoint.

Pros:

- verifies more of the request path

Cons:

- must not depend on an application route
- must remain available during application failure
- needs a stable response

Create a gateway-local health route that does not proxy to a business backend.

## 30.4 Source IP

Client IP behavior depends on:

- NLB target type
- proxy protocol
- TLS termination
- Kubernetes traffic policy
- trusted proxy configuration
- APISIX real-IP configuration

Never apply IP security policies until you have verified which address APISIX sees. Otherwise you may rate-limit or allowlist the NLB address instead of the client.

## 30.5 DNS

After the Service receives an external hostname:

```bash
kubectl get svc apisix-gateway -n ingress-apisix
```

Create a Route 53 alias or CNAME pattern appropriate to the record type.

Then validate:

```bash
dig api.example.com
curl -v https://api.example.com/orders/get
```

---

# 31. GitOps with Flux or Argo CD

APISIX works naturally with GitOps because routing and policy can be expressed as Kubernetes YAML.

```text
Engineer opens pull request
        |
        v
Review and automated validation
        |
        v
Merge
        |
        v
Flux or Argo CD
        |
        v
Kubernetes API
        |
        v
APISIX Ingress Controller
        |
        v
APISIX data plane
```

## 31.1 Suggested repository structure

```text
clusters/
  prod-eu/
    gateway/
      helmrelease.yaml
      gatewayclass.yaml
      public-gateway.yaml
      policies/
    apps/
      orders/
        deployment.yaml
        service.yaml
        httproute.yaml
      catalog/
        deployment.yaml
        service.yaml
        httproute.yaml

platform/
  apisix/
    base/
    overlays/
      dev/
      stage/
      prod/

policies/
  authenticated-api/
  public-read-api/
  partner-api/
```

## 31.2 Separate platform and application ownership

Platform repository or directory:

- APISIX Helm release
- `GatewayClass`
- shared `Gateway`
- load-balancer annotations
- global telemetry
- baseline security
- RBAC
- namespaces

Application repository or directory:

- Deployment
- Service
- HTTPRoute
- approved PluginConfig reference
- application-specific policies

## 31.3 Admission and policy validation

Use policy tooling to prevent:

- public routes without TLS
- wildcard hostnames without approval
- routes pointing across namespaces without grants
- plaintext credentials
- unrestricted CORS
- disabled backend TLS verification
- unsafe plugin use
- `Gateway` creation by application namespaces
- direct public `LoadBalancer` Services outside the gateway namespace

Possible tools include:

- Kyverno
- Gatekeeper
- ValidatingAdmissionPolicy
- CI schema validation
- conformance tests

## 31.4 Promotion

A safe promotion flow:

```text
dev -> integration tests -> stage -> load/security tests -> production
```

Do not copy a mutable “latest” image tag between environments. Pin versions.

---

# 32. Production security recommendations

## 32.1 Protect the Admin API

The APISIX Admin API documentation recommends:

- changing the default Admin API key
- restricting allowed source IPs

Additional production controls:

- use a ClusterIP-only Service
- apply NetworkPolicy
- keep it off public load balancers
- limit callers to the controller or management plane
- use TLS/mTLS where supported
- rotate credentials
- log and alert on access
- do not expose port 9180 publicly

## 32.2 Isolate the gateway namespace

Use RBAC so that application teams cannot modify:

- APISIX Deployment
- gateway Service
- GatewayClass
- management Secrets
- controller ServiceAccount
- cluster-wide policies

## 32.3 Restrict backend access

A backend protected only by APISIX must not also be publicly reachable.

Use:

- `ClusterIP` Services for applications
- security groups
- NetworkPolicy
- private subnets
- no per-application public LoadBalancer unless explicitly required

## 32.4 Pod security

For APISIX and controller Pods:

- run as non-root when supported
- drop unnecessary capabilities
- use a read-only root filesystem where compatible
- set seccomp profile
- disable privilege escalation
- pin images by version or digest
- scan images
- apply resource requests and limits

## 32.5 NetworkPolicy model

Conceptual policy:

```text
Internet/NLB -> APISIX gateway ports
APISIX -> application namespaces and approved ports
Ingress Controller -> Kubernetes API
Ingress Controller -> APISIX management endpoint
Monitoring -> metrics endpoint
Nobody else -> APISIX management endpoint
```

Test NetworkPolicy with the actual CNI implementation.

## 32.6 Secrets

Do not store:

- API keys
- JWT signing keys
- OIDC client secrets
- TLS private keys
- Redis passwords
- Admin API keys

in plaintext Git.

Use encryption at rest and least-privilege IAM.

## 32.7 CORS

Do not solve CORS problems by allowing everything.

Risky:

```text
allow_origins = *
allow_credentials = true
```

Define the required origins, methods and headers.

Remember: CORS is a browser security mechanism. It is not authentication for non-browser clients.

## 32.8 Trusted proxies and real client IP

Configure trusted proxy ranges carefully. Trusting arbitrary `X-Forwarded-For` allows clients to spoof their address.

Trust only known load balancer/proxy hops and validate the final real-IP behavior.

## 32.9 Denial-of-service layers

Use multiple layers:

- AWS Shield baseline protections
- perimeter controls where applicable
- load-balancer limits
- APISIX rate and concurrency limiting
- application backpressure
- autoscaling
- dependency protection
- quotas

Autoscaling alone is not a denial-of-service strategy.

---

# 33. High availability and scalability

## 33.1 Multiple gateway replicas

Run at least two replicas for production.

Spread them across:

- nodes
- availability zones
- failure domains

Use topology spread constraints or anti-affinity.

## 33.2 PodDisruptionBudget

A PDB can preserve a minimum number of available gateway replicas during voluntary disruptions.

Example:

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: apisix
  namespace: ingress-apisix
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app.kubernetes.io/name: apisix
```

Verify labels and ensure `minAvailable` is compatible with replica count.

A badly configured PDB can block node maintenance.

## 33.3 Horizontal Pod Autoscaler

Scale on:

- CPU
- memory, with caution
- request rate
- active connections
- latency or queue signals through custom metrics

Example concept:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: apisix
  namespace: ingress-apisix
spec:
  minReplicas: 3
  maxReplicas: 20
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: apisix
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 60
```

CPU may not predict connection or latency saturation perfectly. Load test.

## 33.4 Controller replicas

Controllers commonly use leader election for active reconciliation.

Multiple replicas improve availability, but do not assume all replicas simultaneously program the gateway.

Monitor:

- leader election
- reconcile duration
- reconcile errors
- queue depth
- API throttling

## 33.5 etcd high availability

For traditional or decoupled mode:

- use an odd number of etcd members
- spread across failure domains
- use TLS
- restrict network access
- monitor quorum, disk latency and database size
- take tested snapshots
- understand compaction and defragmentation
- avoid exposing etcd to application networks

## 33.6 Capacity testing

Test:

- requests per second
- concurrent connections
- TLS handshake rate
- response sizes
- long-lived connections
- plugin overhead
- OIDC discovery/JWKS behavior
- Redis rate-limit latency
- logging backpressure
- trace sampling overhead

A benchmark without production plugins is not representative.

---

# 34. Operations, upgrades and disaster recovery

## 34.1 Pin versions

Pin:

- Helm chart
- APISIX image
- Ingress Controller image
- Gateway API CRD version
- plugin runners
- observability dependencies

Avoid unreviewed automatic major upgrades.

## 34.2 Read upgrade guides

The APISIX Ingress Controller 2.x architecture differs from 1.x, and the official upgrade guide documents compatibility changes.

Upgrade sequence can matter, especially in standalone API-driven mode.

## 34.3 Test CRD changes

Before upgrade:

```bash
kubectl get crd -o yaml > crds-before.yaml
kubectl get gateway,httproute -A -o yaml > routes-before.yaml
kubectl get apisixroute,apisixupstream,apisixconsumer,apisixpluginconfig -A -o yaml \
  > apisix-resources-before.yaml
```

Use a non-production cluster to test:

- conversion
- reconciliation
- status conditions
- plugin behavior
- rollback

## 34.4 Configuration backup

In GitOps, Git stores desired Kubernetes configuration, but it may not store:

- generated Secrets
- dynamically created consumers
- out-of-band Admin API changes
- etcd-only state
- runtime certificates

Inventory every source of configuration.

## 34.5 Avoid out-of-band changes

If GitOps is authoritative, direct Admin API changes can be overwritten by reconciliation or become invisible drift.

Define an emergency change procedure:

1. make controlled change
2. record it
3. update Git
4. reconcile
5. remove temporary exception

## 34.6 Disaster recovery questions

Be able to answer:

- Can APISIX restart if etcd is unavailable?
- How is standalone in-memory configuration repopulated?
- Where are TLS private keys restored from?
- Can a new cluster recreate the gateway?
- Are DNS and load-balancer records automated?
- Are consumer credentials recoverable?
- How long is acceptable for route restoration?
- Can a previous chart and CRD version be restored?

## 34.7 Rollback

A Helm rollback may not safely downgrade CRDs or data formats.

Test rollback before production. Sometimes the correct recovery is a forward fix rather than a downgrade.

---

# 35. Troubleshooting methodology

Troubleshoot by layer.

```text
1. DNS
2. AWS load balancer
3. Kubernetes Service
4. APISIX gateway Pod
5. route attachment and match
6. plugin/policy
7. upstream endpoint discovery
8. backend application
9. downstream dependency
```

Do not begin by changing random annotations.

## 35.1 DNS

```bash
dig api.example.com
nslookup api.example.com
```

Check:

- correct record
- expected load-balancer hostname/address
- propagation
- private/public hosted zone
- split-horizon behavior

## 35.2 AWS load balancer

Check:

- listener exists
- target group contains targets
- targets are healthy
- security groups and NACLs allow traffic
- subnets are correct
- scheme is internal/internet-facing as intended
- health-check protocol, port and path

## 35.3 Kubernetes Service

```bash
kubectl get svc apisix-gateway -n ingress-apisix -o wide
kubectl describe svc apisix-gateway -n ingress-apisix
kubectl get endpointslice -n ingress-apisix
```

Check:

- selector matches Pods
- port and targetPort
- Service annotations
- external hostname
- endpoint readiness

## 35.4 APISIX Pods

```bash
kubectl get pods -n ingress-apisix -o wide
kubectl describe pod -n ingress-apisix POD_NAME
kubectl logs -n ingress-apisix POD_NAME
kubectl logs -n ingress-apisix POD_NAME --previous
```

Check:

- readiness
- restarts
- OOMKilled
- configuration errors
- certificate errors
- upstream failures

## 35.5 Controller

```bash
kubectl get pods -n ingress-apisix | grep ingress
kubectl logs -n ingress-apisix deployment/apisix-ingress-controller
```

Check:

- RBAC errors
- unsupported resource version
- reconciliation errors
- APISIX management connection
- invalid PluginConfig
- missing backend Service
- namespace/reference errors

## 35.6 Gateway API status

```bash
kubectl describe gatewayclass apisix
kubectl describe gateway public-api -n gateway-system
kubectl describe httproute orders -n orders
```

Look for conditions such as:

- Accepted
- Programmed
- ResolvedRefs

A route object can exist but not be accepted.

## 35.7 Backend endpoints

```bash
kubectl get svc orders-service -n orders -o yaml
kubectl get endpointslice -n orders -l kubernetes.io/service-name=orders-service
kubectl get pods -n orders --show-labels
```

No endpoints usually means:

- Service selector mismatch
- Pods not Ready
- wrong namespace
- wrong labels
- wrong port naming/reference

## 35.8 Test inside the cluster

```bash
kubectl run curl \
  --rm -it \
  --restart=Never \
  --image=curlimages/curl \
  -- sh
```

Then:

```bash
curl -i http://orders-service.orders.svc.cluster.local:8080/get
```

If direct Service access fails, APISIX is probably not the first problem.

## 35.9 Test the gateway directly

Port-forward:

```bash
kubectl port-forward \
  -n ingress-apisix \
  svc/apisix-gateway \
  9080:80
```

Then:

```bash
curl -i \
  -H 'Host: api.example.com' \
  http://127.0.0.1:9080/orders/get
```

If direct gateway access works but the NLB path fails, focus on AWS/DNS/Service exposure.

---

# 36. Common failure scenarios

## 36.1 404 from APISIX

Possible causes:

- no route matched
- wrong Host header
- wrong path
- HTTPRoute not accepted
- route attached to a different listener
- route configured in another namespace
- APISIX controller has not programmed it

Check:

```bash
kubectl describe httproute -n orders orders
curl -H 'Host: api.example.com' http://GATEWAY/orders/get
```

## 36.2 503 no healthy upstream

Possible causes:

- Service has no endpoints
- Pods not Ready
- wrong backend port
- health checks failing
- NetworkPolicy blocking APISIX
- endpoint discovery/reconciliation failure
- target Pods listening on another port

## 36.3 401 Unauthorized

Possible causes:

- missing key/token
- wrong header
- expired JWT
- wrong issuer/audience
- Consumer not created
- route does not reference expected PluginConfig
- clock skew

## 36.4 403 Forbidden

Possible causes:

- IP restriction
- authorization policy
- consumer restriction
- WAF rule
- mTLS identity not authorized
- route attachment/RBAC policy, depending on layer

## 36.5 429 Too Many Requests

Determine:

- which limiter generated it
- which key is counted
- local or distributed counter
- quota and window
- whether retries are amplifying requests
- whether client IP is actually the load-balancer IP

## 36.6 TLS certificate mismatch

Possible causes:

- wrong SNI hostname
- wrong certificate Secret
- certificate does not include SAN
- route host differs from Gateway hostname
- TLS terminates at another layer
- stale certificate not reloaded
- client DNS points to wrong gateway

## 36.7 NLB targets unhealthy

Possible causes:

- health check points to wrong port
- APISIX Pod not Ready
- security group/NACL issue
- target type mismatch
- health path requires a Host header or authentication
- Service targetPort incorrect

Use a simple unauthenticated gateway health endpoint.

## 36.8 Controller resources exist but traffic does not change

Possible causes:

- wrong controllerName
- multiple controller instances with conflicting ownership
- unsupported CRD version
- invalid resource
- controller cannot reach APISIX
- stale/failed reconciliation
- GitOps reverted the change

## 36.9 Client IP is wrong

Possible causes:

- proxy protocol not configured consistently
- trusting or not trusting forwarded headers
- instance target path changes source address
- externalTrafficPolicy behavior
- multiple proxies

Verify from APISIX logs before using the IP for security.

## 36.10 Configuration works in one replica only

Possible causes:

- standalone programming did not reach every replica
- local rate-limit state differs
- inconsistent ConfigMaps/Secrets
- rollout left old Pods
- controller/provider incompatibility

Query and compare every Pod where possible.

---

# 37. APISIX compared with related technologies

## 37.1 APISIX versus Kubernetes Ingress

| Area | Ingress API | APISIX |
|---|---|---|
| Type | Kubernetes configuration API | Running gateway software |
| Processes traffic | No | Yes |
| Basic host/path routing | Describes it | Implements it |
| Authentication | Not in core API | Plugins |
| Rate limiting | Not in core API | Plugins |
| Consumers | No | Yes |
| Observability | Controller-specific | Extensive plugin support |
| Needs implementation | Yes | APISIX can be the implementation |

## 37.2 APISIX versus Gateway API

| APISIX | Gateway API |
|---|---|
| Gateway implementation | Kubernetes networking API family |
| Receives requests | Describes listeners/routes |
| Runs plugins | Defines standard filters and extension points |
| Selects upstreams | References Kubernetes backends |
| Product/project implementation | Vendor-neutral specification |

They work together.

## 37.3 APISIX versus AWS API Gateway

| Apache APISIX | Amazon API Gateway |
|---|---|
| Open source and self-managed | AWS managed service |
| Runs in Kubernetes/VMs | Runs as AWS service |
| Cloud-neutral | AWS-native |
| You operate scaling/upgrades | AWS operates service infrastructure |
| Plugin extensibility | AWS feature/integration model |
| Can route directly to Pod endpoints through controller | Commonly integrates with Lambda, HTTP endpoints and private integrations |
| Infrastructure cost model | AWS request/feature pricing model |
| Greater runtime control | Lower gateway infrastructure operations burden |

Use APISIX when Kubernetes-native control, portability and extensibility are important.

Use Amazon API Gateway when a managed AWS API front door and AWS integrations are more important than running the gateway inside Kubernetes.

## 37.4 APISIX versus AWS ALB

| APISIX | ALB |
|---|---|
| API gateway and reverse proxy | Managed AWS Layer-7 load balancer |
| Rich plugin model | AWS listener/rule/action model |
| Consumer authentication patterns | AWS-native authentication options |
| Cloud-neutral | AWS-specific |
| Runs as Pods | AWS-managed |
| Fine-grained gateway policy | Excellent AWS load-balancer integration |

An ALB can directly expose EKS applications. APISIX is justified when you need broader API-management behavior or portability.

## 37.5 APISIX versus NLB

They are complementary.

```text
NLB = managed Layer-4 entry point
APISIX = Layer-7 API gateway
```

## 37.6 APISIX versus NGINX Ingress

Both can route Kubernetes traffic.

APISIX is specifically designed as a dynamic API gateway with a broad plugin and consumer model.

A basic NGINX ingress design can be simpler when only routing and TLS are needed.

Also note that the community `ingress-nginx` project entered retirement in March 2026; this does not mean every NGINX-based commercial or open-source controller is the same project.

## 37.7 APISIX versus Kong

Both are mature API-gateway approaches with:

- Kubernetes controllers
- plugins
- authentication
- traffic control
- observability
- enterprise ecosystems

The correct choice depends on:

- required plugins
- operational model
- database/configuration preference
- performance testing
- support model
- team experience
- Gateway API conformance
- migration cost

Avoid choosing only from benchmark headlines.

## 37.8 APISIX versus service mesh

| API gateway | Service mesh |
|---|---|
| Primarily north-south | Primarily east-west |
| External API consumers | Internal workload identities |
| API keys/OIDC/rate limits | mTLS/service policy |
| Public routing | service-to-service traffic |
| API product boundary | workload communication fabric |

They can coexist:

```text
Internet -> APISIX -> service-mesh ingress/internal workloads
```

## 37.9 APISIX versus application code

Do not move all logic into the gateway.

Good gateway logic:

- generic authentication
- coarse authorization
- routing
- rate limiting
- headers
- telemetry
- protocol/policy concerns

Good application logic:

- order ownership
- payment rules
- stock validation
- domain workflow
- transaction consistency

The gateway should not become an undocumented business-logic monolith.

---

# 38. When APISIX is a good choice

APISIX is a strong candidate when:

- many Kubernetes services need a shared entry point
- you need API keys, JWT or OIDC
- you need per-consumer policy
- you need advanced rate limiting
- you need canary or weighted routing
- you want Kubernetes and GitOps configuration
- you need cloud portability
- you need custom plugins
- you need Prometheus/OpenTelemetry integrations
- you need HTTP/gRPC plus selected stream routing
- you want to standardize cross-cutting API concerns
- you are prepared to operate a critical gateway platform

---

# 39. When APISIX may be unnecessary

APISIX may be excessive when:

- there is only one simple web application
- an ALB already meets every requirement
- no API-level authentication or quotas are required
- the team cannot operate another stateful/control component
- a managed AWS service better fits the operating model
- the architecture would place two Layer-7 gateways in series without a clear reason
- application teams will bypass it, making policy incomplete

Every platform component has a cost:

- upgrades
- monitoring
- incident response
- security review
- capacity
- documentation
- training

Use APISIX when its shared value is greater than that operational cost.

---

# 40. Suggested learning path

## Phase 1: Fundamentals

- Understand API, reverse proxy and API gateway.
- Understand north-south versus east-west traffic.
- Understand Kubernetes Service, EndpointSlice and Ingress.
- Understand TLS, DNS and HTTP host/path matching.

## Phase 2: APISIX core

- Route
- Router
- Service
- Upstream
- Consumer
- Credential
- Plugin
- Plugin Config
- SSL
- deployment modes

## Phase 3: Kubernetes control model

- Ingress Controller reconciliation
- GatewayClass
- Gateway
- HTTPRoute
- route status conditions
- cross-namespace routing
- APISIX CRDs and Gateway API extensions

## Phase 4: Security

- API keys
- JWT
- OIDC
- TLS and mTLS
- IP restriction
- CORS
- Admin API hardening
- secret management
- backend isolation

## Phase 5: Traffic and resilience

- load-balancing algorithms
- health checks
- retries
- timeouts
- rate limits
- concurrency
- canary
- circuit breaking

## Phase 6: Observability

- Prometheus
- request logs
- OpenTelemetry
- request IDs
- dashboards
- alerts
- SLOs

## Phase 7: AWS EKS

- AWS Load Balancer Controller
- NLB IP targets
- Route 53
- subnet design
- security groups
- target health
- multi-AZ distribution

## Phase 8: Production operations

- Helm and GitOps
- upgrades
- backups
- disaster recovery
- load testing
- policy validation
- incident troubleshooting

## Practical checklist

- [ ] Install APISIX in a local cluster.
- [ ] Expose a sample Service with `HTTPRoute`.
- [ ] Add rate limiting.
- [ ] Add API-key authentication.
- [ ] Add HTTPS.
- [ ] Inspect Gateway API status conditions.
- [ ] Create two backend versions and split traffic.
- [ ] Export Prometheus metrics.
- [ ] Send traces to an OpenTelemetry Collector.
- [ ] Reproduce a no-endpoints failure.
- [ ] Reproduce a wrong-host 404.
- [ ] Deploy the gateway Service through an EKS NLB.
- [ ] Put route configuration under GitOps.
- [ ] Write an upgrade and rollback plan.
- [ ] Load test with the real plugin set.

---

# 41. Glossary

**API:** A defined interface through which software communicates.

**API gateway:** Software placed in front of APIs to route, secure, control and observe requests.

**APIG:** Informal shorthand for API Gateway; sometimes Amazon API Gateway.

**APISIX:** Apache open-source API gateway.

**Backend:** The application that ultimately processes a request.

**Consumer:** An identified caller of an API in APISIX.

**Control plane:** Components that manage configuration.

**CRD:** Kubernetes CustomResourceDefinition, which adds new Kubernetes API kinds.

**Data plane:** Components that process real application traffic.

**EndpointSlice:** Kubernetes object representing current backend endpoints for a Service.

**Gateway API:** Kubernetes networking APIs including GatewayClass, Gateway and route kinds.

**GatewayClass:** Cluster-scoped class identifying a gateway controller and behavior.

**Gateway:** Requested listener/infrastructure configuration.

**GitOps:** Operating systems through version-controlled desired state and automated reconciliation.

**Ingress:** Kubernetes API for external HTTP/HTTPS routing.

**Ingress Controller:** Controller that implements Ingress and often other routing APIs.

**Listener:** A Gateway port/protocol/hostname entry point.

**mTLS:** Mutual TLS, where client and server authenticate using certificates.

**NLB:** AWS Network Load Balancer.

**OIDC:** OpenID Connect, an identity layer built on OAuth 2.0.

**Plugin:** APISIX extension implementing gateway behavior.

**Route:** A rule matching requests and mapping them to behavior/backends.

**SNI:** TLS Server Name Indication used to select a certificate/virtual host.

**Service, APISIX:** Reusable APISIX API abstraction.

**Service, Kubernetes:** Stable Kubernetes network abstraction selecting Pods.

**Upstream:** APISIX abstraction containing backend nodes and load-balancing behavior.

---

# 42. Official references

The guide was researched primarily from current official documentation. Recheck these pages when installing or upgrading because versions and schemas evolve.

## Apache APISIX

- Main documentation: <https://apisix.apache.org/docs/apisix/>
- Architecture: <https://apisix.apache.org/docs/apisix/architecture-design/apisix/>
- Deployment modes: <https://apisix.apache.org/docs/apisix/deployment-modes/>
- API gateway terminology: <https://apisix.apache.org/docs/apisix/terminology/api-gateway/>
- Route: <https://apisix.apache.org/docs/apisix/terminology/route/>
- Service: <https://apisix.apache.org/docs/apisix/terminology/service/>
- Upstream: <https://apisix.apache.org/docs/apisix/terminology/upstream/>
- Consumer: <https://apisix.apache.org/docs/apisix/terminology/consumer/>
- Plugin: <https://apisix.apache.org/docs/apisix/terminology/plugin/>
- Admin API: <https://apisix.apache.org/docs/apisix/admin-api/>
- Security threat model: <https://apisix.apache.org/docs/apisix/security-threat-model/>
- OpenID Connect plugin: <https://apisix.apache.org/docs/apisix/plugins/openid-connect/>
- JWT authentication: <https://apisix.apache.org/docs/apisix/plugins/jwt-auth/>
- Key authentication: <https://apisix.apache.org/docs/apisix/plugins/key-auth/>
- Rate limiting by count: <https://apisix.apache.org/docs/apisix/plugins/limit-count/>
- Traffic split: <https://apisix.apache.org/docs/apisix/plugins/traffic-split/>
- Proxy rewrite: <https://apisix.apache.org/docs/apisix/plugins/proxy-rewrite/>
- CORS: <https://apisix.apache.org/docs/apisix/plugins/cors/>
- IP restriction: <https://apisix.apache.org/docs/apisix/plugins/ip-restriction/>
- Prometheus plugin: <https://apisix.apache.org/docs/apisix/plugins/prometheus/>
- OpenTelemetry plugin: <https://apisix.apache.org/docs/apisix/plugins/opentelemetry/>

## APISIX Ingress Controller

- Overview: <https://apisix.apache.org/docs/ingress-controller/overview/>
- Getting started: <https://apisix.apache.org/docs/ingress-controller/getting-started/get-apisix-ingress-controller/>
- Configure routes: <https://apisix.apache.org/docs/ingress-controller/getting-started/configure-routes/>
- Deployment architecture: <https://apisix.apache.org/docs/ingress-controller/concepts/deployment-architecture/>
- Resources: <https://apisix.apache.org/docs/ingress-controller/concepts/resources/>
- Gateway API: <https://apisix.apache.org/docs/ingress-controller/concepts/gateway-api/>
- CRD API reference: <https://apisix.apache.org/docs/ingress-controller/reference/apisix-ingress-controller/api-reference/>
- Configuration examples: <https://apisix.apache.org/docs/ingress-controller/reference/apisix-ingress-controller/examples/>
- Upgrade guide: <https://apisix.apache.org/docs/ingress-controller/upgrade-guide/>

## Kubernetes and Gateway API

- Kubernetes Ingress: <https://kubernetes.io/docs/concepts/services-networking/ingress/>
- Kubernetes Gateway API concept: <https://kubernetes.io/docs/concepts/services-networking/gateway/>
- Gateway API documentation: <https://gateway-api.sigs.k8s.io/>
- Gateway API overview: <https://gateway-api.sigs.k8s.io/docs/concepts/api-overview/>
- Gateway API security model: <https://gateway-api.sigs.k8s.io/docs/concepts/security/>
- Cross-namespace routing: <https://gateway-api.sigs.k8s.io/guides/user-guides/multiple-ns/>
- Gateway API implementations: <https://gateway-api.sigs.k8s.io/docs/implementations/list/>
- Gateway API conformance: <https://gateway-api.sigs.k8s.io/docs/concepts/conformance/>

## Amazon EKS and load balancing

- EKS load-balancing best practices: <https://docs.aws.amazon.com/eks/latest/best-practices/load-balancing.html>
- AWS Load Balancer Controller: <https://docs.aws.amazon.com/eks/latest/userguide/aws-load-balancer-controller.html>
- NLB for EKS workloads: <https://docs.aws.amazon.com/eks/latest/userguide/network-load-balancing.html>
- EKS Auto Mode NLB annotations: <https://docs.aws.amazon.com/eks/latest/userguide/auto-configure-nlb.html>
- EKS best-practices guide: <https://docs.aws.amazon.com/eks/latest/best-practices/introduction.html>

---

## Final summary

The shortest accurate model is:

```text
API Gateway
  = architectural function

Apache APISIX
  = gateway software

APISIX Gateway
  = data plane handling client traffic

APISIX Ingress Controller
  = Kubernetes controller programming APISIX

Gateway API
  = standard Kubernetes resource model

AWS NLB
  = managed AWS network entry point in front of APISIX

Kubernetes Service + EndpointSlice
  = application discovery behind APISIX
```

A production request path can be:

```text
Client
  -> Route 53
  -> AWS NLB
  -> APISIX Gateway
  -> authentication and traffic plugins
  -> Kubernetes application Pod
  -> response
```

The separate configuration path can be:

```text
Git
  -> Flux or Argo CD
  -> Kubernetes API
  -> APISIX Ingress Controller
  -> APISIX configuration
```

Understanding the difference between these two paths is the foundation for designing, securing and troubleshooting APISIX correctly.
