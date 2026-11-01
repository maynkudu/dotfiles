import path from "node:path";
import {
  ROOT,
  ORIGIN,
  UA,
  normalizeUrl,
  urlToPath,
  sectionOf,
  isDocPageUrl,
  readJson,
  writeJson,
} from "./lib.mjs";

const INDEX = `${ORIGIN}/sitemap.xml`;
const URLS = path.join(ROOT, "urls.json");

async function get(url) {
  const res = await fetch(url, { headers: { "User-Agent": UA }, redirect: "follow" });
  if (!res.ok) throw new Error(`HTTP ${res.status} for ${url}`);
  return res.text();
}

function extractLocs(xml) {
  const out = [];
  const re = /<loc>([^<]+)<\/loc>/g;
  let m;
  while ((m = re.exec(xml))) out.push(m[1].trim());
  return out;
}

function isDocUrl(u) {
  try {
    const n = new URL(u);
    if (n.hostname !== "developers.google.com") return false;
    const p = n.pathname.replace(/\/+$/, "");
    return /^\/(search|crawling)\/docs/.test(p);
  } catch {
    return false;
  }
}

async function mapLimit(items, limit, fn) {
  const results = new Array(items.length);
  let i = 0;
  await Promise.all(
    new Array(Math.min(limit, items.length)).fill(0).map(async () => {
      while (i < items.length) {
        const idx = i++;
        results[idx] = await fn(items[idx], idx);
      }
    })
  );
  return results;
}

async function main() {
  console.log("fetching sitemap index...");
  const indexXml = await get(INDEX);
  const shards = extractLocs(indexXml).filter((u) => /sitemap_\d+_of_\d+\.xml$/.test(u));
  console.log(`sitemap shards: ${shards.length}`);

  const found = new Set();
  let done = 0;
  await mapLimit(shards, 6, async (shard) => {
    try {
      const xml = await get(shard);
      const locs = extractLocs(xml);
      let kept = 0;
      for (const loc of locs) {
        if (!isDocUrl(loc)) continue;
        const n = normalizeUrl(loc);
        if (n && isDocPageUrl(n)) {
          found.add(n);
          kept += 1;
        }
      }
      done += 1;
      console.log(`  [${done}/${shards.length}] ${path.basename(shard)}: +${kept} doc urls (total ${found.size})`);
    } catch (err) {
      done += 1;
      console.error(`  [${done}/${shards.length}] ${path.basename(shard)} FAILED: ${err}`);
    }
  });

  const existing = (await readJson(URLS, { urls: [] })) || { urls: [] };
  const byUrl = new Map((existing.urls || []).map((u) => [u.url, u]));
  let added = 0;
  for (const u of found) {
    if (!byUrl.has(u)) {
      byUrl.set(u, { url: u, path: urlToPath(u), section: sectionOf(u), crawled: false, source: "sitemap" });
      added += 1;
    } else {
      byUrl.get(u).source = byUrl.get(u).source || "sitemap";
    }
  }

  const urls = [...byUrl.values()].sort((a, b) => a.path.localeCompare(b.path));
  await writeJson(URLS, { generatedAt: new Date().toISOString(), count: urls.length, urls });

  const bySection = urls.reduce((a, u) => ((a[u.section] = (a[u.section] || 0) + 1), a), {});
  console.log(`sitemap: ${found.size} doc urls; +${added} new; urls.json now ${urls.length}`, bySection);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
