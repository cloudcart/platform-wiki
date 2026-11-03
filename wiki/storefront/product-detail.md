---
type: storefront-page
route_name: product.view
route_path: /product/{slug}/{cart_key?}
themes_using: [all]
tags: [storefront, product, details, add-to-cart, conversion]
created: 2026-06-08
updated: 2026-06-10
source_count: 6
---

# Product detail page

## Purpose

The customer-facing product page — the most-viewed page on every CloudCart storefront and the primary entry point into the cart. It shows the product's images, name, price (with discount badge when applicable), variant picker, "Add to cart" CTA, description / tabs, reviews, and related-product carousels. Every product URL on the storefront — whether linked from a category, search, blog article, sitemap, Google Shopping, or the merchant's own outbound email — resolves to this page.

Because the page covers several distinct concerns (server-side loading, on-page layout, the buying flow, and a large set of JavaScript hooks), the detail is split into four aspect pages. Drill into the one that matches the question rather than reading all four.

## Sub-pages (in this cluster)

- [[product-detail-loading]] — route, middleware, the server-side load sequence, 301/404 rules, the `/embed/product/{id}` Buy Button variant, and the cart "edit" mode.
- [[product-detail-layout]] — what the customer sees region-by-region (gallery, sidebar, price block, tabs, below-the-fold modules) and the per-theme variations.
- [[product-detail-buying]] — the buying flow: variant selection, Add-to-cart, stock states, the quantity stepper, "Notify me when in stock", and conversion tracking.
- [[product-detail-javascript]] — the full catalogue of `.js-*` hook classes, `cc.*` jQuery events, `data-uicontrol` bindings, and the merchant-facing module toggles / per-product authoring.

## URL & route

- **Route name**: `product.view`
- **Route path**: `/product/{slug}/{cart_key?}` (the optional `cart_key` pre-fills the page with a cart line's variant when the customer clicks "edit" on that line).
- **Embed variant**: `product.embed` — `/embed/product/{id}` — renders the same product inside the Buy Button iframe.
- **Middlewares**: `uuid_generate`, `subscriber_uuid`, `TSStatistic:product` (records a TimeSeries "product view" event).

Full route detail, middleware stack, and load sequence are on [[product-detail-loading]].

## How it loads

The product is looked up by URL handle; inactive or missing products return 404, and a stale slug 301-redirects to the canonical URL. Stock-per-shop data, brand/model and size-chart tabs, and the reviews block are conditionally appended depending on installed apps. SEO meta is emitted and the view renders `products.details`. The complete step-by-step sequence is on [[product-detail-loading]].

## What the customer sees

The default `flair` layout splits the page into a main column (image gallery) and a sidebar (title, price block, SKU line, stock badge, variant picker, CTA), with a full-width description/tabs region and below-the-fold module carousels (linked, related, frequently-bought-together, recently-viewed). The region-by-region breakdown is on [[product-detail-layout]].

## Storefront behaviour

Selecting a variant rewrites the price / SKU / stock / gallery in place; the surrounding form POSTs to `cart.add` through the AJAX pipeline and then opens the cart drawer (or redirects, per `action_after_add_to_cart`). Stock states (`in-stock`, `out-of-stock`, `pre-order`, `request`, `subscribe`) decide whether Add-to-cart, a quote request, or a "Notify me" form renders. The full buying flow is on [[product-detail-buying]].

## JavaScript behaviour

The page is driven by hook classes (`.add-to-cart-form-js`, `.js-form-submit-ajax`, `.js-status-bar`, `.js-tabs`, the price-block `*-js` elements), `cc.*` jQuery events (`cc.cart.product.updated`), and `data-uicontrol` bindings (`jqueryZoom`, `spinnerMask`, `select2`). The full verbatim catalogue is on [[product-detail-javascript]].

## Customisations available to the merchant

The `productsDetails` module exposes ~12 show/hide toggles (price, SKU, status, description, compare, wishlist, brand, category, etc.), plus globally relevant cart settings and per-product authoring (dynamic tabs, labels/banners, countdown, size chart, linked/related/combine rules, tags). The full list is on [[product-detail-javascript]].

## Theme variations

Every theme has its own `products/details.tpl`, `details-main.tpl`, `details-sidebar.tpl`; the structure above is the `flair` default. Themes can move the sidebar, switch tabs to an accordion, add a sticky add-to-cart bar, or relayout reviews. The `_global/templates/product/embed/details.tpl` is theme-agnostic and used only for the Buy Button iframe. Theme-specific deviations are catalogued on [[product-detail-layout]].

## Known issues / by-design vs bug

- **301 redirect on slug change / 404 on inactive product** — by design; detailed on [[product-detail-loading]].
- **Quantity-per-shop tab skipped for sites 402 and 8766** — hardcoded per-tenant carve-out (verify); see [[product-detail-loading]].
- **Bundle products skip the variant picker** — bundles render a dedicated bundle-builder UI; see [[product-detail-layout]].
- **Price block can be entirely hidden** — when `show_price` is off or `showPriceForUser` returns false (B2B price-on-login); see [[product-detail-buying]].

## Related

- [[storefront-architecture]] — request lifecycle, theme inheritance, JS-hook conventions.
- [[storefront-cart]] — what happens after Add-to-cart succeeds.
- [[cart-vs-order-lifecycle]] — Cart entity lifecycle.
- [[settings-cart]] — `action_after_add_to_cart`, `cart_max_products`, `cart_max_quantity`.
- [[variants-model]] — how the variant picker is populated.
- [[products-variants-types]] — per-Parameter-type picker DOM.
- [[discount-stacking]] — how the discounted price is computed.
- [[inventory-tracking]] — stock fields (`tracking`, `continue_selling`, `quantity`).
- [[inventory-in-stock-badge]] — the storefront in-stock / out-of-stock badge logic.
- [[seo-handling]] — meta tags + JSON-LD on this page.

## Open questions

- The site-ID exclusion `[402, 8766]` in the quantity-per-shop branch — still needed, or should it become a setting? (verify) — tracked on [[product-detail-loading]].
- A documented list of all `cc.*` events the product page fires (`cc.cart.product.updated` is verified; others referenced in the task brief are not visible in the default `flair` template). (verify) — tracked on [[product-detail-javascript]].
- ✅ Resolved: the up-sell modal is the **Marketing UpSell** system (the platform code), not BumpCart — see [[product-detail-buying]] + [[upsell-list-storefront-firing]].
