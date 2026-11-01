import path from "node:path";
import { promises as fs } from "node:fs";
import {
  ROOT,
  getHtml,
  extractContentImages,
  extractMarkdownImages,
  localPathForImage,
  readJson,
  writeJson,
  mapLimit,
  ensureDir,
  writeAtomic,
  UA,
} from "./lib.mjs";

const URLS = path.join(ROOT, "urls.json");
const DOCS = path.join(ROOT, "docs");
const ASSETS = path.join(ROOT, "assets", "images");
const MANIFEST = path.join(ROOT, "assets", "manifest.json");

async function readDocImages(pagePath) {
  try {
    const md = await fs.readFile(path.join(DOCS, `${pagePath}.md`), "utf8");
    return { found: true, images: extractMarkdownImages(md) };
  } catch {
    return { found: false, images: [] };
  }
}

async function downloadImage(src, dest) {
  const existing = await fs.stat(dest).catch(() => null);
  if (existing && existing.size > 0) return { bytes: existing.size, reused: true };
  const res = await fetch(src, { headers: { "User-Agent": UA } });
  if (!res.ok) return { error: `HTTP ${res.status}` };
  const buf = Buffer.from(await res.arrayBuffer());
  if (!buf.length) return { error: "empty body" };
  await writeAtomic(dest, buf);
  return { bytes: buf.length };
}

async function main() {
  if (process.argv.includes("--text-only")) {
    console.log("text-only mode: skipping image downloads (docs keep Google's remote image URLs).");
    return;
  }
  const { urls = [] } = (await readJson(URLS, { urls: [] })) || {};
  if (!urls.length) {
    console.error("urls.json is empty or missing. Run discover.mjs first.");
    process.exit(1);
  }
  const refresh = process.argv.includes("--refresh");
  const prev = (await readJson(MANIFEST, null)) || {};
  const prevPages = prev.pages || {};
  console.log(`collecting images for ${urls.length} page(s)...`);

  // Union of images referenced in the markdown and embedded in the HTML.
  // Seed from the previous manifest so images don't drop out once docs have
  // been rewired to local paths.
  const pageImages = new Map(); // path -> Map(src -> {src, alt})
  await mapLimit(urls, 8, async (u) => {
    const bySrc = new Map();
    for (const im of prevPages[u.path]?.images || []) {
      if (im.src) bySrc.set(im.src, { src: im.src, alt: im.alt || "" });
    }
    const md = await readDocImages(u.path);
    for (const im of md.images) {
      if (!bySrc.has(im.src)) bySrc.set(im.src, im);
      else if (!bySrc.get(im.src).alt && im.alt) bySrc.get(im.src).alt = im.alt;
    }
    // HTML is the fallback source: always for the docs (image-rich), otherwise
    // only when the markdown yielded no images (saves ~1.7k blog page fetches).
    const isDocs = u.category === "docs" || u.section === "crawling";
    if (isDocs || !md.found || md.images.length === 0) {
      const html = await getHtml(u.url, { refresh });
      if (html.ok) {
        for (const im of extractContentImages(html.body)) {
          if (!bySrc.has(im.src)) bySrc.set(im.src, im);
          else if (!bySrc.get(im.src).alt && im.alt) bySrc.get(im.src).alt = im.alt;
        }
      }
    }
    pageImages.set(u.path, bySrc);
  });

  // Unique images across all pages.
  const unique = new Map(); // src -> {alt}
  for (const bySrc of pageImages.values()) {
    for (const [src, im] of bySrc) {
      if (!unique.has(src)) unique.set(src, { alt: im.alt || "" });
      else if (!unique.get(src).alt && im.alt) unique.get(src).alt = im.alt;
    }
  }
  console.log(`unique images: ${unique.size}; downloading...`);

  const list = [...unique.entries()].map(([src, v]) => ({ src, alt: v.alt }));
  const imgMeta = new Map(); // src -> {local, bytes, error}
  let downloaded = 0;
  let reused = 0;
  let failed = 0;

  await mapLimit(list, 8, async (im) => {
    const dest = localPathForImage(im.src, ASSETS);
    await ensureDir(path.dirname(dest));
    const r = await downloadImage(im.src, dest);
    const local = path.relative(ROOT, dest).split(path.sep).join("/");
    if (r.error) {
      failed += 1;
      imgMeta.set(im.src, { local, error: r.error });
    } else {
      if (r.reused) reused += 1;
      else downloaded += 1;
      imgMeta.set(im.src, { local, bytes: r.bytes });
    }
  });

  const manifest = { generatedAt: new Date().toISOString(), pages: {}, images: [] };
  for (const [src, m] of imgMeta) {
    manifest.images.push({
      src,
      alt: unique.get(src).alt,
      local: m.local,
      ...(m.error ? { error: m.error } : { bytes: m.bytes }),
    });
  }

  let pagesWithImages = 0;
  let refs = 0;
  for (const [pagePath, bySrc] of pageImages) {
    const images = [...bySrc.keys()].map((src) => {
      const m = imgMeta.get(src) || {};
      return { src, alt: bySrc.get(src).alt || unique.get(src)?.alt || "", local: m.local, ...(m.error ? { error: m.error } : {}) };
    });
    manifest.pages[pagePath] = { images };
    if (images.length) {
      pagesWithImages += 1;
      refs += images.length;
    }
  }

  manifest.totals = {
    pages: urls.length,
    pagesWithImages,
    uniqueImages: unique.size,
    references: refs,
    downloaded,
    reused,
    failed,
  };
  await writeJson(MANIFEST, manifest);

  console.log(
    `done: ${unique.size} unique images (${downloaded} downloaded, ${reused} reused, ${failed} failed) ` +
      `referenced ${refs} times across ${pagesWithImages} pages -> assets/`
  );
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
