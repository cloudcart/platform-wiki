---
type: storefront-page
nav_path: "Storefront → Checkout → Time slots (delivery date)"
route_name: checkout.shipping
route_path: /checkout/shipping
themes_using: [all]
aliases: ["Checkout time slots", "Checkout delivery date picker", "Shipping hours storefront", "Часови слотове чекаут", "Дата на доставка"]
tags: [storefront, checkout, shipping, delivery-date, time-slots, apps-shipping-hours]
plan_gates: []
created: 2026-06-12
updated: 2026-06-12
source_count: 3
---

> Part of [[checkout]]. The picker is embedded INSIDE [[checkout-step-shipping-method]] when a shipping provider has the [[apps-shipping-hours|Shipping hours]] app configured.

# Checkout — Time slots / delivery date picker

## Purpose

When the merchant has the **Shipping hours** app installed and configured for a specific shipping provider, the customer at checkout sees a **date + time-slot picker** beside that provider's row — *"book your delivery: Tomorrow 08:00-12:00 / 14:00-18:00 / Thu 18:00-21:00 / ..."*. The chosen slot is bound to the order and surfaces in admin so the merchant can route their courier accordingly.

## URL & route

See `route_name` and `route_path` in frontmatter. This is a sub-section of [[checkout]] — the parent `/checkout` page hosts these step containers; container reload routes are listed under "Where to find it".

## How it loads

Loaded as a sub-region of the `/checkout` page (see [[checkout-page-routing]] for the parent route + middleware stack). On step transitions, the container is GET-reloaded via its `data-ajax-box` URL — see [[checkout-flow-storefront-backend-bridge]] for the full reload-fragment map.

## Where to find it

Inside the shipping-method row on the checkout page — see [[checkout-step-shipping-method]] for the parent row. DOM: nested inside `cc-accordion-section-body js-accordion-shipping-provider-{providerKey}`. The picker renders only when the provider's `delivery_dates` collection is non-empty.

## What the customer sees

A **tab + radio** grid:

```
┌─────────────────────────────────────────────────┐
│ [Mon 16] [Tue 17] [Wed 18] [Thu 19] [Fri 20] │ ← day tabs
├─────────────────────────────────────────────────┤
│ ○ 08:00 - 12:00, Speedy — 6.50 BGN │
│ ○ 12:00 - 16:00, Speedy — 6.50 BGN │
│ ○ 14:00 - 18:00, Speedy — 6.50 BGN (full) │ ← disabled when capacity hit
│ ○ 18:00 - 21:00, Speedy — 6.50 BGN │
└─────────────────────────────────────────────────┘
```

Each radio button:

- **Label format**: `"{from} - {to}, {provider name}{price}"` — e.g. `"08:00 - 12:00, Speedy — 6.50 BGN"`. Price suffix is added only when this picker is in "hide-shipping-box" compact mode and the quote is loaded.
- **Disabled** if the slot is full (per-day per-slot capacity limit set in admin — see [[apps-shipping-hours-settings]]). Disabled slots show description text *"full"* (translation key `sf.shipping_hours.text.full`).
- **Value submitted**: `checkout[shipping][{providerKey}][delivery_date_key]` = the slot's `key` (a per-day identifier the platform issues).

## What triggers the picker to appear

Three conditions must align — verified against the theme templates:

1. The shipping provider must have the **Shipping hours** app installed AND enabled on the store.
2. The provider's `getDeliveryDates` collection must return non-empty rows (the merchant has configured at least one day with at least one slot in [[apps-shipping-hours-settings]]).
3. The cart's customer address must be within the provider's serviceable area.

When any of these is false, the shipping-method row renders without the date picker — the customer just picks the method, the merchant ships in the regular handling window. This is the most common merchant question: *"why don't my customers see time slots"*. Answer in order: confirm the app is enabled; confirm day/slot setup; confirm a serviceable address.

## Auto-pick the provider's radio on slot click

When the customer clicks a slot radio (under the provider's nested accordion), the JS handler auto-checks the **parent provider's radio** (`#checkout-shipping-provider-internal_{providerId}`) AND fires the accordion-title click to expand the row. So picking a slot for Speedy auto-picks Speedy as the shipping method — the customer doesn't have to confirm both.

This handler is registered on `.js-delivery-dates-date` and also fires once on `:checked` to handle the initial pre-selected slot if any (see `_shipping_provider_quotes.tpl` line 178-187).

## Settings & fields

- **App enabled** — Apps → Shipping hours → Install + activate per shipping provider. See [[apps-shipping-hours]].
- **Day-of-week catalogue** — per-day rows with from/to hours, capacity (`limit`), and `interval`. Configured in [[apps-shipping-hours-settings]].
- **Exceptions** — per-date overrides (holidays, etc.) — see [[apps-shipping-hours-settings]].
- **Per-provider activation** — the app is enabled per shipping provider, not store-wide. So a merchant can offer slots on Speedy but not on Econt. See [[apps-shipping-hours-shipping-list]].

## Business rules

- **Slot capacity is global per day** — not per customer. When 3 customers book the *14:00-16:00* slot and the capacity is 3, the 4th customer sees that slot greyed-out *"full"*.
- **Disabled slots stay visible** — the merchant can see when their morning slots fill up first; the disabled state is the customer-facing signal.
- **The slot is captured on the order line, not on a separate entity.** The chosen `delivery_date_key` resolves server-side to a date + time range and is stored on the order's shipping record — see [[orders-details-shipping]] for where it surfaces in admin and [[orders-shipping-waybill]] for how it flows into the carrier waybill.
- **No per-day price difference at the UI level.** All slots share the provider's quoted price; the platform does NOT support per-slot pricing today (a Sunday slot is the same price as a Tuesday morning slot from the customer's perspective).

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

- [[checkout-step-shipping-method]] — parent step; the picker embeds inside its row.
- [[apps-shipping-hours]] — the app that powers the picker.
- [[apps-shipping-hours-settings]] — day-of-week + capacity + interval admin config.
- [[apps-shipping-hours-shipping-list]] — per-provider activation list.
- [[orders-details-shipping]] — where the chosen slot surfaces in admin.
- [[orders-shipping-waybill]] — slot flows here at fulfilment.
- [[shipping-calculation]] — the quote engine that the picker rides on top of.

## Open questions

None — picker rendering + slot-capacity + auto-pick-provider behaviour verified against `_shipping_provider_quotes.tpl` line 130-200 on 2026-06-12.
