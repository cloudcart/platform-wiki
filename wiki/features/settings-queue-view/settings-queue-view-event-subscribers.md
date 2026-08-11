---
type: feature
nav_path: "Settings → Queue → Event subscribers & webhook fan-out"
route_name: queue.settings
route_path: /admin/settings/queue-view
aliases: ["Event subscribers", "Webhook fan-out", "Order event subscriber", "the platform code", "HooksSendRaw"]
tags: [settings, queue, events, webhooks, subscribers]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-queue-view]]. See the hub for the other aspects (page UI, actions, visibility, running-detection, recurring jobs, queue families).

# Queue — event subscribers + webhook fan-out

## Purpose

Map how CloudCart's internal events fan out into queued jobs via event subscribers. Specifically: which events the order-event subscriber handles, what side-effect jobs each event dispatches, and how a single order save becomes one webhook-delivery job per active subscribing webhook on the `order-events8` queue.

This is the aspect the support LLM needs when the merchant asks: *"why did 4 webhooks fire from one order change?"* or *"which queue is delivering my webhook?"*.

## Where to find it

Sidebar → Settings → **Queue**. Route `/admin/settings/queue-view`. Whether the resulting jobs surface on the page depends on visibility — see [[settings-queue-view-visibility-rules]].

## What the merchant can do here

The merchant configures webhooks on [[settings-hooks]] — which then ride this fan-out. The merchant does NOT configure the event-subscriber layer; it's platform code.

## Settings & fields

### Event → Subscriber → Job map

CloudCart's internal events fan out to queued jobs via event subscribers. The seven key subscribers (verify):

| Subscriber | Events handled | Side-effect jobs dispatched |
|---|---|---|
| Order-event subscriber | Order created, order created (post step), payment sync, order product added / edited / removed, order status change, order status change on return, fulfilment added / removed, order archived / unarchived, order note edited, order shipping changed, order product discount added / removed, order product modification removed, pre-order created, order payment updated (18 events) | Webhook delivery on `order-events8`; per-order analytics on `analytics2` with 0 s / 5 s / 60 s delays per event type; status-history rows; customer-income-update job |
| Post-order-event subscriber | Order created (post step), order status change (post step), fulfilment added / removed (post step) (4 events) | Status-change notification emails / SMS (per [[settings-statuses]]); admin alerts for new orders |
| Billing-event subscriber | Transaction created, subscription created / renewed / updated, subscription upcoming payment, offer created / updated, invoice created / updated (9 events) | Internal billing accounting writes; merchant notification emails about renewals + upcoming payments |
| Site-event subscriber | Admin login, admin login (lite), site created, site onboarding (4 events) | Login auditing; site-creation analytics; onboarding kickoff jobs |
| User-event subscriber | Storefront login, logout, register, guest register | Storefront customer session tracking |
| Post-order banned-IP subscriber | Order created (post step) | Risk-engine IP-ban check for new orders |
| Quantity-change listener | Stock quantity created / updated / deleted | Triggers follow-on stock-quantity-update / stock-quantity-delete events |

### Webhook event-type mapping — NOT 1:1 with domain events

The platform's outbound Webhook event types are not 1:1 with the internal save / delete events above. The mapping the platform uses:

| Internal change | Webhook event(s) fired |
|---|---|
| Order saved | `order.created` on insert, `order.updated` on any subsequent save |
| Product saved | `product.created` / `product.updated` |
| Customer saved | `customer.created` / `customer.updated` |
| Customer deleted | `customer.deleted` |
| Product deleted | `product.deleted` |
| Category saved / deleted | `category.*` |
| Vendor saved / deleted | `vendor.*` |
| Discount saved / deleted | `discount.*` |
| Subscriber saved / deleted | `subscriber.*` |
| (intentionally absent) | `order.deleted` — disabled in the platform's webhook event-type list |

When one of these records is saved or deleted, the platform raises a single webhook event carrying the event type plus the entity; it is dispatched once and inflated into one webhook-delivery job per active subscribing Webhook.

### Webhook delivery queue — `order-events8`

Webhook deliveries (the actual HTTP POST attempt to the webhook URL) run on the `order-events8` queue, processed by the `worker-order-events` daemon group (see [[settings-queue-view-queue-families]]). The initial multi-webhook fan-out AND every retry attempt go through this same mapping (`order_hooks_send`) and queue.

## Business rules

### Why a single order change can produce many webhook deliveries

A single order save on a store with N active webhooks subscribed to `order.updated` produces:

- 1 webhook event dispatch.
- 1 fan-out job execution → inflates into N webhook-delivery jobs (one per subscribing webhook).
- Up to N HTTP POSTs to the merchant's webhook receivers.

If any individual delivery fails, that single delivery is retried independently. See [[settings-hooks]] for retry policy + auto-disable behaviour.

### Why webhook deliveries usually do NOT appear on the Queue page

The webhook-delivery job runs on the `order-events8` queue, separately from the per-site queue entries that power the Queue page. Whether a queue-page row is created with `is_visible = true` depends on the platform's per-mapping config. In practice the merchant relies on:

- The webhook auto-disable alert from [[settings-hooks]] for delivery failures.
- Their own receiver-side logging.
- The Queue page only for visibility-enabled jobs.

See [[settings-queue-view-visibility-rules]] for the full visible / hidden catalogue.

### Per-order analytics has staggered delays — 0 s / 5 s / 60 s

The order-event subscriber dispatches analytics writes to `analytics2` with staggered delays (0 s / 5 s / 60 s) depending on the event type. This is intentional — it lets payment-gateway-driven status updates settle before the final aggregation runs. The merchant sees this as *"analytics catches up about a minute after a status change"*, not in real-time.

### Order deletion does NOT fire a webhook

The `order.deleted` event type is intentionally absent from the platform's webhook event-type list (verify). The merchant cannot subscribe to it via [[settings-hooks]] because the platform does not fire it. This is by design — order deletion is rare, and the platform prefers `cancelled` / `refunded` status transitions which DO fire `order.updated`.

## Related

- [[settings-queue-view]] — hub.
- [[settings-queue-view-queue-families]] — `worker-order-events` daemon and the `order-events8` queue.
- [[settings-queue-view-visibility-rules]] — why webhook deliveries usually don't show on the Queue page.
- [[settings-queue-view-recurring-jobs]] — `order_hooks_send` one-shot mapping.
- [[settings-hooks]] — webhook subscription, auto-disable, retry policy.
- [[settings-statuses]] — status-change notification email / SMS pipeline driven by the platform code.

## Open questions

None.
