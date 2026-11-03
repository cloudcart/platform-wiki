---
type: feature
nav_path: "Orders → Order details → Payment → Manual confirm (Mokka)"
route_name: admin.orders.payment.manual
route_path: /admin/orders/action/payment/manual/:order_id
aliases: ["Mokka confirm", "Mokka manual confirm", "Confirm Mokka", "Document number Mokka", "Потвърждение Mokka"]
tags: [orders, payment, manual-confirm, mokka, bnpl, smarty]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 4
---

> Part of [[orders-payment-manual]]. See the hub for related aspects (Klear confirm, change provider, lease, API access).

# Manual confirm — Mokka

## Purpose

For orders paid via the **Mokka** BNPL provider, the manual-confirm action commits the credit transaction on Mokka's side once the goods are ready to ship. The merchant opens a small modal, supplies a **document number** (the dispatch / shipment reference), and saves; the platform calls Mokka's `finish` API to finalise the credit. This is the second stage of Mokka's two-stage flow (apply at checkout → confirm at dispatch).

## Where to find it

From [[orders-details]], in a dedicated action row in the order-actions summary, shown **only when** the payment provider is `mokka` AND the order status is `completed` OR `paid` AND the meta flag `mokka_confirm` is `0` (not yet confirmed). The row shows the Mokka logo + *"Confirm Mokka"* text and a blue **Confirm** button (`mokka_confirm_button` CSS class).

The button uses `data-modal-ajax` → opens the small confirmation modal containing the `document_number` form. Route: `/admin/orders/action/payment/manual/{order_id}` — GET opens the modal, POST commits.

## What the merchant can do here

The Mokka modal shows ONE field. The merchant enters (or accepts the pre-filled) document number and clicks Save.

On success:
- A meta record `mokka_confirm = 1` is created on the order.
- The Mokka confirmation row disappears from [[orders-details]].
- A toast confirms success, and the order summary refreshes (the modal triggers `cc.ajax.reload` on the `.order-summary` panel without a full page reload).
- The order's hooks fire (customer notification email, invoice generation if configured, webhooks).

On error (document number missing, or Mokka rejects the confirmation), an error toast shows Mokka's message and the row stays.

### What the merchant CANNOT do here

- Submit without a document number — server-side returns *"Document number is required"* via toast. There is no client-side validation, so an empty submit is possible but rejected by the server.
- Confirm only a shipped portion — the action commits the FULL order amount (see Business rules).
- Roll back after commit — reversal must go through Mokka's own dashboard.

## Settings & fields

| Field | Required | Notes |
|-------|----------|-------|
| **Document number** (`document_number`) | Yes | The merchant's dispatch / shipment document reference. Plain text — accepts any string and forwards it as-is to Mokka; no client- or server-side format check. Pre-filled with the order's invoice number when available (gated by the Invoicing module — see below). Has `data-autofocus=""` so the cursor lands in the field as the modal opens. |

The modal (`payment/manual_mokka.tpl`) also contains a standard Save / Cancel footer. Its title concatenates the translation key `order.confirm_order.title_modal` + the provider display title, so the merchant sees something like *"Confirm order: Mokka"*. Modal size is `small`.

## Business rules

### Mokka confirmation row visibility

The row renders only when: provider is `mokka` AND order status is `completed` OR `paid` AND `mokka_confirm` meta flag is `0`. On a fresh Mokka order still in `pending` status the row is NOT shown — the merchant must wait for the BNPL credit check to flip the order to `paid`. Manually setting the order back to `pending` via [[orders-status-change]] hides the row again. After a successful confirm (`mokka_confirm = 1`) the row disappears.

### Mokka confirm sends the CURRENT order total, not the original

The platform calls Mokka's `finish` API with the order's current total — i.e., if the merchant edited the order (added a discount, removed a product, changed shipping) AFTER the BNPL credit was approved but BEFORE confirming, the amount sent is the NEW total, not the originally-applied-for amount. If the new total **exceeds** the credit limit Mokka approved at checkout, Mokka rejects the confirmation with an error. If the new total is **lower**, Mokka generally accepts it (the customer pays less). Important when an order is reduced post-credit-approval.

### Invoice-number pre-fill is gated by the Invoicing module

The `document_number` field pre-fills ONLY when the invoicing module has an active provider AND the order has a generated invoice number. If the merchant hasn't enabled invoicing OR hasn't generated an invoice yet, the field is empty and they must type a document number manually. So if Mokka rejects with "document number required", the workaround is to type any internal shipment reference OR generate the invoice first (see [[orders-invoice]]).

### Network failure leaves the order in pending-confirm

A network exception during the `finish` call surfaces the gateway's error message as a toast. The `mokka_confirm` flag is NOT set to 1 and the row stays visible. The merchant can retry by re-opening the modal. There is no background retry — manual operator action only.

### Full-amount, all-or-nothing

The action commits the FULL payment amount. There is no UI to confirm only the shipped portion of a partially-shipped order; partial confirmation must be coordinated via Mokka's own dashboard or support.

### Side effects on success

- Mokka's `finish` API commits the credit (real money movement on Mokka's side).
- `mokka_confirm = 1` meta set; order saved.
- Order hooks fire (notification email, invoice, webhooks) — similar to mark-as-paid.
- Toast confirms; order summary panel reloads.

### Permission

Standard orders write access; no specific manual-confirm grant.

## Related

- [[orders-payment-manual]] — hub.
- [[orders-details]] — parent page hosting the confirmation row.
- [[orders-invoice]] — invoice number used as the document-number default.
- [[orders-status-change]] — setting the order back to `pending` hides the confirmation row.
- [[orders-history]] — confirm event recorded here.
- [[settings-payment-providers]] — Mokka provider configuration.
- [[orders-payment-refund]] — reverse a completed Mokka payment via Mokka's refund API.

## Open questions

None.
