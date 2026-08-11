---
type: feature
nav_path: "Apps → Next Level Delivery"
route_name: apps.nextlevel.overview
route_path: /admin/shipping/nextlevel
aliases: ["Next Level Delivery", "Nextlevel", "Next Level courier", "Некст Левъл", "Next Level куриер", "no enable disable button", "app has no active toggle"]
tags: [apps, shipping, courier, bulgaria, nextlevel, omniship]
plan_gates: []
created: 2026-06-23
updated: 2026-08-06
source_count: 1
---
# Next Level Delivery (courier)

## Purpose

**Next Level Delivery** is a Bulgarian courier integration (OmniShip-based) for delivery **to address, to office, and to parcel locker (automat)**, with cash-on-delivery (COD) and declared-value insurance. It covers the full shipping lifecycle — checkout rate quotes, waybill (bill-of-lading) generation, label printing (A4 / A6, single + bulk), and tracking. **Bulgaria only.**

> **No on/off control — this app has no "active / inactive" state.** Once it is installed it simply works; there is no Enable / Disable button and no "Activate application" switch on its screen. So *"the app is disabled"* is never the explanation for it not working — check its own settings, credentials, or plan access instead, and use **Uninstall** if the merchant genuinely wants it off.
>
> Activation here is **per courier / delivery method**, not per app: each installed courier has its own Enable / Disable button on its own settings page (`/admin/shipping/nextlevel/external/:id`).

## Where to find it

Sidebar → Apps → install → **Next Level** (`/admin/shipping/nextlevel`). App key `nextlevel`. The courier shows at checkout once it is activated **and** a Default sender address is set; the methods it offers are enabled / priced / geo-scoped on [[settings-shipping]] like every other courier.

## What the merchant can do here

- Connect with the Next Level **API Key + API Secret** (validated on save).
- Choose which delivery channels to offer: **to address / to office / to locker**.
- Configure the **sender (pickup)** — office / locker / address.
- Enable **cash on delivery** + **declared value** (insurance).
- Set who pays shipping (**Receiver** / **Sender**), default parcel weight / dimensions, content description, and additional services.
- Generate waybills + print labels (A4 / A6, single + bulk); track shipments.

### What the merchant CANNOT do here

- Use it outside Bulgaria (BG-only).
- Generate **return shipments** — Next Level's API has no return-label flow (unsupported by design, not a bug).
- Use it without valid Next Level API credentials.

## Settings & fields

### Credentials (required)

- **API Key** (`app_id`) + **API Secret** (`app_secret`) — the Next Level platform account credentials, validated against the Next Level API on save. Until they validate, the rest of the form is locked.
- **Mode** (`test_mode`) — test (sandbox) vs production; production stores are locked to live.

### Sender / pickup

- **Pickup** — office / locker / address; `office_id` (when office), `client_city_id` + `client_address` (when address).

### Delivery channels + pricing

- **To address / To office / To locker** toggles (`to_address` / `to_office` / `to_locker`), each with its own pricing model (`pricing_address` / `pricing_office`: calculator / fixed price / fixed weight / free / price + weight).
- **Allowed methods** (`allowed_methods`) — standard / express service types.

### Parcel & waybill

- **Side** (`side`) — Receiver (PAYER_RECEIVER) or Sender (PAYER_SENDER) pays shipping.
- **Cash on delivery** (`cd`) + **card payment of COD** (`cod_card_fee`).
- **Declared value** (`declared_value`) — insurance.
- Default **weight / width / height / depth** (cm; fallback per item), **content description** (`order_content`: name / SKU / barcode), volumetric weight per product (`item_sizes`).
- **Additional services**: shipment review / test-before-payment, return receipt (electronic / paper), return documents, ID verification + signature.
- **Tracking** (`tracking`) — in-store (CloudCart) or on the Next Level site.

## Business rules

- **OmniShip-based; credentials gate everything.** Gateway key `omniship.nextlevel`. The Addresses / Shipments tabs and checkout quotes appear only after credentials validate.
- **A single Default sender address drives every waybill** — no per-zone routing (same model as the other couriers).
- **Package dimensions are in centimetres** (defaults 10×10×10 cm, 0.1 kg).
- **COD has no payout / settlement API** — the COD payment is derived from delivery status (once delivered, the order is treated as paid for the COD amount); COD can't be enabled on already-paid orders.
- **No return shipments** — Next Level's API offers no return-label flow, so the feature is disabled by design.
- **No plan gate** — available on all plans.

## Per-channel delivery pricing

Next Level delivers to **address**, to **office** and to **locker** — each of its **3** delivery channels (to **address**, to **office** and to **locker**) is a separate rate card with its own enable toggle (`to_address` / `to_office` / `to_locker`) and a **Delivery price calculation** type. When the merchant picks a type, the rate card reveals these fields:

- `calculator` — the real-time Next Level quote; **no extra field** of its own.
- `calculator_fixed` — the Next Level quote **plus a fixed fee** you enter in the **Parcel processing Fee** field (`fixed_price_<channel>`).
- `free` — the Next Level quote, but **free above a threshold** you set in **Minimum Order Value for Free Delivery** (`free_shipping_total_<channel>`); below it the customer pays the quote.
- `fixed_price` — a **Fixed value by price** rate table: rows keyed by **cart subtotal** (`from` / `to` / `amount`); the courier quote is ignored.
- `fixed_weight` — a **Fixed value by weight** rate table: rows keyed by **total weight**.
- `price_and_weight` — a combined table keyed by **both cart subtotal and weight**.

The calculator-based types also expose an optional **Fallback price** rate table, used only when the live quote can't return a price; the `fixed_*` types need no fallback (their table **is** the price). **Every** type also adds a **per-category** sub-table ("Set different pricing conditions for products in category/ies") for charging chosen categories differently. Full field mechanics + rate-row semantics: [[shipping-calc-rate-card-fields]] and [[shipping-calc-rate-models]].

## Related

- [[shipping]] — courier directory hub.
- [[settings-shipping]] — enable / price / geo-scope the methods + Delivery days.
- [[orders-shipping-waybill]] — generates the Next Level waybill + label from an order.
- [[apps]] — App Store.

## Open questions

- None.
