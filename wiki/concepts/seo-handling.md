---
type: concept
nav_path: "Concept → SEO handling"
route_name: ""
route_path: ""
aliases: ["SEO", "Search engine optimization", "SEO handling", "Storefront SEO", "Sitemap and meta", "Crawler directives", "URL handles", "Search-engine indexing", "SEO model", "SEO стратегия", "SEO настройки", "SEO модел", "Индексиране", "Сайтмап и роботс"]
tags: [marketing, seo, sitemap, robots, canonical, meta-tags, indexing, concepts]
plan_gates: []
created: 2026-05-23
updated: 2026-06-25
source_count: 14
---

# SEO handling

## Definition

**SEO handling** is the cross-cutting set of behaviors CloudCart applies to make a storefront discoverable, indexable, and rankable by search engines (Google, Bing, Yandex) and crawlable by share-preview generators (Facebook, LinkedIn, X/Twitter). The system spans **ten distinct surfaces** the merchant configures across [[marketing-seo]] and its sub-screens — each surface controls one piece of the search-engine signal model, but the merchant outcome is the combined effect of all of them working together.

The pieces:

1. **Canonical tag** — `<link rel="canonical">` master URL signal ([[marketing-seo-canonical]]; mechanics in [[seo-canonical-noindex]]).
2. **Deindex of filtered/sorted pages** — `noindex` over a query-param threshold ([[marketing-seo-deindex]]; mechanics in [[seo-canonical-noindex]]).
3. **Pagination word in meta titles** — "Page" / "Страница" prefix ([[marketing-seo-meta-title]]; mechanics in [[seo-canonical-noindex]]).
4. **Sitemap.xml** — auto-generated catalog ([[marketing-seo-sitemap]]; mechanics in [[seo-sitemap-robots]]).
5. **Robots.txt** — URL-level crawl rules ([[marketing-seo-robots]]; mechanics in [[seo-sitemap-robots]]).
6. **Sharing module + Open Graph image** — `og:image` default ([[marketing-seo-sharing]]; mechanics in [[seo-sharing-rss]]).
7. **RSS feed** — newest-products feed for Pricerunner / Skroutz ([[marketing-seo-rss]]; mechanics in [[seo-sharing-rss]]).
8. **Per-section meta titles & descriptions** — `<title>` / `<meta name="description">` for Home / Contacts / Products / Vendors / Blog ([[marketing-seo-meta]]; mechanics in [[seo-meta-tags]]).
9. **Per-URL 301 redirects** — permanent URL redirects ([[marketing-seo-301-redirects]]; mechanics in [[seo-301-redirects]]).
10. **URL handles (slugs)** — per-entity slug editable on entity editor; auto-tracked handle history (30-day TTL) in [[seo-301-redirects]].

Each card on [[marketing-seo]] saves its setting in isolation; the storefront combines them at request time to produce the meta tags, sitemap, robots.txt, and canonical / noindex directives a crawler sees.

## Sub-pages (in this cluster)

This concept is split into 7 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[seo-sitemap-robots]] — `/sitemap.xml` (sitemap-index, 1-hour cache, 1,000 URLs per sub-sitemap, `.xml.gz` variant) + `/robots.txt` pipeline (merchant body + platform-appended `Disallow: /checkout|/cart|/wishlist|/bbt` block + `Crawl-Delay: 3`, 5-minute cache).
- [[seo-canonical-noindex]] — `<link rel="canonical">` self-canonical rule + special cases; `<meta name="robots" content="noindex">` on filtered/sorted pages over the `noindex_query_limit` threshold (0-5); pagination word ("Page", "Страница", etc.) prepended to paginated meta.
- [[seo-meta-tags]] — `<title>` / `<meta name="description">` four-step fallback chain (per-entity → per-section → language file → English); per-section meta on [[marketing-seo-meta]] (per-language + per-theme); legacy 16-section escape hatch (`marketing-seo-meta=old` cookie, verify).
- [[seo-301-redirects]] — per-URL 301 redirect manager (24-hour cache, wildcards via `*`, marketing-param preservation `fbclid|gclid|gclsrc|msclkid|utm_*|dclid|zanpid`, CSV import with 2FA gate); auto-tracked URL handle history (30-day TTL); prefix optimization for 7 named prefixes.
- [[seo-sharing-rss]] — dead AddThis module (only `og:image` matters); sharing card POSTs to legacy `/admin/marketing/seo/add-this` route; `/feed` RSS 2.0 (products-only, no cache, `rss_feed_count` 1-100 default 20).
- [[seo-plan-overrides]] — trial / `plan_expired` / development stores serve hard-coded `User-agent: *` + `Disallow: /`; `cc-demo` plan stores always emit `<meta name="robots" content="noindex, nofollow">`.
- [[seo-route-catalog]] — verbatim lists of indexable routes / noindex-eligible routes / always-noindex routes / robots-meta-exempt routes.

## Critical merchant-facing realities (verified)

- **Sitemap per-file cap is 1,000 URLs** (verify) — not 20,000 → [[seo-sitemap-robots]].
- **Robots.txt save bumps `Last-Modified` on every save**, even no-op → [[seo-sitemap-robots]].
- **Sharing card POSTs to LEGACY** `/admin/marketing/seo/add-this` (verify) → [[seo-sharing-rss]].
- **RSS item body** includes 300-char-truncated description + store contact / social block (verify) → [[seo-sharing-rss]].
- **Redirect prefix optimization** only for `product, category, vendor, blog, article, page, selection` → [[seo-301-redirects]].
- **Corrupted `noindex_query_limit` defaults to 1**, not 0 (verify) → [[seo-canonical-noindex]].

## Scope

