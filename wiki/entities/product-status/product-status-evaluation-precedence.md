---
type: entity
nav_path: "Entity → Product Status → Evaluation precedence"
aliases: ["Product Status priority chain", "Product Status evaluation order", "Out-of-stock override", "Bundle stock evaluation", "Status sorting auto-assignment"]
tags: [entity, catalog, products, statuses, precedence]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

# Product Status — Evaluation precedence

> Part of [[product-status]]. See the hub for related aspects (attributes, Conditional vs Non-conditional, action behaviour, lifecycle, storefront rendering).

## Identity

When the storefront renders a product card or detail page, the platform must pick **exactly one** Product Status to display. This page documents the **strict 5-level priority chain** used to pick, plus the Bundle exception (binary in-stock / out-of-stock only) and the `sorting` auto-assignment rule for newly created Conditional rules.

## Aliases

- **Priority chain** — the 5-level evaluation order.
- **Out-of-stock override** — the top-priority slot for the `out_of_stock_id` reference.
- **Explicit slot** — the merchant-assigned `status_id` value, which beats every Conditional rule.
- **Hard fallback** — the platform's last-resort localised label when no Status row applies.

## Key Attributes

### The 5-level priority chain

The platform evaluates which Product Status applies in this strict order — **first match wins**:

1. **Out-of-stock override** — if `tracking = yes`, `continue_selling = no`, AND the variant quantity is below its minimum, and the product has a non-null `out_of_stock_id`, that Status applies — even if a Conditional rule would otherwise match.
2. **Explicit in-stock pick** — if the product has a non-null `status_id` and stock is sufficient (or tracking is off), that Status applies — overrides every Conditional rule.
3. **Conditional rules** — the platform iterates Conditional Statuses in the order set on [[products-statuses]] (top to bottom by `sorting`) and applies the FIRST whose operator + quantity match the product's current stock.
4. **Fallback by type** — if no Conditional rule matches, the platform shows the first system Status whose `type` matches the resolved state (`in_stock` if buyable, `out_stock` otherwise).
5. **Hard fallback** — if no Status of the right type exists at all, the platform renders a default *"Out of stock"* or *"In stock"* label (localised) without any badge styling.

So a merchant who explicitly assigns a Status on the Product editor (slot 2) always wins against Conditional rules; the Conditional system is consulted only when the slot is empty.

### When zero Conditional rules match

When ZERO Conditional rules match a product, the storefront shows whatever Non-conditional status is manually assigned via `status_id` / `out_of_stock_id`. If none is assigned, the product shows **no status badge at all** (the badge area is empty) — there is no platform default fallback label beyond the localised hard-fallback text in step 5 above.

### Bundle stock evaluation is binary

For a Bundle product, the Status guess engine **bypasses the operator chain** — it just asks *"are all constituents in stock?"* If yes → in-stock Status. If no → out-of-stock Status. Quantity-comparison operators (Lower than 5, Greater than 0, etc.) **never fire** for Bundle products.

See [[inventory-bundle-stock]] for the underlying bundle-stock derivation rules.

### `sorting` is auto-assigned on creation

When the merchant creates a new Conditional Status, the platform auto-assigns `sorting = max(existing sorting) + 1` — so new Conditional Statuses are appended to the bottom of the list with the lowest priority. The merchant must drag them up if they should take precedence over older rules. Non-conditional Statuses receive `sorting = 0` and are not part of the priority chain.

### One status per product (NOT per variant)

The Conditional status is evaluated against the product's **aggregate stock** (sum across variants). A single status badge displays on the storefront product card / detail. To indicate per-variant stock state to customers, the merchant uses the variant picker UI itself (the theme shows greyed-out / unavailable variants based on per-variant quantity); **there is no per-variant Product Status badge**.

### What the merchant CANNOT do at evaluation time

- Set up complex multi-condition rules (AND combinations of quantity + price + category) — only ONE condition per status.
- Schedule a status to apply only between specific dates / times — statuses are evaluated in real-time based on current stock.
- Configure a different priority chain — the 5-level order is fixed.

## Where it appears

- [[products-statuses]] — the merchant edits priority via drag-reorder of the Conditional table.
- [[product]] — the entity carries `status_id` (slot 2) and `out_of_stock_id` (slot 1) — see [[product-status-conditional-vs-non-conditional]] for how the slots interact with the Conditional rules.
- Storefront product card + detail — the chain runs on every storefront query.
- [[inventory-bundle-stock]] — the bundle-stock derivation that the bundle Status exception delegates to.

## Related

- [[product-status]] — hub.
- [[products-statuses]] — taxonomy management screen with drag-reorder.
- [[product]] — carries the two status reference slots.
- [[bundle]] — bundle entity; uses binary Status evaluation.
- [[inventory-bundle-stock]] — bundle stock derivation rules.
- [[inventory-variant-model]] — the `tracking` and `continue_selling` flags feeding the override step.

## Open Questions

None.
