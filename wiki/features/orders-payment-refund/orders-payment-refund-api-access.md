---
type: feature
nav_path: "Orders → Order details → Payment → Refund → API access"
route_name: admin.orders.payment.refund
route_path: /admin/orders/action/payment/refund/:payment_id
aliases: ["Refund via API", "API refund", "Refund JSON-API v2", "Refund read-only API", "Chargeback vs refund"]
tags: [orders, payment, refund, api, chargeback]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[orders-payment-refund]]. See the hub for the other aspects (visibility, provider matrix, gateway quirks, side effects, partial refunds, status-flip rules).

# Payment refund — API access and chargebacks

## Purpose

Refund is **admin-panel-only**. The JSON-API v2 surface exposes payments as a **read-only** resource — no endpoint allows originating a refund. This page documents what the API CAN do (read the resulting state), why the refund itself is not exposed via API, and how chargebacks (a related but distinct gateway-initiated flow) are recorded.

## Where to find it

- **JSON-API v2 read access** — payments are exposed as the [[api-order-payment]] resource. Useful for fetching payment status, `refunded_at` timestamp, and the provider's reference ID after a refund.
- **Refund button** — admin-panel only, on [[orders-details]]. See [[orders-payment-refund-visibility]].
- **Chargebacks** — webhook-initiated; the merchant sees the status change automatically in [[orders-history]] (action 44).

## What the merchant can do here

### Via JSON-API v2

- **Read payment state** — fetch the current status (`completed` / `refunded` / `partially_refunded` / `chargebacked` / etc.).
- **Read `refunded_at` timestamp** — when the refund was recorded locally.
- **Read provider reference ID** — the gateway's transaction ID, useful for cross-referencing in the gateway's dashboard or in accounting / ERP systems.
- **Read partial-refund state** — when a partial refund has been synced from the gateway's webhook (action 21), the API surfaces the resulting payment state.

### Not exposed via API

- **Originate a refund** — there is no `POST /payments/{id}/refund` or equivalent endpoint. The Refund action is gated to the admin panel.
- **Originate a chargeback** — gateway-initiated only.
- **Originate a partial refund** — gateway-dashboard initiated only.

## Settings & fields

This page documents API access patterns, not configuration. The relevant configuration lives on [[json-api-v2]] (auth, pagination, filtering) and on each merchant's API key permissions.

## Business rules

### Refunds are admin-panel-only by design

Refunds are real-money actions against the payment gateway with per-provider quirks (Stripe full-charge refund, Mokka's always-throws-error pattern, Klear's email-to-staff manual flow, Borica WAY4's retry-idle helper, FusionPay's exclusion, etc.). The platform requires refunds to flow through validated admin paths so that:

- The `orders.refund` permission gate is enforced (see [[orders-payment-refund-visibility]]).
- The gateway-call error handling (HTTP 504 + log entry on network failures) runs.
- The post-refund cascade (status auto-flip from `completed` to `refunded` only when no other completed payments exist, stock auto-restore, customer income decrement, history entry, webhook fan-out) runs reliably (see [[orders-payment-refund-side-effects]] + [[orders-payment-refund-status-flip-rules]]).
- The audit log captures the acting admin user.

Allowing API-driven refunds would bypass several of these guarantees, which is why the API is read-only.

### Reading refund state (use cases)

- **Accounting / ERP sync** — periodically pull refunded payments to mirror reversals externally.
- **Reconciliation** — verify which orders have been refunded after a batch refund.
- **Dashboards** — surface refund counts / amounts in custom merchant reporting.
- **After a gateway-dashboard partial refund** — pull the updated partially-refunded state to mirror in external systems.

### Gateway-side partial refunds — webhook + API read

When a merchant issues a partial refund directly through the gateway's dashboard, the gateway's webhook reports the partial refund back to CloudCart and emits action 21 (`order_payment_partially_refunded`) in [[orders-history]]. That path is webhook-driven, not API-driven — but the API can READ the resulting partial-refund state. See [[orders-payment-refund-partial-refunds]] for the full flow.

### Chargebacks — gateway-initiated, action 44

A chargeback is when the customer disputes a charge directly with their card issuer / payment provider, bypassing the merchant. The merchant does NOT trigger chargebacks via the Refund button — they are gateway-initiated:

1. The customer disputes the charge with their bank / Stripe / PayPal.
2. The gateway processes the dispute and (eventually) reports a chargeback back to CloudCart via webhook.
3. CloudCart automatically updates the order's status to `chargebacked` and records action 44 (`chargebacked`) in [[orders-history]].

The merchant sees the status change in the order's history with the source (gateway webhook). Chargebacks are typically NOT followed by a refund button click — the funds have already been pulled back at the gateway level.

### Chargeback vs refund — key differences

| Property | Refund | Chargeback |
|----------|--------|-----------|
| Initiated by | Merchant (admin panel) | Customer (via bank / provider) |
| CloudCart surface | Refund button on [[orders-details]] | Inbound webhook only |
| History action | 20 (full) / 21 (partial) | 44 |
| Order status | `refunded` (if conditions met) | `chargebacked` |
| Side effects | Stock restock, customer income decrement, etc. | Status update; merchant should investigate fraud |
| Cancellable | No (irrevocable at gateway) | No (already pulled by issuer) |

### API surfaces resulting state, not pending state

The API reflects the state of payments AFTER any synchronous handler has run. A refund that's mid-flight (e.g., Mokka's manual processing) will show whatever local state the platform has set; the gateway-side eventual state may not be reflected yet. The merchant cross-references with the gateway's dashboard for ground truth.

## Related

- [[orders-payment-refund]] — hub.
- [[orders-payment-refund-partial-refunds]] — webhook-driven partial refund path.
- [[orders-payment-refund-side-effects]] — what fires on refund (vs what's available via API).
- [[api-order-payment]] — the read-only JSON-API v2 resource.
- [[json-api-v2]] — API overview; read-vs-mutate principle on payment actions.
- [[orders-history]] — action 44 records chargebacks.
- [[settings-hooks]] — inbound webhook surface (where chargeback events arrive).
- [[orders-status-change]] — manual status changes (alternative to webhook-driven flips).

## Open questions

None.
