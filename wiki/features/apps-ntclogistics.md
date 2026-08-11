---
type: feature
nav_path: "Apps → NTC Logistics"
route_name: apps.ntclogistics.overview
route_path: /admin/shipping/ntclogistics
aliases: ["NTC Logistics", "NTC courier", "Ntclogistics"]
tags: [apps, shipping, courier, montenegro, omniship]
plan_gates: []
created: 2026-05-22
updated: 2026-06-26
source_count: 4
---
# NTC Logistics (Montenegrin courier)

## Purpose

**NTC Logistics** integration — a courier serving **Montenegro** (ME). The integration provides real-time delivery quotes, waybill generation, and tracking for orders shipping to Montenegrin addresses with valid post codes.

## Where to find it

Sidebar → Apps → install → **NTC Logistics** OR direct routes. Standard OmniShip sub-pages.

## What the merchant can do here

- Install / activate / deactivate the integration.
- Configure credentials + sender address in the Settings sub-page.
- Generate waybills per order.
- Show NTC as a checkout option, priced from the merchant's own rate table (NTC has no live-rate calculator).

### What the merchant CANNOT do here
- Use NTC without a registered NTC Logistics courier contract.
- Generate waybills for destinations outside Montenegro.
- Ship to Montenegrin addresses whose post codes aren't in NTC's city list (the platform validates against NTC's synced post-code registry).

## Settings & fields

### Credentials

| Field | Notes |
|-------|-------|
| **Username** | NTC API username. |
| **Password** | NTC API password. |

### Sender address (required at install)

The merchant configures a default sender address that NTC will use as the dispatch point:

| Field | Notes |
|-------|-------|
| **Sender's name** (`sender_name`) | Sender / company name — required. |
| **Sender's phone number** (`sender_phone`) | Sender phone number — required. |
| **Country code** (`country_code`) | Sender country (typically ME) — required. |
| **City** (`city`) | Sender city — required. |
| **Post code** (`post_code`) | Sender post code — required. |
| **Address** (`address`) | Street address text — required. |

### Pricing modes (storefront) — 3 only, NO live calculator

NTC Logistics supports only 3 pricing types (`PRICING_TYPES`): `fixed_price`, `fixed_weight`, `price_and_weight`. **No live-quote / calculator mode** — the merchant configures their own rate tables. NTC's API is still used for waybill creation, tracking, and city/post-code validation but not for checkout-time rate quotes.

- **Fixed value at price** — flat price per cart-value tier.
- **Fixed value by weight** — flat price per weight tier.
- **Fixed value by price and weight** — combined flat rules.

### Payer side (parent + per-order)

- **Default payer** (at parent level) — `Sender` (merchant pays) by default. The merchant can flip to `Recipient` (customer pays).
- **Per-order override** via the waybill form — the merchant picks Sender vs. Recipient on each shipment.

### Additional waybill fields

| Field | Notes |
|-------|-------|
| **Comment** | Free-text shipment notes. |
| **Declared Value** | Optional declared-value declaration (for insurance / customs). |
| **Return documents** | Toggle — request signed delivery documents back. |
| **Payment method** | `Cash` or `Account` — how the payer settles with NTC. |

## Business rules

Standard OmniShip pattern with NTC-specific quirks below.

## How it works (verified against backend)

### Coverage: Montenegro only (post-code gated)

The integration checks the receiver address's country and matches against NTC's synced city table. Quotes are only generated when:
- Country ISO is `ME` (Montenegro), AND
- Post code matches a record in NTC's city table.

Customers outside Montenegro, or in Montenegrin post codes not in NTC's registry, won't see NTC at checkout. NTC's `fallback_allowed_countries` is empty — there is no hardcoded country whitelist; the city/post-code lookup is the gate.

### Address-only delivery channel

Supported channel is **address only** (door delivery). No locker / office channels exposed.

### Default SENDER pays, per-order price-list override

The default payer is `SENDER` (merchant pays courier). The merchant can switch payer per order via a `price_list` setting (1 = sender pays, 2 = receiver pays).

### COD supported with cap

COD is enabled when the merchant's COD setting is on AND the order is within the COD cap (10000 BGN for BGN stores; no platform cap for non-BGN — NTC's own server-side limits apply).

