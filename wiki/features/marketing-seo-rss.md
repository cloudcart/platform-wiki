---
type: feature
nav_path: "Marketing → SEO → RSS Feed"
route_name: seo-main
route_path: /admin/marketing-new/seo
aliases: ["RSS file", "RSS feed", "Products RSS", "RSS syndication", "Feed URL", "Product feed", "RSS файл", "РСС файл", "РСС feed", "Канал за продукти", "Продуктов поток"]
tags: [marketing, seo, rss, distribution]
plan_gates: []
created: 2026-05-23
updated: 2026-06-10
source_count: 4
---
# RSS feed (newest-products syndication)

## Purpose

This is the **"RSS file"** card on the [[marketing-seo]] screen (7th and last card). It lets the merchant control two things about the storefront's auto-generated RSS feed:

1. How many products the feed contains (1-100, default 20).
2. The feed URL (read-only display, copy-to-clipboard).

The feed is a public XML endpoint at `<primary-store-host>/feed` that any third party — Google Shopping ingesters, Pricerunner, Skroutz, comparison engines, email "new products" blocks, the merchant's own blog — can subscribe to in order to receive a stream of the store's **newest products in reverse-chronological order**.

The feed is platform-generated. The merchant cannot edit the XML body, the item structure, or the channel metadata (title, description) directly — those are derived automatically (see Business rules).

## Where to find it

Sidebar → Marketing → **SEO** → scroll to the bottom, the **"RSS file"** card. Route is `/admin/marketing-new/seo`. The card has its own inline Save / Revert bar that appears only after the merchant changes the count.

## What the merchant can do here

- Read and change the product-count limit on the feed (any integer 1-100).
- Read the feed URL and copy it to clipboard with one click (toast: "Copied to clipboard").
- Hand the copied URL to a third party (Google Shopping form, Skroutz onboarding, email-marketing RSS-to-email block, etc.).

### What the merchant CANNOT do here

The count is the only editable value. Everything else is platform-fixed (detail in Business rules): the feed is **products only** (no articles, news, categories, vendors, CMS pages, orders); always ordered by product `id` descending; filtered only by the standard `visible` scope (no category / stock / discount filter); always **RSS 2.0** at `<primary-store-host>/feed` (no Atom / JSON Feed / Google Shopping schema, no alternate path); channel `<title>` = `site_name` and `<description>` = empty string; the item schema is hardcoded; there is no item-level customisation, no way to disable the feed (count 0 fails validation), and no caching control.

## Settings & fields

The card has exactly two controls.

| Field | What it does | Default | Validation / notes |
|-------|--------------|---------|--------------------|
| **Number of products to display in the RSS file** (integer-only number input) | Sets `setting('rss_feed_count')` — how many products the feed serves (the newest N by `id` descending). | `20` | `int, min:1, required, max:100`. Errors: "Minimum value is 1" (`rss_feed_count.min`), "Maximum value is 100" (`rss_feed_count.max`), "rss_feed_count is required" (`rss_feed_count.required`). Decimals rejected client-side (`:digits="0"`) and server-side (`int`). The storefront additionally clamps to `min(setting, 100)`, so a legacy DB value > 100 can never produce more than 100 items. |
| **Path for the RSS Feed** (read-only display + copy button) | Shows the absolute feed URL; clicking copies it to clipboard. | `<primary scheme>://<primary host>/feed` | Not editable anywhere in admin. Changes only when the merchant changes their primary domain on [[settings-domains]]. |

The card uses the shared **Save / Revert** wrapper — both buttons appear in an inline action bar only after the count changes. Save POSTs to the SEO settings sub-path `/rss-feed` with `{rss_feed_count: <number>}`. Save toast: "Saved Successfully".

## Business rules

### What's in the feed — products only, newest first

Each request to `/feed`:

1. Loads products in `visible` state (the same filter the storefront catalog uses to hide out-of-catalog, draft, and admin-only products). This is the **only** filter — no price / stock / vendor / category filter. Orphaned products with no category still appear (with empty `<category>`).
2. Orders by product `id` descending (newest first — there is no `created_at` column used).
3. Limits to `min(rss_feed_count, 100)`.
4. Builds one `<item>` per product. Products without a `name` are silently skipped.

