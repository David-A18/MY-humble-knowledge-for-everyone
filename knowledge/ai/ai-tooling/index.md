# AI tooling

AI tooling guidance for MCP servers, Claude and Codex custom tools, skills, and agent-ready knowledge bases.

## Reader path

| Guide | Start here when |
| --- | --- |
| [Model Context Protocol](model-context-protocol.md) | You want a beginner explanation of how an AI application reaches a server for information or an action, and what MCP does not guarantee. |
| [Create AI tools for Claude and Codex](create-ai-tools-for-claude-and-codex.md) | Choose a function tool, shared MCP server, or agent skill by following one simple knowledge lookup. |
| [Knowledge-base creation, management, and optimization](knowledge-bases-creation-management-and-optimization.md) | You want to see how a simple, sourced article becomes a page people can find, and how new topics fit into the bundle. |
| [Agent knowledge bases](knowledge-bases/index.md) | You need the full Git-backed, standards-aware reference architecture for AI agent knowledge systems. |
| [Knowledge-base upgrade hub](../../../knowledge-base-upgrade/README.md) | You need the repository-specific upgrade plan for features, tools, skills, MCP server templates, and instructions. |

## How the pieces fit

| Layer | Best fit |
| --- | --- |
| Tool | A callable capability such as `search_knowledge`, `create_ticket`, or `run_query`. |
| MCP server | A standard way to expose tools, resources, and prompts to AI hosts. |
| Skill | A reusable Markdown workflow with optional references, scripts, and assets. |
| Knowledge base | Durable facts, runbooks, schemas, decisions, and examples for humans and agents. |
| Retrieval index | A disposable search layer over a knowledge base when the full corpus is too large for prompt context. |
| OKF bundle | A portable Markdown and YAML-frontmatter knowledge package with provenance, trust, lifecycle, freshness, and optional attestation metadata. |

Use the smallest surface that solves the problem. A prompt is enough for one-off behavior, a skill is better for repeatable workflow guidance, an MCP server is better for live tools and data, and a curated knowledge base is better for durable reference material.

## Related links

- [Back to AI index](../index.md)
- [Back to AI agents index](../../ai-agents/index.md)
- [Back to LLM index](../../llm/index.md)
- [Back to knowledge index](../../index.md)
