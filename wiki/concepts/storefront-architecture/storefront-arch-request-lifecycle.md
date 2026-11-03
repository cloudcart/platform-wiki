---
type: concept
nav_path: "Concept → Storefront architecture → Request lifecycle"
aliases: ["Storefront request lifecycle", "Host to HTML", "Site resolver lifecycle", "Storefront route dispatch", "Storefront AJAX endpoints"]
tags: [storefront, smarty, lifecycle, routes, ajax, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-11
source_count: 4
---

> Part of [[storefront-architecture]]. See the hub for related aspects (theme inheritance, search read-side, JS bundles, Smarty plugins, CSS assets, caching).

# Storefront — request lifecycle

## Definition

The request lifecycle is the deterministic chain that turns an incoming request on a storefront hostname into a fully-rendered HTML response. It is the **same chain for every CloudCart-hosted store** — multi-tenancy lives entirely inside one resolver step, not in separate code paths per merchant.

The pivot is **site resolution**: the platform maps the inbound `Host` header to the merchant's store record, reads its active theme slug (referenced in templates as the `site('template')` setting key), and prepares a per-tenant template engine with the platform's full plugin catalogue. Everything downstream — route dispatch, data loading, template lookup with theme-then-`_global` fallback, and render — runs against that per-request, per-tenant template instance.

## Scope

Covered:

- The end-to-end lifecycle from the platform edge to rendered HTML in the browser.
- Site resolution: `Host` → store record, theme slug, per-tenant template engine and its isolated compiled-template cache.
- The route dispatch model: each storefront URL maps to a page handler, grouped by feature (catalogue, cart, checkout, customer, blog, embedded surfaces).
- The page-dispatch helper that wraps a named template in the `main` layout (header, footer, head, scripts).
- The three parallel AJAX product-listing endpoint trees (`/ajax/*`, `/ajax-products/*`, `/filters-ts/*`).
- The full inventory of platform-managed AJAX endpoints (cart drawer, checkout fragments, autosuggest, wishlist, courier offices).

Compiled-template isolation: each merchant has its own per-tenant compiled-template cache. This means a merchant switching theme does **not** invalidate other merchants' compiled templates; and a theme-author push of new template files invalidates the compiled copy the next time a request hits each affected (theme, template) pair, because the source modification time is checked.

Not covered here:

- Template inheritance details (theme templates → `_global` fallback) — see [[storefront-arch-theme-inheritance]].
- The Smarty plugin catalogue registered at site resolution — see [[storefront-arch-smarty-plugins]].
- The search read-side query path for catalogue pages — see [[storefront-arch-search-read-side]].
- Asset URL emission with `last_build` — see [[storefront-arch-css-assets]].

## Contrasts

- **`main`-layout dispatch vs raw template render** — most pages route through the page-dispatch helper, which always wraps the supplied view inside the `main` layout. The `/embed/*` routes may bypass this to render bare templates (verify).
- **Three AJAX product-listing trees** — three parallel routes the merchant doesn't choose between (the active theme decides which it consumes):
  - `/ajax/<entity>/<slug>` — full HTML fragment (products + filters + pagination).
  - `/ajax-products/<entity>/<slug>` — products-only HTML fragment.
  - `/filters-ts/<entity>/<slug>` — filter-state fragment alone (used by themes that maintain filter state in the URL).
  Whether `/ajax/*` is a deprecation path or a forever-three-flavours design (verify — a merchant on an older theme uses `/ajax/*`; newer themes use `/filters-ts/*`).

## Where it applies

Every Smarty-rendered storefront page goes through this lifecycle. The lifecycle runs, in order: the platform edge ([[platform-rate-limits]]) terminates TLS and applies the platform's abuse protections; static asset URLs (`/cdn/...`, `/themes/.../js/...`, `/themes/.../css/...`) are served directly from cache and the rest is passed to the application; site resolution maps `Host` → store record, theme slug, and per-tenant template engine + compiled-template cache; the URL is dispatched to its page handler; data is loaded (catalogue from the search index per [[storefront-arch-search-read-side]], transactional and per-customer state from the database and caches); the page-dispatch helper renders the named template inside the `main` layout; template resolution walks theme templates then `_global` fallback (see [[storefront-arch-theme-inheritance]]); first request per (theme, template) compiles and is cached, later requests reuse it; the HTML returns through the edge to the browser, pulling in the theme's compiled CSS via `{styleScript}`, compiled JS via `{themeScript}`, the merchant's hosted `theme.css`, Google Fonts, the platform analytics setup script, and the merchant's Custom CSS/JS (see [[storefront-arch-css-assets]]); finally jQuery binds on `.js-*` hook classes and the page goes interactive (see [[storefront-arch-js-bundles]]).

The full inventory of routes that participate:

### Page routes (URL-bar entry)

Catalogue: `/`, `/category/{slug}`, `/categories`, `/product/{slug}`, `/products`, `/search`, `/tags/{slug}`, `/vendor/{slug}`, `/vendors`, `/selection/{slug}`, `/showcase/{slug}`, `/bundles`, `/bundles/category/{slug}`.

Cart and checkout: `/cart`, `/cart/panel`, `/checkout/*` (multi-step: authorize → shipping address → shipping → payment → return), `/checkout/return/{status}/{payment_hash}`.

Customer: `/account`, `/account/orders`, `/account/order-view/{order_id}`, `/account/wishlist`, `/account/address/*`, `/auth/login`, `/auth/register`, `/auth/forgotten`.

Static: `/page/{slug}`, `/blog`, `/blog/{filter}/{slug}`, `/article/{slug}`, `/contacts`, `/about`, `/stores`, `/store/{handle}`.

Embedded: `/embed/product/{id}` (Buy Button), `/embed/checkout`, `/checkout-link/{variant_id?}`, `/restore-abandoned/{code}/{source}/{discount_code?}`, `/tracking/{hash}`.

### AJAX endpoints (XHR-only, no direct URL-bar entry)

AJAX endpoints carry a `robots:noindex` route attribute so they don't dilute SEO.

Product listings:

- `/ajax/search`, `/ajax/category/{slug}`, `/ajax/tags/{slug}`, `/ajax/vendor/{slug}`, `/ajax/selection/{slug}`, `/ajax/showcase/{slug}`, `/ajax/bundles`, `/ajax/bundles/category/{slug}` — full-fragment listings.
- `/ajax-products/*` — products-only variant.
- `/filters-ts/*` — filter-state fragment.
- `/ajax/latest-viewed` — recently viewed products.

Cart drawer + summary:

- `/cart/compact`, `/cart/panel`, `/cart/summary`, `/cart/total-formatted` — cart drawer + cart-summary fragments.

Search and wishlist:

- `/module/search/autocomplete` — search autosuggest.
- `/wishlist/menu` — wishlist drawer.

Checkout sidebar:

- `/checkout/summary`, `/checkout/summary-totals`, `/checkout/summary-products`, `/checkout/summary-discount-code`.
- `/checkout/offices`, `/checkout/lockers`, `/checkout/offices/{machine}` — courier office / locker autocomplete.

## Related

- [[storefront-architecture]] — hub.
- [[storefront-arch-theme-inheritance]] — template resolution + `_global` fallback.
- [[storefront-arch-smarty-plugins]] — what the per-tenant template engine registers.
- [[storefront-arch-search-read-side]] — what page handlers read for catalogue pages.
- [[platform-rate-limits]] — the edge step.
- [[seo-handling]] — SEO meta tags, robots.txt, sitemap.
- [[checkout-flow]] — the checkout multi-step state machine.
- [[cart-vs-order-lifecycle]] — cart / order entity lifecycle.

## Open Questions

- **Whether the storefront request-stage order is documented as a canonical sequence** — per-route stages such as `uuid_generate`, `subscriber_uuid`, `TSStatistic`, `cart_cookie`, `XSS`, `robots`, `gdpr_policy_acceptances`, `postThrottle` are visible per-route but there's no single document listing the full sequence and what each does (verify).
- **Whether the three parallel AJAX product-listing endpoint trees** (`/ajax/*`, `/ajax-products/*`, `/filters-ts/*`) are a deprecation path or a forever-three-flavours design (verify).
- **Whether the embed routes (`/embed/*`) bypass the `main`-layout wrapping** and render bare templates (verify).
