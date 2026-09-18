#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const defaultIgnoredParts = [
  ".git",
  "node_modules",
  "sources/incoming",
  "sources/processed",
];

const portableBundlePrefix = "ai/ai-tooling/knowledge-bases/examples/okf-v0.2/";

function toPosix(filePath) {
  return filePath.split(path.sep).join("/");
}

function withoutFenceBlocks(markdown) {
  const lines = markdown.split(/\r?\n/);
  let fenced = false;
  let fenceMarker = "";

  return lines
    .map((line) => {
      const match = line.match(/^(\s*)(`{3,}|~{3,})/);
      if (match) {
        const marker = match[2][0];
        if (!fenced) {
          fenced = true;
          fenceMarker = marker;
        } else if (marker === fenceMarker) {
          fenced = false;
          fenceMarker = "";
        }
        return "";
      }
      return fenced ? "" : line;
    })
    .join("\n");
}

function githubSlug(text, used) {
  let slug = text
    .trim()
    .toLowerCase()
    .replace(/<[^>]+>/g, "")
    .replace(/[`*_~]/g, "")
    .replace(/[^\p{L}\p{N}\s-]/gu, "")
    .replace(/\s+/g, "-")
    .replace(/-+/g, "-");

  const base = slug;
  let suffix = 0;
  while (used.has(slug)) {
    suffix += 1;
    slug = `${base}-${suffix}`;
  }
  used.add(slug);
  return slug;
}

function collectHeadings(markdown) {
  const headings = new Set();
  const used = new Set();
  const cleaned = withoutFenceBlocks(markdown);

  for (const line of cleaned.split(/\r?\n/)) {
    const match = line.match(/^(#{1,6})\s+(.+?)\s*#*\s*$/);
    if (match) {
      headings.add(githubSlug(match[2], used));
    }
  }

  return headings;
}

function walkMarkdown(root, ignoredParts = defaultIgnoredParts) {
  const files = [];

  function visit(dir) {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const fullPath = path.join(dir, entry.name);
      const rel = toPosix(path.relative(root, fullPath));
      if (ignoredParts.some((part) => rel === part || rel.startsWith(`${part}/`))) {
        continue;
      }
      if (entry.isDirectory()) {
        visit(fullPath);
      } else if (entry.isFile() && entry.name.endsWith(".md")) {
        files.push(rel);
      }
    }
  }

  visit(root);
  return files.sort();
}

function isExternal(destination) {
  return /^(https?:|mailto:|tel:|ftp:)/i.test(destination);
}

function normalizeDestination(rawDestination) {
  return rawDestination
    .trim()
    .replace(/^<|>$/g, "")
    .split(/\s+/)[0];
}

function splitDestination(destination) {
  const hashIndex = destination.indexOf("#");
  if (hashIndex === -1) {
    return { target: destination, fragment: "" };
  }
  return {
    target: destination.slice(0, hashIndex),
    fragment: destination.slice(hashIndex + 1),
  };
}

function extractLinks(markdown) {
  const cleaned = withoutFenceBlocks(markdown);
  const links = [];
  const referenceDefinitions = new Map();
  const lines = cleaned.split(/\r?\n/);

  for (let index = 0; index < lines.length; index += 1) {
    const line = lines[index];
    const def = line.match(/^\s*\[([^\]]+)]:\s*(\S+)/);
    if (def) {
      referenceDefinitions.set(def[1].trim().toLowerCase(), normalizeDestination(def[2]));
      continue;
    }

    const inlinePattern = /(?<!!)\[[^\]]+\]\(([^)]+)\)/g;
    for (const match of line.matchAll(inlinePattern)) {
      links.push({
        line: index + 1,
        destination: normalizeDestination(match[1]),
      });
    }

    const referencePattern = /(?<!!)\[([^\]]+)\]\[([^\]]*)\]/g;
    for (const match of line.matchAll(referencePattern)) {
      const label = (match[2] || match[1]).trim().toLowerCase();
      if (referenceDefinitions.has(label)) {
        links.push({
          line: index + 1,
          destination: referenceDefinitions.get(label),
        });
      }
    }
  }

  return links;
}

