---
type: Explanation
title: Model Context Protocol
description: Understand how an AI application uses MCP to ask another program for information or an action, and where the protocol's responsibility ends.
tags: [ai, ai-tooling, model-context-protocol]
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
  - id: mcp-architecture
    resource: https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture
    title: MCP architecture overview
  - id: mcp-base
    resource: https://modelcontextprotocol.io/specification/2026-07-28/basic/index
    title: MCP base protocol
  - id: mcp-tools
    resource: https://modelcontextprotocol.io/specification/2026-07-28/server/tools
    title: MCP tools
  - id: mcp-resources
    resource: https://modelcontextprotocol.io/specification/2026-07-28/server/resources
    title: MCP resources
  - id: mcp-transports
    resource: https://modelcontextprotocol.io/specification/2026-07-28/basic/transports
    title: MCP transports
  - id: mcp-typescript-sdk
    resource: https://ts.sdk.modelcontextprotocol.io/v2/api/@modelcontextprotocol/server/
    title: MCP TypeScript server SDK v2
---

# Model Context Protocol

## The simple idea

**Model Context Protocol (MCP)** is a shared way for an AI application to
request information or an action from another program. For example, an AI
assistant could ask a knowledge server to search articles, then use the
returned article to answer a reader's question. MCP defines the exchange
between the programs; the server still decides where its information comes
from and what a caller may access.[^mcp-architecture][^mcp-base]

Think of a library desk. You ask the assistant a question; it sends a
request to the library desk, which finds a relevant page and returns it.
That picture helps explain the direction of the request. It stops there:
MCP does not make the returned page accurate, grant permission to enter
every collection, or choose how the assistant explains the page.

## The three participants

| Participant | Plain-language role | In the knowledge example |
| --- | --- | --- |
| **Host** | The AI application you use. It coordinates its connections. | The assistant where you ask a question. |
| **Client** | The part of that host that talks to one MCP server. | The connection that sends the assistant's search request. |
| **Server** | A program that offers information or operations. It can run locally or remotely. | A service that searches the knowledge articles. |

A host can have several clients, each connected to a different server.
The server is the provider of the capability; it is not necessarily a
large remote machine.[^mcp-architecture]

```mermaid
flowchart LR
  person["Reader"] --> host["AI host"]
  host --> client["MCP client"]
  client <-->|"MCP messages"| server["MCP server"]
  server --> corpus["Knowledge articles"]
```

Text alternative: the reader asks the AI host. A client inside that host
exchanges MCP messages with a server. In this example, the server reads
knowledge articles and returns a result to the host.

## What a server can offer

MCP groups common server capabilities into three useful kinds. A server
may offer one, two, or all three.[^mcp-base]

| Capability | What you can ask for | Knowledge example |
| --- | --- | --- |
| **Tool** | Run a named operation with inputs and receive a result. | `search_knowledge` takes a query and returns matching article IDs. |
| **Resource** | Read content identified by a URI. | `kb://terraform/state` identifies a readable article. |
| **Prompt** | Get a reusable prompt template. | A template could ask the host to explain an article for a beginner. |

A tool can read or change something, depending on what the server
implements. The word *tool* alone does not mean an operation is safe or
read-only. A resource is content offered for reading; a prompt is a
template, not an automatic answer.[^mcp-tools][^mcp-resources]

## Follow one question

Imagine a reader asking, “What does Terraform state do?” The following
is an **illustrative design**, not a running server:

1. The host's MCP client calls a `search_knowledge` tool with
   `{"query": "Terraform state"}`.
2. The server searches its allowed articles and returns a few titles,
   stable IDs, and the knowledge revision it searched.
3. The client requests the selected article, perhaps through a resource
   URI such as `kb://terraform/state`, if that server exposes one.
4. The host uses the returned content to explain state and can cite the
   article and its source revision.

MCP carries those requests and responses. It does not prescribe Git,
Markdown, a database, or any particular search algorithm behind the
server. It also cannot guarantee that the selected article is correct
or that the model will explain it well. Those need source review and
answer evaluation.[^mcp-architecture][^mcp-tools][^mcp-resources]

For this repository, [Terraform state management](../../terraform/fundamentals/state-management.md)
is a real article. The sample URI and tool name above are only examples;
this page does not claim that this repository has a live MCP server.

## The boundaries that matter

| Question | Short answer |
| --- | --- |
| How do messages travel? | A local server can use `stdio`; a remote server can use Streamable HTTP. The transport changes delivery, not the meaning of a tool or resource.[^mcp-transports] |
| Does a connection remember the conversation? | In MCP version 2026-07-28, each request supplies the information needed to process it. A server must not infer conversation state from earlier requests on the same connection. If work spans requests, the client passes an explicit identifier.[^mcp-base] |
| Who checks access? | The server must validate and authorize what it serves or changes. A tool description or a `readOnlyHint` is descriptive metadata, not an access-control rule.[^mcp-tools] |
| Who decides whether to use a result? | The host controls its user interaction and what context it gives the model. MCP does not define the model's reasoning or the final answer.[^mcp-architecture] |

If a server offers both `search_knowledge` and `edit_article`,
the write operation needs its own permission checks and a clear user
decision. Returning an article through MCP never authorizes editing it.

## Check your understanding

- In the question example, which participant owns the knowledge
  articles, and which participant gives the final answer?
- Would changing from local `stdio` to remote HTTP make an article
  trustworthy by itself? Why?
- If a tool says it is read-only, what must the server still check?

## Explore further

- Read the [MCP architecture overview](https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture)
  for the host, client, and server relationship.[^mcp-architecture]
- Read the [base protocol](https://modelcontextprotocol.io/specification/2026-07-28/basic/index),
  [tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools),
  and [resources](https://modelcontextprotocol.io/specification/2026-07-28/server/resources)
  specifications when designing an integration.[^mcp-base][^mcp-tools][^mcp-resources]
- For current implementation examples, start with the
  [TypeScript server SDK v2](https://ts.sdk.modelcontextprotocol.io/v2/api/@modelcontextprotocol/server/).
  Its v2 release replaces the older monolithic TypeScript package used
  by earlier recipes.[^mcp-typescript-sdk]
- For this repository's design, continue to
  [Agent knowledge bases](knowledge-bases/index.md) and
  [Create AI tools for Claude and Codex](create-ai-tools-for-claude-and-codex.md).

[^mcp-architecture]: [MCP architecture overview](https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture), source record `mcp-architecture`.
[^mcp-base]: [MCP base protocol, version 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/basic/index), source record `mcp-base`.
[^mcp-tools]: [MCP tools specification](https://modelcontextprotocol.io/specification/2026-07-28/server/tools), source record `mcp-tools`.
[^mcp-resources]: [MCP resources specification](https://modelcontextprotocol.io/specification/2026-07-28/server/resources), source record `mcp-resources`.
[^mcp-transports]: [MCP transports overview](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports), source record `mcp-transports`.
[^mcp-typescript-sdk]: [MCP TypeScript server SDK v2](https://ts.sdk.modelcontextprotocol.io/v2/api/@modelcontextprotocol/server/), source record `mcp-typescript-sdk`.
