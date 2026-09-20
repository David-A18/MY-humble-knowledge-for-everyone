#!/usr/bin/env node

import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import assert from "node:assert/strict";
import { validateRepository } from "./validate-local-links.mjs";

function makeFixture(name, files) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), `kb-link-${name}-`));
  for (const [relativePath, contents] of Object.entries(files)) {
    const fullPath = path.join(root, relativePath);
    fs.mkdirSync(path.dirname(fullPath), { recursive: true });
    fs.writeFileSync(fullPath, contents);
  }
  return root;
}

function run(name, files) {
  return validateRepository(makeFixture(name, files)).errors;
}

assert.deepEqual(
  run("valid", {
    "README.md": "# Root\n\n- [Guide](guides/README.md)\n",
    "guides/README.md": "# Guides\n\n- [Guide one](one.md#details)\n",
    "guides/one.md": "# Guide one\n\n## Details\n\nSee [root][root].\n\n[root]: ../README.md\n",
  }),
  [],
);

assert.match(
  run("broken-target", {
    "README.md": "# Root\n\n[Missing](missing.md)\n",
  }).join("\n"),
  /missing local target/,
);

assert.match(
  run("broken-fragment", {
    "README.md": "# Root\n\n[Guide](guide.md#missing-heading)\n",
    "guide.md": "# Guide\n",
  }).join("\n"),
  /missing heading/,
);

assert.deepEqual(
  run("fenced-link", {
    "README.md": "# Root\n\n```markdown\n[Ignored](missing.md)\n```\n",
  }),
  [],
);

assert.deepEqual(
  run("okf-bundle", {
    "README.md": "# Root\n\n[Knowledge](knowledge/index.md)\n",
    "knowledge/index.md": "# Knowledge\n\n[Guide](guides/index.md)\n",
    "knowledge/guides/index.md": "# Guides\n\n[Guide](one.md)\n",
    "knowledge/guides/one.md": "# Guide\n",
  }),
  [],
);

console.log("Local link validator fixtures passed.");
