---
type: feature
nav_path: "Products → Products → Bulk actions"
route_name: products-index.new
route_path: /admin/products/products-new
aliases: ["Product bulk actions", "Products mass tools", "Bulk publish products", "Bulk duplicate products", "Bulk change vendor", "Bulk tag products", "Масови действия върху продукти"]
tags: [catalog, products, bulk, mass-actions, list]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[products-products]]. See the hub for the other aspects (list view, editor, variants matrix, AI content, change log, known issues).

# Products — Bulk actions

## Purpose

The bulk-action menu on [[products-list-view]] lets the merchant operate on **many products at once** with a single API call — flipping flags, reassigning category / vendor, tagging, setting quantity, sorting, changing status, or deleting. Without bulk actions, large catalog rearrangements (e.g. *"hide every Draft from the storefront before Black Friday"*) would require row-by-row editing.

This aspect documents:

- The full bulk-action catalogue.
- The bulk-action sub-popup mechanics — what input each action collects, and what guards block it.
- The two draft-without-category guards specific to **Publish**.
- The bulk duplicate verified specifics.

## Where to find it

[[products-list-view]] → multi-select rows via the leftmost checkbox column → bulk-action menu appears in the table header (replaces the column header). The menu is dismissed when no rows are selected.

## What the merchant can do here

### Bulk-action catalogue

| Action | What it does |
|--------|--------------|
| **Publish** | Sets all selected to published. If any are drafts (no category yet), opens a publish-confirmation popup. See "Draft-without-category guards" below. |
| **Unpublish** | Sets all selected to unpublished. |
| **Duplicate** | Creates copies of all selected products. See "Bulk duplicate verified specifics" below. |
| **Mark as new** | Toggles the NEW badge ON. |
| **Remove marked as new** | Toggles the NEW badge OFF. |
| **Show in store** | Sets the Hidden flag OFF. |
| **Hide from store** | Sets the Hidden flag ON (kept in admin but invisible to customers). |
| **Activate track quantity** | Turns on stock tracking. Opens a popup to set the starting quantity. |
| **Deactivate track quantity** | Turns off stock tracking. |
| **Set product tags** | Opens a popup to assign tags to all selected. |
| **Change main category** | Opens a popup to reassign all selected to a different primary category. |
| **Change vendor** | Opens a popup to reassign all selected to a different vendor. |
| **Sort number** | Opens a popup to set a specific sort order across selected. |
| **Change product status "Available"** | Opens a popup to set product status to a specific Available value (custom statuses — see [[products-statuses]]). |
| **Change product status "Out of stock"** | Same but for Out-of-stock statuses. |
| **Delete** | Confirmation modal *"Are you sure you want to delete? Caution: This action cannot be undone."* Permanent. See [[products-known-issues]] for the cascade. |

### Bulk-action sub-popup

Many list-page bulk actions don't apply immediately — they open a small **bulk-action popup** that captures one input value, then applies it to all selected products in a single API call:

| Bulk action type | Popup field |
|------------------|-------------|
| **Set product tags** | Multi-tag autocomplete (Includes / Does not include) + a comma-separated paste shortcut (paste `a,b,c` → 3 tags added at once). |
| **Change main category** | Single-select category from autocomplete. |
| **Change vendor** | Single-select vendor from autocomplete. |
| **Sort number** | Numeric input (min 0). |
| **Change product status "Available"** | Single-select from [[products-statuses]] (in-stock statuses). |
| **Change product status "Out of stock"** | Single-select from [[products-statuses]] (out-of-stock statuses). |
| **Activate track quantity** | Numeric quantity input — the bulk-action enables tracking AND sets the initial quantity to this value across selected. |
| **Publish** | No input — but shows a warning info-box (see below) and silently drops uncategorised products from the batch. |

## Settings & fields

### Draft-without-category guards (Publish only)

The **Publish** bulk action has special handling for drafts without a category:

- If SOME selected products are drafts without a category → the popup shows a warning info-box *"Some of the products are with NO SELECTED CATEGORY, so they cannot be published via the mass tools!"* and silently drops the uncategorised products from the batch. The categorised ones publish normally.
- If ALL selected products lack a category → the popup blocks the action entirely with *"All of the products don't have selected category. You can not publish them via the mass tools"*. The merchant must assign categories first (via the editor or via the **Change main category** bulk action).

This prevents publishing uncategorised products that would never be findable on the storefront.

### Confirmation modal for Delete

The **Delete** bulk action shows a confirmation modal *"Are you sure you want to delete? Caution: This action cannot be undone."* Hard delete, irreversible — see [[products-known-issues]] for what cascades.

## Business rules

### Bulk duplicate — verified specifics

When duplicating a product (single via per-row action, or bulk via this menu):

- Copy's name = original name + `"-Copy"` (truncated at 191 chars to fit).
- Copy's URL handle = original handle + `"-Copy"` (truncated at 191 chars).
- Copy is set to **Draft** (`active = no`) — never auto-publishes. This is the safe default: a bulk-duplicate doesn't accidentally republish.
- Copy carries `app_import = duplicate_product-<original-id>` — searchable via the [[products-list-view|Imported with]] filter to find or undo duplications.
- Variants are deduplicated by their `(v1, v2, v3)` combination — older databases with duplicate variant rows get cleaned up in the copy.
- **Categories, tags, tabs (custom info sections), files, brand-model links, smart-collection memberships, and category-property values are all copied.**
- Product files are copied directly server-side in a single operation, so duplicating 50 files takes a fraction of a second.

The new product needs the merchant to edit it before going live.

### Per-action side-effects fire on every product touched

Each bulk action runs the **same save-time side-effects** as a single-product save for every product in the batch:

- The search index re-indexes each affected product.
- Smart-collection re-evaluation runs for each.
- Storefront cache invalidates for each.
- `product.updated` webhook fires for each — receivers must be ready for the chatty volume on large bulk operations.

See the "Side effects on save" section on [[products-products]] for the full coverage rule (admin-panel-only webhooks vs always-on search-sync).

### Moderator restrictions apply

A moderator with restricted access (per [[settings-staff]]) can only run bulk actions on products in their permitted categories. The list view filters their visible products automatically, so a bulk select-all only covers the permitted slice.

### Bulk delete cascade is identical to single delete

Bulk **Delete** cascades the same way as single deletion — see [[products-known-issues]] for the full cascade table (files, variants, digital records, stored file folders, bundle deactivation, discount rules, quantity discounts, change log).

## Related

- [[products-products]] — hub.
- [[products-list-view]] — where bulk-action multi-select lives.
- [[products-known-issues]] — bulk-delete cascade, hard-delete irreversibility.
- [[products-statuses]] — drives the Change-status bulk popups.
- [[products-categories]] — drives Change-main-category.
- [[products-vendors]] — drives Change-vendor.
- [[settings-hooks]] — `product.updated` webhook fired per touched product.
- [[settings-staff]] — moderator restrictions that scope the visible (and therefore selectable) products.

## Open questions

None.
