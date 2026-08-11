---
type: concept
nav_path: "Concept → Storefront architecture"
aliases: ["Storefront architecture", "Smarty themes", "Theme system", "Storefront framework", "Storefront engine", "Storefront rendering", "Smarty storefront", "Theme inheritance", "Архитектура на storefront", "Smarty шаблони", "Архитектура на магазина", "Тема система"]
tags: [storefront, smarty, themes, architecture, frontend]
plan_gates: []
created: 2026-06-08
updated: 2026-06-10
source_count: 8
---

# Storefront architecture

## Definition

CloudCart's storefront is a **server-rendered, multi-tenant, theme-templated Smarty 4.x application**. Every customer-facing page on every CloudCart-hosted store (`/`, `/category/...`, `/product/...`, `/cart`, `/checkout`, `/account`, `/blog/...`, etc.) is produced by the same platform: an incoming request's host name resolves to the store, the store's active theme is looked up, the request is dispatched to the matching storefront page, and a Smarty template is rendered — first looking under the theme's own templates, then falling back to a shared `_global` template when the theme hasn't overridden it.

Each theme ships **its own compiled JS and CSS bundle** (`scripts.min.js`, `styles.min.css`) built by a per-theme build pipeline. There is **no platform-level storefront JS shipped across all themes** — the only cross-theme contract is a set of conventions: `.js-*` hook classes, jQuery 3.x as the framework of choice, a handful of `cc.*` custom events on `document`, and platform-managed AJAX endpoints under `/ajax/*`, `/ajax-products/*`, `/filters-ts/*`, `/module/*`, `/cart/*`, `/wishlist/*`, `/checkout/*`. Per-merchant visual customisation happens in three layers ([[theme-customization-layers]]) — most notably **Theme Editor variables** substituted into the theme's pre-built `theme.css` at save time, producing a merchant-specific `theme.css` served from storage.

Storefront pages are protected behind the platform edge ([[platform-rate-limits]]) — TLS termination and cached fragments. Asset URLs are cache-busted with a `?<last_build>` query string, so every deploy invalidates every storefront's JS / CSS bundle URLs in one go.

## Sub-pages (in this cluster)

This concept is split into 7 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[storefront-arch-request-lifecycle]] — host name → rendered HTML; store resolution, route dispatch, page rendering, Smarty compile, response; the three parallel AJAX product-listing endpoint trees.
- [[storefront-arch-search-read-side]] — why catalogue surfaces read from the search index not the database; the sync pipeline (live-sync vs full re-index); the `searchable-import4` / `searchable-import8` / `cc-system7` queues; the "queue lag, not bug" operational rule.
- [[storefront-arch-theme-inheritance]] — per-file override on the theme's own templates → shared `_global` template fallback; what lives in `_global` (cart, checkout, customer, product, payments, draft_order, form-components, geo_zone); anatomy of a new theme.
- [[storefront-arch-js-bundles]] — per-theme `scripts.min.js` composition (bundled jQuery 3.x + theme code + third-party plugins); the `.js-*` hook-class convention (verified set); the `cc.*` custom-event bus (`cc.variant.changed`, `cc.filters.filters.after`, `cc.ajax.reload`, etc.).
- [[storefront-arch-smarty-plugins]] — the Smarty plugin catalogue registered on every storefront request (`route`, `site`, `setting`, `config`, `lang`, `__`, `money`, `themeScript`, `styleScript`, `csrf_token`, `view`, `noImage`, `routeExists`, `activeRoute`, `routeParameter`, plus standard template helpers).
- [[storefront-arch-css-assets]] — theme `theme.css` + Theme Editor variable substitution → storage; the storefront `<head>` asset order; the `last_build` cache-buster vs the per-merchant `stylesheet_version`.
- [[storefront-arch-caching-invalidation]] — three cache layers (the platform edge fragment cache, per-theme compiled Smarty cache, browser + CDN); invalidation cascades on theme switch vs Theme Editor save vs Custom CSS/JS save.

## Why it matters to the merchant

Every architectural decision here shapes what the merchant can change, how fast a change reaches the visitor, and where to look when something looks wrong. Five high-impact consequences:

- **Theme inheritance keeps cart and checkout consistent.** Most themes do NOT override the cart/checkout templates, so checkout looks the same regardless of the theme's home-page style; a theme that does override them can break checkout subtly — see [[storefront-arch-theme-inheritance]].
- **The catalogue reads from the search index, not the database.** When a merchant says *"I changed it in admin but the storefront still shows the old value"*, the answer is usually **queue lag on `searchable-import4`** — see [[storefront-arch-search-read-side]] + [[background-queue-inventory]].
- **There is no shared platform JS.** Every theme bundles its own jQuery + plugins, so a custom script from [[design-custom-assets]] runs in the theme's jQuery world and cross-theme behaviour cannot be assumed — see [[storefront-arch-js-bundles]].
- **Theme Editor saves and Custom CSS/JS saves invalidate different caches.** A colour change rebuilds `theme.css` and bumps `stylesheet_version`; a Custom CSS/JS save is picked up on the next render but the CDN may serve stale HTML — see [[storefront-arch-caching-invalidation]].
- **Asset URLs are versioned by `last_build`.** Every platform-wide deploy flips every storefront's JS / CSS bundle URL, so merchants don't need to "clear the cache" after a platform update — see [[storefront-arch-css-assets]].

