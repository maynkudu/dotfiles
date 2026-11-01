import { promises as fs } from "node:fs";
import path from "node:path";
import zlib from "node:zlib";
import { fileURLToPath } from "node:url";

export const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
export const CACHE = path.join(ROOT, ".cache");
export const HTML_CACHE = path.join(CACHE, "html");
export const ORIGIN = "https://developers.google.com";
export const UA =
  "Mozilla/5.0 (compatible; google-seo-skills-builder/1.0; +https://developers.google.com/search/docs)";

export function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

export async function ensureDir(dir) {
  await fs.mkdir(dir, { recursive: true });
}

async function writeAtomic(file, data) {
  await ensureDir(path.dirname(file));
  const tmp = `${file}.${process.pid}.tmp`;
  await fs.writeFile(tmp, data);
  await fs.rename(tmp, file);
}

export function normalizeUrl(u) {
  let s = String(u).trim();
  if (!s) return null;
  try {
    const url = new URL(s, ORIGIN);
    url.hash = "";
    url.search = "";
    let p = url.pathname.replace(/\.md\.txt$/, "");
    p = p.replace(/\/+$/, "");
    if (!p) p = "/";
    url.pathname = p;
    return `${url.origin}${url.pathname}`;
  } catch {
    return null;
  }
}

export function urlToPath(url) {
  const u = new URL(url);
  const p = u.pathname.replace(/^\/+/, "").replace(/\/+$/, "");
  return p || "index";
}

export function sectionOf(url) {
  const p = urlToPath(url);
  if (p.startsWith("crawling/")) return "crawling";
  if (p.startsWith("search/")) return "search";
  return "other";
}

const BINARY_EXT_RE = /\.(png|jpe?g|gif|svg|webp|avif|ico|bmp|pdf|xml|txt|json|zip|gz|csv|mp4|webm|css|js)$/i;

export function isDocPageUrl(url) {
  const p = urlToPath(url);
  if (!p.startsWith("search/docs") && !p.startsWith("crawling/docs")) return false;
  return !BINARY_EXT_RE.test(p);
}

export async function fetchText(url, { headers = {}, accept } = {}) {
  const opts = {
    redirect: "follow",
    headers: { "User-Agent": UA, ...headers },
  };
  if (accept) opts.headers["Accept"] = accept;
  try {
    const res = await fetch(url, opts);
    const body = await res.text();
    return {
      status: res.status,
      ok: res.ok,
      body,
      etag: res.headers.get("etag"),
      contentType: res.headers.get("content-type") || "",
      url: res.url,
    };
  } catch (err) {
    return { status: 0, ok: false, body: "", contentType: "", error: String(err) };
  }
}

function htmlCacheFile(url) {
  return path.join(HTML_CACHE, `${urlToPath(url).replace(/\//g, "__")}.html.gz`);
}

function withLang(url) {
  try {
    const u = new URL(url);
    if (!u.searchParams.has("hl")) u.searchParams.set("hl", "en");
    return u.toString();
  } catch {
    return url;
  }
}

export async function getHtml(url, { useCache = true, refresh = false } = {}) {
  const file = htmlCacheFile(url);
  const urlFile = `${file}.url`;
  if (useCache && !refresh) {
    try {
      const buf = await fs.readFile(file);
      const finalUrl = await fs.readFile(urlFile, "utf8").catch(() => url);
      return {
        status: 200,
        ok: true,
        body: zlib.gunzipSync(buf).toString("utf8"),
        url: finalUrl.trim(),
        cached: true,
      };
    } catch {
      /* miss */
    }
  }
  const res = await fetchText(withLang(url), { accept: "text/html,application/xhtml+xml" });
  if (res.ok && res.body) {
    await writeAtomic(file, zlib.gzipSync(Buffer.from(res.body, "utf8")));
    await writeAtomic(urlFile, res.url || withLang(url));
  }
  return { ...res, cached: false };
}

export async function readJson(file, fallback = null) {
  try {
    return JSON.parse(await fs.readFile(file, "utf8"));
  } catch {
    return fallback;
  }
}

