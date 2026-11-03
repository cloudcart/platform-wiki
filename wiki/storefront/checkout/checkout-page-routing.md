---
type: storefront-page
route_name: checkout
route_path: /checkout
themes_using: [all]
tags: [storefront, checkout, routing, middleware, plan-gate]
created: 2026-06-10
updated: 2026-06-10
source_count: 8
---

> Part of [[checkout]]. See the hub for the other aspects (steps & layout, submit & payment handoff, JavaScript hooks, merchant customisation).

# Checkout — routes, middleware & load sequence

## Purpose

The complete URL map, middleware stack, and server-side load sequence for the express checkout page. This aspect answers "what URL does each checkout step POST to?", "what guards can bounce a customer back to the cart?", and "in what order are the steps built?". The visual layout of those steps is covered in [[checkout-page-steps]]; the place-order submit is in [[checkout-page-submit]].

## URL & route

- **Entry** — `checkout` — `/checkout`.
- **Authorize step** — `checkout.authorize` — `/checkout/authorize`; with sub-routes for login (`checkout.authorize.login`), register (`checkout.authorize.register`), forgotten-password (`checkout.auth.forgotten`), email auth-code (`checkout.authorize.code`), guest (`checkout.guest`).
- **Shipping address step** — `checkout.shipping.address` — `/checkout/shipping-address` (GET render, POST save).
- **Office / locker autocomplete** — `checkout.offices`, `checkout.lockers`, `checkout.newOffices`.
- **Shipping address office quotes** — `checkout.shipping.address-quotes`, `checkout.shipping.shipping.quotes.submit` — POST per provider.
- **Billing address step** — `checkout.billing.address` — `/checkout/billing-address`.
- **Shipping method step** — `checkout.shipping.shipping` — `/checkout/shipping` (GET render, POST submit).
- **Shipping recalculation** — `checkout.shipping.recalculate` — `/checkout/shipping-recalculate` (fires when address or COD/POP-affecting payment changes — see [[checkout-page-submit]]).
- **Quotes per provider** — `checkout.shipping.quotes` — `/checkout/shipping-quotes/{provider}/{type?}`.
- **Payment step** — `checkout.payment` — `/checkout/payment` (GET render, POST submit at `checkout.payment.submit`).
- **Discount code** — `checkout.discount.code` (POST) / `checkout.discount.code.remove` (GET).
- **Sidebar fragments** — `checkout.summary`, `checkout.summary.totals`, `checkout.summary.products`, `checkout.summary.discount.code`.
- **Edge** — `checkout.unconfirmed_accounts_restrict`, `checkout.countdown_discount_popup`.
- **Return URL (post-gateway)** — `checkout.return` — `/checkout/return/{status}/{payment_hash}` — see [[checkout-return]].