## Scope

Across the 7 sub-pages this concept covers the full request lifecycle, theme inheritance, the Smarty plugin catalogue, the per-theme JS/CSS bundles with the `.js-*` and `cc.*` conventions, the search-index read-side and sync pipeline, and the caching/invalidation layers — see the Sub-pages list above. The platform theme catalogue holds 70+ themes (verified — 71 production-active themes).

What it does NOT cover:

- Plan gating, billing, or theme purchase — see [[design-themes]] and [[plan-gates]].
- The admin panel (`/admin/*`) — Vue 3 SPA backed by [[json-api-v2]].
- The Nitrogen headless storefront — separate stack ([[headless-storefront]]) using GraphQL at `/api/sf` and Cloudflare Workers.
- SEO meta-tag emission, canonical URLs, robots.txt, sitemap — see [[seo-handling]].
- Multi-language / multi-currency rendering — see [[multi-language]] and [[multi-currency]].
- The checkout state machine — see [[checkout-flow]] and [[cart-vs-order-lifecycle]].

## Contrasts

- **Smarty storefront vs Vue admin panel** — server-rendered Smarty for customers; Vue 3 SPA at `/admin/*` backed by [[json-api-v2]] for staff. Same the application framework monolith, different render layers.
- **Smarty storefront vs Nitrogen headless** — Smarty is the default (works out of the box at `<store>.cloudcart.com`). [[headless-storefront]] is a separate optional product using Storefront GraphQL at `/api/sf`. A merchant can run **both at once** on different hostnames.
- **JSON-API v2 vs Storefront GraphQL** — `/api/v2/*` is admin-side (API-key auth, full CRUD); `/api/sf` is customer-side (Storefront token, scoped to one storefront).
- **Per-theme JS bundles vs shared bundle** — each theme ships its own `js/scripts.min.js`. Cross-theme contract is conventions (`.js-*`, `cc.*`), not code. See [[storefront-arch-js-bundles]].
- **Theme override vs per-merchant override** — the **theme** is the file-system layer (merchants don't edit the theme templates directly). The **per-merchant override** is the [[theme-customization-layers]] stack (Theme Editor variables, Custom CSS/JS, dynamic Page-Builder pages).

## Where it applies

Every Smarty-rendered customer-facing storefront page — catalogue ([[home]], [[storefront-category]], [[product-detail]], [[products-list]], [[search]], [[tag]], [[storefront-vendor]], [[selection]], [[showcase]], [[storefront-bundles-list]]); cart and checkout ([[storefront-cart]], [[checkout]], [[checkout-return]]); customer account ([[customer-account]], [[customer-orders]], [[wishlist]], [[customer-addresses]], [[customer-login]], [[customer-register]]); static content ([[page]], [[blog-list]], [[contacts]]); embedded surfaces ([[restore-abandoned]], `/embed/product/{id}`, `/embed/checkout`, `/checkout-link/{variant_id?}`, `/tracking/{hash}`). Plus the AJAX endpoint trees catalogued in [[storefront-arch-request-lifecycle]]. Per-merchant customisation lives in [[theme-customization-layers]] / [[design-themes]] / [[design-theme-editor]] / [[design-custom-assets]] / [[design-modules]]. Edge / infrastructure: [[platform-rate-limits]], [[seo-handling]], [[geo-targeting]].

## Related

- [[theme-customization-layers]] — the 3-layer per-merchant customisation stack on top of the architecture described here.
- [[design-themes]] — Themes catalogue, install, switch, purchase.
- [[design-theme-editor]] — the visual variable editor at `/admin/builder`.
- [[design-custom-assets]] — the raw HTML/CSS/JS injection screen at `/admin/storefront/custom-assets`.
- [[design-modules]] — per-theme module catalogue.
- [[storefront-themes-catalog]] — sibling concept: the catalogue of themes available.
- [[storefront-known-issues]] — sibling concept: cross-theme storefront issues.
- [[headless-storefront]] — the Nitrogen alternative storefront.
- [[json-api-v2]] — the admin-side REST API.
- [[platform-rate-limits]] — the edge rate-limit and cache layer.
- [[seo-handling]] — meta tags, canonical URLs, robots.txt, sitemap.
- [[multi-language]] — language resolution and translated strings.
- [[multi-currency]] — currency resolution and price formatting.
- [[geo-targeting]] — currency / language auto-switching.
- [[checkout-flow]] — the multi-step checkout state machine.
- [[cart-vs-order-lifecycle]] — the cart / order entity lifecycle.
- [[plan-gates]] — plan-feature gating (paid themes, `storefront_builder`).
- [[background-queue-inventory]] — the search-index sync queues.

## Open Questions

Distributed across the 7 aspect pages.