**Item fields** per product:

- `<title>` = product name.
- `<image>` = the product's main image URL (600×600, same image shown in the catalog).
- `<description>` = a CDATA-wrapped HTML block — richer than just the description text. It contains, in order: the 600×600 image; the product description **HTML-stripped and truncated to 300 characters** (`...` appended if longer); the price when `showPriceForUser` allows (guest pricing rules); a line linking to the product mentioning its category and vendor ("[Product] is published in [Category] by [Brand] sold by [Store]"); the **store contact block** (`site_name`, `site_street`, `site_city`, `postal_code`, `country`, `site_phone` as a `<ul>`); and **all configured social-media links** (from each `<provider>_link` setting).
- `<link>` = the product's full storefront URL.
- `<guid isPermaLink="true">` = the same URL (RSS readers use it to de-duplicate).
- `<category>` = the product's category breadcrumb path joined with ` > ` (e.g. "Clothing > Men > T-Shirts"). Empty if the product has no category.

### Channel metadata — derived, not editable

- `<title>` = `setting('site_name')`, falling back to the language-pack default feed name (`sf.module.rss.default_feed_name`), then "CloudCart". Edited on [[settings-general]], not here.
- `<description>` = empty string (always — even though RSS 2.0 expects it; most readers tolerate this).
- `<link>` = the store's primary domain (from [[settings-domains]]).
- `<atom:link rel="self" type="application/rss+xml" href="…/feed">` points back to the feed URL.
- `<pubDate>` / `<lastBuildDate>` = the current request timestamp in RFC 822 format — they change on every request even if no products were added.

### No caching, no conditional GET

Unlike sitemap.xml (cached ~1 hour), the RSS feed has **no cache layer on the response**. Every external hit to `/feed` runs a fresh DB query, loads N products, and serializes the XML. The response carries only `Content-Type: application/xml; charset=utf-8` — **no `Last-Modified` / `ETag`**, so crawlers cannot do conditional GETs; every fetch is a full refresh. For high-volume Pricerunner / Skroutz crawlers with `rss_feed_count = 100` and expensive product accessors this can be heavy, but most merchants don't notice (crawl rate is minutes-apart, not seconds).

### Feed URL — derived from primary domain

Built from the store's primary host record. With multiple domains the URL uses the **primary** (default on [[settings-domains]]). If the primary domain changes, the URL changes and the merchant must re-paste it into every third party that subscribed. Path is always `/feed`, no extension.

### Use cases

The copied URL is typically handed to: **Google Shopping** (older Merchant Center setups accepting RSS 2.0 — a coarse fallback only, since full Google Shopping needs price/availability/condition/GTIN/brand fields not in this feed, so merchants usually use the dedicated Product Feed app instead); **Skroutz / Pricerunner** and other EU comparison engines that accept generic RSS as a discovery source; **RSS-to-email** automations (Mailchimp / Sendinblue / Brevo / GetResponse) that turn newest products into a newsletter block; the merchant's own blog / news site (WordPress / Joomla RSS plugin); and generic RSS readers (Feedly, Inoreader).

### Permission & plan gates

Behind `hasApiPermission:marketing.seo`. No plan gate — included with every plan.

## Related

- [[marketing-seo]] — Main SEO settings (parent screen).
- [[marketing-seo-meta]] — per-section meta titles & descriptions.
- [[marketing-seo-sharing]] — Social sharing module & default Open Graph image (sibling card).
- [[marketing-seo-canonical]] — canonical-tag setting (sibling card).
- [[marketing-seo-deindex]] — noindex on filtered/sorted pages (sibling card).
- [[marketing-seo-sitemap]] — sitemap.xml URL display (sibling card; the search-engine equivalent of this feed — full URL set rather than newest-N, and cached).
- [[marketing-seo-robots]] — robots.txt editor (sibling card).
- [[marketing-seo-meta-title]] — pagination word in meta titles (sibling card).
- [[settings-domains]] — primary domain (the feed URL is built from it).
- [[settings-general]] — store name used as the feed channel `<title>`.
- [[product]] — products appear in the feed automatically once visible.

## Open questions

No outstanding questions.
