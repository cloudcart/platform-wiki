---
type: feature
nav_path: "Apps → Barsy → Behaviour modes"
route_name: apps.barsy.overview
route_path: /admin/apps/barsy
aliases: ["Barsy sync modes", "Barsy behaviour modes", "Sync only vs Import and Sync", "Barsy order export trigger", "Barsy sync only", "Barsy inbound outbound", "Barsy action mode", "Barsy allow send order"]
tags: [apps, erp, retail, sync, behaviour]
plan_gates: []
created: 2026-06-16
updated: 2026-06-16
source_count: 1
---

> Part of [[apps-barsy]]. See the hub for credentials, the tab layout, the full per-setting reference, and the order-push business rules.

# Barsy — behaviour modes

## Purpose

Barsy is not one on/off integration. Its settings form **independent axes**, and a store's actual behaviour is the *combination* of the choices on each. This page is the behavioural model — how the settings combine into "what syncs, in which direction, and when". The most common confusion — *"Barsy is installed, why didn't X happen?"* — comes from treating Barsy as a single mode instead of separate axes. Inbound (catalogue / stock / price) and outbound (orders) are configured, and behave, independently of each other.

## Where to find it

All of these are configured on **Sidebar → Apps → Barsy → Settings** (`/admin/apps/barsy`). Each field named below lives on that screen; the per-field reference (options, defaults, validation) is on the hub [[apps-barsy]] under Settings & fields. This page explains how those fields combine into behaviour, not where each toggle sits.

## What the merchant can do here

Pick the behaviour along each axis independently:

- **Inbound** — whether Barsy creates products in CloudCart or only refreshes stock / prices.
- **Outbound** — whether (and when) placed orders are pushed to Barsy.
- **Location** — single Barsy object, or many objects mapped to store locations.
- **Delivery** — route orders to all suppliers without Glovo, or to Glovo for last-mile.

The store's overall behaviour is the product of these four choices — none of them is implied by another.

## Settings & fields

### Inbound — catalogue / stock / price (Barsy → CloudCart)

Set by **Action mode** (`action`):

- **Import and Sync** — Barsy's catalogue is *created* in CloudCart (new products land in the chosen default category) and then kept in sync. Barsy owns the catalogue.
- **Sync only** — **no new products** are created; the CloudCart catalogue is left as-is, and only **stock + prices** are refreshed on products matched to Barsy. Use when the catalogue is maintained in CloudCart and Barsy is only the stock / price source.

Modifiers that narrow the inbound flow:

- **Only update** (`only_update`, default on) — only products that changed in Barsy are taken on each run.
- **Clear quantities** (`clear_qty`, available only when `only_update` is off) — a product missing from the Barsy feed has its CloudCart stock set to 0.
- **Quantity tracking** + **default quantity** — apply a fallback stock to imported products that carry no quantity from Barsy.
- **Product matching** (`compare_by` ↔ `compare_barsy`) — which identifier pairs a CloudCart product to a Barsy one (ID / SKU / Code / Barcode).

### Outbound — order export (CloudCart → Barsy)

Set by the **Order export trigger** (`send_order`), **independent of the inbound axis**:

- **New Order** — push on order creation.
- **Paid** — push when the payment is reported `completed`.
- **Sent** — push when a fulfilment is added.

Layered on top:

- **Allow send order** (`allow_send_order`, default on) — a master switch that pauses *all* order pushes without uninstalling the app.
- **Close order** (`close_order`) — separately finalises a paid / completed order that already reached Barsy (only paid orders with payment details are closed).
- **Cancellation** is automatic and trigger-independent — once an order that reached Barsy becomes `cancelled`, the cancellation (with the chosen `cancel_reason`) is pushed.

### Secondary axes

- **Operation mode** (`type`) — single-location (one Barsy object) vs multi-location (each Barsy object ↔ a CloudCart store location; needs [[apps-store-locations]]).
- **Delivery method** — orders routed to all suppliers without Glovo, or forwarded to [[apps-glovo|Glovo]] for last-mile.

## Business rules

The axes do not gate each other:

- Choosing **Sync only** does **not** stop orders exporting.
- Pausing **Allow send order** does **not** affect catalogue / stock sync.
- The order trigger fires regardless of whether the catalogue is imported or sync-only.

So a store's behaviour is the *product* of the choices, for example:

| Inbound | Outbound | Resulting behaviour |
|---|---|---|
| Sync only | Paid | "Leave my catalogue alone, keep stock/prices current, push each order to Barsy when it's paid." |
| Import and Sync | New Order | "Barsy owns the catalogue; every new order goes to Barsy on creation." |
| Import and Sync (+ Glovo) | Sent | "Barsy owns the catalogue; orders push when fulfilled and ship via Glovo." |
| any | Allow send order off | "Keep syncing the catalogue / stock, but stop sending orders to Barsy entirely." |

## Related

- [[apps-barsy]] — hub: credentials, tabs, full per-setting reference, order-push business rules.
- [[apps-store-locations]] — required for the multi-location operation mode.
- [[apps-glovo]] — last-mile when the Glovo delivery method is chosen.
- [[erp-integrations]] — ERP category; the shared catalogue / inventory / price / order sync model.
- [[order-processing-pipeline]] — the order events that fire the outbound push.

## Open questions

_None._
