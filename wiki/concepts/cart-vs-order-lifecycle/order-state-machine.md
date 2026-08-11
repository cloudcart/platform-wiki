---
type: concept
nav_path: "Concept → Cart vs Order lifecycle → Order state machine"
aliases: ["Order state machine", "Order lifecycle states", "Order statuses", "11 canonical statuses", "Status-gated mutability", "Order draft", "Draft order", "Lock on edit", "Жизнен цикъл на поръчка", "Статуси на поръчка"]
tags: [cart, order, lifecycle, state-machine, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-08-06
source_count: 3
---

> Part of [[cart-vs-order-lifecycle]]. See the hub for the other aspects (cart state machine, handoff, abandonment, restore).

# Order state machine

## Definition

An **[[order|Order]]** is the finalised record of a placed sale, created when the customer clicks **Place order** at checkout (see [[cart-to-order-handoff]] for the snapshot mechanics) and kept in the merchant's [[orders]] list. Its `status` is one of **11 hard-coded canonical states**; status drives mutability, accounting-document eligibility, discount-usage counting (see [[discount-stacking]]), stock decrement / re-credit (see [[inventory-tracking]]), and customer notification emails. A separate `status_fulfillment` field tracks courier dispatch independently of payment, and an `is_draft` metadata flag marks admin-created orders that bypass post-creation side-effects until finalised.

Mutability is **status-gated** — most edits (line items, addresses) are allowed only while `status` is `pending`, `paid`, or `authorized`; cancelled / refunded / completed orders have limited editability. Custom statuses defined on [[settings-statuses]] are sub-labels on the canonical 11 — the gates always check the underlying canonical status. And once a cancelled / refunded order carries a return record or an issued credit number, its status is **locked** and only toggles between `cancelled` and `refunded` — see [[order-status-negative-semantics]].

## Scope

Covered:

- The 11 canonical order statuses (positive flow + negative branch).
- The `status_fulfillment` dimension and the `is_draft` admin meta-flag.
- Status-gated mutability table.
- Custom statuses + `order-<slug>` keys; webhook payload stability across rename.
- Lock-on-edit (7-min `lock_orders_time`); store-owner bypass.
- The reversal lock on a committed cancellation / refund.
- Per-order `notify_customer` suppression toggle.
- Hard-delete (no soft-deletes); `order.deleted` webhook before cascade.
- Order-side webhooks (`order.created`, `order.updated`, `order.deleted`).

Not covered here: the Place-order snapshot + event fan-out ([[cart-to-order-handoff]]); cart-side states ([[cart-state-machine]]); allowed transitions + per-transition events ([[order-status-workflow]]); end-to-end side-effects ([[order-processing-pipeline]]); stock decrement / re-credit ([[inventory-tracking]]).

## Contrasts

- **Order draft vs Order pending**: a Draft order (admin-created via [[orders-add]] with `is_draft = 1`) is invisible to the customer, fires no emails, and doesn't decrement stock. A Pending order (the storefront default) is fully visible and triggers all post-creation events.
- **Order status vs fulfillment status**: `status` tracks payment / lifecycle (`pending` → `paid` → `completed`); `status_fulfillment` tracks courier dispatch (`not_fulfilled` → `fulfilled`). The two are independent — an order can be `paid` + `not_fulfilled` (paid but not shipped) or `pending` + `fulfilled` (rare; shipped before paid).
- **Order address vs Customer profile address**: editing the order's address ([[orders-address-edit]]) is a SNAPSHOT edit — it does NOT propagate back to the saved profile, and updating the profile address doesn't retroactively change historical orders.
- **Canonical status vs custom status**: custom statuses defined via [[settings-statuses]] are sub-labels on the canonical 11; gates check the canonical underneath (slug + webhook details below).
- **Order soft-delete vs archive**: the order has no soft-delete / `deleted_at` — deletion is a hard cascade. The default cleanup pattern is archive (`date_archived`), fully reversible via [[orders-archive]].

## Where it applies

**The 11 canonical states (+ `is_draft` meta-flag).**

Positive flow:
- `authorized` — pre-auth on the card (funds reserved, not captured).
- `pending` — default for newly-created orders; awaiting payment.
- `paid` — payment captured.
- `completed` — fulfillment complete + paid + the `order_complete` setting is ON; auto-set or manually marked.

Negative branch (excluded from revenue analytics, discount usage counters, and most workflow gates):
- `voided` — pre-auth cancelled before capture.
- `timeouted` — payment provider timed out.
- `cancelled` — merchant or auto-cancel cancelled it.
- `failed` — payment failed at the gateway.
- `refunded` — money returned.
- `chargebacked` — bank chargeback.
- `disputed` — pre-chargeback dispute.

Fulfillment (independent of order status):
- `not_fulfilled` — default; not yet dispatched.
- `fulfilled` — courier confirmed pickup / delivery.

Draft sub-state (admin-only): `is_draft = 1` is a metadata flag on orders created via [[orders-add]]. While drafted, the order is invisible to the customer and fires no confirmation emails or stock decrement. The merchant clicks "Create order" on [[orders-details]] to finalise — the flag clears and the post-creation pipeline runs.

See [[order-status-workflow]] for transitions; [[order]] for the full attribute table.

**Status-gated mutability.** Most order edits are gated by `status`:

| Action | Allowed status |
|--------|----------------|
| Edit line items (add / remove / change quantities) | `pending`, `paid`, `authorized` |
| Edit shipping / billing address | `pending`, `paid`, `authorized` (limited even then) |
| Cancel order | Any status except `paid` / `completed`; not gated by stock |
| Mark as paid manually | `pending` |
| Capture pre-auth | `authorized` |
| Refund | `paid`, `completed` (gated by the provider's refund API) |
| Mark as completed | `paid` **or** `status_fulfillment = fulfilled` — either is enough |
| Issue invoice | Any except `cancelled` / `failed` / `voided` |
| Issue credit note | `cancelled`, `refunded` + invoice exists |
| Archive | Any |
| Delete | Any (one-at-a-time from [[orders-details]]) |

The gates above check the underlying canonical status, not the merchant's custom sub-labels.

**Custom statuses use the slug `order-<slug>`.** Statuses created via [[settings-statuses]] are stored as keys `order-<slugified-name>`; the slugifier appends `-1`, `-2`, … on collision. Typing "Paid" produces `order-paid`, distinct from the built-in `paid` — the dropdown shows the merchant-facing label, and webhook payloads carry the stored key, so renaming the display name does NOT change the integration payload.

**Order lock-on-edit — 7-minute soft TTL.** When an admin opens an order for edit on [[orders-details]], the lock records that admin's username. Others opening it within **7 minutes** (the `lock_orders_time` setting, default 7) see *"Order is opened from `<user>`"*. The lock auto-expires after 7 minutes of inactivity. Store owners bypass it. Reads are not blocked — only saves fail.

**Per-order notification suppression.** Each order has a `notify_customer` flag. When ON (default), the customer is emailed on every status change — using the single status-change template shared by all statuses, subject also to that template's own active flag and the store-wide `customer_email_notifications` switch. There is no per-status notification toggle. When OFF, all future automated emails on this order are suppressed — useful for opt-out customers and fraud cases. Toggling the flag sends nothing on its own; to re-fire an email, re-apply the status. The merchant flips it in [[orders-notify-customer]]; there is no storefront opt-back-in (the account-wide marketing-consent flag is a separate switch on the [[customer]] record).

**Order soft-delete does NOT exist.** There is no `deleted_at`; deletion is a **hard delete** that cascades to all child records (line items, payments, discounts, fulfillment, history, meta, taxes, totals). The `order.deleted` webhook fires BEFORE the cascade, so the integration receives the final state. The default cleanup pattern is **archive** (`date_archived`), fully reversible via [[orders-archive]].

**Order-side webhook events.** Fired via [[settings-hooks]]:

| Event | When |
|-------|------|
| `order.created` | A new order is persisted (post-cart-submission or post-draft-confirmation). |
| `order.updated` | The order is edited — status, address, payment confirmation, or line items. |
| `order.deleted` | The order is permanently deleted (NOT fired on archive). |

For cart-side events (`cart.created`, `cart.updated`) see [[cart-state-machine]]. Draft orders bypass `order.created` until the merchant clicks **Create order** — see [[cart-to-order-handoff]] for the event sequence.

## Related

- [[cart-vs-order-lifecycle]] — hub.
- [[order]] — Order entity (full attribute table).
- [[order-status-workflow]] — allowed transitions + per-transition events.
- [[order-status-negative-semantics]] — the reversal lock on a committed cancellation / refund.
- [[order-processing-pipeline]] — end-to-end side-effects per lifecycle event.
- [[orders]] — placed-orders list.
- [[orders-details]] — per-order edit hub.
- [[orders-status-change]] — manual status transitions.
- [[orders-history]] — per-order audit log.
- [[orders-add]] — manual order creation (draft orders).
- [[orders-archive]] — archive / unarchive.
- [[orders-notify-customer]] — per-order email suppression toggle.
- [[orders-address-edit]] — address snapshot edits.
- [[orders-invoice]] / [[orders-credit]] / [[orders-receipt]] — accounting documents.
- [[orders-payment-mark-paid]] / [[orders-payment-capture]] / [[orders-payment-refund]] — payment actions.
- [[settings-statuses]] — status taxonomy + customer-notification + counted-statuses.
- [[settings-hooks]] — `order.*` webhook subscriptions.
- [[inventory-tracking]] — stock decrement / re-credit on transitions.
- [[discount-stacking]] — discount usage counting on counted-status orders.
- [[multi-currency]] — currency freeze on the order.
- [[multi-language]] — locale freeze on the order.

## Open Questions

None.