export async function writeJson(file, obj) {
  await writeAtomic(file, JSON.stringify(obj, null, 2) + "\n");
}

export async function mapLimit(items, limit, fn) {
  const results = new Array(items.length);
  let i = 0;
  const workers = new Array(Math.min(limit, items.length)).fill(0).map(async () => {
    while (i < items.length) {
      const idx = i++;
      results[idx] = await fn(items[idx], idx);
    }
  });
  await Promise.all(workers);
  return results;
}

export function stripHtml(s) {
  return String(s)
    .replace(/<[^>]*>/g, "")
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/\s+/g, " ")
    .trim();
}

const IMG_TAG_RE = /<img\b[^>]*>/gi;
const ATTR_RE = (name) => new RegExp(`${name}\\s*=\\s*("([^"]*)"|'([^']*)'|([^\\s>]+))`, "i");

function attr(tag, name) {
  const m = ATTR_RE(name).exec(tag);
  if (!m) return "";
  return (m[2] ?? m[3] ?? m[4] ?? "").trim();
}

export function extractContentImages(html) {
  const out = [];
  const seen = new Set();
  IMG_TAG_RE.lastIndex = 0;
  let m;
  while ((m = IMG_TAG_RE.exec(html))) {
    const tag = m[0];
    const src = attr(tag, "src") || attr(tag, "data-src");
    if (!src) continue;
    if (!/\/static\/search\/docs\/images\//.test(src)) continue;
    let abs;
    try {
      abs = new URL(src, ORIGIN).toString();
    } catch {
      continue;
    }
    if (seen.has(abs)) continue;
    seen.add(abs);
    out.push({ src: abs, alt: stripHtml(attr(tag, "alt")) });
  }
  return out;
}

export function extractDocLinks(html) {
  const links = new Set();
  const re = /href\s*=\s*"(\/(?:search|crawling)\/docs\/?[^"#?]*)"/gi;
  let m;
  while ((m = re.exec(html))) {
    const n = normalizeUrl(m[1]);
    if (n) links.add(n);
  }
  return [...links];
}

const PLACEHOLDER_HOST_RE = /^https?:\/\/(www\.)?(example\.(com|org|net)|localhost|your-?domain\.[a-z]+)/i;

function isFetchableImageUrl(u) {
  if (!/^https?:\/\//i.test(u)) return false;
  if (PLACEHOLDER_HOST_RE.test(u)) return false;
  return true;
}

const MD_IMG_RE = /!\[([^\]]*)\]\(\s*<?([^)>\s]+)>?(?:\s+["'][^"']*["'])?\s*\)/g;
const HTML_IMG_RE = /<img\b[^>]*>/gi;

export function extractMarkdownImages(md) {
  const out = [];
  const seen = new Set();
  let m;
  MD_IMG_RE.lastIndex = 0;
  while ((m = MD_IMG_RE.exec(md))) {
    const src = m[2];
    if (!isFetchableImageUrl(src) || seen.has(src)) continue;
    seen.add(src);
    out.push({ src, alt: stripHtml(m[1]) });
  }
  HTML_IMG_RE.lastIndex = 0;
  while ((m = HTML_IMG_RE.exec(md))) {
    const src = attr(m[0], "src");
    if (!src || !isFetchableImageUrl(src) || seen.has(src)) continue;
    seen.add(src);
    out.push({ src, alt: stripHtml(attr(m[0], "alt")) });
  }
  return out;
}

export function localPathForImage(src, assetsRoot) {
  const u = new URL(src);
  const clean = decodeURIComponent(u.pathname).replace(/^\/+/, "");
  const segs = clean.split("/").map((s) => s.replace(/[^a-zA-Z0-9._-]/g, "_")).filter(Boolean);
  if (u.hostname === "developers.google.com") return path.join(assetsRoot, ...segs);
  return path.join(assetsRoot, "_external", u.hostname.replace(/[^a-zA-Z0-9.-]/gi, "_"), ...segs.slice(-1));
}

export { writeAtomic };

