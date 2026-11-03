---
type: storefront-page
route_name: product.view
route_path: /product/{slug}/{cart_key?}
themes_using: [all]
tags: [storefront, product, add-to-cart, stock, conversion, tracking]
created: 2026-06-10
updated: 2026-06-10
source_count: 6
---

> Part of [[product-detail]]. See the hub for the other aspects (routing & load, on-page layout, JavaScript hooks & customisation).

# Product detail — the buying flow

## Purpose

Everything that happens between "customer picks a variant" and "product is in the cart": variant selection rewriting the price / SKU / stock, the Add-to-cart form and its post-submit behaviour, the five stock states and the CTAs each one renders, the quantity stepper and its caps, the "Notify me when in stock" flow, and the conversion-tracking events that fire on view and add. The DOM these interactions touch is described on [[product-detail-layout]]; the underlying hook classes are catalogued on [[product-detail-javascript]].

## URL & route

The buying flow runs on the product page (`product.view` — `/product/{slug}/{cart_key?}`) and posts to `cart.add` (`/cart/add`). In cart "edit" mode the page is opened with a `cart_key` and the submit updates the existing line instead of adding a new one — see [[product-detail-loading]].

## How it loads

Stock state is computed server-side at load and stamped onto the status badge (`js-status-bar` `data-status`); for products with variants the badge is hidden until the customer picks a variant, then JS fills it in. The load sequence is on [[product-detail-loading]].

## What the customer sees

What renders in place of (or alongside) the Add-to-cart button depends on the computed stock state:

- **in-stock** — green badge, Add-to-cart enabled.
- **out-of-stock** — Add-to-cart button is **hidden** (replaced by a "Notify me when in stock" subscribe button if the `request_subscribe` flow is configured).
- **pre-order** — its own CTA.
- **request** — a "request a quote" CTA.
- **subscribe** — a subscribe-to-availability CTA.

A "Choose a variant first" notice appears if the customer clicks Add-to-cart before identifying a unique variant.

## Storefront behaviour

- **Variant selection** — the variant picker dispatches per-parameter changes that the variant-picker module hooks. As soon as a unique variant is identified, the JS pushes the matching variant's `price`, `SKU`, stock state and gallery main image into the existing DOM (`price-new-js`, `price-old-js`, `price-discount-js`, `variant-sku-js`, `js-status-bar`).
- **Add to cart** — the entire sidebar + main is wrapped in a `<form class="add-to-cart-form-js js-form-submit-ajax" action="{route('cart.add')}" method="POST">`. Submitting goes through the AJAX form-submit pipeline (see [[storefront-architecture]]) which POSTs to `cart.add` (`/cart/add`), and on success:
  - Fires `cc.cart.product.updated` on `document`.
  - Opens the cart drawer ([[storefront-cart]]) — controlled by the `action_after_add_to_cart` setting ([[settings-cart]]): `panel` (drawer), `redirect` (jump to `/cart`), or `none` (silent).
  - If a cross-sell rule fires (a Cross-Sell with the `add_to_cart` trigger event — see [[cross-sell-trigger-events]]), the cross-sell modal opens (the platform code, route `site.crossSell.view`).
  - If an up-sell rule fires, the up-sell modal opens (the platform code, route `site.upSell.*`) — this is the **Marketing UpSell** system ([[marketing-up-sell-list]]), distinct from the [[apps-bumpcart|BumpCart]] checkout-bump app.
- **Stock states**:
  - `in-stock` — green badge, Add-to-cart enabled.
  - `out-of-stock` — when `tracking=yes` AND `continue_selling=no` AND `quantity=0`; Add-to-cart button is **hidden** (replaced by "Notify me when in stock" if `request_subscribe` is configured).
  - `pre-order`, `request`, `subscribe` — render their own CTAs (request quote, subscribe to availability).
  - `continue_selling=yes` overrides 0-quantity → Add-to-cart stays enabled. See [[inventory-oversell]].
  - The full storefront badge logic (including `minimum` order-quantity blocking sellability at positive stock) is on [[inventory-in-stock-badge]].
