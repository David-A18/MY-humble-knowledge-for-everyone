# AI tooling

AI tooling guidance for MCP servers, Claude and Codex custom tools, skills, and agent-ready knowledge bases.

## Reader path

| Guide | Start here when |
| --- | --- |
| [Model Context Protocol](model-context-protocol.md) | You need to understand MCP hosts, clients, servers, tools, resources, prompts, transports, schemas, and server design. |
| [Create AI tools for Claude and Codex](create-ai-tools-for-claude-and-codex.md) | You need to expose custom actions, APIs, files, skills, or MCP servers to Claude, Claude Code, Codex, or OpenAI tools. |
| [Knowledge-base creation, management, and optimization](knowledge-bases-creation-management-and-optimization.md) | You need to build Markdown, retrieval, vector-store, or OKF knowledge bases that agents can search, cite, and maintain. |

## How the pieces fit

| Layer | Best fit |
| --- | --- |
| Tool | A callable capability such as `search_knowledge`, `create_ticket`, or `run_query`. |
| MCP server | A standard way to expose tools, resources, and prompts to AI hosts. |
| Skill | A reusable Markdown workflow with optional references, scripts, and assets. |
| Knowledge base | Durable facts, runbooks, schemas, decisions, and examples for humans and agents. |
| Retrieval index | A search layer over a knowledge base when the full corpus is too large for prompt context. |

Use the smallest surface that solves the problem. A prompt is enough for one-off behavior, a skill is better for repeatable workflow guidance, an MCP server is better for live tools and data, and a curated knowledge base is better for durable reference material.

## Related links

- [Back to AI index](../README.md)
- [Back to AI agents index](../../ai-agents/README.md)
- [Back to LLM index](../../llm/README.md)
- [Back to root index](../../README.md)
