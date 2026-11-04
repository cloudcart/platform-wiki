---
type: concept
nav_path: "Concept → Discount stacking → Per-variant rows"
aliases: ["Per-variant discount rows", "Per-product attachment regeneration", "product_to_discount", "From X now Y listing", "Discount listing price rebuild", "Latest update for this discount", "force_save", "Save the discount on your order"]
tags: [marketing, discounts, stacking, attachments, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-11-04
source_count: 3
---

> Part of [[discount-stacking]]. See the hub for the other aspects (code_apply toggle, evaluation order, cart code slots, uses counter, plan gating, Cart Rules interaction).

# Discount stacking — per-variant rows

## Definition

A no-code Flat, Percent, free-shipping or Fixed [[discount|Discount]] is stored as **one row per targeted product variant**. These rows are how a discount without a code becomes the product's own price: the storefront reads them to show "from X / now Y" on category pages and product detail pages, and the cart reads them to pick each line's product discount.

Only those discounts create rows. Quantity and Countdown discounts, codes, Code PRO and Container discounts do not.

## Scope

Covered:

- Which discounts create per-variant rows, and which variants get one.
- When rows are rebuilt, and what does not rebuild them.
- The `force_save` switch on order edit.

Not covered here:

- The runtime stacking toggle (`code_apply`) — see [[discount-stacking-code-apply]].
- The `uses` recomputation on order status changes — see [[discount-stacking-uses-counter]].
- What the amount comes off for each target — see [[discount-stacking-amount-by-target]].
- The customer-side display of "from X / now Y" pricing — see [[discounts-storefront-display]].

## Contrasts

- **No code vs. code** — a no-code discount sits on each unit as the product's own price, listings included. A code sits on the cart line and has no row, so it never changes a listing price.
- **Rows vs. the Active switch** — checkout applies a status change at once. The switch in the Discounts list and the bulk status action do not rebuild rows; saving the form does.
- **`force_save` vs `code_apply`** — `force_save` is a **persistence** switch (keeps the discount on a saved order when it is edited). `code_apply` is a **stacking** switch. They operate at different moments and are independent.

## Where it applies

- **Discount create and form save** (admin or JSON-API v2) — start the background rebuild.
- **Storefront listing pages and product pages** — read the rows.
- **Cart** — a line takes the cheapest active row among Fixed and no-code Flat or Percent, unless an up-sell, cross-sell, bundle price or Quantity tier applies first. See [[discount-stacking-evaluation-order]].
- **Order edit** on [[orders-details]] — `force_save` decides whether the discount stays.

### Which variants get a row

| Discount | Row |
|---|---|
| No-code Flat | Variants priced at or above the amount, on products whose lowest price is at or above it. The row's price is the variant price less the amount, per unit. Bundles left out. |
| No-code Percent | Each targeted variant. The row's price is the variant price less the percentage, per unit. Bundles left out. |
| No-code free shipping | Variants priced at or above the threshold. The row carries no saving. |
| Fixed | Each listed variant, at the price the merchant set. |

### When rows are rebuilt

- **Creating a discount or saving its form** writes its rows during the save. The listing engine and smart collections are refreshed afterwards.
- **Saving a product** refreshes that product's rows.
- **Editing a product's prices on a Fixed discount** removes that product's rows from every discount, Fixed, Flat and Percent, and writes back only the edited one. Flat and Percent rows return when the product is next saved or that discount is rebuilt.

The switch in the Discounts list, bulk status and list delete start no rebuild. When the expiry sweep switches a discount off, it takes that discount's rows out of use.

### `force_save` — persistence on order edit

*"Save the discount on your order"* (`force_save`) is the merchant's own switch on the discount form, and it can be off. On, it keeps the discount on a saved order even if admin-side edits make the cart no longer meet the conditions (e.g., removing the qualifying product from an order with a free-shipping-over-X discount). Off, the discount stays listed on the order, but stops being deducted while the condition is not met.

## Related

- [[discount-stacking]] — hub.
- [[discount-stacking-amount-by-target]] — per unit vs per line.
- [[discount-stacking-code-apply]] — runtime stacking toggle (independent of `force_save`).
- [[discount-stacking-evaluation-order]] — which row a line takes.
- [[discount]] — entity carrying `force_save`, `is_container`.
- [[discounts-storefront-display]] — "from X / now Y" pricing.
- [[marketing-discounts]] — discounts CRUD; a form save fires the rebuild.
- [[marketing-discounts-flat]] / [[marketing-discounts-percent]] / [[marketing-discounts-shipping]] / [[marketing-discounts-fixed]] — the discounts that create rows.
- [[marketing-discounts-quantity]] / [[marketing-discounts-countdown]] / [[marketing-discounts-code-pro]] — discounts without rows.
- [[orders-details]] — order-edit; `force_save` decides retention.
- [[api-discounts]] — JSON-API v2; saving fires the same rebuild.
- [[background-queue-inventory]] — analogous queue concept for inventory.

## Open Questions

None.
