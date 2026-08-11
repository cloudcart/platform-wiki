---
type: concept
nav_path: "Concept → Storefront architecture → Caching and invalidation"
aliases: ["Storefront caching", "Storefront invalidation", "the platform edge fragment cache", "Compiled Smarty cache", "Theme switch invalidation", "Theme Editor save invalidation", "Custom CSS save invalidation", "CcCache"]
tags: [storefront, cache, invalidation, themes, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-23
source_count: 4
---

> Part of [[storefront-architecture]]. See the hub for related aspects (request lifecycle, theme inheritance, the search index read-side, JS bundles, Smarty plugins, CSS assets).

# Storefront — caching and invalidation

## Definition

Storefront pages can be cached at three layers, each with its own invalidation rules:

1. **the platform edge fragment cache** ([[platform-rate-limits]]) — a per-URL, per-tenant, per-language cache that sits in front of the storefront; a hit serves cached HTML without re-rendering the page. Invalidated on storefront-relevant model updates.
2. **Per-theme compiled templates** — each (merchant, theme, template) is compiled and cached separately, and is rebuilt automatically the next time a request hits it after the theme author ships a new template file. One merchant's recompile never invalidates another's, so a theme switch on one store leaves other stores' compiled templates untouched.
3. **Browser + intermediate CDN** — driven by the asset URL's `?<last_build>` or `?<stylesheet_version>` query string (see [[storefront-arch-css-assets]]). Asset bytes are served with long-lived `Cache-Control`; cache-busting relies on the URL query string flipping, so the platform cannot purge a visitor's browser cache directly — it can only emit a different URL.

**Per-context cache keying (important).** The storefront full-page cache key is **not** just the URL — it is composed application-side from the **site (tenant)**, the **URL path**, the **query string**, the **customer group** (`cgid.<group_id>`), and the active **geo-zone** (`zone-<geo_zone_id>`, from the store-location cookie). So the *same* URL is cached **separately per customer group and per geo-zone**: a VIP and a retail shopper hitting the same product URL get different cached buckets. This is what keeps [[customer-group-targeting|group-differentiated pricing/discounts]] and zone-differentiated availability correct under full-page caching — and why a store with many groups/zones multiplies its cache entries per URL.

**Only guests and crawlers are full-page-cached — signed-in customers always render fresh.** Because the key is per customer *group* (`cgid`), not per individual customer, a logged-in customer (and any admin preview) **bypasses the full-page cache entirely** and gets a freshly rendered page on every request. The reason is leak-avoidance: per-customer content that ends up in the HTML — the wishlist "heart" state on product cards, the header wishlist, the cart — is *not* part of the cache key, so serving one shopper's cached group bucket to another shopper in the same group would show them the first shopper's personal state. The trade-off is that signed-in shoppers don't get the cache speed-up (their pages are rendered per request), while the bulk of anonymous traffic still hits the cache. So if a merchant reports that a *logged-in* customer sees up-to-date content while a *guest* still sees a stale page (or vice-versa), this split is why.

Different operational actions trigger different invalidation cascades. A theme switch is aggressive; a Theme Editor save is medium; a Custom CSS/JS save is lightest (no explicit cache key flipped — the storefront picks up new code on next render, but the CDN may serve stale HTML for a while).

## Scope

Covered:

- The three cache layers and what each holds.
- The invalidation cascade for theme switch, Theme Editor save, Custom CSS/JS save.
- The interaction with the platform-wide `last_build` and per-merchant `stylesheet_version` cache-busters.
- The role of the per-storefront in-process `CcCache`, which holds frequently-read merchant data (settings, theme metadata, currency table). It is cleared on theme switch (and a few other heavy operations) but NOT by routine product or category saves. Because it lives in-process per worker, a busy store may see brief inconsistency between requests until every worker has re-fetched.

Not covered here:

- The search index read-side queue lag — that's a separate consistency lag, not a cache — see [[storefront-arch-search-read-side]].
- The asset URL emission with `last_build` — see [[storefront-arch-css-assets]].
- the platform edge internals (TLS termination and caching) — see [[platform-rate-limits]].

## Contrasts

- **Cache vs queue lag** — the storefront has TWO independent consistency lags: cache invalidation (this concept) and search-index queue lag ([[storefront-arch-search-read-side]]). When a merchant says *"my change isn't visible"*, both are candidates and the symptoms differ. search-index queue lag affects catalogue surfaces (product cards, listings); cache lag affects whole-page renders and asset URLs.
- **Theme switch vs Theme Editor save** — theme switch is the aggressive cascade: it recompiles the merchant's CSS, regenerates storefront translations, re-seeds the theme's demo landing pages, clears `CcCache`, and bumps `stylesheet_version` (so the browser re-fetches `theme.css`); the platform edge fragment cache then invalidates on the next render. The next storefront request re-fetches everything. Theme Editor save is much lighter: it only recompiles the merchant's `theme.css`, stamps `stylesheet_version`, and clears the `front_theme` per-merchant cache — the theme-author-shipped JS/CSS bundles are left alone and other storefront caches are untouched.
- **Theme Editor save vs Custom CSS/JS save** — Theme Editor save flips `stylesheet_version` (immediate browser invalidation). Custom CSS/JS save does NOT explicitly invalidate any cache key — the storefront picks it up on the next render, but the merchant's CDN (if any) and the platform edge fragment cache (until its TTL elapses) may keep serving the old HTML. To confirm a Custom CSS/JS change is live, save then open "View store" in a private/incognito window to bypass your own browser cache. This is intentional: Custom CSS/JS is the merchant's escape hatch and is edited frequently, so a forced cache flush per save would be too costly.

## Where it applies

- **the platform edge fragment cache** — every cached storefront URL across every tenant.
- **Compiled Smarty cache** — every (merchant, theme, template) triple, cached per merchant.
- **Browser cache** — every visitor's browser.
- **CDN** (if the merchant fronts the storefront with a CDN) — depends on CDN config.

Invalidation triggers:

- Product save, category save, vendor save → the platform edge fragment invalidation for affected URLs.
- Page save, blog publish → the platform edge fragment invalidation.
- Theme switch → all-layers cascade.
- Theme Editor save → `stylesheet_version` flip + `front_theme` cache clear.
- Custom CSS/JS save → no explicit invalidation; picked up on next render.
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
- **the platform edge fragment cache TTL** and the exact set of model updates that emit invalidation signals — see [[platform-rate-limits]] (verify whether it documents this).
