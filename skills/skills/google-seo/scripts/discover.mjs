import path from "node:path";
import { promises as fs } from "node:fs";
import {
  ROOT,
  getHtml,
  extractDocLinks,
  normalizeUrl,
  urlToPath,
  sectionOf,
  isDocPageUrl,
  writeJson,
  readJson,
  mapLimit,
  sleep,
  CACHE,
} from "./lib.mjs";

const SEEDS_FILE = path.join(ROOT, "scripts", "seeds.txt");
const OUT = path.join(ROOT, "urls.json");
const HTML_DIR = path.join(CACHE, "html");

async function readSeeds() {
  const raw = await fs.readFile(SEEDS_FILE, "utf8");
  return raw
    .split("\n")
    .map((l) => l.trim())
    .filter((l) => l && !l.startsWith("#"))
    .map(normalizeUrl)
    .filter(Boolean);
}

async function main() {
  const refresh = process.argv.includes("--refresh");
  const existing = await readJson(OUT, { urls: [] });
  const known = new Map((existing.urls || []).map((u) => [u.url, u]));

  const seeds = await readSeeds();
  const found = new Set([...seeds, ...(existing.urls || []).map((u) => u.url)].filter(isDocPageUrl));

  // Pages we still need to fetch to discover their sidebar links.
  let queue = [...found].filter((u) => {
    const meta = known.get(u);
    return refresh || !meta || !meta.crawled;
  });

  const crawled = new Set((existing.urls || []).filter((u) => u.crawled).map((u) => u.url));

  // Prefer fetching section roots first for faster convergence.
  queue.sort((a, b) => a.split("/").length - b.split("/").length);

  console.log(`seeds: ${seeds.length} | queued to crawl: ${queue.length}`);

  let round = 0;
  while (queue.length) {
    round += 1;
    const batch = queue.splice(0, 25);
    const results = await mapLimit(batch, 5, async (url) => {
      const res = await getHtml(url, { refresh });
      if (!res.ok) return { url, links: [], status: res.status };
      return { url, links: extractDocLinks(res.body), status: res.status };
    });

    let added = 0;
    for (const r of results) {
      crawled.add(r.url);
      for (const l of r.links) {
        if (!isDocPageUrl(l)) continue;
        if (!found.has(l)) {
          found.add(l);
          added += 1;
          queue.push(l);
          known.set(l, { url: l, path: urlToPath(l), section: sectionOf(l), crawled: false });
        }
      }
    }
    console.log(
      `round ${round}: crawled ${batch.length}, +${added} new urls, ${queue.length} queued, ${found.size} total`
    );
    if (!added && queue.length === 0) break;
    await sleep(150);
  }

  const urls = [...found]
    .map((u) => ({
      url: u,
      path: urlToPath(u),
      section: sectionOf(u),
      crawled: crawled.has(u),
    }))
    .sort((a, b) => a.path.localeCompare(b.path));

  await writeJson(OUT, {
    generatedAt: new Date().toISOString(),
    count: urls.length,
    urls,
  });

  const bySection = urls.reduce((acc, u) => ((acc[u.section] = (acc[u.section] || 0) + 1), acc), {});
  console.log(`wrote urls.json: ${urls.length} urls`, bySection);
  console.log(`html cached in ${HTML_DIR}`);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
