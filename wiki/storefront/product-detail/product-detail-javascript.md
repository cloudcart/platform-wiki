---
type: storefront-page
route_name: product.view
route_path: /product/{slug}/{cart_key?}
themes_using: [all]
tags: [storefront, product, javascript, hooks, uicontrol, customisation]
created: 2026-06-10
updated: 2026-06-10
source_count: 6
---

> Part of [[product-detail]]. See the hub for the other aspects (routing & load, on-page layout, the buying flow).

# Product detail — JavaScript hooks & customisation

## Purpose

The complete, verbatim catalogue of the JavaScript hook classes (`.js-*`), jQuery custom events (`cc.*`), and `data-uicontrol` bindings that wire up the product page — the reference a developer or support agent needs when a theme override breaks a behaviour. It also collects the merchant-facing knobs: the `productsDetails` module show/hide toggles, the globally relevant cart settings, and the per-product authoring options. The behaviours these hooks implement live on [[product-detail-buying]] and [[product-detail-layout]].

## URL & route

These hooks fire on the product page (`product.view` — `/product/{slug}/{cart_key?}`) and inside the Buy Button embed (`/embed/product/{id}`). Routing detail is on [[product-detail-loading]].

## How it loads

The hooks bind on `DOMReady` after the controller renders `products.details` (and the `details-main.tpl` / `details-sidebar.tpl` partials). The render sequence is on [[product-detail-loading]].

## What the customer sees

The hooks themselves are invisible — they drive the visible behaviours (price rewrite on variant select, the tab toggle, the gallery zoom, the quantity stepper). What the customer sees as a result is on [[product-detail-layout]] and [[product-detail-buying]].

## Storefront behaviour

The hook classes are the contract between the rendered DOM and the storefront JS bundle. A theme that renames or drops one of these classes silently disables the matching behaviour — which is why this catalogue is kept verbatim. The functional flows they implement (Add-to-cart, variant rewrite, tab toggle) are on [[product-detail-buying]] and [[product-detail-layout]].

## JavaScript behaviour

Hook classes / data attributes used by the product page (verified in the theme templates, `details-main.tpl`, `details-sidebar.tpl`):

- `.add-to-cart-form-js` — the surrounding form (legacy class name).
- `.js-form-submit-ajax` — the standard AJAX form submit handler; sends a serialised POST to the form's action and processes the JSON response (`reload`, `replaces`, `events`, `status`, `msg`).
- `.product-details-js[data-product-id]` — the wrapper element; the `data-product-id` is read by analytics and by the wishlist add button.
- `.js-product-details-container` — full-page outer wrapper.
- `.js-product-details-sidebar` — the sidebar (used for sticky-scroll behaviour).
- `.js-product-title` — title — used by JS that updates the title when the variant changes (some themes show variant-specific names).
- `.js-status-bar` — stock-status badge — JS replaces classes and `data-status` when the variant changes.
- `.js-tabs`, `.js-tabs-link`, `.js-tab` — description-tabs module.
- `.js-carousel`, `.js-carousel-container`, `.js-carousel-next`, `.js-carousel-prev` — related-products carousel.
- `.js-ratings-trigger` — anchor target for "see reviews" links (e.g. on the rating-line in the meta block).
- `.price-new-js`, `.price-old-js`, `.price-discount-js`, `.product-details-price-js` — price-block elements that the variant picker rewrites.
- `.variant-sku-js` — SKU line that the variant picker reveals.
- `.choose-variant-msg-js` — "choose a variant first" notice toggled by the variant picker.
- `[data-module="product-wishlist"]` — wishlist heart binding (handled by the wishlist module JS).
- `[data-ajax-panel]` — opens the credit-calculator / size-chart in a side panel instead of navigating.
- `[data-uicontrol="jqueryZoom"]` — primary-image zoom binding.
- `[data-uicontrol="spinnerMask"]` — quantity stepper with mask (decimals + unit suffix for grocery-style products).
- `[data-uicontrol="select2"]` — enhanced variant dropdown picker.

**jQuery custom events** (fired on `document`). Most are dispatched **server-side** — the AJAX response carries an `events` array that the storefront JS replays as `$(document).trigger(...)`; a few are fired directly in theme JS. The ones the product page touches:

