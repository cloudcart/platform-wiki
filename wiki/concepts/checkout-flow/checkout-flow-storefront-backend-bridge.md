---
type: concept
nav_path: "Concept → Checkout flow → Storefront ↔ backend bridge"
aliases: ["Checkout DOM-to-endpoint map", "Checkout AJAX pipeline", "Checkout reload semantics", "Cart attribute reload mapping", "Връзка чекаут бекенд"]
tags: [concepts, checkout, storefront, backend, ajax, reload, cart-attributes]
plan_gates: []
created: 2026-06-12
updated: 2026-06-12
source_count: 3
---

> Part of [[checkout-flow]]. This is the **bridge page** — every storefront submit on `/checkout` maps to a controller method that writes a cart attribute and returns a `reload` array. The Assistant uses this page to answer *"what does X-submit do on the server?"* and *"which fragments refresh when?"*

# Checkout flow — Storefront ↔ backend bridge

## Definition

The checkout page is rendered as a single Smarty template but **operates as a multi-step state machine** driven by AJAX. Every customer action (submit a form, click a slot, paste a code) goes through a fixed pattern:

1. **Storefront**: the form submits via `js-form-submit-ajax-new` to a route.
2. **Backend**: the controller method (the platform code in the theme templates) validates the input, writes to the **cart attribute** that step depends on (e.g. `cart.customer_shipping_address_id`, `cart.shipping_type`, `cart.payment->provider`), advances the `cart.step` to the next step, and returns a JSON response with a `reload` array.
3. **Storefront**: the response's `reload` array is forwarded to the page's reload JS — every named selector's `data-ajax-box` URL is GET-fetched and its DOM is replaced.

This page maps each storefront affordance to its (endpoint, cart attribute, reload fragment) triple.

## Scope

Covered:

- The DOM → route → cart-attribute → reload-fragment mapping for every step.
- What `js-form-submit-ajax-new` and `js-checkout-hash-reload` do at the JS level (high level).
- The structure of the JSON response shape every checkout endpoint returns.

Not covered here:

- The visual rendering of each step — see per-step pages ([[checkout-step-customer]], [[checkout-step-shipping]], [[checkout-step-shipping-address]], [[checkout-step-shipping-pickup]], [[checkout-step-shipping-method]], [[checkout-step-payment]], [[checkout-step-sidebar]], [[checkout-step-discount]]).
- The step-machine routing logic — see [[checkout-page-routing]].
- The JS hook catalogue — see [[checkout-page-javascript]].
- Place-Order submit and gateway-redirect variants — see [[checkout-page-submit]].

## Contrasts

- **Storefront state vs cart entity.** The storefront does NOT hold derived state in JS — the cart row in the DB IS the source of truth. Every reload re-renders from the cart. No optimistic UI, no client-side merge conflicts. The per-step pages document what the customer sees; the cart attribute documents what's authoritative.
- **Full-page reload vs scoped fragment reload.** CloudCart's checkout never full-page-reloads — every navigation is a scoped fragment reload via the `reload` array. Compare to a Vue SPA: there's no router on the storefront; the "current step" lives on the cart's `step` attribute, not the URL.
- **Per-sub-section sidebar routes vs one big summary route.** The sidebar's 4 sub-sections each have their own `data-ajax-box` URL, so step submits can declare granular reload arrays. Reading **only** `checkout.summary` would re-fetch all 4 every time, churning the DOM unnecessarily.
- **Discount-code submit vs all other step submits.** Apply / remove discount is the ONLY submit that resets the step machine BACKWARDS (to `shippingAddress`). Every other submit advances forward.

## The fixed JSON shape

Every checkout endpoint returns:

```json
{
  "status": "success" | "error",
  "reload": [".js-…", ".js-…", …],
  "events": ["cc.checkout.step", …],
  "step": "shippingAddress" | "shipping" | "payment" | null
}
```

- **`reload`** — list of jQuery selectors. The page's JS GETs each selector's `data-ajax-box` URL and replaces its DOM.
- **`events`** — custom events fired on `document` after reload completes. `cc.checkout.step` is the universal one — the step machine listens on it.
- **`step`** — the new active step name; the step machine opens that accordion section.

