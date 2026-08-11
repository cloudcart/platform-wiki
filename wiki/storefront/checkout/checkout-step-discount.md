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
updated: 2026-06-12
source_count: 3
---

> Part of [[checkout]]. Lives inside [[checkout-step-sidebar]] as the second sub-section. Discount eligibility itself is documented in [[marketing-discounts]] + sub-aspects.

# Checkout — Discount-code field

## Purpose

The text input + Apply button in the sidebar where the customer enters a coupon code. On submit, the platform tries to resolve the code as a [[marketing-discounts-codes|regular discount code]] OR as a [[marketing-discounts-code-pro|discount container code]], applies it to the cart, and refreshes all dependent surfaces. This page documents the storefront UX + the backend endpoint behaviour — for what discounts CAN apply see [[marketing-discounts]].

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
  (error: "This code is not valid") ← shown if session('discount_error') is set

Applied codes:
  ─────────────────
  SUMMER25 [×] ← shown if any discount(s) attached to cart
  WELCOME10 [×]
```

Inputs:

- **`<input name="discount_code">`** — placeholder *"Enter discount code"* (`sf.widget.cart.ph.enter_discount_code`).
- **`<button type="submit">`** — labelled *"Apply"* (`sf.widget.cart.act.discount_code_submit`), starts **disabled** + becomes enabled when the input has text.

Error display: when the previous submit attempt set `session('discount_error')`, the error string renders as `<span class="help-block-error">`. The session value is consumed on render — the error doesn't persist past one page render.

Applied-code display: when the cart has any attached discount codes, each renders as a chip with a `×` remove icon. The remove link points to `route('checkout.discount.code.remove', $discount)` and is intercepted by `data-checkout-link-ajax="true"` so the page never reloads.

## The submit pipeline (verified 2026-06-12)

Form POSTs to `checkout.discount.code` → controller `submitDiscountCode(DiscountCodeRequest $request)`:

1. **Two-step code resolution**: the platform first tries the platform code (regular discount codes — [[marketing-discounts-codes]]). If that returns a discount → `$cart->setDiscountCode($code)`. Otherwise it falls through to `$cart->setDiscountContainerCode($code)` (the [[marketing-discounts-code-pro|Code-Pro container]] path). So a single typed code can resolve via either path; the customer doesn't need to know which.
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

The remove `×` link points to `GET /checkout/remove-discount-code/{code}` (`route('checkout.discount.code.remove')`). The controller calls `$cart->removeDiscountCode($code)` and returns a parallel reload array (same scope as submit). Step machine is reset to `shippingAddress` the same way.

When the cart has multiple codes, the URL includes the specific code to remove; removing one leaves the others applied.

## Eligibility — why a code may be rejected

The actual *"is this code valid"* logic is documented across the discount cluster — see [[discounts-codes-redemption]] for redemption rules, [[discounts-eligibility]] for eligibility filters, and [[discount-stacking]] for the stacking rules when multiple discounts try to apply. From the storefront's perspective the only signal is `session('discount_error')` — a generic error string. The wiki documents the full rule catalogue; the storefront does not expose per-rule failure reasons to the customer.

## Settings & fields

There are no per-store settings for the field itself — it's always shown in the checkout sidebar (and the cart drawer). To restrict who can apply codes the merchant uses the discount's own eligibility rules.

## Business rules

- **Two-path resolution is invisible to the customer.** The customer types one code; the platform tries both code-types in order.
- **Apply ALWAYS resets the step machine.** Even if the code applies cleanly, the customer is bounced back to the shipping-address step. This is by design — shipping methods + payment options can change with the new total.
- **Errors come via session, not inline JSON.** The submit response carries the reload array but not the error text; the error is set in session and rendered on the next GET of the sub-section.
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
- [[marketing-discounts-codes]] — regular discount-code mechanism (path 1 of resolution).
- [[marketing-discounts-code-pro]] — Code-Pro container mechanism (path 2 of resolution).
- [[discounts-eligibility]] — eligibility filters.
- [[discounts-codes-redemption]] — redemption rules.
- [[discount-stacking]] — stacking rules across types.
- [[storefront-cart]] — same field renders in the cart drawer.

## Open questions

None — two-path resolution, step-reset, and reload arrays verified against the platform code + `removeDiscountCode` on 2026-06-12.
