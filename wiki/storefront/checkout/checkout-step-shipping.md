---
type: storefront-page
nav_path: "Storefront → Checkout → Shipping step"
route_name: checkout.shipping.address
route_path: /checkout/shipping-address
themes_using: [all]
aliases: ["Checkout shipping step", "Shipping type radio", "Address vs office vs locker vs marketplace", "Стъпка доставка", "Тип доставка"]
tags: [storefront, checkout, shipping, address, office, locker, marketplace]
plan_gates: []
created: 2026-06-12
updated: 2026-06-12
source_count: 4
---

> Part of [[checkout]]. See the hub for the other aspects (customer, payment, sidebar, submit, routing). The 4 channels expand into [[checkout-step-shipping-address]], [[checkout-step-shipping-pickup]], and the [marketplace](#marketplace-merchants-own-stores) section below.

# Checkout — Shipping step (channel picker)

## Purpose

The customer picks **how** they want the order delivered: to their home address, to a courier office, to a self-service locker, or pickup at the merchant's physical store ("marketplace" — see [[apps-stores]]). This is the single most-customised checkout step — the merchant's installed shipping apps + customer's geo determine which channels appear and how each channel collects the address.

## URL & route

See `route_name` and `route_path` in frontmatter. This is a sub-section of [[checkout]] — the parent `/checkout` page hosts these step containers; container reload routes are listed under "Where to find it".

## How it loads

Loaded as a sub-region of the `/checkout` page (see [[checkout-page-routing]] for the parent route + middleware stack). On step transitions, the container is GET-reloaded via its `data-ajax-box` URL — see [[checkout-flow-storefront-backend-bridge]] for the full reload-fragment map.

## Where to find it

Below the customer step on `/checkout`. DOM: `<div class="cc-checkout-step cc-checkout-step-shipping-address js-checkout-shipping-address">`. Container reloads via `data-ajax-box="{route('checkout.shipping.address')}"`.

## The 4 shipping channels

The platform exposes 4 **shipping channel keys** the customer can choose between. The merchant doesn't pick them directly — they're inferred from the installed shipping apps + the per-provider configuration:

| Channel key | What it means | Where the actual location comes from |
|---|---|---|
| `address` | Courier delivers to a typed address | Customer types / picks from saved addresses |
| `office` | Customer picks up at a carrier office (Econt, Speedy, Cargus office) | Carrier API — see [[checkout-step-shipping-pickup]] |
| `locker` | Customer picks up at a self-service locker (Econtomat, BoxNow, Speedy APT) | Carrier API — see [[checkout-step-shipping-pickup]] |
| `marketplace` | Customer picks up at one of the merchant's own stores | Merchant's [[apps-stores]] catalogue — see [marketplace section](#marketplace-merchants-own-stores) below |

For the underlying per-channel pricing + waybill mechanics see [[shipping-provider-mech-pickup-points]].

## What the customer sees — the type radio + sub-accordions

The controller passes a `$types` collection where each entry has `{key, name, active, html}`. The template renders:

- **If `$types->count > 1`**: an accordion with one radio per type. Selecting a radio opens that type's `html` sub-accordion (the inner form). Form name = `checkout[shipping][type]`.
- **If exactly one type**: the type's `html` is rendered directly inside a `cc-form-section` wrapper; the type key goes into a hidden input.
- **If zero types**: a notification message *"sf.widget.checkout.nfy.no_shipping_types_available"* — the customer cannot proceed.

The `html` for each type comes from a per-type sub-template:

| Type key | Sub-template |
|---|---|
| `address` | `checkout/steps/shipping-address/address.tpl` — see [[checkout-step-shipping-address]] |
| `office` | `checkout/steps/shipping-address/_office_locker.tpl` with `$officeType='office'` |
| `locker` | `checkout/steps/shipping-address/_office_locker.tpl` with `$officeType='locker'` |
| `marketplace` | `checkout/steps/shipping-address/marketplace.tpl` |

The `office` and `locker` sub-templates are the SAME file (`_office_locker.tpl`) parameterised by `$officeType` — see [[checkout-step-shipping-pickup]] for the full per-field walk.

### Billing-address checkbox (below the type accordion)

When the merchant has NOT forced the billing address (`checkout_hide_billing_address = no` AND `checkout_require_billing_address = no`), a checkbox appears below the shipping type:

```
☐ Use a different billing address
```

Checking it triggers the billing-address sub-accordion to expand. The platform stores the choice on the cart (`cart.hide_billing_address` becomes `0`). If the merchant forces *"always require billing"* (`checkout_require_billing_address = yes`), a `<input type="hidden" name="checkout[billing][has]" value="1">` is rendered instead — the checkbox is gone and the billing-address step is always visible.

If the merchant hides billing entirely (`checkout_hide_billing_address = yes`), no checkbox + no billing-address step.

## Marketplace — merchant's own stores

The `marketplace` channel is **not** a courier — it's the merchant's own physical store. Used by stores running [[apps-stores]] (the in-store-pickup app). The sub-template (`marketplace.tpl`) differs from offices/lockers:

- **All marketplaces pre-loaded** — the `$marketplaces` collection is rendered into the `<select>` as `options=$marketplaces->pluck('title_with_address','id')`. There is NO autocomplete API call; the merchant typically has 1–20 stores so the full list fits in a dropdown.
- **Google Map shows all markers at once** — instead of "nearby N", every marketplace is plotted on the map as a clickable marker.
- **Same customer-info fields as office/locker** — first_name, last_name, email (guest), phone, gated by the standard `checkout_hide_*` settings.
- **NO `hasGoogleMapKey` gate** for the marker — the `$hideMap` flag (per-installation default) controls whether the map is shown; if no Maps key, markers won't render but the `<select>` still works.

## Business rules

- **Channel availability is per-shipping-provider, not store-wide.** A provider declares which channels it supports (`SUPPORT_ADDRESS`, `SUPPORT_OFFICE`, `SUPPORT_LOCKER`). The controller iterates every active provider and unions their supported channels — see [[shipping-provider-mechanism]].
- **Per-category restrictions can hide channels.** If a product's category has `restrictions` of type `shipping`, providers NOT in the allowlist are dropped, which can in turn drop a whole channel.
- **Zone-aware filtering happens here too.** the platform code filters by the customer's resolved zone — see [[geo-targeting-zones]].
- **A bumper-offer block can inject below the type accordion.** When the `bumper_offer` app is installed + enabled with eligible products, the block renders inside the form (`hidden-lg` on desktop — it's a mobile affordance).
- **The "Save & continue" button is disabled if no type is active** (`{if !$hasActive} disabled{/if}`). The customer must explicitly pick one.

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
- [[checkout-step-shipping-address]] — `address` channel in depth.
- [[checkout-step-shipping-pickup]] — `office` + `locker` channels in depth (with / without Google Maps).
- [[checkout-step-shipping-method]] — the next step (provider × service radio + price + delivery date).
- [[checkout-step-customer]] — previous step.
- [[apps-stores]] — marketplace = merchant's own physical stores.
- [[settings-shipping]] — provider catalogue.
- [[settings-cart]] — billing-address visibility + custom-fields.
- [[shipping-provider-mechanism]] — provider configuration + channel support catalogue.
- [[shipping-provider-mech-pickup-points]] — channel-vs-channel comparison (address / office / locker).
- [[shipping-calculation]] — how price is computed per channel.
- [[geo-targeting-zones]] — zone-aware provider filtering.

## Open questions

None — all channel rendering verified against the theme templates + per-type sub-templates on 2026-06-12.
