---
type: concept
nav_path: "Concept → Order status workflow → Auto-transitions"
aliases: ["Auto-promote to completed", "Auto-promotion", "order_complete setting", "Banned IP auto-cancel", "Gateway-driven status", "Draft order", "is_draft", "Order draft state"]
tags: [orders, statuses, auto, draft, gateway, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-08-06
source_count: 3
---

> Part of [[order-status-workflow]]. See the hub for the other aspects (taxonomy, custom statuses, transitions, side-effects, negative semantics, action gates).

# Order status — auto-transitions

## Definition

Most status changes are merchant-driven, but the platform performs **several automatic transitions** without the merchant clicking anything. The four cases are: **auto-promotion to `completed`** when paid + fulfilled, **banned-IP auto-cancel** on offline-payment orders, **gateway-driven moves** (`paid`, `failed`, `timeouted`, `chargebacked`, `refunded`) from payment-provider sync, and the implicit **draft sub-state** (`is_draft = 1`) that admin-placed orders start in.

## Scope

Covered:

- Auto-promotion to `completed` (the `order_complete` setting on [[settings-cart]]).
- Banned-IP auto-cancel.
- Gateway-driven status moves.
- The draft sub-state for admin-placed orders.

Not covered here:

- Merchant-initiated changes — see [[order-status-transitions]].
- What side-effects fire on these auto-transitions — see [[order-status-side-effects]].
- The full taxonomy of statuses involved — see [[order-status-taxonomy]].

## Contrasts

- **Auto-promotion vs manual completion** — `paid` + `fulfilled` + `order_complete = 1` auto-promotes to `completed` in the same save (one history row, one webhook, one email — and *none of those* when the promotion comes from adding a fulfilment); with `order_complete = 0` the merchant must pick `completed` manually.
- **Banned-IP auto-cancel vs merchant cancel** — auto-cancel silently sets `notify_customer = 0` and writes the ban description to the admin note; the merchant cancel goes through the normal cascade with `notify_customer` honoured.
- **Gateway-driven moves vs merchant moves** — gateway transitions originate from payment-provider sync and only emit the 5 gateway-only statuses (`failed`, `timeouted`, `chargebacked`, `disputed`, `voided`) plus `paid` / `refunded` / `disputed`; merchants cannot set them from the dropdown.
- **Draft sub-state vs status** — `is_draft = 1` is a parallel meta-flag, not one of the 11 statuses. While draft, status is typically `pending` but stock decrement and customer emails are suppressed.

## Where it applies

Every order's lifecycle runs through at least one of the four auto-transition paths:

### Auto-promotion to `completed`

The most common merchant question — *"why did my order jump from paid to completed?"*

**Trigger**: `status = paid` AND `status_fulfillment = fulfilled` AND the store setting `order_complete = 1` on [[settings-cart]] (the "Mark order as completed" toggle).

**Behaviour**: the platform rewrites `status` to `completed` **in the same save** that recorded "paid + fulfilled" — before the row hits the DB. So the same persistence call writes `completed` instead of `paid`. Downstream listeners (the per-status side-effect chain in [[order-status-side-effects]], the `order.updated` webhook, the [[orders-history]] entry) see `status = completed` directly.

The flip is silent — there is no separate status-change event for the auto-promotion. Because it happens **before** the change event fires, the merchant sees:

- **ONE** history row on [[orders-history]], and it reads `completed` — not a `paid` row followed by a `completed` row. There is no intermediate `paid` step to see.
- **ONE** `order.updated` webhook, carrying `completed`.
- **ONE** customer email, for `completed`. There is no `paid` email to suppress; it was never queued.

**The fulfilment route is completely silent.** When the order is already `paid` and the merchant simply adds the fulfilment (generates a waybill, marks it shipped), the promotion to `completed` is applied as the order is saved — with **no status-change event at all**. So: no history row, no status email, no `order.updated` from the status change. The merchant sees the pill jump from Paid to Completed with nothing in the History tab explaining it. This is the single most common *"who changed my order to Completed?"* report; the answer is the fulfilment they just created.

**To disable**: turn OFF the "Mark order as completed" setting in [[settings-cart]]. Orders stop at `paid` even after fulfillment, and the merchant must manually pick `completed` from the dropdown.

**API context**: because [[api-orders]] / [[api-order-fulfillment]] often batches status + fulfillment changes in one call, an order can land in `completed` after a single API call — still as one delivery showing `completed`, not two ([[settings-hooks]]).

### Banned-IP auto-cancel

On every new **offline-payment** order, the platform checks the customer's IP against the `OrderBannedIp` list ([[settings-banned-ip]]). If the IP is on the banned list:

- The order's `notify_customer` is set to `0` (no customer email).
- The ban description / IP is written to the order's admin note.
- The order's status is immediately transitioned to `cancelled`.

The check runs on order creation for offline payments only — **online-payment orders skip the IP-ban check** (the payment provider handles fraud upstream). There is no per-merchant fraud-score threshold mechanism in this code path; the only auto-cancel trigger from the platform is the banned-IP list match.

### Gateway-driven status moves

The 5 gateway-driven statuses are not directly settable from the merchant's dropdown (see [[order-status-transitions]] — they're filtered out of the picker). They are emitted by payment-provider sync:

