---
type: feature
nav_path: "Products → Bundles → Stock & availability"
route_name: bundles-list.new
route_path: /admin/products/bundles-new
aliases: ["Bundle stock", "Bundle availability", "Bundle out of stock", "Bundle max quantity", "Bundle min stock"]
tags: [apps, administration, products, bundles, inventory]
plan_gates: ["bundles"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---
# Bundles — stock & availability

> Part of [[bundles-list]]. See the hub for the other aspects (creation, pricing, plan gates).

## Purpose

This aspect covers **where a bundle's stock comes from and how its availability is decided**: stock is always pulled from the constituents (never an independent bundle count), displayed quantity is the MIN of tracked constituents, the standard "Out of stock" overlay is skipped, the cart max-quantity is capped to the smallest constituent cap, and deleting a bundle cleans it out of active carts.

The inventory-side concept (the min-across-children rule, child-flag-wins, auto-deactivation) is documented on [[inventory-bundle-stock]]; this page is the **admin/merchant-facing** view from the Bundles screen.

## Where to find it

Availability surfaces on the Bundles list (route `bundles-list.new`, path `/admin/products/bundles-new`) and on the bundle's storefront listing. There is no separate stock-editing field on the bundle — the merchant edits the constituents' stock via [[products-inventory]].

## What the merchant can do here

- See whether each bundle is in stock (driven by constituents, not a typed number).
- Toggle the bundle's `enable_sell` flag to force its storefront status.
- Restock a bundle by restocking its worst-stocked constituent (there is no bundle-level stock field to edit).

## Settings & fields

- `enable_sell` — the bundle's own sell flag (forces In Stock / Out of Stock status, see below).
- `tracking` — derived: YES if at least one component is tracked, NO if none are. Not a typed bundle field.

## Business rules

### Stock pulls from constituents, never from the bundle

When a customer buys a bundle, the platform decrements the QUANTITY of each constituent product. So if Bundle X = 1 camera + 1 lens, buying one bundle decrements 1 camera + 1 lens. The bundle product itself has no independent stock count — its availability is derived from the constituents.

### Bundle stock = MIN of tracked constituent stock

The displayed bundle quantity is the **minimum quantity across constituents that have stock tracking ON**. So if Bundle = `Camera (qty 5) + Lens (qty 2) + Bag (tracking OFF)`, the bundle shows quantity = `2`. A constituent with tracking OFF does not constrain bundle availability. The bundle's `tracking` flag is YES if at least one component is tracked, NO if none are.

### Bundle availability ignores the standard "Out of stock" overlay

The red "Out of stock" overlay/label the platform automatically applies to regular products (when `enable_sell` is off OR a variant is out of stock) is **explicitly skipped for bundles**. Bundles get their availability solely from constituent stock plus the bundle's own `enable_sell` flag. The storefront product status is forced:

- `enable_sell` ON → bundle shows **In Stock** status.
- `enable_sell` OFF → bundle shows **Out of Stock** status.

The conditional product-status rules configured in [[products-statuses]] are NOT evaluated for bundles.

### Maximum buy quantity = MIN of constituent max-quantities

When a customer sets bundle quantity in the cart, the cap is the smallest `maximum_quantity` across the bundle's components. So if one component allows max 3 and another allows max 10, the bundle's cap is 3.

### Cart cleanup on bundle delete

When a bundle is deleted, all bundle-item rows for that bundle are removed from active carts — customers who had it in their cart see it disappear on the next page load, and the constituent items do not auto-add separately. (The same rule is noted from the editing angle on [[bundles-list-creation]].)

## Related

- [[bundles-list]] — hub.
- [[inventory-bundle-stock]] — the inventory-side concept (min-across-children, child-flag-wins, auto-deactivation).
- [[products-inventory]] — where constituent stock is edited.
- [[products-statuses]] — custom statuses that bundles deliberately bypass.
- [[bundle]] — the bundle entity (`enable_sell`, `tracking`).

## Open questions

None.
