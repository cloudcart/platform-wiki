---
type: concept
nav_path: "Concept → Storefront architecture"
aliases: ["Storefront architecture", "Smarty themes", "Theme system", "Storefront framework", "Storefront engine", "Storefront rendering", "Smarty storefront", "Theme inheritance", "Архитектура на storefront", "Smarty шаблони", "Архитектура на магазина", "Тема система"]
tags: [storefront, smarty, themes, architecture, frontend]
plan_gates: []
created: 2026-06-08
updated: 2026-11-09
source_count: 9
---

# Storefront architecture

## Definition

CloudCart's storefront is a **server-rendered, multi-tenant, theme-templated Smarty 4.x application**. Every customer-facing page on every CloudCart-hosted store (`/`, `/category/...`, `/product/...`, `/cart`, `/checkout`, `/account`, `/blog/...`, etc.) is produced by the same platform: an incoming request's host name resolves to the store, the store's active theme is looked up, the request is dispatched to the matching storefront page, and a Smarty template is rendered — first looking under the theme's own templates, then falling back to a shared `_global` template when the theme hasn't overridden it.

Each theme ships **its own compiled JS and CSS bundle** (`scripts.min.js`, `styles.min.css`) built by a per-theme build pipeline, on top of a **shared platform layer** every theme page loads: jQuery 3.2.1 with its plugins in the head and `site/js/build.js` at the end of the page. The cross-theme contract is that layer plus conventions: `.js-*` hook classes, a handful of `cc.*` custom events on `document`, and platform-managed AJAX endpoints under `/ajax/*`, `/ajax-products/*`, `/filters-ts/*`, `/module/*`, `/cart/*`, `/wishlist/*`, `/checkout/*`. Per-merchant visual customisation happens in three layers ([[theme-customization-layers]]) — most notably **Theme Editor variables** substituted into the theme's pre-built `theme.css` at save time, producing a merchant-specific `theme.css` served from storage.

Storefront pages sit behind the platform edge ([[platform-rate-limits]]) for the platform's abuse protections; whole pages are cached by the platform itself ([[storefront-arch-caching-invalidation]]). Asset URLs are cache-busted with a `?<last_build>` query string, so every deploy invalidates every storefront's JS / CSS bundle URLs in one go.

## Sub-pages (in this cluster)

This concept is split into 8 aspect pages. Drill into the aspect that matches the question.

- [[storefront-arch-request-lifecycle]] — host name → rendered HTML; store resolution, route dispatch, page rendering, Smarty compile, response; the three parallel AJAX product-listing endpoint trees.
- [[storefront-arch-search-read-side]] — why catalogue surfaces read from the search index not the database; the sync pipeline (live-sync vs full re-index); the `searchable-import4` / `searchable-import8` / `cc-system7` queues; the "queue lag, not bug" operational rule.
- [[storefront-arch-theme-inheritance]] — per-file override on the theme's own templates → shared `_global` template fallback; what lives in `_global` (cart, checkout, customer, product, payments, draft_order, form-components, geo_zone); anatomy of a new theme.
- [[storefront-arch-js-bundles]] — the shared platform scripts and the per-theme `scripts.min.js`, where each loads and with what `defer`; the `.js-*` hook-class convention (verified set); the `cc.*` custom-event bus (`cc.variant.changed`, `cc.filters.filters.after`, `cc.ajax.reload`, etc.).
- [[storefront-arch-smarty-plugins]] — the Smarty plugin catalogue registered on every storefront request (`route`, `site`, `setting`, `config`, `lang`, `__`, `money`, `themeScript`, `styleScript`, `csrf_token`, `view`, `noImage`, `routeExists`, `activeRoute`, `routeParameter`, plus standard template helpers).
- [[storefront-arch-css-assets]] — theme `theme.css` + Theme Editor variable substitution → storage; the storefront `<head>` asset order; the `last_build` cache-buster vs the per-merchant `stylesheet_version`.
- [[storefront-arch-caching-invalidation]] — the full-page cache (about 20 minutes for guests, 1–2 days for crawlers), what a save does and does not clear, the `X-Cache` headers.
- [[storefront-arch-root-files-and-pwa]] — what a store serves at its root, the platform `/manifest.json` and push service worker, install-as-app, `/.well-known/` files.

## Why it matters to the merchant

Six consequences that shape what a merchant can change and how fast it reaches visitors:

