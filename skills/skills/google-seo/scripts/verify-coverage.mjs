import path from "node:path";
import { promises as fs } from "node:fs";
import { ROOT, readJson } from "./lib.mjs";

const URLS = path.join(ROOT, "urls.json");
const DOCS = path.join(ROOT, "docs");
const REFS = path.join(ROOT, "references");
const LINK_RE = /\]\((<?)([^)>\s]+)>?\)/g;

async function exists(p) {
  try {
    await fs.access(p);
    return true;
  } catch {
    return false;
  }
}

async function walk(dir) {
  const out = [];
  let ents = [];
  try {
    ents = await fs.readdir(dir, { withFileTypes: true });
  } catch {
    return out;
  }
  for (const e of ents) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) out.push(...(await walk(p)));
    else if (p.endsWith(".md")) out.push(p);
  }
  return out;
}

async function validate(files) {
  let ok = 0;
  let broken = 0;
  let remote = 0;
  const brokenList = [];
  for (const f of files) {
    const txt = await fs.readFile(f, "utf8");
    for (const m of txt.matchAll(LINK_RE)) {
      const t = m[2];
      if (/^(https?:|mailto:|#|\/)/i.test(t)) {
        remote += 1;
        continue;
      }
      const target = path.normalize(path.join(path.dirname(f), t.split("#")[0]));
      if (await exists(target)) ok += 1;
      else {
        broken += 1;
        if (brokenList.length < 20) brokenList.push(`${f} -> ${t}`);
      }
    }
  }
  return { ok, broken, remote, brokenList };
}

async function main() {
  const { urls = [] } = (await readJson(URLS, { urls: [] })) || {};

  const missing = [];
  for (const u of urls) {
    if (u.hasMarkdown === false) continue;
    if (!(await exists(path.join(DOCS, `${u.path}.md`)))) missing.push(u.path);
  }

  console.log("== Coverage ==");
  console.log(`  urls: ${urls.length}`);
  console.log(`  missing local markdown: ${missing.length}`);
  for (const m of missing.slice(0, 20)) console.log(`    MISSING ${m}`);

  const docFiles = await walk(DOCS);
  const refFiles = await walk(REFS);
  const docLinks = await validate(docFiles);
  const refLinks = await validate(refFiles);

  console.log("\n== Links ==");
  console.log(`  docs: ${docFiles.length} files — ${docLinks.ok} local ok, ${docLinks.broken} broken, ${docLinks.remote} remote`);
  console.log(`  references: ${refFiles.length} files — ${refLinks.ok} local ok, ${refLinks.broken} broken, ${refLinks.remote} remote`);
  for (const b of docLinks.brokenList) console.log(`    BROKEN ${b}`);
  for (const b of refLinks.brokenList) console.log(`    BROKEN ${b}`);

  const pass = missing.length === 0 && docLinks.broken === 0 && refLinks.broken === 0;
  console.log(`\n${pass ? "PASS" : "FAIL"}`);
  process.exit(pass ? 0 : 1);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