- `cc.product.details.init` — fired when the product-detail module initialises (modules can hook post-init setup).
- `cc.variant.changed` — fired by the variant picker when the selected variant changes (price / SKU / gallery / stock listeners react).
- `cc.cart.product.addToCart` — the add-to-cart event, carrying the added product as JSON. Cross-sell/up-sell offers fire the namespaced variant `cc.cart.product.addToCart.disable-panel` to add without opening the cart drawer.
- `cc.cart.product.updated` — fired after the cart changes (the cart drawer + mini-cart count listen for it to refresh).
- `cc.countdown.ended` — fired when a countdown-discount timer on the page reaches zero.
- `cc.ajax.success` / `cc.ajax.reload` / `cc.ajax.error` — generic lifecycle events from the storefront AJAX form pipeline (add-to-cart goes through it). See [[storefront-arch-js-bundles]] for the full storefront `cc.*` event vocabulary.

## Customisations available to the merchant

Module-level toggles (Theme Editor → Product page module → `productsDetails`):

- `show_price` — show/hide the price block (B2B catalogue mode).
- `show_SKU` — show/hide the variant SKU line.
- `show_product_status` — show/hide the stock badge.
- `show_product_description` — show/hide the description tab.
- `show_compare` — show/hide compare button.
- `show_wishlist` — show/hide wishlist heart.
- `show_brand` — show/hide vendor link in meta block.
- `show_category` — show/hide category link in meta block.
- `show_page` — show/hide info-page link.
- `short_product_description` — show/hide short-description above the price.
- `show_categories_characteristics` — show/hide category-properties block.
- `show_link_as_popup` — open info-page in side panel.

Globally relevant settings:

- `action_after_add_to_cart` — `panel` / `redirect` / `none` ([[settings-cart]]).
- `cart_max_products` — per-variant cap (also enforced at add-to-cart time).
- `cart_max_quantity` — total-cart cap.
- `default_image_size` — image size used in galleries (not the product page directly, but used by modules).

Per-product authoring (admin → Products → edit):

- Up to N **dynamic tabs** appended after the description tab.
- **Labels** and **banners** (HTML blocks) rendered inside the sidebar.
- A **countdown** end-date that surfaces a timer in the sidebar.
- A **size chart** assigned via the SizeChart app.
- **Linked products**, **Frequently bought together**, **Related products** rules.
- **Tags** — appear as a tab and at the bottom of the sidebar.

## Theme variations

- All hook classes are theme-independent contracts; the storefront JS bundle binds them regardless of theme. A theme that omits a class disables the corresponding behaviour for that theme only.
- `[data-uicontrol]` bindings (`jqueryZoom`, `spinnerMask`, `select2`) can be swapped by a theme — e.g. a theme replacing `jqueryZoom` with a lightbox simply changes the data attribute. See [[product-detail-layout]] for the per-theme deviations.

## Known issues / by-design vs bug

- ✅ Resolved: the product-page `cc.*` events are catalogued above (`cc.product.details.init`, `cc.variant.changed`, `cc.cart.product.addToCart` [+ `.disable-panel`], `cc.cart.product.updated`, `cc.countdown.ended`, `cc.ajax.*`). Most are dispatched server-side via the AJAX response's `events` array (not hard-coded in the Smarty template), which is why they weren't visible by reading the template alone. Full storefront vocabulary on [[storefront-arch-js-bundles]].
- **Legacy class name `add-to-cart-form-js`** — the form class predates the `.js-` prefix convention; it is kept for backward compatibility with custom themes. By design.
- **`data-ajax-panel` double-purposed** — the same attribute opens both the credit-calculator and the size-chart in a side panel; the target is decided by the link's `href`, not a distinct hook. By design.

## Related

- [[product-detail]] — hub.
- [[storefront-architecture]] — the `.js-form-submit-ajax` pipeline and JS-hook conventions shared across the storefront.
- [[storefront-cart]] — listens for `cc.cart.product.updated` to refresh the drawer / mini-cart.
- [[products-variants-types]] — the per-Parameter-type picker DOM the `select2` / variant hooks bind to.
- [[settings-cart]] — `action_after_add_to_cart`, `cart_max_products`, `cart_max_quantity`.

## Open questions

- ✅ Resolved (see the jQuery custom events list + [[storefront-arch-js-bundles]]): the events are dispatched server-side through the AJAX `events` array, so grepping the template alone misses them.
