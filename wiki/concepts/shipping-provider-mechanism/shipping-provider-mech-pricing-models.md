---
type: concept
nav_path: "Concept → Shipping provider mechanism → Pricing models"
aliases: ["Shipping pricing models", "Live API quote", "Custom shipping rates", "Based on price", "Based on weight", "Based on price and weight", "Local Pickup", "Free shipping rate", "Three shipping pricing models", "Ценови модели на доставка", "Тарифи по тегло", "Тарифи по цена"]
tags: [shipping, couriers, providers, pricing, rates, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[shipping-provider-mechanism]]. See the hub for the other aspects (configuration, pickup points, waybill, COD, geo routing, status tracking).

# Shipping provider mechanism — Pricing models

## Definition

CloudCart supports **three pricing models** for shipping methods, and every method falls into exactly one of them: a **live API quote** from a carrier integration, **merchant-defined rate rows** in a custom method, or a **local-pickup / free / fixed** flat rate. Both kinds of method appear side-by-side at checkout — the customer sees them all as shipping options and picks one. Which model a method uses is decided when the method is created and cannot be switched without removing and re-adding the method.

The pricing model determines:

- Whether the merchant edits individual rate rows (custom) or accepts the carrier's tariff opaquely (integration).
- Whether the platform calls a remote API at checkout (integration) or looks up locally (custom).
- Whether the merchant picks a geographic scope (custom) or the carrier's API decides coverage (integration).

## Scope

Covered:

- Model 1: live API quote from carrier integrations.
- Model 2: merchant-defined rate rows (Based on price / weight / both).
- Model 3: Local Pickup / Free / Fixed.
- How the "Deliver to" column renders for each model.
- "Different price for categories" second rate table.

Not covered:

- The full filtering cascade (geo gating, customer-group filter, Cart Rules override) that decides which methods are *candidates* before pricing runs — see [[shipping-provider-mech-geo-routing]] and [[shipping-calc-cascade]].
- COD surcharge added on top of the priced line — see [[shipping-provider-mech-cod]].
- Multi-currency conversions at carrier-call time — see [[shipping-provider-mech-geo-routing]].

## Contrasts

- **Live API quote vs. merchant rate rows**: live quote is real-time, opaque, tracks the carrier's tariff automatically, requires valid credentials. Merchant rate rows are deterministic, transparent, editable, work offline. Carriers like Econt and Speedy use the live quote model; the merchant cannot override the prices the carrier returns.
- **Based on price vs. Based on weight vs. Based on price and weight**: three flavours of merchant rate rows. Price-based looks up by subtotal, weight-based by the cart's total physical weight, price-and-weight by both axes nested. Used in different logistics setups (e.g., heavy-furniture stores often use weight; standard retail often uses price).
- **Custom method vs. Local Pickup**: both are merchant-controlled, but Local Pickup is the *customer's* pickup from a physical store the merchant configured via [[apps-stores]] — there's no logistics network involved. A custom method's "Local Pickup" line at checkout reads "Local pickup from [Store Name]" with a typically-zero fee.

## Where it applies

### Model 1 — Live API quote (carrier integrations)

When a customer at checkout selects (or just lands on) a carrier-integration method, the platform calls the carrier's `getQuotes` API in real time with the package details (dimensions + weight + delivery channel + destination address) and the customer-selected COD / insurance amounts. The carrier returns one or more service options with its current tariff prices (e.g., Econt returns "To address tomorrow 6.50 BGN", "To Econtomat 4 BGN", "Same-day 12 BGN"). The customer's choice is stored on the cart.

The merchant **cannot edit individual rate rows** for an integration-backed method — the carrier's pricing is opaque to CloudCart. The integration just passes the carrier's number through to the customer.

The "Deliver to" column in [[settings-shipping]] shows *"Regions are determined by the provider"* for integration methods, reflecting that the carrier's API decides where it serves; the merchant doesn't define a Geo Zone for these.

### Model 2 — Merchant-defined rate rows (custom methods)

The merchant configures a Custom shipping method with one of three rate models:

- **Based on price** — rate rows are price brackets (`from` / `to` subtotal range → `amount`). At checkout the cart's subtotal looks up the matching row.
- **Based on weight** — rate rows are weight brackets (`from` / `to` weight range → `amount`). The cart's total weight (sum of product weights × quantities) looks up the matching row.
- **Based on price and weight** — nested brackets in both dimensions. Used for logistics partners that price on both axes.

The merchant adds rate rows with `from`, `to`, and `amount`. **Both bounds are inclusive, and a blank `to` means NO upper limit (the bracket runs to infinity) — not an invalid row.** So the standard top row is left with an empty upper bound on purpose, to catch every heavier/pricier cart; leaving it blank never hides the method. A row with `amount = 0` is effectively free shipping for that bracket. See [[shipping-calc-rate-models]] for the full lookup arithmetic (inclusive bounds, blank-bound semantics, and cheapest-row-wins on overlap). The merchant also picks a single geographic scope per method (whole world OR one [[settings-geo-zones]]) — see [[shipping-provider-mech-geo-routing]] for the geo gating mechanics.

Custom methods support a SECOND rate table scoped to specific product categories ("Different price for categories") — useful for "heavy furniture costs more to ship than other products" patterns. See [[shipping-calc-rate-models]] for the full lookup arithmetic.

### Model 3 — Local Pickup / Free / Fixed

- **Local Pickup (Marketplace)** — the customer picks a physical store location the merchant has configured. Available only when the Stores app is installed. The "shipping" line at checkout reads "Local pickup from [Store Name]" with a typically-zero pickup fee.
- **Free / Fixed flat rate** — a Custom method with one rate row covering the whole bracket at a fixed amount (often 0 for free shipping over a threshold).

### Default selection at checkout

The default shipping method auto-selected at the customer's checkout step is configured in [[settings-cart]] — NOT in [[settings-shipping]]. The setting picks both default shipping TYPE (carrier vs. custom) and default PROVIDER (specific carrier). When [[settings-cart]]'s *"Automatically select if only one is available"* toggle is ON and exactly one method matches the customer's cart, that method is pre-selected without showing the picker.

## Related

- [[shipping-provider-mechanism]] — hub.
- [[shipping-calculation]] — the full arithmetic of how the chosen line is computed.
- [[shipping-calc-rate-models]] — rate-row lookup logic (price brackets, weight brackets, nested both).
- [[shipping-calc-carrier-integrations]] — the integration-side variant of the cascade.
- [[settings-shipping]] — the methods hub where each method's pricing model is picked.
- [[shipping-provider-pricing-models]] — sister entity-side documentation of the same models.
- [[apps-stores]] — Stores app powering Local Pickup.
- [[settings-cart]] — default carrier + auto-select toggle.
- [[settings-boxes]] — package dimensions feeding live-quote weight / volumetric calculations.

## Open Questions

None.
