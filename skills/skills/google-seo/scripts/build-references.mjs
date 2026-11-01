import path from "node:path";
import { promises as fs } from "node:fs";
import { ROOT, readJson, writeAtomic, ensureDir, stripHtml } from "./lib.mjs";

const URLS = path.join(ROOT, "urls.json");
const REFS = path.join(ROOT, "references");

const GROUPS = [
  {
    file: "01-essentials.md",
    title: "Search Essentials",
    intro:
      "The non-negotiables for appearing in Google Search: technical requirements, spam policies, and the key best practices. Start here when auditing whether a page or site is eligible at all.",
    match: (p) => p === "search/docs/essentials" || p.startsWith("search/docs/essentials/"),
  },
  {
    file: "02-fundamentals.md",
    title: "SEO Fundamentals",
    intro:
      "How Search works, the SEO starter guide, people-first content, AI/Generative-AI guidance, and the practical first steps for site owners and developers.",
    match: (p) => p === "search/docs" || p.startsWith("search/docs/fundamentals/"),
  },
  {
    file: "03-crawling-indexing.md",
    title: "Crawling & Indexing",
    intro:
      "How Googlebot discovers URLs, canonicalization, robots meta and X-Robots-Tag, mobile-first indexing, JavaScript rendering, redirects, removals, and crawl troubleshooting.",
    match: (p) =>
      p === "search/docs/crawling-indexing" ||
      (p.startsWith("search/docs/crawling-indexing/") && !p.includes("/sitemaps")),
  },
  {
    file: "04-sitemaps.md",
    title: "Sitemaps",
    intro:
      "Building, formatting, and submitting sitemaps, plus specialized extensions for images, news, and video.",
    match: (p) => p.includes("/sitemaps"),
  },
  {
    file: "05-appearance.md",
    title: "Search Appearance",
    intro:
      "How to earn and control rich results and SERP features: titles, snippets, images, video, Discover, page experience, and visual elements.",
    match: (p) =>
      p === "search/docs/appearance" ||
      (p.startsWith("search/docs/appearance/") && !p.includes("/structured-data")),
  },
  {
    file: "06-structured-data.md",
    title: "Structured Data & Rich Results",
    intro:
      "Per-feature structured-data markup guides (Article, FAQ, HowTo, Product, Breadcrumb, Event, and 40+ more), validation, and eligibility.",
    match: (p) => p.includes("/structured-data") || p.includes("intro-structured-data"),
  },
  {
    file: "07-crawlers-robots.md",
    title: "Google Crawlers & robots.txt",
    intro:
      "Google's crawlers, fetchers and user-triggered agents, verifying Googlebot, reducing crawl rate, and writing robots.txt rules.",
    match: (p) => p.startsWith("crawling/"),
  },
  {
    file: "08-specialty-monitoring.md",
    title: "Specialty Sites & Monitoring",
    intro:
      "Ecommerce, international and explicit-content guidance, plus Search Console, Analytics, security and traffic-drop debugging.",
    match: (p) =>
      p.startsWith("search/docs/specialty/") ||
      p.startsWith("search/docs/monitor-debug/") ||
      p.startsWith("search/docs/advanced/"),
  },
];

async function docTitle(rel) {
  try {
    const txt = await fs.readFile(path.join(ROOT, rel), "utf8");
    const m = txt.match(/^#\s+(.+)$/m);
    return m ? m[1].trim() : null;
  } catch {
    return null;
  }
}

function cleanTitle(t, fallback) {
  if (t && /^\(Moved\)/i.test(t)) return fallback.replace(/-/g, " ");
  if (!t) return fallback;
  return stripHtml(t.replace(/\s*\|\s*Google Search Central\s*$/i, "")).trim();
}

function link(fromFile, absPath) {
  return path.relative(REFS, path.join(ROOT, absPath)).split(path.sep).join("/");
}

async function main() {
  const { urls = [] } = (await readJson(URLS, { urls: [] })) || {};
  await ensureDir(REFS);

  const entries = [];
  for (const u of urls) {
    const docRel = path.join("docs", `${u.path}.md`);
    try {
      await fs.access(path.join(ROOT, docRel));
    } catch {
      continue;
    }
    entries.push({ path: u.path, docRel, url: u.url, title: cleanTitle(await docTitle(docRel), u.path.split("/").pop()) });
  }

  const used = new Set();
  for (const g of GROUPS) {
    const items = entries.filter((e) => g.match(e.path)).sort((a, b) => a.title.localeCompare(b.title));
    items.forEach((i) => used.add(i.path));
    const lines = [
      `# ${g.title}`,
      "",
      g.intro,
      "",
      `${items.length} pages · local markdown under \`docs/\`.`,
      "",
    ];
    for (const it of items) {
      lines.push(`## [${it.title}](<${link(g.file, it.docRel)}>)`);
      lines.push("");
      lines.push(`- Source: ${it.url}`);
      lines.push(`- Local: \`${it.docRel}\``);
      lines.push("");
    }
    await writeAtomic(path.join(REFS, g.file), lines.join("\n").replace(/\n+$/, "\n"));
  }

  const leftover = entries.filter((e) => !used.has(e.path));
  if (leftover.length) {
    const lines = [
      "# Legacy URL Aliases",
      "",
      "Old documentation URLs that now 301-redirect. Each stub file points to and includes the canonical content mirrored elsewhere in this skill.",
      "",
      `${leftover.length} pages.`,
      "",
    ];
    for (const it of leftover.sort((a, b) => a.title.localeCompare(b.title))) {
      lines.push(`## [${it.title}](<${link("09-other.md", it.docRel)}>)`, "", `- Source: ${it.url}`, `- Local: \`${it.docRel}\``, "");
    }
    await writeAtomic(path.join(REFS, "09-other.md"), lines.join("\n").replace(/\n+$/, "\n"));
    console.log(`note: ${leftover.length} legacy aliases in 09-other.md`);
  }

  console.log(`references: ${GROUPS.length} topic files, ${used.size}/${entries.length} docs indexed`);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
