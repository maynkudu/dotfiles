# SEO Audit Checklist

Actionable checklist for auditing a site's SEO against Google's documented requirements.
Work top-down: **eligibility → crawlability → indexability → content → structured data → appearance → monitoring**.
Every item links to the authoritative page in `docs/` — read it before reporting a finding.

## 1. Eligibility & policies
- [ ] Site meets the [technical requirements](../docs/search/docs/essentials/technical.md) (not blocked, reachable, indexable).
- [ ] Content complies with the [spam policies](../docs/search/docs/essentials/spam-policies.md) (no cloaking, doorway pages, scraped/spun content, link spam, sneaky redirects).
- [ ] Follows [Search Essentials](../docs/search/docs/essentials.md) best practices.

## 2. Crawlability
- [ ] [robots.txt](../docs/crawling/docs/robots-txt/robots-txt-spec.md) doesn't unintentionally block Googlebot or key resources.
- [ ] Googlebot isn't blocked by [the site or server](../docs/crawling/docs/crawlers-fetchers/verify-google-requests.md); [crawl rate](../docs/crawling/docs/crawlers-fetchers/reduce-crawl-rate.md) is sane.
- [ ] Links are [crawlable `<a href>` links](../docs/search/docs/crawling-indexing/links-crawlable.md) (not JS-only onclick).
- [ ] A [sitemap](../docs/search/docs/crawling-indexing/sitemaps/build-sitemap.md) exists, is valid, and lists canonical URLs.
- [ ] [JavaScript content](../docs/search/docs/crawling-indexing/javascript/javascript-seo-basics.md) renders without errors and uses correct [rendering strategy](../docs/search/docs/crawling-indexing/javascript/dynamic-rendering.md).
- [ ] [Crawl budget](../docs/crawling/docs/crawl-budget.md) isn't wasted on low-value or faceted URLs.

## 3. Indexability
- [ ] Only [indexable file types](../docs/search/docs/crawling-indexing/indexable-file-types.md) are expected to rank.
- [ ] No accidental [`noindex` / robots meta / X-Robots-Tag](../docs/search/docs/crawling-indexing/robots-meta-tag.md) on pages that should rank.
- [ ] Canonicalization is correct: [canonical URLs](../docs/search/docs/crawling-indexing/canonicalization.md) self-consistent, no conflicting signals.
- [ ] [Duplicate URLs consolidated](../docs/search/docs/crawling-indexing/consolidate-duplicate-urls.md); parameters handled.
- [ ] [URL structure](../docs/search/docs/crawling-indexing/url-structure.md) is clean; redirects are [301](../docs/search/docs/crawling-indexing/301-redirects.md), not chains/loops.
- [ ] [Page metadata](../docs/search/docs/crawling-indexing/valid-page-metadata.md) is valid.
- [ ] [Removals](../docs/search/docs/crawling-indexing/remove-information.md) and [site moves](../docs/search/docs/crawling-indexing/site-move-with-url-changes.md) follow Google's process.

## 4. Content quality
- [ ] Content is [helpful and people-first](../docs/search/docs/fundamentals/creating-helpful-content.md) (demonstrates first-hand expertise, clear sourcing).
- [ ] Follows the [SEO starter guide](../docs/search/docs/fundamentals/seo-starter-guide.md) basics (titles, headings, descriptive text).
- [ ] Any [generative-AI content](../docs/search/docs/fundamentals/using-gen-ai-content.md) is used appropriately and adds value.
- [ ] Considerations for [AI features / AI Mode](../docs/search/docs/fundamentals/ai-optimization-guide.md) are understood.

## 5. Structured data & rich results
- [ ] Markup follows the [structured data policies](../docs/search/docs/appearance/structured-data/sd-policies.md).
- [ ] Relevant types implemented per the [intro guide](../docs/search/docs/appearance/structured-data/intro-structured-data.md) (e.g. [Article](../docs/search/docs/appearance/structured-data/article.md), [Product](../docs/search/docs/appearance/structured-data/product.md), [FAQ](../docs/search/docs/appearance/structured-data/faqpage.md), [Breadcrumb](../docs/search/docs/appearance/structured-data/breadcrumb.md)).
- [ ] Markup is valid and matches visible content; verified with the Rich Results Test.

## 6. Search appearance
- [ ] [Title links](../docs/search/docs/appearance/title-link.md) are descriptive and unique.
- [ ] [Snippets / meta descriptions](../docs/search/docs/appearance/snippet.md) are compelling.
- [ ] [Image SEO](../docs/search/docs/appearance/google-images.md) best practices (alt text, discoverability).
- [ ] [Video](../docs/search/docs/appearance/video.md) and [favicon](../docs/search/docs/appearance/favicon-in-search.md) requirements met.
- [ ] [Page experience](../docs/search/docs/appearance/page-experience.md) and [Core Web Vitals](../docs/search/docs/appearance/core-web-vitals.md) are healthy.
- [ ] No [intrusive interstitials](../docs/search/docs/appearance/avoid-intrusive-interstitials.md).

## 7. Monitoring & debugging
- [ ] Site is verified in [Search Console](../docs/search/docs/monitor-debug/search-console-start.md).
- [ ] [Crawl errors](../docs/search/docs/crawling-indexing/troubleshoot-crawling-errors.md) reviewed and fixed.
- [ ] [Search traffic drops](../docs/search/docs/monitor-debug/debugging-search-traffic-drops.md) are diagnosed systematically.
- [ ] [Security issues](../docs/search/docs/monitor-debug/security/malware.md) monitored.

## Reporting a finding
For every issue, report:
1. **Finding** — what is wrong, on which URL.
2. **Severity** — critical / high / medium / low (blocking indexation > ranking > polish).
3. **Evidence** — the checked item and the observed value.
4. **Doc** — citation: the Google page title + URL + local `docs/...` path.
5. **Recommendation** — the concrete fix, in Google's own terms.
