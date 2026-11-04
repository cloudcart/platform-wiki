---
type: feature
nav_path: "Orders → Order details → Discount → Recalculation & side effects"
route_name: admin.orders.discount.add
route_path: /admin/orders/action/discount/:order_id/add
aliases: ["Order discount recalculation", "Discount side effects", "Discount total recalculation", "Discount uses counter recount", "order.updated on discount", "overwrite_product_price"]
tags: [orders, discount, recalculation, side-effects, webhooks]
plan_gates: []
created: 2026-06-10
updated: 2026-11-04
source_count: 4
---

> Part of [[orders-discount-add]]. See the hub for the other aspects (form fields, existing-discount eligibility, manual discounts, delete, API).

# Order-level discount — recalculation & side effects

## Purpose

What happens **after** an order-level discount is added or removed: the totals recalculation cascade, the side effects on the discount and order records, the `order.updated` webhook, the history / audit entries, and the usage-counter recount.

## Where to find it

These effects are not a screen — they run server-side on save / delete from the Add Discount flow ([[orders-discount-add-form]], [[orders-discount-add-delete]]). The merchant observes the results in [[orders-details]] (new totals), [[orders-history]] (audit entries), and any webhook receiver.

## What the merchant can do here

Nothing directly — this aspect documents the automatic consequences the merchant should expect after applying or removing a discount. The merchant relies on these to know the totals are correct, the audit trail captured who acted, and integrations were notified.

## Settings & fields

### Recalculation cascade — product re-pricing then totals

Inside one DB transaction, adding runs both steps below and removing runs only the totals step:

1. **Product re-pricing** — re-applies discount logic across the order's products.
2. **Totals recompute** — recomputes subtotals, taxes, shipping, and the order total.

A failure rolls back the entire discount add / delete. Concretely:

- **Subtotal** recalculation.
- **Tax** recalculation (the new discounted total may fall into a different tax bracket — see [[settings-taxes]]).
- **Shipping** recalculation (some shipping rates depend on the order total).

### Existing-discount add sets `overwrite_product_price`

When an existing discount has a CODE and is type `flat` / `percent`, the platform marks the order-discount with `overwrite_product_price = 1`. The flag does not decide where the amount goes; the target does. A code for all products changes the product lines, and an Orders over code stays one amount on the order ([[discount-stacking-amount-by-target]]). Free-shipping codes skip the flag.

### Existing-discount add copies the code fields

When the merchant picks an existing discount, the saved order-discount record copies the discount's `code`, `code_apply`, `code_prefix`, and `code_format`. A code for all products shows inside each product line with the code in brackets and adds no totals row; in the admin order the figure is per unit (the amount ÷ the quantity). An Orders over code is a row in the totals. The master record stays unchanged except for the recalculated usage count.

## Business rules

### Side effects on ADD

- New order-discount record created (typed `flat` / `percent` / etc.).
- Order's `price_discount` and `price_total` recalculated; tax + shipping recalculated.
- For the existing-discount path: the master discount's usage is recounted (see below).
- `order.updated` webhook fires.
- History entry: `order_discount_add`.

### Side effects on DELETE

- Order-level discount record(s) deleted (all where `target_product_id IS NULL`).
- Master discount's usage restored (existing discounts only).
- Order recalculated.
- `order.updated` webhook fires.
- History entry: `order_discount_remove`. Removing order-level modifications writes no history entry.

### Uses-counter is a RECOUNT, not increment / decrement

Adding an existing discount does NOT simply bump a counter. Instead the platform RECOUNTS the discount's total uses by counting orders that have the discount AND are in a "used status" (default `paid`, `completed`, `fulfilled` — configurable in the discount statuses panel, setting `discounts_used_statuses`). Consequences:

- Adding a discount to a **pending** order does NOT bump the counter (pending isn't a used status).
- Once the order moves to paid / completed / fulfilled, a later event re-triggers the recount and the counter goes up.
- Deleting a discount from a **used-status** order recounts immediately, lowering the counter.

So merchants should not treat the counter as fully live — it reflects only orders in used statuses, and in-flight pending orders may make "uses left" projections slightly off.

### `order.updated` webhook — no discount-specific event

After add or delete, the platform fires `order.updated` with the new order state; the payload includes the discount in the order's discounts array. There is no discount-specific webhook. Receivers should be idempotent. See [[settings-hooks]].

### Audit captures the acting admin

Each add / delete writes a [[orders-history]] entry that includes the order-discount payload AND the acting admin (from the current session), so the merchant can later see WHO applied or removed the discount.

### No customer notification

The add / delete actions fire only the `order.updated` webhook for integrations — they do NOT email the customer. The customer sees the new total only when they next interact with the order (open the invoice PDF, receive the next status-change email, etc.).

## Related

- [[orders-discount-add]] — hub.
- [[orders-discount-add-form]] — add path that triggers the cascade.
- [[orders-discount-add-delete]] — delete path that triggers the cascade.
- [[settings-taxes]] — tax recalculation on discount change.
- [[settings-hooks]] — `order.updated` webhook.
- [[orders-history]] — `order_discount_add` / `order_discount_remove` audit entries.
- [[orders-invoice]] — where the discount shows on the invoice.
- [[marketing-discounts]] — master record whose usage is recounted.
- [[order]] — entity page.

## Open questions

None.
