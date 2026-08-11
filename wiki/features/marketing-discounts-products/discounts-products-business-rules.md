---
type: feature
nav_path: "Marketing → Discounts → Products → Business rules"
route_name: discounts-products
route_path: /admin/marketing-new/discounts/products/:id
aliases: ["Discount products business rules", "Fixed discount type guard", "Default fixed discount singleton", "Customer-group fan-out for discount products", "MSRP save EUR display", "Picker only active products", "Бизнес правила за продукти в отстъпка"]
tags: [marketing, discounts, fixed, products, business-rules, msrp, customer-groups, plan-gates]
plan_gates: ["discount_fixed"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

# Discount products — business rules & edge cases

> Part of [[marketing-discounts-products]]. See the hub for the list view, modal flow, fields, and save semantics.

## Purpose

This page catalogues the **cross-cutting rules** that affect what the merchant sees on the Discount products page but don't fit cleanly into list, modal, fields, or save-flow scopes: the discount-type guard, the picker's search source, the MSRP-mode "Save X EUR" display, the default Fixed discount singleton, customer-group + date inheritance from the parent discount, plan-gating, and permissions.

These rules are the most common source of support tickets where the merchant says "I don't understand why my discount shows X" — most of the time the answer lives here, not in the modal or list views.

## Where to find it

The rules apply to Marketing → Discounts → (click **Products** on a Fixed-type discount row) → list at `/admin/marketing-new/discounts/products/:id` and its modal. Several of them depend on parent-discount settings that live on the [[marketing-discounts-fixed]] edit form.

## What the merchant can do here

Most of these rules describe behaviour the merchant **inherits** rather than controls directly. The merchant influences them by:

- Choosing the parent Fixed discount's MSRP mode + customer-group restrictions on the parent edit form.
- Choosing the parent Fixed discount's date window.
- Activating products in the catalog before adding them to the discount.
- Choosing a plan that includes `discount_fixed`.

## Settings & fields

This page documents behaviour driven by parent-discount settings (MSRP mode, customer groups, dates) and store-level settings (plan, permissions). Its own fields are documented on [[discounts-products-fields]].

## Business rules

### Discount-type guard

The parent record must be of type `fixed` — the controller hard-filters to that type. Visiting `/admin/marketing-new/discounts/products/<some-non-fixed-id>` returns 404. (Quantity discounts have their own products-management UI; this page is shared under the same modern Vue route name, but the backend rejects mismatched types.)

### Product picker only returns active products

The Add-modal product picker queries `/admin/api/core/products/search` with the typed string. That endpoint scopes by default to active / published products. Disabled or unpublished products won't appear in the picker — the merchant has to **activate the product first** before they can add it to a Fixed discount. This is also why a merchant who deactivates a product later still sees it on the discount's list (the row stays attached) but cannot re-add it via the picker.

### Product picker search source

The same `/admin/api/core/products/search` endpoint is used by other discount targets, cart rules, and the campaign builder — so the merchant sees a **consistent product result set across all of marketing**. A product that's missing from this picker is missing from all of them; the fix is on the product's status, not on the discount.

### Per-render price formatting

The list cell renders `discount.price` (cents) ÷ 100 as `final`, and `discount.price + discount.save` (cents) ÷ 100 as `total`. The `save` column is precomputed at save time — see [[discounts-products-save-replace]] for the exact formula — so this page does no per-render computation. A merchant who changes the catalog price after saving the discount will NOT see the "Save X EUR" update until the discount row is re-saved.

### Single-source-of-truth for the product's discount data

The list endpoint returns rows grouped by `product_id` (one row per product, not per variant) — the single row carries an `items` array with each variant's `discount_price` and `msrp_price`. The edit-modal opens this same payload (via the per-product `getProductDiscountById` endpoint), so the list and the modal stay in sync without a separate per-variant fetch.

### Plan-gating

This page inherits the `discount_fixed` plan feature from the parent Fixed discount. Merchants on plans without Fixed discounts can't reach this page (the parent discount type can't be created — see [[marketing-discounts]] for the gate).

### Permission

The page and all CRUD endpoints are scoped under the standard `marketing.discounts` permission.

### MSRP-mode "Save X EUR" reflects MSRP delta, not catalog delta

When the parent Fixed discount has MSRP mode on, the savings shown on the storefront ("Save X EUR") is computed as `msrp_price − fixed_price` — **NOT** as `catalog_price − fixed_price`. So a product with catalog 800 EUR, MSRP 1,000 EUR, fixed 700 EUR displays "Save 300 EUR" — even though the customer was previously seeing the catalog 800 EUR price (true saving is 100 EUR). Merchants should communicate this clearly in their copy to avoid surprises. See [[marketing-discounts-fixed]] for the full MSRP rule and the `msrp = 1` flag.

### Default fixed discount (auto-created)

The platform has a concept of a **default Fixed discount** — a singleton Fixed discount marked with `for_products = yes` meta, auto-created on first need. Used as a fallback container for products discounted ad-hoc (e.g., via inline price edits on the product page). Most merchants never see this; it's an internal helper. A merchant who notices an unexpected Fixed discount appearing in their list is usually seeing this auto-created singleton — they shouldn't delete it manually.

### Customer-group fan-out happens at the parent discount's save, not here

When the parent Fixed discount has customer-group restrictions, the platform clones each variant row per group at the **parent's** save time. This products-list page doesn't expose customer groups — it inherits them from the parent. The merchant who wants to set per-customer-group prices must rely on Fixed discount's customer-group fan-out — they cannot override per-product per-group from this UI.

### Per-variant date and discount_id inheritance

When inserting variant rows, missing `date_start`, `date_end`, and parent-discount linkage are auto-filled from the parent discount before insert. Editing the parent discount's date range automatically updates every variant row's dates via the underlying model's update hook — the merchant doesn't have to re-save each product. See [[discounts-products-save-replace]] for the row-write details.

### `fixed_price >= variant.price` is silently dropped

A row that fails the *"strictly cheaper than catalog"* check on save is **skipped without an error message**. The merchant sees the saved discount with FEWER variants than they entered. See [[discounts-products-save-replace]] for the full sequence — combined with the full-replace semantics, this is the single most common cause of "my discount lost variants" tickets.

## Related

- [[marketing-discounts-products]] — hub.
- [[marketing-discounts-fixed]] — parent discount; MSRP mode + customer groups + date window are set here.
- [[discounts-products-save-replace]] — the row-write details that the silent-drop and inheritance rules depend on.
- [[discounts-products-fields]] — error messages referenced inline.
- [[customers-custom-groups]] — customer-group fan-out trigger.
- [[products-products]] — product activation rule (only active products appear in the picker).
- [[marketing-discounts]] — `discount_fixed` plan gate.
- [[settings-hooks]] — `discount.updated` webhook on each save / toggle / delete.

## Open questions

No outstanding questions.
