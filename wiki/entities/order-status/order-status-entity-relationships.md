---
type: entity
nav_path: "Entity → Order Status → Relationships"
aliases: ["Order Status relationships", "Status independence", "Status vs payment vs shipping", "What Order Status drives"]
tags: [entity, orders, statuses, relationships]
created: 2026-06-10
updated: 2026-08-06
source_count: 3
---

> Part of [[order-status]]. See the hub for the other aspects (canonical values, custom statuses, side-effects, API access, edge cases).

# Order Status — Relationships

## Identity

Order Status is **independent of** [[payment-status]] (the money) and [[shipping-status]] (the package). Together, the three answer three different questions — and they can disagree. This aspect catalogues what the Order Status belongs to, what it cooperates with, and what it drives downstream.

## Aliases

- **Status independence** — the rule that an order can be `paid` while its payment is `refunded`, etc.
- **Status side-effects** — what flips automatically when status changes (see [[order-status-entity-side-effects]] for the firing order).

## Key Attributes

### What an Order Status belongs to / cooperates with

An Order Status:

- **Belongs to** exactly one [[order|Order]] at a time. Every order has one Order Status value (never null — defaults to `pending` at creation, or `authorized` for pre-auth providers).
- **References** [[settings-statuses]] for merchant-facing label translations. Custom statuses are also defined here — see [[order-status-entity-custom-statuses]]. Notification settings do NOT live there — one status-change email template covers every status, managed in [[marketing-omnichannel-mails-list]].
- **Cooperates with** [[payment-status]] AND [[shipping-status]] in the order-completion rule: the order auto-promotes to `completed` when ALL of {`status = paid`, `status_fulfillment = fulfilled`, store setting `order_complete = 1`} hold simultaneously.

### What an Order Status drives downstream

- **[[notification-delivery|Customer notification dispatch]]** — if the destination status has Customer notification turned ON in [[settings-statuses]] AND the order's `notify_customer` flag is ON (default), the platform sends the configured email to the customer.
- **`order.updated` webhook fan-out** to [[settings-hooks]] subscribers on every status change. The webhook payload carries the unchanged status **CODE** (`paid`, `cancelled`), NOT the merchant's renamed label — so external integrations stay stable across renames.
- **[[orders-history|History-log entry]]** — one row per change, recording the prior status, the new status, the staff member, the timestamp.
- **Stock decrement / restore** — when the order's status matches `order_status_for_quantity_decrease` (default `paid` per [[settings-cart]]), stock is decremented; transitioning OUT restores it. See [[inventory-decrement-timing]] + [[inventory-restock]].
- **[[discount|Discount]] uses-counter** — when the order's status matches one of the `discounts_used_statuses` (default `paid`, `completed`, `fulfilled` per [[settings-cart]]), the discount's `uses` counter increments and the per-customer cap counter advances. Transitioning OUT decrements them.
- **Admin notification** — when the merchant subscribes to `order_status_change` / `order_payment_status_change` in [[settings-admin-notifications]], staff get bell-icon alerts on transitions.
- **Action availability gates** — the action buttons on [[orders-details]] (Edit, Refund, Cancel, Mark as Completed, Issue Invoice, Issue Credit Note) check the current status.

### Independence from payment-status and shipping-status

The **single most important rule**: Order Status is independent of [[payment-status]] and [[shipping-status]]. An order can be:

- `status = paid`, `status_fulfillment = not_fulfilled` (paid but not yet packed — typical post-checkout state for many minutes to hours).
- `status = paid`, `status_fulfillment = fulfilled` (paid and packed — ready for pickup or auto-promotes to completed).
- `status = completed`, payment-status = `refunded`, `status_fulfillment = returned` (the whole order has been reversed but the merchant marked it Complete first).

The merchant cannot infer one status from another. Each is set independently.

### Action gates per status — what the merchant can do at each step

| Action | Status required |
|--------|-----------------|
| **Edit line items / customer / address** | `pending`, `paid`, `authorized` |
| **Mark as Paid** | Any non-paid status (typically `pending` / `authorized`); subject to payment-gateway readiness |
| **Capture authorization** | `authorized` |
| **Refund** | `paid` (or any status where a payment record is in `completed` state — refund button is actually gated by [[payment-status]], not Order Status) |
| **Mark as Completed** | `paid` **OR** `status_fulfillment = fulfilled` — either is enough; only an order that is neither is refused |
| **Cancel order** | Any status except `paid` / `completed`; not gated by stock |
| **Issue invoice** | Any status with payment captured (varies by store invoicing settings) |
| **Issue credit note** | `cancelled` OR `refunded` AND `invoice_number` is populated (per [[orders-credit]]) |
| **Issue receipt** | Any status with payment captured |
| **Archive** | `completed` or `cancelled` (per [[orders-archive]]) |
| **Bulk status change (from list)** | Currently UI only exposes "Mark as completed"; per-order changes for all other statuses |

### What an Order Status is NOT

- **Not [[payment-status]]** — the canonical state of an individual payment record (**14** values: `authorized`, `initiated`, `requested`, `pending`, `held`, `completed`, `failed`, `refunded`, `voided`, `cancelled`, `timeouted`, `chargebacked`, `disputed`). The Order Status is the workflow; the Payment Status is the money.
- **Not [[shipping-status]]** — the order's fulfillment state (`not_fulfilled` / `fulfilled` plus typically `shipped`, `delivered`, `returned` for integrated stores).
- **Not a custom status the merchant adds** — custom statuses are extra labels, not new canonical values. See [[order-status-entity-custom-statuses]].
- **Not an archive flag** — `date_archived` is a separate field; archived orders are status-locked (status cannot change until unarchive).

## Where it appears

- [[order]] — the entity carrying the `status` field.
- [[orders-details]] — action buttons gated by status.
- [[orders-history]] — every transition recorded as a history row.
- [[orders-archive]] — archived orders are status-locked.
- [[settings-cart]] — `order_status_for_quantity_decrease` + `order_complete` reference the status.
- [[settings-admin-notifications]] — `order_status_change` / `order_payment_status_change` admin alerts.
- [[settings-hooks]] — `order.updated` webhook fires on every change.
- [[payment-status]] / [[shipping-status]] — independent sibling enums.

## Related

- [[order-status]] — hub.
- [[order-status-entity-side-effects]] — the firing order of side-effects on a transition.
- [[order-status-entity-canonical-values]] — the 11 values themselves.
- [[order-status-workflow]] — concept page on the 3-status interaction (Order × Payment × Shipping).
- [[notification-delivery]] — how a transition becomes a customer email.

## Open Questions

None.
