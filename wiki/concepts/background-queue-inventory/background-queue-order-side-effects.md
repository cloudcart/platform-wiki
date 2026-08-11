---
type: concept
nav_path: "Concept → Background processes → Order side-effects + campaigns"
aliases: ["Order side-effects", "Order async fan-out", "Webhook delivery queue", "Discount usage counters", "Admin-panel notifications", "Marketing campaign delivery", "Campaign segment recalculation", "Campaign send"]
tags: [background, async, orders, webhooks, campaigns, support, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[background-queue-inventory]]. See the hub for related aspects (recurring platform jobs, imports/exports, the search index sync, Queue View, process catalogue).

# Background processes — order side-effects + campaign delivery

## Definition

When a customer places, edits, or cancels an order, **several side-effect processes fire** to keep downstream state in sync — discount-usage counters increment, outbound webhooks deliver to the merchant's external systems, admin-panel notifications queue for display. Separately, **marketing-campaign delivery** runs through its own background processes: segment members are recalculated when a campaign with a segment trigger fires, the subscriber list is materialised just before send, and individual messages (email / SMS / Viber / web push) are dispatched.

The merchant interacts with these mostly indirectly — the order goes through, the webhook arrives at the merchant's external system, the campaign messages start landing in subscriber inboxes. Failures surface on [[settings-queue-view]] (for visible campaign processes) and [[settings-hooks]] (for webhook delivery).

## Scope

Covered:

- Order-driven async fan-out: discount-usage counter increment, outbound webhook delivery, admin-panel notification queuing.
- Site provisioning (new site setup).
- Marketing campaign processes: segment member recalculation, subscriber-list materialisation, message dispatch (email / SMS / Viber / web push).
- Visibility rules per process category.

Not covered:

- The order status transitions themselves — see [[order-processing-pipeline]] + [[orders-status-change]].
- Stock decrement / restock triggered by status change — that's inventory, see [[inventory-decrement-timing]] + [[inventory-restock]].
- the search index sync triggered by stock change — see [[background-queue-search-sync]].
- Webhook event reference per event name — see [[settings-hooks]].
- Campaign authoring — see the marketing feature pages.

## Contrasts

- **Order side-effect vs order pipeline.** The order pipeline (status transitions, payment capture, stock decrement) is the **primary** flow. Side-effects (counters, webhooks, notifications) are the secondary fan-out that happens **after** the primary flow lands. A failed webhook never blocks the order itself.
- **Outbound webhook vs admin notification.** Outbound webhooks deliver to the merchant's external HTTPS endpoint (configured on [[settings-hooks]]). Admin notifications are intra-platform — they queue messages for display in the admin panel's notification bell or for transactional email send.
- **Segment recalculation vs subscriber-list materialisation.** Recalculation determines who currently belongs to a segment given the latest subscriber data; materialisation snapshots that list at send time so the campaign sends to a stable cohort even if memberships change mid-send.

## Where it applies

### Order side-effects

| What happens | When | Visible on Queue View |
|---|---|---|
| Discount-usage counters are updated for any [[discount]] applied to the order | On order placement / payment / cancellation | No |
| Outbound webhooks to the merchant's external systems are delivered | On order placement / status change | No (visible on [[settings-hooks]]) |
| Admin-panel alerts for the merchant (new order, low stock, payment failed) are queued | At the triggering event | No |

Webhook delivery deserves special attention: it is the **chattiest** of all background processes. `product.updated` fires on every stock change; `order.created` / `order.updated` / `order.status.changed` fire on the order lifecycle. Merchant integrations must be idempotent — the same event can deliver more than once on retry. See [[settings-hooks]] for the catalogue of event names and the delivery-retry policy.

Admin-panel notification queuing is what feeds the admin's notification bell and triggers transactional-email sends for things like *"New order #N just arrived"*, *"Low stock on Product X"*, *"Payment failed on order #N"*. The actual transactional email send runs on a generic email queue downstream.

### Site provisioning

| What happens | When | Visible on Queue View |
|---|---|---|
| New site is provisioned (database created, default settings seeded, default theme installed) | Merchant signs up for a new CloudCart account | No |

This runs once per new site, single-platform-wide-locked (only one site provisions at a time). New-merchant onboarding completion depends on this process finishing — typically within a minute or two. If a brand-new merchant says *"my admin panel won't load after signup"*, the provisioning may still be running.

### Marketing campaign delivery

| What happens | When | Visible on Queue View |
|---|---|---|
| Segment members are recalculated when subscribers come in / out of scope | When a campaign with a segment trigger fires | Yes |
| Subscriber list is materialised for a scheduled campaign | Just before the campaign sends | Yes |
| Individual campaign messages (email / SMS / Viber / web push) are dispatched | At campaign send time | Yes |

Campaign delivery is visible on Queue View because the merchant needs progress feedback for large sends — *"how many of my 50 000 subscribers have we hit so far?"* The visible processes surface the in-progress count; the actual per-message dispatch happens on per-channel sub-queues that are not individually surfaced (a stuck single email is invisible; only a stuck overall campaign is visible).

**What "stuck campaign" looks like.** If a scheduled campaign shows **Running** on Queue View for more than 30 minutes without progress, escalate — most segment recalculations finish in under 10 minutes even for large subscriber bases. The watchdog automatically kills hung workers every 2 minutes (see [[background-queue-view-and-stuck]]) so a truly stuck row points to a deeper issue (broken segment query, dispatch credential failure, third-party SMS gateway outage) rather than a hung worker.

**Failed campaign delivery.** A failed campaign typically points to a recipient-quota issue (plan limit) or a credential issue (SMS / push provider). The Failed row carries the one-line error message. The merchant can re-trigger the campaign once the underlying issue resolves.

## Related

- [[background-queue-inventory]] — hub.
- [[settings-queue-view]] — visible-campaign progress.
- [[settings-hooks]] — webhook delivery surface.
- [[order-processing-pipeline]] — order status flow that fires these side-effects.
- [[orders-status-change]] — status-transition triggers.
- [[discount]] — usage-counter target.
- [[notification-delivery]] — Event → Subscriber → Background Process pattern.
- [[background-queue-view-and-stuck]] — watchdog mechanics + stuck-campaign diagnosis.
- [[background-queue-process-catalogue]] — internal-identifier mapping.

## Open Questions

None.
