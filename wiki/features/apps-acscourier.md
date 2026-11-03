---
type: feature
nav_path: "Apps → ACS Courier"
route_name: apps.acscourier.overview
route_path: /admin/shipping/acscourier, /admin/shipping/acscourier/settings, /admin/shipping/acscourier/pickuplist, /admin/shipping/acscourier/history, /admin/shipping/acscourier/shipments, /admin/shipping/acscourier/shipments-return
aliases: ["ACS Courier", "ACS Greece", "ACS courier", "ACS Smartpoint", "ACS pickup station", "ACS billing code", "ACS Гърция", "Куриер ACS"]
tags: [apps, shipping, courier, greece, omniship]
plan_gates: []
created: 2026-05-22
updated: 2026-11-03
source_count: 5
---
# ACS Courier (Greece)

## Purpose

**ACS Courier** integration — the largest privately-owned courier in Greece (owned by Quest Holdings). It ships within Greece, following the standard OmniShip flow: quotes → bill-of-lading → tracking via [[orders-shipping-waybill]].

## Where to find it

Sidebar → Apps → install → **ACS Courier**, then open its sub-pages directly. The integration exposes six sub-pages:

| Sub-page | Route name | Path |
|----------|------------|------|
| Overview | `apps.acscourier.overview` | `/admin/shipping/acscourier/` |
| Settings | `apps.acscourier.settings` | `/admin/shipping/acscourier/settings` |
| **Pickup list** | `apps.acscourier.pickuplist` | `/admin/shipping/acscourier/pickuplist` |
| **History** | `apps.acscourier.history` | `/admin/shipping/acscourier/history` |
| Shipments | `apps.acscourier.shipments` | `/admin/shipping/acscourier/shipments` |
| Shipments return | `apps.acscourier.shipments-return` | `/admin/shipping/acscourier/shipments-return` |

**Pickup list** and **History** are ACS-specific extra tabs (only Econt/Evropat also adds a custom tab — Addresses). ACS does **not** expose a Payments sub-page (unlike Econt / DPD).

## What the merchant can do here

- Install / activate / deactivate the integration.
- Configure credentials, sender data, rates and add-ons in the Settings sub-page.
- See real-time quotes at checkout once credentials are validated.
- Generate the daily **Pickup list** the merchant hands to the ACS driver, and review past lists under **History**: [[apps-acscourier-pickup-vouchers]].
- View / bulk-print generated waybills on the Shipments sub-page (A4/A6 print-format choice).
- Manage returns on the Shipments return sub-page.

### What the merchant CANNOT do here
- Use the integration without an active ACS contract + valid API credentials.
- Generate waybills for destinations the courier does not serve.

## Settings & fields

### 1. Credentials — six fields (most complex credential set of any CloudCart courier)

| Field | Setting key | Notes |
|-------|-------------|-------|
| **Company ID** | `company_id` | ACS company identifier. Required. |
| **Company password** / *Парола на фирмата* | `company_password` | Company-level password (different from user password). Masked. Required. |
| **Username** | `username` | Per-user API username. Required. |
| **User password** / *Парола на потребителя* | `password` | Per-user API password. Masked. Required. |
| **API key** | `key` | Integration secret issued by ACS. Required. |
| **Billing code** | `billing_code` | ACS billing reference. Carries the ACS store: it starts with 2 then the store code, e.g. `2ΑΘ123456`. Required. |

Company ID + Company password authenticate the merchant's organisation; Username + User password authenticate the API user under it.

**Pickup station**, shown under the Billing code field: *"ACS prices and picks up your parcels from this store. It comes from the billing code."* An unknown code is refused on Connect and Save: *"This billing code does not match an ACS store"*, *"ACS billing codes start with 2 and the code of your ACS store, e.g. 2ΑΘ123456."* Quotes and vouchers start from this station; the sender city and zip are only a fallback.

### 2. Name & logo (Visualization)

### 3. Sender data box (slide-down editor)
- **Sender name** (`sender_name`) — required.
- **Location of sender** (`input_city`) — text input. Required.
- **Postal code of the settlement** (`input_zipcode`) — text input. Required.

### 4–5. Services / per-channel rate cards
ACS supports two delivery channels — **address** (door) and **office** (pickup). Smartpoint / locker points are offered in the office channel. An office destination uses the office's own station. Standard rate cards per channel.

### 6–7. Geo zones / Payment providers — standard.

### 8. Additional settings — three boxes