| Trigger | Action |
|---------|--------|
| Payment gateway reports a successful capture | Move to `paid`. |
| Payment gateway reports a failure | Move to `failed`. |
| Payment gateway reports a timeout | Move to `timeouted`. |
| Payment provider event reports chargeback | Move to `chargebacked`. |
| Payment provider event reports refund | Move to `refunded`. |
| Payment provider event reports dispute | Move to `disputed`. |
| Payment auth voided / expired | Move to `voided`. |

These run the same [[order-status-side-effects|side-effect cascade]] as manual changes — stock, invoice / receipt numbers, discount recount, authorisation release — **but with a significant exception**. On the gateway return / webhook routes the "post" part of the cascade (webhook, customer email, history rows) is deliberately skipped for everything except a **cancellation** and a **recovery** (negative → `paid` / `authorized` / `completed`). A routine `pending → paid` from a gateway therefore leaves **no history row, no customer email and no `order.updated`** — see [[order-status-side-effects]].

Note also that once a merchant has changed the status by hand from the list pill or via JSON-API v2, the order carries a `manual` marker and the platform **stops recomputing its status from payment rows** — gateway events no longer move it. See [[order-status-transitions]].

### Draft sub-state (`is_draft`)

Orders created via [[orders-add]] (admin-placed orders) start with a meta-flag `is_draft = 1`. This is **NOT one of the 11 statuses** — it is a parallel sub-state on top of whatever `status` the order has (typically `pending`).

While draft:

- Order is invisible to the customer.
- No confirmation email fires.
- No stock is decremented (regardless of `order_status_for_quantity_decrease`).
- The status pill on [[orders-details]] shows a **"Draft"** badge instead of a status pill.
- The status dropdown shows **only `Cancelled`** as an option — the merchant cannot flip a draft to other statuses directly.

The merchant transitions out of draft by clicking **Create order** on [[orders-details]], which clears `is_draft` and runs the normal post-create pipeline (stock decrement, confirmation email, webhooks). Alternatively, picking `Cancelled` from the limited dropdown also clears the meta — the first explicit status change on a draft is what flips the order out of draft state (the metadata flag doesn't survive the first explicit status pick) (verify).

## Related

- [[order-status-workflow]] — hub.
- [[settings-cart]] — `order_complete` toggle controlling auto-promotion + `order_status_for_quantity_decrease` for the stock trigger.
- [[settings-banned-ip]] — IP-ban list driving auto-cancel.
- [[orders-add]] — admin-placed orders that start as drafts.
- [[orders-details]] — Draft badge + "Create order" button.
- [[orders-history]] — both manual and auto-transition rows appear here.
- [[order-status-transitions]] — merchant-initiated changes.
- [[order-status-side-effects]] — the cascade these auto-transitions run through.
- [[order-status-taxonomy]] — the gateway-driven statuses that get auto-emitted.
- [[api-orders]] / [[api-order-fulfillment]] — API batching that often triggers auto-promotion.

## Open Questions

None.
