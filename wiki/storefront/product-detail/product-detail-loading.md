---
type: storefront-page
route_name: product.view
route_path: /product/{slug}/{cart_key?}
themes_using: [all]
tags: [storefront, product, routing, middleware, embed, seo]
created: 2026-06-10
updated: 2026-06-10
source_count: 6
---

> Part of [[product-detail]]. See the hub for the other aspects (on-page layout, the buying flow, JavaScript hooks & customisation).

# Product detail — routes, embed & load sequence

## Purpose

The URL map, middleware stack, and server-side load sequence for the product detail page — plus the two routing edge cases support is most often asked about: the **301 redirect when a merchant renames a product handle** and the **404 when a product is deactivated**. This aspect also documents the `/embed/product/{id}` Buy Button variant and the cart "edit" mode that re-opens the page pre-filled with a cart line's variant. What the customer actually sees once the page loads is on [[product-detail-layout]].

## URL & route

- **Route name**: `product.view`
- **Route path**: `/product/{slug}/{cart_key?}` — the optional `cart_key` is used when the customer clicks "edit" on a cart line; it pre-fills the page with that line's selected variant + options.
- **Embed variant**: `product.embed` — `/embed/product/{id}` — renders the same product inside the Buy Button iframe (template the theme templates).
- **Middlewares**: `uuid_generate`, `subscriber_uuid`, `TSStatistic:product` (records a TimeSeries "product view" event).

## How it loads

1. Smarty bootstrap resolves the tenant (host header → site) and the theme — see [[storefront-architecture]].
2. The product controller looks up the product by URL handle from the catalogue engine.
3. If no product is found → 404 with message `sf.store.err.product_no_longer_exists`.
4. If found but `active = no` → 404 with message `store.err.product_inactive`.
5. If the slug in the URL doesn't match the product's canonical `url_handle` (e.g. the merchant changed the handle and a stale URL came in), it issues a **301 redirect to the canonical URL**.
6. Stock-per-shop data is loaded (skipped for `request` / `subscribe` status products and bundles) — populates the "Quantity per shop" tab.
7. If the BrandModel app is installed and the product has linked brand/models, a "Brand / Model" tab is appended.
8. If the Product Review app is installed and enabled, reviews + questions + ratings progress bar are rendered into the reviews block (`sf.review.tab.title`).
9. If the SizeChart app is installed and the product's category has a chart, a "Size chart" link is exposed.
10. The product is registered in the platform code so modules, SEO, and tracking can pick it up.
11. SEO meta tags are emitted via the platform code (delegates to the platform code helper) — see [[seo-handling]].
12. The view renders `products.details` — which under the default `flair` theme is the theme templates.

## What the customer sees

The load sequence above produces either a redirect / 404, or the rendered product page. The visible result of the conditional steps (which tabs appear, whether the reviews block renders) depends on which apps are installed:

- **No product / inactive product** → the storefront 404 page (see [[storefront-error-404]]).
- **Stale handle** → the browser silently follows the 301 to the canonical URL and the correct page renders.
- **Live product** → the full page, with the Quantity-per-shop, Brand/Model, Size-chart, and reviews tabs conditionally present per the installed apps. The region-by-region layout is on [[product-detail-layout]].

## Storefront behaviour

- **Canonical-URL enforcement** — the slug in the URL is always reconciled against the product's current `url_handle`; a mismatch 301s. This keeps old category links, Google Shopping feed URLs, and outbound-email links working after a handle change.
- **Cart "edit" mode** — when the customer clicks the "edit" icon on a cart line, the URL is `/product/{slug}/{cart_key}` and the page opens in a modal / panel (the platform code) instead of a full page, pre-loaded with that line's variant + options. The page header changes to `sf.cart.header.product.edit`. The buying-flow consequences of edit mode are on [[product-detail-buying]].
- **Embed mode** — `/embed/product/{id}` renders the theme-agnostic embed template for the Buy Button iframe; it carries the same buying flow but a stripped layout.
- **Recently-viewed reset** — the previous "latest viewed products" session list is cleared on each product view (`session->forget('_latest_viewed')`); the current product is added back when the `lastViewedProducts` module renders (see [[product-detail-layout]]).

## JavaScript behaviour

Loading is server-side; the only JS relevant at load time is the analytics injection (`cc-analytics`) that fires the `ViewContent` tracking event once the page renders — documented under tracking on [[product-detail-buying]]. The full hook catalogue is on [[product-detail-javascript]].

## Customisations available to the merchant

Routing / load behaviour is not directly merchant-configurable, but two adjacent settings affect it:

- A product's **URL handle** (admin → Products → edit → SEO) — changing it triggers the 301 from old URLs.
- A product's **active / inactive** toggle — deactivating sends the URL to 404.

The on-page module toggles and per-product authoring are on [[product-detail-javascript]].

## Theme variations

- The route and load sequence are theme-independent — every theme resolves `product.view` the same way and renders its own `products/details.tpl`.
- The `_global/templates/product/embed/details.tpl` is used **only** for the Buy Button iframe (`/embed/product/{id}`) and is theme-agnostic.

## Known issues / by-design vs bug

- **301 redirect on slug change** — if a merchant renames a product's URL handle, the old slug returns a 301 to the new canonical URL. Customers / bots holding the old URL are not broken. By design — see [[seo-handling]].
- **Inactive product → 404** — once a product is deactivated, the URL returns 404 (not a redirect). Customers with bookmarks lose the page. By design.
- **Quantity-per-shop tab skipped for sites 402 and 8766** — there is a hardcoded exclusion of two specific tenant IDs in the product controller (`!in_array(site('site_id'), [402, 8766])`). This is a per-tenant carve-out (verify — likely a legacy fix and should be settings-driven).
- **`_latest_viewed` session is cleared on every view** — by design, because tracking has moved to a cookie-driven mechanism; the legacy session array is no longer the source of truth for the "Recently viewed" module.

## Related

- [[product-detail]] — hub.
- [[storefront-architecture]] — request lifecycle, theme inheritance, JS-hook conventions.
- [[storefront-error-404]] — the 404 page returned for missing / inactive products.
- [[seo-handling]] — canonical URLs, the 301 on handle change, meta tags + JSON-LD.
- [[storefront-cart]] — the cart line whose "edit" icon opens this page in `cart_key` mode.

## Open questions

- The site-ID exclusion `[402, 8766]` in the quantity-per-shop branch — is this still needed, or should it be removed / made a setting? (verify)
