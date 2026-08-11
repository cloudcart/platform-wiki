---
type: feature
nav_path: "Apps → Cargus"
route_name: apps.cargus.overview
route_path: /admin/shipping/cargus
aliases: ["Cargus", "Urgent Cargus", "Cargus courier", "Cargus Romania"]
tags: [apps, shipping, courier, romania, omniship]
plan_gates: []
created: 2026-05-22
updated: 2026-05-28
source_count: 3
---
# Cargus (Romanian courier)

## Purpose

**Urgent Cargus** integration — one of Romania's major courier services (alongside [[apps-sameday]] and the country-specific [[apps-dpdromania]]). Cargus focuses on traditional courier delivery (home + office), with strong nationwide RO coverage. Through CloudCart's OmniShip layer the Cargus app provides real-time quotes, bill-of-lading generation, sender configuration, and COD support.

Romanian merchants typically run Cargus alongside Sameday and / or DPD Romania — providing customers multiple courier options.

## Where to find it

Sidebar → Apps → install → **Cargus** OR direct routes.

Cargus exposes only TWO sub-pages (the LEANEST router among the Romanian couriers — no Shipments / Payments tabs):

| Sub-page | Route name | Path |
|----------|------------|------|
| Overview | `apps.cargus.overview` | `/admin/shipping/cargus/` |
| Settings | `apps.cargus.settings` | `/admin/shipping/cargus/settings` |

Generated waybills appear in the global [[orders]] list filtered by shipping provider — not under the Cargus app.

## What the merchant can do here

### Settings

