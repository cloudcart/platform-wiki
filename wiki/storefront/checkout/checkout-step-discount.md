---
type: storefront-page
nav_path: "Storefront → Checkout → Discount code field"
route_name: checkout.discount.code
route_path: /checkout/discount-code
themes_using: [all]
aliases: ["Checkout discount code", "Apply coupon", "Coupon field checkout", "Discount-code error", "Remove discount code", "Промокод чекаут", "Купон код"]
tags: [storefront, checkout, sidebar, discount, coupon]
plan_gates: []
created: 2026-06-12
updated: 2026-11-04
source_count: 3
---

> Part of [[checkout]]. Lives inside [[checkout-step-sidebar]] as the second sub-section. Discount eligibility itself is documented in [[marketing-discounts]] + sub-aspects.

# Checkout — Discount-code field

## Purpose

The text input + Apply button in the sidebar where the customer enters a coupon code. On submit, the platform tries to resolve the code first as a single discount code or a [[marketing-discounts-code-pro|Code PRO code]], then as a [[marketing-discounts-codes|Container code]], applies it to the cart, and refreshes all dependent surfaces. This page documents the storefront UX + the backend endpoint behaviour — for what discounts CAN apply see [[marketing-discounts]].

## URL & route

See `route_name` and `route_path` in frontmatter. This is a sub-section of [[checkout]] — the parent `/checkout` page hosts these step containers; container reload routes are listed under "Where to find it".

## How it loads

Loaded as a sub-region of the `/checkout` page (see [[checkout-page-routing]] for the parent route + middleware stack). On step transitions, the container is GET-reloaded via its `data-ajax-box` URL — see [[checkout-flow-storefront-backend-bridge]] for the full reload-fragment map.

## Where to find it

Sidebar / right column on `/checkout`, between the products list and the totals breakdown — see [[checkout-step-sidebar]]. DOM: `<div class="js-checkout-summary-discount-code" data-ajax-box="{route('checkout.summary.discount.code')}">`.

## What the customer sees

A single-row form:

```
┌──────────────────────────────────────────┐
│ [ Enter discount code… ] [Apply] │
└──────────────────────────────────────────┘
  (error: "Invalid discount code") ← the reason the last attempt was refused

Applied codes:
  ─────────────────
  SUMMER25 [×] ← one promo code, or several Container codes
```

Inputs:

- **`<input name="discount_code">`** — placeholder *"Enter discount code"* (`sf.widget.cart.ph.enter_discount_code`).
- **`<button type="submit">`** — labelled *"Apply"* (`sf.widget.cart.act.discount_code_submit`), starts **disabled** + becomes enabled when the input has text.

Error display: a refused code comes back with its reason in the submit response, shown against the code field.

Applied-code display: the promo code, or each Container code, renders as a chip with a `×` remove icon. The remove link points to `checkout.discount.code.remove` (with the code, for a Container code) and is intercepted by `data-checkout-link-ajax="true"` so the page never reloads.

## The submit pipeline (verified 2026-06-12)

Form POSTs to `checkout.discount.code`:

1. **Two-step code resolution**: the platform first looks for a single discount code or a [[marketing-discounts-code-pro|Code PRO code]]. If one is found, it goes into the cart's one promo-code slot, replacing any code there. Otherwise the code is added to the cart's Container codes ([[marketing-discounts-codes]]), which clears the promo-code slot. So a single typed code can resolve via either path; the customer doesn't need to know which.
2. **Step machine reset** — if the customer is past the `authorize` step, the step is reset to `shippingAddress` (so the customer re-confirms the address with the new total + re-quotes shipping).
3. **Wide reload array** — returns:
   ```
   ['.js-checkout-summary-totals',
    '.js-checkout-shipping-address',
    '.js-checkout-shipping',
    '.js-checkout-payment',
    '.js-checkout-summary-products',
    '.js-checkout-summary-discount-code',
    '.js-cc-cart-panel']
   ```
   So one Apply click refreshes the products list (some may now be free), totals, all 3 downstream step containers, the discount-code subsection itself (to show the applied chip), and the cart drawer.
4. **`cc.checkout.step` event fires** so the JS step machine knows it was advanced backwards.

## Removing a code

The remove `×` link points to `GET /checkout/remove-discount-code/{code}` (`checkout.discount.code.remove`). It returns a parallel reload array (same scope as submit). Step machine is reset to `shippingAddress` the same way.

Several codes can sit together only as Container codes: the URL includes the specific code to remove, and removing one leaves the others applied. Removing the promo code clears the slot.

## Eligibility — why a code may be rejected

The actual *"is this code valid"* logic is documented across the discount cluster — see [[discounts-codes-redemption]] for redemption rules, [[discounts-eligibility]] for eligibility filters, and [[discount-stacking]] for the stacking rules when multiple discounts try to apply. The customer sees the specific reason: *"The code is valid only for registered users"*, *"You have used this discount code the maximum number of times"*, *"The discount could not be applied because the minimum total price of the products has not been reached."*, *"This discount code can not be applied because you already have a discounted products at your cart"* or *"Invalid discount code"*.

## Settings & fields

There are no per-store settings for the field itself — it's always shown in the checkout sidebar (and the cart drawer). To restrict who can apply codes the merchant uses the discount's own eligibility rules.

## Business rules

- **Two-path resolution is invisible to the customer.** The customer types one code; the platform tries both code-types in order.
- **Apply resets the step machine past the first step.** Even if the code applies cleanly, a customer past the `authorize` step is returned to the shipping-address step. This is by design — shipping methods + payment options can change with the new total.
- **Errors come in the submit response.** A refused code returns the reason for the code field instead of the reload array.
- **No client-side validation.** The customer can submit any string; the validation is fully server-side.
- **Removal is also a step-reset.** Removing a code re-runs every dependent quote — shipping prices, payment availability, totals.
- **Discount-code field is also in the cart drawer** ([[storefront-cart]]). The sub-template (`discount_code.tpl`) is shared between cart and checkout — exact same behaviour on both surfaces.

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

- [[checkout-step-sidebar]] — parent surface.
- [[checkout-page-routing]] — step machine that the submit resets.
- [[marketing-discounts]] — discount hub.
- [[marketing-discounts-code-pro]] — Code PRO codes (path 1 of resolution, with single discount codes).
- [[marketing-discounts-codes]] — Container codes (path 2 of resolution).
- [[discounts-eligibility]] — eligibility filters.
- [[discounts-codes-redemption]] — redemption rules.
- [[discount-stacking]] — stacking rules across types.
- [[storefront-cart]] — same field renders in the cart drawer.

## Open questions

None.
