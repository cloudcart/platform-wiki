---
type: feature
nav_path: "Orders → List → Bulk actions"
route_name: admin.orders
route_path: /admin/orders/list
aliases: ["Orders bulk actions", "Bulk archive orders", "Bulk unarchive orders", "Bulk mark complete", "Bulk-status orders", "Масови действия върху поръчки"]
tags: [orders, list, bulk-actions, archive, mark-complete, smarty]
plan_gates: []
created: 2026-06-10
updated: 2026-08-06
source_count: 5
---

> Part of [[orders]]. See the hub for the other aspects (columns, filters, status taxonomy, default visibility, export, locking).

# Orders list — bulk actions

## Purpose

The list lets the merchant select multiple rows via checkboxes, then run a single bulk action against them: **Archive**, **Unarchive**, or **Mark as completed**. There are exactly three bulk actions — no bulk-delete, no bulk-cancel, no bulk-refund. Bulk Mark as completed is the most consequential because it fires per-order customer-notification emails.

## Where to find it

Row checkboxes on `/admin/orders` (leftmost column). Selecting at least one row reveals the bulk-action bar above or below the table; choosing an action triggers a confirmation dialog.

## What the merchant can do here

### The three bulk actions

| Action | Confirmation dialog (verbatim) | What it does |
|--------|---|--------------|
| **Archive** | *"This will archive your order. Please confirm."* | Moves selected orders to archive (hidden from the default list) — **only if every one of them is `completed` or `cancelled`**, see below. |
| **Unarchive** | *"Do you want to unarchive?"* | Restores selected orders from archive. No status restriction. |
| **Mark as completed** | *"Are you sure you want to complete this order? If you mark it as completed, you will not be able to change its status never again."* | Sets the order status of all selected to **Completed**. Fires per-order customer notification emails. |

Two things to note about the strings: all three are phrased in the **singular** ("your order", "this order") even though they run on a whole selection, and the Mark-as-completed one explicitly warns that the change is **irreversible** — that is the strongest warning in the Orders area and it is accurate: `completed` is a terminal status for the pill.

There is **no bulk-delete** action — and no per-order delete either. Orders are archived, never deleted (see [[orders-archive]]).

### Bulk endpoints (route names)

- Archive: `admin.orders.archive-bulk` route, action `yes`.
- Unarchive: `admin.orders.archive-bulk` route, action `no`.
- Mark as completed: `admin.orders.bulk-status` route, status `completed`.

All three routes accept a list of selected IDs driven by the row checkboxes.

### Bulk-status dropdown is RESTRICTED to a subset of statuses

While there are 11 canonical statuses (see [[orders-list-status-taxonomy]]), the bulk-status (and inline status-pill) dropdown REMOVES five of them: `chargebacked`, `disputed`, `timeouted`, `failed`, `voided`. So the merchant CANNOT bulk-set any of those — they're only reachable via automated transitions (payment-gateway webhooks, the payment-provider integration's own logic). The dropdown effectively offers the six remaining canonical statuses — **pending, authorized, paid, completed, cancelled, refunded** — plus the two fulfillment statuses (Fulfilled / Not fulfilled) and the merchant's own custom statuses. (`abandoned` and `requested` are NOT canonical order statuses and do NOT appear here.)

## Settings & fields

There is **one** status-change customer email template shared by every status — there is no per-status "send email to customer" toggle anywhere. Three things gate it: the per-order `notify_customer` flag (see [[orders-notify-customer]]), the template's own active flag, and the store-wide `customer_email_notifications` switch — both of the latter on [[marketing-omnichannel-mails-list]].

There is no UI toggle on the bulk action to override either of these — the bulk path runs the standard pipeline per order.

## Business rules

### Bulk Mark as completed propagates customer notifications

When the merchant bulk-completes orders, the underlying status-change pipeline runs per order — which means the store's single status-change customer email goes out for each one. The merchant should NOT bulk-complete unless they want each affected customer to receive it.

There is **no UI toggle** on the bulk action to suppress emails, and no per-status notification setting to switch off. The options are to first toggle `notify_customer = no` on each order in [[orders-details]] (see [[orders-notify-customer]]), or to deactivate the status-change email template in [[marketing-omnichannel-mails-list]] for the duration.

### Bulk Archive is status-gated — one bad row kills the whole batch

Archiving only accepts orders whose status is **`completed` or `cancelled`** (drafts are exempt and can be archived in any state). The whole selection runs as a **single transaction**, so if even one selected order is `pending`, `paid` or `refunded`, that order throws and **the entire batch is rolled back** — nothing is archived at all. The merchant sees only the error *"Only completed orders can be archived."*, with no indication of which order caused it.

The reliable workflow is: filter the list to `completed` / `cancelled` first, then select-all and archive. Note the message is slightly misleading — cancelled orders are allowed too.

**Unarchive has no restriction** and cannot fail this way.

### Bulk Mark as completed can report success and change nothing

The bulk status change validates each order in turn: `completed` is refused only when the order is **neither** `paid` **nor** fulfilled (either one on its own is enough, so a paid-but-unshipped order completes fine); archived orders are refused outright, as are orders locked after a cancellation / refund.

There is also a **payment-authorisation check**: if a selected order still carries an authorisation hold that does not cover its total, the batch **stops at that order**. The consequential part is that it stops *silently* — the merchant still gets a **success** response. Orders processed before the offending one are committed; the offending order and **every order after it** are left untouched, with no error shown.

So after bulk-completing a large mixed selection, the merchant should **re-check the list** rather than trust the success toast. Running the same action on a single order from its detail page does surface the error properly.

### Archive / Unarchive do NOT change status

Bulk Archive sets only the archived flag — it does NOT change the order's status or fulfillment, does NOT fire customer-notification emails, does NOT touch stock. Archived orders disappear from the default list (see [[orders-list-default-visibility]]) but remain queryable via the **Archived = Yes** filter. Unarchive is the symmetric inverse.

For the per-order archive surface (toggle from inside [[orders-details]]'s header dropdown), see [[orders-archive]].

### Selection persists only within the current filtered view

Row checkboxes don't survive a filter change or page reload. The merchant must finish the bulk action before changing filters, or the selection resets.

### Side effects of save apply to each order in the batch

Bulk Mark as completed runs the full order-event chain PER ORDER: stock recompute (see [[inventory-tracking]] / [[inventory-decrement-timing]]), invoice / receipt number generation if configured, customer income totals recompute (async), discount usage counters increment, `order.updated` webhook (see [[settings-hooks]]), audit log row written with `bulk` as the acting source. Full pipeline: [[order-processing-pipeline]].

## Related

- [[orders]] — hub.
- [[orders-list-status-taxonomy]] — canonical statuses; explains the dropdown restriction.
- [[orders-list-default-visibility]] — what Archive / Unarchive hide and reveal.
- [[orders-archive]] — per-order archive toggle (single-order alternative to bulk Archive).
- [[orders-status-change]] — the per-order status-change flow that bulk-complete invokes.
- [[orders-notify-customer]] — per-order customer-notification toggle.
- [[orders-details]] — per-order editing (no delete action exists there either).
- [[settings-statuses]] — per-status customer-email config.
- [[settings-hooks]] — `order.updated` webhook fires per-order.
- [[order-processing-pipeline]] — the chain of side-effects each order in the batch triggers.

## Open questions

None.