function resolveLocalTarget(root, sourceRel, rawTarget) {
  const sourceDir = path.dirname(path.join(root, sourceRel));
  const decoded = decodeURIComponent(rawTarget);
  const candidate = rawTarget
    ? path.resolve(sourceDir, decoded)
    : path.resolve(root, sourceRel);

  if (!candidate.startsWith(root)) {
    return { fullPath: candidate, rel: toPosix(path.relative(root, candidate)), exists: false };
  }

  if (fs.existsSync(candidate) && fs.statSync(candidate).isDirectory()) {
    const readme = path.join(candidate, "README.md");
    return {
      fullPath: readme,
      rel: toPosix(path.relative(root, readme)),
      exists: fs.existsSync(readme),
    };
  }

  return {
    fullPath: candidate,
    rel: toPosix(path.relative(root, candidate)),
    exists: fs.existsSync(candidate),
  };
}

export function validateRepository(rootDirectory) {
  const root = path.resolve(rootDirectory);
  const markdownFiles = walkMarkdown(root);
  const markdownSet = new Set(markdownFiles);
  const headingsByFile = new Map();
  const graph = new Map(markdownFiles.map((file) => [file, new Set()]));
  const errors = [];

  for (const file of markdownFiles) {
    const markdown = fs.readFileSync(path.join(root, file), "utf8");
    headingsByFile.set(file, collectHeadings(markdown));
  }

  for (const file of markdownFiles) {
    const markdown = fs.readFileSync(path.join(root, file), "utf8");
    for (const link of extractLinks(markdown)) {
      const destination = link.destination;
      if (!destination || isExternal(destination)) {
        continue;
      }

      const { target, fragment } = splitDestination(destination);
      const resolved = resolveLocalTarget(root, file, target);

      if (!resolved.exists) {
        errors.push(`${file}:${link.line} missing local target ${destination}`);
        continue;
      }

      if (resolved.rel.endsWith(".md") && markdownSet.has(resolved.rel)) {
        graph.get(file).add(resolved.rel);
      }

      if (fragment && resolved.rel.endsWith(".md") && markdownSet.has(resolved.rel)) {
        const slug = decodeURIComponent(fragment).toLowerCase();
        if (!headingsByFile.get(resolved.rel).has(slug)) {
          errors.push(`${file}:${link.line} missing heading #${fragment} in ${resolved.rel}`);
        }
      }
    }
  }

  for (const file of markdownFiles) {
    const dir = path.dirname(file);
    if (file.startsWith(portableBundlePrefix)) {
      continue;
    }
    if (dir !== "." && !dir.startsWith(".github") && path.basename(file) !== "README.md") {
      const readme = toPosix(path.join(dir, "README.md"));
      if (!markdownSet.has(readme)) {
        errors.push(`${file}: documentation directory is missing README.md`);
      }
    }
  }

  const reachable = new Set();
  const queue = markdownSet.has("README.md") ? ["README.md"] : [];
  while (queue.length > 0) {
    const current = queue.shift();
    if (reachable.has(current)) {
      continue;
    }
    reachable.add(current);
    for (const next of graph.get(current) || []) {
      if (!reachable.has(next)) {
        queue.push(next);
      }
    }
  }

  for (const file of markdownFiles) {
    if (file.startsWith(portableBundlePrefix)) {
      continue;
    }
    if (!reachable.has(file)) {
      errors.push(`${file}: not reachable from README.md through local Markdown links`);
    }
  }

  return {
    filesChecked: markdownFiles.length,
    errors,
  };
}

function main() {
  const rootArg = process.argv[2] || process.cwd();
  const result = validateRepository(rootArg);

  if (result.errors.length > 0) {
    for (const error of result.errors) {
      console.error(error);
    }
    console.error(`Checked ${result.filesChecked} Markdown files; ${result.errors.length} local link errors.`);
    process.exitCode = 1;
    return;
  }

  console.log(`Checked ${result.filesChecked} Markdown files; local links, fragments, indexes, and reachability passed.`);
}

const currentFile = fileURLToPath(import.meta.url);
if (process.argv[1] && path.resolve(process.argv[1]) === currentFile) {
  main();
}
