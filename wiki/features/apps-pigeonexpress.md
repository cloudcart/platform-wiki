---
type: feature
nav_path: "Apps → Pigeon Express"
route_name: apps.pigeonexpress
route_path: /admin/apps/pigeonexpress
aliases: ["Pigeon Express", "Pigeonexpress", "Pigeon Express courier", "Пиджън Експрес", "Pigeon shipping"]
tags: [apps, shipping, courier, bulgaria, cod, omniship]
plan_gates: []
created: 2026-06-11
updated: 2026-06-26
source_count: 1
---
# Pigeon Express (shipping courier)

## Purpose

**Pigeon Express** is a courier integration that lets the store offer Pigeon Express delivery at checkout and generate its waybills from the order. It is **Bulgaria-first** and connects with the merchant's own Pigeon Express API credentials. Delivery is offered to a **home/office address**, to a **Pigeon office**, or to a **locker**, with live price quotes, cash-on-delivery, declared value, and a set of optional courier services.

It runs on the shared shipping framework (the same engine behind [[apps-econt]], [[apps-dpdbulgaria-speedy|Speedy]], [[apps-speedex]]), so the Settings layout, per-channel pricing models, and geo-zone gating follow the common pattern.

## Where to find it

Sidebar → **Apps** → install → **Pigeon Express**. The app has an **Overview** (`apps.pigeonexpress`) and a **Settings** screen (`apps.pigeonexpress.settings`). The merchant first connects credentials (**Connect Pigeon Express**, `apps.pigeonexpress.connect`), then configures delivery.

## What the merchant can do here

- Connect the store to Pigeon Express with an **API Key** + **API Secret**.
- Offer delivery to **address**, **office**, or **locker** (`support = address / office / locker`).
- Set per-channel pricing: `calculator`, `calculator_fixed`, `free`, `fixed_price`, or `price_and_weight`.
- Enable **cash on delivery** and **declared value**.
- Add optional courier services (review/test before payment, return receipt, return documents, ID verification, card payment of COD).
- Choose who pays shipping, the default parcel weight/dimensions, and the waybill content description.
- Print waybills and track shipments from the order.

### What the merchant CANNOT do here

- Use the app without valid API credentials — connecting fails with *"You have not entered an API key"* / *"You have not entered an API secret"*.
- Offer COD beyond Pigeon's accepted band, or to a non-served country (Bulgaria-first; see Business rules).

## Settings & fields

### Credentials (Connect)

| Field | Notes |
|---|---|
| **API Key** (`api_key`) | Required. |
| **API Secret** (`api_secret`) | Required. |

The **Connect Pigeon Express** button validates the pair against Pigeon's API; the live vs test account is selected per environment.

### Box 1 — general settings

- **Default weight for one item** (`default_weight`) — weight unit.
- **Default width / depth / height for one item** (`default_width` / `default_depth` / `default_height`) — cm.
- **Choose a content description** (`order_content`) — Product name / SKU / barcode.
- **Submit product sizes** (`item_sizes`) — switch; when on, product dimensions are sent so Pigeon computes **volumetric weight** and each cart product is treated as a **separate package**.

### Box 2 — parcel & waybill settings

- **Who pays the shipping cost** (`side`) — radio: Receiver (default) / Sender.
- **Enable cash on delivery** (`cd`) — switch.
- **Declared value** (`declared_value`) — switch.
- **Tracking shipment** (`tracking`) — where the tracking link points (e.g. *In your store*).
- **Additional services** (sent as `service_codes` on the quote / waybill):
  - **Review by the recipient** (`shipment_review`) and **Review and test before payment** (`shipment_test_before_payment`) — **mutually exclusive** (one `shipment_view` choice).
  - **Allow card payment of cash on delivery** (`cod_card_fee`).
  - **Return receipt (electronic)** (`return_receipt`) and **Return receipt (paper)** (`paper_return_receipt`).
  - **Return documents** (`service_return_documents`).
  - **ID verification and signature** (`ID_verification_and_document_signature`).

Channel + geo-zone + payment-provider boxes follow the shared shipping form (same as [[apps-econt]] / [[apps-dpdbulgaria-speedy|Speedy]]).

## Business rules

### OmniShip-based provider

Pigeon Express runs on CloudCart's shared shipping framework. Quotes, waybill creation, the per-channel pricing models, the three delivery channels, and geo-zone gating are all the common engine; only the credentials and the Pigeon-specific service list are unique to this app.

### Reference data is cached

Pigeon's countries, cities, offices, and lockers are pulled from its API and **cached** by background tasks, so the office / locker pickers load instantly and don't hit Pigeon on every checkout. A newly opened Pigeon office may take until the next refresh to appear.

### Office / locker weight cap

Delivery to a Pigeon **office** has a default maximum weight of **1000** (heavier parcels fall back to address delivery or are not offered to office/locker).

### Cash on delivery + card option

When `cd` is on, the COD amount rides on the waybill; `cod_card_fee` additionally lets the recipient pay the COD by card. COD and declared value are amount services handled separately from the checkbox services above.

### Cross-border COD

COD behaviour is tuned for Bulgaria: when the payer is the **receiver** and the shipping country is **not BG**, the platform adjusts the COD/payer handling accordingly (Bulgaria-first integration).

## Per-channel delivery pricing

Pigeon Express delivers to **address**, to **office** and to **locker** — each of its **3** delivery channels (to **address**, to **office** and to **locker**) is a separate rate card with its own enable toggle (`to_address` / `to_office` / `to_locker`) and a **Delivery price calculation** type. When the merchant picks a type, the rate card reveals these fields:

- `calculator` — the real-time Pigeon Express quote; **no extra field** of its own.
- `calculator_fixed` — the Pigeon Express quote **plus a fixed fee** you enter in the **Parcel processing Fee** field (`fixed_price_<channel>`).
- `free` — the Pigeon Express quote, but **free above a threshold** you set in **Minimum Order Value for Free Delivery** (`free_shipping_total_<channel>`); below it the customer pays the quote.
- `fixed_price` — a **Fixed value by price** rate table: rows keyed by **cart subtotal** (`from` / `to` / `amount`); the courier quote is ignored.
- `fixed_weight` — a **Fixed value by weight** rate table: rows keyed by **total weight**.
- `price_and_weight` — a combined table keyed by **both cart subtotal and weight**.

The calculator-based types also expose an optional **Fallback price** rate table, used only when the live quote can't return a price; the `fixed_*` types need no fallback (their table **is** the price). **Every** type also adds a **per-category** sub-table ("Set different pricing conditions for products in category/ies") for charging chosen categories differently. Full field mechanics + rate-row semantics: [[shipping-calc-rate-card-fields]] and [[shipping-calc-rate-models]].

## Related

- [[shipping-calc-rate-models]] — rate-table semantics: when a method uses a from/to rate table (по тегло / по цена), an **empty upper bound (`до` / `to`) means no upper limit — the bracket runs to infinity** (both bounds inclusive). A blank top row is intended, not invalid, and never hides the method at checkout.
- [[apps]] — App Store.
- [[apps-econt]] — Econt courier (same shared shipping framework, richer feature set).
- [[apps-dpdbulgaria-speedy|Speedy]] / [[apps-speedex]] — other Bulgarian couriers on the same engine.
- [[shipping]] — shipping concept hub.
- [[orders-shipping-waybill]] — generating the waybill on an order.
- [[settings-shipping]] — where shipping methods are enabled per store.

## Open questions

- The exact list of countries Pigeon Express serves beyond Bulgaria (verify against the populated reference data).
- Whether lockers are nationwide or limited to specific cities (verify).
