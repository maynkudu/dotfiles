# google-seo-skill

An **offline, text-only copy of Google Search Central's documentation**, packaged as an
[Agent Skill](https://docs.claude.com/en/docs/claude-code/skills) so any compatible agent
(Claude, opencode, etc.) can audit a site, answer SEO questions, and produce a **cited report**
grounded in Google's own guidance.

It contains **247 pages** of Google's official docs as local markdown, indexed by topic in
`references/`, plus an actionable `references/00-audit-checklist.md`.

## What's inside

```
SKILL.md         skill entrypoint: audit workflow + report format + topic map
references/      topic indexes (01–09) + 00-audit-checklist, each linking into docs/
docs/            Google Search Central markdown (URL path preserved, images by remote URL)
urls.json        page inventory
scripts/         refresh pipeline (Node 18+, no dependencies)
```

Coverage: **186/186** Search Central doc pages (verified 0 missing against Google's sitemap),
plus legacy-URL alias stubs.

## Install

Clone into your agent's skills directory:

```bash
# Claude / opencode (user-level skills)
git clone https://github.com/mainkunalhu/google-seo-skill.git ~/.agents/skills/google-seo
```

Or copy the folder anywhere your agent loads skills from. The skill name is `google-seo`.

## Use

Ask your agent things like:

- "Audit https://example.com for technical SEO and give me a prioritized report."
- "Why might these pages not be getting indexed?"
- "Is our Product structured data valid and eligible for rich results?"
- "Write correct robots.txt rules to block faceted URLs."

The agent reads `references/00-audit-checklist.md`, opens the relevant local docs, and reports
findings with severity, evidence, and a link to the Google source.

## Refresh the docs

```bash
node scripts/discover-full.mjs     # sitemap -> urls.json (docs scope)
node scripts/fetch-docs.mjs        # <url>.md.txt -> docs/
node scripts/build-references.mjs  # rebuild references/
node scripts/verify-coverage.mjs   # assert 0 missing pages and 0 broken links
```

## Sources & attribution

Content is mirrored from **Google Search Central** — `developers.google.com/search/docs` and
`developers.google.com/crawling/docs` — via Google's own `.md.txt` renderings, discovered from
`developers.google.com/sitemap.xml`. All documentation content is **© Google** and is included
here for offline reference only (see `NOTICE`). The scripts in `scripts/` are MIT licensed
(see `LICENSE`). This project is unofficial and not affiliated with Google.
