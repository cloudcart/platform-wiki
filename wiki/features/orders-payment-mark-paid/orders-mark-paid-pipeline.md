---
type: feature
nav_path: "Orders → Order details → Payment → Mark as paid → Post-paid pipeline"
route_name: admin.orders.payment.mark_paid
route_path: /admin/orders/action/payment/mark_paid/:payment_id
aliases: ["Mark-paid side effects", "Post-paid pipeline", "Mark-paid cascade", "COD stock decrement", "Mark-paid invoice generation", "Payment date NOW"]
tags: [orders, payment, manual-payment, pipeline, side-effects]
plan_gates: []
created: 2026-06-10
updated: 2026-08-06
source_count: 4
---

> Part of [[orders-payment-mark-paid]]. See the hub for the other aspects (form & visibility, status-flip rules, adjacent actions, API position).

# Mark as paid — the post-paid pipeline

## Purpose

When the merchant clicks Save on the mark-as-paid modal, the platform treats it as if a gateway just confirmed the payment, and runs a **heavyweight cascade** — far more than just flipping the payment status. This page catalogues every side-effect that fires, so the merchant understands that marking a payment paid touches stock, invoicing, customer aggregates, webhooks, and the order history all at once. The order-status auto-flip that this cascade also triggers has its own page — [[orders-mark-paid-status-flip]].

## Where to find it

There is no separate screen for this — the cascade runs server-side the moment the merchant Saves the [[orders-mark-paid-form]] modal. Its visible traces appear on [[orders-details]] (refreshed status, stock changes), the [[orders-history]] timeline (action 19), and any subscribed webhook receivers.

## What the merchant can do here

The merchant cannot configure the cascade per-action — it is a fixed pipeline. What the merchant CAN control is the inputs: whether `invoice_generate=auto` is on (per [[settings-invoicing]]), whether the paid status has a customer-notification email (per [[settings-statuses]]), and whether stock was already decremented earlier in the order lifecycle. The merchant's main job is to be aware of the cascade before clicking Save.

## Settings & fields

The cascade reads (it does not write) these merchant settings:

| Setting | Source | Effect on the cascade |
|---------|--------|-----------------------|
| `invoice_generate` | [[settings-invoicing]] | When `auto` and no number exists yet, an invoice number is generated. |
| Receipt auto-generation | [[settings-invoicing]] | Same conditions as the invoice number. |
| Status-change mail active flag + store-wide `customer_email_notifications` | [[marketing-omnichannel-mails-list]] | Together with the order's `notify_customer` flag, decide whether the customer notification email fires. There is no per-status toggle. |
| `order.updated` webhook subscription | [[settings-hooks]] | Decides whether the webhook fan-out reaches an external receiver. |

## Business rules

### Manual confirmation drives the full post-paid pipeline

Clicking Save means:

- Customer notification email for the new (paid) status fires per [[settings-statuses]].
- Invoice number generation runs if `invoice_generate=auto` per [[settings-invoicing]].
- `order.updated` webhook fires per [[settings-hooks]].
- Stock decrement / fulfilment workflows may trigger.
- The order's status updates per the platform's pending-to-paid transition rules (see [[orders-mark-paid-status-flip]]).

So marking as paid is a heavyweight action — the merchant should be confident the offline payment actually arrived.

### The Payment Sync handler — what fires, in order

The Payment Sync event handler performs (synchronously, per the listener):

1. **Stock decrement** — the order's products' quantity is decreased (when the new status moves toward `paid`/`completed`) or restored (when moving away). For COD orders, the moment of mark-as-paid is typically when stock gets decremented, since the COD flow does not decrement at checkout. See [[inventory-decrement-timing]] for the store-wide `order_status_for_quantity_decrease` setting that governs this.
2. **Invoice number generation** — if `invoice_generate=auto` per [[settings-invoicing]] AND no number exists yet.
3. **Receipt number generation** — same conditions as the invoice.
4. **Customer income recalculation** — the platform updates the customer's total-spend aggregate (used for customer segmentation per [[customers-custom-groups]]).
5. **`order.updated` webhook** — fires per [[settings-hooks]].
6. **History entry** — action code 19 (`order_payment_paid`) on the order's timeline ([[orders-history]]).

So clicking Mark-as-paid touches more than the merchant might expect — especially the stock decrement on COD orders. If the merchant did not reserve stock at checkout (a common COD setting), the stock decrement happens HERE, and an out-of-stock condition may surface only at this point.

### Payment date — always set to NOW

The platform sets the payment's status to `completed` and syncs it, which timestamps the payment with the CURRENT moment. The merchant CANNOT back-date the payment to the actual receipt date. For accounting purposes the merchant should ideally mark-paid promptly after the offline payment arrives, since the platform's record reflects the recording date, not the receipt date.

### Audit captures the acting admin

Every mark-as-paid invocation produces an `order_payment_paid` history entry (action code 19) tied to the current session's admin. So the merchant can later see WHO marked the order paid in [[orders-history]].

### Mark-as-paid skips webhook idempotency — no protection against double-clicks

The merchant clicking the Mark-as-paid button twice in quick succession produces TWO payment-sync events and two history entries (action code 19 each). The platform does not de-duplicate. The end state is still correct (payment.status = completed), but the audit log shows two entries. Frontend AJAX submit-button disabling is the only protection.

## Related

- [[orders-payment-mark-paid]] — hub.
- [[orders-mark-paid-form]] — the modal whose Save triggers this cascade.
- [[orders-mark-paid-status-flip]] — the order-status auto-flip this cascade also runs.
- [[inventory-decrement-timing]] — when the stock decrement step actually fires (`order_status_for_quantity_decrease`).
- [[settings-invoicing]] — auto-invoice / receipt number generation.
- [[settings-statuses]] — paid-status notification email.
- [[settings-hooks]] — `order.updated` webhook.
- [[customers-custom-groups]] — customer-income aggregate used for segmentation.
- [[orders-history]] — action 19 entry.
- [[order-processing-pipeline]] — the full status-transition pipeline.

## Open questions

None.
