---
type: concept
nav_path: "Concept → Order processing pipeline → Stage 2 Status"
aliases: ["Order status change pipeline", "Stage 2 status transitions", "11 statuses side-effects", "Stock-bearing statuses", "Negative statuses", "Auto-created return"]
tags: [orders, lifecycle, status, side-effects, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-08-06
source_count: 5
---

> Part of [[order-processing-pipeline]]. See the hub for the other aspects (placement, payment sync, fulfillment, edits, edge cases).

# Order pipeline — Stage 2: Status change

## Definition

**Stage 2** fires every time an order's status transitions — the merchant picks a new status from the dropdown on [[orders-details]], a payment-gateway webhook flips the order to `paid`, the merchant cancels via bulk action, or any other path into a new status. This is the stage with the most side-effects: stock movements, invoice / receipt number generation, payment-gateway authorisation cancellation, discount-usage recount, webhook fan-out, customer email, two distinct history-row audit entries, and — on cancel / refund of a committed sale — an auto-recorded return.

## Scope

Covered:

- The 11 canonical statuses grouped by behaviour (stock-bearing / negative / authorized).
- The full status-change chain step by step, plus the route-gating that suppresses the post-events on the storefront checkout-submit route and on the payment-gateway return / webhook routes.
- Custom statuses as partial participants (no stock, no auth-cancel, no auto-created return).
- The auto-created system return on cancel / refund of a committed sale.

Not covered here:

- The allowed-transitions matrix (which status can follow which) — see [[order-status-workflow]].
- Payment-row status sync that cascades into Stage 2 — see [[order-pipeline-stage-3-payment]].
- Fulfillment add / remove (its own stage) — see [[order-pipeline-stage-4-fulfillment]].

## Contrasts

- **Stock-bearing vs negative vs `authorized`** — three behaviour groups, not 11 individual rules.
- **Standard vs custom statuses** — only the 11 canonical statuses move inventory, release a gateway authorisation, or auto-record a return; custom statuses still fire the webhook, the customer email, both history rows, invoice / receipt numbering and the discount recount.
- **Admin-driven change vs gateway callback** — an admin / API change runs the whole chain; a routine gateway `pending → paid` skips the post-events entirely (no webhook, no email, no history row).

## Where it applies

The 11 statuses (see [[order-status-workflow]] for the full transition rules):

- **Stock-bearing statuses** (count as "stock is out"): `paid`, `authorized`, `completed` — plus `pending` when the order's decrement setting is `pending`.
- **Negative statuses** (restock inventory + cancel any payment-gateway authorisation): `voided`, `timeouted`, `cancelled`, `failed`, `refunded`, `chargebacked`, `disputed`. Two of them — `cancelled` and `refunded` — additionally auto-record a system return on a committed sale.
- Which setting applies is **snapshotted onto the order at placement** (new stores are seeded with `pending`), so changing the store setting never affects existing orders.

### The status-change chain — what fires, in order

| # | Side-effect | When | Conditional |
|---|---|---|---|
| 1 | **Stock movement** — decrement when the order is `fulfilled`, or when its snapshotted setting is `paid` and its status is `paid`/`authorized`/`completed`, or when its setting is `pending` and its status is any of those plus `pending`. Restock is **blocked** while the status is `paid`/`authorized`/`completed`, so stock comes back when the order leaves that set. Each movement writes an entry to the affected product's [[products-change-log\|Change log]] with the order as Initiator (action = order, a clickable *"Edit from order #N"* link) | Sync | Per-line `tracked` flag |
| 2 | **Low / out-of-stock admin emails** — queued when stock falls below the merchant's threshold OR reaches zero | Queued | Each notification's own on/off row on [[settings-admin-notifications]] plus the master `administrator_email_notifications` switch |
| 3 | **Storefront search-index re-sync + `product.updated` webhook** — for every product the stock movement touched | Sync | Skipped when the [[apps-store-locations]] multi-warehouse app is installed (it handles its own per-location sync) |
| 4 | **Invoice number generated** — on *every* status change, not only on `paid` | Sync | An invoicing provider must be active on [[settings-invoicing]]; otherwise no invoice number is assigned (order goes to fulfillment without one) |
| 5 | **Receipt number generated** | Sync | Same gating as invoice number |
| 6 | **Customer lifetime-spend recalculation queued** | Queued | Always (unless store statistics are disabled) |
| 7 | **Payment-gateway authorisation cancelled** — when the new status is "negative" AND the payment row has an `authorize_amount` (pre-auth held, not captured), the platform releases the hold (e.g. Stripe clears the pending charge on the customer's card) | Sync | Status in `voided`/`timeouted`/`cancelled`/`failed`/`refunded`/`chargebacked`/`disputed` AND a pre-auth exists |
| 8 | **Discount-usage figure recounted** — every [[discount]] attached to the order is re-counted across all orders in a counted status; a fallback job 10s later covers race conditions (retries up to 15× on duplicate-key) | Sync + queued | Sits OUTSIDE the post-event block, so it still runs on gateway routes |
| 9 | **Webhook `order.updated` fan-out** | Per-subscriber (sync or queued, set on the subscription) | [[settings-hooks]] subscribers |
| 10 | **Customer "status changed" email queued** — one shared template for all statuses; the job carries only the order id, so it renders the status the order has when it runs | Queued (~10s) | `notify_customer = yes` on the order, the template's own active flag, and the store-wide `customer_email_notifications` — see [[orders-notify-customer]]. The store's own copy rides inside this step |
| 11 | **Digital-product download-link email** — separate email with download URLs when the new status is `paid` or `completed` | Queued | Order has at least one digital product |
| 12 | **Order history row written** — previous + new status; shown on [[orders-details]] History tab | Sync | Both built-in and custom statuses write it |
| 13 | **Status-history detail row written** — separate timestamped audit trail; basis for the *"how long in status X"* analytics on [[orders-details]] | Sync | Always |

### Steps 14–15 — cancel / refund of a committed sale

| # | Side-effect | When | Conditional |
|---|---|---|---|
| 14 | **System return auto-recorded** — created straight as `returned`, source `refund`, created by the system, covering the remaining quantity. Idempotent | Sync | New status is `cancelled` or `refunded` AND the order was a committed sale (invoiced, or coming from a positive status). Merchant-visible: it counts in return reporting — see [[orders-returns-lifecycle]] |
| 15 | **Reversal lock armed** — from then on the order's status only toggles between `cancelled` and `refunded` | Sync | A return record or an issued credit number exists on a cancelled / refunded order |

**Route-gating:** the post-status-change chain (steps 9–13) is **skipped** in two places, not one:

- The storefront's `checkout.payment.submit` route — the platform treats this as the order's first status assignment and lets the placement pipeline ([[order-pipeline-stage-1-place]]) handle the post-events.
- The **payment-gateway return and webhook routes** — with two exceptions that DO get the post-events: a **cancellation**, and a **recovery** (a negative status returning to `paid` / `authorized` / `completed`, so fulfilment partners see the correction).

So a routine online payment moving the order `pending → paid` writes **no history row, sends no customer email, and delivers no `order.updated`**. Steps 1–8 and 14–15 still run. See [[order-pipeline-known-edge-cases]].

### Custom statuses — partial participants

Only the 11 canonical statuses (`authorized`, `pending`, `voided`, `timeouted`, `cancelled`, `failed`, `refunded`, `chargebacked`, `paid`, `completed`, `disputed`) move inventory, release a gateway authorisation, or auto-record a return. Custom statuses defined on [[settings-statuses]]:

- **DO** fire the `order.updated` webhook (carrying the custom status's stable `order-…` slug), queue the customer "status changed" email, write **both** history rows, generate invoice / receipt numbers, and run the discount-usage recount.
- **DO NOT** affect inventory, cancel a payment-gateway authorisation (even when labelled "cancelled"-like), or auto-record a return.

A merchant who uses a custom status to "mark cancelled" instead of the platform's `cancelled` ends up with: stock NOT restored, payment authorisation NOT released, no return record, and the order still counted in revenue. Use the canonical statuses for these transitions.

## Related

- [[order-processing-pipeline]] — hub.
- [[order-pipeline-stage-1-place]] — placement pipeline; Stage 2 follows the first status assignment.
- [[order-pipeline-stage-3-payment]] — payment-row changes cascade into Stage 2.
- [[order-pipeline-stage-4-fulfillment]] — fulfillment add / remove can flip the status.
- [[order-pipeline-known-edge-cases]] — route-gating exceptions and other non-obvious behaviour.
- [[order-status-workflow]] — the 11 statuses + allowed transitions + custom statuses.
- [[orders-details]] — where the merchant triggers status changes.
- [[settings-statuses]] — custom-status definitions.
- [[settings-invoicing]] — invoice number generation gating.
- [[settings-hooks]] — webhook subscription + delivery log.
- [[settings-admin-notifications]] — low-stock / out-of-stock admin email gating.
- [[orders-notify-customer]] — `notify_customer` flag gating customer emails.
- [[marketing-omnichannel-mails-list]] — the single status-change email template + the store-wide kill switch.
- [[orders-returns-lifecycle]] — the auto-created system return and the reversal lock.
- [[inventory-decrement-timing]] — the `paid` vs `pending` decrement setting.
- [[products-change-log]] — per-product audit trail; each Stage 2 stock movement writes here.
- [[apps-store-locations]] — multi-warehouse app handling its own search-index sync.

## Open Questions

- **`disputed` behaviour** — confirm whether `disputed` is truly part of the negative-statuses group for auth-cancel purposes, or whether the platform treats disputes as a hold (verify).
- **Discount-counter race** — the belt-and-suspenders queued job retries up to 15× on duplicate-key. Confirm what happens after the 15th retry — does the merchant get an alert (verify)?
