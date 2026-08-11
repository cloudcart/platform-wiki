---
type: storefront-page
route_name: cart.add
route_path: /cart/add
themes_using: [all]
tags: [storefront, cart, add-to-cart, ajax, javascript]
created: 2026-06-10
updated: 2026-06-10
source_count: 6
---

> Part of [[storefront-cart]]. See the hub for the other aspects (the three render surfaces, merchant customisation + known issues).

# Cart — actions, AJAX pipeline & JS hooks

## Purpose

Documents every **cart mutation** (add / update / bulk update / remove / clear / discount-code / proceed-to-checkout / shared-link merge / guest-to-customer merge), the AJAX reload pipeline that keeps the three surfaces in sync, and the complete `.js-*` hook + `cc.*` event inventory the cart code emits. The surfaces these mutations refresh are documented on [[storefront-cart-surfaces]].

## URL & route

The POST (and a few GET) action routes:

- `cart.add` — `/cart/add` (also `cart.add.upload` for option-file uploads).
- `cart.validate` — `/cart/validate` (pre-flight check for required option files).
- `cart.remove` — `/cart/remove/{cart_item_key?}` (GET or POST).
- `cart.clear` — `/cart/clear`.
- `cart.update` — `/cart/update`.
- `cart.update-product` — `/cart/update-product/{item_key}`.
- `cart.update-product-quantity` — `/cart/update-product-quantity/{item_key}`.
- `cart.update-bulk` — `/cart/update-bulk`.
- `cart.checkout` — `/cart/checkout` (POST — redirects to `/checkout`).
- **Discount-code link** — `cart.discount.code` — `/cart/discount:{code}`.
- **Option-file download** — `cart.file` — `/cart/file/{option_id}`.

**Middlewares** on POST cart actions: `cart_cookie` (issues / refreshes the cart-key cookie).

## How it loads

These are action endpoints, not page renders. Each POST returns a JSON response (`status`, `msg`, `events`, `reload`, `replaces`) that the AJAX form-submit pipeline consumes — it reloads every matching `[data-ajax-box]` fragment and fires the listed `document` events. The fragments being reloaded are defined on [[storefront-cart-surfaces]].

## What the customer sees

After a mutation the customer sees the updated totals and line state appear in place (no full-page reload), plus a toast notification for removes. Visual surface detail is on [[storefront-cart-surfaces]]; the mechanics of each mutation are below.

## Storefront behaviour

- **Add to cart** — POST to `cart.add`. Server validates against `cart_max_products` (per-variant cap) and `cart_max_quantity` (per-cart cap); throws translated error messages when exceeded. On success the JSON response contains `events: ['cc.cart.product.updated']`, the formatted cart total to swap into `.js-checkout-total-formatted`, and triggers the cart drawer to open per `action_after_add_to_cart` (see [[storefront-cart-customisation]]).
- **Update quantity** — POST to `cart.update` (or `cart.update-product-quantity/{item_key}`). Re-computes totals server-side; response includes `reload: ['.js-checkout-total-formatted']` and the `cc.cart.product.updated` event. The form-submit-ajax pipeline finds every `[data-module="cart"]` and `[data-module="cart-compact"]` element and reloads them from their `data-ajax-box` URLs — so updating the drawer quantity also updates the full-page total and the header bubble in one round-trip.
- **Bulk update** — POST to `cart.update-bulk` with `cart[variants][{key}] = qty`. Used when the customer changes several quantities and clicks "Update" once. Runs in a transaction so partial errors roll back.
- **Remove a line** — GET or POST to `cart.remove/{cart_item_key}`. Returns a toast-style notification (`data-ajax="toast"`) and refires the cart-module reload.
- **Clear cart** — `cart.clear`. Deletes all items on the cart row. Fires `cc.cart.product.removed` AND `cc.cart.product.deleted` events on `document` (note: NOT `cc.cart.product.updated` — see [[storefront-cart-customisation]]).
- **Add discount code** — GET `cart.discount.code/{code}`. Looks the code up; if it's a regular discount → applied as the discount; otherwise → treated as a "discount container code". Customer is redirected to `/checkout` (or home if the cart is empty) with a translated "discount accepted" flash. See [[discount-stacking]].
- **Proceed to checkout** — the `cartForm` form action is `cart.checkout` (POST) which simply redirects to `/checkout`.
- **Shared cart link** — visiting `/cart/{key}` with a key that doesn't match the resolved cart merges that cart into the current session. This is the mechanism behind "share your cart" links and email/CRM-generated cart links that aren't `restore-abandoned/`.
- **Customer association** — guests have a cookie-bound cart key; the moment a guest logs in or registers, their guest cart is **merged** into their stored customer cart (see [[cart-vs-order-lifecycle]] for merge semantics).

