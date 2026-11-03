---
type: concept
nav_path: "Concept → SEO handling → Canonical and noindex"
aliases: ["Canonical tag", "Self-canonical", "Noindex", "Noindex on filtered pages", "Deindex", "Pagination word", "Filter parameter count", "Canonical-noindex"]
tags: [seo, canonical, noindex, robots-meta, pagination, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-11-03
source_count: 3
---

> Part of [[seo-handling]]. See the hub for related aspects (sitemap / robots, meta tags, redirects, sharing / RSS, plan overrides, route catalog).

# SEO — canonical tag, noindex on filtered pages, pagination word

## Definition

Three meta-level signals that work together to tell search engines which URL of a category / list page is the "master" copy, which URL variants should be ignored, and which paginated pages are distinct vs. duplicate:

- **Canonical tag** — `<link rel="canonical" href="<URL>">` emitted in every indexable page's `<head>`. Default: **self-canonical per URL** (every page declares itself the master).
- **Noindex on filtered / sorted pages** — `<meta name="robots" content="noindex">` on category / list / search / vendor / tag pages when the number of "meaningful" query parameters exceeds the merchant's threshold (`noindex_query_limit`).
- **Pagination word** — the literal word ("Page", "Страница", "Página", "Seite") prepended to meta titles on paginated pages 2+ so they don't read as duplicate meta to Google.

## Scope

Covered:

- The self-canonical rule + special cases (pagination, filters, CMS / selection overrides, vendor-contact carve-out).
- The deindex parameter count + which params are excluded vs counted; threshold range **0-5**.
- The `noindex_query_limit` setting + the **corrupted-value default of 1** (not 0) — invalid values get clamped to 1 at storefront render time (verify).
- The pagination word + its single-global-string nature (no per-language).
- How canonical + noindex interact.

Not covered here:

- The admin UI of the Canonical / Deindex / Pagination cards on [[marketing-seo]] — see [[marketing-seo-canonical]] / [[marketing-seo-deindex]] / [[marketing-seo-meta-title]].
- Per-entity meta titles (the full `<title>` text) → [[seo-meta-tags]].
- Which routes are eligible to emit `noindex` → [[seo-route-catalog]].
- The trial / demo plan overrides that always force `noindex, nofollow` → [[seo-plan-overrides]].

## Contrasts

- **Canonical vs. 301 vs. robots Disallow vs. noindex** — four signals merchants confuse. **Canonical** keeps the URL accessible but tells Google "credit this other URL". **301** changes the URL the browser sees (HTTP status 301 + Location header) — old URL stops working. **Robots Disallow** blocks crawlers from fetching at all. **Noindex meta** lets crawlers fetch but tells them not to index. Pick by intent: rename → 301; reduce duplicate weighting → canonical; block crawling → robots; hide from search but keep customer-accessible → noindex.
- **Self-canonical vs cross-canonical** — CloudCart's default is self-canonical (every page is its own master). The CMS-page editor and the Selection editor let the merchant override that to point elsewhere (cross-canonical).
- **Pagination word ([[marketing-seo-meta-title]]) vs Meta title ([[marketing-seo-meta]])** — pagination word is the literal "Page" / "Страница" prepended to meta titles on paginated pages 2+. Meta title is the FULL `<title>` text for a section page. Different settings; the card on [[marketing-seo]] is mislabeled "Title", which confuses merchants. The pagination word lives on its own setting screen — see [[marketing-seo-meta-title]].
- **Canonical and noindex side-by-side** — they work together: canonical keeps similar-but-not-duplicate pages from competing; noindex hides truly redundant variants. A page that is `noindex, nofollow` gets no canonical; a filtered listing that is `noindex, follow` points its canonical at the kept parameters.

## Where it applies

### Canonical — self-canonical per URL, with overrides

When canonical is ON (the default), every storefront page emits `<link rel="canonical" href="<current URL>">`. Special cases:

- **Paginated lists**: ignored parameters are stripped and `?page=N` re-added. So `/category/shoes?utm_source=x&page=3` canonicalizes to `/category/shoes?page=3`. Each paginated page declares itself the canonical — pages 1, 2, 3, 4 are distinct URLs to Google, not duplicates.
- **Filtered listings** get a canonical with the first N counted parameters, and no `?page=N` when they are over the threshold. At threshold 0 that is the unfiltered listing.
- **CMS pages with custom canonical**: if the merchant set a canonical override on a specific CMS page, that override wins over the auto-generated value.
- **Selection (curated list) canonical override**: same — explicit override wins.
- **Vendor-contact carve-out**: contact pages reached via `/contacts/<vendor>` canonicalize back to the main `/contacts` route.
- **Noindexed pages get no canonical** — if a page is `noindex, nofollow` (checkout, cart, account, etc.), the storefront skips the canonical to avoid signaling the URL as a master copy.

### Noindex on filtered / sorted pages — paired with canonical

When [[marketing-seo-deindex]] is ON with threshold N, the storefront counts "meaningful" query parameters on the eligible routes (see [[seo-route-catalog]] for the full list — `category.view`, `selection`, `site.vendor.view`, `site.tag`, `products.search`, `bundles.list.list`, `bundles.list.category`):

- **Counted**: `order_by`, `order_direction`, `variants`, `price_range`, `price_from`, `price_to`, `vendors`, `brand`, `new`, `sale`, `query`, and on category pages the category property keys.
- **Not counted**: `page`, `per_page`, an empty `query`, and every other parameter, ad trackers (`gclid`, `fbclid`, `utm_*`) included. These are ignored for the canonical too.

If the count exceeds N, the page renders `<meta name="robots" content="noindex, follow">`. With the switch off, N is 0. Threshold range is **0-5** (5 = up to 5 stacked filters indexed, 6th is noindex).

**Corrupted-value default = 1.** A `noindex_query_limit` value outside the validated range (e.g. `99`) gets clamped to **1** at storefront render time, not to 5 or 0 (verify).

### Pagination word — solves the duplicate-meta problem

The self-canonical-per-page strategy creates a side effect: pages 2, 3, 4 all have the same `<title>` and `<meta name="description">` text. Google flags that as duplicate meta. The platform fixes this by prepending the **pagination word** + page number + dash to the meta on page 2+. With the default word "Page" and a category named "Shoes":

```
<title>Page 2 - Shoes</title>
<meta name="description" content="Page 2 - <existing description>">
```

The merchant sets the word per storefront language ("Page", "Страница", "Página", "Seite"). The page number and separator (" - ") are added automatically.

**One global string, not per-language.** The pagination word setting on [[marketing-seo-meta-title]] is one global value, not per-language. A storefront switching between languages should re-set the word to match the current display language. The field is `required` — leaving it empty fails validation, so there's no clean "off" switch.

### Always-noindex routes

Independent of the filter-parameter threshold, certain routes always emit `noindex` — `checkout`, `checkout.*`, `cart.*`, `compare`, `site.auth.*`, `site.account`, `site.account.*`. See [[seo-route-catalog]] for the full list. These routes never get a canonical either.

## Related

- [[seo-handling]] — hub.
- [[seo-route-catalog]] — the indexable / noindex / exempt route list.
- [[seo-plan-overrides]] — trial / demo overrides that force `noindex, nofollow` regardless.
- [[seo-meta-tags]] — the per-section / per-entity `<title>` + meta description these signals decorate.
- [[marketing-seo-canonical]] — admin card (1st card on [[marketing-seo]]).
- [[marketing-seo-deindex]] — admin card (2nd card).
- [[marketing-seo-meta-title]] — pagination word (3rd card).
- [[marketing-seo]] — Main SEO settings hub.

## Open Questions

- Per-language pagination word. Today it's a single global string; multi-language merchants pick one canonical pagination label that surfaces on all language storefronts. Per-locale override is not implemented.