### COD + recalculate-on-payment-change

Switching payment method on an order recalculates shipping when COD is supported — same OmniShip family behavior.

### Insurance supported (declared-value)

NTC supports insurance via the "Declared Value" field. When enabled, the merchant declares the shipment's value and pays NTC's insurance premium.

### Integration runs in sandbox mode by default

The NTC integration runs against NTC's sandbox API — verified by the codebase setting test-mode permanently to true. There is no merchant-facing toggle to switch to production mode; that change would require a code-level update.

### Cities synced from NTC's API

NTC's city + post-code list is synced from NTC's API on a scheduled background job — the merchant doesn't manage this list manually. When NTC adds coverage to new Montenegrin post codes, those appear in CloudCart within the sync window.

## Settings page — full layout (shared OmniShip form + custom sender)

NTC Logistics uses `SettingsFormShippings` with the SHARED `UsernamePasswordCredentials` credentials card AND a custom **`#senderData` slot**:

### Credentials card (shared)
- **Username** (text, required).
- **Password** (text, required).
- `Connect` button.

### Sender data card (custom `#senderData` slot)
The merchant configures a default sender via `SenderDataSection.vue`. Fields (all required):

| Field | Input | Notes |
|-------|-------|-------|
| Sender's name (`sender_name`) | Text | Error key: `ntclogistics.sender_name` |
| Sender's phone number (`sender_phone`) | Phone input | Error key: `ntclogistics.sender_phone` |
| Country code (`country_code`) | Text | "Country code is required" |
| City (`city`) | Text | "City is required" |
| Post code (`post_code`) | Text | "Post code is required" |
| Address (`address`) | Text | "Sender address is required" |

Sender Data is exposed via the standard `SettingRow` (preview + pencil-to-edit). The pencil opens an inline panel; Save persists via the sticky submit bar.

### Remaining shared sections
- **Visualization** — courier display name + logo upload.
- **Service-type cards** — `address` only. Pencil opens the **Service-type calculator modal** with the 3 NTC pricing modes (fixed price, fixed weight, price+weight — no calculator mode) + rate rows + countries + categories.
- **Ships to (Geo Zones)** — geo-zone allow-list (in practice ME-only is meaningful).
- **Payment providers** — payment method multi-select.
- **Additional Settings box** (`general_settings`) — actual fields:
  - **Who pay the shipping cost** (`side`) — radio (Sender / Receiver).
  - **Default weight for one item** (`default_weight`) — required.
  - **Enable cash on delivery** (`cd`) — switch.
  - **Payment method** (`payment_type`) — select: `Cash` (`account`) / `Account` (`cash`).
  - **Return documents** (`doc_return`) — switch.

  Comment / Declared Value fields are NOT on the Settings page — they appear on the per-order waybill creation form, not in the integration settings.

## Per-channel delivery pricing

NTC Logistics delivers to **address** — the single **address** channel is a separate rate card with its own enable toggle (`to_address`) and a **Delivery price calculation** type. When the merchant picks a type, the rate card reveals these fields:

- `fixed_price` — a **Fixed value by price** rate table: rows keyed by **cart subtotal** (`from` / `to` / `amount`); the courier quote is ignored.
- `fixed_weight` — a **Fixed value by weight** rate table: rows keyed by **total weight**.
- `price_and_weight` — a combined table keyed by **both cart subtotal and weight**.

Each `fixed_*` type's table **is** the price (there is no live calculator on NTC Logistics, so no fallback). **Every** type also adds a **per-category** sub-table ("Set different pricing conditions for products in category/ies") for charging chosen categories differently. Full field mechanics + rate-row semantics: [[shipping-calc-rate-card-fields]] and [[shipping-calc-rate-models]].

## Related

- [[shipping-calc-rate-models]] — rate-table semantics: when a method uses a from/to rate table (по тегло / по цена), an **empty upper bound (`до` / `to`) means no upper limit — the bracket runs to infinity** (both bounds inclusive). A blank top row is intended, not invalid, and never hides the method at checkout.
- [[apps]] — App Store.
- [[shipping]] — shipping landing.
- [[orders-shipping-waybill]] — waybill flow.
- [[shipping-provider-mechanism]] — common shipping pattern.

## Open questions

_None — all questions answered above._
