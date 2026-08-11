---
type: feature
nav_path: "Apps → Mikmik"
route_name: apps.mikmik.overview
route_path: /admin/shipping/mikmik
aliases: ["Mikmik", "Mik Mik courier", "MikMik"]
tags: [apps, shipping, courier, western-balkans, omniship]
plan_gates: []
created: 2026-05-22
updated: 2026-06-26
source_count: 4
---
# Mikmik

## Purpose

**MikMik** is a Western Balkans courier serving Kosovo, Albania, and North Macedonia. The CloudCart integration provides real-time delivery quotes, waybill generation, and tracking — useful for merchants shipping to / within these three markets.

## Where to find it

Sidebar → Apps → install → **Mikmik** OR direct routes. Standard OmniShip sub-pages.

## What the merchant can do here

- Install / activate / deactivate the integration.
- Configure credentials in the Settings sub-page.
- Generate waybills + track shipments per order.
- Show MikMik as a checkout option (priced from the merchant's own rate table — see Pricing modes below).

### What the merchant CANNOT do here
- Use MikMik without a registered MikMik courier contract.
- Generate PDF waybill labels — MikMik does NOT support printing waybills as PDF from CloudCart.
- Ship outside MikMik's coverage area (Kosovo / Albania / North Macedonia).

## Settings & fields

Three credential fields:

| Field | Notes |
|-------|-------|
| **MikMik Username** | API username. |
| **MikMik Password** | API password. |
| **MikMik Login ID** | MikMik account / login identifier. |

## Business rules

Same OmniShip pattern (quotes → waybill → tracking) with MikMik-specific quirks documented below.

## How it works (verified against backend)

### Coverage countries
**Western Balkans.** MikMik populates cities for three country IDs in its database:
- **Kosovo (XK)**.
- **Albania (ALB / AL)**.
- **North Macedonia (MKD / MK)**.

A customer outside these three countries won't see MikMik at checkout.

### Pricing modes (storefront price options) — 3 only, NO live calculator
MikMik supports only 3 pricing types (`PRICING_TYPES`): `fixed_price`, `fixed_weight`, `price_and_weight`. There is **NO live-quote / calculator mode** — the merchant configures their own rate tables. The MikMik API is still used for waybill creation and tracking, but not for checkout-time rate quotes.
- **Fixed value at price without MikMik calculator** — flat price per cart-value tier.
- **Fixed weight value without MikMik calculator** — flat price per weight tier.
- **Fixed value for price and weight without MikMik calculator** — combined flat rules.

### Delivery channels
Supported channel is **address only** (door delivery). MikMik does NOT expose office / locker channels via the CloudCart integration.

### PDF waybill printing NOT supported
**Bill of lading printing as PDF is NOT supported** by MikMik. The label can be generated in MikMik's system but not printed straight as a PDF from CloudCart — message: *"Bill of lading printing is not supported."* The merchant prints labels from MikMik's own portal.

### Sameday service option
MikMik exposes a **"Sameday"** service option, used for same-day delivery shipments within their coverage area.

### "Open before paying" requires SENDER to pay
The option to inspect the parcel before payment is only available when **the SENDER pays for the shipment**. If the recipient is the payer, the option is hidden. Help text: *"The Open before paying option can only be used if the payer of the shipment is the SENDER."*

### Waybill validation messages
If the merchant tries to create a waybill without selecting the paying party:
- *"Please select the party that will pay for the shipment."*
- *"The selected paying party is invalid."* — if value is unrecognized.

### COD supported with cap
COD is enabled when the merchant's COD setting is on AND the order is within the COD cap (10000 BGN for BGN stores). Sender is the default payer.

### Integration runs in sandbox mode by default
The MikMik integration runs against MikMik's sandbox API — verified by the codebase setting test-mode permanently to true. There is no merchant-facing toggle to switch to production mode; that change would require a code-level update.

## Settings page — full layout (shared OmniShip form + custom credentials)

MikMik uses `SettingsFormShippings` with a custom **`#credentials` slot**:

### Credentials card (custom — `CourierCredentialsSection.vue`)
| Field | Input | Required | Notes |
|-------|-------|----------|-------|
| MikMik Username (`username`) | Text (`column-style`) | Yes | Error: "Invalid credentials" |
| MikMik Password (`password`) | PasswordInput (masked, eye toggle) | Yes | Error: "Invalid credentials" |
| MikMik Login ID (`id_login`) | Text | Yes | "ID login is required" |

`Connect` button → validates; on success the rest of the form slides in.

### Remaining shared sections
- **Visualization** — courier display name + logo upload.
- **Service-type cards** — `address` only. Pencil opens the **Service-type calculator modal** with the 3 MikMik pricing modes (fixed price, fixed weight, price+weight — no calculator mode) + rate rows + countries + categories.
- **Ships to (Geo Zones)** — geo-zone allow-list (in practice XK / AL / MK).
- **Payment providers** — payment method multi-select.
- **Additional Settings box** (`parcel_and_waybill_settings`) — only two fields exist here:
  - **Enable cash on delivery** (`cd`) — switch.
  - **View** (`view_test`) — switch.

  There is NO `default_weight` field, NO `Sameday` switch, NO payer-side selector, and NO "Open before paying" toggle in this box.

## Per-channel delivery pricing

MikMik delivers to **address** — the single **address** channel is a separate rate card with its own enable toggle (`to_address`) and a **Delivery price calculation** type. When the merchant picks a type, the rate card reveals these fields:

- `fixed_price` — a **Fixed value by price** rate table: rows keyed by **cart subtotal** (`from` / `to` / `amount`); the courier quote is ignored.
- `fixed_weight` — a **Fixed value by weight** rate table: rows keyed by **total weight**.
- `price_and_weight` — a combined table keyed by **both cart subtotal and weight**.

Each `fixed_*` type's table **is** the price (there is no live calculator on MikMik, so no fallback). **Every** type also adds a **per-category** sub-table ("Set different pricing conditions for products in category/ies") for charging chosen categories differently. Full field mechanics + rate-row semantics: [[shipping-calc-rate-card-fields]] and [[shipping-calc-rate-models]].

## Related

- [[shipping-calc-rate-models]] — rate-table semantics: when a method uses a from/to rate table (по тегло / по цена), an **empty upper bound (`до` / `to`) means no upper limit — the bracket runs to infinity** (both bounds inclusive). A blank top row is intended, not invalid, and never hides the method at checkout.
- [[apps]] — App Store.
- [[shipping]] — shipping landing.
- [[orders-shipping-waybill]] — waybill flow.
- [[shipping-provider-mechanism]] — common shipping pattern.

## Open questions

_None — all questions answered above._
