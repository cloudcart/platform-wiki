---
type: concept
nav_path: "Concept → Order processing pipeline → Stage 4 Fulfillment"
aliases: ["Fulfillment add", "Fulfillment remove", "Waybill side-effects", "Stage 4 fulfillment", "captureAutomaticAuthorization", "Pre-auth capture", "Fulfill products", "Mark as unfulfilled"]
tags: [orders, lifecycle, fulfillment, shipping, side-effects, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-08-06
source_count: 3
---

> Part of [[order-processing-pipeline]]. See the hub for the other aspects (placement, status transitions, payment sync, edits, edge cases).

# Order pipeline — Stage 4: Fulfillment

## Definition

**Stage 4** fires when the merchant generates a waybill on [[orders-shipping-waybill]] (whether through the courier-specific waybill form or the generic fallback form) — the **fulfillment-add** event — or when the merchant clicks **Remove waybill** to void the dispatch on the courier side — the **fulfillment-remove** event. Each branch has its own chain. Fulfillment-add can also capture a pre-authorised payment for authorise-then-capture gateways (e.g., Stripe), turning the held auth amount into a real charge.

## Scope

Covered:

- The fulfillment-add chain step by step.
- The fulfillment-remove chain step by step.
- Pre-auth capture at fulfillment time (`captureAutomaticAuthorization` capability).
- Idempotency of stock decrement with prior stages.
- Why there is no customer email on fulfillment-remove.

Not covered here:

- Courier-specific waybill form mechanics — see [[orders-shipping-waybill]].
- Shipping rate calculation — see [[shipping-calculation]].
- Per-provider receiver-pays / sender-pays toggles — see [[orders-shipping-waybill]].
- Per-shipping-provider `sync_payments` and free-shipping settings — see [[settings-shipping]].

## Contrasts

- **Fulfillment-add vs fulfillment-remove** — add fires 9 effects (including the customer "shipped" email); remove fires 7 effects and **no customer email**. The customer is not notified that their shipment was voided.
- **Pre-auth capture vs sync charge** — for gateways supporting `captureAutomaticAuthorization` (Stripe and similar), the customer's card is pre-authorised at order placement and the actual charge fires here (step 6). For sync-charge gateways the charge already happened at placement; step 6 is a no-op.
- **Status flip on remove** — fulfillment-remove rewrites the order status back to `paid` (if the last payment is `completed`) or `pending` **directly, bypassing the status pipeline**: no status-change event, so no history row, no customer email, no `order.updated` from the status side. It also only restocks on orders whose snapshotted decrement setting is `paid`.

## Where it applies

Every fulfillment surface enters here:

- Courier-specific waybill form on [[orders-shipping-waybill]] (the generic fallback form too).
- Bulk fulfillment actions on [[orders]].
- Mark-as-fulfilled toggle on [[orders-details]] (no waybill, but the fulfillment flag flips).

### Fulfillment-add chain

| # | Side-effect | Conditional |
|---|---|---|
| 1 | **Stock decrement** (idempotent — already-decremented orders from Stage 2 don't double-count) | Per-product `tracked` flag |
| 2 | **Invoice + receipt number generation** | Active invoicing provider |
| 3 | **Order history row "fulfillment add"** | Always |
| 4 | **Status-history transition: `not_fulfilled` → `fulfilled`** | Always |
| 5 | **Customer lifetime-spend recalculation queued** | Always |
| 6 | **Pre-authorised payment captured** — for gateways supporting authorise-then-capture (e.g., Stripe), the held auth amount is now turned into a real charge | Payment row has `authorize_amount` AND gateway supports `captureAutomaticAuthorization` |
| 7 | **Webhook `order.updated` fan-out** | [[settings-hooks]] subscribers |
| 8 | **Customer "your order shipped" email queued** | `notify_customer = yes` on the order |
| 9 | **Discount-usage counter sync queued** | Always (belt-and-suspenders) |

### Fulfillment-remove chain

| # | Side-effect | Conditional |
|---|---|---|
| 1 | **Order status auto-reset** — back to `paid` (if last payment is `completed`) or `pending` | Always |
| 2 | **Stock restoration** | Per-product `tracked` flag |
| 3 | **Order history row "fulfillment remove"** | Always |
| 4 | **Status-history transition: `fulfilled` → `not_fulfilled`** | Always |
| 5 | **Customer lifetime-spend recalculation queued** | Always |
| 6 | **Webhook `order.updated` fan-out** | [[settings-hooks]] subscribers |
| 7 | **Discount-usage counter sync queued** | Always |

**No customer email is sent on fulfillment removal** — the customer is not notified that their shipment was voided.

### Auto-fulfillment for digital orders

A **fully-digital order auto-fulfills when it reaches `paid`** — the platform marks the fulfillment automatically (no waybill, no click at all), because there is nothing physical to dispatch (see [[digital-products]] for the `digital` flag that drives this). Adding a digital product that turns an order all-digital also auto-fulfills it. Combined with `order_complete = 1` (`paid + fulfilled → completed`), a paid digital order therefore **auto-promotes straight to `completed`** with no manual shipping step — see [[order-status-auto-transitions]]. For a **mixed** order, only the physical lines need fulfillment: the waybill flow covers the `digital = no` products and excludes digital lines (see [[orders-shipping-waybill]]).

### Idempotency: stock decrement across stages

Fulfillment-add step 1 is one of the three moments stock can move (see [[inventory-decrement-timing]]). When Stage 2 has already decremented the order's stock (because the status moved to `paid` first), this step is a no-op via the per-line decrement-tracking flag. The merchant should not see stock move twice for one order even if a status change AND a payment sync AND a fulfillment all happen in sequence.

### Pre-auth capture (step 6) in practice

For Stripe-style authorise-then-capture flows:

- Customer card is pre-authorised at order placement (Stage 1 step 3 calls the gateway's purchase that returns an auth, not a settled charge).
- Cancellation before fulfillment releases the pre-auth at [[order-pipeline-stage-2-status]] step 7 (negative-status transition).
- Fulfillment-add at step 6 here captures the held auth — this is the moment the customer's card actually settles.
- The auto-capture-vs-authorise behaviour is a **gateway capability** (defined in the provider's integration code), NOT a merchant-toggleable setting.

A merchant who hits "fulfillment add" before realising the customer already cancelled by phone will trigger a successful capture on a pre-auth that should have been released. The fix is to manually refund via [[orders-payment-refund]].

## Related

- [[order-processing-pipeline]] — hub.
- [[order-pipeline-stage-1-place]] — pre-auth held at placement; released or captured here.
- [[order-pipeline-stage-2-status]] — the status chain that fulfillment-remove bypasses.
- [[order-pipeline-stage-3-payment]] — pre-auth capture flips a payment row, which cascades into Stage 3 effects.
- [[order-pipeline-known-edge-cases]] — capture-on-cancelled-order edge case, sync-payments flips.
- [[orders-shipping-waybill]] — fulfillment-add / fulfillment-remove triggers.
- [[orders-details]] — mark-as-fulfilled toggle.
- [[orders-payment-capture]] — manual capture surface (mirrors the auto-capture at step 6).
- [[orders-payment-refund]] — refund path when capture was incorrect.
- [[shipping-calculation]] — shipping rate at checkout time.
- [[settings-hooks]] — webhook subscription.
- [[settings-invoicing]] — invoice / receipt number generation.
- [[inventory-decrement-timing]] — three moments stock can move.
- [[inventory-restock]] — per-line decrement-tracking flag for idempotency.
- [[settings-shipping]] — per-provider `sync_payments` and free-shipping settings.

## Open Questions

- **Mark-as-fulfilled without waybill** — confirm whether [[orders-details]] exposes a "mark fulfilled" toggle that triggers Stage 4 without producing a waybill row (verify).
- **Per-gateway capture-support matrix** — Stripe is verified to support `captureAutomaticAuthorization`; CloudCart Pay and other gateways need confirmation (verify).
