import path from "node:path";
import { promises as fs } from "node:fs";
import {
  ROOT,
  readJson,
  writeJson,
  mapLimit,
  fetchText,
  ensureDir,
  writeAtomic,
  getHtml,
  htmlToMarkdown,
  normalizeUrl,
  CACHE,
} from "./lib.mjs";

const URLS = path.join(ROOT, "urls.json");
const DOCS = path.join(ROOT, "docs");
const META = path.join(DOCS, "_meta.json");
const ETAGS = path.join(CACHE, "md-etags.json");

function looksLikeHtml(body, contentType = "") {
  if (/text\/html/i.test(contentType)) return true;
  if (/markdown|text\/plain/i.test(contentType)) return false;
  return /^\s*(<!doctype\s+html|<html[\s>])/i.test(body.slice(0, 200));
}

/**
 * Some docs pages have no `.md.txt` rendering but a live HTML page (e.g. the
 * crawlable `web-bot-auth` page). Convert the article HTML to markdown so the
 * page isn't lost. Redirect aliases (final URL differs) are skipped, since the
 * canonical page is captured separately.
 */
async function htmlFallback(u) {
  const html = await getHtml(u.url);
  if (!html.ok || !html.body) return null;
  const finalUrl = normalizeUrl(html.url || u.url);
  if (finalUrl && finalUrl !== u.url) return { alias: finalUrl };
  const md = htmlToMarkdown(html.body);
  if (md.replace(/\s/g, "").length < 200) return null;
  return { body: md, canonical: finalUrl || u.url };
}
async function main() {
  const { urls = [] } = (await readJson(URLS, { urls: [] })) || {};
  if (!urls.length) {
    console.error("urls.json is empty or missing. Run discover.mjs first.");
    process.exit(1);
  }
  const refresh = process.argv.includes("--refresh");
  const etags = (await readJson(ETAGS, {})) || {};
  const only = process.argv.find((a) => a.startsWith("--only="))?.slice("--only=".length);
  const aliases = !process.argv.includes("--no-aliases");

  const targets = urls.filter((u) => !only || u.path.includes(only));
  console.log(`fetching ${targets.length} markdown file(s)...`);

  const meta = await readJson(META, { pages: {} });
  meta.pages = meta.pages || {};

  let saved = 0;
  let skipped = 0;
  let unchanged = 0;
  let aliasSaved = 0;
  const dead = new Set();

  await mapLimit(targets, 6, async (u) => {
    const mdUrl = `${u.url}.md.txt`;
    const headers = {};
    if (!refresh && etags[u.url]) headers["If-None-Match"] = etags[u.url];
    const res = await fetchText(mdUrl, { headers, accept: "text/markdown,text/plain;q=0.9,*/*;q=0.5" });

    const dest = path.join(DOCS, `${u.path}.md`);
    const entry = { url: u.url, mdUrl, path: u.path, section: u.section, category: u.category };

    if (res.status === 304) {
      unchanged += 1;
      entry.status = 304;
      meta.pages[u.path] = { ...meta.pages[u.path], ...entry };
      return;
    }
    const mdOk = res.status === 200 && res.body && !looksLikeHtml(res.body, res.contentType);
    if (mdOk) {
      await ensureDir(path.dirname(dest));
      await writeAtomic(dest, res.body.endsWith("\n") ? res.body : res.body + "\n");
      if (res.etag) etags[u.url] = res.etag;
      saved += 1;
      meta.pages[u.path] = {
        ...meta.pages[u.path],
        ...entry,
        status: 200,
        hasDoc: true,
        bytes: res.body.length,
      };
      return;
    }

    // No markdown rendering: try HTML (either convert, or resolve a legacy alias).
    const fb = await htmlFallback(u);
    if (fb && fb.body) {
      await ensureDir(path.dirname(dest));
      await writeAtomic(dest, fb.body.endsWith("\n") ? fb.body : fb.body + "\n");
      saved += 1;
      meta.pages[u.path] = {
        ...meta.pages[u.path],
        ...entry,
        status: 200,
        hasDoc: true,
        source: "html-fallback",
        bytes: fb.body.length,
      };
      console.log(`  html->md ${u.path}`);
      return;
    }
    if (fb && fb.alias && aliases) {
      const a = await fetchText(`${fb.alias}.md.txt`, {
        accept: "text/markdown,text/plain;q=0.9,*/*;q=0.5",
      });
      if (a.status === 200 && a.body && !looksLikeHtml(a.body, a.contentType)) {
        const header = `# (Moved) ${u.url}\n\n> This legacy URL now redirects to ${fb.alias}.\n> Canonical content mirrored below.\n\n`;
        await ensureDir(path.dirname(dest));
        await writeAtomic(dest, header + a.body.replace(/^\s+/, ""));
        aliasSaved += 1;
        meta.pages[u.path] = {
          ...meta.pages[u.path],
          ...entry,
          status: 200,
          hasDoc: true,
          source: "alias",
          aliasOf: fb.alias,
        };
        console.log(`  alias->md ${u.path} -> ${fb.alias}`);
        return;
      }
    }
    if (fb && fb.alias) {
      meta.pages[u.path] = { ...meta.pages[u.path], ...entry, status: 0, hasDoc: false, error: `alias of ${fb.alias}` };
      skipped += 1;
      dead.add(u.path);
      return;
    }
    skipped += 1;
    dead.add(u.path);
    entry.status = res.status || 0;
    entry.error = res.error || "not available";
    meta.pages[u.path] = { ...meta.pages[u.path], ...entry, hasDoc: false };
    if (u.category === "docs") console.log(`  skip [${entry.status}] ${u.path}`);
  });

  await writeJson(ETAGS, etags);
  meta.generatedAt = new Date().toISOString();
  meta.counts = { saved, unchanged, skipped, aliasSaved, attempted: targets.length };
  await writeJson(META, meta);

  // Keep urls.json truthful: anything that produced no document has no markdown.
  if (dead.size) {
    const store = (await readJson(URLS, { urls: [] })) || { urls: [] };
    let changed = 0;
    for (const u of store.urls) {
      if (dead.has(u.path) && u.hasMarkdown !== false) {
        u.hasMarkdown = false;
        changed += 1;
      }
    }
    if (changed) await writeJson(URLS, store);
  }

  console.log(`done: ${saved} saved (${aliasSaved} alias stubs), ${unchanged} unchanged, ${skipped} skipped -> docs/`);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
