---
type: entity
nav_path: "Entity → Product Status"
aliases: ["Product Status", "Stock status", "Availability status", "Product availability", "In-stock label", "Out-of-stock label", "Статус на продукта", "Наличие", "Налични", "Изчерпан", "Очаквана наличност"]
tags: [entity, catalog, products, statuses, stock, customer-facing]
created: 2026-05-21
updated: 2026-06-10
source_count: 1
---

# Product Status

## Identity

A **Product Status** is the **stock-based availability label** that customers see on the storefront product card and product detail page — *"In stock"*, *"Out of stock"*, *"Limited stock — only 3 left"*, *"Coming soon"*, *"Request a quote"*, etc. Each status carries a **name** (what the customer sees), an optional **quantity condition** (a rule that triggers it automatically based on the product's stock count — e.g., *"when quantity is ≤ 0"*), and an **action type** that controls what happens to the Buy button when the status applies (show it normally, hide it, replace it with a "Request" button, or replace it with a "Notify me when in stock" subscription button).

A Product Status is **distinct from the Order / Payment / Shipping statuses** ([[order-status]], [[payment-status]], [[shipping-status]]) configured in [[settings-statuses]] — those govern the order lifecycle. Product Status is purely about **product availability** as customers see it on the storefront. The taxonomy is managed under [[products-statuses]]; the page splits statuses into two groups (Conditional vs. Non-conditional). Each [[product|Product]] has two slots for status references on its record: `status_id` (the in-stock status, e.g., *"Ships tomorrow"*) and `out_of_stock_id` (the out-of-stock status, e.g., *"Notify me"*). Conditional statuses also auto-apply at storefront query time based on the product's current stock count.

## Aliases

- **Product Status** — the canonical merchant-facing term in the admin UI.
- **Stock status** / **Availability status** — used interchangeably in storefront contexts.
- **Product availability** — informal phrasing.
- **In-stock label** / **Out-of-stock label** — used when referring to the two slots on the product record.
- **Статус на продукта** / **Наличие** / **Налични** / **Изчерпан** / **Очаквана наличност** — Bulgarian equivalents.

## Key Attributes

A Product Status is NOT a fixed enum — the merchant defines as many as the store needs in [[products-statuses]]. The high-level shape is:

- **Status name** — required, customer-facing label.
- **Quantity operator** — one of 8 values, optional. Empty operator = Non-conditional (manual). Set operator = Conditional (auto-applies).
- **Quantity value** — the numeric value the operator compares against.
- **Action type** — one of 4 values controlling the Buy button (show / hide / request / subscribe).
- **Button text** — custom CTA label for Request / Subscribe substitute buttons.
- **Sort order** — drag-and-drop position in the Conditional table; topmost matching rule wins.

For the full field catalogue with the 8 operators, the 4 action types, and the silent auto-clear rules for `button_text` and `quantity`, see [[product-status-attributes]].

## Sub-pages (in this cluster)

This entity is split into 6 aspect pages. The Assistant should drill into the aspect that matches the question, not read every page.

- [[product-status-attributes]] — verbatim field set + the 8 quantity operators + the 4 action types + the `button_text` / `quantity` auto-clear rules on save.
- [[product-status-conditional-vs-non-conditional]] — the two-table taxonomy split, priority ordering for Conditional rules, the conflict indicator in the Sorting column, why one status applies per product at a time.
- [[product-status-evaluation-precedence]] — the strict 5-level priority chain (out-of-stock override → explicit slot → Conditional rules → fallback by type → hard fallback); bundle binary stock evaluation; `sorting` auto-assignment on create.
- [[product-status-actions-buy-button]] — what each action type does on the storefront (Show / Hide / Request / Subscribe); Request app dependency; back-in-stock subscriber capture; theme-controlled visual styling.
- [[product-status-lifecycle-management]] — the Create → Active → Re-evaluated → Updated → Deleted lifecycle; 2 default statuses seeded at install; silent NULL on delete; no `active` flag; store-wide cache + 24-hour TTL.
- [[product-status-storefront-rendering]] — how the status is rendered to the customer; real-time re-evaluation on stock change; per-product (not per-variant or per-channel) badge; bulk-change product status flow; relationship with `order_status_for_quantity_decrease`.

## Where it appears

- [[products-statuses]] — the management screen for the taxonomy (two tables: Conditional + Non-conditional, with the Add / Edit modal).
- [[products-products]] — the product list; the bulk action *"Change product status"* applies Non-conditional statuses to multiple products at once.
- [[product]] — the entity that carries `status_id` (in-stock) and `out_of_stock_id` (out-of-stock) references.
- [[products-inventory]] — the per-product inventory editor; the *"Continue selling when sold out"* flag is evaluated by the *"Continue selling"* Product Status operator.
- [[products-missing-product]] — the subscribers waiting for *"Notify me when in stock"* emails (driven by the *"Show as subscribe"* action).
- Storefront product card + product detail page — where the customer actually sees the status badge.

## Related

### Related entities

- [[product]] — every Product carries two Product Status references (in-stock + out-of-stock).
- [[variant]] — variants drive the aggregate stock count that Conditional statuses evaluate against. (Note: no per-variant Product Status — one badge per product.)
- [[order-status]] / [[payment-status]] / [[shipping-status]] — distinct status taxonomies governing the order lifecycle, NOT the product.

### Cross-cutting concepts

- [[inventory-tracking]] — the inventory model hub.
- [[inventory-variant-model]] — the `tracking` and `continue_selling` flags that drive when Conditional statuses fire.
- [[inventory-decrement-timing]] — the `order_status_for_quantity_decrease` setting controls when stock decrements and therefore when statuses flip.
- [[inventory-in-stock-badge]] — storefront badge logic + low-stock alert gating.
- [[checkout-flow]] — checkout decrements stock, which re-triggers Conditional status evaluation.

### Settings & feature pages

- [[products-statuses]] — the taxonomy management screen.
- [[products-products]] — the product list with bulk *"Change product status"*.
- [[products-inventory]] — per-product inventory editor.
- [[products-missing-product]] — back-in-stock subscriber management.
- [[settings-cart]] — the `order_status_for_quantity_decrease` setting controls when stock decrements and therefore when statuses flip.
- [[settings-hooks]] — `product.updated` webhook fires on stock changes that trigger status re-evaluation.

## Open Questions

None — all items resolved or distributed to aspect sub-pages.
