---
type: feature
nav_path: "Orders → List → Status taxonomy"
route_name: admin.orders
route_path: /admin/orders/list
aliases: ["Order statuses", "Canonical order statuses", "11 hard-coded statuses", "NEGATIVE_STATUS", "Custom statuses as sub-labels", "Таксономия на статуси на поръчки"]
tags: [orders, list, statuses, taxonomy, negative-status, custom-statuses]
plan_gates: []
created: 2026-06-10
updated: 2026-08-06
source_count: 3
---

> Part of [[orders]]. See the hub for the other aspects (columns, filters, bulk actions, default visibility, export, locking).

# Orders list — status taxonomy

## Purpose

The canonical taxonomy of order statuses surfaced everywhere in the Orders list: the Status column badge, the **Status** filter, the bulk-status dropdown, the per-order status pill. There are **exactly 11 hard-coded statuses** — 4 positive flow + 7 negative flow. Custom statuses defined by the merchant in [[settings-statuses]] are **sub-labels** that layer onto these — not replacements.

## Where to find it

The taxonomy is surfaced in:
- The **Status** column badge in the list (see [[orders-list-columns]]).
- The **Status** filter on the filter bar (see [[orders-list-filters]]).
- The bulk-status dropdown (see [[orders-list-bulk-actions]]).
- The per-order status pill on [[orders-details]] (see [[orders-details-header]]).

Custom-status configuration lives on [[settings-statuses]].

## What the merchant can do here

### The 11 canonical statuses (verified)

**Positive flow (4 statuses):**

- `authorized` — payment authorized but not captured.
- `pending` — order placed, not yet paid.
- `paid` — payment captured.
- `completed` — fulfillment done.

**Negative flow (7 statuses — the `NEGATIVE_STATUS` array):**

- `voided`
- `timeouted` — payment timeout.
- `cancelled`
- `failed`
- `refunded`
- `chargebacked`
- `disputed`

The `NEGATIVE_STATUS` array is referenced throughout the platform for filtering and business logic (e.g., "don't count chargebacked / cancelled orders in revenue").

### Bulk-status dropdown REMOVES 5 statuses

The bulk-status (and inline status-pill) dropdown surfaces only 6 of the 11 canonical statuses to the merchant — **pending, authorized, paid, completed, cancelled, refunded**. The five removed are: `chargebacked`, `disputed`, `timeouted`, `failed`, `voided`. Orders reach those statuses ONLY through automated transitions (payment-gateway webhooks, the payment-provider integration's own logic). See [[orders-list-bulk-actions]] for the bulk path and [[orders-details-header]] for the per-order status pill.

The dropdown also offers the two **fulfillment statuses** (Fulfilled / Not fulfilled) and the merchant's own custom statuses on top of the 6 canonical ones. (`abandoned` and `requested` are NOT canonical order statuses and do NOT appear in this dropdown.)

### Custom statuses (per [[settings-statuses]]) are SUB-LABELS

The 11 statuses are the CANONICAL taxonomy. Merchant-defined custom statuses are typically sub-labels / colour-codes that layer onto these — useful for kanban-style workflows but don't replace the canonical taxonomy. Behaviour:

- The platform's hard-coded `completed` status is what bulk-complete sets. Merchants who define custom substatuses CANNOT bulk-set them; only the core 11 statuses are first-class.
- A custom status is associated with a parent canonical status (see [[settings-statuses]]). Transitioning the order to the custom status implicitly puts it in the parent canonical bucket.
- The Status filter shows custom statuses alongside the canonical ones; selecting "Paid" matches all orders whose parent canonical status is `paid`, including those tagged with a "Paid: ready to ship" custom sub-label.

## Settings & fields

The 11 canonical statuses are platform constants — not editable. [[settings-statuses]] lets the merchant rename them and add custom statuses; the status record carries only its type, key and display name.

There is **no per-status customer-notification toggle**. One status-change email template serves every status. Whether it fires is decided by the order's `notify_customer` flag (see [[orders-notify-customer]]), the template's own active flag, and the store-wide `customer_email_notifications` switch — the latter two on [[marketing-omnichannel-mails-list]].

## Business rules

### `NEGATIVE_STATUS` membership drives platform-wide logic

The 7-status `NEGATIVE_STATUS` array is the platform's "this order doesn't count" predicate. Implications:

- Orders in `NEGATIVE_STATUS` are excluded from revenue / GMV reports.
- Stock is restocked on transition INTO any negative status — see [[inventory-restock]].
- Payment authorisation auto-cancels on transition INTO any negative status — see [[orders-payment-capture]].
- Customer income totals (lifetime value) recompute to exclude the order.
- Discount uses counters decrement to release the discount-code redemption.

### Default list silently HIDES `cancelled` AND `voided`

When the merchant lands on **Orders** with NO filters applied, the grid silently excludes orders whose status is `cancelled` or `voided` — even though they're full canonical statuses. To see them the merchant must add a **Status** filter (Is cancelled / Is voided). The moment ANY filter is applied (even unrelated to status), the cancelled / voided exclusion is dropped. See [[orders-list-default-visibility]] for the full rule + the related Archive exclusion.

### Custom status (audit-log action code 53) renders status name from taxonomy at view time

When a merchant changes the order to a custom status, the audit row stores action code `53` and the custom status KEY. At view time, the platform looks up the current name of that status from the status taxonomy. If the merchant later RENAMES the custom status, OLD history entries display the NEW name — the audit log is not snapshot-frozen for custom statuses. See [[orders-history]].

### Auto-promotion to `completed` is silent

Every save of an order with **Auto-complete orders when paid & fulfilled** ON (`order_complete` — default ON on [[settings-cart]]) silently rewrites `status = completed` if the order is `paid` AND `status_fulfillment = fulfilled`. This applies to ANY save, not just status changes — see [[orders-list-locking]] for the full caveat and how it interacts with the order-lock window.

### Status badge colour scheme

The status badge's CSS class depends on combined state (full table on [[orders-details-header]]): Completed / Paid → green, Cancelled → red, Pending+Not-fulfilled → orange, Pending+Fulfilled → purple, custom → blue, Archived → gray.

### Status is NOT directly sortable in the list

The list lets the merchant sort by Order number, Date, Total — but NOT by Status (see [[orders-list-columns]]). To group by status, the merchant applies a Status filter instead.

## Related

- [[orders]] — hub.
- [[orders-list-filters]] — Status filter target values.
- [[orders-list-bulk-actions]] — bulk-status dropdown (restricted subset).
- [[orders-list-default-visibility]] — cancelled / voided default-hide rule.
- [[orders-list-locking]] — auto-promotion to `completed` on save.
- [[settings-statuses]] — custom-status configuration + per-status email toggle.
- [[orders-status-change]] — per-order status-change flow + transition gates.
- [[orders-details-header]] — per-order status pill UX.
- [[orders-history]] — audit-log rendering of custom-status name lookups.
- [[orders-payment-capture]] — payment authorisation auto-cancel on negative-status transition.
- [[inventory-restock]] — automatic stock return on negative-status transition.
- [[orders-notify-customer]] — per-order email-suppression toggle.
- [[order-processing-pipeline]] — full side-effect chain per status transition.

## Open questions

None.
