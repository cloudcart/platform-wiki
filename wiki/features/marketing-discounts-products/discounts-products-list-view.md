---
type: feature
nav_path: "Marketing → Discounts → Products → List view"
route_name: discounts-products
route_path: /admin/marketing-new/discounts/products/:id
aliases: ["Discount products list view", "Discount products row actions", "Discount products bulk actions", "Discount products filter sort", "Списък с продукти в отстъпката", "Масови действия върху продукти в отстъпка"]
tags: [marketing, discounts, fixed, products, list-view, bulk-actions]
plan_gates: ["discount_fixed"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

# Discount products — list view, row actions, bulk actions

> Part of [[marketing-discounts-products]]. See the hub for the modal flow, fields, save semantics, and business rules.

## Purpose

The list view is the **first thing the merchant sees** when they click **Products** on a Fixed-type discount row. It shows every product currently attached to the discount with its original and discounted prices, lets the merchant act on individual rows (open the edit modal, toggle active, remove) and on selections (bulk-toggle status, bulk-delete), and offers the standard filter / sort / paginate controls.

## Where to find it

Marketing → Discounts → (click **Products** on a Fixed-type discount row) → list view loads at `/admin/marketing-new/discounts/products/:id`. The breadcrumb reads "Marketing → Discounts → Products".

## What the merchant can do here

- **See every product attached** to this discount, paginated and sortable, with: **Product Name** (image thumbnail + name, clickable to open the edit modal, plus a *"View in store"* tooltip linking to the storefront page), **Price** (original price struck-through over the new fixed price, with the EUR-to-EUR dual display when active), **Active** toggle per product, **Remove** action per product.
- **Click the product name or image** — opens the [[discounts-products-modal-flow|Discount product modal]] pre-filled with the existing per-variant prices.
- **Toggle a product's active state inline** via the row switch — POSTs to `/admin/api/core/discounts/products/{discount_id}/status` with the product id and `status: yes|no`. Toast on success: *"Status changed successfully"*.
- **Remove a single product** — DELETEs to `/admin/api/core/discounts/products/{discount_id}?ids[product_ids][0]={product_id}`. Removal is immediate (no soft-delete here). Toast: *"Removed successfully"*.
- **Bulk-toggle** via checkbox selection + action bar — *"Set status active"* / *"Set status unactive"*. Both POST to the same status endpoint with the selected product ids.
- **Bulk-delete** via checkbox selection + the table's default delete bulk-action — DELETEs to the same endpoint with all selected `product_ids[]`.
- **Filter** by Active = Yes / No.
- **Sort** by Price (ascending / descending) and Active (toggle column header).
- **Paginate** with the standard table controls.

## Settings & fields

### List columns

| Column | What it shows |
|--------|---------------|
| **Product Name** | Product image thumbnail + name. Image links to the storefront page (tooltip *"View in store"*). Name link opens the edit modal. |
| **Price** | Two lines, formatted via `moneyFormat`: top line = original price (struck-through) and the new fixed price (e.g., `999 EUR / 799 EUR`); second line shows the EUR-to-EUR dual display when EUR-display is active for the store. |
| **Active** | Per-row toggle — green = active, grey = inactive. Inactive products keep the discount attachment but the storefront skips applying it. |
| (Remove) | Per-row remove action — immediately deletes the product from the discount. |

### List filters

| Filter | Options |
|--------|---------|
| **Active** | Yes / No |

### List sorting

Sortable columns: **Price** (ascending / descending), **Active**.

### List bulk actions

| Action | Label | Effect |
|--------|-------|--------|
| `active` | "Set status active" | Toggles selected products' attachment to active. Toast: *"Status set to active successfully"*. Error: *"Error while setting the status"*. |
| `unactive` | "Set status unactive" | Toggles selected products' attachment to inactive. Toast: *"Status set to unactive successfully"*. Error: *"Error while setting the status"*. |
| `delete` | (Default delete) | Removes selected products from the discount. |

## Business rules

- **Row-level Active is per-product, but writes per-variant.** Toggling Active on one row flips the `active` column on **every variant row** for that product under this discount — see [[discounts-products-save-replace]] for the row-fan-out details.
- **Remove is immediate, not soft-delete.** Once the merchant confirms the remove, the variant rows are deleted; there is no "Restore" undo. Re-adding the product creates fresh rows.
- **List read groups per product.** The list endpoint returns one row per `product_id` (even when the product has multiple variants with different fixed prices), with an `items` array carrying each variant's `discount_price` and `msrp_price`. The modal opens that same payload — see [[discounts-products-modal-flow]].
- **Per-render price formatting is precomputed.** The list cell renders `discount.price` (cents) ÷ 100 as the final price and `discount.price + discount.save` (cents) ÷ 100 as the original. The `save` column is precomputed at save time — this page does no per-render computation.
- **Status toggle + delete both fire two events** on every affected variant row: `ProductUpdated` (listing-engine rebuild) and the search re-index (the search index re-index). See [[discounts-products-save-replace]] for the full event chain.

## Related

- [[marketing-discounts-products]] — hub.
- [[discounts-products-modal-flow]] — clicking a row or **+ Add product** opens this modal.
- [[discounts-products-save-replace]] — the events fired on bulk-toggle / bulk-delete.
- [[marketing-discounts-fixed]] — parent Fixed discount; drives plan-gating and the type-filter.
- [[products-products]] — the products in the row are linked here.
- [[storefront-architecture]] — the search index re-index path that bulk actions trigger.

## Open questions

No outstanding questions.
