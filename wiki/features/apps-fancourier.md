---
type: feature
nav_path: "Apps → FanCourier"
route_name: apps.fancourier.overview
route_path: /admin/shipping/fancourier
aliases: ["FanCourier", "Fan Courier", "Fan Courier Romania"]
tags: [apps, shipping, courier, romania, omniship]
plan_gates: []
created: 2026-05-22
updated: 2026-05-28
source_count: 4
---
# FanCourier (Romania)

## Purpose

**FanCourier** integration — another major Romanian courier alongside [[apps-sameday]], [[apps-cargus]], and [[apps-dpdromania]]. Strong nationwide RO coverage with home delivery + pickup-point network.

## Where to find it

Sidebar → Apps → install → **FanCourier** OR direct routes.

FanCourier exposes FOUR sub-pages (no Payments tab — different from Econt / DPD):

| Sub-page | Route name | Path |
|----------|------------|------|
| Overview | `apps.fancourier.overview` | `/admin/shipping/fancourier/` |
| Settings | `apps.fancourier.settings` | `/admin/shipping/fancourier/settings` |
| Shipments | `apps.fancourier.shipments` | `/admin/shipping/fancourier/shipments` |
| Shipments return | `apps.fancourier.shipments-return` | `/admin/shipping/fancourier/shipments-return` |

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
| **Username** | FanCourier API username. |
| **Password** | FanCourier API password. |
| **Client ID** | FanCourier customer ID. |

## Business rules

### RO-focused

Single-country (Romania). Quotes in RON.

### COD supported

Standard COD flow via [[orders-sync-cod]].

### Same OmniShip pattern

Real-time quotes → bill-of-lading → tracking.

## Per-channel delivery pricing

FAN Courier delivers to **address**, to **office** and to **locker** — each of its **3** delivery channels (to **address**, to **office** and to **locker**) is a separate rate card with its own enable toggle (`to_address` / `to_office` / `to_locker`) and a **Delivery price calculation** type. When the merchant picks a type, the rate card reveals these fields:

- `calculator` — the real-time Fan Courier quote; **no extra field** of its own.
- `calculator_fixed` — the Fan Courier quote **plus a fixed fee** you enter in the **Parcel processing Fee** field (`fixed_price_<channel>`).
- `free` — the Fan Courier quote, but **free above a threshold** you set in **Minimum Order Value for Free Delivery** (`free_shipping_total_<channel>`); below it the customer pays the quote. It also adds **Free Delivery Service within the City** and **Intercity** selects that pick which Fan Courier service fulfils the free leg.
- `fixed_price` — a **Fixed value by price** rate table: rows keyed by **cart subtotal** (`from` / `to` / `amount`); the courier quote is ignored.
- `fixed_weight` — a **Fixed value by weight** rate table: rows keyed by **total weight**.
- `price_and_weight` — a combined table keyed by **both cart subtotal and weight**.

The calculator-based types also expose an optional **Fallback price** rate table, used only when the live quote can't return a price; the `fixed_*` types need no fallback (their table **is** the price). **Every** type also adds a **per-category** sub-table ("Set different pricing conditions for products in category/ies") for charging chosen categories differently. Full field mechanics + rate-row semantics: [[shipping-calc-rate-card-fields]] and [[shipping-calc-rate-models]].

## Related

- [[shipping-calc-rate-models]] — rate-table semantics: when a method uses a from/to rate table (по тегло / по цена), an **empty upper bound (`до` / `to`) means no upper limit — the bracket runs to infinity** (both bounds inclusive). A blank top row is intended, not invalid, and never hides the method at checkout.
- [[apps]] — App Store.
- [[apps-sameday]] / [[apps-cargus]] / [[apps-dpdromania]] — alternative RO couriers.
- [[shipping]] — shipping landing.
- [[orders-shipping-waybill]] — waybill flow.
- [[orders-sync-cod]] — COD sync.

## How it works (verified against backend)

### Romania-ONLY