**Middlewares**: the entire `/checkout/*` group is wrapped by `XSS` and `cart_checkout`. The controller additionally enforces `cart_customer` (auto-creates a guest Customer row), `checkout_steps` (state-machine validation — won't allow a customer to skip from authorize straight to payment), `unconfirmed_accounts_restrict` (if the `unconfirmed_accounts_restrict` setting is on, customers with unconfirmed emails are blocked), `gdpr_policy_acceptances` (on the address-save and payment-submit endpoints), and `site.sandbox` (on payment submit — guards against test submissions in sandbox mode).

## How it loads

1. Customer arrives at `/checkout` (typically by clicking the cart's "Continue to checkout" button).
2. Plan-gate check: if the merchant's plan doesn't include `checkout`, throws `checkout.disabled` (same gate as cart).
3. If no cart instance exists, redirect back to `/cart/{newKey}`.
4. **Cart minimum / maximum guards** — if `checkout_min_price` > 0 and subtotal < min, OR `checkout_max_price` > 0 and subtotal > max, render only a notice (`checkout_min_price.tpl`) with the threshold message. No steps render.
5. **Cart-state guards** in the constructor:
   - `max_quantity_reached` → bounce back to `/cart`.
   - `has_minimum_stock` (a cart line went below stock) → bounce back to `/cart`.
6. **Empty cart** — `products_count <= 0` → bounce back to `/cart`.
7. Persist the cart's `checkout` flag to `1` (so abandoned-cart classification knows the customer entered checkout — see [[abandoned-cart-recovery]]).
8. Build the steps array via `_getSteps` — the canonical order is:
   1. `authorize` (sign in / register / guest email)
   2. `shippingAddress` (only if cart has shippable items)
   3. `billingAddress`
   4. `shipping` (only if cart has shippable items)
   5. `payment`
9. Each step is rendered to HTML (`themes/_global/templates/checkout/steps/<step>.tpl`); steps the customer hasn't reached yet are rendered as an empty placeholder (`steps/empty/*`); the **current step** is rendered fully open.
10. Render the theme templates with the steps array. In AJAX mode, the page is rendered into a side panel (the cart drawer's "Checkout" button → opens checkout as a panel).

## What the customer sees

If a guard fired, the customer does not see the steps at all — they see one of:

- The **cart min / max notice** (`checkout_min_price.tpl`), styled `cc-box dashed error`, with the threshold message — when the subtotal is outside the `checkout_min_price` / `checkout_max_price` band.
- An immediate **redirect back to `/cart`** — when the cart is empty, a line exceeded `max_quantity_reached`, or a line fell below stock (`has_minimum_stock`).

Otherwise the full accordion renders — see [[checkout-page-steps]] for the region-by-region layout.

## Storefront behaviour

- **Cart minimum / maximum** — enforced on initial render AND in the `XSS` middleware on every checkout submit. Below-min → render the min-price notice. Above-max → render the max-price notice. Both render with the same `cc-box dashed error` styling.
- **`checkout` flag persistence** — entering this page sets the cart's `checkout` flag to `1`. This is what lets abandoned-cart classification distinguish "added to cart" from "started checkout".
- **State-machine enforcement** — the `checkout_steps` middleware re-validates the step order on every step POST; a customer cannot jump from authorize straight to payment. Each "save and continue" sets the cart's `step` attribute, re-runs `_getSteps`, and returns the updated steps HTML.
- **Office / locker typeahead** — `/checkout/offices`, `/checkout/lockers`, `/checkout/offices/{machine}` — return up to `TYPEAHEAD_LIMIT = 10` matches and (for the map view) up to `MAP_NEAREST_LIMIT = 100` markers.

## JavaScript behaviour

This aspect is server-side routing; the client-side hook classes and `cc.*` events that drive the step reloads and accordion are catalogued in [[checkout-page-javascript]]. The relevant ones for routing are the per-step containers (`.js-checkout-shipping-address`, `.js-checkout-shipping`, `.js-checkout-payment`) that the AJAX `reload` array targets after each step POST.

## Customisations available to the merchant

Routing/guard-affecting settings ([[settings-cart]] + Checkout settings):

- `checkout_min_price`, `checkout_max_price` — cart-amount gates that block the steps from rendering.
- `checkout_customer_access` — required-account / allow-guest setting (drives the authorize step's available tabs).
- `unconfirmed_accounts_restrict` — when on, customers with unconfirmed emails are blocked from checkout.

The full settings catalogue (layout, billing, maps, defaults) is on [[checkout-page-customisation]].

## Theme variations

- Routing and middleware are theme-independent — every theme hits the same `/checkout/*` routes.
- The only theme-visible routing effect: on some themes the cart's "Continue to checkout" CTA opens `/checkout` **as a side panel** (history-pushed AJAX modal); on most themes it navigates. Either way the same routes are used. See [[checkout-page-customisation]] for theme override points.

## Known issues / by-design vs bug

- **`max_quantity_reached` and `has_minimum_stock` bounce back to cart** — if a cart line becomes invalid between cart and checkout (e.g. another buyer ate the last unit), the customer is bounced back. By design.
- **Crawlers get 404** — the `cart_checkout` middleware rejects crawler requests with `noindex`. Checkout is uncrawlable.
- **`site.sandbox` middleware on payment submit** — in sandbox mode, real payment submits are blocked; only test cards work. By design.
- **Plan-gate** — sandbox / trial plans without `checkout` enabled cannot reach this page. By design.
- **Checkout opens in a side panel from `/cart`** — clicking "Continue to checkout" on the cart page can open the checkout as a slide-over panel (history-pushed). Hitting back lands on the cart. By design.

## Related

- [[checkout]] — hub.
- [[storefront-architecture]] — request lifecycle, AJAX-pipeline, middleware conventions.
- [[storefront-cart]] — the page customers come from; the guards bounce back to it.
- [[abandoned-cart-recovery]] — the `checkout` flag this page sets feeds abandoned-cart classification.
- [[shipping-calculation]] — the quotes engine behind the office/locker autocomplete and recalc routes.
- [[settings-cart]] — checkout-affecting settings.
- [[checkout-return]] — the post-gateway return URL.

## Open questions

- The `creditor` sub-flow (`creditor.select`, `creditor.consent`) is shown in routes but its UX in the express checkout is unclear from the express template alone. (verify)
