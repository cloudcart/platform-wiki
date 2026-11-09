---
type: concept
nav_path: "Concept → SEO handling → 301 redirects and URL handle history"
aliases: ["301 redirect", "Per-URL redirect", "URL handle history", "Slug history", "Auto-tracked redirect", "Redirect CSV import", "Wildcard redirect", "Redirect cache"]
tags: [seo, redirects, 301, url-handle, slug, csv-import, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-11-09
source_count: 4
---

> Part of [[seo-handling]]. See the hub for related aspects (sitemap / robots, canonical / noindex, meta tags, sharing / RSS, plan overrides, route catalog).

# SEO — 301 redirects and URL handle history

## Definition

Two mechanisms keep old URLs reachable after a rename or migration:

- **Per-URL 301 redirects** — merchant-curated manager on [[marketing-seo-301-redirects]]. Every redirect is **301 (permanent)** — no 302 (temporary) option. Cached **24 hours** per requested URI. No TTL on the rows themselves.
- **Auto-tracked URL handle history** — when an entity's `url_handle` (slug) changes, the platform records the OLD handle with a **30-day TTL**. The storefront serves an internal **301** to the entity's current URL whenever the old slug is requested, for 30 days. After 30 days the old URL 404s unless the merchant created a manual row.

## Scope

Covered:

- Redirect row types (Manual / External / Product / Category / Vendor / Page / Blog / Article / Section).
- Cache: per-requested-URI, **24 hours**, flushed on save / edit / delete.
- Wildcards: literal `*` in `old_url` → `%` in the SQL LIKE lookup, so `/old-shop/*` matches any sub-path.
- Marketing-parameter preservation on redirect (exact list below).
- Cascade on entity delete (entity-based rows auto-removed; manual / external / section rows are not).
- CSV import wizard: 3-step modal (upload → map columns → confirm), background job, idempotent re-import.
- Auto-tracked URL handle history: 30-day TTL, internal 301, fallback when the handle changes.
- Redirect lookup prefix optimization for **7 named prefixes** only: `product`, `category`, `vendor`, `blog`, `article`, `page`, `selection` — any other first path segment triggers a slower full-LIKE scan.
- Permission gate: `marketing.seo`; CSV import additionally requires the importing user to have 2FA enabled.

Not covered here:

- The dedicated admin screen UI (button copy, modal labels, table columns) → [[marketing-seo-301-redirects]].
- **Whole-domain forwarding** — native only to this store's own primary domain ([[settings-domains-primary]]); [[apps-domain-redirect]] is own-stores geo-routing; no native forward to an external domain ([[seo-301-redirects-types]]).
- HTTPS / www / trailing-slash redirects — automatic, not rules on this manager → [[seo-search-console-indexing]].

## Contrasts

- **Auto-tracked URL handle history (30-day TTL) vs. Manual 301 redirect (no TTL)** — renaming a product slug auto-creates an internal redirect that lasts 30 days. After 30 days, the old URL 404s — unless the merchant manually creates a 301 row, which has no expiration. Merchants migrating from another platform should use manual rows, not rely on auto-tracking.
- **301 vs canonical vs robots Disallow vs noindex** — see [[seo-canonical-noindex]] for the four-signal contrast. 301 changes the URL the browser sees (HTTP 301 + `Location` header); the old URL stops working entirely.
- **Entity-based redirect vs Manual / External row** — entity-based rows store the entity ID; if the entity's slug is renamed later, the redirect target follows the entity automatically. Manual / External rows store frozen URLs.
- **Cascade-on-delete: entity rows vs other rows** — when an entity is deleted, entity-based redirect rows pointing to it are auto-deleted. Manual / External / Section redirects are NEVER auto-deleted.

## Where it applies

### Redirect row types

[[marketing-seo-301-redirects]] is a per-URL redirect manager. Every redirect created here is **301 (permanent)** — there is no 302 option. Types:

- **Manual** — free-form path on the same store.
- **External** — full URL to a different domain.
- **Product / Category / Vendor / Page / Blog / Article** — picks an entity by ID; the redirect's target URL follows the entity if the entity's slug is renamed later (because the row stores the entity ID, not a frozen URL).
- **Section** — built-in storefront route (Home / Contacts / Cart / Wishlist / etc.).

### Cache

Redirects are cached per requested URI for **24 hours**. Saving / editing / deleting a redirect flushes the cache so the merchant sees the change immediately — but external CDN / browser caches may serve stale 301s for longer.

### Wildcards

A literal `*` in `old_url` is treated as `%` in the SQL LIKE lookup. So `/old-shop/*` matches any sub-path of `/old-shop/`.

### Marketing-parameter preservation

When a rule fires, exactly these ten parameters are copied onto the target, so analytics still attribute the click: `fbclid`, `gclid`, `gclsrc`, `msclkid`, `dclid`, `zanpid`, `utm`, `utm_source`, `utm_medium`, `utm_campaign`. Every other parameter is dropped, including `utm_term`, `utm_content` and `utm_id`. A rule without `*` matches only an address with no query string, so a visit to `/old?gclid=…` needs a rule such as `/old*` ([[seo-301-redirects-wildcards]]). The automatic 301 after a rename drops the whole query string.

### Cascade on entity delete

When a product / category / vendor / page / blog / article is deleted, **entity-based** redirect rows pointing to it are auto-deleted. Manual / External / Section redirects are never auto-deleted.

### CSV import wizard

The CSV import on [[marketing-seo-301-redirects]] lets the merchant upload a CSV of `old_url, new_url` pairs through a 3-step modal (upload → map columns → confirm). The import runs as a **background job**; duplicates by `old_url` are deleted-then-reinserted, so **re-importing the same CSV is idempotent**.

### Redirect lookup prefix optimization

The redirect middleware uses a prefix shortcut for **7 named first-path-segments** only:

`product`, `category`, `vendor`, `blog`, `article`, `page`, `selection`.

Any other first path segment triggers a slower full-LIKE scan across all redirect rows.

### Activation routes — when the middleware runs

The redirect middleware runs **before the page renders** on these "indexable" route names — see [[seo-route-catalog]]:

`site.home`, `selection`, `site.showcase`, `site.vendors`, `site.vendor.view`, `site.tag`, `category.view`, `category.list`, `blog.list`, `blog.view`, `blog.article.view`, `page`, `site.preview.page`, `bundles.list.list`, `bundles.list.category`, `product.view`, `products.list`, `contacts`.

So a matching rule overrides a live, working page on these routes; it is not a 404-only fallback. A storefront 404 on any path runs the same lookup again. A rule on a live non-indexable page (cart, checkout, account, search) never fires — see [[seo-301-redirects-middleware]].

### Auto-tracked URL handle history — 30-day TTL

Products, categories, vendors, CMS pages, blog categories, blog articles and selections have a `url_handle` (slug), generated from the name and editable on the item's editor.

When the handle changes, the platform keeps the OLD handle in a hidden history for **30 days**: no row appears on [[marketing-seo-301-redirects]]. Within that window the old address of a product, category, selection, page or blog category answers a 301 to the current one (a vendor's old address still opens the vendor page (verify); articles (verify)). Each retired handle keeps its own 30 days, counted from the rename that retired it. After 30 days the auto-tracked old slug stops working; at that point if the merchant cares about preserving SEO, they should create a manual row in [[marketing-seo-301-redirects]] (which has no TTL).

### Permission

[[marketing-seo-301-redirects]] sits behind the `marketing.seo` permission. CSV import on this screen additionally requires the importing user to have 2FA enabled (security measure for bulk URL rewrites that could break SEO).

## Related

- [[seo-handling]] — hub.
- [[seo-canonical-noindex]] — the canonical / 301 / Disallow / noindex four-signal contrast.
- [[seo-route-catalog]] — routes the redirect middleware activates on.
- [[marketing-seo-301-redirects]] — admin screen for per-URL redirects + CSV import.
- [[apps-domain-redirect]] / [[apps-domain-redirect-settings]] — geo-routing between the merchant's own stores (302, lands at root).
- [[product]] / [[category]] / [[vendor]] / [[blog-article]] — entity editors carry the editable `url_handle` and feed the auto-tracked history.
- [[settings-domains]] — primary domain determines redirect target host.

## Open Questions

None.
