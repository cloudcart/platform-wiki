---
type: feature
nav_path: "Orders → List → Locking & save side-effects"
route_name: admin.orders
route_path: /admin/orders/list
aliases: ["Order locking", "Lock orders setting", "Moderator collision protection", "Auto-promotion to completed", "order_complete setting", "Save side effects", "Заключване на поръчки", "Лок при достъп до поръчка"]
tags: [orders, list, locking, lock-orders, auto-complete, save-side-effects, smarty]
plan_gates: []
created: 2026-06-10
updated: 2026-08-06
source_count: 3
---

> Part of [[orders]]. See the hub for the other aspects (columns, filters, bulk actions, status taxonomy, default visibility, export).

# Orders list — locking and save side-effects

## Purpose

Two cross-cutting behaviours that affect the list (but are easier to understand together): the **order-lock** moderator-collision protection (preventing two moderators from editing the same order at once) and the **auto-promotion-to-completed** silent side-effect on every save. The lock lives on **Settings → General** and the auto-promotion on **Settings → Cart**; both apply to every interaction that opens or saves an order — including bulk actions on the list.

## Where to find it

They live on two different settings screens:

- **Settings → General** → *Locking orders* box ([[settings-general-operational-toggles]]): **Lock orders** (`lock_orders`, default `yes`) and **Lock time** (`lock_orders_time`, default `7` minutes — the field only appears while the switch is ON).
- **Settings → Cart** ([[settings-cart-limits-and-decrement]]): `order_complete`, default ON — the auto-promotion toggle.

Both behaviours are silent — the merchant doesn't see UI for them on the Orders list, but they shape what happens when the merchant opens an order from the list and when bulk actions run.

## What the merchant can do here

### Toggle the lock

The store owner enables or disables **Lock orders** (`lock_orders`) on **Settings → General** ([[settings-general-operational-toggles]]). When ON (default), opening a single order from the list writes a lock on that order; a second moderator opening the same order within the lock window gets an access-denied screen.

### Tune the lock window

The owner adjusts **Lock time** (`lock_orders_time`) on **Settings → General** — value in minutes, default `7`. Longer values reduce collision risk but increase the wait if a moderator opened an order and forgot it; shorter values let moderators take over more quickly but increase the risk of two-moderators-editing collisions.

### Toggle auto-complete

The owner toggles `order_complete` on [[settings-cart]] — default ON. When ON, every save of an order silently rewrites `status = completed` if the order is `paid` AND `status_fulfillment = fulfilled`.

## Settings & fields

| Setting | On | Location | Default |
|---|---|---|---|
| `lock_orders` | Order-lock collision protection | **Settings → General** ([[settings-general-operational-toggles]]) | `yes` |
| `lock_orders_time` | Lock window duration (minutes) | **Settings → General** ([[settings-general-operational-toggles]]) | `7` |
| `order_complete` | Auto-promote to `completed` on save | [[settings-cart]] | ON |

## Business rules

### Order locking — silent moderator collision protection

When `lock_orders = yes` AND the viewing admin is NOT the store owner, opening [[orders-details]] writes a lock onto the order: `{moderator_id, date_locking, lockFrom}` stored in order meta. If a SECOND moderator opens the same order within the next `lock_orders_time` minutes (default `7`), they get an *"Order is opened from other"* access-denied screen and CANNOT view the order.

Key implications:

- The owner role **bypasses the lock entirely** — owner can always open any order.
- The lock is silently **auto-released when its window expires** — there's no explicit unlock action in the UI.
- The lock applies to **single-order opening**, not to bulk operations on the list. Bulk actions ([[orders-list-bulk-actions]]) release any database row locks the platform holds before iterating and do not enforce the order-lock check per row.
- A moderator who navigates AWAY from the order page does NOT release the lock — the timer continues until expiry.

### Auto-promotion to `completed` (silent side-effect on every save)

