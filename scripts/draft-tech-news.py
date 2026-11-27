"""Draft Markdown briefs from corroborated upstream release records."""
import argparse
from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
import re
import sys
from urllib.parse import quote, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener
from zoneinfo import ZoneInfo

import yaml

PROJECTS = {
    "openai/codex": ("Codex", ["ai", "ai-tools", "coding-agents"]),
    "anthropics/claude-code": ("Claude Code", ["ai", "ai-tools", "coding-agents"]),
    "modelcontextprotocol/typescript-sdk": ("MCP TypeScript SDK", ["ai-tools", "mcp"]),
    "modelcontextprotocol/ruby-sdk": ("MCP Ruby SDK", ["ai-tools", "mcp"]),
    "vercel-labs/skills": ("Vercel Skills", ["ai-tools", "agent-skills"]),
    "huggingface/transformers": ("Transformers", ["ai", "ml"]),
    "kubernetes/kubernetes": ("Kubernetes", ["kubernetes", "platform-engineering"]),
    "hashicorp/terraform": ("Terraform", ["terraform", "infrastructure"]),
    "docker/compose": ("Docker Compose", ["docker", "devops"]),
}
GITHUB = "https://api.github.com/repos/"
TAG = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,89}\Z")
PROMPT = Path("governance/news-automation-instructions.md")


class SameOriginRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        origin = urlsplit(req.full_url)
        target = urlsplit(newurl)
        if (origin.scheme, origin.netloc) != (target.scheme, target.netloc):
            raise ValueError("Refusing to forward a token across origins")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def request(url, token, data=None):
    headers = {
        "Authorization": f"Bearer {token}", "User-Agent": "knowledge-news-editor",
        "Accept": "application/json", "Content-Type": "application/json",
    }
    req = Request(url, data=json.dumps(data).encode() if data else None, headers=headers)
    limit = 12_000_000 if url.startswith(GITHUB) else 2_000_000
    with build_opener(SameOriginRedirect()).open(req, timeout=25) as response:
        body = response.read(limit + 1)
    if len(body) > limit:
        raise ValueError("Source response exceeded the size limit")
    return json.loads(body)


def collect(now, token, known):
    candidates = []
    for repo, (name, tags) in PROJECTS.items():
        releases = request(f"{GITHUB}{repo}/releases?per_page=8", token)
        for release in releases:
            tag, published = release["tag_name"], release["published_at"]
            if release["draft"] or release["prerelease"] or not published or not TAG.fullmatch(tag):
                continue
            stamp = datetime.fromisoformat(published)
            url = f"https://github.com/{repo}/releases/tag/{tag}"
            if not now - timedelta(hours=36) <= stamp <= now or url in known or release["html_url"] != url:
                continue
            notes = (release.get("body") or "").strip()
            if not notes:
                continue
            commit = request(f"{GITHUB}{repo}/commits/{quote(tag, safe='')}", token)
            sha = commit["sha"]
            if not re.fullmatch(r"[a-f0-9]{40}", sha):
                raise ValueError(f"Invalid commit for {repo} {tag}")
            candidates.append({
                "name": name, "repo": repo, "tag": tag, "tags": tags, "published": published,
                "url": url, "commit": f"https://github.com/{repo}/commit/{sha}", "notes": notes[:6500],
            })
    return sorted(candidates, key=lambda item: item["published"], reverse=True)[:14]


def select(candidates, token, model):
    reply = request("https://api.openai.com/v1/chat/completions", token, {
        "model": model, "response_format": {"type": "json_object"},
        "max_completion_tokens": 2500,
        "messages": [
            {"role": "system", "content": PROMPT.read_text(encoding="utf-8")},
            {"role": "user", "content": json.dumps(list(enumerate(candidates)))},
        ],
    })
    output = json.loads(reply["choices"][0]["message"]["content"])["briefs"]
    if not isinstance(output, list) or len(output) > 2:
        raise ValueError("Expected at most two briefs")
    used = set()
    for item in output:
        idx = item["index"]
        if type(idx) is not int or not 0 <= idx < len(candidates) or idx in used:
            raise ValueError("Invalid or duplicate candidate index")
        used.add(idx)
        for field in ("change", "impact", "next_step"):
            value = item[field]
            if not isinstance(value, str) or not 15 <= len(value) <= 280 or re.search(r"[<>\[\]`\r\n]|https?://", value):
                raise ValueError(f"Expected short plain text in {field}")
        yield candidates[idx], item


