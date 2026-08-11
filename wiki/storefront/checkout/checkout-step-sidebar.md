---
type: storefront-page
nav_path: "Storefront → Checkout → Sidebar (order summary)"
route_name: checkout.summary
route_path: /checkout/summary
themes_using: [all]
aliases: ["Checkout sidebar", "Order summary panel", "Right-column checkout", "Checkout slide-over (mobile)", "checkoutText", "checkoutSideText", "Десен панел чекаут"]
tags: [storefront, checkout, sidebar, summary, totals, app-injection]
plan_gates: []
created: 2026-06-12
updated: 2026-06-12
source_count: 4
---

> Part of [[checkout]]. The summary is the live mirror of the cart while the customer fills in the left-column steps; see [[checkout-step-shipping-method]] and [[checkout-step-payment]] for the steps that change totals.

# Checkout — Sidebar (order summary)

## Purpose

The desktop right-column / mobile slide-over panel on `/checkout`. It mirrors the cart state in real time as the customer progresses: products list, applied discount, totals breakdown, error/info messages, plus optional merchant-customisable text blocks. **Every step submit on the left reloads relevant sub-sections of this panel** so totals never go stale.

## URL & route

See `route_name` and `route_path` in frontmatter. This is a sub-section of [[checkout]] — the parent `/checkout` page hosts these step containers; container reload routes are listed under "Where to find it".

## How it loads

Loaded as a sub-region of the `/checkout` page (see [[checkout-page-routing]] for the parent route + middleware stack). On step transitions, the container is GET-reloaded via its `data-ajax-box` URL — see [[checkout-flow-storefront-backend-bridge]] for the full reload-fragment map.

## Where to find it

- **Desktop**: fixed right column — `<div class="cc-checkout-sidebar js-checkout-sidebar-toggle">`.
- **Mobile**: slide-over toggled by the *"Cart details"* button at the top — same DOM, CSS handles the layout switch.
- Route: `/checkout/summary` (`route('checkout.summary')`) — reloadable as `data-ajax-box`.

## What the customer sees — 4 fixed sub-sections + 0-N modules

The sidebar is composed in the theme templates, which inclues 4 fixed sub-templates in this fixed order:

| Sub-section | Sub-template | DOM hook | Independent reload route |
|---|---|---|---|
| 1. Products list | `include/summary/products.tpl` | `.js-checkout-summary-products` | `checkout.summary.products` |
| 2. Discount-code field + applied codes | `include/summary/discount_code.tpl` | `.js-checkout-summary-discount-code` | `checkout.summary.discount.code` |
| 3. Totals breakdown | `include/summary/totals.tpl` | `.js-checkout-summary-totals` | `checkout.summary.totals` |
| 4. Messages (errors, info) | `include/summary/messages.tpl` | (no separate route) | reloaded with parent `checkout.summary` |

Plus 2 optional **custom text blocks** rendered AFTER the summary include, in the parent wrapper (`express.tpl`):

| Block | When shown |
|---|---|
| `checkoutText` widget | When the merchant has enabled the `checkoutText` widget — see [[design-modules]]. |
| `checkoutSideText` widget | When the merchant has enabled the `checkoutSideText` widget — separate slot configurable in the Theme Editor side-text section. |

Plus an **app-injection** affordance for the `bumper_offer` app (currently commented out in `express.tpl` but documented in code) — bumper-products appear in the sidebar on the cart page; in checkout it surfaces only inside the per-step accordions.

Plus a **BGN-to-EUR conversion message** placeholder (`<div class="bgn2eur-convertion-message-checkout">`) injected by the [[apps-bgn2eur]] app during the BG-to-EUR transition (currently hidden by default).

## How sub-sections reload

The reload pattern is reverse: instead of the sidebar polling for changes, **every step submit returns a `reload` array** the left-column JS forwards into the sidebar's per-section ajax-boxes. Example from the discount-code submit (the platform code, verified 2026-06-12):

```
reload = [
  '.js-checkout-summary-totals',
  '.js-checkout-shipping-address',
  '.js-checkout-shipping',
  '.js-checkout-payment',
  '.js-checkout-summary-products',
  '.js-checkout-summary-discount-code',
  '.js-cc-cart-panel',
]
```

So picking a coupon refreshes: the products list (some may be free now), totals, all 3 downstream step containers, and the cart drawer. Each container fetches its own `data-ajax-box` route fresh. The same pattern is used by every step submit + every cart action.

For the full DOM → POST → reload-fragment map of the whole flow see [[checkout-flow-storefront-backend-bridge]].

