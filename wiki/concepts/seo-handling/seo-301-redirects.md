---
type: concept
nav_path: "Concept → SEO handling → 301 redirects and URL handle history"
aliases: ["301 redirect", "Per-URL redirect", "URL handle history", "Slug history", "Auto-tracked redirect", "Redirect CSV import", "Wildcard redirect", "Redirect cache"]
tags: [seo, redirects, 301, url-handle, slug, csv-import, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
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
- Marketing-parameter preservation on redirect: `fbclid`, `gclid`, `gclsrc`, `msclkid`, `utm_*`, `dclid`, `zanpid`.
- Cascade on entity delete (entity-based rows auto-removed; manual / external / section rows are not).
- CSV import wizard: 3-step modal (upload → map columns → confirm), background job, idempotent re-import.
- Auto-tracked URL handle history: 30-day TTL, internal 301, fallback when the handle changes.
- Redirect lookup prefix optimization for **7 named prefixes** only: `product`, `category`, `vendor`, `blog`, `article`, `page`, `selection` — any other first path segment triggers a slower full-LIKE scan.
- Permission gate: `marketing.seo`; CSV import additionally requires the importing user to have 2FA enabled.

Not covered here:

- The dedicated admin screen UI (button copy, modal labels, table columns) → [[marketing-seo-301-redirects]].
- **Cross-domain redirects** (whole old domain → current store) — different mechanism → [[apps-domain-redirect]].
- HTTPS / www / trailing-slash redirects — handled by storefront infrastructure, not by this manager.

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

The redirect middleware preserves these tracking parameters onto the redirect target so the merchant's analytics still attribute the click:

`fbclid`, `gclid`, `gclsrc`, `msclkid`, `utm_*`, `dclid`, `zanpid`.

### Cascade on entity delete

When a product / category / vendor / page / blog / article is deleted, **entity-based** redirect rows pointing to it are auto-deleted. Manual / External / Section redirects are never auto-deleted.

### CSV import wizard

The CSV import on [[marketing-seo-301-redirects]] lets the merchant upload a CSV of `old_url, new_url` pairs through a 3-step modal (upload → map columns → confirm). The import runs as a **background job**; duplicates by `old_url` are deleted-then-reinserted, so **re-importing the same CSV is idempotent**.

### Redirect lookup prefix optimization

The redirect middleware uses a prefix shortcut for **7 named first-path-segments** only:

`product`, `category`, `vendor`, `blog`, `article`, `page`, `selection`.

Any other first path segment triggers a slower full-LIKE scan across all redirect rows.

### Activation routes — when the middleware runs

The redirect middleware activates on these "indexable" route names only — see [[seo-route-catalog]] for the full enumeration:

`site.home`, `selection`, `site.showcase`, `site.vendors`, `site.vendor.view`, `site.tag`, `category.view`, `category.list`, `blog.list`, `blog.view`, `blog.article.view`, `page`, `site.preview.page`, `bundles.list.list`, `bundles.list.category`, `product.view`, `contacts`.

### Auto-tracked URL handle history — 30-day TTL

Every indexable entity (product, category, vendor, CMS page, blog article) has a `url_handle` (slug) that forms the storefront URL. The handle is auto-generated from the entity name when the entity is created — slugified, lower-case, dash-separated. The merchant can edit the handle on the entity's editor.

When the handle changes, the platform records the OLD handle into an internal URL-handle-history with a **30-day TTL**. The storefront's controllers consult this history when a 404 would otherwise happen, and serve an internal 301 to the entity's current URL. So the merchant does NOT need to manually create a 301 redirect row when they rename a product / category / page / article — the platform tracks the old slug automatically for 30 days. After 30 days the auto-tracked old slug stops working; at that point if the merchant cares about preserving SEO, they should create a manual row in [[marketing-seo-301-redirects]] (which has no TTL).

### Permission

[[marketing-seo-301-redirects]] sits behind the `marketing.seo` permission. CSV import on this screen additionally requires the importing user to have 2FA enabled (security measure for bulk URL rewrites that could break SEO).

## Related

- [[seo-handling]] — hub.
- [[seo-canonical-noindex]] — the canonical / 301 / Disallow / noindex four-signal contrast.
- [[seo-route-catalog]] — routes the redirect middleware activates on.
- [[marketing-seo-301-redirects]] — admin screen for per-URL redirects + CSV import.
- [[apps-domain-redirect]] / [[apps-domain-redirect-settings]] — whole-domain (cross-domain) redirect app.
- [[product]] / [[category]] / [[vendor]] / [[blog-article]] — entity editors carry the editable `url_handle` and feed the auto-tracked history.
- [[settings-domains]] — primary domain determines redirect target host.

## Open Questions

None.
