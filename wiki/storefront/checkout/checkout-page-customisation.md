---
type: storefront-page
route_name: checkout
route_path: /checkout
themes_using: [all]
tags: [storefront, checkout, settings, form-fields, theme, customisation, apps]
created: 2026-06-10
updated: 2026-06-10
source_count: 8
---

> Part of [[checkout]]. See the hub for the other aspects (routing & middleware, steps & layout, submit & payment handoff, JavaScript hooks).

# Checkout — merchant customisation & theme overrides

## Purpose

Everything a merchant can change about the checkout page without code: the layout/behaviour settings, the `form_fields` configuration, per-payment- and per-shipping-provider configuration, app-level overrides, and the theme override points. This is the "where do I change X on my checkout?" aspect. The behaviours these settings affect are described in [[checkout-page-steps]] and [[checkout-page-submit]].

## URL & route

These settings are applied to the `checkout` — `/checkout` — page; they live in the admin under [[settings-cart]] (Checkout settings), admin → Layout → Form fields, and per-provider configuration screens. The storefront page that consumes them renders the theme templates.

## How it loads

Each setting is read when the checkout controller builds the steps array and renders the express template. Form-field config is read from the `form_fields` table per form. Per-provider config is read when the payment/shipping step filters and renders providers (see [[checkout-page-steps]]). Changing a setting takes effect on the next checkout render.

## What the customer sees

The visible result depends on the settings below — e.g. with `checkout_hide_billing_address` on, the customer never sees a billing-address step; with `payment_description = 1`, each payment option shows its description text. The region-by-region view is in [[checkout-page-steps]].

## Storefront behaviour

Settings change which guards fire and which steps render. For example `checkout_min_price` / `checkout_max_price` block the steps entirely behind a notice (see [[checkout-page-routing]]); `default_payment_provider` / `default_shipping_provider` pre-select a radio so the customer's first render already has a choice made.

## JavaScript behaviour

- `checkout_animation` toggles whether the accordion sections use slide animations on open/close. The underlying hook classes are unchanged — see [[checkout-page-javascript]].
- All other settings here are server-side render toggles; they change which hook-bearing elements are emitted, not the JS bindings themselves.

## Customisations available to the merchant

Layout and behaviour settings ([[settings-cart]] + Checkout settings):

- `checkout_animation` — enable accordion slide animations.
- `checkout_enable_footer` — render the storefront footer below the checkout (off by default — checkout is a "one-task page").
- `checkout_hide_billing_address` — billing address is never collected.
- `checkout_require_billing_address` — billing address is always required (no "Use different" toggle).
- `checkout_hide_address_map`, `checkout_hide_office_map`, `checkout_hide_locker_map` — hide the Google Maps map per shipping type.
- `checkout_hide_single_shipping` — when only one shipping option is available, auto-select it and hide the picker (currently commented out in several code paths — verify).
- `checkout_min_price`, `checkout_max_price` — cart-amount gates.
- `checkout_customer_access` — required-account / allow-guest setting.
- `default_payment_provider`, `default_shipping_provider` — pre-selected radio.
- `payment_description` — `1` shows the per-provider description text.
- `hide_marketing` — hides the marketing-consent checkbox.

Form-field configuration (admin → Layout → Form fields):

- The `form_fields` table drives per-form (register / billing / shipping / customer) field visibility, required-ness, and order. Each row has a `form`, `field_key`, `position`, `required`, `visible`. Custom fields can be added.

Per-payment-provider configuration:

- `payment_description` text per provider.
- `min_price`, `max_price` per provider.
- Allowed-order-amount slabs.
- Restrictions to specific shipping providers.
- Customer-details fields per provider (e.g. Mokka, Borica installments).

Per-shipping-provider configuration:

- Allowed payment providers (`provider->payments` relation).
- COD / POP allowance.
- Geo-zone restriction.

App-level overrides:

- **Bumper Offer** — inserts a one-click upsell block in the steps stack.
- **Membership** — adjusts the order with subscription-page rights on success.
- **Store Locations** — restricts shipping address to allowed zones.

## Theme variations

- The checkout layout is **almost entirely shared** — the theme templates is the source of truth. Themes can override:
  - `checkout/express.tpl` for layout rearrangement (column order, sticky bar position).
  - `checkout/include/logo.tpl` for branding.
  - `checkout/include/summary.tpl` for sidebar layout.
  - Individual `steps/*.tpl` for per-step customisation.
- A handful of themes (`flair-bmw`, `flair-clothesforyou`) tweak the checkout's logo placement.
- The cart-link button at the bottom of the cart's "Continue to checkout" CTA opens the checkout **as a side panel** (AJAX-modal) on some themes; on most, it navigates.
- **Override risk** — a theme that overrides a `steps/*.tpl` must keep the `.js-*` hooks (see [[checkout-page-javascript]]) or the corresponding behaviour silently breaks.

## Known issues / by-design vs bug

- **`hide_marketing` and GDPR interaction** — when `hide_marketing` is on AND GDPR is inactive, the customer's marketing flag is automatically set to `no` on submit; this can confuse merchants who expected the customer's prior preference to be preserved.
- **`checkout_hide_single_shipping` partially wired** — the code paths (`_checkSingleQuoteShippingManager`) are commented out in multiple places; the setting may not currently auto-hide the single shipping option (verify).
- **`checkout_enable_footer` off by design** — checkout is a "one-task page"; merchants who expect their footer to show on checkout must enable it explicitly.

## Related

- [[checkout]] — hub.
- [[settings-cart]] — the admin home for most checkout settings.
- [[checkout-page-steps]] — the regions these settings show/hide.
- [[checkout-page-submit]] — per-provider config that shapes the payment handoff.
- [[payment-provider-mechanism]] — per-payment-provider configuration model.
- [[shipping-provider-mechanism]] — per-shipping-provider configuration model.
- [[shipping-calculation]] — how shipping quotes (and COD/POP allowance) are computed.

## Open questions

- `checkout_hide_single_shipping` — whether the setting is still functional given the commented-out code paths. (verify)
- The full `form_fields` form keys beyond register / billing / shipping / customer, and which custom field types are supported. (verify)
