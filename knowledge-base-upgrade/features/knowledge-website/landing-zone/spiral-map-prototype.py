"""Build the knowledge-spiral data map used by the landing zone prototype.

Usage: python3 spiral-map-prototype.py generated/knowledge-catalog.json data.json
Prototype only: the website will own the real spiral map and check it at build time.
"""
import json, sys
catalog = json.load(open(sys.argv[1]))['concepts']
REPO = "https://github.com/David-A18/MY-humble-knowledge-for-everyone/blob/main/"

def area(path):
    return path.split('/')[1:]

# (spiral id, title, [(loop id, loop title, predicate)])
def starts(*prefixes):
    return lambda p: any(p.startswith('knowledge/' + x) for x in prefixes)

SPIRALS = [
  ("ai", "AI", [
    ("ai-tools", "AI tools & MCP", lambda p: p.startswith('knowledge/ai/') and '/knowledge-bases/' not in p),
    ("knowledge-bases", "Knowledge bases", starts('ai/ai-tooling/knowledge-bases/')),
    ("rag", "RAG", starts('llm/')),
  ]),
  ("cloud", "Cloud & Platform", [
    ("aws", "AWS", starts('cloud/aws/')),
    ("kubernetes", "Kubernetes", starts('kubernetes/')),
    ("terraform", "Terraform", starts('terraform/')),
    ("git", "Git", starts('git/')),
    ("devops", "DevOps", starts('devops/')),
    ("finops", "FinOps", starts('finops/')),
    ("databases", "Databases", starts('databases/')),
    ("migrations", "Migrations", starts('migrations/')),
    ("security", "Security", starts('security/')),
    ("multicloud", "Multi-cloud & edge", starts('cloud/edge/', 'cloud/gcloud/', 'cloud/solutions/', 'cloud/azure/')),
    ("guides", "Cross-topic guides", starts('cross-topic-guides/')),
    ("architecture", "Architecture & languages", starts('solutions-architect/', 'programming-languages/')),
  ]),
  ("news", "Tech News", [
    ("news-ai", "AI news", lambda p: False),
    ("news-security", "Security news", lambda p: False),
    ("news-economy", "Economy", lambda p: False),
  ]),
]
LIBRARY = starts('start-here', 'glossary', 'decision-records/', 'templates/')

def page(c):
    d = c['description'].strip()
    if len(d) > 150:
        d = d[:147].rsplit(' ', 1)[0] + '…'
    return {"t": c['title'], "d": d, "s": c['status'], "ty": c['type'], "u": REPO + c['path']}

out = {"spirals": [], "library": []}
used = set()
for sid, stitle, loops in SPIRALS:
    s = {"id": sid, "title": stitle, "loops": []}
    for lid, ltitle, pred in loops:
        pages = []
        for c in catalog:
            p = c['path']
            if p in used: continue
            ok = pred(p)
            if sid == 'news' and p.startswith('knowledge/news/'):
                tags = c['tags']
                cat = 'news-ai' if 'ai' in tags else 'news-security' if 'security' in tags else 'news-economy' if 'economy' in tags else None
                ok = cat == lid
            if ok:
                pages.append(page(c)); used.add(p)
        pages.sort(key=lambda x: x['t'].lower())
        s["loops"].append({"id": lid, "title": ltitle, "pages": pages})
    out["spirals"].append(s)
for c in catalog:
    if c['path'] not in used and LIBRARY(c['path']):
        out["library"].append(page(c)); used.add(c['path'])
missing = [c['path'] for c in catalog if c['path'] not in used]
print("unplaced:", missing, file=sys.stderr)
for s in out['spirals']:
    print(s['id'], [(l['id'], len(l['pages'])) for l in s['loops']], file=sys.stderr)
print("library", len(out['library']), file=sys.stderr)
json.dump(out, open(sys.argv[2], 'w'), ensure_ascii=False, separators=(',', ':'))