Every time an order is saved AND `order_complete` is ON (default), the platform silently rewrites `status = completed` if the order is `paid` AND `status_fulfillment = fulfilled`. This applies to ANY save, not just status changes — so an admin who edits a note on a paid+fulfilled order can inadvertently promote it to completed, firing the "Completed" customer notification email.

Interactions with the list:

- **Bulk Mark as completed** is the explicit path to `completed`, but auto-promotion can promote an order BEFORE the merchant tries bulk-completing it.
- **Any per-order save** from [[orders-details]] (edit note, address change, line edit) can trigger auto-promotion if the order is already paid + fulfilled.
- **JSON-API v2 PATCHes** (see [[api-orders]] + [[json-api-v2]]) run through the SAME save pipeline — so auto-promotion fires on API edits too.

To suppress auto-promotion on a specific save: the merchant first unsets `notify_customer` on the order (so the silent promotion doesn't email the customer) — but the promotion itself still happens. To stop it entirely the owner turns off `order_complete` on [[settings-cart]].

### Side effects of save — the chain

Every order save (whether from the list's bulk path, the detail page, or the API) fires the platform's full order-event chain. See [[order-processing-pipeline]] for the canonical catalogue. Key high-impact effects:

- **Stock recompute** on canonical-status transitions — see [[inventory-decrement-timing]] and [[inventory-restock]].
- **Invoice / receipt number generation** if configured — see [[settings-invoicing]].
- **Customer income totals recompute** (async).
- **Discount usage counters** increment / decrement to match the order's discount usage.
- **Payment-authorisation auto-cancel** on transition INTO a negative status — see [[orders-payment-capture]].
- **Customer email** — fires when transitioning into a status with the per-status email toggle ON (see [[settings-statuses]]) AND the per-order `notify_customer` flag is ON (see [[orders-notify-customer]]).
- **`order.updated` webhook** — see [[settings-hooks]].
- **Audit log row** — see [[orders-history]].

### "Stock changed and we didn't change it" — explained by the chain

When the merchant reports unexpected stock movement on an order, the root cause is almost always one of: the silent auto-promotion firing a status change, the bulk-status path running per-order, or a JSON-API v2 PATCH triggering the same chain. The product's Change log records the Initiator — see [[inventory-debugging-playbook]] for the 6-step investigation.

### Permission boundary

Lock and auto-promotion behaviours are platform-wide — they apply equally to moderators and the store owner (the owner only bypasses the LOCK check; auto-promotion still fires on the owner's saves). Lock interplay with the **orders** permission section is straightforward: a moderator without orders permission can't reach the detail page at all, so the lock is irrelevant.

## Related

- [[orders]] — hub.
- [[orders-list-bulk-actions]] — bulk actions release database row locks but don't enforce the order-lock.
- [[orders-list-status-taxonomy]] — `completed` is one of the 11 canonical statuses.
- [[orders-details]] — where the lock is written on open.
- [[orders-details-known-issues]] — the lock + auto-promotion appear in the by-design caveats catalogue.
- [[orders-history]] — audit log row written for every save.
- [[orders-notify-customer]] — per-order customer-email toggle that gates the auto-promotion email.
- [[settings-general-operational-toggles]] — `lock_orders` + `lock_orders_time` (**Settings → General**).
- [[settings-cart]] — `order_complete` setting.
- [[settings-statuses]] — per-status email toggle.
- [[settings-hooks]] — `order.updated` webhook.
- [[settings-invoicing]] — invoice / receipt numbering on save.
- [[inventory-debugging-playbook]] — "stock changed unexpectedly" diagnostic.
- [[inventory-decrement-timing]] — stock decrement timing on save.
- [[inventory-restock]] — stock restock on negative-status transition.
- [[orders-payment-capture]] — payment auth auto-cancel on negative-status transition.
- [[api-orders]] — JSON-API v2 PATCH fires the same chain.
- [[json-api-v2]] — API overview.
- [[order-processing-pipeline]] — the full chain of save side-effects.

## Open questions

None.
