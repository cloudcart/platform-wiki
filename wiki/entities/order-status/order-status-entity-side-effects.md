---
type: entity
nav_path: "Entity → Order Status → Side-effects"
aliases: ["Order Status side-effects", "Status change side-effects", "Status change order of operations", "Bulk status change", "Auto-promotion"]
tags: [entity, orders, statuses, side-effects, auto-transitions]
created: 2026-06-10
updated: 2026-08-06
source_count: 3
---

> Part of [[order-status]]. See the hub for the other aspects (canonical values, relationships, custom statuses, API access, edge cases).

# Order Status — Side-effects on transition

## Identity

When the merchant changes an Order Status (single or bulk), the platform fires a **deterministic cascade** of side-effects in a fixed order. This aspect documents that order, the auto-promotion to `completed`, hard gates that block transitions, and bulk-operation semantics.

## Aliases

- **Status change cascade** / **firing order** — the side-effect pipeline.
- **Auto-promotion** / **auto-completion** — the `paid + fulfilled + order_complete = 1` rule.
- **Hard gates** — transitions the platform rejects with an error message.
- **Bulk status change** — the [[orders]] list action.

## Key Attributes

### Side-effects of a status change (in order)

When the merchant changes a status (single or bulk), the platform fires in this order:

1. **Stock decrement / restore.** Decided by the order's fulfillment state plus the decrement setting **snapshotted onto the order at placement** (`order_status_for_quantity_decrease`; new stores are seeded with `pending`). Decrement applies when the order is `fulfilled`, or when its setting is `paid` and its status is `paid` / `authorized` / `completed`, or when its setting is `pending` and its status is any of those plus `pending`. Restore never happens while the order sits in `paid` / `authorized` / `completed`. See [[inventory-decrement-timing]] + [[inventory-restock]].
2. **Invoice number + receipt number issued** — on every status change, provided an invoicing provider is active on [[settings-invoicing]].
3. **Customer lifetime-spend recomputation queued.**
4. **The "post" block — webhook, then customer email, then history rows.** `order.updated` goes to every endpoint subscribed in [[settings-hooks]] carrying the stable status CODE (see [[order-status-entity-api-access]]); then the single status-change customer email is queued when the order's `notify_customer` flag, the template's own active flag and the store-wide `customer_email_notifications` all allow it (the store's own copy of that notification rides inside this same step); then two [[orders-history]] rows — a typed action row (`order_paid`, `order_cancelled`, `order_custom_status`, …) and a previous → new row. **This whole block is skipped on the payment-gateway return / webhook paths**, except for cancellations and for a negative → positive recovery.
5. **Discount uses recounted** — inline plus a resync queued ~10 s later.
6. **Payment authorisation released at the gateway** — negative statuses only.
7. **System return auto-recorded** — `cancelled` / `refunded` only, and only on a committed sale; the reversal lock follows it. See [[order-status-entity-edge-cases]].

Auto-promotion to `completed` is not a step in this list — it is applied to the order **before** the change event fires, so the whole cascade above simply runs once with `completed` as the new status.

### Auto-promotion to `completed` — the most common merchant question

Setup: [[settings-cart]] → "Mark order as completed" toggle is ON (the `order_complete` setting). The merchant marks an order `paid` AND marks its fulfillment `fulfilled`. **Result**: the platform auto-promotes the order to `completed` in the same save.

To disable: turn OFF the "Mark order as completed" setting. Orders stop at `paid` even after fulfillment.

### Auto-completion writes ONE history row, not two

The promotion is applied **before** the change event fires, so there is no intermediate `paid` state for anything to observe. The merchant sees **one** history row, reading `completed`; subscribers get **one** `order.updated`, carrying `completed`; the customer gets **one** email.

**And when the promotion comes from adding a fulfilment to an already-`paid` order, it is completely silent** — the status is rewritten as the order saves, with no status-change event at all. No history row, no email, no webhook from the status side. This is the usual answer to *"who changed my order to Completed and why is there nothing in the History tab?"*

### Auto-transitions the platform performs

| Trigger | Action |
|---------|--------|
| `status = paid` AND `status_fulfillment = fulfilled` AND store setting `order_complete = 1` | Auto-promote to `completed` in the same save. Fires another history row and another webhook. |
| Order's source IP / email matches a [[settings-banned-ip]] rule | Auto-cancel to `cancelled`. The `notify_customer` flag is set OFF automatically so the customer is not emailed. |
| Payment gateway reports successful capture | Move to `paid`. |
| Payment gateway reports failure | Move to `failed`. |
| Payment gateway reports timeout | Move to `timeouted`. |
| Payment provider event reports chargeback / refund | Move to `chargebacked` / `refunded`. |

### Hard gates the platform enforces

| Rule | Effect |
|------|--------|
| **Archived order's status cannot change.** | Error: *"Статусът на архивирана поръчка не може да бъде променен. Първо разархивирай."* / *"The status of an archived order cannot be changed. Unarchive first."* The merchant must unarchive via [[orders-archive]] first. |
| **Some shipping integrations lock fulfillment status.** | Error: *"Моля, генерирайте товарителница за тази поръчка. Смяната на статуса от тук, не е възможен."* — the merchant must trigger the courier's waybill flow ([[orders-shipping-waybill]]) instead of editing fulfillment directly. |
| **`completed` needs `paid` OR `fulfilled`.** | Refused only when the order is neither. Error: *"Only paid and/or fulfilled orders can be marked as Completed"*. A `paid` but unshipped order completes fine. |
| **`cancelled` refused from `paid` / `completed`.** | Error: *"Only open orders can be canceled."* Refund the order instead. |
| **Reversal lock.** | A cancelled / refunded order carrying a return record or an issued credit number can only toggle between `cancelled` and `refunded`. Error: *"The order is locked after a cancellation/refund — its status can no longer be changed."* |
| **Under-authorised order: no status change at all.** | When the payment authorisation is smaller than the order total, every status change is refused with *"The order amount is `<total>` and cannot exceed the authorized payment `<amount>`."* The check runs BEFORE the target status is looked at, so such an order cannot even be cancelled from the pill. |
| **Draft orders can ONLY transition to Cancelled** via the dropdown — other statuses require the merchant to "Create order" first. | |

### Bulk status change is currently `completed` only

The [[orders]] list bulk action only exposes **Mark as completed** as a bulk status change. For other bulk transitions (bulk-cancel, bulk-refund, bulk-mark-paid), the merchant must per-order each one via [[orders-details]]. The endpoint behind the bulk action validates the requested status against the same merchant-pickable set the dropdown offers — the 5 gateway-driven statuses are rejected as invalid. Bulk operations process inside a DB transaction with fail-fast behavior: if ANY order fails, the whole transaction aborts and NONE are updated.

### Bulk-completing N orders fires N customer emails

A common gotcha: bulk-completing 100 orders may send 100 emails. There is no per-status notification toggle to switch off — the mitigations are to flip `notify_customer = no` on the selected orders first, or to deactivate the status-change email template in [[marketing-omnichannel-mails-list]] for the duration.

### Customer notification can be suppressed per-order

Each order has a `notify_customer` flag (default ON), toggled via [[orders-notify-customer]]. When OFF, all future automated emails on this order are suppressed (across all status types). Useful for B2B / wholesale customers or test orders.

### Stock-decrement timing edge case

`order_status_for_quantity_decrease` on [[settings-cart]] picks which statuses count as "stock is out" (new stores are seeded with `pending`). Its value is **snapshotted onto each order when the order is placed**, so changing the store setting never affects orders that already exist — not just "no retroactive adjustment", but no effect at all on their future transitions either. Only orders placed after the change follow the new rule.

### The `manual` marker freezes gateway-driven status updates

Changing status from the [[orders]] list status pill, or through JSON-API v2, marks the order as manually managed. The platform then **stops recomputing its status from payment rows** — permanently. A gateway webhook arriving later still updates the payment but no longer moves the order.

## Where it appears

- [[orders-status-change]] — the per-order + bulk status-change flow.
- [[orders-details]] — the status pill fires the cascade on each change.
- [[orders-history]] — captures the two rows written in the post block.
- [[settings-cart]] — `order_complete` (auto-promotion) + `order_status_for_quantity_decrease` (stock).
- [[settings-statuses]] — status taxonomy (names only; no notification settings).
- [[marketing-omnichannel-mails-list]] — the status-change email template + the store-wide kill switch.
- [[settings-invoicing]] — invoicing provider gating the invoice / receipt numbers.
- [[settings-hooks]] — webhook subscriptions.
- [[settings-banned-ip]] — auto-cancel rule.

## Related

- [[order-status]] — hub.
- [[order-status-entity-canonical-values]] — values the cascade transitions between.
- [[order-status-entity-edge-cases]] — additional negative-status side-effects (fulfillment reset, auth release).
- [[order-status-side-effects]] — sibling concept page in the workflow cluster.
- [[order-status-auto-transitions]] — concept page on auto-transitions.
- [[order-processing-pipeline]] — the full pipeline this cascade is embedded in.

## Open Questions

None.
