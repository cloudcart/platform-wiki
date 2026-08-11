---
type: feature
nav_path: "Apps → TCS Courier"
route_name: apps.tcscourier.overview
route_path: /admin/shipping/tcscourier
aliases: ["TCS Courier", "Tcscourier"]
tags: [apps, shipping, courier, greece, omniship]
plan_gates: []
created: 2026-05-22
updated: 2026-06-26
source_count: 4
---
# TCS Courier

## Purpose

**TCS Courier** integration — a Greek courier (API endpoint `tcs.evresis.gr`). Used by Greek-market CloudCart merchants who ship via TCS.

Like [[apps-speedex]] (the other "merchant-priced" Greek integration), TCS Courier does **NOT** return live rates from the courier API — the merchant sets pricing themselves with a fixed table, or mirrors another shipping method's price.

## Where to find it

Sidebar → Apps → install → **TCS Courier** OR direct routes. Standard OmniShip sub-pages.

Four sub-pages:

| Sub-page | Route name |
|----------|------------|
| Overview | `apps.tcscourier.overview` |
| Settings | `apps.tcscourier.settings` |
| Shipments | `apps.tcscourier.shipments` |
| Shipments return | `apps.tcscourier.shipments-return` |

## What the merchant can do here

- Install / activate / deactivate the integration.
- Configure credentials in the Settings sub-page.
- Pick a pricing model (fixed tiers or mirror another method — TCS API does not return rates).
- Generate waybills + print labels per order.
- View / manage waybills in the Shipments sub-page.
- Manage returns in the Shipments return sub-page.

### What the merchant CANNOT do here
- Get a real-time rate quote from TCS Courier's API — TCS pricing is merchant-defined.
- Use locker / office channels — door-to-door (`address`) only.
- Use the integration without TCS Courier credentials.

## Settings & fields

### Credentials card

| Field | Notes |
|-------|-------|
| **Username** (`username`) | TCS API username — required. |
| **Password** (`password`) | TCS API password (masked) — required. |
| **Account Type** (`test_mode`) | Test Account / Real Account dropdown. Both modes currently point to `tcs.evresis.gr/rest3/`; the flag controls credential routing only. |

### Additional Settings box (`general_settings`)

| Field | Notes |
|-------|-------|
| **Enable cash on delivery** (`cd`) | Switch — when ON, COD is offered for orders within the COD cap. |
| **Default weight for one item** (`default_weight`) | Number — fallback weight when product weight is missing. |

Pricing model is configured PER service-type via the service-type calculator modal, not in the Additional Settings box.

### Required-field validation messages
- *"Username is required"*, *"Password is required"*.
- *"Select shipping methods"* — appears when the merchant picks "Based on other delivery method" without selecting any source method.

### Waybill validation messages
- *"Please enter the shipment weight."* / *"The weight must be a number."* / *"The weight cannot be negative."*
- *"When cash on delivery is selected, you must enter an amount."* / *"The cash on delivery amount must be a number."* / *"The cash on delivery amount must be a positive number."*
- *"The order does not exist or has been deleted."*
- *"The order is not configured for TCS Courier delivery."*
- *"A waybill cannot be issued for an archived order."*
- *"The order has no shipping address. Please add an address before generating a waybill."*
- *"The order does not contain any physical products for which a waybill can be issued."*
- *"The order already has a waybill. Please cancel it first if you want to issue a new one."*
- *"Cash on delivery cannot be enabled on an order that is already paid or completed."*

## Business rules

### Pricing model — merchant-defined, not from courier API
TCS Courier supports three pricing models (the merchant picks one):

- **Fixed price** (`fixed_price`) — one flat price per cart-value tier.
- **Fixed value by weight** (`fixed_weight`) — flat price per weight tier.
- **Fixed value by price and weight** (`price_and_weight`) — combined flat rules.

There is no live-quote mode like the carrier-priced couriers (Econt, Speedy/DPD Bulgaria, GLS). The TCS API IS still called for waybill creation and credential validation — just not for rate calculation at checkout.

