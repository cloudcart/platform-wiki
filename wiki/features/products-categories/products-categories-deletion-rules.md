---
type: feature
nav_path: "Products → Categories → Deletion rules"
route_name: categories.settings
route_path: /admin/products/categories
aliases: ["Category delete", "Cannot delete category", "Discount cascade on delete", "category path-rebuild", "Категория — изтриване"]
tags: [products, categories, taxonomy, deletion, cascade, support]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[products-categories]]. See the hub for the other aspects (list & organize, edit modal, hierarchy rules, cart restrictions, SEO/taxonomy, JSON-API/validation).

# Categories — Deletion rules

## Purpose

Everything the platform does (and refuses to do) when the merchant tries to delete a category — the "no auto-reassign" safety rule, the XML-import lock, the discount-cascade side effect, the orphaned-image quirk, and the CloudCart-staff-only `category:path-rebuild` support tool for fixing drift between the live `parent_id` chain and the materialised `path` column. These are the rules behind the most common deletion-related support tickets: *"why won't this category delete?"* and *"the breadcrumbs are wrong for this category."*

## Where to find it

- Sidebar → Products → **Categories** → List tab → per-row Delete action (or bulk Delete).
- Sidebar → Products → **Categories** → Organize tab → tree-node Delete icon → inline *"Remove category?"* confirmation popover.

There is no merchant-facing UI for the path-rebuild support tool — it is invoked by CloudCart staff via a support ticket.

## What the merchant can do here

- Delete a single category that has **no products** (and no descendant subcategory has products), no blocking XML import tasks, via the row Delete button or the tree Delete icon.
- Bulk-delete multiple categories via the List tab's bulk-delete action (each one must individually pass the same checks).
- Reassign products to another category before deletion (one product at a time, from the [[products-products]] editor — there is no bulk reassign on this screen).
- Open a support ticket if storefront breadcrumbs or category-subtree search results look wrong (path-column drift symptom — see below).

### What the merchant CANNOT do here

- Delete a category with products still inside (or with populated descendant subcategories) — the platform does NOT silently re-parent products.
- Bulk-reassign products from one category to another — must edit each product individually, or use [[apps-csv-import]].
- Recover a deleted category — deletion is permanent; the cascade-deleted discounts (see below) are also permanent.

## Settings & fields

The delete action has no configurable fields — it is a confirm-and-go action. The error messages it can surface:

| Trigger | Error message |
|---------|--------------|
| Category has products (or any descendant has products) | *"Cannot delete category. The category has products"* |
| Bulk delete — one or more categories blocked | *"Some categories still has products: Cat A; Cat B; Cat C"* |
| Active XML import task references the category | *"Cannot delete: the category has XML import tasks: {names}"* |

## Business rules

### Deletion is BLOCKED when products remain — no auto-reassign

Deleting a category with **any products inside** is REJECTED with the error *"Cannot delete category. The category has products"*. The platform **does NOT silently re-parent products** to the deleted category's parent — the merchant must first clear every product (move it to another category, or delete it) before delete succeeds.

The check covers products in **any descendant subcategory** too: deleting "Electronics" with empty "Electronics" but populated "Electronics → Phones" still fails.

**Bulk-delete** uses the same block but reports all blocked names in one error: *"Some categories still has products: Cat A; Cat B; Cat C"*.

### XML-import lock

Deletion is also rejected when any **active XML import task** (see [[apps-csv-import]] / XML imports) is using the category — error *"Cannot delete: the category has XML import tasks: {names}"*. The merchant must wait for the import to finish or remove the category from the task.

### Discount cascade — discounts scoped to the category are auto-deleted

When a category delete DOES succeed, **all discounts scoped to that category (and its descendants) are also deleted automatically** — see [[marketing-discounts]]. This is irreversible. Merchants who delete category branches with active discounts on them should expect those discounts to disappear silently.

### Category image is NOT auto-deleted (orphan)

The uploaded category image stays in the file manager as orphan storage — see [[settings-files]]. The merchant must clean up orphan images manually if storage usage is a concern.

### URL-handle 301 redirect entry is NOT auto-removed (verify)

The 301 redirect history entry that was created when the category's URL handle changed is **not** automatically cleaned up on category delete (verify) — the redirect may continue to serve to the now-nonexistent destination (verify storefront behaviour).

### Side effects on successful delete

- The category record is removed.
- The materialised `path` table rows for this category and (via cascade) its descendants are removed.
- Sibling `order` values are renumbered contiguously.
- Search index re-build is queued (storefront search reflects the change after the queue processes).
- Storefront cart cache is flushed.
- Discounts scoped to the category cascade-delete (per above).

### Same delete rules apply on the JSON-API v2 path

DELETE through [[api-categories]] hits the same blocks (products-still-present, XML-import-lock) and returns 422 with the same error messages. See [[products-categories-api-validation]].

### Permission

Deleting a category requires the products / categories permission section. Moderators without it see the Categories sidebar entry only if they have read access; they cannot delete.

### Path-column drift — `category:path-rebuild` (CloudCart-staff-only)

The `category` table stores each category's full ancestor path in a `path` column (e.g., `1/14/29`) so the tree can be traversed efficiently without recursive queries — see [[products-categories-hierarchy-rules]] for the path mechanics. The platform updates this column automatically on every create / parent-change / delete.

In rare cases — bulk DB-level moves from a migration, a corrupted partial-save, an interrupted Magento/Shopify import — the `path` values can drift from the actual `parent_id` chain. Symptoms:

- Categories appear under the wrong tree position.
- Breadcrumbs are wrong.
- Storefront-search filtering by category subtree returns the wrong set.

**CloudCart-staff-only repair tool**: an artisan command walks every category, recomputes the path from the live `parent_id` chain, and writes it back. Safe to run on a live store (read-then-write per category, no schema changes). **Merchants cannot trigger it from the admin UI** — they should open a support ticket if the symptoms above appear.

## Related

- [[products-categories]] — hub.
- [[products-categories-list-organize]] — where the row + bulk delete actions live.
- [[products-categories-hierarchy-rules]] — the `path` column mechanics that the support tool repairs.
- [[products-categories-api-validation]] — same delete rules on JSON-API v2.
- [[products-products]] — where products must be re-categorised before a category delete can succeed.
- [[marketing-discounts]] — discounts scoped to the deleted category are cascade-deleted.
- [[settings-files]] — where the orphaned category image lives after delete.
- [[apps-csv-import]] — XML imports lock category deletion while active.

## Open questions

- Whether the URL-handle 301 redirect history entry is cleaned up on category delete (verify storefront behaviour).
- Exact behaviour when a category is deleted while a discount scoped to it is **active on live carts** — does the discount drop from those carts at the next storefront request, or only on next checkout (verify).
