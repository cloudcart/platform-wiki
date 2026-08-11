---
type: storefront-page
route_name: checkout
route_path: /checkout
themes_using: [all]
tags: [storefront, checkout, accordion, address, shipping, payment, summary]
created: 2026-06-10
updated: 2026-06-10
source_count: 8
---

> Part of [[checkout]]. See the hub for the other aspects (routing & middleware, submit & payment handoff, JavaScript hooks, merchant customisation).

# Checkout — steps, layout & what the customer sees

## Purpose

The region-by-region layout of the express (single-page accordion) checkout: the stacked steps, the order-summary side panel, and the consent / notes / CTA elements — what's on the screen and what each box does. The routes the steps POST to are in [[checkout-page-routing]]; the place-order action is in [[checkout-page-submit]].

## URL & route

All regions are served from route `checkout` at `/checkout`. Step fragments and shared includes are themeable (see Theme variations). The per-step render/save routes are catalogued in [[checkout-page-routing]].

## How it loads

The steps sequence is built server-side (see [[checkout-page-routing]]). Each step renders into one accordion section; the current step renders fully open, future steps render as empty placeholders. This aspect describes the rendered result the customer interacts with.

## What the customer sees — at a glance

The checkout is a **single-column page** of stacked accordion steps on the left + a fixed **sidebar** on the right (slide-over on mobile). Page-level regions:

- **Mobile header** — store logo + cart-details toggle button.
- **Free-shipping progress bar** — "X left to free shipping" hint when applicable; suppressed when the Bumper Offer app's goal is free-shipping.
- **Payment-cancelled flash** — error banner when the customer just returned from a cancelled payment gateway (`payment_canceled` session message).
- **Steps stack** (`js-checkout-container`) — accordion sections, one active at a time.
- **Sidebar** (`js-checkout-sidebar`) — order summary + discount-code + totals + messages, plus optional custom text widgets.

Each step has its own aspect page with the full per-template, per-field, per-endpoint detail:

| Step | Aspect page | What's documented |
|---|---|---|
| 1. Customer (authorize) | [[checkout-step-customer]] | guest / login / register / email-code tabs; `allowed_tabs` priority |
| 2. Shipping (channel picker) | [[checkout-step-shipping]] | address / office / locker / marketplace radio |
| 2a. Shipping → To address | [[checkout-step-shipping-address]] | saved-address list vs inline form; Google Maps gating; field catalogue |
| 2b. Shipping → To office / locker | [[checkout-step-shipping-pickup]] | typeahead + Google-Maps-vs-no-Maps fallback; carrier-merged autocomplete |
| 2c. Billing address | (gated by `checkout_hide_billing_address` / `checkout_require_billing_address`) | rendered as a sibling sub-accordion when "different billing" is on |
| 3. Shipping method | [[checkout-step-shipping-method]] | provider × service radio; COD-allowance; re-quote triggers |
| 3a. Time slots (per-method, when active) | [[checkout-step-time-slots]] | day-tab + slot-radio grid; capacity limit; auto-pick-provider |
| 4. Payment | [[checkout-step-payment]] | regular + credit groups; 8-stage filter pipeline; per-provider extras |
| 5. Place Order (terminal) | [[checkout-page-submit]] | redirect / popup / inline-tokenize per provider |
| → Right column | [[checkout-step-sidebar]] | 4 sub-sections + custom-text widgets + app-injection points |
| → Discount-code field | [[checkout-step-discount]] | two-path resolution; step-reset; reload semantics |
| → Bridge (storefront ↔ backend) | [[checkout-flow-storefront-backend-bridge]] | DOM → endpoint → cart-attribute → reload-fragment full map |

Below: a concise cross-step overview. **For per-step depth, drill into the aspect page** — the Assistant should NOT use this overview as a substitute for the aspect.

## Storefront behaviour