### Address channel only
Supported delivery channels = `['address']`. No locker / office pickup.

### Default RECEIVER pays
The default `side` setting is `PAYER_RECEIVER` — the customer pays the courier fee (consistent with the Greek COD market).

### COD supported with cap
COD is enabled when `cd` is ON AND the order is within the COD cap. For EUR stores no platform-side cap applies — TCS server-side limits decide.

### COD + recalculate-on-payment-change
When COD is enabled, switching the customer's payment method on the order (COD ↔ online) triggers a shipping cost recalculation.

### No country whitelist — TCS API + merchant geo zones decide
The integration has no hard-coded country list. The platform delegates the destination to the courier; outside Greece (the courier's market) no waybill option will appear. The merchant's geo-zone configuration on the shipping provider also constrains where TCS shows up at checkout.

### Side effects
Saving Settings validates credentials against `tcs.evresis.gr`. Waybill creation calls TCS's API (`store` endpoint); errors surface to the merchant on the waybill form. COD amounts use the field name `antikposo` in the API payload (Greek for COD).

### Permission
Standard apps permission scope.

## Settings page — full layout (shared OmniShip form + custom credentials)

TCS Courier uses `SettingsFormShippings` with a custom **`#credentials` slot**:

### Credentials card (custom — `CourierCredentialsSection.vue`)
| Field | Input | Required | Notes |
|-------|-------|----------|-------|
| TCS courier's username (`username`) | Text | Yes | Error: "Invalid credentials". |
| TCS courier's password (`password`) | PasswordInput (masked, eye toggle) | Yes | Error: "Invalid credentials". |
| Account type (`test_mode`) | Select | — | Options: `Test Account` (1) / `Real Account` (0). Both currently route to `tcs.evresis.gr/rest3/`; flag is a forward-compatibility toggle. |

`Connect` button → POSTs to validate; the rest of the form slides in on success.

### Remaining shared sections
- **Visualization** — courier display name + logo upload.
- **Service-type cards** — `address` only. Pencil opens the **Service-type calculator modal** with the 3 fixed pricing modes (Fixed price, Fixed weight, Price+weight) — NO calculator mode since TCS doesn't quote.
- **Ships to (Geo Zones)** — geo-zone allow-list.
- **Payment providers** — payment method multi-select.
- **Additional Settings box** — only two fields: `cd` (cash on delivery) + `default_weight`. There is NO insurance field and NO payer-side selector here.

## Per-channel delivery pricing

TCS Courier delivers to **address** — the single **address** channel is a separate rate card with its own enable toggle (`to_address`) and a **Delivery price calculation** type. When the merchant picks a type, the rate card reveals these fields:

- `fixed_price` — a **Fixed value by price** rate table: rows keyed by **cart subtotal** (`from` / `to` / `amount`); the courier quote is ignored.
- `fixed_weight` — a **Fixed value by weight** rate table: rows keyed by **total weight**.
- `price_and_weight` — a combined table keyed by **both cart subtotal and weight**.

Each `fixed_*` type's table **is** the price (there is no live calculator on TCS Courier, so no fallback). **Every** type also adds a **per-category** sub-table ("Set different pricing conditions for products in category/ies") for charging chosen categories differently. Full field mechanics + rate-row semantics: [[shipping-calc-rate-card-fields]] and [[shipping-calc-rate-models]].

## Related

- [[shipping-calc-rate-models]] — rate-table semantics: when a method uses a from/to rate table (по тегло / по цена), an **empty upper bound (`до` / `to`) means no upper limit — the bracket runs to infinity** (both bounds inclusive). A blank top row is intended, not invalid, and never hides the method at checkout.
- [[apps]] — App Store.
- [[apps-speedex]] — sister Greek courier (also merchant-priced).
- [[apps-acscourier]] — Greek courier with live API quotes.
- [[shipping]] — shipping landing.
- [[orders-shipping-waybill]] — waybill flow.

## Open questions

_None — coverage clarified above._