## Settings & fields

| Setting | Effect |
|---|---|
| `cc_cart->getDiscountCodeNew` returning a code | Renders the "Applied code" row with a remove × link. |
| `session('discount_error')` | Error message rendered under the discount-code input. |
| `checkoutText` widget enabled | Custom HTML block appears below the totals. |
| `checkoutSideText` widget enabled | Same — separate slot. |
| [[apps-bgn2eur]] active | Conversion message overlay appears. |

## App-injection points — what apps CAN show content here

Verified locations where third-party / first-party apps can inject content in the sidebar (or the parent wrapper that contains it):

| App | Mechanism |
|---|---|
| Custom text widgets `checkoutText` + `checkoutSideText` | Two named widget slots merchants can fill via Theme Editor / [[design-modules]]. |
| **BGN-to-EUR** | Pre-positioned `<div class="bgn2eur-convertion-message-checkout">` placeholder filled by the app's JS. |
| **Cart Rules** ([[apps-cart-rules]]) | Surfaces effect lines inside the totals (e.g. *"BGN 5 discount: Buy 2 get 1"*) via the cart's `messages` collection. |
| **Marketing discounts** | Same path — surfaces inside the messages block and the discount-code applied list. |
| **Cross-sell / Up-sell modules** ([[marketing-cross-sell-list]] / [[marketing-up-sell-list]]) | Render inside step accordions on the left, NOT in the sidebar — they need product-list context the sidebar doesn't expose. |

There is **no generic plugin/extension API** for arbitrary apps to inject DOM into the sidebar. New surfaces require a CloudCart-staff template change.

## Business rules

- **The sidebar is a child of the step machine.** It doesn't drive the cart state — it reflects it. Every change happens on the left; the sidebar refreshes.
- **Reloads are scoped, not full-page.** The `reload` array names specific containers — never a full-page reload — so the customer never loses focus.
- **The discount-code submit ALSO advances the step machine.** Submitting a discount code resets the step to `shippingAddress` (so the customer re-confirms the address with the new total). See `submitDiscountCode` in [[checkout-step-discount]].
- **Mobile slide-over uses the same DOM.** No separate mobile template; CSS classes + the `js-checkout-sidebar-toggle` mechanism handle the layout switch.
- **The "Cart details" toggle button is hidden on desktop** (`hidden-lg` class). On mobile it shows a summary chip (item count + total) and toggles the panel.

## Storefront behaviour

See [[checkout-flow-storefront-backend-bridge]] for the DOM → endpoint → cart-attribute → reload-fragment full map. This section's specific form/click handlers + reload arrays are documented inline in the sections above.

## JavaScript behaviour

The container uses the universal checkout JS hooks — `.js-form-submit-ajax-new` (intercepts form submit, processes JSON response), `.js-checkout-hash-reload` (URL hash → auto-reload on page entry), `cc.checkout.step` event. Full catalogue: [[checkout-page-javascript]].

## Customisations available to the merchant

Merchant-controlled settings affecting this section are listed under "Settings & fields" above. Full theme-wide customisation catalogue: [[checkout-page-customisation]].

## Theme variations

The template is shared from the theme templates — every theme inherits the same DOM. Themes can override individual sub-templates for per-theme tweaks, but the structure documented here applies to the default `flair` theme and every variant unless explicitly overridden.

## Known issues / by-design vs bug

None recorded for this section. Any merchant-facing surprises specific to this step are noted inline in the sections above (Business rules / Open questions).

## Related

- [[checkout]] — hub.
- [[checkout-step-discount]] — discount-code field documented in detail.
- [[checkout-step-payment]] / [[checkout-step-shipping-method]] — left-column steps that drive sidebar reloads.
- [[checkout-flow-storefront-backend-bridge]] — full DOM → endpoint → reload map.
- [[checkout-page-javascript]] — the AJAX-form + reload JS pipeline.
- [[checkout-page-customisation]] — `checkoutText` / `checkoutSideText` widget configuration.
- [[design-modules]] — widget catalogue including the two checkout text slots.
- [[apps-bgn2eur]] — BGN-to-EUR conversion overlay.
- [[apps-cart-rules]] — Cart Rules messages surface here.
- [[storefront-cart]] — sibling cart page; same `summary.tpl` is used in the cart drawer.

## Open questions

None — sidebar composition, reload semantics, and app-injection points verified against `express.tpl` + `summary.tpl` + the platform code reload arrays on 2026-06-12.