function decodeEntities(s) {
  return String(s)
    .replace(/&#(\d+);/g, (_, d) => String.fromCodePoint(Number(d)))
    .replace(/&#x([0-9a-f]+);/gi, (_, h) => String.fromCodePoint(parseInt(h, 16)))
    .replace(/&nbsp;/g, " ")
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#39;|&apos;/g, "'")
    .replace(/&hellip;/g, "...");
}

function stripTags(s) {
  return String(s).replace(/<[^>]+>/g, " ");
}

function inlineClean(s) {
  return decodeEntities(stripTags(s)).replace(/[ \t]*\n[ \t]*/g, " ").replace(/\s+/g, " ").trim();
}

/**
 * Best-effort HTML -> Markdown for documentation pages that have no `.md.txt`
 * rendering (e.g. parts of the Google Crawling guide). Not a general converter.
 */
export function htmlToMarkdown(html) {
  let s = String(html);
  const start = s.search(/<div[^>]*class="[^"]*devsite-article-body/);
  if (start !== -1) {
    const end = s.indexOf("</article>", start);
    s = s.slice(start, end === -1 ? undefined : end);
  }
  s = s
    .replace(/<script[\s\S]*?<\/script>/gi, "")
    .replace(/<style[\s\S]*?<\/style>/gi, "")
    .replace(/<nav[\s\S]*?<\/nav>/gi, "")
    .replace(/<form[\s\S]*?<\/form>/gi, "")
    .replace(/<devsite-[\s\S]*?<\/devsite-[a-z-]+>/gi, "")
    .replace(/<devsite-[^>]*>/gi, "");

  const codes = [];
  s = s.replace(/<pre[^>]*>([\s\S]*?)<\/pre>/gi, (_, code) => {
    codes.push(decodeEntities(stripTags(code)).replace(/\s+$/, ""));
    return `\n\u0000CODE${codes.length - 1}\u0000\n`;
  });

  s = s
    .replace(/<a[^>]*href="([^"]+)"[^>]*>([\s\S]*?)<\/a>/gi, (_, href, text) => {
      const label = inlineClean(text);
      if (!label) return "";
      let abs = href;
      try {
        abs = new URL(href, ORIGIN).toString();
      } catch {
        /* keep */
      }
      return `[${label}](${abs})`;
    })
    .replace(/<img[^>]*>/gi, (tag) => {
      const src = attr(tag, "src");
      if (!src) return "";
      let abs = src;
      try {
        abs = new URL(src, ORIGIN).toString();
      } catch {
        /* keep */
      }
      return `![${inlineClean(attr(tag, "alt"))}](${abs})`;
    });

  s = s
    .replace(/<h([1-6])[^>]*>([\s\S]*?)<\/h\1>/gi, (_, lvl, t) => `\n\n${"#".repeat(+lvl)} ${inlineClean(t)}\n\n`)
    .replace(/<li[^>]*>([\s\S]*?)<\/li>/gi, (_, t) => `- ${inlineClean(t)}\n`)
    .replace(/<\/?(ul|ol)[^>]*>/gi, "\n")
    .replace(/<\/(t[dh])>/gi, " | ")
    .replace(/<br\s*\/?>/gi, "\n")
    .replace(/<(strong|b)[^>]*>([\s\S]*?)<\/\1>/gi, "**$2**")
    .replace(/<(em|i)[^>]*>([\s\S]*?)<\/\1>/gi, "*$2*")
    .replace(/<\/(p|div|section|article|tr|table|blockquote|h[1-6])>/gi, "\n\n");

  s = decodeEntities(s.replace(/<[^>]+>/g, ""));
  s = s
    .replace(/\u00a0/g, " ")
    .replace(/^[ \t]+/gm, "")
    .replace(/[ \t]+\n/g, "\n")
    .replace(/\n{3,}/g, "\n\n")
    .replace(/\u0000CODE(\d+)\u0000/g, (_, i) => `\n\`\`\`\n${codes[+i]}\n\`\`\`\n`)
    .trim();
  return `${s}\n`;
}