def write(path, value):
    path.write_text(value, encoding="utf-8", newline="\n")


def add_link(index, link, header=None):
    content = index.read_text(encoding="utf-8")
    if link in content.splitlines():
        return
    if header and header in content:
        content = content.replace(header + "\n", header + "\n\n" + link + "\n", 1)
    else:
        marker = re.search(r"(?m)^\[Back to .+\]\(", content)
        position = marker.start() if marker else len(content)
        block = (header + "\n\n" if header else "") + link + "\n\n"
        content = content[:position].rstrip() + "\n\n" + block + content[position:]
    write(index, content)


def render(today, candidate, item):
    root = Path("knowledge/news")
    year = root / today.strftime("%Y")
    month = year / today.strftime("%m")
    month.mkdir(parents=True, exist_ok=True)
    date_label = today.strftime("%B %Y")
    if not (year / "index.md").exists():
        write(year / "index.md", f"# {today.year}\n\n[Back to news](../index.md)\n")
    if not (month / "index.md").exists():
        write(month / "index.md", f"# {date_label}\n\n[Back to {today.year}](../index.md)\n")
    slug = re.sub(r"[^a-z0-9]+", "-", f"{candidate['repo']}-{candidate['tag']}".lower()).strip("-")
    path = month / f"{slug}.md"
    if path.exists():
        raise ValueError(f"Brief already exists: {path}")
    title = f"{candidate['name']} {candidate['tag']} released"
    source_date = candidate["published"][:10]
    meta = {
        "type": "News Brief", "title": title, "description": item["change"],
        "tags": ["news", "open-source", *candidate["tags"]], "status": "draft",
        "audience": "Engineering learners and practitioners", "maintainer": "unassigned",
        "published": today, "stale_after": today + timedelta(days=90),
        "sources": [
            {"id": "release", "resource": candidate["url"], "title": f"{title} notes"},
            {"id": "tagged-commit", "resource": candidate["commit"], "title": "Upstream commit resolved from the release tag"},
        ],
    }
    write(path, f"""---
{yaml.safe_dump(meta, sort_keys=False, allow_unicode=True).rstrip()}
---

# {title}

## What happened

Upstream published this release on {source_date}.[^release][^tagged-commit]
{item["change"]}[^release]

## Why it matters

{item["impact"]}[^release]

## What to do

{item["next_step"]}[^release]

## Related links

- [Monthly index](index.md)
- [News](../../index.md)
- [Knowledge home](../../../index.md)

[^release]: [Upstream release notes]({candidate["url"]})
[^tagged-commit]: [Commit resolved from the release tag]({candidate["commit"]})
""")
    add_link(month / "index.md", f"- [{title}]({path.name})", "## Upstream release briefs")
    if f"({month.name}/index.md)" not in (year / "index.md").read_text(encoding="utf-8"):
        add_link(year / "index.md", f"- [{date_label}]({month.name}/index.md)")
    news_index = root / "index.md"
    if f"({year.name}/index.md)" not in news_index.read_text(encoding="utf-8"):
        add_link(news_index, f"- [{year.name}]({year.name}/index.md)", "### Archive")
    add_link(news_index, f"- [{date_label} upstream releases]({year.name}/{month.name}/index.md#upstream-release-briefs)", "## Upstream release coverage")
    print(path.as_posix())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--discover-only", action="store_true")
    args = parser.parse_args()
    now = datetime.now(timezone.utc)
    catalog = json.loads(Path("generated/knowledge-catalog.json").read_text(encoding="utf-8"))
    # The Markdown preserves full source URLs even when catalog records only carry source IDs.
    known = set()
    for record in catalog["concepts"]:
        if record["type"] == "News Brief":
            body = Path(record["path"]).read_text(encoding="utf-8")
            known.update(re.findall(r"https://github\.com/[^\s)]+", body))
    candidates = collect(now, os.environ["GH_TOKEN"], known)
    print(f"Corroborated candidates: {len(candidates)}")
    if args.discover_only or not candidates:
        for item in candidates:
            print(item["url"], item["commit"])
        return
    token = os.environ.get("OPENAI_API_KEY")
    if not token:
        sys.exit("Set the repository OPENAI_API_KEY secret before enabling brief generation.")
    today = now.astimezone(ZoneInfo("Europe/Madrid")).date()
    drafts = list(select(candidates, token, os.environ.get("NEWS_MODEL") or "gpt-5-mini"))
    for candidate, item in drafts:
        render(today, candidate, item)


if __name__ == "__main__":
    main()
