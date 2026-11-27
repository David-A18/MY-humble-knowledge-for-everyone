---
type: News Brief
title: Ruby MCP SDK adds support for Agent Skills
description: Ruby MCP SDK 1.9.0 adds a way for servers to publish skills and clients to discover and verify them.
tags: [news, ai, ai-tools, agent-skills, mcp, open-source, ruby]
status: draft
audience: Engineering learners and practitioners
maintainer: unassigned
published: 2026-11-26
stale_after: 2027-02-26
sources:
  - id: ruby-sdk
    resource: https://github.com/modelcontextprotocol/ruby-sdk/blob/main/CHANGELOG.md
    title: Ruby MCP SDK 1.9.0 changelog
  - id: skills-wg
    resource: https://github.com/modelcontextprotocol/modelcontextprotocol/discussions/3502
    title: MCP Skills working group notes for 3 November 2026
---

# Ruby MCP SDK adds support for Agent Skills

## What happened

On 3 November 2026, the Ruby Model Context Protocol (MCP) SDK recorded
support for the Skills extension in version 1.9.0. The release lets a server
publish Agent Skills from a directory or handler. The client can list and
read those skills and check them against the digests in the
manifest.[^ruby-sdk]

## Why it matters

A team working in Ruby can evaluate distributing reusable agent instructions
through an MCP server. The working group classified the extension as beta,
so check compatibility with the client and server versions you plan to use
before depending on it.[^ruby-sdk][^skills-wg]

## What to do

For a first trial, choose a small skill and check whether the intended client
can discover and read it. Review the skill's contents and permissions before
using it. A matching digest verifies the contents against a manifest and
should be one step in that review.[^ruby-sdk]

## Related links

- [November 2026](index.md)
- [News](../../index.md)
- [Knowledge home](../../../index.md)

[^ruby-sdk]: [Ruby MCP SDK 1.9.0 changelog](https://github.com/modelcontextprotocol/ruby-sdk/blob/main/CHANGELOG.md)
[^skills-wg]: [MCP Skills working group notes for 3 November 2026](https://github.com/modelcontextprotocol/modelcontextprotocol/discussions/3502)
