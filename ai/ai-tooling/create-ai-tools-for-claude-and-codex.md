# Create AI tools for Claude and Codex

## Purpose

This guide explains how to design custom AI tools for Claude, Claude Code, Codex, and OpenAI workflows. It focuses on practical choices: function tools, MCP servers, skills, Markdown instructions, and platform-specific configuration.

## When to use this

| Need | Prefer |
| --- | --- |
| One application needs the model to call known backend functions | Function tools or Claude client tools. |
| Multiple agents or products need the same tools and data | MCP server. |
| A coding agent needs repeatable workflow guidance | `SKILL.md`, `AGENTS.md`, `CLAUDE.md`, or project rules. |
| A tool should operate on private workspace data | MCP server or approved connector with explicit auth. |
| A model should create free-form commands for a deterministic executor | Custom tool with grammar or strict executor-side parser. |

Do not start by exposing every backend endpoint. Start with the user job and design the smallest safe tool surface that completes it.

## Shared tool design rules

| Rule | Why it matters |
| --- | --- |
| Use clear names | Models route better when names encode service and action. |
| Write detailed descriptions | Claude documentation emphasizes detailed descriptions as the strongest driver of tool-use performance. |
| Validate with schemas | JSON Schema catches malformed requests before execution. |
| Return stable IDs | Follow-up calls, citations, and audits need durable references. |
| Keep outputs small | Return what the model needs for the next decision, not full API payloads. |
| Split read and write tools | Read-only workflows should not inherit write risk. |
| Add explicit errors | The model can recover from `not_found`, `conflict`, or `unauthorized`; it cannot recover from vague failures. |

## Claude API tools

Claude API tools are passed in the `tools` parameter. For client tools, Claude emits `tool_use` blocks, your application executes the function, and you send back a `tool_result`.

### Define a Claude client tool

```python
tools = [
    {
        "name": "kb_search",
        "description": (
            "Search the curated engineering knowledge base. Use this when the user "
            "asks for repository guidance, operational procedures, or technical "
            "reference material that may exist in the knowledge base. Returns "
            "stable entry IDs, titles, paths, and short summaries. Does not modify files."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search phrase using the user's topic and likely aliases.",
                },
                "limit": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 10,
                    "default": 5,
                },
            },
            "required": ["query"],
        },
        "strict": True,
    }
]
```

What it does: defines a strict Claude client tool with a detailed description and bounded input schema.

### Handle the tool-use loop

```python
response = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=1024,
    tools=tools,
    tool_choice={"type": "auto"},
    messages=[{"role": "user", "content": "Find the EKS workload identity guide."}],
)

tool_use = next(block for block in response.content if block.type == "tool_use")
result = kb_search(**tool_use.input)

messages = [
    {"role": "user", "content": "Find the EKS workload identity guide."},
    {"role": "assistant", "content": response.content},
    {
        "role": "user",
        "content": [
            {
                "type": "tool_result",
                "tool_use_id": tool_use.id,
                "content": result,
            }
        ],
    },
]
```

What it does: executes the client tool in application code and returns the result to Claude for the final answer.

### Claude tool choices

| `tool_choice` | Behavior |
| --- | --- |
| `auto` | Claude decides whether to call a tool. |
| `any` | Claude must call one available tool. |
| `tool` | Claude must call a specific tool. |
| `none` | Claude cannot call tools. |

Use `auto` for most workflows. Use forced tool calls only when the user explicitly needs fresh external data or the application contract requires a tool result.

## Claude Code tools and skills

Claude Code can use project memory, skills, commands, subagents, permissions, and MCP servers.

| Surface | Use it for |
| --- | --- |
| `CLAUDE.md` | Durable project memory, conventions, commands, and repository-specific context. |
| `.claude/skills/<name>/SKILL.md` | Repeatable task workflows that should load only when relevant. |
| `.claude/commands/*.md` | Legacy custom commands; current Claude Code guidance treats skills as the preferred richer format. |
| `/mcp` | Manage MCP server connections and OAuth authentication inside Claude Code. |
| `/permissions` | Control allow, ask, and deny rules for tool execution. |

### Claude Code skill example

```markdown
---
name: summarize-changes
description: Summarizes uncommitted changes and flags risky edits. Use when the user asks what changed or wants a commit summary.
---

## Current changes

!`git diff HEAD`

## Instructions

Summarize the changes in two or three bullets. Then list risks such as missing validation, missing tests, hardcoded values, or unsafe operations. If the diff is empty, say there are no uncommitted changes.
```

