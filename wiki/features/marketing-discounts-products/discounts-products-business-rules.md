---
type: feature
nav_path: "Marketing → Discounts → Products → Business rules"
route_name: discounts-products
route_path: /admin/marketing/discounts/products/:id
aliases: ["Discount products business rules", "Fixed discount type guard", "Default fixed discount singleton", "Default Fixed Discount", "On Sale product form", "Customer-group fan-out for discount products", "Бизнес правила за продукти в отстъпка", "Добави отстъпка", "Цена след отстъпка"]
tags: [marketing, discounts, fixed, products, business-rules, customer-groups, plan-gates]
plan_gates: ["discount_fixed"]
created: 2026-06-10
updated: 2026-11-09
source_count: 3
---

# Discount products — business rules & edge cases

> Part of [[marketing-discounts-products]]. See the hub for the list view, modal flow, fields, and save semantics.

## Purpose

This page catalogues the **cross-cutting rules** that affect what the merchant sees on the Discount products page but don't fit cleanly into list, modal, fields, or save-flow scopes: the discount-type guard, the picker's search source, the default Fixed discount singleton, customer-group + date inheritance from the parent discount, plan-gating, and permissions.

These rules are the most common source of support tickets where the merchant says "I don't understand why my discount shows X" — most of the time the answer lives here, not in the modal or list views.

## Where to find it

The rules apply to Marketing → Discounts → (click **Products** on a Fixed-type discount row) → list at `/admin/marketing/discounts/products/:id` and its modal. Several of them depend on parent-discount settings that live on the [[marketing-discounts-fixed]] edit form.

## What the merchant can do here

Most of these rules describe behaviour the merchant **inherits** rather than controls directly. The merchant influences them by:

- Choosing the parent Fixed discount's customer-group restrictions on the parent edit form.
- Choosing the parent Fixed discount's date window.

## Settings & fields

This page documents behaviour driven by parent-discount settings (customer groups, dates) and store-level settings (plan, permissions). Its own fields are documented on [[discounts-products-fields]].

## Business rules

### Discount-type guard

The parent record must be of type `fixed` — the controller hard-filters to that type. Visiting `/admin/marketing/discounts/products/<some-non-fixed-id>` returns 404. (Quantity discounts have no products page; their tiers are on the discount form.)

### Product picker searches the whole catalog

The Add-modal product picker queries `/admin/api/core/products/search` with the typed string, by product name, SKU or barcode. It finds inactive and unpublished products too; it leaves out wallet and gift-card items.

### Product picker search source

The same `/admin/api/core/products/search` endpoint is used by other discount targets, cart rules, and the campaign builder — so the merchant sees a **consistent product result set across all of marketing**.

### Per-render price formatting

The list cell renders `discount.price` (cents) ÷ 100 as `final`, and `discount.price + discount.save` (cents) ÷ 100 as `total`. The `save` column is precomputed at save time — see [[discounts-products-save-replace]] for the exact formula — so this page does no per-render computation. Saving the product recalculates the saving automatically while the discount is active and unexpired.

### Single-source-of-truth for the product's discount data

The list endpoint returns rows grouped by `product_id` (one row per product, not per variant) — the single row carries an `items` array with each variant's `discount_price`. The edit-modal opens this same payload (via the per-product `getProductDiscountById` endpoint), so the list and the modal stay in sync without a separate per-variant fetch.

### Plan-gating

Creating a Fixed discount is checked by plan on create only — see [[fixed-discount-plan-gates]]. This page itself has no plan check.

### Permission

The page and all CRUD endpoints are scoped under the standard `marketing.discounts` permission.

### Default fixed discount (auto-created)

The discount block on the product form (the **On Sale** switch, a **Discount** as an amount or a percent, and the resulting sale price, see [[products-variants-matrix]]) does not create a discount of its own. It writes into one Fixed discount, **Default Fixed Discount**, created on first use (active, no end date) and reused from then on. The Admin GraphQL bulk sale-price action writes into it too.

- **A percent is turned into a price** before saving: the regular price minus that percent, rounded to the cent. The discount stores only the resulting fixed price per variant, so a later change of the regular price does not re-apply the percent.
- **Each save of the product form replaces** the product's prices in this discount with what the form shows; switching **On Sale** off removes them. A sale price not below the regular price is refused: *"The discounted price must be lower than the regular price!"* (BG *"Намалената цена трябва да е по ниска от редовната цена!"*).
- **It shows in the Discounts list** as *Default Fixed Discount* (type Fixed). Its **Active** switch there is greyed out; the bulk status action still switches it.
- **When it is inactive**, a price entered on the product form is still saved into it, without any warning, but the storefront never applies it. After a reload the form shows no discount, because it reads only active prices, and the next save of the product deletes the saved price. Switching the container back on brings back the prices still stored in it.

Merchants should not delete it; it is recreated on the next use, empty.

### Customer groups are copied when a product's prices are saved

When the parent Fixed discount has customer-group restrictions, the platform clones each variant row per group when a product's prices are saved here. This products-list page doesn't expose customer groups — it inherits them from the parent. Changing groups on an existing Fixed discount does not change products already attached until each is edited. The merchant who wants to set per-customer-group prices must rely on Fixed discount's customer-group fan-out — they cannot override per-product per-group from this UI.

### Per-variant date and discount_id inheritance

When inserting variant rows, missing `date_start`, `date_end`, and parent-discount linkage are auto-filled from the parent discount before insert. Editing the parent discount's date range automatically updates every variant row's dates via the underlying model's update hook — the merchant doesn't have to re-save each product. See [[discounts-products-save-replace]] for the row-write details.

### A price above the catalog price fails the save

A price above the variant's catalog price fails the whole save with *"Price must be at least 1 and less than <variant.price>"*; nothing is dropped. A price equal to the catalog price is saved with no saving. See [[discounts-products-save-replace]].

## Related

- [[marketing-discounts-products]] — hub.
- [[marketing-discounts-fixed]] — parent discount; customer groups + date window are set here.
- [[discounts-products-save-replace]] — the row-write details that the inheritance rules depend on.
- [[discounts-products-fields]] — error messages referenced inline.
- [[customers-custom-groups]] — customer-group fan-out trigger.
- [[products-products]] — the products the picker searches.
- [[marketing-discounts]] — `discount_fixed` plan gate.
- [[settings-hooks]] — `discount.updated` fires when the discount record itself is saved, not on product changes here.

## Open questions

No outstanding questions.
