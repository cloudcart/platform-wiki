---
type: storefront-page
route_name: checkout
route_path: /checkout
themes_using: [all]
tags: [storefront, checkout, conversion, payment, shipping, discount]
created: 2026-06-08
updated: 2026-06-10
source_count: 8
---

# Checkout

## Purpose

The single page that converts the customer's [[storefront-cart]] into an order. CloudCart uses an **express (single-page, step-by-step accordion) checkout** by default: all of "Sign in / guest", "Shipping address", "Billing address", "Shipping method", and "Payment" are present on one page, in stacked accordion sections, and switch open / collapsed as the customer progresses. There is **no multi-page wizard variant** — every theme renders the same `checkout/express.tpl` layout.

This is the most error-prone page on the platform (payment failures, shipping miscalculations, address validation, country/state dependencies, GDPR consent, plan-gate edge cases) and therefore the most-consulted by support. Because it covers many distinct concerns, the detail is split into five aspect pages — drill into the one that matches the question rather than reading all five.

## Sub-pages (in this cluster)

**Per-step pages (split 2026-06-12 — each is the canonical depth-page for that step):**

- [[checkout-step-customer]] — authorize step; guest / login / register / email-code; `allowed_tabs` priority.
- [[checkout-step-shipping]] — shipping channel picker (address / office / locker / marketplace).
- [[checkout-step-shipping-address]] — to-address sub-flow; saved addresses vs inline form; Google Maps gating.
- [[checkout-step-shipping-pickup]] — to-office / to-locker; typeahead + Google-Maps-vs-no-Maps fallback; carrier-merged autocomplete; the must-document fallback for support tickets.
- [[checkout-step-shipping-method]] — provider × service radio; COD/POP-allowance flag flow; re-quote triggers.
- [[checkout-step-time-slots]] — date + time-slot grid (when `apps-shipping-hours` is active).
- [[checkout-step-payment]] — payment step; 8-stage filter pipeline; regular vs credit groups; per-provider extras.
- [[checkout-step-sidebar]] — right column / mobile slide-over; 4 sub-sections + custom-text widgets + app-injection points.
- [[checkout-step-discount]] — discount-code field; two-path resolution; step-reset semantics.

**Mechanics pages:**

- [[checkout-page-routing]] — full route map + middleware stack + step machine.
- [[checkout-page-steps]] — slim cross-step overview (one-line-per-step + links to the aspect pages above).
- [[checkout-page-submit]] — Place Order; per-provider redirect / popup / inline-tokenize.
- [[checkout-page-javascript]] — `.js-*` hook + `cc.*` event reference.
- [[checkout-page-customisation]] — merchant settings + theme overrides.

**Concept companion:**

- [[checkout-flow-storefront-backend-bridge]] — the full DOM → endpoint → cart attribute → reload fragment map.

## URL & route

- **Entry** — `checkout` — `/checkout`. Full route map (authorize, shipping-address, billing-address, shipping, payment, discount-code, summary fragments, edge routes) is on [[checkout-page-routing]].
- **Return URL (post-gateway)** — `checkout.return` — `/checkout/return/{status}/{payment_hash}` — see [[checkout-return]].
- **Middleware**: the entire `/checkout/*` group is wrapped by `XSS` and `cart_checkout`, plus controller-level `cart_customer`, `checkout_steps`, `unconfirmed_accounts_restrict`, `gdpr_policy_acceptances`, and `site.sandbox` — see [[checkout-page-routing]].

## How it loads

At a high level: plan-gate check → cart-exists check → cart min/max + stock guards → set the cart's `checkout` flag → build the steps array (`authorize`, `shippingAddress`, `billingAddress`, `shipping`, `payment`) → render the current step open and future steps as placeholders → render `express.tpl`. The full step-by-step sequence and every guard that can bounce the customer back to `/cart` is on [[checkout-page-routing]].

## What the customer sees

A single-column page with a free-shipping progress bar, a stacked accordion of the five steps, the place-order CTA + consent checkboxes + order-notes field, and an order-summary side panel (products, totals, discount-code field). The region-by-region breakdown is on [[checkout-page-steps]].

## Storefront behaviour

Step transitions POST to per-step endpoints that re-run `_getSteps` and return updated steps HTML; the side panel reloads on every step change to keep totals accurate; shipping recalculates when the address or a COD-affecting payment changes; discount codes apply/remove via dedicated endpoints. The recalc + discount + submit behaviours are detailed on [[checkout-page-submit]].

## JavaScript behaviour

The page binds a large set of `.js-*` hook classes (per-step containers, summary fragments, accordion bodies, quote-box loading states, the place-order form) and fires `cc.*` events on step transitions, sign-in, and cart recomputation. The complete reference is on [[checkout-page-javascript]].

## Customisations available to the merchant

Layout/behaviour settings (`checkout_animation`, `checkout_hide_billing_address`, `checkout_min_price`/`checkout_max_price`, `default_payment_provider`, `hide_marketing`, etc.), the `form_fields` per-form configuration, per-payment- and per-shipping-provider configuration, and app overrides (Bumper Offer, Membership, Store Locations) are all catalogued on [[checkout-page-customisation]] — most live under [[settings-cart]].

## Theme variations

The checkout layout is almost entirely shared; themes can override `express.tpl`, `include/logo.tpl`, `include/summary.tpl`, and individual `steps/*.tpl`. A theme that overrides a step template must keep the `.js-*` hooks intact. Details on [[checkout-page-customisation]].

## Known issues / by-design vs bug

- **The checkout page is the single source of truth for cart totals** — the final total is recomputed from the cart entity at submit-time; the idempotency guard catches double-submits. See [[checkout-page-submit]].
- **Emails fire from the return page, not from checkout submit** — see [[checkout-return]].
- **Crawlers get 404; sandbox/trial plans without `checkout` can't reach the page** — see [[checkout-page-routing]].
- **`hide_marketing` + GDPR interaction** can silently set the customer's marketing flag to `no` — see [[checkout-page-customisation]].

## Related

- [[storefront-architecture]] — request lifecycle, AJAX-pipeline, accordion + form-submit conventions.
- [[storefront-cart]] — the page customers come from.
- [[checkout-return]] — the page customers return to after off-site payment.
- [[checkout-complete]] — the thank-you page (if a custom page is configured).
- [[cart-vs-order-lifecycle]] — Cart → Order transition.
- [[checkout-flow]] — end-to-end conceptual flow.
- [[order-processing-pipeline]] — what happens server-side after submit.
- [[order-status-workflow]] — Order state machine after creation.
- [[settings-cart]] — checkout-affecting settings.
- [[discount-stacking]] — discount application order.
- [[shipping-calculation]] — how shipping quotes are computed.
- [[shipping-provider-mechanism]] — shipping provider integration.
- [[payment-provider-mechanism]] — payment provider integration.
- [[storefront-known-issues]] — cross-page bugs.

## Open questions

- The `cc.place.change` event for the country/state/city dependency chain — referenced but the precise selector binding wasn't located in surveyed templates. (verify — see [[checkout-page-javascript]])
- `checkout_hide_single_shipping` — code paths are commented out; is the setting still functional? (verify — see [[checkout-page-customisation]])
- Whether there's a documented allowlist of payment providers that support inline (no-redirect) tokenization. (verify per [[payment-provider-mechanism]])
- The `creditor` sub-flow (`creditor.select`, `creditor.consent`) UX in the express checkout. (verify — see [[checkout-page-submit]])
