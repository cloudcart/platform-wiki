---
type: feature
nav_path: "Orders → Order details → History → Synthetic entries"
route_name: admin.orders.history
route_path: /admin/orders/action/history/:order_id
aliases: ["Order history synthetic entries", "Derived history rows", "Order creation row", "Receipt-sent history row", "История — синтетични записи"]
tags: [orders, history, audit, smarty]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[orders-history]]. See the hub for the other aspects (timeline UI, action codes, record model, enrichment, acting party, API & triggers).

# Order history — synthetic (view-time) entries

## Purpose

Two entries always appear in the timeline that are **NOT** stored in the history table — they are constructed at view time. This page explains which two, why, and what that means for anyone reconciling the on-screen timeline against the stored data.

## Where to find it

These entries appear inline in the History panel on [[orders-details]], interleaved with the stored rows. To the merchant they look identical to any other entry — the synthetic origin is invisible in the UI. See [[orders-history-timeline-ui]] for the rendering.

## What the merchant can do here

Nothing special — the merchant reads them like any other entry. The practical takeaway: the **order creation** line and (when applicable) the **receipt-sent** line are always present even if no corresponding row exists in the audit table.

## Settings & fields

No editable settings. The two synthetic entries are:

| Synthetic entry | Built from | When it appears |
|---|---|---|
| `order_add` (order created) | The order's `date_added` + customer info | Always — prepended to the top of the timeline. |
| `order_receipt_sent` | The active invoicing app's receipt date | Only when the active invoicing app has issued a receipt; positioned chronologically by the receipt date. |

## Business rules

### The creation row is prepended, not stored

When the merchant opens the order's history, the platform **prepends** a synthetic `order_add` entry constructed from the order's `date_added` and customer info. This row does not exist in the audit table — it is always derived. This guarantees every order shows a creation event at the top of its timeline even though the platform doesn't write a stored creation row (the creation trigger is "synthetic only" — see [[orders-history-api-and-triggers]]).

### The receipt-sent row is inserted by receipt date

When the active invoicing app has issued a receipt, the platform **inserts** a synthetic `order_receipt_sent` entry, positioned chronologically by the receipt's date rather than appended at the end. This keeps the receipt event in correct time order relative to the stored rows around it.

### Consequence — the timeline is NOT a pure database read

Because these two entries are derived at view time, the rendered timeline is **always** the stored rows (see [[orders-history-record-model]]) PLUS up to two synthetic entries. Anyone reconciling on-screen entries against stored data must account for the gap: the creation row and the receipt-sent row will not be found in the table.

### Side effects

None — these are read-time constructions only.

## Related

- [[orders-history]] — hub.
- [[orders-history-record-model]] — the stored rows these two are added to.
- [[orders-history-timeline-ui]] — how they render alongside stored rows.
- [[orders-history-api-and-triggers]] — why order creation is "synthetic only" and not stored.
- [[orders-receipt]] — the receipt the synthetic `order_receipt_sent` row reflects.

## Open questions

None.
