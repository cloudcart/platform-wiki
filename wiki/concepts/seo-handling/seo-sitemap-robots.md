---
type: concept
nav_path: "Concept → SEO handling → Sitemap and robots"
aliases: ["Sitemap", "Sitemap.xml", "Robots.txt", "Crawl directives", "Sitemap-robots", "Sitemap cache", "Robots safety block"]
tags: [seo, sitemap, robots, crawler, indexing, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[seo-handling]]. See the hub for related aspects (canonical / noindex, meta tags, redirects, sharing / RSS, plan overrides, route catalog).

# SEO — sitemap.xml and robots.txt

## Definition

The storefront serves two crawler-facing endpoints derived from merchant settings + platform defaults:

- **`/sitemap.xml`** — auto-generated **sitemap-index** pointing to per-entity sub-sitemaps (vendors, categories, products, CMS pages, blogs, blog articles). Each sub-sitemap is cached for **1 hour** under a name+page key. Cache headers on the response are `Cache-Control: no-store, no-cache, must-revalidate` so browsers / proxies don't extend the platform's 1-hour cache.
- **`/robots.txt`** — merchant-saved text + a **platform-appended safety block** that always disallows checkout / cart / wishlist regardless of what the merchant saves. Cached **5 minutes**. Updating it bumps `Last-Modified` on **every save** — even a no-op save (Save clicked with unchanged content) updates the timestamp, prompting crawlers to re-parse.

## Scope

Covered:

- The sitemap-index → sub-sitemap structure, the **1,000 URLs per file** cap, the **1-hour cache**, the `.xml.gz` variant.
- Which entity types are included; the `visible` scope filter.
- The robots.txt request pipeline: merchant body + platform safety block + 5-minute cache.
- The platform default template (used when the merchant has never edited robots.txt).
- The "sitemap doesn't reference itself from robots.txt" gap.
- The "sitemap omits noindex'd URLs" rule.

Not covered here:

- The **trial / `plan_expired` / development** `Disallow: /` override → [[seo-plan-overrides]].
- The **`cc-demo` `noindex, nofollow`** override → [[seo-plan-overrides]].
- The robots admin UI (Save modal, editor field) → [[marketing-seo-robots]].
- The sitemap URL display card → [[marketing-seo-sitemap]].
- Which storefront routes get a `noindex` tag → [[seo-canonical-noindex]] + [[seo-route-catalog]].

## Contrasts

- **Sitemap.xml vs robots.txt vs RSS** — sitemap is the "here are my indexable URLs" catalog. Robots.txt is the "here's what you can / can't fetch" instruction. RSS is a product feed (Skroutz / Pricerunner / RSS-to-email), NOT a search-engine submission — see [[seo-sharing-rss]].
- **Merchant-saved robots vs platform safety block** — the merchant cannot make `/checkout`, `/cart`, `/wishlist` crawlable. Even an empty merchant body gets the safety block appended.
- **Per-file cap 1,000 vs the old 20,000** — verified: the active sitemap helper hardcodes **`maxURLsPerSitemap = 1000`** (verify). The 20,000 number applied to a legacy class no longer used for live requests. A store with 60k products produces **60 sub-sitemap pages** (`/sitemap/product/1.xml` through `/sitemap/product/60.xml`), all linked from `/sitemap.xml`.

## Where it applies

### Sitemap.xml — what's inside

`/sitemap.xml` is a sitemap-index. Each entry points to a per-entity sub-sitemap (`/sitemap/<type>/<page>.xml`). Currently indexed entity types:

- vendors
- categories
- products (`visible` scope only)
- CMS pages (`visible` scope only)
- blogs (with at least one active article)
- blog articles

Per-entity sub-sitemap pagination caps at **1,000 URLs per file** (verify). `.xml.gz` (gzip-compressed) is also accepted — Google Search Console fetches gzip by default for large sitemaps.

**Newly created products lag by up to 1 hour** in the sitemap because of the 1-hour cache TTL. There is no proactive cache flush on product create.

URLs the storefront marks as `noindex` (via [[seo-canonical-noindex]], or system pages like cart / checkout / account) are **NOT** included in the sitemap. The sitemap is meant to expose indexable URLs only.

### Robots.txt — the request pipeline

1. Fetch merchant's saved value (cached **5 minutes**). If empty, use the platform default template.
2. **Append** a mandatory block to the merchant's body, verbatim:
   ```
   Disallow: /checkout
   Disallow: /checkout/*
   Disallow: /cart
   Disallow: /cart/*
   Disallow: /wishlist/*
   Disallow: /bbt
   Disallow: /bbt/*
   Crawl-Delay: 3
   ```
3. Return as `text/plain` with `Last-Modified` from the merchant's last save timestamp.

Even if the merchant saves a completely empty robots.txt, checkout / cart / wishlist are still blocked. The merchant cannot make those URLs crawlable from the admin UI.

The platform default template (used when the merchant has never edited robots.txt or saves empty) **also blocks `/tags` and `/contacts/*`** — the merchant has to deliberately keep those allowed by saving custom content if they want them indexed.

### Sitemap reference from robots.txt — NOT auto-injected

The platform does **NOT** automatically inject a `Sitemap: https://<host>/sitemap.xml` line into the served robots.txt. If the merchant wants crawlers to discover the sitemap from robots.txt (a common best practice), they have to paste that line into the robots editor themselves.

### Robots.txt live cache

After saving robots.txt, the live `/robots.txt` updates within **5 minutes** (the cache TTL). Not instant. There is no proactive cache flush on save — the merchant just waits up to 5 minutes.

### Robots.txt save bumps `Last-Modified` on no-op saves

Even a save with unchanged content updates `Last-Modified`. Crawlers re-parse the file as a result.

## Related

- [[seo-handling]] — hub.
- [[seo-plan-overrides]] — trial / expired / dev `Disallow: /` overrides this whole pipeline.
- [[seo-canonical-noindex]] — `noindex` decisions feed back into which URLs the sitemap omits.
- [[seo-route-catalog]] — the storefront route lists that govern which pages emit indexable / noindex tags.
- [[marketing-seo-sitemap]] — admin card for the sitemap URL display.
- [[marketing-seo-robots]] — admin editor for the robots.txt body.
- [[settings-domains]] — primary domain determines the host used for sitemap / robots URLs.
- [[apps-google-search-console]] — submitting `/sitemap.xml` to Google.

## Open Questions

None.
