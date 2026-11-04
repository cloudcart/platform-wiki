---
type: feature
nav_path: "Marketing → Discounts → Quantity → Uniqueness constraint"
route_name: discounts-create
route_path: /admin/marketing/discounts/create/quantity
aliases: ["Quantity discount one per product", "Volume discount conflict", "A volume discount with this product already exists", "Product is already in use", "Quantity discount delete cascade"]
tags: [marketing, discounts, quantity, validation, constraints]
plan_gates: []
created: 2026-06-10
updated: 2026-11-04
source_count: 2
---

> Part of [[marketing-discounts-quantity]]. See the hub for the other aspects (form, tier evaluation, stacking, plan gating, storefront display).

# Quantity discount — one product per discount, one discount per product

## Purpose

This aspect documents the **uniqueness constraint** on Quantity discounts — a given product can only be on one Quantity discount at a time, regardless of `active` status. It covers the validation strings on create and on edit, the workflow when a merchant needs to switch products, and the cascade behaviour when the discount or its target product is deleted.

## Where to find it

The conflict surfaces on the **Customer buys** product picker on the Quantity create / edit form (`/admin/marketing/discounts/create/quantity` — see [[quantity-discount-form]]) and in the create / update endpoint response when the form is bypassed. The list of existing Quantity discounts is [[marketing-discounts]] — that's where the merchant finds (and deletes) the conflicting record.

## What the merchant can do here

When the uniqueness validation blocks a save, the merchant's path is to **edit the existing Quantity discount on that product** and adjust its tiers (preserves the row + customer-group settings). Neither deactivating nor deleting the conflicting discount from the list releases the product — see Business rules below.

## Settings & fields

The constraint is enforced on `product_id` — the field exposed on the Quantity form. No merchant-tunable settings on this aspect; the validation strings are the surface.

| Field | Backend key | Constraint surface |
|-------|-------------|--------------------|
| **Customer buys** (product picker) | `product_id` | On create: *"Product is already in use"*. On edit, when switching to a product another Quantity discount uses: *"A volume discount with this product already exists"* (BG: *"Вече съществува количествена отсъпка с този продукт"*). |

The constraint counts rows in the `quantity_discounts` table by `product_id` alone — `active` is NOT a filter. See [[quantity-discount-form]] for the picker UX and [[products-products]] for the target product's relation.

## Business rules

### One product per Quantity discount

A product can be on only **one** Quantity discount at a time, regardless of its `active` status. When the merchant **creates** a new Quantity discount and picks (in the **Customer buys** select) a product that another Quantity discount already uses — active OR inactive — the save is rejected with:

> *"Product is already in use"*

So a deactivated Quantity discount still blocks a new one on the same product. The way forward is to **edit the existing Quantity discount on that product and adjust its tiers** — that preserves the row and just changes the ladder.

The conflict check also runs when editing: switching an existing discount to a product another Quantity discount already uses is refused with *"A volume discount with this product already exists"*. Name, dates and customer groups changed in the same save stay saved.

Net effect: if the merchant edits an existing Quantity discount and submits the **same** `product_id` (the most common case — they're tweaking the tiers), no conflict fires. If they edit the discount and try to **switch** the `product_id` to another product that's already taken, the save is refused.

### Why deactivation does not release the slot

The guard query counts rows by `product_id` only, with no `active` filter. Setting `active = no` on a Quantity discount keeps the row in the table, so the slot stays held. This is intentional — the merchant's stored configuration shouldn't silently become "available to be overwritten" just because they paused the discount.

A merchant who wants to temporarily replace a Quantity discount on a product edits its tiers; neither deactivating nor deleting it frees the product.

### Deleting the discount from the list

Deleting a Quantity discount from the [[marketing-discounts]] list (or with `discountsBulkDelete`) removes the discount, but its tier rows stay and still count for the product: creating a new Quantity discount on that product keeps failing with *"Product is already in use"*. The left-over rows give no discount in the cart or on the product page.

Order-discount history on past orders is **preserved** — analytics keep the trail, and the saved per-line tier price on an existing order doesn't change retroactively. See [[quantity-discount-tier-evaluation]] for the namespace gate that prevents admin order-edit from re-evaluating tiers (a deleted Quantity discount thus has no effect on already-placed orders, but the tier price on their lines stays).

### Delete cascade — product → Quantity discount

When the **underlying product** is deleted, the delete-by-product helper deletes the Quantity discount AND its child tier rows (so a Quantity discount has no orphaned child rows after the product is removed).

The merchant doesn't need to manually clean up the discount after deleting the product — the cascade runs in the same transaction as the product delete.

### Deleting a product is permanent for its Quantity discount

Deleting a product permanently deletes its Quantity discount and tiers. Restoring the product does not restore them; the merchant creates the discount again.

### Permission

The page and CRUD endpoints fall under the standard `marketing.discounts` admin permission. A user without this permission gets a generic HTTP 403 from the discount-related endpoints (independent of plan gating — see [[quantity-discount-plan-gating]] for the plan-level 403s).

### Customer-group filter is per-discount, not per-tier

(Related constraint, same uniqueness logic.) The customer-group allow-list lives on the parent Discount record — every tier in the ladder shares the same `customer_groups` restriction. There's no way to say "Tier 1 applies to everyone, Tier 2 applies only to VIPs". Merchants who need group-segmented tier ladders must create separate Quantity discounts per group — which **then collides with the one-Quantity-discount-per-product rule on a single product**. So group-segmented tiers on the same product aren't supported in practice; the workaround is multiple separate Quantity discounts on different product slugs (e.g. clone the product) or [[apps-cart-rules]] which can express multi-condition promotions.

## Related

- [[marketing-discounts-quantity]] — hub.
- [[quantity-discount-form]] — the `product_id` picker and the verbatim error strings.
- [[quantity-discount-plan-gating]] — different 403 path (plan-level instead of permission-level).
- [[marketing-discounts]] — parent feature; shared list / delete endpoints.
- [[products-products]] — the target product; deleting it cascades to the Quantity discount.
- [[apps-cart-rules]] — alternative for multi-condition promotions that the one-per-product rule blocks.
- [[customers-custom-groups]] — `customer_groups[]` allow-list source for the per-discount audience filter.

## Open questions

None.
