---
type: entity
nav_path: "Entity → Shipping Provider → Cash on delivery"
aliases: ["Shipping provider COD", "Cash on delivery shipping", "COD surcharge", "COD cap", "COD agreement number", "COD sync", "Automatic COD paid sync", "10000 BGN COD cap"]
tags: [entity, shipping, couriers, providers, cod, cash-on-delivery, payments, multi-currency]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[shipping-provider]]. See the hub for the other aspects (attributes, lifecycle, pricing models, checkout filters, delivery channels & waybill).

# Shipping Provider — Cash on delivery (COD)

## Identity

When the customer picks **Cash on delivery (COD)** as the payment method, the courier collects the cash on the merchant's behalf at delivery time. This changes three things relative to a paid-up-front order: the price the customer pays (carrier surcharge), what's allowed at checkout (per-currency cap), and what happens after delivery (automatic payment sync). Every COD-supporting Shipping Provider needs a configured **COD agreement number** plus the **COD-sync toggle** on its settings page (see [[shipping-provider-attributes]]).

## Aliases

- **Cash on delivery shipping** / **Shipping provider COD** — the umbrella term.
- **COD surcharge** — the carrier-side fee.
- **COD cap** / **10,000 BGN COD cap** — the per-currency upper bound.
- **COD agreement number** / **`cod_account`** — the carrier contract ID stored on the provider.
- **COD sync** / **Automatic COD paid sync** — the post-delivery payment-status flip.

## Key Attributes

### COD surcharge

When the customer selects COD as their payment method, the courier collects the cash at delivery on the merchant's behalf. Three things differ from a card / online payment:

- **For carrier-integration methods**, the surcharge is **included in the carrier's quoted shipping price** (Speedy / Econt / etc. bake their COD margin into the rate).
- **For Custom methods**, the merchant sets a flat COD fee in [[settings-cart]] or per-method settings.

### Currency-specific COD cap

The platform enforces a **10,000 BGN cap** on COD per order **only when the store currency is the literal `BGN`** (legacy). Carts above the cap have the COD option **hidden at checkout**.

- For **any other currency — including `EUR`, the new Bulgarian norm after the euro adoption** — no platform-side cap applies; only the carrier's own server-side limit applies. So a BG store that switched to EUR no longer has the 10,000 platform cap.
- The cap is **currency-aware** (per [[multi-currency]]) — different store currencies may surface different caps.

### Automatic COD-paid sync

When the courier collects the cash at delivery and reports the COD-collected event, CloudCart automatically marks the order's payment as `completed` via [[orders-sync-cod]] (assuming the COD-sync toggle is ON).

The toggle's UI label:

> *"Automatically set order status to paid when we get information from shipping provider with Cash on delivery"*

For COD to work end-to-end, the merchant must:

1. **Have the carrier's COD agreement** — a contractual setup with the carrier's bank.
2. **Configure the COD agreement number** in the carrier's settings (Econt's `cod_account` field, Speedy's equivalent, etc.).
3. **Enable the COD-sync toggle** on the provider's settings page.

### Multi-currency COD conversion at API-call

Same pattern as the general pricing-model conversions (see [[shipping-provider-pricing-models]]):

- **[[apps-dpdbulgaria-speedy|DPD Bulgaria (Speedy)]]** bills in **EUR**; for a store in a different currency (e.g. RON), the platform converts the COD amount to EUR on the quote / waybill call.
- **Cargus** requires COD amounts in RON.
- The order's stored COD amount stays in the original currency — the conversion is only for the API request.

### COD-agreement validation against carrier client list

Econt and Speedy verify the configured COD account against the merchant's registered carrier-side clients before each quote; outdated configs are silently dropped — the COD option simply disappears from checkout without an inline error in the admin UI. If the merchant changes their carrier-side client (e.g., new contract number), they must update the COD agreement field on the provider page.

### Cart Rules can add / remove COD surcharges

[[apps-cart-rules]] can modify the COD-related shipping surcharge on qualifying carts. See [[shipping-provider-checkout-filters]] for the full Cart Rules override pattern.

## Where it appears

- Per-carrier app pages — the **COD agreement number** field + **COD-sync toggle** live here (e.g., [[apps-econt]], [[apps-dpdbulgaria-speedy|Speedy]], [[apps-dpdbulgaria-speedy]], [[apps-cargus]]).
- [[settings-shipping]] — visible COD-enabled marker on each provider row.
- [[settings-cart]] — Custom-method flat COD fee + global COD options.
- [[orders-sync-cod]] — the post-delivery payment-status flip handler.
- [[orders-details]] — per-order COD amount + sync status are displayed in the payment section.
- [[checkout-flow]] — the cap + carrier-validation filters decide whether COD is offered to the customer.

## Related

- [[shipping-provider]] — hub.
- [[shipping-provider-attributes]] — where the COD agreement number + COD-sync toggle live.
- [[shipping-provider-pricing-models]] — multi-currency conversions apply to COD as well.
- [[shipping-provider-checkout-filters]] — Cart Rules can override COD surcharges.
- [[orders-sync-cod]] — the auto-paid handler.
- [[orders-details]] — per-order payment view.
- [[payment-provider]] — sister entity; the COD payment provider is what the customer actually selects.
- [[settings-cart]] — Custom-method flat COD fee.
- [[multi-currency]] — currency-aware cap + API-call FX conversion.

## Open Questions

- Whether the 10,000 BGN cap is ever overridable on a per-merchant basis `(verify)`.
- Exact behaviour when the COD-sync toggle is OFF but the carrier still pushes the COD-collected webhook — does the platform record the event silently for the merchant to manually reconcile, or drop it? `(verify)`