## JavaScript behaviour

Hook classes / data attributes used (verified in `_global/templates/cart/include/*.tpl` and `flair/templates/cart/*.tpl`):

- `.cart-form-js`, `.js-form-submit-ajax` — the AJAX form-submit pipeline. Posts the form, parses the JSON response (`status`, `msg`, `events`, `reload`, `replaces`), reloads matching `[data-ajax-box]` elements, fires `document` events.
- `.js-cart-clear` — "Clear cart" link binding; sends to `cart.clear` and reloads cart modules.
- `.js-cart-product-remove` — per-line remove link; `data-ajax="toast"` means the response message is shown as a toast.
- `.js-cart-product-{key}` — class on each line in the panel template, used for targeted line replacement.
- `.js-checkout-total-formatted` — span containing the formatted subtotal; included in the standard reload list after every cart mutation.
- `.js-checkout-hash-reload` — marker class meaning "reload me when the URL hash changes".

(Surface-targeting attributes — `[data-ajax-box]`, `[data-module]`, `[data-effect]`, `[data-ajax-panel]`, the spinner controls — are catalogued on [[storefront-cart-surfaces]].)

Custom `cc.*` events fired by cart code (verified in the cart controller + cart templates):

- `cc.cart.product.updated` — fires after add or update.
- `cc.cart.product.removed`, `cc.cart.product.deleted` — fire after remove / clear.
- `cc.cart.updated` — fires after a cart-rule modification re-applies.
- `cc.cart.open.checkout` — fires when the "Continue to checkout" path is triggered.

## Customisations available to the merchant

Mutations are gated/shaped by a few settings (full detail on [[storefront-cart-customisation]]):

- `cart_max_products` — per-variant quantity cap enforced by `cart.add`.
- `cart_max_quantity` — per-cart total quantity cap enforced by `cart.add`.
- `checkout_min_price` / `checkout_max_price` — bounds the "Proceed to checkout" path.
- `action_after_add_to_cart` — what the UI does after a successful `cart.add`.

## Theme variations

- The action endpoints are identical across themes; only the markup that posts to them varies. Themes differ in whether the discount-code field posts from the cart page or only from checkout, and in where the "Continue to checkout" CTA that triggers `cart.checkout` sits — see [[storefront-cart-surfaces]] for the theme-variation surface.

## Known issues / by-design vs bug

- **"Clear cart" doesn't fire `cc.cart.product.updated`** — it fires `removed` and `deleted` instead. Listeners that only bind to `updated` will miss clear events. (Catalogued with the other event quirks on [[storefront-cart-customisation]].)
- **`action_after_add_to_cart=none` still fires the cart-updated event and reloads the cart module** — the visual drawer just doesn't open. By design.

## Related

- [[storefront-cart]] — hub.
- [[storefront-cart-surfaces]] — the fragments these mutations reload.
- [[storefront-architecture]] — the AJAX form-submit pipeline + `data-ajax-box` reload mechanics.
- [[cart-vs-order-lifecycle]] — guest-to-customer cart merge semantics.
- [[discount-stacking]] — how line discounts + global discount + discount codes interact in line totals.
- [[checkout]] — where `cart.checkout` lands.

## Open questions

- The exhaustive list of `cc.*` events fired by cart JS isn't easy to enumerate purely from the templates — the per-theme JS bundle is the source of truth. (verify)
- Is there a documented limit on how many concurrent cart-item rows a single cart can hold? A `CART_LIMIT = 50` constant is defined but its usage chain isn't traced here. (verify)
- Whether the `/cart/discount:{code}` short-link mechanism is a merchant-facing feature or only used by marketing-email templates. (verify)
