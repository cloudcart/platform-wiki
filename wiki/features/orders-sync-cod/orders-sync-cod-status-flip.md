---
type: feature
nav_path: "Orders → COD sync → Status flip"
route_name: admin.orders.sync.cod
route_path: /admin/orders/sync/cod
aliases: ["COD sync status flip", "COD sync marks completed", "COD sync amount override", "COD sync payment record", "COD paid sync result"]
tags: [orders, cod, sync, order-status, payment]
plan_gates: ["shipping_payment_sync"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---
# COD sync — status flip

> Part of [[orders-sync-cod]]. See the hub for related aspects (log view, eligibility, polling job, errors, quota, manual alternatives).

## Purpose

Describes **exactly what happens to an order when a courier reports the COD has been collected**. This is the page to consult when a merchant asks *"why did my order skip 'Paid' and go straight to 'Completed'?"* or *"why does the payment amount differ from the order total?"*.

## Where to find it

No control surface — the flip is performed by the background job. The merchant sees the result on the order itself ([[orders-details]]) and a summary row on [[orders-sync-cod-log-view]].

## What the merchant can do here

- Observe the flipped status and the recorded amount on [[orders-details]].
- Read the action code in the order's history (see Business rules below).
- Nothing is configurable — the flip behaviour is fixed.

## Settings & fields

### What a successful sync writes to the order

When the courier reports the COD collected with a non-zero amount, the platform:

1. **Overwrites the order's payment amount** with the courier-reported amount — so if the courier collected a different sum than the original order total (e.g., the customer paid rounded cash, the courier kept change as a fee), the platform's payment record matches what the courier actually got.
2. Sets the payment's `provider_reference_id` to the courier's waybill ID.
3. Sets the payment status to `completed`.
4. **Flips the order's status DIRECTLY to `completed`** (not `paid`) — bypassing the normal status precedence. This is a hard status-change-to-`completed` call.
5. Records the amount + courier-returned `type` (cash / card / other) + `last` timestamp in order meta.
6. Clears any previous `sync_payment_error` and counter meta.
7. Fires the normal customer-notification / invoice-generation / webhook pipeline for the new status.

### Amount mismatch — courier-reported wins

The courier's amount **overrides** the original order total. If the courier reports 45 BGN collected but the order total was 50 BGN, the platform stores 45 BGN as the payment amount and the order is marked completed at that figure. The merchant can reconcile by checking the order's history (action code `19` = `order_payment_paid`, carrying the new amount) or by comparing against the courier's own report.

## Business rules

### No `paid` intermediate state for synced COD orders

Merchants relying on the `paid` → `completed` lifecycle won't see `paid` as an intermediate state for COD orders that sync successfully — the platform jumps straight to `completed`. This is by design and distinct from a merchant manually clicking Mark as paid (which sets `completed` on the payment but is a different path — see [[orders-sync-cod-manual]]).

### The flip fires the full downstream pipeline

Because step 7 runs the normal status-change pipeline, a successful sync can trigger the customer order-status email (per [[settings-statuses]]), invoice generation, and the order webhook — exactly as if the merchant had changed the status by hand. Merchants who don't want a "completed" email on COD collection must adjust their status-notification settings on [[settings-statuses]].

### Reconciliation guidance

When the recorded amount differs from the order total, the difference is real money the courier reports — not a bug. The merchant reconciles against the courier's settlement report. The order history's `order_payment_paid` entry is the authoritative record of what the platform stored.

## Related

- [[orders-sync-cod]] — hub.
- [[orders-details]] — where the flipped status and recorded amount appear.
- [[orders-history]] — the `order_payment_paid` (code 19) audit entry for the synced amount.
- [[settings-statuses]] — status-transition notifications the flip can trigger.
- [[orders-sync-cod-manual]] — contrast with a manual Mark as paid.

## Open questions

None.
