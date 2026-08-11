---
type: feature
nav_path: "Orders → Bulk → Status change"
route_name: admin.orders.bulk-status
route_path: /admin/orders/action/bulk-status
aliases: ["Bulk status change", "Bulk mark as completed", "Bulk archive", "Bulk unarchive", "Bulk status fail-fast"]
tags: [orders, status, bulk, transactions]
plan_gates: []
created: 2026-06-10
updated: 2026-08-06
source_count: 3
---

> Part of [[orders-status-change]]. See the hub for the other aspects (pill, transition rules, side effects, notification, fulfillment gate, API).

# Order status change — Bulk

## Purpose

The [[orders]] list exposes three bulk-status actions: **Archive**, **Unarchive**, and **Mark as completed**. The bulk processor wraps the entire selection in a single DB transaction and is **fail-fast**: the first order to fail any gate aborts the whole batch and NONE of the orders are updated. This page documents the bulk-only behaviours that differ from per-order status changes — the fail-fast model, the notification multiplier, and why bulk actions for other statuses are deliberately absent.

## Where to find it

[[orders]] list → tick the orders → click the bulk-actions dropdown above the list. Three status actions are exposed:

1. **Archive** — moves selected orders to archived state (filtered out of default views).
2. **Unarchive** — un-archives the selected orders.
3. **Mark as completed** — runs `validateChangeStatus` per order with target = `completed`.

Each opens a confirmation dialog before executing:

- *"Are you sure you want to archive these orders?"* (`order.order_archive_are_you_sure`).
- *"Are you sure you want to unarchive these orders?"* (`order.order_unarchive_are_you_sure`).
- *"Are you sure you want to mark as completed?"* (`order.order_complete_are_you_sure`).

The bulk dropdown also exposes other actions (Print, Export, etc. — see [[orders]] for the full bulk-action inventory). Only the three status actions above are covered on this page.

## What the merchant can do here

### Three bulk status actions — no Cancel / Paid / Refunded

The bulk dropdown is deliberately minimal — only Archive / Unarchive / Mark as completed are bulk-exposed. There is NO bulk action for:

- Cancel (would require per-order `quantity_enough` check + payment-authorization release).
- Paid (would require per-order payment-provider gating).
- Refunded (would require per-order credit-note + refund-handling).
- Any custom status.

A merchant wanting to mass-cancel an old set of pending orders has to click into each one. This is by design — bulk Cancel is operationally risky (it fires customer emails + stock restores + authorization releases per order) and the platform leaves it as a per-order decision.

### Fail-fast on first error — WHOLE batch rolls back

The bulk-status processor wraps the entire batch inside a SINGLE database transaction with no per-order error containment. The moment ONE order fails ANY gate, the platform throws and rolls back the WHOLE transaction. NONE of the selected orders are updated — including any that had already been processed within the transaction.

Common failure modes that abort a bulk:

- **Transition rule violation** — e.g., one order in the selection is `Pending` and unfulfilled while the bulk is Mark as completed (which needs `Paid` **or** `Fulfilled`). The first such order aborts the batch.
- **Archived block** — one order in the selection is archived; Mark as completed on archived is blocked.
- **Under-authorised order** — one order's payment authorisation is smaller than its total. That check runs before the target status is even looked at, so it aborts the batch regardless of which status was requested.
- **Invalid status code** — shouldn't happen via the UI but possible via direct route hits.

The merchant sees only the FIRST failing order's error message. Successive orders in the selection are not processed and their pre-existing state is preserved (rolled back).

### Bulk Archive / Unarchive — simpler gates

The Archive / Unarchive bulk actions don't go through `validateChangeStatus` — they flip the archived flag directly. They have fewer failure modes and typically succeed across mixed selections. The merchant can safely bulk-archive a mix of completed / cancelled / refunded orders without hitting the fail-fast model.

### Mixed-status bulk Mark as completed — common pitfall

A merchant selecting a mix of `paid` orders and unfulfilled `pending` orders for bulk Mark as completed WILL hit the fail-fast model on the first `pending` one — none of the orders get marked completed, including the `paid` ones that would have succeeded individually (a `paid` order completes fine whether or not it is fulfilled). The merchant has to:

1. Filter the list to `paid` (or `fulfilled`) orders FIRST (via the [[orders]] list filters).
2. Then bulk-select and Mark as completed.

The error message identifies only the first failing order — the merchant has to re-filter and re-bulk-select to identify other unprocessable orders.

### Customer-notification multiplier

The customer-notification switches (see [[orders-status-change-notification]]) apply per order in the bulk — so bulk-completing 100 orders where all three allow it fires 100 outbound emails. This is the most common surprise of bulk operations: "I bulk-completed and got 100 customer complaints about a notification email".

Mitigations before a bulk:

1. Untick "Notify customer" on the target status in [[settings-statuses]] globally before the bulk, then re-enable afterward.
2. Toggle each order's `notify_customer = 0` first (but this defeats the speed of bulk).
3. Deactivate the status-change email template, or use the store-wide kill switch `customer_email_notifications` (test / dev stores only). There is no per-status notification toggle.

## Settings & fields

The bulk-status flow consumes the same settings as the per-order flow:

- [[settings-statuses]] — status taxonomy (rename / add custom).
- [[settings-cart]] — `order_status_for_quantity_decrease` (decrement timing, snapshotted per order at placement).
- [[marketing-omnichannel-mails-list]] — status-change email template + the store-wide `customer_email_notifications` kill switch.
- [[settings-hooks]] — `order.updated` webhook fires PER order in the bulk.

## Business rules

- The bulk action runs inside a SINGLE DB transaction. If ANY order fails ANY gate, the whole transaction rolls back. There is NO partial-success mode.
- Side effects fire per order — for a 100-order bulk that succeeds entirely: 100 pairs of history rows, 100 webhooks, up to 100 emails, 100 invoice / receipt numbers, 100 stock movements.
- The bulk processor unlocks DB tables before the transaction (a workaround for legacy table-lock issues; wrapped in error handling). `(verify if still needed after the latest order-table migration)`.
- The bulk action does NOT support a "dry-run" / "preview which would fail" mode. The merchant has to attempt the bulk and read the error.
- Bulk Mark as completed honours `notify_customer` per order — orders with `notify_customer = 0` won't email. So a merchant can pre-flip `notify_customer = 0` on selected orders before the bulk to silence emails for that batch.
- The bulk processor is admin-panel-only — there is NO bulk-status endpoint in JSON-API v2. Integrators must PATCH orders one-by-one via [[api-orders]] (each PATCH is a separate request and a separate side-effect chain). See [[orders-status-change-api]].

## Programmatic access

There is no JSON-API v2 bulk-status endpoint. To mass-update statuses programmatically, integrators iterate `PATCH /orders/:id` calls — each call is a separate transaction with its own side-effect chain. This gives integrators per-order error containment that the admin bulk action does NOT provide. See [[orders-status-change-api]].

## Related

- [[orders-status-change]] — hub.
- [[orders]] — list page hosting the bulk-actions dropdown.
- [[orders-status-change-transition-rules]] — gates that determine which orders fail in a mixed bulk.
- [[orders-status-change-notification]] — multiplier risk; pre-bulk mitigations.
- [[orders-status-change-side-effects]] — side effects fire per order.
- [[orders-archive]] — bulk archive / unarchive flow.
- [[orders-status-change-api]] — JSON-API v2 has no bulk endpoint; iterate instead.

## Open questions

- Whether the legacy table-unlock workaround is still required after the latest order-table migration `(verify)`.
- Whether a future update will expose a "preview / dry-run" mode for bulk Mark as completed `(verify)`.
