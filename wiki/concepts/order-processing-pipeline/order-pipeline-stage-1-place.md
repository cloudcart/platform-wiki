---
type: concept
nav_path: "Concept → Order processing pipeline → Stage 1 Place"
aliases: ["Order placement pipeline", "OrderCreated side-effects", "Stage 1 order place", "Order create chain", "What fires when an order is placed", "Draft to real order"]
tags: [orders, lifecycle, placement, side-effects, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-08-06
source_count: 4
---

> Part of [[order-processing-pipeline]]. See the hub for the other aspects (status transitions, payment sync, fulfillment, edits, edge cases).

# Order pipeline — Stage 1: Order placement

## Definition

**Stage 1** is the chain that fires when a brand-new order is created — the moment the customer clicks "Place order" at storefront checkout, or the merchant clicks **+ Add order** on [[orders-add]] for a manual offline-payment order, or a saved draft is finalised. The order row + product lines are written, the payment gateway is contacted (for online providers), and a fan-out of secondary effects (admin email, webhook, search-index sync, customer-income recalc, live admin broadcast) is dispatched. Stock decrement does NOT happen here for storefront orders — that waits for the first status-bearing transition (see [[order-pipeline-stage-2-status]]).

## Scope

Covered:

- Three entry-points (storefront checkout, admin manual order, draft conversion) and how they differ.
- The placement chain itself, step by step.
- Pre-action vs post-action split (`OrderCreated` vs `PostOrderCreated`).
- Synchronous vs queued effects in this stage.
- Draft-mode short-circuit — no events fire while `is_draft` meta is present.
- Banned-IP auto-cancellation for offline-payment orders.

Not covered here:

- Stock decrement (deferred to Stage 2 — see [[order-pipeline-stage-2-status]]).
- Online-payment confirmation arriving later — see [[order-pipeline-stage-3-payment]].
- Pre-checkout journey — see [[checkout-flow]] and [[cart-vs-order-lifecycle]].

## Contrasts

- **Storefront checkout vs admin manual order** — storefront fires the full chain end-to-end. Admin manual orders only fire Stage 1 when the payment provider is OFFLINE (cash on delivery, bank transfer); for ONLINE providers the merchant instead sends a payment-URL to the customer and Stage 1 fires later when the customer pays.
- **Draft vs confirmed** — admin manual orders start in **draft** (`is_draft` meta present). While drafted, NO webhooks fire and NO events fan out. The platform short-circuits every event side-effect. Once the merchant clicks **Confirm**, the draft flag is removed and the placement pipeline runs from the top.
- **Pre-action vs post-action events** — `OrderCreated` fires SYNCHRONOUSLY inside the same web request and runs the immediate work (gateway purchase call, row writes). `PostOrderCreated` fires RIGHT AFTER and runs the secondary effects (webhooks, emails, history rows). The split ensures the customer's HTTP response isn't blocked on a slow webhook receiver.

## Where it applies

Every entry point that produces a fresh order:

| Entry-point | Where the merchant sees it | Variation |
|---|---|---|
| **Storefront checkout** | Order appears on [[orders]] | Full chain below |
| **Admin manual order** | [[orders-add]] | Only fires when payment provider is OFFLINE; ONLINE providers defer to gateway return |
| **Draft conversion** | The draft surface inside [[orders-add]] | Identical to storefront flow once confirmed |

### The placement chain — what fires, in order

| # | Side-effect | When | Setting that changes it | If it fails |
|---|---|---|---|---|
| 1 | **Guest converted to customer** — if the storefront cart had a guest who completed checkout, their guest record gets turned into a full customer record (with the entered email, addresses, etc.) | Sync, before the order row is written | `guest_to_customer = yes` on [[settings-cart]] (when off, the guest stays as an anonymous one-time buyer) | Rethrown — placement aborts |
| 2 | **Order row + product lines written to the database** | Sync | n/a | Rethrown — placement aborts |
| 3 | **Payment-gateway "purchase" call** — for online payment providers, the platform calls the gateway to start the payment session (e.g., Stripe creates a PaymentIntent, the customer sees the gateway's pay page) | Sync | n/a | Rethrown — placement aborts |
| 4 | **Admin "new order" email queued** | Queued to the admin-notification background process | The master `administrator_email_notifications = yes` AND the "New Order Add" row's own on/off switch on [[settings-admin-notifications]] — when either is off, no admin email is sent | Swallowed (logged for CloudCart support) |
| 5 | **Customer lifetime-spend recalculation queued** | Queued | Platform-config gate (always on for active stores) | Swallowed |
| 6 | **Webhook `order.created` fan-out** — carries a **24-hour idempotency guard**, so a retried or re-dispatched creation cannot deliver it twice for the same order | Sync or queued **per subscriber** — each subscription carries its own flag; the number of subscribers is never counted (see [[settings-hooks]]) | Per-hook subscription on [[settings-hooks]] | Sync hook: swallowed for the customer's response, then retried once after 60s; queued hook: retried up to 5× at 120s / 180s / 240s / 300s / 360s; final failure alerts the merchant |
| 7 | **Storefront search index quantity sync** — every product on the order has its remaining stock pushed to the search index (so the storefront's *"only N left"* / *"sold out"* badges update) | Sync (event handler) | n/a | Swallowed |
| 8 | **Per-product `product.updated` webhook fan-out** — one webhook per product on the order (subscribers see the stock-changed payload) | Same machinery as `order.created`, minus the idempotency guard | [[settings-hooks]] | Same as above |
| 9 | **Storefront session cleanup** — UTM tracking data and Advanced-Search filters are dropped from the customer's session | Sync | n/a | Swallowed |
| 10 | **Live admin-dashboard broadcast** — *"new order"* notification appears on the merchant's [[notifications|admin notifications]] popover for any currently-logged-in admin | Sync WebSocket broadcast | Storefront-only (not fired for admin manual orders) | Swallowed |
| 11 | **Banned-IP cancellation** — if the order originated from an IP in the merchant's banned-IP list AND the payment provider is OFFLINE, the order is immediately auto-cancelled with `notify_customer = 0` and a reason recorded in `note_administrator` | Sync; after step 6 | Banned-IP list lives in admin-only screens; affects only offline-payment orders | Swallowed |

**Stock decrement does NOT happen here** for storefront orders. Stock moves only when the order's status transitions into a status that counts as "stock is out" under the decrement setting snapshotted onto the order at placement — see [[order-pipeline-stage-2-status]].

**Order is in "draft" until the merchant explicitly confirms it** for admin manual orders. While drafted, NO webhooks fire and NO events fan out. Once the merchant clicks **Confirm**, the pipeline runs from the top.

### Failure handling in Stage 1

Steps 1–3 (`guest_to_customer`, row writes, gateway purchase) are **critical-path** — failure rethrows and aborts the placement. The customer sees the error on the checkout page. The order row is rolled back.

Steps 4–11 are **swallowed-but-logged** — failure does NOT surface to the customer. The platform's error log captures them for CloudCart support to review. This is by design: a slow webhook receiver or a backed-up email queue cannot block the customer's "thank you" response.

## Related

- [[order-processing-pipeline]] — hub.
- [[order-pipeline-stage-2-status]] — sibling stage that handles stock decrement once the order leaves `pending`.
- [[order-pipeline-stage-3-payment]] — sibling stage for the deferred online-payment confirmation that turns into a status change.
- [[order-pipeline-known-edge-cases]] — gateway timeouts, draft-confirm race conditions, and other Stage 1 edge cases.
- [[checkout-flow]] — pre-placement customer journey.
- [[cart-vs-order-lifecycle]] — entity-model differences between Cart and Order.
- [[orders-add]] — admin manual-order screen (draft entry-point).
- [[orders]] — order list where placed orders appear.
- [[settings-cart]] — `guest_to_customer` toggle.
- [[settings-admin-notifications]] — admin "new order" email gating (master switch + the notification's own row).
- [[settings-hooks]] — webhook subscription + delivery log.
- [[background-queue-inventory]] — which queue handles the deferred work.

## Open Questions

- **Banned-IP list UI** — confirm which admin screen exposes the banned-IP list to merchants (currently described as "admin-only screens") (verify).
- **WebSocket broadcast for admin manual orders** — verified that the live-dashboard broadcast is storefront-only; confirm whether any admin-side broadcast equivalent exists for manual orders (verify).
