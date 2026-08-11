---
type: feature
nav_path: "Payment Providers → Raiffeisen Bank → Refund, sync & status"
route_name: apps.raiffeisen.overview
route_path: /admin/payment-providers/kbc
aliases: ["Raiffeisen refund", "Raiffeisen sync", "Raiffeisen status mapping", "Raiffeisen 3DS", "Raiffeisen 3-D Secure", "Raiffeisen payment status", "Raiffeisen order ID format", "Райфайзен възстановяване", "Райфайзен синхронизация", "Райфайзен 3D Secure"]
tags: [paymentproviders, payment-providers, raiffeisen, kbc, card-gateway, refund, status]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[payment-providers-raiffeisen]]. See the hub for the other aspects (setup, capture/authorize, save-card).

# Raiffeisen Bank — Refund, sync & status

## Purpose

This aspect covers what happens to a Raiffeisen payment **after** the customer pays: the mandatory 3-D Secure flow, how Raiffeisen's response codes map to platform payment statuses, the automatic status-sync reconciliation, and how full refunds are issued.

## Where to find it

Refunds are initiated from the order's payment panel (see [[orders-payment-refund]]), not from the provider screen. Status sync runs automatically in the background. The mapping and behaviour are configured implicitly by the integration — there are no merchant-facing controls for them on `/admin/payment-providers/kbc`.

## What the merchant can do here

- **Issue a full refund** of a completed Raiffeisen payment from [[orders-payment-refund]].
- Rely on **automatic status sync** to reconcile a payment's state against Raiffeisen.
- Read the resulting [[payment-status]] on the order.

## Settings & fields

No merchant-editable fields. Refund / sync / status mapping run automatically. (The Authorization-mode and credentials settings that drive payments live in [[raiffeisen-setup]] and [[raiffeisen-capture-authorize]].)

## Business rules

### 3-D Secure is mandatory

Every Raiffeisen charge runs through UPC's 3DS flow. The merchant **cannot** disable 3DS — it is enforced bank-side. The customer is redirected to Raiffeisen's hosted page, completes 3DS if challenged, and is redirected back to the platform's `/return/provider/kbc` URL. A `payByToken` charge (saved card — see [[raiffeisen-save-card]]) may still be challenged with a 3DS step-up by the issuer.

### Card networks supported

Visa, Mastercard. Maestro / Amex / JCB depend on Raiffeisen's per-merchant acquiring contract.

### Status code mapping

Raiffeisen's transaction-status reading translates the bank's response code to a platform [[payment-status]]:

| Raiffeisen status | Mapped platform status |
|-------------------|------------------------|
| Successful purchase | `Completed` |
| Successful authorize (with `Delay=1`) | `Authorized` |
| Successful capture | `Completed` |
| Successful refund | `Refunded` |
| Customer cancelled / declined | `Canceled` |
| Provider error / timeout | `Failed` |

### Order ID format

The platform sends `OrderID = <internal_order_id>` (numeric). The purchase description sent to Raiffeisen reads `<site_url> | Order #<order_id>`. The `SD` field (a free-form reference) carries the platform's payment ID so the return-callback can locate the payment row.

### Sync skips final-status payments

The sync flow short-circuits if the payment status is already `Completed`, `Canceled`, or `Refunded` — these are terminal states, so it doesn't re-query Raiffeisen. For other statuses it polls Raiffeisen's transaction-fetch endpoint with `TotalAmount`, `OrderID`, `PurchaseTime` to reconcile.

### Refund support — full only

Full refunds (triggered from [[orders-payment-refund]]) call Raiffeisen's refund endpoint with `TotalAmount`, `OrderID`, `ApprovalCode`, `Rrn`. After Raiffeisen confirms, the platform marks the payment `Refunded`. **Partial refunds are not exposed in the admin UI today** — refunds always use the full payment amount. (Cancelling an authorization also reuses the refund call — see [[raiffeisen-capture-authorize]].)

### Signature verification on return

The bank POSTs back to `<cc_payments_domain>/return/provider/kbc` (customer return) and `<cc_payments_domain>/webhook/kbc` (server-to-server IPN). The response HMAC is verified using the same private key + algorithm configured in [[raiffeisen-setup]]; the platform then reads `Rrn`, `ApprovalCode`, `IntRef`, and the response code before applying the status mapping above.

## Related

- [[payment-providers-raiffeisen]] — hub.
- [[orders-payment-refund]] — initiates a full refund through Raiffeisen.
- [[payment-status]] — Authorized / Completed / Canceled / Refunded / Failed enum.
- [[orders-details]] — where the order's payment status is shown.
- [[payment-provider]] — entity definition.

## Open questions

None.
