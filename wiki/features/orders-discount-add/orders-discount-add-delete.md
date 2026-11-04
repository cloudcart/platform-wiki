---
type: feature
nav_path: "Orders → Order details → Discount → Delete"
route_name: admin.orders.discount.delete
route_path: /admin/orders/action/discount/:order_id/delete
aliases: ["Remove order discount", "Delete order discount", "Delete modifications", "Remove discount confirmation", "Restore discount usage count"]
tags: [orders, discount, delete]
plan_gates: []
created: 2026-06-10
updated: 2026-11-04
source_count: 3
---

> Part of [[orders-discount-add]]. See the hub for the other aspects (form fields, existing-discount eligibility, manual discounts, recalculation, API).

# Order-level discount — delete (remove discount / modifications)

## Purpose

The flow for **removing an order-level discount** — and the sister action that removes the order's order-level **modifications**. Removing an existing discount also restores its consumed usage on the master [[marketing-discounts]] record.

## Where to find it

[[orders-details]] → **Discount action row** → **Remove Discount** button (shown when an order-level discount IS applied).

Routes:
- `admin.orders.discount.delete` (GET) — remove the order-level discount.
- `admin.orders.modifications.delete` (GET) — remove the order's order-level modifications.

## What the merchant can do here

- **Remove the order-level discount** — confirm the browser dialog; the discount is deleted and totals recalculate.
- **Remove order-level modifications** — a separate action, shown when the order has any.

## Settings & fields

### Delete-discount confirmation

No modal — the Remove button uses a `data-confirm` browser dialog: *"Remove order discount"* (`order.confirm.remove_order_discount`). Confirmed = GET to `admin.orders.discount.delete`, which removes ALL non-line-targeted discount records on the order (all where `target_product_id IS NULL`) in one transaction.

### Delete-modifications is a SEPARATE flow

The `delete-modifications` route removes ALL order-level modifications (those with no associated order product), such as a cart rule's amount off the whole order. Discounts do not create modifications, so this action is independent of removing a discount.

## Business rules

### Deletion restores usage count (existing discounts only)

When the merchant removes an EXISTING discount, the platform restores the consumed usage on the discount's master record — freeing that "use" for a future customer. For **manual** discounts there is no master record to restore (see [[orders-discount-add-manual]]).

Note the usage counter is a **recount**, not a simple decrement — deleting a discount from a used-status order recounts immediately and lowers the counter. Full mechanics on [[orders-discount-add-recalculation]].

### Archived orders blocked

The `delete` and `delete-modifications` routes both reject archived orders with *"Cannot perform this operation on archived order"*. The merchant must unarchive via [[orders-archive]] first.

### Swap requires delete-then-add

Because the platform enforces one order-level discount at a time ([[orders-discount-add]]), swapping discounts means deleting the current one here, then re-adding via [[orders-discount-add-form]].

### Delete triggers the recalculation cascade + audit

Removing a discount recalculates totals, tax and shipping, fires `order.updated`, and writes a history entry with the action string `order_discount_remove`. Removing order-level modifications recalculates totals and fires `order.updated` but writes no history entry. See [[orders-discount-add-recalculation]] and [[orders-history]].

## Related

- [[orders-discount-add]] — hub.
- [[orders-discount-add-recalculation]] — the cascade + usage-counter recount that run on delete.
- [[orders-discount-add-manual]] — why manual discounts have no usage to restore.
- [[marketing-discounts]] — the master record whose usage is restored.
- [[orders-archive]] — archived orders block delete.
- [[orders-history]] — `order_discount_remove` history entry.
- [[discount]] — entity page.

## Open questions

None.