The fallback allowed countries list is `['RO']` — Romanian-only courier.

### Three delivery channels

Supported delivery channels are `['address', 'office', 'locker']` — full 3-channel support (address, office pickup, locker).

### 3 required credentials

Three credential fields: Username, Password, Client ID — heavier than the 2-credential providers (Cargus, Econt, Speedy, DPD Bulgaria, DPD Romania, all of which use just username + password) but lighter than BoxNow's `client_id + client_secret + partner_id` triple or DHL's 5-credential stack.

### Default — receiver pays

Default settings: receiver-pays (typical RO COD pattern — customer pays courier), door delivery enabled by default, real-time calculator pricing, 0.1 kg default weight when products lack a configured weight. Same architecture as Cargus + DPD Romania defaults.

### Per-setting channel toggles

Each channel (Address, Office, Locker) has its own enable toggle in settings.

### COD supported with same family rules

COD support is the standard OmniShip family check (merchant's COD toggle + amount cap). For non-BGN store currencies (typical for Romania), there's no platform-side cap on COD amount; FanCourier's server-side limits still apply.

### COD + recalculate-on-payment-change

When the merchant switches the customer's payment method on an order with FanCourier shipping, shipping cost recalculates — FanCourier's COD fee disappears when payment moves online.

### Three pickup-point types — office + locker + address

FanCourier covers door delivery, pickup from FanCourier offices, and locker pickup. Available offices and lockers come from FanCourier's API after the merchant saves credentials; the merchant enables the channels their contract includes via the "Allowed methods" picker.

### Service tier list comes from FanCourier's API

The integration doesn't hardcode service tiers (Standard / Express). Available services are fetched from FanCourier's API and exposed in the "Allowed methods" picker; only the tiers the merchant's contract supports appear at checkout.

## Settings tab — full layout (deep audit 2026-05-27)

### 1. Credentials box (custom `CourierCredentialsSection.vue`)
Three required fields:
- **Client ID** (`client_id`) — text input. Required.
- **Password** (`password`) — masked. Required.
- **Username** (`username`) — text input. Required.

On Save the platform validates credentials against FanCourier's API; failure shows "Invalid credentials" inline on all three fields. "Connect" button until validated.

### 2. Name & logo (Visualization)

### 3. Sender data box — slide-down editor (`SenderDataSection.vue`)
- **Sender name** (`sender_name`) — single input, full width. No phone/address/office fields exposed here — FanCourier doesn't surface a full sender form, just the sender label.

Pickup keys: `sender_name`.

### 4. Services
- Multi-tag select (FanCourier services); rendered only when the provider supports `services` AND providerKey ≠ sameday. Tier list comes from FanCourier's API.

### 5. Per-channel rate cards (address / office / locker)
Standard three-channel modals with full pricing-mode options. When `pricingType = free` the city / intercity / international service selectors appear (FanCourier is in the courier whitelist that exposes these).

### 6. Geo zones / 7. Payment providers — standard.

### 8. Additional settings — two boxes (backend-driven)

#### Box 1 — `general_settings`
- **Default weight for one item** (`default_weight`).
- **Default width / length / height** (mm).
- **Choose a content description** (`order_content`) — Product name / SKU / barcode.

#### Box 2 — `parcel_and_waybill_settings` (inline edit)
- **Who pay the shipping cost** (`side`) — radio.
- **Enable cash on delivery** (`cd`) — switch.
- **Declared value of the shipment** (`insurance`) — switch.
- **Saturday delivery** (`saturday_delivery`) — switch.
- **ePOD** (`epod`) — switch (electronic proof-of-delivery service).
- **Options before payment** (`option_before_payment`) — switch.

### 9. Submit-changes sticky footer.

## Shipments / Shipments return tabs
Shared `Shipments.vue`. Bulk-print goes through `PrintFormatSelectModal` (A4/A6).

## Overview tab — standard.

## No Payments tab
FanCourier's Vue router does NOT mount a Payments sub-page.

## Open questions
