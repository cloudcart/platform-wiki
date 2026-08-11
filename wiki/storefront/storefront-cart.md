---
type: storefront-page
route_name: cart.list
route_path: /cart/{cart_key}
themes_using: [all]
tags: [storefront, cart, drawer, add-to-cart, conversion]
created: 2026-06-08
updated: 2026-06-10
source_count: 6
---

# Cart (page + drawer + header compact) — hub

## Purpose

The customer's open shopping list — the staging area between browsing and [[checkout]]. One `Cart` controller serves **three surfaces** that all render from the same `Cart` model instance and stay in sync via AJAX reloads:

1. **Cart full page** — `/cart/{cart_key}` — standalone cart page with sidebar.
2. **Cart drawer (panel)** — `/cart/panel/{cart_key}` — right-side slide-over opened on Add-to-cart or by clicking the cart icon.
3. **Cart compact (header bubble)** — `/cart/compact` — always-visible header element with item count + total + dropdown preview.

This page is large enough that it is split into a hub (this file) + three aspect pages. The Assistant should drill into the aspect that matches the question, not read every page.

## Sub-pages (in this cluster)

- [[storefront-cart-surfaces]] — the three render surfaces (full page / drawer / compact), how each loads, what the customer sees per surface, and the per-line markup; plus theme variations.
- [[storefront-cart-actions]] — every cart mutation (add / update / bulk / remove / clear / discount-code / checkout / shared-link / guest merge), the AJAX reload pipeline, and the `.js-*` hooks + `cc.*` events.
- [[storefront-cart-customisation]] — merchant-facing settings ([[settings-cart]]), per-product line behaviour, the `checkout` plan gate, and the by-design-vs-bug edge cases.

## URL & route

- **Cart full page** — `cart.list` — `/cart/{cart_key}` (`cart_key` is a 32+-char alphanumeric key — guests get a fresh one per browser; logged-in customers re-use their own).
- **Cart bare entry** — `cart.site` — `/cart` (redirects to `/cart/{cart_key}` with a freshly-issued key when the customer has no cart yet).
- **Cart drawer** — `cart.panel` — `/cart/panel/{cart_key?}` (AJAX-only).
- **Cart compact (header)** — `cart.compact` — `/cart/compact` (AJAX-only).
- **Cart actions (POST)**: `cart.add`, `cart.validate`, `cart.remove`, `cart.clear`, `cart.update`, `cart.update-product-quantity`, `cart.update-bulk`, `cart.checkout`. Full route table on [[storefront-cart-actions]].

**Plan gate**: every cart route is wrapped by a middleware that throws `checkout.disabled` if the merchant's plan doesn't include `checkout`. Crawlers receive a 404 with `X-Robots-Tag: noindex`. See [[storefront-cart-customisation]].

## How it loads

1. The bare `/cart` route redirects to `/cart/{freshKey}` so the browser holds a stable URL.
2. The cart instance resolves the current cart — for guests by the `_cart_key` cookie, for logged-in customers by their account; if both exist they are merged (see [[cart-vs-order-lifecycle]]).
3. A **shared cart link** (URL key ≠ resolved instance key) merges the linked cart and redirects to the canonical URL.
4. The Smarty template `cart.full` renders the cart HTML (full layout in non-AJAX mode, fragment only in AJAX mode).

Per-surface load detail (the `data-ajax-box` / `data-module` / `data-effect` wrappers) is on [[storefront-cart-surfaces]].

## What the customer sees

- **Full page** — breadcrumb, "Clear cart" link, product list (left), and a sticky totals sidebar (right) with subtotal, discounts, free-shipping-left message, total, and the "Continue to checkout" button.
- **Drawer** — right-side slide-over with the same line markup + a footer totals block.
- **Compact** — cart icon + bubble count + subtotal, with a hover-dropdown preview.

Full per-surface breakdown + per-line markup is on [[storefront-cart-surfaces]].

## Storefront behaviour

Cart mutations (add, update quantity, bulk update, remove, clear, add discount code, proceed to checkout, shared-link merge, guest-to-customer merge) all post to dedicated routes and re-compute totals server-side, then the AJAX pipeline reloads every `[data-module="cart"]` and `[data-module="cart-compact"]` element from its `data-ajax-box` URL. Full behaviour catalogue is on [[storefront-cart-actions]].

## JavaScript behaviour

The cart uses the storefront AJAX form-submit pipeline plus a set of `.js-*` hook classes and `cc.*` `document` events (e.g. `cc.cart.product.updated`, `cc.cart.product.removed`, `cc.cart.product.deleted`). The complete hook + event inventory is on [[storefront-cart-actions]].

## Customisations available to the merchant

Store-wide settings on [[settings-cart]] (`show_cart`, `action_after_add_to_cart`, `compact_cart_panel`, `cart_max_products`, `cart_max_quantity`, `checkout_min_price`, `checkout_max_price`), the Theme Editor "Checkout text" block, and per-product line behaviour (`allow_quantity_change`, `tracking` + `continue_selling`, bundle sub-product visibility). Full detail is on [[storefront-cart-customisation]].

## Theme variations

Most themes redefine `cart/full.tpl` and `cart/compact.tpl` but reuse the `_global` line-markup includes. The variation surface (hover-dropdown vs click-only, CTA placement, discount-field placement, empty-state carousel) is documented on [[storefront-cart-surfaces]].

## Known issues / by-design vs bug

The cart-key permanence, guest-merge semantics, drawer-vs-page summary difference, "Clear cart" event quirk, `action_after_add_to_cart=none` behaviour, crawler 404, and plan-gate hard-crash are all catalogued on [[storefront-cart-customisation]].

## Related

- [[storefront-cart-surfaces]] — surfaces, rendering, theme variations.
- [[storefront-cart-actions]] — mutations, AJAX pipeline, JS hooks + events.
- [[storefront-cart-customisation]] — settings, per-product behaviour, plan gate, known issues.
- [[storefront-architecture]] — request lifecycle, AJAX-pipeline, `data-ajax-box` / `data-module` conventions.
- [[product-detail]] — where Add-to-cart originates.
- [[checkout]] — the next step after cart.
- [[cart-vs-order-lifecycle]] — Cart entity lifecycle (active → abandoned → recovered / converted).
- [[settings-cart]] — cart-related store settings.
- [[discount-stacking]] — how line discounts + global discount + discount codes interact in line totals.
- [[abandoned-cart-recovery]] — what happens when this cart is abandoned.
- [[restore-abandoned]] — the page that brings the customer back to this cart.

## Open questions

None at the hub level — surface-, action-, and customisation-specific open questions live on the respective aspect pages.
