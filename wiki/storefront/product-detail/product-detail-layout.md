---
type: storefront-page
route_name: product.view
route_path: /product/{slug}/{cart_key?}
themes_using: [all]
tags: [storefront, product, layout, gallery, sidebar, tabs, modules]
created: 2026-06-10
updated: 2026-06-10
source_count: 6
---

> Part of [[product-detail]]. See the hub for the other aspects (routing & load, the buying flow, JavaScript hooks & customisation).

# Product detail — on-page layout

## Purpose

The region-by-region breakdown of what the customer sees on the product page — the image gallery, the sidebar (title / price / SKU / stock badge / variant picker / CTA), the description-tabs region, the below-the-fold module carousels — and how each theme rearranges them. The server-side load sequence that produces this DOM is on [[product-detail-loading]]; the buying interactions on top of it are on [[product-detail-buying]].

## URL & route

This aspect covers the layout rendered at `product.view` — `/product/{slug}/{cart_key?}` — under any theme. Routing detail is on [[product-detail-loading]].

## How it loads

The controller renders `products.details` (default `flair`: the theme templates, with `details-main.tpl` for the gallery column and `details-sidebar.tpl` for the sidebar). The full conditional load sequence is on [[product-detail-loading]].

## What the customer sees

The default `flair` layout splits the page into a main column and a sidebar:

- **Breadcrumb** — Home → Category → Product.
- **Image gallery** (`_product-details-pictures-container`):
  - **Bundle products**: bundle image (if `meta.show-image` is set) + a bundle-builder block (`product/bundle/choose.tpl`) instead of variant pickers.
  - **Regular products**: thumbnail strip carousel + primary image with hover-zoom (`jqueryZoom`). 1280x1280 source. Vertical thumbnail strip with `swiper`-style breakpoints (`369 480 768 7680`).
  - **Video / 360 gallery items** mixed into the gallery when present.
- **Sidebar** (`_product-sidebar js-product-details-sidebar`):
  - Title (`<h1 class="js-product-title">`) and short description.
  - Price block (`_product-details-price product-details-price-js`): new price, old strikethrough price, "You save" line — only rendered when the platform code is on AND `showPriceForUser` allows it (B2B price-hiding plays in here — see [[product-detail-buying]]).
  - SKU line (hidden by default — `_product-details-sku variant-sku-js hide`; revealed by JS when a variant is chosen, if the platform code is on).
  - Stock-status badge (`_product-details-stock-status-bar js-status-bar`) with `data-status` ∈ {`in-stock`, `out-of-stock`, `pre-order`, `request`, `subscribe`, ...}. Hidden initially if the product has variants.
  - Meta block: rating-line, category link, vendor link, public files for download, info-page link, size-chart link.
  - Countdown timer (if `countDownDetails` is set on the product).
  - "Choose a variant first" notice (`choose-variant-msg-js hide`) — revealed by JS when the customer clicks "Add to cart" before selecting a variant.
  - **Variant picker** — one picker per Parameter attached to the product. The DOM shape of each picker is decided by the Parameter's **type** chosen in admin (`select` → dropdown, `radio` → radio buttons, `image` → image tiles, `color` → colour swatches, `2d` and `numeric_alpha` → 2D table) — see [[products-variants-types]] for the per-type mapping and the verified template (`variants_type_generate.tpl`). Uses `select2` for dropdowns and `spinnerMask` for the quantity stepper.
  - **Leasing / credit-calculator button** (if a leasing payment provider is configured for the product).
  - Wishlist heart + Compare button (when modules enabled).
  - Tags pill row.
- **Description / tabs** (below the fold, full-width):
  - `_product-details-description js-tabs` — multi-tab nav (`js-tabs-link`) over: description, every `product_tabs` row the merchant has defined for the product, tags.
  - Tab content is `js-tab` divs, only the first is visible — JS toggles them.
