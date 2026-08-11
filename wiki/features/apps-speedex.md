---
type: feature
nav_path: "Apps → Speedex"
route_name: apps.speedex.overview
route_path: /admin/shipping/speedex
aliases: ["Speedex", "Speedex Greece", "Speedex courier"]
tags: [apps, shipping, courier, greece, omniship]
plan_gates: []
created: 2026-05-22
updated: 2026-06-26
source_count: 5
---
# Speedex (Greece)

## Purpose

**Speedex** integration — Greek courier alongside [[apps-acscourier]]. Used by Greek merchants for domestic delivery (and Cyprus via the same contract). The integration connects to Speedex's Greek API (`spdxws.gr`).

Unlike most OmniShip couriers (Econt, Speedy, GLS), Speedex does **NOT** quote rates from its API. The merchant configures pricing themselves — either as fixed price tiers, or by mirroring the price of OTHER shipping methods already set up in the store ("based on other delivery method").

## Where to find it

Sidebar → Apps → install → **Speedex** OR direct routes. Standard OmniShip sub-pages.

Four sub-pages:

| Sub-page | Route name |
|----------|------------|
| Overview | `apps.speedex.overview` |
| Settings | `apps.speedex.settings` |
| Shipments | `apps.speedex.shipments` |
| Shipments return | `apps.speedex.shipments-return` |

## What the merchant can do here

- Install / activate / deactivate the integration.
- Configure credentials in the Settings sub-page.
- Choose a pricing model (Speedex does NOT return live rates — see below).
- Generate waybills + print labels from each order.
- View / manage generated waybills in the Shipments sub-page.
- Manage returns in the Shipments return sub-page.

### What the merchant CANNOT do here
- Get a real-time price from Speedex's API — Speedex has no rate calculator endpoint in this integration; pricing is merchant-defined.
- Use locker / Speedex office channels — door-to-door (`address`) is the only supported channel.
- Use the integration without an active Speedex contract (four credentials must be valid).
- Quote shipments for destinations outside Greece (the API only returns a quote when the receiver country is `GR`).

## Settings & fields

### Credentials card

| Field | Input | Notes |
|-------|-------|-------|
| **Username** (`username`) | Text | Required. Error on bad login: "Invalid credentials". |
| **Password** (`password`) | Masked (eye toggle) | Required. Error on bad login: "Invalid credentials". |
| **Customer ID** (`customer_id`) | Text | Required. |
| **Agreement ID** (`agreement_id`) | Text | Required. |
| **Account type** (`test_mode`) | Select | `Test Account` (1) / `Real Account` (0). Routes credential validation to `devspdxws.gr` vs `spdxws.gr`. |

A **Connect** button validates the credentials. On success the card collapses and the rest of the form slides into view.

### Other shared form sections
- **Visualization** — courier display name + logo upload.
- **Service-type cards** — only the `address` channel. The pencil opens the **Service-type calculator modal**, where the pricing model is configured (see "Pricing model" under Business rules).
- **Ships to (Geo Zones)** — geo-zone allow-list.
- **Payment providers** — payment-method multi-select.

### Additional Settings box (`general_settings`)

| Field | Notes |
|-------|-------|
| **Default weight for one item** (`default_weight`) | Number, used when a product has no weight. Default `0.1` kg. |
| **Enable cash on delivery** (`cd`) | Switch — when ON, COD is offered for orders within the COD cap. |
| **Insurance** (`insurance`) | Switch — when ON, declared-value insurance can be added per shipment. |

Pricing model is configured per service-type via the service-type calculator modal (see "Pricing model" under Business rules), not in the Additional Settings box. The Additional Settings box has only these three fields — there is NO payer-side selector here.

### Required-field validation messages
- *"Username is required"*, *"Password is required"*.
- *"Agreement number is required"*, *"Customer ID is required"*.
- *"Select shipping methods"* — appears when the merchant picks "Based on other delivery method" without selecting any source method.

### Waybill validation messages
- *"Please enter the shipment weight."* / *"The weight must be a number."* / *"The weight cannot be negative."*
- *"Please enter the number of packages."* / *"The number of packages must be a whole number."* / *"The number of packages must be at least 1."* / *"The number of packages cannot exceed 100."*
- *"When cash on delivery is selected, you must enter an amount."* / *"The cash on delivery amount must be a number."* / *"The cash on delivery amount must be a positive number."*
- *"When insurance is selected, you must enter an insurance value."* / *"The insurance value must be a number."* / *"The insurance value must be a positive number."*
- *"The order does not exist or has been deleted."*
- *"The order is not configured for Speedex delivery."*
- *"A waybill cannot be issued for an archived order."*
- *"The order has no shipping address. Please add an address before generating a waybill."*
- *"The order does not contain any physical products for which a waybill can be issued."*
- *"The order already has a waybill. Please cancel it first if you want to issue a new one."*
- *"Cash on delivery cannot be enabled on an order that is already paid or completed."*

