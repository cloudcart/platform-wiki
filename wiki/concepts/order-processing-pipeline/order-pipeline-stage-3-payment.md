---
type: concept
nav_path: "Concept → Order processing pipeline → Stage 3 Payment"
aliases: ["Payment status sync", "Payment gateway webhook", "Stage 3 payment", "payment_intent.succeeded", "iCard 3DS return", "Payment row status flip", "Auto-recompute order status"]
tags: [orders, lifecycle, payment, side-effects, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[order-processing-pipeline]]. See the hub for the other aspects (placement, status transitions, fulfillment, edits, edge cases).

# Order pipeline — Stage 3: Payment status sync

## Definition

**Stage 3** fires when a payment row's status changes — typically because a payment gateway POSTs a confirmation webhook back to CloudCart (e.g., Stripe sends `payment_intent.succeeded`; iCard returns the 3DS success), or because the merchant manually edits the payment status on [[orders-payment-mark-paid]]. The chain runs four direct effects, then **cascades** into [[order-pipeline-stage-2-status]] by recomputing the order's status from the sum of payment-row statuses.

In practice, payment sync is the most common reason a customer's order moves from `pending` to `paid` without the merchant clicking anything.

## Scope

Covered:

- The four direct payment-sync effects.
- The order-status auto-recompute (the cascade into Stage 2).
- Manual mark-paid as an equivalent trigger.
- Idempotency of stock decrement when both Stage 2 and Stage 3 try to fire it.

Not covered here:

- The full Stage 2 chain that runs as the cascade — see [[order-pipeline-stage-2-status]].
- Pre-auth capture at fulfillment time — see [[order-pipeline-stage-4-fulfillment]].
- Per-provider payment-gateway setup — see [[settings-payment-providers]] and [[payment-provider-mechanism]].
- Per-payment refund flow — see [[orders-payment-refund]].

## Contrasts

- **Stage 3 vs Stage 2** — Stage 3 is triggered by a *payment row* changing status; Stage 2 by the *order* changing status. Stage 3 typically *causes* Stage 2 via the auto-recompute. The order can move `pending → paid` without a merchant click because Stage 3 fires Stage 2 in cascade.
- **Gateway webhook vs manual mark-paid** — both arrive at the same code path. The gateway webhook is asynchronous (the customer is no longer waiting); the manual mark-paid is synchronous in the merchant's request. The side-effects are identical.
- **Payment row vs Order row** — the order can have multiple payment rows (split payment, partial refund, COD + online). The auto-recompute sums them; the order status only flips when the sum of payment statuses crosses a threshold (all paid / fully refunded / etc.).

## Where it applies

Every path that changes the status of a payment row triggers Stage 3:

- Payment-gateway confirmation webhook (`payment_intent.succeeded`, 3DS return, etc.).
- Manual mark-paid by the merchant on [[orders-payment-mark-paid]].
- Refund issued from [[orders-payment-refund]] (flips the payment row to refunded).
- Capture completed at fulfillment for authorise-then-capture providers (see [[order-pipeline-stage-4-fulfillment]] step 6).

### The payment-sync chain

| # | Side-effect | Conditional |
|---|---|---|
| 1 | **Stock decrement** — if payment is now `completed`, stock decrements (note: this may overlap with Stage 2 step 1 if the order also moves to `paid` — the implementation guards against double-counting via the `tracked` flag) | Always |
| 2 | **Order status auto-recompute** — the order looks at the sum of payment statuses across all its payment rows and decides whether to move to `paid` / `completed` / `refunded` / etc.; that status move then fires [[order-pipeline-stage-2-status]] from the top | Always |
| 3 | **Invoice + receipt number generation** | Active invoicing provider |
| 4 | **Customer lifetime-spend recalculation queued** | Always |

The Stage 2 cascade in step 2 is the engine behind almost every "the order changed status by itself" observation. The merchant didn't touch the dropdown — Stage 3 did, in response to the gateway webhook.

### Idempotency: stock decrement across stages

The platform's stock-counter logic is **idempotent**. When Stage 3 step 1 decrements stock and then Stage 3 step 2 cascades into Stage 2 step 1 (which would also decrement stock), the per-line decrement-tracking flag prevents the double-count. See [[inventory-restock]] for the decrement-tracking flag mechanics and [[inventory-decrement-timing]] for the three moments stock can move.

### Sync-payments app integration

When the merchant has the [[apps-store-locations]] / courier-COD `sync_payments` capability enabled (per-provider toggle on [[settings-shipping]]; plan-gated by `shipping_payment_sync`), the courier API itself acts as the "gateway" — the courier reports back when COD is collected and the platform receives that as a payment-row status flip into Stage 3. The same chain runs.

## Related

- [[order-processing-pipeline]] — hub.
- [[order-pipeline-stage-1-place]] — for online-payment providers, Stage 1 only fires after the gateway return; Stage 3 then drives the status to `paid`.
- [[order-pipeline-stage-2-status]] — the cascade target of step 2.
- [[order-pipeline-stage-4-fulfillment]] — pre-auth capture also enters Stage 3 via a payment-row update.
- [[order-pipeline-known-edge-cases]] — gateway-webhook race conditions, duplicate webhook deliveries.
- [[orders-payment-mark-paid]] — manual mark-paid trigger.
- [[orders-payment-refund]] — refund trigger.
- [[orders-payment-capture]] — capture trigger.
- [[payment-provider-mechanism]] — how payment providers attach to orders.
- [[settings-payment-providers]] — per-provider configuration.
- [[settings-invoicing]] — invoice / receipt number generation.
- [[inventory-decrement-timing]] — when stock actually moves (one of three moments).
- [[inventory-restock]] — per-line decrement-tracking flag (idempotency).
- [[background-queue-inventory]] — customer-income recalculation queue.

## Open Questions

- **Partial payments + auto-recompute** — confirm exactly how the status auto-recompute handles a split-payment order where one payment row is `completed` and another is still `pending` (verify).
- **Duplicate-webhook idempotency** — gateways sometimes deliver the same webhook twice. Confirm what protects Stage 3 from running the chain twice on a duplicate (verify).
