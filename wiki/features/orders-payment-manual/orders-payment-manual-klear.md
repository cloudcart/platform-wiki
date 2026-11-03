---
type: feature
nav_path: "Orders → Order details → Payment → Manual confirm (Klear)"
route_name: admin.orders.payment.manual
route_path: /admin/orders/action/payment/manual/:order_id
aliases: ["Klear confirm", "Klear manual confirm", "Confirm Klear", "Klear capture", "Потвърждение Klear"]
tags: [orders, payment, manual-confirm, klear, bnpl, smarty]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 3
---

> Part of [[orders-payment-manual]]. See the hub for related aspects (Mokka confirm, change provider, lease, API access).

# Manual confirm — Klear

## Purpose

For orders paid via the **Klear** BNPL provider, the manual-confirm action captures the credit on Klear's side once the goods are ready to ship. Unlike [[orders-payment-manual-mokka|Mokka]], Klear needs no merchant input — the merchant clicks Confirm and the platform immediately calls Klear's capture API using the stored checkout data. The whole flow is a single click → one POST → toast.

## Where to find it

From [[orders-details]], in a dedicated action row in the order-actions summary, shown **only when** the payment provider is `klear` AND the order status is `completed` OR `paid` AND the payment's `provider_data->capture` is empty (capture hasn't happened). The row shows the Klear logo + *"Confirm Klear"* text and a blue **Confirm** button (`klear_confirm_button` CSS class).

The Klear button uses `data-request` (NOT `data-modal-ajax`) → it POSTs directly to the manual route with no modal. The click handler does a `$.post` to the manual route; the handler immediately calls Klear's capture API and shows a toast. The merchant sees no form. Route: `/admin/orders/action/payment/manual/{order_id}` (POST).

## What the merchant can do here

The single action is **Confirm**. On click, the platform:

1. Loads the order's stored Klear transaction stub from the payment's `provider_data->transaction` (saved during the original checkout).
2. Calls Klear's capture API with the checkout-id (`transaction.checkout_id`) + order-id + payment-id.
3. Stores BOTH the original transaction AND the capture response as `provider_data` for full audit.
4. Saves the order + the underlying payment record.
5. Returns a toast (success or error message).

On success the order's hooks fire (customer notification email, invoice generation if configured, webhooks), like mark-as-paid, and the Klear confirmation row disappears.

### What the merchant CANNOT do here

- Enter any field — Klear's capture is automatic from stored data; there is no document-number input (unlike Mokka).
- Confirm only a shipped portion — capture is FULL-amount, all-or-nothing.
- Roll back after capture — reversal goes through Klear's own dashboard.

## Settings & fields

This is a no-input action — there are no merchant-editable fields. The capture is driven entirely by the stored `provider_data->transaction.checkout_id` from the original checkout.

| Provider | Required field | Notes |
|----------|----------------|-------|
| **Klear** | (none) | Capture is automatic from stored checkout data. |

## Business rules

### Klear confirmation row visibility (parallel to Mokka)

The row renders only when: provider is `klear` AND order status is `completed` OR `paid` AND the payment's `provider_data->capture` is empty. After a successful capture the row disappears because `provider_data->capture` becomes non-empty. The visibility logic checks `empty($order->payment->payment->provider_data->capture)` rather than a separate meta flag — Klear's state is tracked **inside** `provider_data` itself, unlike Mokka's external `mokka_confirm` meta.

### Klear capture API call

The capture call retrieves the stored `transaction.checkout_id` from `provider_data` and calls Klear's capture API with checkout-id + order-id + payment-id. Both the original transaction AND the capture response are stored as `provider_data`, giving a full audit trail.

### Error handling differs from Mokka

The Klear capture response is stored as `provider_data` but is NOT explicitly checked for an error code before commit. If Klear returns an error in its response body, the platform may still flag the local payment as captured (until a later webhook from Klear corrects it). This is existing platform behaviour `(verify)` — for now the merchant should re-check the Klear dashboard if the captured status looks off.

### Full-amount, all-or-nothing

The capture commits the FULL payment amount. There is no UI to capture only the shipped portion of a partially-shipped order; partial capture must be coordinated via Klear's own dashboard or support.

### Side effects on success

- Klear's capture API commits the credit (real money movement on Klear's side).
- `provider_data` updated with the capture response; both order and the underlying payment record are saved.
- Order hooks fire (notification email, invoice, webhooks).
- Toast confirms.

### Excluded from the Lease flow

Klear is explicitly excluded from the credit-provider Payment Lease re-confirmation flow — Klear handles its own re-confirmation outside CloudCart. See [[orders-payment-manual-lease]].

### Permission

Standard orders write access; no specific manual-confirm grant.

## Related

- [[orders-payment-manual]] — hub.
- [[orders-details]] — parent page hosting the confirmation row.
- [[orders-history]] — capture event recorded here.
- [[settings-payment-providers]] — Klear provider configuration.
- [[orders-payment-refund]] — reverse a completed Klear payment via Klear's refund API.

## Open questions

- Whether the platform should check Klear's capture response for an error code before marking the local payment captured `(verify)`.