**Box 1 — `general_settings`**
- **Add a default weight** (`default_weight`) — required.
- **Default width / length / height** (mm).
- **Choose a content description** (`order_content`).

**Box 2 — `parcel_and_waybill_settings`** (inline edit)
- **Who pay the shipping cost** (`side`) — radio.
- **Enable cash on delivery** (`cd`) — switch.
- **Insurance** (`insurance`) — switch (with declared amount).
- **Saturday delivery** (`saturday`) — switch.
- **Back documents request** (`documents`) — switch.
- **Require a protocol** (`protocol`) — switch.

**Box 3 — `services_addition_settings`**
- **Default service name to address** (`service_name_to_address`) — free-text string. The exact ACS service-tier label sent with address-delivery waybills (e.g., "ACS Express").
- **Default service name to office** (`service_name_to_office`) — free-text string. The exact label sent with office-delivery waybills.

### Pricing models

The merchant picks ONE pricing model per shipping rate:

- **AcsCourier calculator** — live API quote at checkout.
- **AcsCourier calculator + processing fee** — API quote plus a fixed processing fee.
- **AcsCourier calculator + free shipping** — API quote zeroed out for the customer.
- **Fixed value at price without AcsCourier calculator** — flat price tier per order subtotal.
- **Fixed value by weight without AcsCourier calculator** — flat price tier per package weight.
- **Fixed value for price and weight without AcsCourier calculator** — combined price + weight matrix.

## Business rules

### Greece coverage
The integration ships within Greece: the allowed country is GR, the office lists hold Greek points, and quotes are in EUR.

### Table prices survive an ACS error
When ACS returns an error, `fixed_price`, `fixed_weight` and `price_and_weight` still quote from their tables, so the method stays at checkout. A zero-price answer gives no quote.

### Service names must match the ACS contract
The two service-name strings in Box 3 are free text. The merchant must type the exact ACS service-tier names matching their contract (e.g., "ACS Express", "ACS Saturday Delivery"). Wrong names cause ACS to **reject the waybill**.

### Cash on delivery
COD is enabled when the merchant's COD setting is on AND the order is within the configured cap. For non-BGN stores (EUR for GR) there is no platform-side cap. Switching payment method on an order with ACS shipping triggers a shipping-cost recalculation while COD is active.

### Pickup list and vouchers

The daily pickup list, voucher rules, deleting and insurance: [[apps-acscourier-pickup-vouchers]].

### Lists refresh on their own

Offices refresh daily and cities weekly, when a store loads or saves its ACS settings.

## Per-channel delivery pricing

ACS Courier delivers to **address** and to **office** — each of its **2** delivery channels (to **address** and to **office**) is a separate rate card with its own enable toggle (`to_address` / `to_office`) and a **Delivery price calculation** type. When the merchant picks a type, the rate card reveals these fields:

- `calculator` — the real-time ACS Courier quote; **no extra field** of its own.
- `calculator_fixed` — the ACS Courier quote **plus a fixed fee** you enter in the **Parcel processing Fee** field (`fixed_price_<channel>`).
- `free` — the ACS Courier quote, but **free above a threshold** you set in **Minimum Order Value for Free Delivery** (`free_shipping_total_<channel>`); below it the customer pays the quote.
- `fixed_price` — a **Fixed value by price** rate table: rows keyed by **cart subtotal** (`from` / `to` / `amount`); the courier quote is ignored.
- `fixed_weight` — a **Fixed value by weight** rate table: rows keyed by **total weight**.
- `price_and_weight` — a combined table keyed by **both cart subtotal and weight**.

The calculator-based types also expose an optional **Fallback price** rate table, used only when the live quote can't return a price; the `fixed_*` types need no fallback (their table **is** the price). **Every** type also adds a **per-category** sub-table ("Set different pricing conditions for products in category/ies") for charging chosen categories differently. Full field mechanics + rate-row semantics: [[shipping-calc-rate-card-fields]] and [[shipping-calc-rate-models]].

## Related

- [[shipping-calc-rate-models]] — rate-table semantics: when a method uses a from/to rate table (по тегло / по цена), an **empty upper bound (`до` / `to`) means no upper limit — the bracket runs to infinity** (both bounds inclusive). A blank top row is intended, not invalid, and never hides the method at checkout.
- [[apps-acscourier-pickup-vouchers]] — pickup list and voucher rules.
- [[apps]] — App Store.
- [[apps-speedex]] — alternative Greek courier.
- [[shipping]] — shipping landing.
- [[orders-shipping-waybill]] — waybill flow.

## Open questions
