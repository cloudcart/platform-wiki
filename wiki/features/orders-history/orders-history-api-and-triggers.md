---
type: feature
nav_path: "Orders → Order details → History → API & triggers"
route_name: admin.orders.history
route_path: /admin/orders/action/history/:order_id
aliases: ["Order history triggers", "What writes a history row", "Order history API", "History via JSON-API v2", "История — източници"]
tags: [orders, history, audit, api, smarty]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[orders-history]]. See the hub for the other aspects (timeline UI, action codes, record model, synthetic entries, enrichment, acting party).

# Order history — what writes a row (triggers & API)

## Purpose

The audit log is populated as a **side effect** of order operations — the merchant never adds a row by hand. This page lists what actually writes a history entry, and explains that mutations through JSON-API v2 land in the **same** log as admin-panel actions (so API-driven changes are auditable too).

## Where to find it

The written rows surface in the History panel on [[orders-details]] — see [[orders-history-timeline-ui]]. This page covers the originating operations, not a screen.

## What the merchant can do here

The merchant cannot write history rows directly. What they CAN do is rely on the log to capture changes from **all** sources — admin panel, apps, and JSON-API v2 — so that an external integration changing an order leaves an auditable trace.

## Settings & fields

No editable settings. The recognised write sources are the admin panel, apps (via their namespace), and JSON-API v2 (namespace `api2`).

## Business rules

### History rows are written by the listener pipeline

History rows are produced by the platform's listener pipeline as a side effect — not added manually. The most merchant-relevant triggers (verified):

- **Order created** — synthetic only (NOT stored; prepended at view time — see [[orders-history-synthetic-entries]]).
- **Status change** — written automatically by the status-change handler for canonical statuses, plus a separate custom-status row for custom-status changes. See [[orders-status-change]].
- **Address change / edit / reposition** — written by the address-update flow. See [[orders-address-edit]].
- **Customer change / edit** — written by the customer-change flow. See [[orders-customer-change]].
- **Product add / edit / remove** — written by the product-line management flow. See [[orders-products]].
- **Discount add / remove** — written for both line-level and order-level discounts. See [[orders-discount-add]].
- **Fulfillment add / remove** — written by the fulfillment generation flow (waybill creation). See [[orders-shipping-waybill]].
- **Note edit** — written by the note-edit route.
- **Lock toggle** — written when the merchant flips the recalculate-lock from order details.
- **Currency convert** — written when the merchant converts the order's currency (e.g., BGN→EUR migration).
- **Archive / unarchive** — written by the archive toggle.
- **App events** — third-party apps call into the same history pipeline using their app namespace.

### JSON-API v2 mutations write to the SAME log

Mutations made through JSON-API v2 (see [[api-orders]]) appear in the **same** history table alongside admin-panel actions — every status PATCH, fulfillment POST, etc. writes a row.

### `api2` is the only externally-recognised namespace

When an action is triggered through JSON-API v2, the platform stores `api2` in the row's `namespace` field. This is the **only** namespace value that gets a friendly display label — it renders as **"API"** in the timeline. All other integration namespaces (apps, listeners) render the row as *"No such admin"*. See [[orders-history-acting-party]] for the full chain.

### The audit log is NOT a JSON-API v2 resource

The history itself is **not** exposed as a JSON-API v2 resource — it is read through the admin-panel view only. There is no API endpoint to fetch or write history rows directly; the API only *causes* rows by mutating orders.

### Abandoned-cart recovery banner trigger

When the order's `abandoned` flag is set AND a `restore_source` exists, the timeline shows a recovery banner — the trigger comes from [[marketing-campaigns]] recovery flows. The banner rendering is documented in [[orders-history-timeline-ui]].

### Side effects

None on this read surface. The history WRITE is itself the side effect of the order operations above. See [[json-api-v2]] for the platform-wide side-effects principle.

## Related

- [[orders-history]] — hub.
- [[orders-history-acting-party]] — why `api2` is shown as "API" and others as "No such admin".
- [[orders-history-synthetic-entries]] — why "order created" is not a stored trigger.
- [[orders-history-timeline-ui]] — the recovery banner rendering.
- [[api-orders]] — JSON-API v2 endpoint whose mutations emit `api2` rows.
- [[json-api-v2]] — API overview + side-effects principle.
- [[orders-status-change]] / [[orders-address-edit]] / [[orders-customer-change]] / [[orders-products]] / [[orders-discount-add]] / [[orders-shipping-waybill]] — flows that write history rows.
- [[marketing-campaigns]] — abandoned-cart recovery behind the banner.

## Open questions

None.
