---
type: concept
nav_path: "Concept → Order status workflow"
route_name: (none)
route_path: (none)
aliases: ["Order status workflow", "Order lifecycle", "Order status transitions", "How order statuses change", "Status flow", "Order state machine", "Работен процес на статуси", "Жизнен цикъл на поръчка", "Преходи на статуси", "Поток на статуси"]
tags: [orders, statuses, lifecycle, notifications, webhooks, concepts]
plan_gates: []
created: 2026-05-23
updated: 2026-08-06
source_count: 7
---

# Order status workflow

## Definition

The **lifecycle every order moves through** from "placed" to "done" — and the rules that govern what the merchant can DO with the order at each step. Every order carries a single `status` field (one of **11** platform-defined values) plus an independent `status_fulfillment` field (two values: `not_fulfilled`, `fulfilled`) plus an optional **custom status** layered on top by the merchant from [[settings-statuses]]. Together those values decide whether the order shows in revenue reports, whether stock is decremented, whether discount uses are counted, whether invoices and credit notes can be issued, whether the customer can be emailed, and which webhooks fire for the merchant's external systems.

The platform **does** enforce transition rules — they are just narrow rather than a full state machine. Five rules are refused outright: `completed` needs the order to be `paid` **or** `fulfilled`; `cancelled` is refused from `paid` / `completed`; `abandoned` is not a settable status at all; an archived order cannot change status; and a cancelled / refunded order that already carries a return record or a credit note is **locked** and can only toggle between `cancelled` and `refunded`. Everything outside those rules moves freely. On top of transitions, several **gates** restrict the downstream actions available in each status (e.g., refund only after paid; credit note only after `cancelled` / `refunded` with an invoice; line-item edits only in `pending` / `paid` / `authorized`).

Merchant mental model: the status says where this order is in MY workflow; the platform watches it and triggers the side effects (emails, stock, accounting, webhooks). Custom statuses add sub-labels ("Awaiting confirmation", "In production", "Ready to ship") on top of the 11 built-ins without breaking the underlying logic.

## Sub-pages (in this cluster)

Split into 7 aspect pages. Drill into the one that matches the question, not all of them.

- [[order-status-taxonomy]] — the 11 canonical statuses (4 positive + 7 negative) and the parallel 2-value fulfillment dimension; what each value means.
- [[order-status-custom]] — merchant-added custom statuses via [[settings-statuses]]; how they layer on top of the 11 built-ins and what semantics they DON'T inherit.
- [[order-status-transitions]] — manual, bulk, and API-driven status changes; the dropdown vs full-list distinction; archived-order lock; shipping-integration locks; status rename safety.
- [[order-status-auto-transitions]] — auto-promotion to `completed` (the `order_complete` setting), banned-IP auto-cancel, gateway-driven moves, the draft sub-state (`is_draft`).
- [[order-status-side-effects]] — the side-effect cascade fired on every status change (stock, invoice / receipt numbers, webhook, customer email, history, discount recount, authorisation release, auto-created return) and when the gateway paths suppress most of it.
- [[order-status-negative-semantics]] — the 7 negative statuses; revenue exclusion, fulfillment reset, payment-authorisation release, the auto-created system return, and the reversal lock.
- [[order-status-action-gates]] — what the merchant CAN do per status (edit / refund / complete / invoice / credit note / cancel); the action-availability table.

## Scope

What this cluster covers (across the 7 sub-pages, listed above): the 11 canonical statuses + 2 fulfillment statuses; transition mechanics (manual, bulk, automatic); the side-effect cascade on every change; action gates per status; the draft sub-state for admin-placed orders; custom statuses + their limited semantics; the archived-order lock.

What it does NOT cover:

- The status **taxonomy management UI** (renaming, adding custom, deleting custom) — that's [[settings-statuses]].
- The **payment status** lifecycle (the money side, with its own values) — that's [[payment-status]].
- **Invoice / credit-note / receipt issuance** flows — those are [[orders-invoice]] / [[orders-credit]] / [[orders-receipt]].
- The **abandoned-cart recovery** flow that creates orders — that's [[orders-abandoned]].
- **Carrier-side fulfillment** (waybill generation, tracking) — that's [[orders-shipping-waybill]] and the carrier apps.

## Contrasts

