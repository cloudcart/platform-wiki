---
type: concept
nav_path: "Concept → Inventory tracking → Oversell + backorders"
aliases: ["Inventory oversell", "Continue selling when sold out", "continue_selling flag", "Backorders", "Pre-orders", "Replenishable goods", "Negative inventory", "Quantity clamped to 0"]
tags: [catalog, inventory, stock, oversell, backorders, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[inventory-tracking]]. See the hub for the other aspects (variant model, decrement timing, restock, bundle stock, multi-warehouse, in-stock badge, debugging playbook).

# Inventory — oversell + backorders

## Definition

The **`continue_selling`** flag on the parent [[product|Product]] is the merchant's primary tool for accepting orders against zero or negative on-hand inventory:

- When **`continue_selling = yes`**, the storefront keeps the Add-to-cart action open at `quantity = 0`. On the order-decrement code path, the platform **clamps the resulting Variant `quantity` to 0** rather than allowing it to go negative.
- When **`continue_selling = no`** (default), the storefront blocks Add-to-cart at `quantity = 0` — the button is greyed out, the Variant shows out-of-stock.

This is the merchant's mechanism for three concrete use cases:

- **Backorders** — accept orders for goods not yet in stock; the merchant ships when the next batch arrives.
- **Pre-orders** — sell a future product (e.g., a book that releases next month) at `quantity = 0` from the start.
- **Replenishable consumables** — goods the merchant restocks frequently and doesn't want to wait for a save cycle to make available again.

## Scope

Covered:

- The `continue_selling` flag and what it does at the storefront + decrement code path.
- The clamping-at-0 rule (Variant `quantity` never goes negative).
- How to track "we owe N units" when the platform clamps.
- Inventory screen's own clamping.
- The admin order-add override.

Not covered here:

- The three master switches in general — see [[inventory-variant-model]].
- When decrement happens — see [[inventory-decrement-timing]].
- Storefront in-stock badge logic — see [[inventory-in-stock-badge]].

## Contrasts

- **`continue_selling` vs `tracking`** — `continue_selling` is the oversell flag; `tracking` is the master ignore switch. With `tracking = no`, `quantity` is ignored entirely; `continue_selling` becomes irrelevant. With `tracking = yes`, `continue_selling` decides whether the storefront accepts orders at `quantity = 0`.
- **Native clamping vs true negative inventory** — many e-commerce platforms let the Variant quantity go to `-3` when you sell 3 units after stock is gone. CloudCart clamps to `0`. This is **the most-misstated rule** about CloudCart inventory.
- **Storefront block (default) vs admin order-add override** — when `continue_selling = no`, the storefront greys out Add-to-cart at `quantity = 0`. Trying to bypass via the admin order-add flow ([[orders-add]]) also blocks unless the merchant explicitly uses the "Allow overselling" action on the cart line.

## Where it applies

`continue_selling = yes` activates these behaviours simultaneously:

- **Storefront** — Add-to-cart stays open at `quantity = 0` for every Variant of the product.
- **Order-decrement code path** — when an order moves to a decrementing status against a 0-stock Variant, the resulting `quantity` is **clamped to 0** rather than going negative.
- **Inventory screen** — the per-row "Continue selling when sold out" toggle on [[products-inventory]] mirrors the same flag.
- **In-stock badge** — the storefront treats `continue_selling = yes AND quantity = 0` as "in stock" (see [[inventory-in-stock-badge]]).
- **Back-in-stock eligibility** — the segment query marks a Variant restocked the moment `continue_selling = yes` flips — every queued [[products-missing-product]] subscriber for that Variant becomes ready-to-notify on the next campaign send.

### How the merchant tracks "owed" units when clamping is active

Because the Variant's `quantity` never goes negative, **the field cannot be used as a "net stock" indicator**. The merchant tracks how many units they owe customers by looking at **outstanding orders against the 0-stock Variant**:

1. Filter [[orders]] to orders that are `paid` AND not yet `fulfilled` (or completed, depending on the merchant's status flow).
2. Filter by the affected Variant SKU.
3. The count of matching orders × per-order quantity = the units the merchant has committed to ship from the next inbound batch.

When the new shipment arrives, the merchant edits the Variant's `quantity` to the full new batch count. The platform did NOT track "owed" units automatically — the new batch goes in at full value, and the merchant ships from it against the outstanding-orders queue manually.

**Practical takeaway**: the Variant `quantity` field is a "current sellable units" counter, not a "net stock position." Merchants doing heavy backorder workflows treat the Orders list (filtered to paid + un-fulfilled + Variant SKU) as their actual backorder queue.

### Worked example — clamping with `continue_selling = yes`

The merchant sells a popular book. Stock is `quantity = 0` but `continue_selling = yes` because a new shipment arrives next week. With `order_status_for_quantity_decrease = paid` (default):

1. Customer 1 places order for 1 unit → order goes `pending`. No stock change (`paid` setting; `pending` doesn't decrement).
2. Customer 2 places order for 1 unit → also `pending`. Same — no stock change.
3. Customer 1 pays → order goes `paid` + auto-fulfilled by merchant marking. Stock would decrement to `-1` but the platform **clamps to 0**. Storefront still shows in-stock because `continue_selling = yes`.
4. Customer 2 pays → order goes `paid`. Quantity stays at 0 (clamp again).
5. New shipment arrives (52 units). Merchant edits the Variant's `quantity` to 52.
6. Two customers are owed units (from steps 3 + 4). Merchant filters Orders to `paid + un-fulfilled` for this Variant → 2 orders. Ships those 2 from the new batch. Remaining sellable: 50.

The Variant's Change log shows the decrement events (clamped at 0) + the manual restock — see [[products-change-log]].

### Inventory screen also clamps

The Inventory screen ([[products-inventory]]) clamps **Set / Add** edits at `0` — so even directly editing the field cannot push a Variant into negative inventory. If the merchant tries to set `quantity = -5`, the platform stores `0`.

### Admin order-add override

When `continue_selling = no` AND `quantity = 0`, the storefront blocks Add-to-cart, but a merchant creating an order on behalf of the customer through [[orders-add]] (admin manual order) can override on a per-line basis using the explicit **"Allow overselling"** action on the cart line. This is the only path that bypasses the `continue_selling = no` block — useful when the merchant has units physically present but not yet entered into the system.

## Related

- [[inventory-tracking]] — hub.
- [[inventory-variant-model]] — the parent `continue_selling` switch.
- [[inventory-decrement-timing]] — when the clamp triggers (on transition into a decrementing status).
- [[inventory-restock]] — symmetric flow when overstock returns (e.g., a backorder cancellation re-credits the clamped 0).
- [[inventory-in-stock-badge]] — `continue_selling = yes` keeps the Variant showing in-stock at `quantity = 0`.
- [[inventory-debugging-playbook]] — investigating unexpected stock changes.
- [[product]] — the entity carrying the `continue_selling` flag.
- [[products-inventory]] — per-row `continue_selling` toggle + Set/Add clamping.
- [[orders-add]] — manual order with "Allow overselling" override.
- [[products-missing-product]] — `continue_selling = yes` flip marks all queued subscribers ready-to-notify.
- [[product-visibility]] — stock gating is one input to whether a product shows; oversell keeps a 0-stock product sellable + visible.

## Open Questions

None.
