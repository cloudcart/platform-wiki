---
type: feature
nav_path: "Orders → Order details → Status → Side effects"
route_name: admin.orders.change-status
route_path: /admin/orders/action/status/:order_id/:status
aliases: ["Status change side effects", "Order status pipeline", "What happens on status change", "Status change downstream"]
tags: [orders, status, side-effects, pipeline]
plan_gates: []
created: 2026-06-10
updated: 2026-08-06
source_count: 4
---

> Part of [[orders-status-change]]. See the hub for the other aspects (pill, transition rules, notification, fulfillment gate, bulk, API).

# Order status change — Side effects

## Purpose

Once a status change passes the transition gates (see [[orders-status-change-transition-rules]]), the platform runs a deterministic chain of side effects. This page is the canonical catalogue of what happens, in roughly the order it happens. The chain runs identically whether the trigger is the breadcrumb pill ([[orders-status-change-pill]]), the bulk action ([[orders-status-change-bulk]]), or the JSON-API v2 PATCH ([[orders-status-change-api]]) — the only difference is the source namespace recorded in [[orders-history]].

For the full end-to-end pipeline including events outside the status-change flow, see [[order-processing-pipeline]].

## Where to find it

The side effects are not surfaced as a single UI block — the merchant observes them across multiple surfaces: a history row appears in [[orders-history]], a customer-notification email may arrive, stock may decrement on the affected variants ([[products-inventory]]), an invoice may be auto-generated ([[orders-invoice]]), and the `order.updated` webhook fires ([[settings-hooks]]).

## What the merchant can do here

The merchant does not interact with the side-effect chain directly — it runs automatically. But understanding what fires (and when) prevents common surprises like "I changed status and now my customer got an email" or "I marked refunded and lost the credit-note number".

### The order the chain actually runs in

1. Stock movement.
2. Invoice number + receipt number issued.
3. Customer lifetime-spend recomputation queued.
4. The "post" block: `order.updated` webhook → customer email → the two history rows. **Skipped on gateway paths** — see below.
5. Discount-usage recount (inline + a resync queued ~10 s later).
6. Payment-authorisation release at the gateway (negative statuses only).
7. System return auto-recorded (`Cancelled` / `Refunded` only, on a committed sale).

The rest of this section covers each of these.

### Side effect 1 — Stock decrement / restore

Two things decide it: the order's fulfillment state, and the decrement setting **snapshotted onto the order at placement** ([[settings-cart]] → `order_status_for_quantity_decrease`; new stores are seeded with `pending`). Because it is a snapshot, changing the store setting **never** affects orders that already exist.

Stock is **decremented** when the order is `fulfilled`, or when:

- the order's setting is `paid` and its status is Paid / Authorized / Completed; or
- the order's setting is `pending` and its status is Paid / Authorized / Completed **or** Pending.

Stock is **never restocked** while the order sits in Paid / Authorized / Completed. It comes back when the order leaves that set — most commonly into a negative status.

So a merchant on a `paid`-configured store who bulk-cancels old pending orders sees NO stock returned (those pending orders never decremented). And a pre-auth order in Authorized counts as decremented under both settings. Per-line tracking prevents double-counting — see [[inventory-decrement-timing]] and [[inventory-restock]].

### Side effect 2 — Invoice / receipt number issued

Invoice and receipt numbers are issued on **every** status change, not only on `Paid`, provided an invoicing provider is active per [[settings-invoicing]]. See [[orders-invoice]] for numbering modes (auto / manual / external) and [[orders-receipt]] for fiscal-receipt cases. Receipt / fiscal printer apps fire here too.

### Side effect 3 — Webhook, customer email, history rows (the "post" block)

Fired in that order:

- **`order.updated`** to every active subscriber in [[settings-hooks]].
- **Customer status-change email**, queued with a ~10-second delay, when the three switches allow it — the order's `notify_customer` flag, the status-change template's own active flag, and the store-wide `customer_email_notifications`. There is ONE template for all statuses. The store's own copy of that notification rides inside this same step, so suppressing the customer email suppresses the admin one too. See [[orders-status-change-notification]].
- **Two history rows** on [[orders-history]] — the typed action row (matching the new status; `order_custom_status` for a custom one) plus a separate previous → new row. The source namespace is `admin` for the breadcrumb pill / bulk action and `api2` (rendered "API") for JSON-API v2 changes.

**This whole block is skipped on the payment-gateway return / webhook paths**, except for a cancellation and for a recovery (a negative status moving back to Paid / Authorized / Completed). So a routine online payment flipping the order `pending → paid` produces **no customer email, no `order.updated`, and no history row** — the most common explanation for *"the paid email never went out"* and *"my ERP never saw the order go paid"*. The storefront checkout-submit path suppresses the same block. Everything else in the chain still runs.

### Side effect 4 — Discount-usage recount

The discount's `uses` figure is recounted across every order in a counted state, inline and again ~10 seconds later as a fallback. Because the fallback sits outside the "post" block, the counter stays correct even on the gateway paths. See [[marketing-discounts]].

### Side effect 5 — Negative-status auto-effects

When the merchant moves an order to ANY NEGATIVE status (`Cancelled`, `Voided`, `Refunded`, `Failed`, `Disputed`, `Chargebacked`, `Timeouted`), the platform resets fulfillment to `not_fulfilled` if it was `fulfilled`, releases any payment authorisation at the gateway, and restocks per the rule above. See [[orders-status-change-fulfillment-gate]] for the fulfillment + authorization mechanics.