Sometimes the response also includes `replaces` (full HTML replacements when the section can't refetch itself), `cart` (a fresh cart snapshot), and `redirect` (Place-Order gateway-redirect URLs — see [[checkout-page-submit]]).

## DOM → endpoint → cart attribute → reload fragments

The verified mapping for every storefront submit (verified 2026-06-12 against the platform code + the platform code + the per-step Smarty templates):

| Storefront action | Form endpoint | Cart attribute written | Returned `reload` |
|---|---|---|---|
| Submit guest form | `POST /checkout/authorize/guest` (`checkout.guest`) | `cart.customer` (guest), `cart.step → shippingAddress` | `.js-checkout-authorize`, `.js-checkout-shipping-address`, `.js-cc-cart-panel`, summary fragments |
| Submit login form | `POST /checkout/authorize/login` (`checkout.authorize.login`) | Cart attaches to existing customer | Same as above |
| Submit register form | `POST /checkout/authorize/register` (`checkout.authorize.register.post`) | Creates customer + attaches to cart | Same as above |
| Submit email-code | `POST /checkout/authorize/code` | Cart attaches to existing customer | Same as above |
| Submit shipping-address form (any channel) | `POST /checkout/shipping-address` (`checkout.shipping.address.save`) | `cart.shipping_type`, `cart.customer_shipping_address_id` (or new address row); `cart.step → shipping` | `.js-checkout-shipping-address`, `.js-checkout-shipping`, `.js-checkout-payment`, `.js-checkout-summary-totals`, `.js-checkout-summary-products`, `.js-cc-cart-panel` |
| Change billing address | `POST /checkout/billing-address` (`checkout.billing.address.submit`) | `cart.customer_billing_address_id` | `.js-checkout-billing-address`, totals, payment (some providers re-quote on billing change) |
| Office/locker typeahead search | `GET /checkout/offices?query=…` (`checkout.offices`) / `/lockers` | (no write — read-only autocomplete) | (no reload — returns JSON list) |
| Pick shipping method | `POST /checkout/shipping` (`checkout.shipping`) | `cart.shipping_provider_key`, `cart.shipping_quote`, `cart.step → payment` | `.js-checkout-shipping`, `.js-checkout-payment`, totals |
| Pick time slot | (same as method submit — slot value travels in `checkout[shipping][{key}][delivery_date_key]`) | `cart.shipping_quote.delivery_date_key` | Same as method submit |
| Recalculate shipping on payment change | `POST /checkout/shipping-recalculate` (`checkout.shipping.recalculate`) | Re-runs shipping pipeline with new payment context | shipping + payment + totals |
| Pick payment provider | `POST /checkout/payment` (`checkout.payment`) | `cart.payment->provider`, `cart.payment->html` | `.js-checkout-payment`, totals |
| Apply discount code | `POST /checkout/discount-code` (`checkout.discount.code`) | `cart.discount_code` or `cart.discount_container_code`; `cart.step → shippingAddress` | Full set: summary + all 3 step containers + cart panel |
| Remove discount code | `GET /checkout/remove-discount-code/{code?}` (`checkout.discount.code.remove`) | Detaches code; `cart.step → shippingAddress` | Same as apply |
| Refresh summary on demand | `GET /checkout/summary` + per-section variants | (no write) | (target fragment only) |
| Place order | `POST /checkout/submit` (`checkout.submit`) | Creates `Order`; flow ends | (redirect or replaces — see [[checkout-page-submit]]) |

## Where it applies

This bridge logic applies anywhere the customer interacts with `/checkout/*` on the storefront. It does NOT apply to:

- The cart drawer / cart page ([[storefront-cart]]) — uses a similar but separate AJAX pipeline scoped to cart actions.
- Order details on the customer-account page ([[customer-orders]]) — read-only views, no submit pipeline.
- Admin order editing ([[orders-details]]) — runs through `Sitecp/the platform code`, not the storefront controller.

Within `/checkout/*`, every per-step form documented in the per-step storefront pages ([[checkout-step-customer]] through [[checkout-step-discount]]) maps to one of the controller methods catalogued below.

## Cart entity is the single source of truth

Every endpoint above writes to the same cart row (`carts` table) via the [[cart-entity-model|Cart entity model]]. The storefront does NOT hold derived state in JS — the cart row IS the state. This is why every step-submit can trigger a sidebar reload: the sidebar's `data-ajax-box` URLs re-read the same cart row and re-render. No client-side caching, no optimistic UI, no merge-conflicts.

See [[checkout-flow-cart-entity]] for the cart's attribute catalogue + state-transition rules.

## Independent reload routes per sidebar sub-section

The sidebar's 4 sub-sections each have their own GET route ([[checkout-step-sidebar]]). Why? So the step-submit endpoints can declare granular reload arrays. A payment-change response only reloads `.js-checkout-summary-totals` (not the whole `.js-checkout-summary` parent) → less DOM churn → no flicker on the products list that didn't change.

The granular routes:

- `GET /checkout/summary-products` → `.js-checkout-summary-products`
- `GET /checkout/summary-discount-code` → `.js-checkout-summary-discount-code`
- `GET /checkout/summary-totals` → `.js-checkout-summary-totals`
- `GET /checkout/summary` (parent) → `.js-checkout-summary` (all 4 sub-sections)

## Universal JS hooks

- **`js-form-submit-ajax-new`** — class on every checkout form. The bound submit handler intercepts the submit, POSTs to the form's action, and handles the JSON response (reload array + events + step).
- **`js-checkout-hash-reload`** — class on every accordion step container. Lets the URL hash (`/checkout#payment`) auto-reload that step on page load.
- **`js-checkout-summary-*`** — the four sidebar sub-section ajax-boxes.
- **`js-cc-cart-panel`** — the cart drawer (mobile slide-over + desktop cart icon dropdown). Reloaded by every checkout submit so the drawer stays in sync.

Full catalogue: [[checkout-page-javascript]].

## Where the cart's `step` attribute is used

`cart.step` (one of `authorize` / `shippingAddress` / `shipping` / `payment`) governs which accordion section is "active" on initial page render. Most submits advance the step forward; the **discount-code submit (apply + remove) is the only one that resets it backwards** to `shippingAddress` — see [[checkout-step-discount]] for why.

When the customer returns to `/checkout` after navigating away, the URL hash (or `cart.step` falls back) decides which section opens automatically. See [[checkout-page-routing]] for the routing rules.

## Related

- [[checkout-flow]] — hub.
- [[checkout-flow-cart-entity]] — the cart entity that all endpoints write to.
- [[checkout-page-routing]] — step-machine + URL hash routing.
- [[checkout-page-javascript]] — JS hook catalogue.
- [[checkout-page-submit]] — Place Order (terminal endpoint).
- [[checkout-step-customer]] / [[checkout-step-shipping]] / [[checkout-step-shipping-address]] / [[checkout-step-shipping-pickup]] / [[checkout-step-shipping-method]] / [[checkout-step-payment]] / [[checkout-step-sidebar]] / [[checkout-step-discount]] / [[checkout-step-time-slots]] — per-step pages.
- [[storefront-cart]] — the cart drawer / cart page that reloads alongside checkout.

## Open Questions

None — endpoint catalogue + cart-attribute writes + reload-array shapes verified end-to-end against the controller methods on 2026-06-12.
