---
type: storefront-page
route_name: checkout
route_path: /checkout
themes_using: [all]
tags: [storefront, checkout, javascript, js-hooks, events, ajax]
created: 2026-06-10
updated: 2026-06-10
source_count: 8
---

> Part of [[checkout]]. See the hub for the other aspects (routing & middleware, steps & layout, submit & payment handoff, merchant customisation).

# Checkout — JavaScript hooks & events

## Purpose

The exhaustive reference of client-side hook classes (`.js-*`), data attributes (`[data-*]`), and custom jQuery events (`cc.*`) the express checkout binds to. This aspect exists so support / theme developers can find the exact selector a behaviour hangs off — these strings are load-bearing and preserved verbatim. The behaviours these hooks drive are described functionally in [[checkout-page-steps]] and [[checkout-page-submit]].

## URL & route

These hooks all appear on `checkout` — `/checkout` — within the theme templates, `steps/*.tpl`, and `include/*.tpl`. There is no separate route for the JS layer.

## How it loads

The hook classes are emitted server-side in the checkout templates; the storefront's bundled checkout JS binds behaviours to them on `document.ready` and re-binds after each AJAX fragment reload (`cc.ajax.reload`). The AJAX `reload` array returned by each step POST names the `.js-checkout-*` containers to swap (see [[checkout-page-submit]] for the discount-code reload set).

## What the customer sees

This aspect is non-visual — it documents the hooks behind the visible accordion, quote-box loading spinners, and submit-button loaders. The customer sees the *effects*: accordion sections expanding, quote boxes showing a loading state then results, and the Place-order button showing a spinner. See [[checkout-page-steps]] for the visible regions.

## Storefront behaviour

The hooks drive every AJAX reload, accordion toggle, and quote-loading state on the page. The per-step containers below are reloaded as instructed by the response's `reload` array on each step transition.

## JavaScript behaviour

Hook classes / data attributes used (verified in `_global/templates/checkout/express.tpl`, `steps/*.tpl`, `include/*.tpl`):

- `.js-cc-checkout` — root wrapper.
- `.js-checkout-container` — steps wrapper.
- `.js-checkout-sidebar`, `.js-checkout-sidebar-toggle` — side panel + mobile-toggle target.
- `.js-checkout-summary` — order-summary fragment.
- `.js-checkout-authorize`, `.js-checkout-shipping-address`, `.js-checkout-billing-address`, `.js-checkout-shipping`, `.js-checkout-payment` — per-step containers; reloaded as instructed by the AJAX `reload` array.
- `.js-checkout-summary-totals`, `.js-checkout-summary-products`, `.js-checkout-summary-discount-code` — summary fragments.
- `.js-checkout-payment-form` — the place-order form.
- `.js-checkout-hash-reload` — marker meaning "reload this section on hash change".
- `.js-checkout-total-formatted` — sub-total display in the mobile cart-toggle button.
- `.js-body-reload` — set on `<body>` when a logged-in customer is present; triggers a full reload after some cart events (used to keep the summary fresh).
- `.js-payments` — payment-provider accordion wrapper.
- `.js-accordion-payment-provider-{provider}` — per-provider body.
- `.js-accordion-shipping-provider-{provider}` — per-shipping-provider body.
- `.js-accordion-shipping-type-{type}` — per-shipping-type body (`address` / `office` / `lockers` / `marketplace`).
- `.js-accordion-item-head-radio` — the radio inside an accordion head that opens/closes its body.
- `.js-shipping-quotes-box`, `.js-shipping-quotes-box-holder-{key}`, `.js-shipping-quotes-box-loaded`, `.js-shipping-quotes-box-loading`, `.js-shipping-quotes-box-no-shipping` — quote-rendering states.
- `.js-shipping-service-hidden` — quotes-box of a service that's been filtered out.
- `.js-single-shipping-type-{type}` — appears when only one shipping type is available (the type-picker collapses).
- `.js-creditor-customer`, `.js-leasing-options-table` — credit / leasing payment-provider UIs.
- `.js-delivery-dates-date` — date-picker in the shipping step (e.g., for couriers that pick a delivery date).
- `.js-complex-field` — field group with show/hide-on-focus behaviour.
- `.js-fillable-checkout-shipping-address-address-first-name`, `…-last-name`, `…-email`, `…-address-phone` — fields the inline script (in `steps/shipping-address.tpl`) synchronises across the multi-form layout so first-name typed in one form copies to the others.
- `.js-form-submit-ajax-new` — the modern AJAX form-submit pipeline (with submit-loader); `data-submit-loader="true"` adds the spinner overlay.
- `.js-action` — generic JS action binding (used on inline "log in" link).
- `.js-loading` — submit button with built-in loading spinner.
- `[data-shipping-recalculate="{url}"]` — radio data attribute on payment providers that need to trigger shipping recalc when chosen.
- `[data-ajax-box]`, `[data-module="accordion"]`, `[data-accordion-title]`, `[data-accordion-content]` — accordion + AJAX-fragment plumbing.
- `[data-toggle-box1=".js-checkout-billing-address"]` — toggle-target binding for "Use different billing address".

Custom `cc.*` events fired by checkout code:

- `cc.checkout.step` — fires every step transition; modules that need to update on step change bind to this.
- `cc.guest.sign.in`, `cc.user.sign.in` — fire after guest / registered customer authorizes.
- `cc.customer.update`, `cc.user.details.updated` — fire after customer profile update.
- `cc.cart.product.updated`, `cc.cart.updated` — fire when discount/total recomputation affects cart.
- `cc.ajax.reload` — fires when an `[data-ajax-box]` is reloaded.
- `cc.overlay.hide` — fires when a side panel closes.

## Customisations available to the merchant

A merchant or theme developer can bind custom JS to any of the `cc.*` events above to extend checkout (e.g. fire a custom pixel on `cc.checkout.step`, or react to `cc.guest.sign.in`). The hook classes are stable contract points; the settings that toggle which hooks appear (e.g. `checkout_animation` for accordion slide) are on [[checkout-page-customisation]].

## Theme variations

- The hook classes and events are **shared across all themes** — they are emitted by `_global/templates/checkout/`. A theme overriding a `steps/*.tpl` must keep the `.js-*` hooks intact or the checkout JS will not bind. This is the main risk when a theme customises a step template.
- `checkout_animation` toggles whether the accordion uses slide animations on open/close; the hooks are the same either way.

## Known issues / by-design vs bug

- **Theme overrides must preserve `.js-*` hooks** — if a custom `steps/*.tpl` drops a hook class (e.g. `.js-checkout-payment-form`), the corresponding behaviour silently breaks. This is the most common cause of "checkout button does nothing" tickets on heavily-customised themes.
- **`cc.place.change`** — referenced in the brief for the country/state/city dependency chain but the precise selector binding wasn't located in the surveyed templates (verify). The other `cc.*` events are confirmed.
- **`.js-fillable-*` cross-form sync** — first-name/last-name/email/phone typed in one form copy to the others via the inline script in `steps/shipping-address.tpl`; if a theme reorders fields this sync can mis-target (verify on customised themes).

## Related

- [[checkout]] — hub.
- [[storefront-architecture]] — the AJAX-pipeline + accordion conventions these hooks plug into.
- [[checkout-page-steps]] — the visible regions these hooks drive.
- [[checkout-page-submit]] — the recalc / discount / place-order behaviours bound to these hooks.

## Open questions

- The `cc.place.change` event — referenced in some address-form module JS but the precise selector binding wasn't located in the surveyed templates. (verify in the address-form module JS)
