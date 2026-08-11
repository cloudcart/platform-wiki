---
type: feature
nav_path: "Apps → Albanian Courier"
route_name: apps.albanian_courier.overview
route_path: /admin/shipping/albanian_courier
aliases: ["Albanian Courier", "Albania courier"]
tags: [apps, shipping, courier, albania, omniship]
plan_gates: []
created: 2026-05-22
updated: 2026-05-28
source_count: 4
---
# Albanian Courier

## Purpose

**Albanian Courier** integration — courier service for Albanian merchants. Used by CloudCart stores operating in Albania.

## Where to find it

Sidebar → Apps → install → **Albanian Courier** OR direct routes. Standard OmniShip sub-pages.

## What the merchant can do here

- Install / activate / deactivate the integration.
- Configure credentials in the Settings sub-page.
- View generated waybills / shipments in the Shipments sub-page.
- Manage returns in the Shipments return sub-page.
- See real-time quotes at checkout once credentials are validated.

### What the merchant CANNOT do here
- Use the integration without an active courier contract + valid API credentials.
- Generate waybills for destinations the courier does not serve.

## Settings & fields

| Field | Notes |
|-------|-------|
| **Username** | API username. |
| **Password** | API password. |
| **Client ID** | Customer identifier. |

### Send method

| Value | Meaning |
|-------|---------|
| **D2D** | Address to address (door-to-door, the default). |
| **P2D** | Office to address (pickup-to-door). |

### Pricing models

The merchant picks ONE pricing model per shipping rate:

- **Albanian Courier calculator** — live API quote.
- **Albanian Courier calculator + handling fee** — API quote plus a fixed processing fee.
- **Albanian Courier calculator + free shipping** — API quote zeroed out for the customer.
- **Fixed price without Albanian Courier calculator** — flat price tier per order subtotal.
- **Fixed value by weight without Albanian Courier calculator** — flat price tier per weight.
- **Fixed value by price and weight without Albanian Courier calculator** — combined matrix.

## Business rules

Standard OmniShip pattern. Albania-focused (lekë / EUR quoting).

## Per-channel delivery pricing

Albanian courier delivers to **address** — the single **address** channel is a separate rate card with its own enable toggle (`to_address`) and a **Delivery price calculation** type. When the merchant picks a type, the rate card reveals these fields:

- `calculator` — the real-time Albanian Courier quote; **no extra field** of its own.
- `calculator_fixed` — the Albanian Courier quote **plus a fixed fee** you enter in the **Parcel processing Fee** field (`fixed_price_<channel>`).
- `free` — the Albanian Courier quote, but **free above a threshold** you set in **Minimum Order Value for Free Delivery** (`free_shipping_total_<channel>`); below it the customer pays the quote.
- `fixed_price` — a **Fixed value by price** rate table: rows keyed by **cart subtotal** (`from` / `to` / `amount`); the courier quote is ignored.
- `fixed_weight` — a **Fixed value by weight** rate table: rows keyed by **total weight**.
- `price_and_weight` — a combined table keyed by **both cart subtotal and weight**.

The calculator-based types also expose an optional **Fallback price** rate table, used only when the live quote can't return a price; the `fixed_*` types need no fallback (their table **is** the price). **Every** type also adds a **per-category** sub-table ("Set different pricing conditions for products in category/ies") for charging chosen categories differently. Full field mechanics + rate-row semantics: [[shipping-calc-rate-card-fields]] and [[shipping-calc-rate-models]].

## Related

- [[shipping-calc-rate-models]] — rate-table semantics: when a method uses a from/to rate table (по тегло / по цена), an **empty upper bound (`до` / `to`) means no upper limit — the bracket runs to infinity** (both bounds inclusive). A blank top row is intended, not invalid, and never hides the method at checkout.
- [[apps]] — App Store.
- [[shipping]] — shipping landing.
- [[orders-shipping-waybill]] — waybill flow.

## How it works (verified against backend)

### Address-only

Door delivery only. No locker or office channels exposed.

### COD support

COD is enabled when the merchant's COD setting is on AND the order is within the COD cap. For non-BGN stores (typical for Albania — ALL / EUR), there is no platform-side amount cap; the courier's server-side limit applies. Currency conversion to the destination currency happens at API-call time.

### Default: receiver pays, D2D mode

Default payer is the receiver (customer pays courier — typical for COD markets) and the default send method is D2D (door-to-door).

### No country whitelist — courier API decides coverage

No platform-side country restriction. Whether a destination (Albania, Kosovo, North Macedonia, etc.) is quotable depends on the merchant's contract + the courier's API response.

### Six pricing models including calculator

Six pricing types are supported — calculator, calculator + handling fee, calculator + free shipping, fixed price, fixed weight, and price+weight — covering both live-rate pricing and merchant-defined rate tables.

## Settings page — full layout (shared OmniShip form + custom credentials)

Albanian Courier uses `SettingsFormShippings` with a custom **`#credentials` slot**:

### Credentials card (custom — `CourierCredentialsSection.vue`)
| Field | Input | Required | Notes |
|-------|-------|----------|-------|
| Username (`username`) | Text (`column-style`) | Yes | Error: "Invalid credentials" |
| Password (`password`) | PasswordInput (masked, eye toggle) | Yes | Error: "Invalid credentials" |
| Client ID (`client_id`) | Text | Yes | Error: "Invalid credentials" |

`Connect` button → validates; on success the rest of the form slides in.

### Remaining shared sections
- **Visualization** — courier display name + logo upload.
- **Service-type cards** — `address` only. Pencil opens the **Service-type calculator modal** with the 6 pricing modes (calculator, calculator + handling fee, calculator + free, fixed price, fixed weight, price+weight) + rate rows + countries + categories.
- **Ships to (Geo Zones)** — geo-zone allow-list.
- **Payment providers** — payment method multi-select.
- **Additional Settings box** (`general_settings`) — actual fields in order:
  - **Who pay the shipping cost** (`side`) — radio.
  - **Enable cash on delivery** (`cd`) — switch.
  - **Send Method** (`method_send`) — select: `D2D` (Address to address) / `P2D` (Office to address).
  - **Default weight for one item** (`default_weight`) — required.

## Open questions
