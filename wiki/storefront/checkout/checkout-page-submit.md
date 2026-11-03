---
type: storefront-page
route_name: checkout.payment.submit
route_path: /checkout/payment
themes_using: [all]
tags: [storefront, checkout, payment, submit, idempotency, recalculation, discount]
created: 2026-06-10
updated: 2026-06-10
source_count: 8
---

> Part of [[checkout]]. See the hub for the other aspects (routing & middleware, steps & layout, JavaScript hooks, merchant customisation).

# Checkout — submit, recalculation & payment handoff

## Purpose

What happens when the customer interacts with the dynamic parts of checkout and finally presses **Place order**: shipping recalculation, discount-code apply/remove, the place-order validation cascade, the idempotency guard, and the per-provider payment handoff (off-site redirect vs in-page tokenize). The visual payment step is in [[checkout-page-steps]]; the page customers land on afterward is [[checkout-return]].

## URL & route

- **Shipping recalculation** — `checkout.shipping.recalculate` — `/checkout/shipping-recalculate` (POST; fires when address or COD/POP-affecting payment changes).
- **Discount code** — `checkout.discount.code` (POST) / `checkout.discount.code.remove` — `checkout.discount.code.remove/{code?}` (GET).
- **Payment render** — `checkout.payment` — `/checkout/payment` (GET).
- **Place order** — `checkout.payment.submit` — POST.
- **Return URL (post-gateway)** — `checkout.return` — `/checkout/return/{status}/{payment_hash}` — see [[checkout-return]].

These inherit the `/checkout/*` middleware stack (`XSS`, `cart_checkout`, plus `gdpr_policy_acceptances` and `site.sandbox` on submit) — see [[checkout-page-routing]].

## How it loads

The submit endpoint is a POST action, not a rendered page. The place-order flow:

1. **Idempotency guard** — duplicate submits for the same cart don't create a second order. If an in-flight order exists for this cart with an unchanged signature, the controller resumes its payment instead of inserting a new order. A genuinely changed cart yields a different signature and creates a new order.
2. Validates that shipping address + shipping are present (if shippable). If missing → set step back to authorize/shippingAddress and redirect to `/checkout`.
3. Fires the `PreOrderCreated` event.
4. Saves marketing-consent if the customer ticked it (and `hide_marketing` is off + GDPR is inactive).
5. Builds an `OrderModelPopulate` snapshot from the cart and validates it; on failure throws an `Errors` exception (returned as JSON validation messages).
6. Creates the `Order` + `OrderPayment` rows; hands off to the payment provider, which returns either:
   - **A redirect URL** to the gateway (Stripe / PayPal / Borica / etc.) → customer is sent off-site and returns via `/checkout/return/...` ([[checkout-return]]).
   - **A render-in-place payload** (Braintree Drop-in, Mokka inline form) → customer completes payment without leaving the page; the page then redirects to the success return URL.

## What the customer sees

- **Recalculated quotes** — after an address change or a COD-affecting payment choice, the shipping options refresh in place (new prices / delivery dates).
- **Updated totals** — applying or removing a discount code refreshes the side-panel totals, products, and discount-code fragments.
- **Validation messages** — a failed `OrderModelPopulate` validation returns JSON messages rendered inline in the relevant step.
- **The gateway / inline form** — on submit, the customer is either redirected off-site to the gateway, sees a popup (Mokka), or completes an inline tokenized form (Braintree Drop-in) without leaving the page.

## Storefront behaviour

- **Shipping recalculation** — when address changes, OR when a payment provider is chosen that supports recalculation, OR when the customer toggles COD vs not, the `shipping-recalculate` endpoint is POSTed. The recalc runs the omniship quotes engine ([[shipping-calculation]]) and pushes back updated quote prices/services/dates.
- **Discount code submit** — POSTs to `checkout.discount.code`. The cart-side `setDiscountCode` runs (or `setDiscountContainerCode` for container codes); response includes `reload: ['.js-checkout-summary-totals', '.js-checkout-shipping-address', '.js-checkout-shipping', '.js-checkout-payment', '.js-checkout-summary-products', '.js-checkout-summary-discount-code', '.js-cc-cart-panel']` + event `cc.checkout.step`. If the referer included `/cart/`, also reloads `[data-module="cart"], [data-module="cart-compact"]`. See [[discount-stacking]] for stacking rules.
- **Discount code remove** — `checkout.discount.code.remove/{code?}` — same reload set + event.
- **Submit payment** (Place Order) — POST `checkout.payment.submit`, running the validation + idempotency cascade above before handing off to the provider.

