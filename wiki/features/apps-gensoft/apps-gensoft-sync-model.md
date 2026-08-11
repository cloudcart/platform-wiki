---
type: feature
nav_path: "Apps → Gensoft → Sync model"
route_name: apps.gensoft.overview
route_path: /admin/apps/gensoft
aliases: ["Gensoft sync model", "Gensoft incremental import", "Gensoft last_import", "Gensoft sync frequency", "Gensoft order export", "Gensoft increment decrement", "Gensoft SOAP"]
tags: [apps, erp, gensoft, sync, soap, orders]
plan_gates: []
created: 2026-06-25
updated: 2026-06-25
source_count: 3
---

> Part of [[apps-gensoft]]. See the hub for the other aspects (settings, product matching, reset import, diagnostics).

# Gensoft — sync model

## Purpose

How Gensoft actually syncs: the SOAP pull, the **date-based incremental import**, the sweep frequencies, and how orders are pushed back (including the increment/decrement stock dance that follows the order lifecycle).

## Where to find it

No dedicated screen — this is the behaviour behind the **Status** tab (Start / Stop) and the **Orders** tab. The direction is set by **Action** on [[apps-gensoft-settings]].

## What the merchant can do here

Start / stop the sync, choose `Action` (import vs send-orders-only), and watch order pushes in the Orders tab.

## Settings & fields

No fields of its own — the levers (`Action`, `all_products`, `ten_minute_update`, send-all-products) are on [[apps-gensoft-settings]].

## Business rules

### CloudCart pulls Gensoft over SOAP

Unlike the XML-push ERPs, CloudCart **calls Gensoft's SOAP web service** to fetch articles, categories, prices and stock, and to push orders. The connection target is the `wsdl_url` ([[apps-gensoft-settings]]).

### Date-based incremental import (the `last_import` watermark)

The catalogue import is **incremental**: it asks Gensoft for articles **changed since the last import** (a stored `last_import` watermark; the paid fast sweep keeps its own `last_import_fast`). After a successful run the watermark advances, so each run only carries the delta. A first run (no watermark) pulls from the beginning. Clearing the watermark forces a full re-fetch — that is exactly what [[apps-gensoft-reset-import|Reset import]] does.

### Sync frequency

- **Products** (`gensoft_products`) + **categories** (`gensoft_categories`) — every **4 hours**.
- **Fast paid sweep** (`gensoft_products_paid`) — every **10 minutes**, only on the dedicated plan (the `ten_minute_update` option) — typically to catch price/stock changes on subscriber-flagged products.
- **Order resend** (`gensoft_resend_orders`) — every **6 hours**, resubmits orders that failed to push.

### Action mode

- **Import** — full catalogue import (+ order push).
- **Send orders only** — push orders, do **not** import the catalogue.

### Order export follows the order lifecycle (increment / decrement)

The order-event listener sends **decrement** instructions when the order is `pending`, `paid`, or `completed` (reduce Gensoft stock for items now sold), and **increment** for other statuses (e.g. `cancelled`, `refunded` — return stock). This is unusual among CloudCart ERPs (most push only final-state orders), so Gensoft stock tracks CloudCart's lifecycle closely. **Send all products** (on [[apps-gensoft-settings]]) decides whether every order line is sent or only Gensoft-imported ones. An order can also be **cancelled** in Gensoft from CloudCart (failure: *"Could not cancel order [order] in Gensoft."*).

### Double-decrement guard

A `gensoft_order_created_request_send` meta key marks that a decrement was already sent for an order; if set, a further decrement event is skipped — preventing double-decrement as an order moves through multiple "sold" statuses.

### Mid-flight line-item edits also sync

On `OrderProductAdd` / `OrderProductEdit` / `OrderProductRemove`, the listener queues a product-change job, keeping Gensoft's view of the order's lines in sync with edits made in CloudCart after the initial push — another behaviour most ERPs skip.

### Plan-gated faster queue

When the plan has `gensoft_update` enabled, all Gensoft order jobs route to the faster `system8` queue; otherwise the default queue — prioritising order sync for higher tiers.

### Order-history + logging

Successful syncs log `send_erp_success` in [[orders-history]]; failures log `send_erp_error` with the upstream message. Every status change also writes an internal debug log (visible to CC support, not the merchant).

## Related

- [[apps-gensoft]] — hub.
- [[apps-gensoft-settings]] — `Action`, `all_products`, `ten_minute_update`, send-all-products.
- [[apps-gensoft-reset-import]] — clears the `last_import` watermark to force a full re-fetch.
- [[apps-gensoft-product-matching]] — order push needs each line's Gensoft id from the mapping.
- [[orders-history]] — the `send_erp_success` / `send_erp_error` events.

## Open questions

(none)
