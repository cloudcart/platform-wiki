---
type: concept
nav_path: "Concept → Order processing pipeline"
aliases: ["Order processing pipeline", "Order side-effects", "What happens when an order is placed", "Order events catalog", "Order lifecycle side-effects", "Two-phase event model orders", "OrderCreated PostOrderCreated"]
tags: [orders, lifecycle, processing, side-effects, troubleshooting, concepts]
plan_gates: []
created: 2026-05-28
updated: 2026-08-06
source_count: 10
---

# Order processing pipeline (end-to-end side-effects)

## Definition

When an order moves through CloudCart — from the moment the customer clicks "Place order", through payment confirmation, through fulfillment, and any later edits — **a chain of side-effects fires for every event**: inventory adjusts, the customer's lifetime spend recalculates, invoice numbers get issued, webhooks fan out, transactional emails go out, admin alerts queue, discount-usage counters tick, and history rows are written.

This concept is the **complete end-to-end side-effect catalogue** for every event in an order's life: who triggers it, what fires synchronously, what gets queued, which settings change behaviour, which webhooks fan out, which emails are sent. The Assistant consults it when the merchant asks *"why didn't X fire"*, *"why is my stock count wrong"*, *"why did the invoice number get assigned at THIS moment"*.

CloudCart uses a **two-phase event model**: pre-action events (`OrderCreated`, `OrderStatusChange`, `FulfillmentAdd`, etc.) fire SYNCHRONOUSLY inside the same web request and run the immediate effects; `Post*` events fire RIGHT AFTER and run the secondary effects (webhook fan-out, customer emails, history rows, discount-usage sync). The split exists so transactional work completes before any webhook or email goes out — if the immediate work fails the order rolls back; a slow webhook receiver never slows the checkout response.

**Synchronous vs queued:** synchronous effects run inside the customer's request; queued effects are picked up later by a [[background-queue-inventory|background process]]. **Failure handling:** most secondary effects are **swallowed-but-logged** — they fail silently for the customer and are captured in the platform error log. Critical-path effects (payment-authorisation cancellation, guest-to-customer conversion) instead block the user action on failure.

## Sub-pages (in this cluster)

Split into 7 aspect pages — the Assistant drills into the one that matches the question:

- [[order-pipeline-stage-1-place]] — Stage 1: order placement. Storefront / admin / draft entry-points; 11-step chain (guest conversion → gateway purchase → admin email → webhook fan-out → banned-IP cancel). Stock does NOT move here.
- [[order-pipeline-stage-2-status]] — Stage 2: status change. 11 statuses (stock-bearing / negative / `authorized`); 15-step chain including the auto-created return. Gateway callbacks suppress the post-events. Custom statuses are partial participants.
- [[order-pipeline-stage-3-payment]] — Stage 3: payment status sync. Gateway webhooks (`payment_intent.succeeded`, iCard 3DS) and manual mark-paid. Four-step chain cascades into Stage 2.
- [[order-pipeline-stage-4-fulfillment]] — Stage 4: fulfillment. Add (9 effects + pre-auth capture for `captureAutomaticAuthorization` gateways) vs remove (7 effects, no customer email; status auto-reset).
- [[order-pipeline-stage-5-edit]] — Stage 5: manual edits. Per-line add / edit / remove, discount, shipping, note, archive. Most edits fire their own `order.updated` inline; archive / change-customer / change-payment-method and draft orders do not.
- [[order-pipeline-recalculation]] — recalculation & freeze model: what re-derives vs stays frozen on edit, the `recalculate_locked` lock (paid → frozen), and the full set of conditions the **payment method** carries into the total (payment-linked fee, per-provider discount, payment-tied free shipping, payer side, payment-targeted Cart Rules, COD mode).
- [[order-pipeline-known-edge-cases]] — non-obvious: the gateway-callback suppression of webhook / email / history, `checkout.payment.submit` route-gating, gateway-timeout / duplicate webhooks, discount-counter race (15× retry), lifetime-spend lag, `SITE_PLAN_EXPIRED` exit, `test_mail` kill switch, custom-status pitfalls, the fulfilment-remove bypass, the reversal lock, "what can fail silently" symptom table.

## Scope

Covered (across the 7 sub-pages): order placement (storefront, admin "+ Add order", draft conversion); status changes (the 11 statuses); payment sync (gateway webhooks + manual mark-paid); fulfillment (waybill add / remove + pre-auth capture); manual edits on an existing order; cross-cutting background processes (discount usage, customer income, webhook retries, search-index sync); the 3 stock-decrement moments; failure handling.

Out of scope: the 11 statuses themselves (transitions / meaning) — see [[order-status-workflow]]; pre-placement journey — see [[checkout-flow]] + [[cart-vs-order-lifecycle]]; discount math — see [[discount-stacking]]; tax — see [[tax-computation]]; shipping rates — see [[shipping-calculation]]; webhook subscription mechanics — see [[settings-hooks]].

## Contrasts

Four sibling concepts cover the same lifecycle at different angles. This one answers *"what runs when X happens?"*. [[order-status-workflow]] answers *"what status is allowed after Y?"* (per-status rules). [[checkout-flow]] answers *"how does the customer pay?"* (pre-order journey). [[cart-vs-order-lifecycle]] answers *"cart vs order — what's the difference?"* (entity model). The Assistant uses this concept when the merchant asks *"why didn't X fire"*; the siblings cover their own merchant questions.

## Where it applies

