---
name: google-seo
description: Authoritative offline copy of Google Search Central documentation — Search Essentials, technical requirements, spam policies, SEO fundamentals, crawling & indexing, canonicalization, robots.txt, sitemaps, structured data & rich results, search appearance, and monitoring/debugging. Use when auditing or advising on SEO: technical SEO reviews, crawlability, indexability, canonicals, robots.txt, sitemaps, structured data validation, SERP/appearance issues, or diagnosing Search Console crawl and indexing problems. Ships 230+ pages of Google's own docs as local markdown to ground every finding.
---

# Google SEO (offline Google Search Central)

A text-only mirror of Google's official Search Central documentation: **247 pages** of markdown
in `docs/`, indexed by topic in `references/`. Use it to **audit a site, answer SEO questions,
and produce a cited report** — always grounded in Google's own wording, never third-party lore.

## When to use this skill
- "Audit my site / page for SEO", "technical SEO review", "why isn't my page indexed?"
- Crawl/index issues: robots.txt, noindex, canonicalization, redirects, sitemaps, crawl budget, JS rendering.
- Structured data / rich results eligibility and markup questions.
- SERP appearance: titles, snippets, images, video, page experience.
- Diagnosing Search Console crawl errors and traffic drops.

## How to use it (audit workflow)
1. **Classify** the request by topic.
2. **Open the matching reference** in `references/` (see map below) to find the relevant pages.
3. **Read the canonical doc** at the linked `docs/...` path — quote/paraphrase Google's actual guidance.
4. **Apply the checklist**: `references/00-audit-checklist.md` gives the audit items in order
   (eligibility → crawlability → indexability → content → structured data → appearance → monitoring).
5. **Report** each issue using the format below. Never invent rules — if it isn't in the docs, say so.

## Report format
```
## Finding: <short title>
- Severity: critical | high | medium | low
- Affected: <URL / route / template>
- Evidence: <what you checked and observed>
- Why it matters: <one line>
- Doc: "<Google page title>" — <https://developers.google.com/...> (local: docs/...)
- Recommendation: <concrete fix in Google's terms>
```
Group findings by severity (critical first). Lead with a 2–3 line summary.

## Topic map
| Topic | Reference |
| --- | --- |
| Eligibility: technical requirements, spam policies, best practices | `references/01-essentials.md` |
| How Search works, SEO starter guide, people-first & AI content | `references/02-fundamentals.md` |
| Crawling & indexing: canonicalization, robots meta, JS, redirects, removals, crawl budget | `references/03-crawling-indexing.md` |
| Sitemaps: build/submit + image/news/video extensions | `references/04-sitemaps.md` |
| Search appearance: titles, snippets, images, video, Discover, page experience | `references/05-appearance.md` |
| Structured data & rich results (45+ types) | `references/06-structured-data.md` |
| Google crawlers & robots.txt | `references/07-crawlers-robots.md` |
| Specialty sites (ecommerce, international, explicit) & monitoring/debugging | `references/08-specialty-monitoring.md` |
| Legacy URL aliases | `references/09-other.md` |
| Full audit checklist | `references/00-audit-checklist.md` |

## Citation policy
Always cite the Google source for a claim: page title + `https://developers.google.com/...` URL +
the local `docs/...` path. If a question falls outside these docs, say it's out of scope.

## Layout
```
SKILL.md         this file
references/      00-audit-checklist + 01..09 topic indexes into the docs
docs/            Google Search Central documentation (markdown, URL path preserved)
urls.json        page inventory
scripts/         refresh pipeline (Node 18+, no dependencies)
```

## Notes
- **Text-only:** images are referenced by Google's remote URLs (not bundled), keeping the skill ~6 MB.
- **Source:** Google's `.md.txt` renderings, discovered from `developers.google.com/sitemap.xml`.
  Docs coverage verified 0 missing. Content is © Google, mirrored for offline reference.
- **Scope:** documentation only (no blog/help/API pages).
- **Refresh:** `node scripts/discover-full.mjs && node scripts/fetch-docs.mjs && node scripts/build-references.mjs && node scripts/verify-coverage.mjs`
