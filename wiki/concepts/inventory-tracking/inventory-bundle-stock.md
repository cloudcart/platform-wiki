---
type: concept
nav_path: "Concept → Inventory tracking → Bundle stock"
aliases: ["Bundle stock", "Bundle product stock", "Bundle in-stock derivation", "Bundle child-wins rule", "Bundle minimum-available rule"]
tags: [catalog, inventory, stock, bundles, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[inventory-tracking]]. See the hub for the other aspects (variant model, decrement timing, restock, oversell, multi-warehouse, in-stock badge, debugging playbook).

# Inventory — bundle stock derivation

## Definition

A **bundle product** (`type = bundle`) does NOT have its own `quantity`. Its sellable units are composed of OTHER products (the bundle's children). The bundle's effective stock is **the minimum available stock across all constituent child Variants**, scaled by how many of each child the bundle includes.

The storefront does not display a single "bundle stock count" anywhere — the check is **binary**: "in stock" or "out of stock" based on whether every child can be sold. The merchant who wants to know "how many bundles can I sell right now" has to compute it themselves from the children's stock counts.

## Scope

Covered:

- The min-across-children rule and what "scaled by inclusion count" means.
- The child-flag-wins rule (child's `continue_selling = no` overrides the bundle's flag).
- Auto-deactivation when a child is deactivated.
- Why bundle stock is not a numeric display.

Not covered here:

- The bundle entity model itself — see [[product]] (`type = bundle`) and [[bundles-list]].
- Per-child decrement when a bundle order ships — that follows [[inventory-decrement-timing]].
- Multi-warehouse handling of bundle children — see [[inventory-multi-warehouse]].

## Contrasts

- **Bundle stock vs Component stock** — a bundle doesn't have its own stock; it's derived from its child Variants. Restocking the worst-stocked child brings the bundle back.
- **Bundle child-flag wins** — even if the bundle parent has `continue_selling = yes`, a child with `tracking = yes`, `continue_selling = no` and `quantity = 0` makes the bundle out-of-stock. The child flag wins. This is the **opposite** of how merchants usually expect bundle aggregation to work.
- **Binary in-stock vs numeric count** — the storefront treats bundle stock as a yes/no, not a number. There is no "12 bundles available" badge anywhere in the admin or storefront.

## Where it applies

The bundle stock check runs at every storefront product-card render + order-submission validation:

- **Storefront product card / detail page** — the bundle shows "In stock" only if EVERY child Variant satisfies `tracking = no OR continue_selling = yes OR (quantity > 0 AND quantity >= minimum)`. If any child fails, the bundle is out-of-stock.
- **Order submission** — when a customer checks out with a bundle in the cart, the platform validates each child Variant has enough stock for the requested bundle quantity. Failure blocks checkout with a "Variant X is out of stock" message.
- **Order fulfillment** — when the bundle's order moves to a decrementing status (per [[inventory-decrement-timing]]), each child Variant decrements by the bundle's child-inclusion count × the order's bundle quantity. Cancelling the order re-credits each child per [[inventory-restock]].

### Worked example — bundle stock from worst-stocked child

A "Spring Outfit" bundle includes:
- 1× T-shirt Red Large
- 1× Jeans Blue 32
- 1× Cap Black

Variant stock:
- T-shirt Red Large: 10
- Jeans Blue 32: 3
- Cap Black: 50

Effective bundle stock = `min(10, 3, 50) = 3 bundles available`.

When the third bundle sells (T-shirt Red Large now 9, Jeans Blue 32 now 2, Cap Black now 49), the bundle stays in-stock (2 more available). When Jeans Blue 32 sells out separately from another customer buying just the jeans, the bundle goes out-of-stock — even though T-shirt and Cap still have plenty.

### Auto-deactivation of bundles when a child deactivates

When a child product of a bundle is deactivated (e.g., the merchant un-publishes the T-shirt because it's discontinued), the bundle is **auto-deactivated** too. The storefront stops listing the bundle.

When the child is reactivated later, the bundle is **NOT auto-reactivated** — the merchant must do that manually (per [[product|Product]]'s bundle business rules). This is intentional: re-publishing a child product doesn't always mean the merchant wants the bundle to come back automatically.

### Child `continue_selling = no` blocks the bundle, regardless of bundle's own flag

The bundle's in-stock check passes only when EVERY child satisfies: `tracking = no OR continue_selling = yes OR quantity > 0`. So even if the merchant sets `continue_selling = yes` on the bundle parent, a single child with `tracking = yes`, `continue_selling = no` and `quantity = 0` makes the bundle out-of-stock. **The child flag wins.**

Common merchant confusion: *"I turned on Continue selling on my bundle but it still shows out-of-stock — why?"* — answer: at least one child has `continue_selling = no` AND has run out. The merchant either turns on `continue_selling` for the affected child or restocks it.

### Bundle as a child of another bundle — not supported (verify)

Nesting bundles inside bundles is not a documented use case. The platform's bundle check walks `bundle.children` flatly; if a child is itself a bundle, the behaviour is undefined `(verify)`. Merchants nesting bundles for kit-of-kits scenarios should test carefully before relying on the stock check.

## Related

- [[inventory-tracking]] — hub.
- [[inventory-variant-model]] — the per-Variant `quantity` that bundle children carry.
- [[inventory-decrement-timing]] — when bundle-child stock decrements (same rules as standalone products).
- [[inventory-restock]] — bundle-child restock on cancel.
- [[inventory-oversell]] — child's `continue_selling` flag wins over bundle's.
- [[inventory-in-stock-badge]] — bundle card shows binary in-stock based on worst child.
- [[product]] — the entity (`type = bundle`).
- [[bundles-list]] — admin bundle list + creation flow.

## Open Questions

- Nesting bundles inside bundles — does the platform handle bundle-of-bundles correctly, or does the stock check break? Not documented in current code path `(verify)`.
