---
type: feature
nav_path: "Marketing → SEO → Robots.txt → Served file"
route_name: seo-main
route_path: /admin/marketing-new/seo
aliases: ["robots.txt served file", "Assembled robots.txt", "Robots.txt appended block", "Robots.txt platform default", "Robots.txt cache", "Robots.txt Last-Modified", "What crawlers actually see"]
tags: [marketing, seo, robots, storefront, cache]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[marketing-seo-robots]]. See the hub for the other aspects (the editor card, the trial-store block).

# Robots.txt — the served file

## Purpose

What a crawler downloads from `/robots.txt` is **not** the raw text in the [[seo-robots-editor|editor textarea]]. The storefront assembles the live file on every request: it takes the merchant's saved body (or a platform default if the body is empty), appends a fixed safety block, caches the result for 5 minutes, and serves it as `text/plain` with a `Last-Modified` header. This page documents that assembly pipeline — the part the merchant never sees directly. (The separate `Disallow: /` override for non-production stores is on [[seo-robots-trial-block]].)

Understanding the assembly matters because it explains two things merchants ask about: why checkout / cart are always blocked even on an "empty" robots.txt, and why a save takes up to 5 minutes to show up.

## Where to find it

This is storefront behaviour, not an admin screen. The output is visible at `https://<your-domain>/robots.txt` for any store. The body the merchant edits lives on [[seo-robots-editor]]; the host that serves it is the store's primary domain — see [[settings-domains]].

## What the merchant can do here

- View the live assembled file by visiting `/robots.txt` on the storefront.
- Add a `Sitemap:` line to the editor body to point crawlers at [[marketing-seo-sitemap]] (it is not auto-injected).
- Reset to the platform default by saving an empty body on [[seo-robots-editor]] (the storefront then serves the default template).

### What the merchant CANNOT do here

- Remove or edit the appended safety block (checkout / cart / wishlist Disallow + `Crawl-Delay: 3`).
- Force an instant refresh — the 5-minute cache TTL is the floor; there is no manual flush.
- See the assembled output inside the admin (no preview — the editor shows only the merchant portion).

## Settings & fields

This aspect has no editable fields of its own. The inputs are the merchant's saved `robots.txt` body (edited on [[seo-robots-editor]]) and the `update_robots` timestamp (which drives `Last-Modified`). Everything else is platform-fixed and described in Business rules.

## Business rules

### What the storefront ACTUALLY serves at `/robots.txt`

The pipeline on every `/robots.txt` request is:

1. Fetch the merchant's saved value (cached 5 minutes). If empty, fetch the platform default template.
2. Append these mandatory lines:
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
3. Return as `text/plain` with a `Last-Modified` header derived from the `update_robots` timestamp.

So even if the merchant writes a totally empty robots.txt, checkout / cart / wishlist / bbt are still blocked from crawling. The merchant cannot accidentally make those URLs crawlable from the editor card.

### Platform default (when the merchant has not edited)

If the merchant has never edited robots.txt (or saves an empty textarea on [[seo-robots-editor]]), the storefront falls back to the platform default template. The default body is:

```
User-agent: *
Disallow: /tags
Disallow: /tags/*
Disallow: /contacts/*
Disallow: /checkout
Disallow: /checkout/*
Disallow: /cart
Disallow: /cart/*
Disallow: /wishlist/*
Disallow: /bbt
Disallow: /bbt/*
Crawl-Delay: 3
```

This default blocks the tag listings, vendor sub-contact pages (`/contacts/<vendor>`), and the standard checkout / cart / wishlist URLs. The default already contains the checkout-cart-wishlist lines that the platform also appends — so the live served file may have those lines duplicated when the merchant saves an empty body. Duplicate `Disallow` lines are harmless from a crawler's perspective.

The default template file is read fresh on every cache miss, so if the platform updates the default via a deploy, stores that have NOT customized pick it up within 5 minutes.

### 5-minute cache

The storefront caches the assembled robots.txt body under the fixed key `robots-txt` for **5 minutes**. After the merchant saves, the live file updates within 5 minutes — not instantly. The cache key is fixed per store (no per-language / per-host variants), and there is **no proactive flush on save** — the merchant just waits up to 5 minutes for the TTL to expire. (The `Last-Modified` header updates immediately because it is set inside the response, not read from the cache.)

### `Last-Modified` header — based on `update_robots`

The HTTP response includes a `Last-Modified` header derived from the `update_robots` setting timestamp (or the max of `last_build` and `stylesheet_version` for the default-template fallback). This timestamp updates on every save — including a save with no actual content change (see [[seo-robots-editor]]). Crawlers use `Last-Modified` to skip re-parsing if nothing has changed since their last fetch.

### Sitemap reference — not auto-injected

The platform does NOT automatically add a `Sitemap:` line pointing at [[marketing-seo-sitemap]] (`https://<host>/sitemap.xml`) to the served robots.txt. If the merchant wants crawlers to discover the sitemap from robots.txt, they have to paste a line like `Sitemap: https://<their-domain>/sitemap.xml` into the editor textarea themselves. Most search engines can discover the sitemap independently when it's submitted via their webmaster tools, so this isn't strictly required — but it's a common SEO best practice.

### Mixed line endings in the appended block

The fixed appended block uses `\r\n` (Windows) line separators regardless of what line endings the merchant used in their saved body. A merchant on Mac/Linux saving `\n`-separated content gets mixed line endings in the final file. Crawlers tolerate this, but the source can look messy when viewed.

### No file size limit enforced

The storefront doesn't truncate — see [[seo-robots-editor]] for the matching note that the editor enforces no length cap either.

## Related

- [[marketing-seo-robots]] — hub.
- [[seo-robots-editor]] — the admin card that supplies the merchant body and the `update_robots` timestamp.
- [[seo-robots-trial-block]] — the separate `Disallow: /` template served instead of this pipeline for non-production stores.
- [[marketing-seo-sitemap]] — the sitemap URL a merchant can reference from the served body.
- [[settings-domains]] — the host crawlers fetch `/robots.txt` from; every domain serves the same body.

## Open questions

None.