- **Theme inheritance keeps cart and checkout consistent.** Most themes do NOT override the cart/checkout templates, so checkout looks the same regardless of the theme's home-page style; a theme that does override them can break checkout subtly — see [[storefront-arch-theme-inheritance]].
- **The catalogue reads from the search index, not the database.** When a merchant says *"I changed it in admin but the storefront still shows the old value"*, the answer is usually **queue lag on `searchable-import4`** — see [[storefront-arch-search-read-side]] + [[background-queue-inventory]].
- **jQuery is shared, theme code is not.** Every theme page loads the platform's jQuery; theme behaviour lives in each theme's own bundle, so cross-theme behaviour cannot be assumed — see [[storefront-arch-js-bundles]].
- **Guests see a change within about 20 minutes.** A save does not clear cached pages; signed-in customers and anyone signed in to the admin see it at once — see [[storefront-arch-caching-invalidation]].
- **Asset URLs are versioned by `last_build`.** Every platform-wide deploy flips every storefront's JS / CSS bundle URL, so merchants don't need to "clear the cache" after a platform update — see [[storefront-arch-css-assets]].
- **No server access.** Stores run on the shared platform, not on hosting accounts of their own: there is no FTP / SFTP, SSH, cPanel or direct database access, and no admin screen issues such credentials. Data is reached through the admin, exports and the APIs ([[json-api-v2]], [[admin-graphql-api]]); the look through [[theme-customization-layers]] or Nitrogen ([[nitrogen-vs-themes]]). FTP fields in ERP apps ([[apps-posmaster]]) point at the merchant's own server.

## Scope

The 8 sub-pages above cover the storefront end to end. The theme catalogue holds 71 production-active themes.

What it does NOT cover:

- Plan gating, billing, or theme purchase — see [[design-themes]] and [[plan-gates]].
- The admin panel (`/admin/*`) — Vue 3 SPA backed by [[json-api-v2]].
- The Nitrogen headless storefront — separate stack ([[headless-storefront]]) using GraphQL at `/api/sf` and Cloudflare Workers.
- SEO meta-tag emission, canonical URLs, robots.txt, sitemap — see [[seo-handling]].
- Multi-language / multi-currency rendering — see [[multi-language]] and [[multi-currency]].
- The checkout state machine — see [[checkout-flow]] and [[cart-vs-order-lifecycle]].

## Contrasts

- **Smarty storefront vs Vue admin panel** — server-rendered Smarty for customers; Vue 3 SPA at `/admin/*` backed by [[json-api-v2]] for staff. Same the application framework monolith, different render layers.
- **Smarty storefront vs Nitrogen headless** — Smarty is the default (works out of the box at `<store>.cloudcart.com`). [[headless-storefront]] is a separate optional product using Storefront GraphQL at `/api/sf`. A merchant can run **both at once** on different hostnames. Choosing between them: [[nitrogen-vs-themes]].
- **JSON-API v2 vs Storefront GraphQL** — `/api/v2/*` is admin-side (API key); `/api/sf` is customer-side (one storefront's token).
- **Per-theme JS bundle vs shared platform layer** — each theme ships its own `js/scripts.min.js`; jQuery and the shared plugins come from the platform. See [[storefront-arch-js-bundles]].
- **Theme override vs per-merchant override** — the **theme** is the file-system layer (merchants don't edit the theme templates directly). The **per-merchant override** is the [[theme-customization-layers]] stack (Theme Editor variables, Custom CSS/JS, dynamic Page-Builder pages).

## Where it applies

Every Smarty-rendered customer-facing storefront page — catalogue ([[home]], [[storefront-category]], [[product-detail]], [[products-list]], [[search]], [[tag]], [[storefront-vendor]], [[selection]], [[showcase]], [[storefront-bundles-list]]); cart and checkout ([[storefront-cart]], [[checkout]], [[checkout-return]]); customer account ([[customer-account]], [[customer-orders]], [[wishlist]], [[customer-addresses]], [[customer-login]], [[customer-register]]); static content ([[page]], [[blog-list]], [[contacts]]); embedded surfaces ([[restore-abandoned]], `/embed/product/{id}`, `/embed/checkout`, `/checkout-link/{variant_id?}`, `/tracking/{hash}`). Plus the AJAX endpoint trees catalogued in [[storefront-arch-request-lifecycle]]. Per-merchant customisation lives in [[theme-customization-layers]] / [[design-themes]] / [[design-theme-editor]] / [[design-custom-assets]] / [[design-modules]]. Edge / infrastructure: [[platform-rate-limits]], [[seo-handling]], [[geo-targeting]].

## Related

- [[theme-customization-layers]] — the 3-layer per-merchant customisation stack.
- [[design-themes]] — Themes catalogue, install, switch, purchase.
- [[design-theme-editor]] — the visual variable editor at `/admin/builder`.
- [[design-custom-assets]] — the raw HTML/CSS/JS injection screen at `/admin/design/custom-assets`.
- [[design-modules]] — per-theme module catalogue.
- [[storefront-themes-catalog]] — the catalogue of themes.
- [[storefront-known-issues]] — cross-theme storefront issues.
- [[headless-storefront]] — the Nitrogen alternative storefront.
- [[nitrogen-vs-themes]] — a standard theme compared with a Nitrogen storefront.
- [[json-api-v2]] — the admin-side REST API.
- [[platform-rate-limits]] — the edge rate-limit layer.
- [[seo-handling]] — meta tags, canonical URLs, robots.txt, sitemap.
- [[geo-targeting]] — currency / language auto-switching.
- [[plan-gates]] — plan-feature gating (paid themes, `storefront_builder`).
- [[background-queue-inventory]] — the search-index sync queues.

## Open Questions

Distributed across the 8 aspect pages.