## Business rules

### Pricing model — no live quotes from Speedex
This is the key difference from other OmniShip couriers. Speedex offers four pricing models the merchant picks ONE of:

- **Based on other delivery method** (`calculator`) — Speedex's quote = the quote of OTHER shipping methods the merchant has set up. The merchant picks WHICH source methods (`Select shipping methods`); Speedex piggy-backs on each one's calculation. Common pattern: mirror an internal flat-rate table.
- **Fixed price without Speedex calculator** (`fixed_price`) — one flat price per cart-value tier.
- **Fixed value by weight without Speedex calculator** (`fixed_weight`) — flat price per weight tier.
- **Fixed value by price and weight** (`price_and_weight`) — combined flat rules.

Fixed modes use rate rows (weight from/to → price, or price from/to → price). The calculator modal also offers allowed-countries / allowed-categories restrictions. Speedex's API IS still called for waybill creation / credential validation — just not for pricing.

### Greek + Cyprus coverage
The integration returns quotes only when the receiver address has country ISO `GR`. Cyprus is reached via the same Speedex contract — depending on contract setup, Cyprus shipments use the same API endpoint. Outside Greece (and Cyprus per contract), no Speedex option appears at checkout.

### Default RECEIVER pays — typical for Greek COD market
The default `side` setting is `PAYER_RECEIVER` — the customer pays the courier fee (common in Greece's COD-heavy retail). The merchant can override to `PAYER_SENDER` per shipment or globally.

### COD supported with the OmniShip-family cap check
COD is enabled when `cd` is ON AND the order is within the COD cap. EUR stores have no platform-side cap — Speedex's server-side limits apply.

### Address channel only
Supported delivery channels = `['address']`. No locker / office pickup. Speedex's own pickup-point network is not exposed by this integration.

### Insurance follows the COD cap
The "Amount of insurance" feature is gated by `insurance` setting AND the COD cap — same amount-range check as for COD.

### COD + recalculate-on-payment-change
When COD is enabled, switching the customer's payment method on the order (COD ↔ online) triggers a shipping cost recalculation.

### Side effects
Saving Settings validates credentials against `spdxws.gr` (or the test endpoint). Generating a waybill calls Speedex's API; failures surface as the API's error description on the waybill form.

### Permission
Standard apps permission scope.

## Per-channel delivery pricing

Speedex delivers to **address** — the single **address** channel is a separate rate card with its own enable toggle (`to_address`) and a **Delivery price calculation** type. When the merchant picks a type, the rate card reveals these fields:

- `calculator` — the real-time Speedex quote; **no extra field** of its own.
- `fixed_price` — a **Fixed value by price** rate table: rows keyed by **cart subtotal** (`from` / `to` / `amount`); the courier quote is ignored.
- `fixed_weight` — a **Fixed value by weight** rate table: rows keyed by **total weight**.
- `price_and_weight` — a combined table keyed by **both cart subtotal and weight**.

The calculator-based types also expose an optional **Fallback price** rate table, used only when the live quote can't return a price; the `fixed_*` types need no fallback (their table **is** the price). **Every** type also adds a **per-category** sub-table ("Set different pricing conditions for products in category/ies") for charging chosen categories differently. Full field mechanics + rate-row semantics: [[shipping-calc-rate-card-fields]] and [[shipping-calc-rate-models]].

## Related

- [[shipping-calc-rate-models]] — rate-table semantics: when a method uses a from/to rate table (по тегло / по цена), an **empty upper bound (`до` / `to`) means no upper limit — the bracket runs to infinity** (both bounds inclusive). A blank top row is intended, not invalid, and never hides the method at checkout.
- [[apps]] — App Store.
- [[apps-acscourier]] — alternative Greek courier.
- [[shipping]] — shipping landing.
- [[orders-shipping-waybill]] — waybill flow.
- [[orders-sync-cod]] — COD reconciliation.

## Open questions

_None — pricing model + coverage clarified above._
