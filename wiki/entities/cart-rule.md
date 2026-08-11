---
type: entity
nav_path: "Entity → Cart Rule"
aliases: ["Cart Rule", "Cart-Rule", "Conditional discount rule", "Trigger-action rule", "Cart automation rule", "Promo rule", "Касово правило", "Маркетингово правило", "Условна отстъпка", "Правило за количка"]
tags: [entity, marketing, automation, discounts, rules-engine, apps]
created: 2026-05-23
updated: 2026-06-10
source_count: 5
---

# Cart Rule

## Identity

A **Cart Rule** is a **trigger-and-action rule** that runs against every cart at checkout. The merchant uses Cart Rules to express conditional promotions that simple [[discount|Discounts]] cannot — composite *"if X AND Y THEN Z"* logic that combines cart-level conditions (total > N), product-level conditions (cart contains product Y), customer-level conditions (customer in group Z, has past orders), and date-window conditions (active between dates), then fires a discount + an optional customer-facing message at checkout. Examples merchants commonly express as Cart Rules:

- *"Give 10% off when the cart contains 3+ items from Vendor X AND total > 50 EUR."*
- *"Buy 5, get the cheapest one free."*
- *"15% off for VIP customers on Brand Y products until end of month."*
- *"Stacked deals: 5% off summer category AND extra 3% if cart > 100 EUR AND free shipping if customer has 3+ past orders."*
- *"Add 6 EUR more for free shipping"* — a customer-facing nudge message.

The merchant manages Cart Rules on [[apps-cart-rules]]. One Cart Rule can hold **multiple distinct deals** (called *"rows"*), each with its own triggers, action, and message. Every cart at checkout passes through every Active rule in **priority order** (the rule's `sort_order`, descending — higher = evaluated first), and matching rules **stack** their discounts on top of standard [[discount|Discounts]] — but with a critical cart-level-vs-product-level split. See [[cart-rule-stacking]].

Cart Rules are evaluated AFTER all standard Discounts have been applied — they operate on the **post-discount** cart, allowing the merchant to compose layered promotions. See [[discount-stacking]] for the evaluation order.

## Aliases

- **Cart Rule** / **Cart-Rule** — the canonical merchant-facing term in CloudCart admin UI ("Cart Rules" sidebar item under Marketing).
- **Conditional discount rule** — emphasising that the rule is a discount gated by conditions.
- **Trigger-action rule** — emphasising the rules-engine shape (when X, do Y).
- **Cart automation rule** / **Promo rule** — informal phrasing.
- **Касово правило** / **Маркетингово правило** / **Условна отстъпка** / **Правило за количка** — Bulgarian variants merchants use interchangeably.

## Key Attributes

The Cart Rule entity is documented across six aspect pages. The high-level shape is:

- **Top-level rule fields** — `name`, `title`, `status` (Active / Inactive / Draft), `active_from`, `active_to`, `sort_order`, `deleted_at`. See [[cart-rule-fields]] for the verbatim catalogue + validation.
- **Rows (multi-deal capability)** — a rule holds many rows, each a trigger-set + action + message. Within a rule, only the FIRST matching row fires (OR-fallback). See [[cart-rule-rows-and-triggers]].
- **Triggers (per row)** — three families: cart-level (`cart_amount`, `cart_quantity`, `cart_products_count`), product-level (14 filters including `product`, `category`, `vendor`, etc.), customer-level (`customer_group`, `order_amount`, `order_count`). Combined with AND inside one row. See [[cart-rule-rows-and-triggers]].
- **Action (per row)** — fixed to a discount; action value type is `percent` / `amount` / `free_shipping`. See [[cart-rule-actions]].
- **Message (per row)** — customer-facing message shown at checkout via the cart's notification slot.
- **Stats** — used-count + total-discount derived via `withStats` join on `orders_modification`. See [[cart-rule-evaluation]].

## Sub-pages (in this cluster)

This entity is split into 6 aspect pages. The Assistant should drill into the aspect that matches the question, not read every page.

- [[cart-rule-fields]] — verbatim attribute catalogue with validation strings (`name`, `title`, `status`, `active_from`, `active_to`, `sort_order`, `deleted_at`, `status_key`, active-date-scope semantics).
- [[cart-rule-rows-and-triggers]] — rows-as-OR-fallback (only the FIRST matching row fires), AND semantics within a row, full trigger taxonomy across the three condition families, action-only filter types.
- [[cart-rule-actions]] — action fixed to discount, the three action value types (`percent` / `amount` / `free_shipping`), action-scoping filters, customer-facing message slot.
- [[cart-rule-stacking]] — Discounts-then-Cart-Rules ordering, cart-level winner-takes-all vs product-level accumulate, `sort_order` priority + the `creating` auto-assignment hook.
- [[cart-rule-lifecycle]] — Draft / Active / Inactive / Expired / Soft-deleted states, save-time transitions, no audit trail, soft-delete one-way without support.
- [[cart-rule-evaluation]] — when the matcher runs, customer snapshot inputs, matches + notifications outputs, `withStats` analytics, AI-assisted construction.

## Where it appears

- [[apps-cart-rules]] — the main list + editor. Drag-and-drop reorder; inline Active toggle; soft-delete trash; AI assistant. This is where the merchant lives when working with Cart Rules.
- [[cart]] — at checkout, the cart's evaluator runs every Active Cart Rule. The cart's notification slot surfaces any per-row messages.
- [[order]] — orders carry any Cart Rule discounts that fired at the time of submit (snapshotted onto the order's discount lines, same as standard Discounts).
- [[discount-stacking]] — explains the evaluation order: Discounts first, then Cart Rules on top.
- [[checkout-flow]] — the cart-to-order flow that triggers Cart Rule evaluation at multiple points.

## Related

- [[cart]] — the entity Cart Rules act on. Carts read the rules at every evaluation.
- [[order]] — orders inherit the Cart Rule discounts present at submit time.
- [[discount]] — Cart Rules and Discounts are sibling promotion mechanics. Discounts are simpler (one condition → one discount); Cart Rules are composite. They stack: Discounts evaluate first, Cart Rules layer on top.
- [[customer-group]] — Cart Rule customer-triggers reference groups (e.g., *"customer in VIP group"*).
- [[product]] / [[category]] / [[vendor]] — Cart Rule product-triggers reference these via product-filter conditions.
- [[customer]] — Cart Rule customer-triggers reference customer attributes (past orders, lifetime revenue, group).
- [[campaign]] — sibling marketing surface for messages (not discounts); contrast with Cart Rules.
- [[discount-stacking]] — overall stacking semantics across Discounts + Cart Rules.
- [[checkout-flow]] — when in the cart-to-order journey Cart Rules evaluate.
- [[cart-vs-order-lifecycle]] — Cart Rules act on the cart; resulting discounts get snapshotted onto the order at submit.

## Open Questions

- ⏸️ Whether Cart Rule discounts count toward the discount usage counter on the resulting [[order|Order]] in the same way standard [[discount|Discount]] uses do — see [[cart-rule-evaluation]].