- **Order status vs. payment status** ([[payment-status]]) — order status answers "where is this order in MY workflow?"; payment status answers "where is the money?". An order can be `completed` while its payment is `refunded`. Two independent fields with independent transitions.
- **Order status vs. fulfillment status** — order status spans 11 values across the full lifecycle; fulfillment status has only 2 (`not_fulfilled`, `fulfilled`) and tracks ONLY whether the courier has shipped. The two combine. See [[order-status-taxonomy]].
- **Built-in vs. custom statuses** — the 11 built-ins are platform-wired with full side effects (revenue exclusion, discount-use counting, stock decrement). Custom statuses are extra labels and do NOT participate in those semantics. See [[order-status-custom]].
- **Status change vs. archive** — changing status updates `status`; archiving sets `date_archived` and HIDES the order from the default list. Both are reversible, but an archived order cannot have its status changed until unarchived. See [[order-status-transitions]].
- **Archived lock vs. reversal lock** — the archived lock lifts as soon as the merchant unarchives. The reversal lock does not: once a cancelled / refunded order carries a return record or an issued credit number, it can only toggle between `cancelled` and `refunded`. See [[order-status-negative-semantics]].
- **Auto-promotion vs. manual completion** — when `order_complete = 1` on [[settings-cart]], `paid` + `fulfilled` auto-promotes to `completed` in the same save. With `order_complete = 0`, the merchant must manually pick `completed`. See [[order-status-auto-transitions]].
- **Webhook payload vs. UI label** — webhooks carry the status CODE (`paid`, `cancelled`); the admin UI / customer emails carry the merchant's renamed label. External integrations sync on stable codes regardless of merchant renames. See [[order-status-side-effects]].

## Why it matters to the merchant

- **Reporting accuracy.** Dashboards filter by status; negative-status orders are excluded from "income" totals, customer LTV, and segment counts. See [[order-status-negative-semantics]].
- **Customer communication.** There is ONE status-change email template for all statuses — it is not per-status. Whether it goes out depends on the order's `notify_customer` flag, the template's own on/off switch, and the store-wide `customer_email_notifications` switch. See [[order-status-side-effects]].
- **Stock control.** Stock decrements according to the order's snapshotted decrement setting (`order_status_for_quantity_decrease`, seeded as `pending` for new stores — [[inventory-decrement-timing]]); cancel or refund returns it automatically.
- **Discount accounting.** A discount's `uses` counter increments only on a counted status (default `paid`, `completed`, `fulfilled`). Cancelled orders don't consume a discount slot.
- **Edit availability.** Edit line items, change addresses, mark paid, and refund are gated by current status. See [[order-status-action-gates]].
- **Accounting documents.** Invoices, credit notes, and receipts have their own status requirements before issuance.
- **Webhook fan-out.** Every status change emits an `order.updated` webhook to all subscribed apps ([[settings-hooks]]).

## Where it applies

- [[order]] — the entity whose `status` field is the subject.
- [[orders]] — list view with status filters and the bulk "Mark as completed" action.
- [[orders-details]] — per-order edit hub; the status pill lives in the breadcrumb.
- [[orders-status-change]] — the dedicated single + bulk status-change flow.
- [[orders-history]] — every transition appears as an audit-log row.
- [[settings-statuses]] — taxonomy management for renaming built-ins and adding custom.
- [[settings-cart]] — `order_complete` (auto-promotion) and `order_status_for_quantity_decrease` (stock trigger).
- [[settings-hooks]] — webhook subscribers for `order.created` / `order.updated` / `order.deleted`.
- [[orders-credit]] — credit-note gate (status `cancelled` / `refunded` + invoice).
- [[orders-invoice]] — invoice issuance is status-aware.
- [[orders-archive]] — archived orders cannot transition.
- [[orders-notify-customer]] — per-order email suppression.

## Programmatic access

This entire workflow applies **identically when status is changed through JSON-API v2** ([[api-orders]]). The platform has no "side-effect-skipping mode" for API mutations — every status change runs through the same pipeline regardless of source. See [[order-status-transitions]] for the API-settable subset and [[order-status-side-effects]] for the cascade.

## Related

(Cross-links already cited in *Sub-pages*, *Contrasts*, *Why it matters*, and *Where it applies* are not repeated here.)

- [[order-status]] — entity page enumerating the 11 + custom values.
- [[shipping-status]] — fulfillment-status taxonomy (2 values).
- [[notifications]] — email templates per status.
- [[notification-delivery]] — how the platform actually sends those emails.
- [[settings-banned-ip]] — auto-cancel rules.
- [[cart-vs-order-lifecycle]] — how a cart becomes an order in the first place.
- [[checkout-flow]] — the customer-side flow producing the order's initial status.
- [[marketing-discounts]] — discount uses are gated by counted statuses.
- [[inventory-tracking]] — stock-decrement timing is status-driven.
- [[inventory-restock]] — symmetric stock-return flow on cancel / refund.
- [[json-api-v2]] — API overview.
- [[order-processing-pipeline]] — per-status side-effect catalogue.

## Open Questions

None — all previously-flagged items resolved or distributed to sub-pages.