- **Below the tabs** (configurable modules):
  - `productInBundles` — "Available in these bundles" listing.
  - Product reviews block (`_product-review-container js-ratings-trigger`).
  - Facebook / Disqus comments (if enabled).
  - `product.linked` module — "Linked products" (manually-curated cross-sells), renderable at `variant`, `recommended`, or `section_recommended` positions.
  - `productsRelated` module — auto-related products carousel.
  - `productsCombine` — "Frequently bought together"-style block.
  - `lastViewedProducts` — recently-viewed strip (browser-cookie-driven).
- **schema.org JSON-LD** — the theme templates (currently commented out in the default `flair` template) + the theme templates — see [[seo-handling]].

## Storefront behaviour

- **Tabs are pure JS** — `js-tabs-link` anchor clicks toggle which `js-tab` div is visible; no AJAX. The hook detail is on [[product-detail-javascript]].
- **Bundle layout** — bundle products replace the variant pickers with the bundle-builder block; the buying consequences are on [[product-detail-buying]].
- **Below-the-fold modules** are independently toggleable carousels; each lazy-renders its own product tiles carrying the storefront's standard tile hooks (see [[products-list]]).

## JavaScript behaviour

The layout DOM is wired by hook classes (`.js-tabs`, `.js-carousel`, the gallery zoom binding) catalogued in full on [[product-detail-javascript]]. The price-block and SKU elements (`price-new-js`, `variant-sku-js`, etc.) are rewritten by the variant picker — see [[product-detail-buying]] for what triggers the rewrite.

## Customisations available to the merchant

The layout exposes the most module toggles of any aspect — show/hide for price, SKU, status badge, description tab, compare, wishlist, brand, category, info-page link, short description, category-properties block. Plus per-product authoring of dynamic tabs, labels / banners, the countdown, the size chart, and the linked / related / combine blocks. The full list is on [[product-detail-javascript]].

## Theme variations

- Every storefront theme has its own `products/details.tpl`, `details-main.tpl`, `details-sidebar.tpl`. The structure above is the `flair` (default) variant. Themes can:
  - Move the sidebar above the gallery (mobile-first themes).
  - Replace the tab layout with an accordion.
  - Replace the gallery's hover-zoom with a full-screen lightbox.
  - Add a sticky add-to-cart bar at the bottom of the viewport.
  - Render reviews above-the-fold or as a dedicated tab.
- The `_global/templates/product/embed/details.tpl` is used **only** for the Buy Button iframe (`/embed/product/{id}`) and is theme-agnostic.

Themes that significantly deviate (verify):
- `flair-bmw`, `flair-camerasandoptics`, `flair-clothesforyou`, `flair-diel`, `flair-electronicstore` — `flair` variants with category-specific layouts.
- `motion` — sticky sidebar with a permanent "Add to cart" footer bar.
- `one` — single-column mobile-style layout.
- `properties` — real-estate-oriented; replaces the variant picker with a "Make an enquiry" form.

## Known issues / by-design vs bug

- **Bundle products skip the variant picker** — bundles render a dedicated bundle-builder UI; the standard variant-picker logic doesn't apply. The buying flow for bundles is on [[product-detail-buying]].
- **Price block can be entirely hidden** — when the platform code is off OR `showPriceForUser` returns false (e.g. price-on-login, B2B group rules). Customers see the product, but no price or Add-to-cart, which can confuse staff who don't know about the B2B switch. See [[product-detail-buying]].
- **schema.org product microdata commented out in `flair`** — the product JSON-LD block is present but disabled in the default template; only breadcrumb microdata renders. (verify per theme.)

## Related

- [[product-detail]] — hub.
- [[storefront-architecture]] — theme inheritance and template-override conventions.
- [[products-variants-types]] — per-Parameter-type picker DOM rendered in the sidebar.
- [[variants-model]] — how the variant picker is populated.
- [[products-list]] — the product-tile hooks reused by the below-the-fold carousels.
- [[seo-handling]] — the JSON-LD microdata blocks.

## Open questions

- Whether the product JSON-LD block is enabled in any shipped theme or only via custom assets. (verify)