## JavaScript behaviour

- **`[data-shipping-recalculate="{url}"]`** — radio data attribute on payment providers that need to trigger shipping recalc when chosen.
- **`.js-checkout-payment-form`** — the place-order form; submitted via the modern AJAX pipeline (`.js-form-submit-ajax-new`, with `data-submit-loader="true"` for the spinner overlay).
- **`.js-loading`** — the submit button's built-in loading spinner.
- **Braintree dropin** — inline-tokenizing gateways load `https://js.braintreegateway.com/web/dropin/1.37.0/js/dropin.min.js` to tokenize the card without leaving the page.
- Events fired during submit/recalc: `cc.checkout.step` (every step transition + discount apply/remove), `cc.cart.product.updated` / `cc.cart.updated` (when discount/total recomputation affects the cart). The full hook + event catalogue is in [[checkout-page-javascript]].

## Customisations available to the merchant

Per-payment-provider configuration that shapes the submit/handoff:

- `payment_description` text per provider.
- `min_price`, `max_price` per provider.
- Allowed-order-amount slabs.
- Restrictions to specific shipping providers.
- Customer-details fields per provider (e.g. Mokka, Borica installments).

Per-shipping-provider configuration that drives recalc:

- Allowed payment providers (`provider->payments` relation).
- COD / POP allowance.
- Geo-zone restriction.

The full settings catalogue is on [[checkout-page-customisation]]. See [[payment-provider-mechanism]] for how each provider's handoff is constructed.

## Theme variations

- The submit flow is **theme-independent** — the place-order form (`include/form_submit.tpl`) and the recalc/discount AJAX endpoints behave identically across themes.
- Themes that rearrange `checkout/express.tpl` (sticky bar position) move the Place-order CTA visually but do not change the submit logic.

## Known issues / by-design vs bug

- **The checkout page IS the single source of truth for cart totals** — even when the cart's "cart-summary" reloads, the final total is recomputed from the cart entity at submit-time (the idempotency guard catches anyone who tries to double-submit a stale total).
- **Browser back from the payment provider** — when a customer hits "back" from Stripe Checkout, they land on `/checkout` with the cart restored. The submit may or may not be re-submittable depending on the provider's session state. The idempotency guard prevents double-charging.
- **In-flight order resume — same-cart only** — the idempotency guard only resumes payments where the cart's signature (contents + totals) matches. A customer who modifies their cart in another tab while a payment is mid-flight will produce a second order. By design.
- **The order's `email_sent` flag is set after the return-page email is sent** — emails only fire from [[checkout-return]], NOT from this submit. Direct admin-created orders that bypass the storefront need to fire emails manually.

## Related

- [[checkout]] — hub.
- [[checkout-return]] — the page customers return to after off-site payment.
- [[checkout-complete]] — the thank-you page for in-page-tokenizing gateways.
- [[payment-provider-mechanism]] — how each provider's handoff (redirect vs inline) is built.
- [[shipping-calculation]] — the omniship quotes engine behind recalculation.
- [[discount-stacking]] — discount application order on apply/remove.
- [[order-processing-pipeline]] — what happens server-side after the order is created.
- [[order-status-workflow]] — the Order state machine after creation.
- [[cart-vs-order-lifecycle]] — the Cart → Order transition this submit performs.

## Open questions

- Whether there's a documented allowlist of payment providers that support inline (no-redirect) tokenization vs the off-site-redirect majority. (verify per [[payment-provider-mechanism]])
- The `creditor` sub-flow (`creditor.select`, `creditor.consent`) is shown in routes but its submit-time UX in the express checkout is unclear from the express template alone. (verify)