Covered across the 7 sub-pages: the ten SEO surfaces and their request-time combination; trial / `plan_expired` / dev / `cc-demo` overrides; per-card vs global save model; the four-step meta fallback chain; auto-tracked URL slug history (30-day TTL); 301 CSV import; sitemap cache (1h) / robots.txt cache (5m) / RSS (no cache); the AddThis EOL (May 2023) consequence.

Not covered:

- Per-card admin UI (button copy, modal labels) — see the dedicated [[marketing-seo-canonical]] / [[marketing-seo-deindex]] / [[marketing-seo-robots]] etc. feature pages.
- Merchant's external work in Google Search Console, Bing Webmaster Tools, audit tools.
- Schema.org / structured-data / JSON-LD — theme template layer.
- AI meta / description generation — see [[apps-seo-spinner]].
- Cross-domain redirects between the merchant's **own** CloudCart stores — see [[apps-domain-redirect]] (geo-routing, 302, lands at target root; **not** an external-domain forwarder).
- Google Shopping / Skroutz / Pricerunner full product feeds — `/feed` RSS is a coarse fallback only.
- HTTP-level redirects (HTTPS upgrade, www↔non-www, trailing slash) — storefront infrastructure.
- **Path-preserving whole-domain forward to an arbitrary EXTERNAL domain** — there is no self-serve native feature for this. The per-URL `external` redirect is a fixed target per rule (no path preservation), and [[apps-domain-redirect]] is own-stores only — see the boundary on [[seo-301-redirects-types]]. A full external migration path-by-path needs per-path rules or an infrastructure / edge-level (the platform edge / CDN / DNS) redirect.

## Contrasts

- **Canonical vs. 301 vs. robots Disallow vs. noindex** — four signals merchants confuse. Canonical: URL accessible, credit elsewhere. 301: URL changes (HTTP 301 + Location). Robots Disallow: blocks fetching. Noindex meta: fetch allowed, index forbidden. Pick by intent: rename = 301; reduce duplicate weighting = canonical; block crawling = robots; hide from search but keep customer-accessible = noindex. See [[seo-canonical-noindex]] + [[seo-301-redirects]] + [[seo-sitemap-robots]].
- **Sitemap.xml vs. robots.txt vs. RSS** — sitemap = indexable-URL catalog; robots.txt = fetch allow/disallow; RSS = third-party product feed, NOT a search-engine submission.
- **Per-section vs. Per-entity meta** — per-section on [[marketing-seo-meta]] is the fallback; per-entity lives on each entity's editor and overrides. See [[seo-meta-tags]].
- **Pagination word vs. Meta title** — "Page" prefix vs. full `<title>`. See [[seo-canonical-noindex]] + [[seo-meta-tags]].
- **Trial `Disallow: /` vs. Demo `noindex, nofollow`** — both invisible to Google; different mechanism + upgrade path. See [[seo-plan-overrides]].
- **Auto-tracked handle history (30-day TTL) vs. Manual 301 (no TTL)** — see [[seo-301-redirects]].
- **Sharing module (dead) vs. `og:image` (alive)** — same card, very different outcomes. See [[seo-sharing-rss]].

## Where it applies

- **Admin** — [[marketing-seo]] (7-card hub) + [[marketing-seo-meta]] + [[marketing-seo-301-redirects]], plus per-entity meta on [[product]] / [[category]] / [[vendor]] / [[blog-article]].
- **Storefront output** — `<title>`, `<meta name="description">`, `<link rel="canonical">`, `<meta name="robots">`, `<meta property="og:*">`, `/sitemap.xml`, `/robots.txt`, `/feed`, and 301 redirect responses on old URLs.
- **Settings dependencies** — [[settings-domains]], [[settings-translations]], [[settings-general]] (`site_name` becomes RSS channel title).
- **Plan dependencies** — see [[seo-plan-overrides]]; general concept on [[plan-gates]].

## Related

- [[seo-sitemap-robots]] — sitemap and robots aspect.
- [[seo-canonical-noindex]] — canonical / noindex / pagination word aspect.
- [[seo-meta-tags]] — meta tag fallback chain aspect.
- [[seo-301-redirects]] — 301 redirects + URL handle history aspect.
- [[seo-sharing-rss]] — Open Graph + RSS feed aspect.
- [[seo-plan-overrides]] — trial / expired / demo override aspect.
- [[seo-route-catalog]] — storefront route catalog aspect.
- [[marketing-seo]] — Main SEO settings hub.
- [[marketing-seo-canonical]] / [[marketing-seo-deindex]] / [[marketing-seo-meta-title]] / [[marketing-seo-sitemap]] / [[marketing-seo-robots]] / [[marketing-seo-sharing]] / [[marketing-seo-rss]] — 7 cards on the Main SEO hub.
- [[marketing-seo-meta]] — Per-section meta titles and descriptions.
- [[marketing-seo-301-redirects]] — Per-URL 301 redirects manager.
- [[apps-domain-redirect]] / [[apps-domain-redirect-settings]] — cross-domain redirects.
- [[apps-seo-spinner]] / [[apps-seo-spinner-settings]] — AI content + meta generation.
- [[apps-google-search-console]] — sitemap submission to Google.
- [[product]] / [[category]] / [[vendor]] / [[blog-article]] — per-entity meta + OG image overrides.
- [[settings-domains]] — primary domain used in sitemap / RSS / canonical / redirect targets.
- [[settings-translations]] — storefront language affects section meta storage.
- [[settings-general]] — store name appears as RSS feed channel title.
- [[plan-gates]] — trial / expired / demo overrides that ALWAYS win over SEO settings.

## Open Questions

- Per-language pagination word — see [[seo-canonical-noindex]] Open Questions.
- All other previously-flagged questions resolved and distributed to sub-pages.