- **Quantity stepper** — `spinnerMask` uicontrol; cap is `product_quantity_unit` when stock-tracked. When the `store_locations` app is installed and a `store_location` cookie is set, the cap is the sum of quantities at the cookie's selected shops.
- **"Edit" mode from cart** — when opened with a `cart_key` (see [[product-detail-loading]]), the submit updates that cart line's variant + options instead of adding a new line.
- **"Notify me when in stock"** — when the product's status is `request` or `subscribe`, a subscribe form appears in place of Add-to-cart and posts to the request-subscribe endpoint.
- **Tracking** — when the page loads, a `ViewContent` Facebook Pixel event fires (and equivalents on Google Analytics / Pinterest / TikTok), driven by `cc-analytics` injected into the head. The Add-to-cart success additionally feeds the cart-update tracking.

## JavaScript behaviour

The buying flow is driven by `.add-to-cart-form-js` / `.js-form-submit-ajax` (the form + AJAX submit), the price-block `*-js` rewrite targets, `.variant-sku-js`, `.choose-variant-msg-js`, `.js-status-bar`, and the `spinnerMask` / `select2` uicontrols. The `cc.cart.product.updated` event fires on success. The full verbatim catalogue is on [[product-detail-javascript]].

## Customisations available to the merchant

Settings that change the buying flow:

- `action_after_add_to_cart` — `panel` / `redirect` / `none` ([[settings-cart]]).
- `cart_max_products` — per-variant cap (also enforced at add-to-cart time).
- `cart_max_quantity` — total-cart cap.
- `show_price` (productsDetails module) — when off, no price and no Add-to-cart render (B2B catalogue mode).
- Per-product `tracking` / `continue_selling` / status (`request` / `subscribe`) — decide which CTA renders. See [[inventory-variant-model]].

The complete module-toggle list and per-product authoring options are on [[product-detail-javascript]].

## Theme variations

- The buying flow is functionally identical across themes — same `cart.add` POST, same stock-state logic.
- Theme-visible differences: `motion` keeps a permanent "Add to cart" footer bar; `properties` replaces the whole flow with a "Make an enquiry" form; some themes redirect to `/cart` rather than opening the drawer (driven by `action_after_add_to_cart`, not the theme). See [[product-detail-layout]] for the theme catalogue.

## Known issues / by-design vs bug

- **Price block can be entirely hidden** — when the platform code is off OR `showPriceForUser` returns false (e.g. price-on-login, B2B group rules). Customers see the product but no price or Add-to-cart, which can confuse staff who don't know about the B2B switch.
- **`continue_selling=yes` keeps Add-to-cart enabled at zero stock** — by design; the product is sellable as a backorder. Stock clamps at 0 and never goes negative — see [[inventory-oversell]].
- **Two customers can race for the last unit** — under `paid`-timing decrement, stock is not reserved at add-to-cart, so simultaneous buyers can both add the last unit; the loser is caught at order time. See [[inventory-decrement-timing]].

## Related

- [[product-detail]] — hub.
- [[storefront-architecture]] — the AJAX form-submit pipeline behind Add-to-cart.
- [[storefront-cart]] — the drawer that opens after Add-to-cart succeeds.
- [[settings-cart]] — `action_after_add_to_cart`, `cart_max_products`, `cart_max_quantity`.
- [[discount-stacking]] — how the discounted price shown in the price block is computed.
- [[inventory-in-stock-badge]] — the storefront stock-badge logic + `minimum` order quantity.
- [[inventory-oversell]] — `continue_selling` and clamping at zero.
- [[inventory-decrement-timing]] — when a sold unit actually leaves stock.
- [[inventory-variant-model]] — `tracking` / `continue_selling` master switches.

## Open questions

- ✅ Resolved: the up-sell modal is driven by the **Marketing UpSell** system (the platform code, [[marketing-up-sell-list]]) — an UpSell offer firing on its configured trigger event, gated by the in-stock + not-already-in-cart checks on [[upsell-list-storefront-firing]]. It is **not** BumpCart (a separate checkout-bump app) nor a generic "Bumper Offer".
