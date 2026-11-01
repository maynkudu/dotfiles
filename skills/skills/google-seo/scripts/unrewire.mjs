import path from "node:path";
import { promises as fs } from "node:fs";
import { ROOT, readJson, writeAtomic } from "./lib.mjs";

const MANIFEST = path.join(ROOT, "assets", "manifest.json");
const DOCS = path.join(ROOT, "docs");
const MD_IMG_RE = /!\[([^\]]*)\]\(\s*<?([^)>\s]+)>?(?:\s+["'][^"']*["'])?\s*\)/g;

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

async function main() {
  const manifest = await readJson(MANIFEST, null);
  if (!manifest) {
    console.error("assets/manifest.json not found; nothing to un-rewire.");
    process.exit(1);
  }

  const map = new Map(); // absolute local path -> source URL
  for (const im of manifest.images || []) {
    if (im.error || !im.local || !im.src) continue;
    map.set(path.join(ROOT, im.local), im.src);
  }
  console.log(`reverse map: ${map.size} local files -> source URLs`);

  const files = await walk(DOCS);
  let restored = 0;
  let changedFiles = 0;

  for (const f of files) {
    const body = await fs.readFile(f, "utf8");
    let touched = false;
    const out = body.replace(MD_IMG_RE, (whole, alt, href) => {
      if (/^https?:/i.test(href)) return whole;
      const abs = path.normalize(path.join(path.dirname(f), href));
      const src = map.get(abs);
      if (!src) return whole;
      touched = true;
      restored += 1;
      return `![${alt}](${src})`;
    });
    if (touched) {
      await writeAtomic(f, out);
      changedFiles += 1;
    }
  }

  console.log(`restored ${restored} image link(s) across ${changedFiles} file(s) to remote URLs`);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