What it does: defines a Markdown skill that injects live Git diff context before Claude reads the instructions.

> [!IMPORTANT]
> Keep `SKILL.md` focused. Put long reference material in supporting files and link to it so the agent loads details only when needed.

## Codex tools and customization

Codex uses several surfaces that should not be mixed blindly.

| Surface | Use it for |
| --- | --- |
| Prompt or current task | One-off constraints and goals. |
| `AGENTS.md` | Durable repository instructions, validation steps, routing, and contribution expectations. |
| `.codex/config.toml` | Trusted-repo Codex settings, including MCP and environment behavior where supported. |
| Skill | Reusable workflow with `SKILL.md`, references, scripts, and assets. |
| Plugin | Packaged capabilities that can include skills, MCP config, apps, hooks, and assets. |
| MCP server or connector | Live external data, private workspace systems, or actions. |

### Codex skill shape

```text
knowledge-curator/
  SKILL.md
  references/
    source-quality.md
    markdown-style.md
  scripts/
    check-links.js
  assets/
    article-template.md
```

What it does: packages reusable workflow instructions with supporting references and deterministic helper scripts.

### Codex repository guidance

Use `AGENTS.md` for repository-wide rules:

```markdown
# Repository instructions

- Read `context.md`, `instructions.md`, and `CONTRIBUTING.md` before documentation edits.
- Use relative links for internal Markdown links.
- Update parent indexes and `CHANGELOG.md` when adding pages.
- Run `git status --short --branch` and Markdown validation before committing.
```

What it does: gives Codex durable project rules that apply before editing.

## MCP for Claude and Codex

MCP is the best shared integration layer when both Claude and Codex need the same external tools.

Recommended server shape:

| Tool | Behavior |
| --- | --- |
| `search_knowledge` | Read-only search over curated docs. |
| `fetch_knowledge_entry` | Read-only fetch by stable ID. |
| `propose_knowledge_update` | Generates a patch without applying it. |
| `modify_knowledge_entry` | Applies a validated write only inside allowlisted paths. |

> [!WARNING]
> Put write tools behind server-side authorization, path allowlists, conflict checks, lint checks, and audit logging. Model intent is not an access-control mechanism.

## Testing checklist

- Test whether the model selects the right tool for common and ambiguous prompts.
- Test missing required fields and malformed arguments.
- Test unauthorized access and verify the tool returns a clear error.
- Test stale IDs and update conflicts.
- Test large outputs and trim them to useful summaries plus IDs.
- Test write tools in dry-run mode before allowing writes.
- Track tool call success rate, invalid schema rate, retry count, latency, and user corrections.

## Troubleshooting

| Symptom | Likely cause | Next step |
| --- | --- | --- |
| Claude does not call the tool | Description does not explain when to use it. | Add concrete "use when" and "do not use when" guidance. |
| Claude calls too many tools | Tool set is too broad or forced tool use is overused. | Use `auto`, reduce exposed tools, and route by task. |
| Codex repeats repository instructions | Same rule appears in prompts, `AGENTS.md`, and skills. | Keep durable repo rules in one place and skills focused on workflows. |
| Tool outputs are hard to use | Results lack stable IDs or are too verbose. | Return concise summaries, IDs, paths, URLs, and next actions. |
| Write tool is risky | Tool accepts broad target paths or raw commands. | Add allowlists, dry-run mode, confirmation requirements, and audit logs. |

## Related links

- Official documentation: [Claude tool use](https://platform.claude.com/docs/claude/docs/tool-use)
- Official documentation: [Claude define tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools)
- Official documentation: [Claude Code skills](https://code.claude.com/docs/en/slash-commands)
- Official documentation: [Codex customization](https://learn.chatgpt.com/docs/customization/overview)
- Official documentation: [OpenAI function calling](https://developers.openai.com/api/docs/guides/function-calling)
- Official documentation: [OpenAI skills guide](https://developers.openai.com/plugins/build/skills)
- [Model Context Protocol](model-context-protocol.md)
- [Knowledge-base creation, management, and optimization](knowledge-bases-creation-management-and-optimization.md)
- [Back to AI tooling](README.md)
- [Back to AI index](../README.md)
- [Back to root index](../../README.md)
