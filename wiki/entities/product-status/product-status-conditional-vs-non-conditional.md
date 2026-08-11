---
type: entity
nav_path: "Entity → Product Status → Conditional vs Non-conditional"
aliases: ["Conditional statuses", "Non-conditional statuses", "Conditional product status", "Non-conditional product status", "Product status priority order", "Conflict indicator"]
tags: [entity, catalog, products, statuses, conditional]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

# Product Status — Conditional vs Non-conditional

> Part of [[product-status]]. See the hub for related aspects (attributes, evaluation precedence, action behaviour, lifecycle, storefront rendering).

## Identity

Product Statuses split into **two groups** by whether they auto-apply or require manual assignment. The split is **not** a manual toggle — it's **derived from the quantity operator**: empty operator → Non-conditional; set operator → Conditional. The two groups render in **two separate tables** on [[products-statuses]] with different banners, different controls, and different priority semantics.

## Aliases

- **Conditional status** — has a quantity operator set; auto-applies based on stock.
- **Non-conditional status** — no quantity operator; assigned manually per product.
- **Priority order** — the drag-and-drop sort within the Conditional table.
- **Conflict indicator** — the red error icon in the Sorting column when two rules overlap.

## Key Attributes

### The two-table split

| Group | Where it lives | Info banner | How it applies |
|-------|----------------|-------------|----------------|
| **Conditional** | Top table on [[products-statuses]]. | *"Conditional statuses are applied automatically based on product stock quantity."* | Auto-applies at storefront query time. The platform evaluates rules top-to-bottom by `sorting` and picks the FIRST whose operator + value match. |
| **Non-conditional** | Bottom table on [[products-statuses]]. | *"Non-conditional statuses are applied manually per product. No quantity check."* | Merchant picks the status manually on each product's editor OR via the bulk action *"Change product status"* on [[products-products]]. Non-conditional statuses do NOT participate in the sort-order priority chain. |

### Priority order matters for Conditional statuses

Two Conditional statuses can both match the same product (e.g., *"Lower than 5"* AND *"Lower than or equal to 5"* both match a product with 3 in stock). The platform picks the **first matching rule by sort order**. The merchant should put the most specific rules first.

**Recommended ordering:**

1. Special states first (*"Continue selling"*, *"Not tracked"*).
2. Specific quantity ranges next (*"Lower than or equal to 5"* → *"Limited stock"*).
3. Catch-all rules last (*"Greater than 0"* → *"In stock"*).

### Conflict indicator catches overlapping rules

The Sorting column displays the rule's index plus an **error indicator** when the rule conflicts with another rule (e.g., two rules both targeting *"quantity = 0"* with different actions). The merchant resolves by editing one of them — the platform applies the topmost matching rule by sort order, so the lower-priority rule would never fire anyway, but the indicator surfaces the unreachable rule.

### One status applies per product at a time

A product can only display ONE status badge on the storefront. The Conditional system picks one based on priority; the Non-conditional override (manually set on a product) takes precedence over Conditional rules if set. See [[product-status-evaluation-precedence]] for the full 5-level priority chain.

### Non-conditional override beats Conditional rules

If the merchant explicitly assigns a Non-conditional status on the Product editor (the `status_id` or `out_of_stock_id` slot), that assignment **overrides** every Conditional rule for that product. The Conditional system is consulted only when both slots are empty. See [[product-status-evaluation-precedence]] for the precedence chain.

### Sort applies only inside the Conditional table

The Non-conditional table also has rows, but those rows don't participate in the priority chain — they only become active when explicitly picked on a product. The `sorting` value on a Non-conditional row is `0` (see [[product-status-lifecycle-management]] for how `sorting` is auto-assigned on create).

## Where it appears

- [[products-statuses]] — the page renders the two tables side-by-side with their respective banners.
- [[product]] — products can be assigned a Non-conditional status via `status_id` / `out_of_stock_id`; Conditional rules also evaluate against the product at query time.
- [[products-products]] — the bulk action *"Change product status"* writes a Non-conditional status onto multiple products at once.
- [[product-status-evaluation-precedence]] — the full precedence chain including how the Conditional vs Non-conditional split feeds in.

## Related

- [[product-status]] — hub.
- [[products-statuses]] — taxonomy management screen.
- [[products-products]] — bulk *"Change product status"* operation.
- [[product]] — carries the two status reference slots.

## Open Questions

None.
