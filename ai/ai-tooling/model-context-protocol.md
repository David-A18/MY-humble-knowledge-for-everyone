# Model Context Protocol

## Purpose

This guide explains what Model Context Protocol is and how to design MCP servers that expose useful, safe tools and context to AI applications.

## When to use this

Use MCP when an AI host needs a reusable connection to live context, private systems, local files, product APIs, or controlled actions. Use direct function calling when the tools only exist inside one application runtime. Use a skill when the model mainly needs reusable instructions rather than a live integration.

## Core model

| Component | Meaning |
| --- | --- |
| Host | The AI application the user interacts with, such as Claude, Claude Code, Codex, ChatGPT, an IDE, or a custom agent. |
| Client | The MCP connection inside the host. It sends requests and receives responses. |
| Server | The local process or remote service that exposes capabilities to the host. |
| Tool | A callable operation for actions, queries, computations, or side effects. |
| Resource | Readable context such as files, schemas, records, documents, or generated views. |
| Prompt | A reusable prompt template exposed by the server. |

MCP messages follow JSON-RPC 2.0. Current MCP guidance treats requests as stateless: servers should not infer user, task, protocol, capability, or conversation context from an earlier request on the same connection. If state needs to span requests, pass an explicit ID, handle, cursor, task ID, or resource URI.

## Transports

| Transport | Use it for | Notes |
| --- | --- | --- |
| `stdio` | Local servers launched by the host. | Read credentials from the local environment; keep logs out of stdout because stdout carries protocol messages. |
| Streamable HTTP | Remote servers reached over the network. | Authenticate and authorize every request; do not rely on connection continuity. |

Transport changes how messages move. It does not change what a tool, resource, or prompt means.

## Server capabilities

### Tools

Tools should represent user goals, not raw backend endpoints.

Good examples:

- `search_knowledge`
- `fetch_knowledge_entry`
- `github_list_pull_requests`
- `jira_create_issue`
- `run_readonly_query`

Avoid a generic `execute` or `do_everything` tool. It hides risk and makes tool routing harder.

Tool definitions should include:

| Field | Good practice |
| --- | --- |
| Name | Stable, verb-object, and namespaced when the server has many domains. |
| Title | Human-readable display name. |
| Description | Explain what the tool does, when to use it, when not to use it, and what it returns. |
| Input schema | Use JSON Schema, preferably 2020-12 when no explicit dialect is required. |
| Output schema | Return predictable structured results where the host or model may continue from the output. |
| Annotations | Mark read-only, destructive, or open-world behavior truthfully. |

### Resources

Resources are for context the host can read. Use resources when nothing needs to be computed or changed.

Useful resources:

- `file://` or `kb://` Markdown documents.
- API schemas.
- Database table definitions.
- OKF concept documents.
- Project metadata.
- Runbook pages.

Use stable resource URIs. They make citations, logs, cache entries, and troubleshooting easier.

### Prompts

Prompts are reusable templates exposed by a server. They are useful for compact, common flows such as "summarize this issue with linked PRs" or "prepare a release note from these commits." For larger workflows with references and scripts, use a skill and let the MCP server supply the live data.

## Design workflow

1. List the user jobs the integration should support.
2. Separate read operations from write operations.
3. Decide which data should be resources and which operations should be tools.
4. Give each tool a precise name, description, input schema, and output shape.
5. Add server-side auth checks for every request.
6. Add allowlists for file paths, API scopes, resource IDs, and write targets.
7. Add dry-run or propose-only tools before write tools.
8. Test tool selection, schema validation, error handling, and approval boundaries.

## Minimal TypeScript MCP server

```bash
npm install @modelcontextprotocol/sdk zod
```

What it does: installs the official TypeScript SDK and `zod` for schemas.