### Side effect 6 — Cancelling / refunding a committed order auto-creates a return

Moving an order to **`Cancelled` or `Refunded`** — and only those two of the seven negative statuses — auto-records a **system return** when the order was a committed sale (already invoiced, or coming from a positive status such as `Paid`). The return is created straight as `returned`, with source `refund`, created by the system, covering the whole remaining quantity. No credit note is needed, and it is idempotent.

Merchant-visible consequence: these are real return records, so cancelled paid orders show up in return reporting even though no goods came back. See [[orders-returns-lifecycle]].

### Side effect 7 — The reversal lock closes the order

Once that return record exists — or once a credit number has been issued — the cancelled / refunded order's status is **locked**. From then on the only accepted change is a toggle between `Cancelled` and `Refunded`; anything else is refused with *"The order is locked after a cancellation/refund — its status can no longer be changed."*

So an order cancelled by mistake **after** it was paid or invoiced cannot simply be flipped back to Paid. A plain cancel of a never-committed order has no return record and stays reversible. See [[orders-status-change-transition-rules]].

### Side effect 8 — Draft flag stripped on first non-Cancelled status

If the order still carries the `is_draft` meta when the merchant changes status, that flag is silently removed as part of the change — EXCEPT when the target is `Cancelled` (which doesn't strip the draft flag). So a draft can be promoted to a live order simply by setting any non-Cancelled status on it.

### Side effect 9 — Paid + digital products = auto-fulfillment record

When the merchant marks an order `Paid` AND the order contains digital products AND fulfillment is not already complete, the platform auto-creates a fulfillment record covering the digital line items (so the file-download email can fire). The merchant doesn't need to manually fulfill digital items. See [[orders-status-change-fulfillment-gate]] for the interplay with external-shipping orders.

### Side effect 10 — Auto-promotion to Completed

If the resulting state is `Paid` + `fulfilled` (e.g. via the digital auto-fulfillment above) AND [[settings-cart]] `order_complete` is set, the order is promoted to `Completed` **before** the change event fires. So the merchant gets **one** history row, **one** webhook and **one** email, all reading `Completed` — not a Paid pair followed by a Completed pair.

When the promotion instead comes from adding a fulfilment to an already-`Paid` order, it is applied silently as the order is saved: **no** status-change event at all, so no history row, no email and no `order.updated`. See [[order-status-auto-transitions]].

## Settings & fields

The side-effect chain is configured indirectly through other pages:

- [[marketing-omnichannel-mails-list]] — the single status-change email template, its active flag, and the store-wide `customer_email_notifications` kill switch.
- [[settings-cart]] — `order_status_for_quantity_decrease` (decrement timing, snapshotted per order at placement), `order_complete` (auto-promotion).
- [[settings-invoicing]] — invoicing provider; without one, no invoice / receipt numbers are issued.
- [[settings-hooks]] — `order.updated` webhook subscriber URLs.

## Business rules

- The chain runs synchronously up to "queue the customer email" — the email itself is queued with a ~10-second delay and processes asynchronously. Because the queued job carries only the order's identifier, the email is rendered from the order as it looks when the job runs; two changes inside that window produce two emails both showing the final status. See [[orders-status-change-notification]].
- A rejected transition (failed gate) writes NO side effects — the chain runs only AFTER the transition rules pass.
- Side effects fire for both per-order changes AND bulk status changes. So bulk-completing 100 orders may fire 100 emails AND 100 webhooks.
- Stock restore on Cancel does NOT undo any operational actions (waybill already sent, fiscal receipt already printed) — those need separate manual cleanup.
- Removing a fulfilment does **not** run this chain at all. The platform rewrites the order's status directly (back to `Paid` if a completed payment exists, otherwise `Pending`) with no status-change event — so no history row, no email, no webhook from the status side. And on a `pending`-configured store it does not restock either.

## Programmatic access

JSON-API v2 PATCH of `status` triggers the EXACT same side-effect chain — same history rows (with `api2` namespace), same notification gating, same stock rule, same auto-release of payment authorization, same auto-created return, same webhook. It also sets the order's `manual` marker, after which gateway events stop moving the order's status. See [[orders-status-change-api]].

## Related

- [[orders-status-change]] — hub.
- [[orders-status-change-transition-rules]] — gates that must pass before side effects fire.
- [[orders-status-change-notification]] — customer-email gating + queue delay.
- [[orders-status-change-fulfillment-gate]] — fulfillment + payment-authorization auto-effects.
- [[orders-status-change-bulk]] — side effects fire per-order in bulk.
- [[orders-history]] — where the two audit rows surface.
- [[inventory-decrement-timing]] — stock decrement timing setting.
- [[inventory-restock]] — automatic stock return mechanics.
- [[orders-invoice]] — invoice numbering.
- [[orders-credit]] — credit-note flow; the credit number arms the reversal lock.
- [[orders-returns-lifecycle]] — the system return auto-recorded on cancel / refund.
- [[order-status-auto-transitions]] — the auto-promotion to Completed, including the silent fulfilment route.
- [[settings-hooks]] — `order.updated` webhook.
- [[order-processing-pipeline]] — full end-to-end pipeline.
- [[marketing-discounts]] — the `uses` figure recounted on every transition.

## Open questions

None.
