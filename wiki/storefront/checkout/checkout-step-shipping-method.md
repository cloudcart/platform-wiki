---
type: storefront-page
nav_path: "Storefront → Checkout → Shipping method step"
route_name: checkout.shipping
route_path: /checkout/shipping
themes_using: [all]
aliases: ["Checkout shipping method", "Shipping provider radio", "Shipping quotes", "Delivery date picker", "COD allowance", "Стъпка метод доставка"]
tags: [storefront, checkout, shipping, providers, quotes, delivery-date]
plan_gates: []
created: 2026-06-12
updated: 2026-06-12
source_count: 3
---

> Part of [[checkout]]. Follows [[checkout-step-shipping]]; precedes [[checkout-step-payment]]. The delivery-date sub-block is documented on [[checkout-step-time-slots]].

# Checkout — Shipping method step (provider × service)

## Purpose

After the customer picks WHERE the order goes ([[checkout-step-shipping]] + [[checkout-step-shipping-address]] / [[checkout-step-shipping-pickup]]), they pick the actual **shipping method** — a provider+service combination with a calculated price and delivery date. This step is fully dependent on the address — every method is quoted live against the chosen address through the [[shipping-calculation]] pipeline.

## URL & route

See `route_name` and `route_path` in frontmatter. This is a sub-section of [[checkout]] — the parent `/checkout` page hosts these step containers; container reload routes are listed under "Where to find it".

## How it loads

Loaded as a sub-region of the `/checkout` page (see [[checkout-page-routing]] for the parent route + middleware stack). On step transitions, the container is GET-reloaded via its `data-ajax-box` URL — see [[checkout-flow-storefront-backend-bridge]] for the full reload-fragment map.

## Where to find it

Below the shipping-address step on `/checkout`. DOM: `<div class="cc-checkout-step cc-checkout-step-shipping js-checkout-shipping">`. Container reloads via `data-ajax-box="{route('checkout.shipping')}"` whenever the address changes upstream.

## What the customer sees

A radio accordion — one row per available provider × service. Each row carries:

- **Provider icon** (`$m->getImage('150x150')`).
- **Provider + service name** (e.g. *"Speedy — economy 3-day"*).
- **Computed price** for this cart on this address (from [[shipping-calculation]]).
- **Delivery date / window** (e.g. *"Tomorrow"*, *"Tue 18 June"*, *"3–5 business days"*).
- **COD-allowance hint** when the provider supports COD AND the cart is COD-eligible — surfaces in the per-row description.

When the chosen method has the **Delivery time** app (`apps-shipping-hours`) configured, a per-service **date + time-slot picker** appears below the row — see [[checkout-step-time-slots]] for the full tab-and-slot grid.

## Where the list comes from — the quote pipeline

The controller hydrates `$managers` for each shipping provider that:

1. **Supports the chosen channel** (address / office / locker / marketplace) AND
2. **Passes the geo-zone filter** for the customer's address (the platform code) AND
3. **Returns a quote** for the cart's subtotal + weight + product categories.

For each surviving provider, the per-service quotes are gathered via `$m->hasCheckoutQuotes && $m->getCheckoutQuotes`. If a provider has more than one service, the row expands into a sub-accordion of sibling services with per-row prices.

The full per-stage calculation (geographic eligibility, rate model, cart-tier matching, carrier-API quote, free-shipping check) is documented in [[shipping-calculation]] and split aspects.

## COD-allowance per quote

Each quote carries a boolean `allowance_cash_on_delivery` flag, returned by the carrier or set by the merchant's per-method config. The flag drives two downstream behaviours:

- **The "Cash on delivery" payment method** appears on the next step ONLY when at least one of: the chosen quote has `allowanceCashOnDelivery = true` OR the merchant's shipping manager `supportsCashOnDelivery = true`. If both are false, COD is dropped from the payment list — see [[checkout-step-payment]] for the filter pipeline.
- **The per-row COD hint** in the description shows the customer they can pay on delivery if they pick this method.

The same flag logic applies to "Pay on place" (POP) via `getAllowancePayOnPlace`.

## Settings & fields

- **Settings → Shipping** ([[settings-shipping]]) — provider catalogue + per-method enablement, custom rate rows, free-shipping rules.
- **Settings → Cart** ([[settings-cart]]) — `checkout_hide_single_shipping` (auto-pick when only one method is available); `shipping_provider_recalculate` semantics.
- **Per-product / per-category restrictions** ([[products-categories-cart-restrictions]]) — categories can limit which shipping providers are offered.
- **Geo zone filtering** ([[geo-targeting-zones]]) — each provider scopes itself to one or more zones.

## Business rules

- **Re-quote on every address change.** The controller re-runs the quote pipeline whenever the shipping address step submits — so changing the city OR the channel (address → office) re-fetches every method's quote.
- **Re-quote on payment change too** (for some providers). Payment providers can flag `supports_recalculate_shipping = true` (e.g. COD changes the COD-handling fee on Speedy). When such a payment is picked, the `data-shipping-recalculate` attribute on the payment radio triggers `checkout.shipping.recalculate` which re-runs the pipeline. See [[checkout-step-payment]].
- **A method that returns no quote is silently dropped.** Carriers that error out (API down, address not serviceable, etc.) don't surface an error to the customer — their row simply doesn't appear. Support tickets *"this carrier is missing"* often trace to a carrier-API failure logged in the platform error log.
- **The "Save & continue" button is disabled if no method is active.** The customer must explicitly pick one. The platform never picks a default — the merchant cannot pre-select a "preferred" provider on this step.
- **Auto-pick when single method.** When `checkout_hide_single_shipping = yes` AND only one method survived the pipeline, the platform auto-selects + auto-advances past this step without rendering the radio.

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
- [[checkout-step-shipping]] — previous step (channel picker).
- [[checkout-step-shipping-address]] / [[checkout-step-shipping-pickup]] — the address input that drives quoting.
- [[checkout-step-payment]] — next step; payment list is filtered by the chosen method's flags.
- [[checkout-step-time-slots]] — delivery-date picker that appears below a method row when `apps-shipping-hours` is configured.
- [[shipping-calculation]] — the full quote pipeline (geo / rate model / cart-tier / carrier API).
- [[settings-shipping]] — provider + method admin.
- [[shipping-provider-mechanism]] — provider integration contract.
- [[geo-targeting-zones]] — zone filtering of providers.
- [[products-categories-cart-restrictions]] — category-level shipping restrictions.
- [[apps-shipping-hours]] — delivery-time / time-slot app.
- [[settings-cart]] — `checkout_hide_single_shipping`.

## Open questions

None — quote pipeline, COD/POP flag flow, re-quote on payment change all verified against the platform code + `_shipping_provider_quotes.tpl` on 2026-06-12.