```ts
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer(
  { name: "knowledge-tools", version: "1.0.0" },
  {
    instructions:
      "Use search_knowledge before fetch_knowledge_entry. Write tools require explicit user intent.",
  },
);

server.registerTool(
  "search_knowledge",
  {
    title: "Search Knowledge",
    description:
      "Search curated Markdown knowledge entries. Use this before fetching a specific entry. Returns stable IDs, titles, paths, and short summaries.",
    inputSchema: {
      query: z.string().min(1),
      limit: z.number().int().min(1).max(10).default(5),
    },
    outputSchema: {
      results: z.array(
        z.object({
          id: z.string(),
          title: z.string(),
          path: z.string(),
          summary: z.string(),
        }),
      ),
    },
    annotations: { readOnlyHint: true },
  },
  async ({ query, limit }) => {
    const results = await searchMarkdownIndex(query, limit);

    return {
      content: [{ type: "text", text: JSON.stringify({ results }) }],
      structuredContent: { results },
    };
  },
);

server.registerResource(
  "mcp-guide",
  "kb://ai/ai-tooling/model-context-protocol",
  {
    title: "Model Context Protocol",
    description: "Guide to MCP concepts and server design.",
    mimeType: "text/markdown",
  },
  async (uri) => ({
    contents: [
      {
        uri: uri.href,
        mimeType: "text/markdown",
        text: await readKnowledgeEntry("ai/ai-tooling/model-context-protocol.md"),
      },
    ],
  }),
);

await server.connect(new StdioServerTransport());
```

What it does: exposes one read-only search tool and one Markdown resource over `stdio`. The helper functions are intentionally left as application code.

## Minimal Python MCP server

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("knowledge-tools", json_response=True)


@mcp.tool()
def search_knowledge(query: str, limit: int = 5) -> list[dict]:
    """Search curated Markdown knowledge entries by query."""
    return search_markdown_index(query=query, limit=limit)


@mcp.resource("kb://entry/{entry_id}")
def fetch_knowledge_entry(entry_id: str) -> str:
    """Fetch a Markdown knowledge entry by stable ID."""
    return read_knowledge_entry(entry_id)


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
```

What it does: creates a Python MCP server with a search tool and a dynamic resource URI over Streamable HTTP.

## Safety rules

> [!WARNING]
> Never let a tool accept arbitrary file paths, shell commands, raw SQL, or raw patches from a model unless the server applies strict allowlists, validation, authorization, and audit logging.

- Validate all inputs on the server, even if the host validates schemas.
- Treat tool descriptions as routing hints, not security controls.
- Split read-only tools from write tools.
- Require explicit user intent for writes, deletes, external messages, purchases, permission changes, or public actions.
- Return machine-readable errors such as `not_found`, `unauthorized`, `validation_failed`, and `conflict`.
- Log who requested the action, the tool name, input IDs, output IDs, and whether a write occurred.

## Troubleshooting

| Symptom | Likely cause | Next step |
| --- | --- | --- |
| Model calls the wrong tool | Names or descriptions overlap. | Add service prefixes and clearer "use when" guidance. |
| Tool is overused | Description is too broad or system prompt says to always use tools. | Narrow the description and make tool use conditional. |
| Tool is skipped | Missing instruction or weak description. | Add a task-specific instruction and stronger examples. |
| Schema errors are frequent | Required fields or enums do not match user language. | Add descriptions, examples, defaults, and validation messages. |
| Remote server behaves inconsistently | Server relies on connection state. | Pass explicit IDs and authenticate every request. |

## Related links

- Official documentation: [MCP overview](https://modelcontextprotocol.io/specification/2026-07-28/basic/index)
- Official documentation: [MCP tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)
- Official documentation: [MCP resources](https://modelcontextprotocol.io/specification/2026-07-28/server/resources)
- Official documentation: [OpenAI MCP server guide](https://developers.openai.com/plugins/build/mcp-server)
- [Create AI tools for Claude and Codex](create-ai-tools-for-claude-and-codex.md)
- [Knowledge-base creation, management, and optimization](knowledge-bases-creation-management-and-optimization.md)
- [Back to AI tooling](README.md)
- [Back to AI index](../README.md)
- [Back to root index](../../README.md)