Every order-screen surface emits events catalogued here — [[orders-add]] (manual order), [[orders-details]] (status + history + edits), [[orders-shipping-waybill]] (fulfillment), [[orders-products]] (line items), [[orders-payment-mark-paid]] (payment), [[orders-invoices]] (issue invoice), [[orders-export]] / archive bulk actions.

### Stock decrement — the 3 distinct moments

The most common merchant question — *"when does my stock count actually move?"* — has three answers because there are three independent moments where decrement can fire. The platform's stock-counter logic is **idempotent** — it tracks whether a given order has already been counted against inventory and won't double-decrement.

| Moment | Trigger | Source |
|---|---|---|
| **At first status-bearing transition** | Order reaches a status that counts as "stock is out" under its own snapshotted decrement setting — `paid` / `authorized` / `completed` always, plus `pending` when that setting is `pending` ([[order-pipeline-stage-2-status]] step 1) | Most common for storefront orders that go straight from cart to `pending` on a `pending`-configured store |
| **When payment is confirmed** | Payment row status flips to `completed` ([[order-pipeline-stage-3-payment]] step 1) | Most common for online-payment orders where placement happens before payment confirmation |
| **At fulfillment** | Waybill generated ([[order-pipeline-stage-4-fulfillment]] step 1) | Falls back here if the prior two skipped |

See [[inventory-decrement-timing]] for the `order_status_for_quantity_decrease` setting and the per-(status × fulfillment × setting) matrix; see [[inventory-restock]] for the per-line decrement-tracking flag that prevents double-counting.

### Merchant-configurable settings

The pipeline is **NOT plan-gated** — every event fires regardless of plan. But several merchant settings shape what fires: `order_status_for_quantity_decrease`, `guest_to_customer`, `product_threshold` on [[settings-cart]]; `administrator_email_notifications` + per-template flags on [[settings-admin-notifications]]; `customer_email_notifications` on [[marketing-omnichannel-mails-list|Customer mails settings]] (separate page); the `test_mail` plan-feature kill switch (see [[order-pipeline-known-edge-cases]]); `invoicing` + numbering on [[settings-invoicing]]; custom statuses on [[settings-statuses]] (second-class — see [[order-pipeline-stage-2-status]]); per-provider settings on [[settings-payment-providers]] and [[settings-shipping]]; geo-zone attachment on [[settings-geo-zones]].

### Webhook payload + background machinery

The `order.created` / `order.updated` payload is the order serialised flat: identifiers + timestamps + `status` + issued document numbers + `email_sent` + `abandoned` + `note_administrator` + `customer` + `products[]` + addresses + `payments[]` + `discounts[]` (real Discount rows AND Cart-Rule modifications, distinguished by `group: discount` vs `group: modification`) + tax / fees + totals + currency / language. Same shape for both events; receiver detects via webhook-header type.

Four background processes run after pipeline events: **discount usage sync** (10s delay; up to 15× retry on duplicate-key); **customer income update**; **webhook delivery retry** (up to 5× with a *linear* delay of 120s / 180s / 240s / 300s / 360s, then a final-failure alert via [[settings-hooks]]; a failed synchronous delivery gets one retry after 60s); **search-index quantity sync** (updates [[apps-advanced-search]] / built-in search). See [[background-queue-inventory]] for the queue catalogue.

## Related

- [[order-status-workflow]] — the 11 statuses + allowed transitions + custom statuses.
- [[orders-returns]] — the return side-effect (restock, refund, credit note, derived `return_status`) raised on a committed order.
- [[cart-vs-order-lifecycle]] — entity-level Cart vs Order differences.
- [[checkout-flow]] — pre-placement customer journey.
- [[inventory-tracking]] — hub for the inventory cluster; `tracked` flag + thresholds.
- [[inventory-decrement-timing]] — the `paid` vs `pending` setting.
- [[inventory-restock]] — per-line decrement-tracking flag (idempotency).
- [[products-change-log]] — per-product audit trail; Stage 2 stock movements write here.
- [[discount-stacking]] / [[tax-computation]] / [[shipping-calculation]] — input math for the order.
- [[order-totals-pipeline]] — the fixed stage order (subtotal → discounts → VAT → shipping → VAT-on-shipping → total) that combines that input math at placement and on recalc.
- [[payment-provider-mechanism]] — how payment providers attach to orders.
- [[notification-delivery]] — event → queue → outbound delivery pattern.
- [[background-queue-inventory]] — queue catalogue for all deferred side-effects.
- [[settings-hooks]] — webhook subscription + delivery log.
- [[settings-admin-notifications]] / [[marketing-omnichannel-mails-list]] — admin vs customer email gating.
- [[settings-invoicing]] — invoice / receipt / credit-note numbering.
- [[settings-cart]] — `order_status_for_quantity_decrease`, `guest_to_customer`, `product_threshold`.
- [[settings-payment-providers]] / [[settings-shipping]] / [[settings-geo-zones]] / [[settings-statuses]] — merchant-side toggles that shape the pipeline.
- [[orders-details]] / [[orders-shipping-waybill]] / [[orders-payment-mark-paid]] / [[orders-products]] / [[orders-notify-customer]] — the order-screen surfaces that trigger each stage.

## Open Questions

None at the hub level — all previously-flagged items distributed to the relevant aspect pages ([[order-pipeline-stage-1-place]], [[order-pipeline-stage-2-status]], [[order-pipeline-stage-3-payment]], [[order-pipeline-stage-4-fulfillment]], [[order-pipeline-known-edge-cases]]).
