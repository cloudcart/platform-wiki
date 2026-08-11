---
type: entity
nav_path: "Entity → Shipping Provider → Pricing models"
aliases: ["Shipping provider pricing models", "Shipping pricing models", "Live API quote", "Carrier-integration pricing", "Custom shipping rate rows", "Based on price", "Based on weight", "Based on price and weight", "Local pickup pricing", "Fixed flat shipping", "Marketplace shipping pricing", "Multi-currency shipping conversion"]
tags: [entity, shipping, couriers, providers, pricing, rates, multi-currency]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[shipping-provider]]. See the hub for the other aspects (attributes, lifecycle, checkout filters, COD, delivery channels & waybill).

# Shipping Provider — Pricing models

## Identity

A shipping method's **pricing model** decides how the price the customer sees at checkout is calculated. The model is set at creation in the "Choose the shipping method type" modal and **cannot be changed afterwards** — the type is permanent (see [[shipping-provider-lifecycle]]'s *Save-time guards*). There are three patterns: live carrier API, merchant-defined rate rows, and Local Pickup / Fixed flat. The model also determines what currency conversions the platform must do on every quote call.

## Aliases

- **Live API quote** / **Carrier-integration pricing** — the carrier-driven model.
- **Custom rate rows** / **Based on price** / **Based on weight** / **Based on price and weight** — the merchant-defined model.
- **Local Pickup** / **Fixed flat** — the marketplace / one-row patterns.
- **Multi-currency shipping conversion** — the FX behaviour on API-call.

## Key Attributes

### Three pricing models

A shipping method is exactly one of three patterns:

- **Live API quote (carrier integrations)** — `type = integration`. When a customer at checkout lands on a carrier-integration method, the platform calls the carrier's quote API in real time with package dimensions + weight + delivery channel + destination address + COD amount + insurance. The carrier returns one or more service options with current tariff prices (e.g., Econt returns "To address tomorrow 6.50 BGN", "To Econtomat 4 BGN", "Same-day 12 BGN"). The merchant **cannot edit individual rate rows** — the carrier's pricing is opaque.
- **Merchant-defined rate rows (custom methods)** — `type = price` / `weight` / `price_and_weight`. The merchant configures a Custom shipping method with one of three rate models:
  - **Based on price** — rate rows = price brackets.
  - **Based on weight** — rate rows = weight brackets.
  - **Based on price and weight** — nested brackets.
  Rate rows have `from` (inclusive), `to` (exclusive, blank = no upper bound), and `amount`. A row with `amount = 0` is effectively free shipping for that bracket. The merchant also picks a single geographic scope per method (see [[shipping-provider-checkout-filters]]).
- **Local Pickup / Fixed flat** — Local Pickup is `type = marketplace` and requires the Stores app ([[apps-stores]]) — the customer picks a physical store location. Fixed flat is a Custom method (`type = price`) with one rate row covering the whole bracket at a fixed amount (often 0 for free shipping over a threshold).

### Category-rate split (custom methods only)

Custom methods support a **SECOND rate table scoped to specific product categories** — e.g., heavy furniture vs. light parcels. The merchant configures one default rate table plus an override per [[category]]. At checkout, lines are bucketed by category and quoted against the matching table. Carrier-integration methods do NOT expose this split.

### Multi-currency conversions at API-call time

For multi-currency stores, the platform converts amounts to the carrier's billing currency at API-call time:

- **Speedy** requires amounts in BGN; for a EUR or RON store, the platform converts COD / insurance / subtotal to BGN.
- **Cargus** requires amounts in RON; non-RON stores convert to RON.
- **DHL** typically supports multi-currency directly.

The order's stored currency stays original; the conversion is only for the API request. Merchants don't see the converted amount in the admin UI.

### Re-quoting on cart change

Carrier-integration quotes are re-fetched when the cart's quotable inputs change (address, weight, dimensions). For Custom rate-row methods, re-quote is a simple recompute against the existing rate table — no API call.

### Pallet rules UI only on Econt

**Econt** is the only carrier with a dedicated pallet-rules UI in [[settings-shipping]] — under its `type = integration` pricing model the merchant can additionally toggle "Pallet Shipment" with a category + minimum-weight rule. When matched, the cart ships as pallets at pallet rates returned by Econt's API. Other carriers (Speedy, Cargus, DPD) accept pallet shipments via their general API but do not have a CloudCart-side pallet-rules form — the merchant configures pallet rates outside CloudCart, and the standard parcel quote returns the carrier's negotiated pallet rate.

## Where it appears

- [[settings-shipping]] — the "Add shipping method" modal picks the pricing-model type; existing rows show the model in the Type column.
- Per-carrier app pages — every carrier-integration provider is implicitly `type = integration` (e.g., [[apps-econt]], [[apps-dpdbulgaria-speedy|Speedy]], [[apps-boxnow]], [[apps-cargus]], [[apps-dhl]], [[apps-gls]]).
- [[apps-stores]] — required for Local Pickup (`type = marketplace`).
- [[multi-currency]] — the FX-rate source for the API-call conversions above.

## Related

- [[shipping-provider]] — hub.
- [[shipping-provider-lifecycle]] — pricing-model type is chosen at install and is permanent.
- [[shipping-provider-checkout-filters]] — geographic scope + customer-group restriction interact with the pricing model (per-method customer-group multi-select is exposed on Custom methods only).
- [[settings-shipping]] — where the pricing model is set.
- [[apps-stores]] — required for Local Pickup.
- [[multi-currency]] — FX-rate conversions for carrier API calls.
- [[shipping-calculation]] — the full arithmetic of how the chosen shipping cost is computed.
- [[category]] — category-rate split bucket key.

## Open Questions

- Whether the per-row `from` / `to` brackets are inclusive / exclusive in all UI surfaces `(verify)`.