- **Step transitions** — a "save and continue" submit on each step calls the relevant POST endpoint, which sets the cart's `step` attribute and returns the **updated steps HTML**. The form-submit AJAX pipeline reloads `.js-checkout-shipping-address`, `.js-checkout-shipping`, `.js-checkout-payment`, etc. as instructed by the response's `reload` array (see [[checkout-page-javascript]]).
- **Country/state/city dependencies** — country picker → state picker → city picker; each change re-fires the relevant typeahead query. Custom event `cc.place.change` is mentioned in the brief but not directly verified in the templates surveyed; the trigger lives in the address-form module JS (verify).
- **Sidebar reload on step change** — the side panel's totals fragment reloads whenever a step changes — this keeps totals accurate as the customer picks shipping, switches address, etc.
- **Office / locker typeahead in the address step** — the marketplace/office shipping types render a typeahead-search + Google Maps map with nearest offices (toggled by the `checkout_hide_*_map` settings).

## JavaScript behaviour

The accordion open/close, per-step radio expansion, and quote-box loading states are all driven by `.js-*` hook classes and `cc.*` events catalogued in [[checkout-page-javascript]]. The step regions on this page map to the `.js-checkout-authorize`, `.js-checkout-shipping-address`, `.js-checkout-billing-address`, `.js-checkout-shipping`, and `.js-checkout-payment` containers.

## Customisations available to the merchant

Layout-affecting settings that change what's rendered in each step:

- `checkout_hide_billing_address` / `checkout_require_billing_address` — control the billing-address step.
- `checkout_hide_address_map`, `checkout_hide_office_map`, `checkout_hide_locker_map` — hide the map per shipping type.
- `hide_marketing` — hides the marketing-consent checkbox.
- `payment_description` — `1` shows the per-provider description text in the payment step.
- `checkoutText` / `checkoutSideText` — custom side-panel text modules.

The form-fields config drives per-form (register / billing / shipping / customer) field visibility, required-ness, and order. The full settings + per-provider config catalogue is on [[checkout-page-customisation]].

## Theme variations

- The step layout is **almost entirely shared** from a single global checkout template set. Themes can override individual step fragments for per-step customisation, the logo include for branding, and the summary include for sidebar layout.
- A handful of themes (`flair-bmw`, `flair-clothesforyou`) tweak the checkout's logo placement.

## Known issues / by-design vs bug

- **The order summary is recomputed at submit, not trusted from the rendered side panel** — even when the sidebar's totals fragment reloads, the final total is recomputed from the cart entity at submit-time (see the idempotency guard in [[checkout-page-submit]]).
- **`hide_marketing` and GDPR interaction** — when `hide_marketing` is on AND GDPR is inactive, the customer's marketing flag is automatically set to `no` on submit; this can confuse merchants who expected the customer's prior preference to be preserved.
- **`checkout_hide_single_shipping` partially wired** — when only one shipping option exists, this setting is meant to auto-select and hide the picker, but the code paths are commented out in several places (verify).

## Related

- [[checkout]] — hub.
- [[checkout-step-customer]] / [[checkout-step-shipping]] / [[checkout-step-shipping-address]] / [[checkout-step-shipping-pickup]] / [[checkout-step-shipping-method]] / [[checkout-step-time-slots]] / [[checkout-step-payment]] / [[checkout-step-sidebar]] / [[checkout-step-discount]] — per-step aspect pages with full depth.
- [[checkout-flow-storefront-backend-bridge]] — DOM ↔ controller ↔ cart attribute map.
- [[checkout-page-routing]] — step machine + URL hash routing.
- [[checkout-page-javascript]] — JS hook catalogue (`.js-*` + `cc.*` events).
- [[checkout-page-submit]] — Place Order terminal endpoint.
- [[checkout-page-customisation]] — settings catalogue.
- [[storefront-cart]] — the page customers come from.
- [[shipping-calculation]] — quote computation backing the shipping-method step.
- [[payment-provider-mechanism]] — payment provider lifecycle.
- [[discount-stacking]] — stacking rules behind the discount-code field.
- [[settings-cart]] — checkout-affecting layout settings.

## Open questions

- The `cc.place.change` event the brief mentions — referenced in some address-form module JS but the precise selector binding wasn't located in the surveyed templates. (verify in the address-form module JS)
- `checkout_hide_single_shipping` setting — code paths are commented out in multiple places. Is this setting still functional? (verify)
