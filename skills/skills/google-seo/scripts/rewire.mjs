import path from "node:path";
import { promises as fs } from "node:fs";
import { ROOT, readJson, writeAtomic } from "./lib.mjs";

const MANIFEST = path.join(ROOT, "assets", "manifest.json");
const DOCS = path.join(ROOT, "docs");
const MARKER = "<!-- google-seo-images -->";
const MD_IMG_RE = /!\[([^\]]*)\]\(\s*<?([^)>\s]+)>?(?:\s+["'][^"']*["'])?\s*\)/g;
const HTML_IMG_RE = /(<img\b[^>]*?\bsrc\s*=\s*")([^"]+)(")/gi;

function toPosix(p) {
  return p.split(path.sep).join("/");
}

async function main() {
  if (process.argv.includes("--text-only")) {
    console.log("text-only mode: no image rewriting (docs keep Google's remote image URLs).");
    return;
  }
  const manifest = await readJson(MANIFEST, null);
  if (!manifest) {
    console.error("assets/manifest.json missing. Run fetch-images.mjs first.");
    process.exit(1);
  }

  // URL -> absolute local file, for successfully downloaded images.
  const map = new Map();
  for (const im of manifest.images || []) {
    if (!im.error && im.local) map.set(im.src, im.local);
  }

  let changed = 0;
  let unresolved = 0;
  const unresolvedSet = new Set();

  for (const [pagePath, page] of Object.entries(manifest.pages)) {
    const docFile = path.join(DOCS, `${pagePath}.md`);
    let body;
    try {
      body = await fs.readFile(docFile, "utf8");
    } catch {
      continue;
    }
    // Remove block written by earlier versions of this script.
    const mIdx = body.indexOf(MARKER);
    if (mIdx !== -1) body = body.slice(0, mIdx).replace(/\s+$/, "\n");

    const dir = path.dirname(docFile);
    const rel = (absLocal) => toPosix(path.relative(dir, path.join(ROOT, absLocal)));

    let touched = false;
    body = body.replace(MD_IMG_RE, (whole, alt, url) => {
      const local = map.get(url);
      if (!local) {
        if (/^https?:/i.test(url)) {
          unresolved += 1;
          unresolvedSet.add(url);
        }
        return whole;
      }
      touched = true;
      return `![${alt}](<${rel(local)}>)`;
    });
    body = body.replace(HTML_IMG_RE, (whole, pre, url, post) => {
      const local = map.get(url);
      if (!local) return whole;
      touched = true;
      return `${pre}${rel(local)}${post}`;
    });

    if (touched) {
      await writeAtomic(docFile, body.endsWith("\n") ? body : body + "\n");
      changed += 1;
    }
  }

  console.log(`rewired ${changed} markdown file(s) to local images`);
  if (unresolvedSet.size) {
    console.log(`unresolved remote images (not downloaded): ${unresolvedSet.size}`);
    for (const u of [...unresolvedSet].slice(0, 10)) console.log(`  - ${u}`);
  }
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
