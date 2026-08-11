---
type: feature
nav_path: "Orders → Details → History"
route_name: admin.orders.details
route_path: /admin/orders/details/:order_id
aliases: ["Order history tab", "Order audit log", "Order activity"]
tags: [orders, order-details, history, audit-log]
plan_gates: []
created: 2026-06-10
updated: 2026-08-06
source_count: 3
---

> Part of [[orders-details]]. See the hub for the other aspects (header, products, addresses, payment, shipping, actions, known issues).

# Order details — History tab

## Purpose

The **History tab** on the order details page surfaces the per-order audit log — every status change, payment event, address edit, line-item add / edit / remove, discount change, fulfilment update, and admin-driven action gets a row with a timestamp + the acting admin or system actor. This is the merchant's first stop for "who changed what, when".

This page documents the SECTION as it appears on order details. The full audit-log catalogue — every action code, every initiator namespace, every message-data placeholder — is on [[orders-history]].

## Where to find it

On `/admin/orders/details/<order_id>`, the History tab is one of the tabs in the main column (alongside Order Summary and the action-row stack). Clicking it loads the history sub-template inline.

**A draft order shows no history at all** — both the heading and the timeline body are suppressed until the draft is committed with **Create order**. So a merchant who asks "why is the history empty on this order?" is almost always looking at a draft (see [[orders-add-draft-state]]).

## What the merchant can do here

### View

Each history entry is rendered as a row with:

- **Timestamp** — single `date` field used for created + updated.
- **Message** — translated message label, with placeholders interpolated from `message_data`.
- **Initiator** — the acting admin user, the app namespace (e.g., `api2` for JSON-API v2 changes), or "Edit from order #N" for cross-order origins.
- **Action code** — numeric, currently running 1–63 — referenced in [[orders-history-action-codes]].

### Filter / drill-down

The History tab itself is a chronological list. For detailed message-data placeholders (e.g., field-level diffs for address-edit and customer-edit actions), the merchant clicks the row to expand it. The history sub-template handles the expansion inline — see [[orders-history]] for the full field catalogue per action code.

## Settings & fields

The History tab has no editable fields — it's a read-only audit surface. The data is read from the per-order audit log table, which has 8 fields per entry:

- `order_id` — the parent order.
- `message` — translation key.
- `message_data` — JSON placeholders.
- `admin_id` — acting admin (null for system / API actors).
- `action` — numeric action code (62 defined codes running to 63; see [[orders-history-action-codes]]).
- `date` — single timestamp.
- `log_id` — FK to a detailed log payload (when applicable).
- `namespace` — acting app's namespace (e.g., `api2`, app codename).

## Business rules

### Granularity is per-action with field-level diffs

The audit log is per-action — one row per save event. For actions like address-edit and customer-edit, the `message_data` JSON includes field-level diffs (before / after) — the merchant sees exactly which fields changed.

### History rows come from many sources — but NOT from every action

Most saves on the order details page write a history row: status pill changes, mark-paid, refund, line-add / line-edit / line-remove, discount add / remove, address add / change / edit, customer edit, fulfilment add, admin-note edit, recalculate-lock toggle, currency conversion, archive / unarchive, and each stage of a return (issued / received / credit note / cancelled / refunded / exchange created). JSON-API v2 writes also append rows with `namespace = api2`.

Several things a merchant might expect to see are **not** logged, because no action type exists for them: waybill generation on its own, invoice-number generation, and credit-note creation as a standalone event. The canonical list of what IS logged is [[orders-history-action-codes]].

### The Notify-customer toggle writes NO history row

Flipping the **Notify customer** switch in the sidebar (see [[orders-details-actions]]) updates the flag **silently** — no timeline entry, no acting admin recorded. So *"who turned customer emails off on this order?"* **cannot** be answered from this tab. The merchant can only read the flag's current value. See [[orders-notify-customer-toggle]].

### Lock + unlock entries

The **Recalculate lock** toggle (see [[orders-details-actions]]) writes two action codes: 54 for `lock_order` and 55 for `unlock_order`. So the merchant can see exactly when the totals-recompute auto-suppress was toggled and by whom.

### Auto-promotion saves write a status-change row

When the **Auto-complete orders when paid & fulfilled** setting (`order_complete` on [[settings-cart]]) silently promotes `paid + fulfilled → completed` on save, the resulting status change writes a history row — so even silent promotions are traceable.

## Related

- [[orders-details]] — hub.
- [[orders-history]] — canonical audit-log page (full action-code catalogue + per-namespace decoding).
- [[order-processing-pipeline]] — events that emit history rows.
- [[orders-status-change]] — status-pill changes that write history rows.
- [[orders-payment-mark-paid]] / [[orders-payment-refund]] / [[orders-payment-capture]] / [[orders-payment-manual]] — payment actions that write history rows.
- [[orders-products]] — line-item edits that write history rows.
- [[orders-address-edit]] — address edits with field-level diffs in `message_data`.
- [[orders-history-action-codes]] — the definitive list of logged action types.
- [[orders-notify-customer-toggle]] — the notify-customer toggle, which is NOT logged.
- [[orders-details-returns]] — return events that write history rows.

## Open questions

None.
