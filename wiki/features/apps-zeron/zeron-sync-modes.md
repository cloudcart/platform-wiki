---
type: feature
nav_path: "Apps → Zeron → Behaviour modes"
route_name: apps.zeron.overview
route_path: /admin/apps/zeron
aliases: ["Zeron sync modes", "Zeron behaviour modes", "Zeron order export trigger", "Zeron warehouses site_id", "Zeron import vs update", "Zeron single vs multi warehouse"]
tags: [apps, erp, sync, behaviour]
plan_gates: []
created: 2026-06-16
updated: 2026-06-16
source_count: 1
---

> Part of [[apps-zeron]]. See the hub for credentials, the full per-setting table, and the misleading-trigger-label business rule.

# Zeron — behaviour modes

## Purpose

Zeron is not one on/off integration. Its settings form **independent axes**, and a store's actual behaviour is the *combination* of the choices on each. This page is the behavioural model — how the settings combine into "what syncs, from which warehouses, and when orders push". The per-setting reference (field types, defaults, validation) is on the hub [[apps-zeron]].

Inbound (catalogue / stock / price) and outbound (orders) are configured, and behave, independently.

## Where to find it

All of these are on **Sidebar → Apps → Zeron → Settings** (`/admin/apps/zeron`).

## What the merchant can do here

Pick the behaviour along each axis independently:

- **Inbound** — whether Zeron creates products in CloudCart or only refreshes stock + prices.
- **Outbound** — when a placed order is pushed to Zeron.
- **Warehouses** — which Zeron warehouses feed stock and which fulfils orders (or a single Zeron object via Site ID).

## Settings & fields

### Inbound — catalogue / stock / price (Zeron → CloudCart)

Set by **Action** (`action`):

- **Import products + update quantities** — Zeron's catalogue is *created* in CloudCart (new products → the chosen default category) and kept synced.
- **Update quantities and prices only** — no new products; the CloudCart catalogue is kept and only stock + prices refresh.

Modifiers: **`compare_by`** (SKU / Barcode) matches products; **`product_price_percent`** applies a markup over the Zeron price on import (**default 20 %** — set to 0 before the first import to keep Zeron prices as-is; shown only when Action = import); **`category_id`** (import only) is where new products land; **`product_status`** decides whether new products are published.

### Outbound — order export (CloudCart → Zeron)

Set by **Send order** (`send_order`), **independent of the inbound axis** — three options. **The option labels do not match their actual trigger** (documented on the hub): the label *"Order complete"* actually fires on payment (Paid or Sent), and *"Paid or Sent"* actually fires when the order reaches **Completed**. Verified mapping:

| Selector label | Actual trigger |
|---|---|
| New order | order creation |
| Order complete | payment reported (Paid or Sent) |
| Paid or Sent | order status becomes Completed |

There is **no master pause toggle, no close-order setting, and no automatic cancellation push** (unlike Barsy). Each push is logged to order history (`send_erp_success` / `send_erp_error`).

### Warehouses — `site_id` gating

A single setting decides single- vs multi-warehouse behaviour:

- **`site_id` empty / 0** → multi-warehouse mode: pick which Zeron **warehouses** feed stock (`warehouses`, multi-select) and which **warehouse fulfils orders** (`warehouse_order`). With the [[apps-stores|Stores]] app installed, **`create_warehouses`** turns each selected warehouse into a CloudCart Store for [[apps-store-locations]] use.
- **`site_id` set** (a Zeron Website ID) → single-object mode: the warehouse selectors are ignored and that one Zeron partition is used.

## Business rules

The axes do not gate each other:

- Choosing **Update quantities and prices only** does **not** stop orders exporting.
- The warehouse selection feeds inbound stock and outbound fulfilment independently of the order trigger.

So a store's behaviour is the *product* of the choices, for example:

| Inbound | Outbound | Warehouses | Resulting behaviour |
|---|---|---|---|
| Update quantities + prices only | New order | multi (`site_id`=0) | "Keep my catalogue, refresh stock/prices from my selected warehouses, push each order on creation." |
| Import + update quantities | Paid or Sent (= Completed) | single (`site_id` set) | "Zeron owns the catalogue from one Website ID; push orders only when completed." |

## Related

- [[apps-zeron]] — hub: credentials, full per-setting table, misleading-label business rule.
- [[apps-stores]] / [[apps-store-locations]] — required for the warehouses-as-Stores option.
- [[erp-integrations]] — ERP category; the shared catalogue / stock / price / order sync model.
- [[order-processing-pipeline]] — the order events that fire the outbound push.

## Open questions

_None._
