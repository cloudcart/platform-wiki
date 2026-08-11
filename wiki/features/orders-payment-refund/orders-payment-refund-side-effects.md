---
type: feature
nav_path: "Orders → Order details → Payment → Refund → Side effects"
route_name: admin.orders.payment.refund
route_path: /admin/orders/action/payment/refund/:payment_id
aliases: ["Refund side effects", "Refund cascade", "Refund stock restock", "Refund customer income", "Refund webhook", "Refund history action"]
tags: [orders, payment, refund, side-effects, webhook, inventory]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[orders-payment-refund]]. See the hub for the other aspects (visibility, provider matrix, gateway quirks, partial refunds, status-flip rules, API access).

# Payment refund — side effects on success

## Purpose

When a refund succeeds at the gateway, the platform performs a cascade of side effects via the **PaymentSync event listener**. This page catalogues the cascade so the merchant (and support agent) knows exactly what changes — and what doesn't — when the toast says *"Refund successful"*.

## Where to find it

Triggered by a successful refund call from [[orders-details]] (per [[orders-payment-refund-visibility]]). The side effects below run AFTER the gateway returns success and the local payment record flips to `refunded` — they are NOT toggleable per-refund; the cascade is unconditional.

## What the merchant can do here

This page documents automatic behaviour. The merchant observes the side effects in [[orders-history]], the product's [[products-change-log|Change log]], and the customer's lifetime-spend stat — there are no toggles on this surface.

## Settings & fields

### Side-effect cascade (in execution order)

| Side effect | Where it shows | Configurable? |
|-------------|----------------|---------------|
| Payment record flips to `refunded` | Order payment row + [[api-order-payment]] | No |
| `refunded_at` timestamp set on the payment | [[api-order-payment]] | No |
| Order status auto-flip to `refunded` (conditional) | Order header + [[orders]] list | Conditional on multi-payment + manual-override state — see [[orders-payment-refund-status-flip-rules]] |
| Stock auto-restore on every variant in the order | Each [[variant]]'s `quantity` increments; recorded in [[products-change-log]] | No — always on |
| Customer lifetime-income aggregate decrement | Customer profile spend stat | No |
| `order.updated` webhook fires | Receivers configured on [[settings-hooks]] | Per-webhook subscription only |
| History action 20 (`order_payment_refunded`) appended | [[orders-history]] | No |
| Order-level history action 43 (`order_refunded`) appended (if order auto-flipped) | [[orders-history]] | No — fires only when the order itself flips to `refunded` |
| Customer email | NOT sent — currently disabled in this flow | The merchant uses [[orders-credit]] to email the customer |

## Business rules

### Stock auto-restore is unconditional

When the payment status changes to `refunded` and the platform code event fires, the listener restores stock for every line in the order. The variants' `quantity` is incremented by the refunded line quantities. This happens **regardless** of `settings-cart` flags about stock-restore — it's always on for the platform's own event handler.

This may surprise merchants who expect to manually decide whether to restock refunded items (e.g., damaged goods that can't be resold). For damaged goods, the merchant needs to manually decrement the variant after the refund to undo the unwanted auto-restock. The stock change appears in [[products-change-log]] with the refund as the Initiator. See [[inventory-restock]] for the broader restock catalogue and [[inventory-tracking]] for the inventory model.

### Order auto-flip is conditional

The order's status flips to `refunded` ONLY when no other completed / authorized / pending payments exist on the order, and the merchant has NOT manually set the order's status. See [[orders-payment-refund-status-flip-rules]] for the full conditions.

### No customer email by default

The notification call in the refund flow is COMMENTED OUT — clicking Refund does NOT directly email the customer. To notify the customer, the merchant should issue + send the credit note via [[orders-credit]] which has its own dedicated send action.

This is a deliberate gap that catches merchants by surprise — many expect a refund email mirror of the order confirmation. The standard remediation is either:
- Manually email the customer (no automated email exists).
- Generate a credit note via [[orders-credit]] and click **Send credit note** — that flow emails the customer with the document attached.

### Customer income aggregate decrement

Each customer carries a lifetime-spend aggregate (`income`). A refund decrements this aggregate by the refunded amount, so the customer's spend stat in their profile, the merchant's customer reports, and any segmentation rules based on lifetime spend all reflect the reversal. The decrement is automatic — no merchant action required.

### `order.updated` webhook fires

The PaymentSync listener emits `order.updated` per [[settings-hooks]]. Receivers must be idempotent — a refund delivers the same event shape as any other order update, with the updated payment + order status reflecting the refund. ERP systems / accounting integrations typically consume this to mirror the refund externally.

### History codes — full vs partial vs order-level

| Action | When |
|--------|------|
| 20 (`order_payment_refunded`) | This Refund button clicked + gateway returns full refund. |
| 21 (`order_payment_partially_refunded`) | Gateway webhook reports a partial refund (initiated outside CloudCart) — see [[orders-payment-refund-partial-refunds]]. |
| 43 (`order_refunded`) | Order status changed to Refunded (only when the conditional auto-flip succeeds — see [[orders-payment-refund-status-flip-rules]]). |
| 44 (`chargebacked`) | Separate flow — gateway-initiated via webhook, NOT this button. See [[orders-payment-refund-api-access]]. |

The merchant CAN see in [[orders-history]] who refunded the order and when, with the appropriate action_string per the type.

## Related

- [[orders-payment-refund]] — hub.
- [[orders-payment-refund-status-flip-rules]] — when the order itself flips to `refunded`.
- [[orders-payment-refund-partial-refunds]] — webhook-driven partial refunds (action 21).
- [[orders-history]] — where the refund action lands.
- [[orders-credit]] — credit-note flow that DOES email the customer.
- [[settings-hooks]] — `order.updated` webhook.
- [[settings-cart]] — does NOT gate the auto-restore (always-on at the event handler).
- [[inventory-restock]] — broader restock catalogue (sibling-flow context).
- [[inventory-tracking]] — inventory model.
- [[products-change-log]] — where the stock auto-restore is logged.
- [[order-processing-pipeline]] — refund triggers the negative-status side-effects.

## Open questions

None.
