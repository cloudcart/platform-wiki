---
type: feature
nav_path: "Orders → Order details → Products → Stock effects"
route_name: admin.orders.products.store
route_path: /admin/orders/action/products/:order_id
aliases: ["Order line stock effects", "Per-line decrement", "Order line restock", "Stock-locations app on order", "Tracked-snapshot rule"]
tags: [orders, products, line-items, inventory, stock, decrement, restock]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[orders-products]]. See the hub for the other aspects (add, edit, delete, line discount, fulfillment popover, side effects).

# Order products — Stock effects

## Purpose

How **each line-item action** (add / edit / delete) affects the variant's `quantity` on the catalog side. CloudCart's order-line CRUD applies stock changes **immediately on save** at the order level, but only when the line is "tracked" — and the **tracked state is a snapshot taken at line-creation time**, not the variant's current `tracking` flag. Stock-locations stores get per-zone validation against the order's `geo_zone_id` meta.

## Where to find it

Cross-cutting. The stock side-effects fire on every successful POST to:

- `admin.orders.products.store` (add — decrement)
- `admin.orders.products.update` (edit — diff)
- `admin.orders.products.delete` (delete — restore)

There is no merchant-visible "stock effects" screen — the merchant sees the side-effect on [[products-inventory]] and on the product's [[products-change-log]].

## What the merchant can do here

- **Watch stock change in real-time** on [[products-inventory]] after every line save.
- **Trace stock changes back to the originating order** via [[products-change-log]] — every line-driven adjustment records `action = order` with the order ID as the Initiator.
- **Oversell** when a variant has `continue_selling = yes` — see [[inventory-oversell]].

## Settings & fields

### The three flags that govern stock effects

| Flag | Where set | Effect on order-line CRUD |
|---|---|---|
| **Variant `tracking`** | [[products-inventory]] (per variant) | Master switch. When OFF at line-creation, NO decrement on add, NO restore on delete — regardless of the variant's current state. |
| **Variant `continue_selling`** | [[products-inventory]] (per product, applies to all variants) | When ON, oversell allowed (line saves even if requested qty > available stock). When OFF, stock validation rejects oversell with *"Not enough quantity for `<quantity>`"*. |
| **Order line `tracked` snapshot** | Set at line creation | Frozen at add-time. Governs whether the line participates in subsequent diff (edit) and restore (delete). |

### The store-wide setting that governs decrement TIMING

- **`order_status_for_quantity_decrease`** on [[settings-cart]] — `paid` (default) vs `pending`. This decides WHEN the platform decrements stock during the order's status journey. The line-CRUD routes apply stock changes on the action itself (add → decrement, edit → diff, delete → restore), but the precise decrement timing relative to status transitions is the [[inventory-decrement-timing]] story.

### Stock-locations app integration

When the `store_locations` app is installed AND the order has a `geo_zone_id` meta value, the platform sums `quantity` ONLY across shops belonging to that geo zone — so multi-warehouse stores get accurate per-warehouse stock checks. Without the app, stock is summed globally per variant. See [[apps-store-locations]].

## Business rules

### Add → decrement immediately on save

Adding a line decrements the variant's `quantity` by the requested amount immediately on save — NOT at order checkout. The line is flagged as `tracked = yes` if the variant was tracking at the moment of save.

### Edit → diff applied (only if line is `tracked`)

When the merchant edits a line's quantity:
- If the line is `tracked = yes` (the snapshot taken at add-time), the platform applies the DIFF (new qty − old qty) to the variant. Positive diff decrements further; negative diff restores.
- If the line is `tracked = no` (snapshot OFF), NO adjustment — even if the variant's current `tracking` flag is now ON.

This is important for merchants who toggle `tracking` AFTER order creation. The order-line's tracked snapshot is the source of truth, not the variant's live flag.

### Delete → restore (only if line is `tracked`)

Removing a tracked line RESTORES the variant's `quantity` by the line's amount. Untracked lines do NOT restore — no decrement happened originally. See [[inventory-restock]] for the symmetric restock catalogue.

### Stock validation only triggers when BOTH `tracking = yes` AND `continue_selling = no`

The *"Not enough quantity for `<quantity>`"* error fires ONLY when:

1. The variant's `tracking = yes`, AND
2. The variant's `continue_selling = no`, AND
3. The requested quantity exceeds available stock.

If either `tracking` is OFF or `continue_selling` is ON, the merchant CAN add over capacity. There is NO global override flag — the per-variant flags govern.

### Stock-locations: per-zone sum

When `store_locations` is active and the order has a `geo_zone_id`, available stock = sum of shop quantities WITHIN that geo zone. A variant with 5 units in Sofia and 3 in Plovdiv shows 5 to a Sofia-zone order and 3 to a Plovdiv-zone order — not 8. See [[inventory-multi-warehouse]].

### Stock-changes are recorded on the product's Change log

Every order-driven stock change writes a `variants.updated` entry on the product's [[products-change-log]] with `action = order` and the order ID as the Initiator (e.g., *"Edit from order #12345"*). This is the trail to use for "stock changed and we didn't change it" tickets — see [[inventory-debugging-playbook]].

### Stock-changes ripple to ES, storefront cache, and webhooks

Every variant `quantity` change fires the standard inventory ripple chain:
- the search re-index re-indexes the product on the search index (via `searchable-import4` queue) — see [[background-queue-inventory]].
- Storefront page-cache fragments invalidate.
- `product.updated` webhook fires per [[settings-hooks]] (chatty — receivers must be idempotent).

So even DRAFT order line edits — which skip the `order.updated` webhook (see [[orders-products-side-effects]]) — STILL fire `product.updated` because the variant moves.

### `continue_selling` clamps the Variant `quantity` to 0 on decrement

Even when oversell is allowed, the variant's `quantity` field does NOT go negative. It clamps to 0. The merchant tracks "how many we owe" via outstanding paid orders against a zero-stock variant, NOT via a negative `quantity`. See [[inventory-oversell]].

## Related

- [[orders-products]] — hub.
- [[orders-products-add]] — decrement happens on add.
- [[orders-products-edit]] — diff applied on quantity edit (only if line is `tracked`).
- [[orders-products-delete]] — restore happens on delete (only if line is `tracked`).
- [[orders-products-side-effects]] — webhook + history side-effects that pair with stock changes.
- [[inventory-tracking]] — concept hub.
- [[inventory-decrement-timing]] — when stock comes off during the order's status journey.
- [[inventory-restock]] — symmetric restock semantics on cancel / refund / void / line delete.
- [[inventory-oversell]] — `continue_selling` flag + zero-clamp rule.
- [[inventory-multi-warehouse]] — `store_locations` app + per-zone stock sums.
- [[settings-cart]] — `order_status_for_quantity_decrease` (decrement timing).
- [[apps-store-locations]] — per-zone stock app.
- [[products-inventory]] — per-variant stock screen.
- [[products-change-log]] — audit trail with `action = order` Initiator.
- [[inventory-debugging-playbook]] — investigation workflow for unexpected stock changes.
- [[background-queue-inventory]] — `searchable-import4` search-index re-index queue.
- [[settings-hooks]] — `product.updated` webhook on every stock change.

## Open questions

None.
