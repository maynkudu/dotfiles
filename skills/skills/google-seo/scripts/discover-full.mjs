import path from "node:path";
import { promises as fs } from "node:fs";
import zlib from "node:zlib";
import {
  ROOT,
  ORIGIN,
  UA,
  CACHE,
  normalizeUrl,
  urlToPath,
  sectionOf,
  isDocPageUrl,
  readJson,
  writeJson,
  mapLimit,
  writeAtomic,
} from "./lib.mjs";

const URLS = path.join(ROOT, "urls.json");
const SITEMAP_CACHE = path.join(CACHE, "sitemap-locs.json.gz");
const PROBE_CACHE = path.join(CACHE, "md-probe.json");

const SITEMAP_INDEX = `${ORIGIN}/sitemap.xml`;

const CATEGORY_RULES = [
  [/^search\/docs(\/|$)/, "docs"],
  [/^crawling\/docs(\/|$)/, "docs"],
  [/^search\/blog(\/|$)/, "blog"],
  [/^search\/help(\/|$)/, "help"],
  [/^search\/updates(\/|$)/, "updates"],
  [/^search\/case-studies(\/|$)/, "case-studies"],
  [/^search\/events(\/|$)/, "events"],
  [/^search\/apis(\/|$)/, "apis"],
  [/^search\/podcasts(\/|$)/, "podcasts"],
  [/^search\/news(\/|$)/, "news"],
];

function categoryOf(p) {
  for (const [re, cat] of CATEGORY_RULES) if (re.test(p)) return cat;
  return "other";
}

const BINARY_EXT_RE = /\.(png|jpe?g|gif|svg|webp|avif|ico|bmp|pdf|xml|txt|json|zip|gz|csv|mp4|webm|css|js)$/i;

async function getText(url, timeoutMs = 300000) {
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), timeoutMs);
  try {
    const res = await fetch(url, { headers: { "User-Agent": UA }, redirect: "follow", signal: ctrl.signal });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.text();
  } finally {
    clearTimeout(t);
  }
}

async function loadSitemapLocs(refresh) {
  if (!refresh) {
    try {
      const buf = await fs.readFile(SITEMAP_CACHE);
      const locs = JSON.parse(zlib.gunzipSync(buf).toString("utf8"));
      console.log(`sitemap (cached): ${locs.length} locs`);
      return locs;
    } catch {
      /* miss */
    }
  }
  console.log("fetching sitemap index...");
  const indexXml = await getText(SITEMAP_INDEX, 60000);
  const shards = [...indexXml.matchAll(/<loc>([^<]+)<\/loc>/g)]
    .map((m) => m[1].trim())
    .filter((u) => /sitemap_\d+_of_\d+\.xml$/.test(u));
  console.log(`sitemap shards: ${shards.length}`);

  const all = [];
  let done = 0;
  await mapLimit(shards, 8, async (shard) => {
    try {
      const xml = await getText(shard);
      for (const m of xml.matchAll(/<loc>([^<]+)<\/loc>/g)) all.push(m[1].trim());
    } catch (err) {
      console.error(`  shard failed ${path.basename(shard)}: ${err}`);
    } finally {
      done += 1;
      if (done % 8 === 0 || done === shards.length) console.log(`  ${done}/${shards.length} shards`);
    }
  });

  await writeAtomic(SITEMAP_CACHE, zlib.gzipSync(Buffer.from(JSON.stringify(all), "utf8")));
  console.log(`sitemap locs: ${all.length} (cached)`);
  return all;
}

async function main() {
  const refresh = process.argv.includes("--refresh");
  const prefixes = (process.argv.find((a) => a.startsWith("--prefix="))?.slice(9) || "search/docs,crawling/docs")
    .split(",")
    .map((s) => s.trim())
    .filter(Boolean);
  const exclude = new Set(
    (process.argv.find((a) => a.startsWith("--exclude="))?.slice(10) || "")
      .split(",")
      .map((s) => s.trim())
      .filter(Boolean)
  );
  const limit = Number(process.argv.find((a) => a.startsWith("--limit="))?.slice(8) || 0) || 0;

  const locs = await loadSitemapLocs(refresh);

  const pages = new Map(); // url -> {path, category}
  for (const loc of locs) {
    let u;
    try {
      u = new URL(loc);
    } catch {
      continue;
    }
    if (u.hostname !== "developers.google.com") continue;
    const p = u.pathname.replace(/\/+$/, "").replace(/^\//, "");
    if (!prefixes.some((pre) => p === pre || p.startsWith(`${pre}/`))) continue;
    if (BINARY_EXT_RE.test(p)) continue;
    const n = normalizeUrl(loc);
    if (!n) continue;
    const np = urlToPath(n);
    const cat = categoryOf(np);
    if (exclude.has(cat)) continue;
    if (!pages.has(n)) pages.set(n, { url: n, path: np, section: sectionOf(n), category: cat });
  }
  console.log(`candidate pages (${prefixes.join(",")}): ${pages.size}`);

  // Probe .md.txt availability (cached).
  const probe = (await readJson(PROBE_CACHE, {})) || {};
  const entries = [...pages.values()];
  const todo = entries.filter((e) => refresh || !(e.url in probe));
  const limitList = limit ? todo.slice(0, limit) : todo;
  console.log(`probing .md.txt for ${limitList.length} pages (cached: ${Object.keys(probe).length})...`);

  let n = 0;
  await mapLimit(limitList, 8, async (e) => {
    const res = await fetch(`${e.url}.md.txt`, {
      headers: { "User-Agent": UA, Accept: "text/markdown,text/plain;q=0.9,*/*;q=0.5" },
      redirect: "follow",
    }).catch(() => null);
    let ok = false;
    if (res && res.ok) {
      const ct = res.headers.get("content-type") || "";
      if (/markdown|text\/plain/i.test(ct)) ok = true;
      else {
        const body = await res.text();
        ok = !/^\s*(<!doctype\s+html|<html[\s>])/i.test(body.slice(0, 200));
      }
    } else if (res) {
      await res.text().catch(() => {});
    }
    probe[e.url] = ok ? 1 : 0;
    n += 1;
    if (n % 200 === 0) console.log(`  probed ${n}/${limitList.length}`);
  });
  await writeJson(PROBE_CACHE, probe);

  let hasMd = 0;
  const existing = (await readJson(URLS, { urls: [] })) || { urls: [] };
  const byUrl = new Map((existing.urls || []).map((u) => [u.url, u]));
  for (const e of entries) {
    const md = probe[e.url] === 1;
    if (md) hasMd += 1;
    const prev = byUrl.get(e.url) || {};
    byUrl.set(e.url, { ...prev, ...e, hasMarkdown: md, crawled: prev.crawled ?? false, source: "sitemap" });
  }

  const urls = [...byUrl.values()].sort((a, b) => a.path.localeCompare(b.path));
  await writeJson(URLS, { generatedAt: new Date().toISOString(), count: urls.length, urls });

  const byCat = {};
  for (const u of urls) {
    const c = u.category || categoryOf(u.path);
    byCat[c] = byCat[c] || { total: 0, md: 0 };
    byCat[c].total += 1;
    if (u.hasMarkdown) byCat[c].md += 1;
  }
  console.log(`\nurls.json now ${urls.length} pages (${hasMd} with markdown):`);
  for (const c of Object.keys(byCat).sort()) console.log(`  ${c.padEnd(14)} ${byCat[c].md}/${byCat[c].total} md`);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