| Field | Notes |
|-------|-------|
| **Username** | Cargus API username (from Cargus's courier portal). |
| **Password** | Cargus API password. |

Plus shared OmniShip configuration (sender data, allowed methods, defaults, insurance, COD).

The Cargus integration is **simpler than Sameday** — only two credentials, single-country (Romania) by default.

### Allowed methods

Cargus is primarily home delivery (door-to-door). No locker channel exposed via this integration.

### What the merchant CANNOT do here
- Use Cargus outside Romania — single-country focus.
- Generate waybills without a Cargus contract.

## Settings & fields

Cargus uses a simpler two-credential pattern (Username + Password). All other configuration follows the standard shipping-provider pattern — sender address, allowed methods, defaults, insurance, COD configuration.

### Pricing models

The merchant picks ONE pricing model per shipping rate:

- **Cargus calculator** — live API quote.
- **Cargus calculator + processing fee** — API quote plus a fixed processing fee.
- **Cargus calculator + free shipping** — API quote zeroed out for the customer.
- **Fixed value at price without Cargus calculator** — flat price tier per order subtotal.
- **Fixed value by weight without Cargus calculator** — flat price tier per weight.
- **Fixed value for price and weight without Cargus calculator** — combined matrix.

## Business rules

### Romania-focused

Cargus operates primarily in Romania. The platform's geo lookups focus on Romanian cities and post-code structure.

### COD supported

COD is supported. The COD amount is synced via [[orders-sync-cod]].

### Recalculation on payment-method change

Switching the payment method on an order (per [[orders-payment-manual]]) triggers shipping cost recalculation when COD is currently active. The Cargus COD fee is added or removed depending on the new payment method.

### Same OmniShip integration patterns

As with all OmniShip couriers, Cargus follows: real-time quotes → bill-of-lading generation → tracking sync. See [[orders-shipping-waybill]] for the unified flow.

### Side effects

Standard OmniShip side effects on save / waybill / etc.

### Permission

Standard apps permission scope.

## Per-channel delivery pricing

Cargus delivers to **address** and to **office** — each of its **2** delivery channels (to **address** and to **office**) is a separate rate card with its own enable toggle (`to_address` / `to_office`) and a **Delivery price calculation** type. When the merchant picks a type, the rate card reveals these fields:

- `calculator` — the real-time Cargus quote; **no extra field** of its own.
- `calculator_fixed` — the Cargus quote **plus a fixed fee** you enter in the **Parcel processing Fee** field (`fixed_price_<channel>`).
- `free` — the Cargus quote, but **free above a threshold** you set in **Minimum Order Value for Free Delivery** (`free_shipping_total_<channel>`); below it the customer pays the quote.
- `fixed_price` — a **Fixed value by price** rate table: rows keyed by **cart subtotal** (`from` / `to` / `amount`); the courier quote is ignored.
- `fixed_weight` — a **Fixed value by weight** rate table: rows keyed by **total weight**.
- `price_and_weight` — a combined table keyed by **both cart subtotal and weight**.

The calculator-based types also expose an optional **Fallback price** rate table, used only when the live quote can't return a price; the `fixed_*` types need no fallback (their table **is** the price). **Every** type also adds a **per-category** sub-table ("Set different pricing conditions for products in category/ies") for charging chosen categories differently. Full field mechanics + rate-row semantics: [[shipping-calc-rate-card-fields]] and [[shipping-calc-rate-models]].

## Related

- [[shipping-calc-rate-models]] — rate-table semantics: when a method uses a from/to rate table (по тегло / по цена), an **empty upper bound (`до` / `to`) means no upper limit — the bracket runs to infinity** (both bounds inclusive). A blank top row is intended, not invalid, and never hides the method at checkout.
- [[apps]] — App Store.
- [[apps-sameday]] — sister RO courier (locker network EasyBox).
- [[apps-dpdromania]] — DPD's Romanian branch (third major RO courier).
- [[apps-fancourier]] — also operates in Romania.
- [[shipping]] — shipping landing.
- [[orders-shipping-waybill]] — waybill flow.
- [[orders-sync-cod]] — COD sync.
- [[settings-payment-providers]] — COD configuration.

## How it works (verified against backend)

### Romanian-only

Fallback allowed countries is just Romania — explicit Romanian-only courier. Cross-border international shipments are NOT supported via this integration; merchants needing RO ↔ HU / BG / EU need a different courier.

### Door-to-door only

Supported delivery channel is address (door delivery) only. **NO locker network exposed** via this integration. For locker delivery in Romania, use [[apps-sameday]] (EasyBox).

### Two credentials

Cargus uses a simpler two-credential setup (Username + Password) than BoxNow's three-credential (`client_id + client_secret + partner_id`) or DHL's five-account structure.

### Default: receiver pays

Default settings:
- **Side** = receiver pays — customer pays the courier.
- **To address** = on — door delivery.
- **Pricing model** = calculator — live rate quote.
- **Default weight** = 100g fallback.

**Key difference from BoxNow**: Cargus defaults to receiver-pays (customer pays the courier) — typical for the Romanian COD-heavy market where the customer pays cash on delivery. BoxNow defaults to sender-pays.

### Six pricing models

Same set as Speedy / Sameday — calculator, calculator + processing fee, calculator + free shipping, fixed price, fixed weight, and price+weight. The merchant picks the model that matches their Cargus contract structure.

### COD supported per OmniShip family

COD is enabled when the OmniShip base allows it, the merchant's COD setting is on, AND the order is within the COD cap. For BGN stores the cap is 10000; for RON stores there's no platform-side cap (Cargus's server-side limit applies).

### Service tiers come from Cargus's API

The Cargus integration doesn't hardcode a list of service tiers (Standard / Express / etc.). Available services are fetched from Cargus's API after the merchant saves credentials, and shown in the "Allowed methods" picker. The merchant enables the tiers their contract includes; only those appear to customers at checkout.

### Insurance gated on COD-band and merchant toggle

Insurance follows the OmniShip pattern: available only when (a) the merchant turned on the insurance toggle in Settings, and (b) the order amount is within the COD cap. Insurance value is converted to BGN before being sent to Cargus's API.

## Settings tab — full layout (deep audit 2026-05-27)

Cargus has the SIMPLEST shipping provider Vue: just two routes (Overview + Settings) and NO custom Sender / Credentials components — uses the shared defaults.

### 1. Credentials box
- **Username** + **Password** (`UsernamePasswordCredentials` — shared default).

### 2. Name & logo (Visualization)

### 3. Sender data box
- No custom `SenderDataSection` — the shared `PickupData` placeholder is used; sender data is configured via the additional-settings boxes (not via a slide-down editor). Cargus's Vue intentionally omits this slot.

### 4. Services / 5. Per-channel rate cards
Standard per-channel modals. Cargus exposes `address` only (door-to-door); no office/locker channel cards.

### 6. Geo zones / 7. Payment providers — standard.

### 8. Additional settings — two boxes (backend-driven `SettingsBox`)

#### Box 1 — `general_settings`
- **Who pay the shipping cost** (`side`) — radio (sender / receiver / other).
- **Default weight for one item** (`default_weight`).
- **Default width / length / height** (mm).
- **Choose a content description** (`order_content`) — Product name / SKU / barcode.

#### Box 2 — `parcel_and_waybill_settings`
- **Enable cash on delivery** (`cd`) — switch.
- **Declared value of the shipment** (`declared`) — switch.
- **Delivery on Saturday** (`saturday`) — switch.
- **Shipment inspection** (`open_package`) — switch (allows recipient to open before paying, contract-permitting).

### 9. Submit-changes sticky footer

## No Shipments / Shipments-return / Payments tabs
Cargus's Vue router does NOT mount Shipments, Shipments-return, or Payments sub-pages. Generated waybills appear in the global Orders list (filtered by shipping provider), not under the Cargus app.

## Overview tab — standard.

## Open questions
