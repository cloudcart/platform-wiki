---
type: concept
nav_path: "Concept → Storefront architecture → Caching and invalidation"
aliases: ["Storefront caching", "Storefront invalidation", "Full-page cache", "Page cache", "X-Cache", "X-Cache-Expires", "Clear storefront cache", "Compiled Smarty cache", "Theme switch invalidation", "Theme Editor save invalidation", "Custom CSS save invalidation", "CcCache"]
tags: [storefront, cache, invalidation, themes, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-11-09
source_count: 5
---

> Part of [[storefront-architecture]]. See the hub for related aspects (request lifecycle, theme inheritance, the search index read-side, JS bundles, Smarty plugins, CSS assets).

# Storefront — caching and invalidation

## Definition

Storefront pages can be cached at three layers, each with its own invalidation rules:

1. **The platform's full-page cache** — the finished HTML of the home page, product, category, listing, search, tag, vendor, bundle, blog and static / Dynamic pages (plus sitemap and feed), replayed to the next visitor. **Guests: 20 minutes** from the visit that rendered the copy. **Crawlers: a separate copy kept 1–2 days** (a random lifetime per page). Maintenance page: 5 minutes. No save in the admin clears it — the cached copy is served until it expires. Every response carries `X-Cache`: `HIT` (served from the cache), `MISS` (rendered and stored now) or `BYPASS` (not cached); a cached page also carries `X-Cache-Expires`, the date and time (ISO 8601) the served copy expires, after which the next visit renders fresh. The store's whole cache, guests and crawlers, is dropped only by the Admin GraphQL `purgeStorefrontCache` mutation ([[admin-graphql-api]]), a logo change made through that API, or CloudCart staff; no admin screen has a clear-cache button.
2. **Per-theme compiled templates** — each (merchant, theme, template) is compiled and cached separately, and is rebuilt automatically the next time a request hits it after the theme author ships a new template file. One merchant's recompile never invalidates another's, so a theme switch on one store leaves other stores' compiled templates untouched.
3. **Browser + intermediate CDN** — driven by the asset URL's `?<last_build>` or `?<stylesheet_version>` query string (see [[storefront-arch-css-assets]]). Asset bytes are served with long-lived `Cache-Control`; cache-busting relies on the URL query string flipping, so the platform cannot purge a visitor's browser cache directly — it can only emit a different URL.

**Per-context cache keying (important).** The storefront full-page cache key is **not** just the URL — it is composed application-side from the **site (tenant)**, the **URL path**, the **query string**, the **customer group** (`cgid.<group_id>`), and the active **geo-zone** (`zone-<geo_zone_id>`, from the store-location cookie). So the *same* URL is cached **separately per customer group and per geo-zone**: a VIP and a retail shopper hitting the same product URL get different cached buckets. This is what keeps [[customer-group-targeting|group-differentiated pricing/discounts]] and zone-differentiated availability correct under full-page caching — and why a store with many groups/zones multiplies its cache entries per URL.

**Only guests and crawlers are full-page-cached — signed-in customers always render fresh.** Because the key is per customer *group* (`cgid`), not per individual customer, a logged-in customer (and any browser signed in to the store's admin) **bypasses the full-page cache entirely** and gets a freshly rendered page on every request. The reason is leak-avoidance: per-customer content in the HTML (wishlist hearts, the header wishlist, the cart) is *not* part of the key, so a shared group copy would show one shopper's state to another. So if a merchant reports that a *logged-in* customer sees up-to-date content while a *guest* still sees a stale page (or vice-versa), this split is why.

No admin save clears the full-page cache, so guests may see the old page for up to 20 minutes and crawlers for up to 2 days. The saves differ only in which internal caches they renew (below).

## Scope

Covered:

- The three cache layers and what each holds.
- The invalidation cascade for theme switch, Theme Editor save, Custom CSS/JS save.
- The interaction with the platform-wide `last_build` and per-merchant `stylesheet_version` cache-busters.
- The per-store `CcCache` of frequently read data (settings, theme metadata, currency table), renewed on theme switch and by module and theme-setting saves (verify the full list).

Not covered here:

- The search index read-side queue lag — that's a separate consistency lag, not a cache — see [[storefront-arch-search-read-side]].
- The asset URL emission with `last_build` — see [[storefront-arch-css-assets]].
- the platform edge internals (TLS termination and caching) — see [[platform-rate-limits]].

## Contrasts

- **Cache vs queue lag** — the storefront has TWO independent consistency lags: cache invalidation (this concept) and search-index queue lag ([[storefront-arch-search-read-side]]). When a merchant says *"my change isn't visible"*, both are candidates and the symptoms differ. search-index queue lag affects catalogue surfaces (product cards, listings); cache lag affects whole-page renders and asset URLs.
- **Theme switch vs Theme Editor save** — theme switch is the aggressive cascade: it recompiles the merchant's CSS, regenerates storefront translations, re-seeds the theme's demo landing pages, clears `CcCache`, and bumps `stylesheet_version` (so the browser re-fetches `theme.css`); guests get the new theme once their cached copy expires. Theme Editor save is much lighter: it only recompiles the merchant's `theme.css`, stamps `stylesheet_version`, and clears the `front_theme` per-merchant cache — the theme-author-shipped JS/CSS bundles are left alone and other storefront caches are untouched.
- **Theme Editor save vs Custom CSS/JS save** — a Theme Editor save flips `stylesheet_version`, but the stylesheet address is written into the page HTML, so a guest gets the new file once the cached page expires. A Custom CSS/JS save renews only the internal cache stamp; the code sits inside the cached HTML, so guests see it within 20 minutes. To check a change at once, view the store while signed in to the admin (those visits skip the cache); a private window shows what a guest sees, cached copy included.

## Where it applies

- **Full-page cache** — the page types listed above, for guests and crawlers; never the cart, checkout, account pages or a non-GET request.
- **Compiled Smarty cache** — every (merchant, theme, template) triple, cached per merchant.
- **Browser cache** — every visitor's browser.
- **CDN** (if the merchant fronts the storefront with a CDN) — depends on CDN config.

Invalidation triggers:

- Product, category, vendor, page, blog, module or Custom CSS/JS save → no full-page clear; guests get it within 20 minutes, crawlers within 1–2 days.
- `purgeStorefrontCache`, or a logo change through the Admin GraphQL API → the store's whole full-page cache is dropped.
- Theme switch → all-layers cascade.
- Theme Editor save → `stylesheet_version` flip + `front_theme` cache clear.
- Platform deploy → `last_build` flip (asset URLs).

## Related

- [[storefront-architecture]] — hub.
- [[storefront-arch-css-assets]] — `last_build` and `stylesheet_version` cache-busters.
- [[storefront-arch-request-lifecycle]] — where compiled Smarty templates fit in the lifecycle.
- [[storefront-arch-search-read-side]] — the OTHER consistency lag (queue, not cache).
- [[platform-rate-limits]] — the platform edge layer that holds Layer 1.
- [[design-themes]] — the theme switch trigger.
- [[design-theme-editor]] — the Theme Editor save trigger.
- [[design-custom-assets]] — the Custom CSS/JS save trigger.
- [[theme-customization-layers]] — the 3-layer customisation stack whose saves invalidate caches differently.

## Open Questions

- **Whether theme switch regenerates translations for all locales or just the current locale** (verify).
- **The exact set of demo landing pages re-seeded on theme switch** — verify by reading the theme-switch routine.
- **The complete list of operations that clear `CcCache`** — verify (theme switch is confirmed; others observed in passing).
- ✅ Resolved: the full-page cache lives in the platform (20 minutes for guests, 1–2 days for crawlers) and no save clears it.
