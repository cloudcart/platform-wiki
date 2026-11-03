---
type: feature
nav_path: "Products → Categories → List & Organize tabs"
route_name: categories.settings
route_path: /admin/products/categories
aliases: ["Categories list", "Categories organize", "Category tree view", "Drag-drop category tree", "Категории — списък", "Категории — подреждане"]
tags: [products, categories, taxonomy, navigation, tree]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[products-categories]]. See the hub for the other aspects (edit modal, hierarchy rules, cart restrictions, SEO/taxonomy, deletion rules, JSON-API/validation).

# Categories — List & Organize tabs

## Purpose

The two tabs at the top of the Categories screen split day-to-day taxonomy work into two distinct modes: the **List** tab is a paginated table for create / edit / delete / filter / bulk-select of individual categories, and the **Organize** tab is a drag-and-drop tree for **reordering** and **re-parenting** the hierarchy as a whole. Both tabs share the same +Add category button in the page header and open the same edit modal — what differs is the read-side: scan-by-row vs see-the-shape-of-the-tree.

## Where to find it

Sidebar → Products → **Categories**.

Tab switcher in the page header — **List** (default) and **Organize**. Route stays `/admin/products/categories` for both; the tab state is local.

## What the merchant can do here

### List tab (default)
- See a paginated table of all categories with **Name**, **Products count**, **Properties count**, **Taxonomy** badge, and per-row actions (Edit, Delete).
- **Expand a row** to see the breadcrumb path of parent categories — e.g., `Electronics → Phones → Smartphones`. For a top-level category the expander shows *"This category is set as a primary one"*.
- **Filter** by **Has products** (yes/no), **Has properties** (yes/no), **Has taxonomy** (yes/no).
- Sort by name, paginate, bulk-select.
- **Bulk-delete** via the standard delete bulk action (subject to the deletion-block rules in [[products-categories-deletion-rules]]).
- Click +Add category to open the create modal — see [[products-categories-edit-modal]].
- Click any row's Edit to open the edit modal pre-filled with the category data.
- Click the **Taxonomy** column cell to open the focused standalone Define-taxonomy modal — see [[products-categories-taxonomy]].

### Organize tab
- See the full category hierarchy as a **drag-and-drop tree**.
- Drag any category to a new position to reorder, OR drag onto another category to make it a subcategory.
- **Search by category name** via a dropdown in the page header — clicking a result highlights and scrolls to that category in the tree.
- Click any node to edit it (same edit modal as on the List tab).
- Saves the new arrangement on drop. Validation errors revert the visual move and surface an inline error — see Business rules below and the full rule set in [[products-categories-hierarchy-rules]].

### What the merchant CANNOT do here
- Bulk-edit categories' fields (rename multiple, set the same parent on multiple) — no bulk action beyond delete.
- Merge categories (reassign all products from one to another) — products must be moved individually.
- See WHICH products are in each category from this page — the Products-count cell is informational only (not a navigation link). To see / edit the products, use [[products-products]] with a category filter.

## Settings & fields

### List tab — table columns

| Column | Notes |
|--------|-------|
| **Name** | Click to edit. Sortable. Clicking the row toggles the breadcrumb expansion. |
| **Products** (`real_products_count`) | Count of products directly assigned to this category. |
| **Properties** (`properties_count`) | Count of properties (specifications) attached to this category — see [[products-property]]. |
| **Taxonomy** (`taxonomy_id`) | Badge with the assigned Google Shopping taxonomy node, or "—" if not set. Click opens the standalone taxonomy modal. |
| **(actions)** | Edit + Delete buttons. |

### Organize tab — per-row controls on the tree

Each tree node renders:
- **Expand/collapse chevron** (only when the category has children) — toggles the inline subtree visibility.
- **Drag handle** (6-dot grip icon) — initiates the drag.
- **Category name** — clickable to open the edit modal.
- **Subcategories badge** — shows `{N} Subcategories` (or "1 Subcategory") when the category has any direct children.
- **Edit icon** (pencil) — opens the edit modal pre-filled.
- **Delete icon** (xmark) — opens an inline delete confirmation popover labelled *"Remove category?"*.

### Drop targets shown on hover (Organize tab)

While dragging a category, three drop-zone indicators light up around the hovered target row:
- **Before** — a thin highlight line above the target row → moved category becomes a sibling immediately above it.
- **After** — a thin highlight line below the target row → moved category becomes a sibling immediately below it.
- **Inside** — the target row is outlined with a thick lavender border → moved category becomes the target's first child.

Releasing the drag sends a single backend call with the target's ID + position (`before` / `after` / `inside`). A loader overlay covers the affected row(s) until the response comes back.

## Business rules

### Tab state is local
Switching tabs does not change the route — `/admin/products/categories` covers both. Reloading the page returns to the List tab. The Organize tab fetches the full tree on activation; the List tab fetches the current page of rows.

### Drag-drop drop persists immediately, but is reverted on validation failure
Every drop fires a single backend call. If validation fails (depth > 6, dropped onto self / own descendant, sibling name clash, etc.), the visual move is **reverted** and an inline error surfaces on the affected row. See [[products-categories-hierarchy-rules]] for the full validation catalogue.

### Sibling renumbering after every drop
On a successful drop, the platform **renumbers all siblings** of both the source and destination parent so `order` values stay contiguous (1, 2, 3, ...) — no gaps after many drops. (verify exact behaviour on partial failures.)

### "Categories were modified" flag triggers tree refetch
Saving from the edit modal sets a flag that the Organize tab's tree-reorder reload uses to know when to refetch — so re-opening the Organize tab after an edit shows the latest tree (verify).

### Permission
The Categories screen (both tabs) requires the products / categories permission section to be granted on the merchant's account. Moderators without it cannot see the Categories sidebar entry.

## Related

- [[products-categories]] — hub.
- [[products-products]] — products are assigned to categories from the product editor; use a category filter to see products in a category.
- [[products-property]] — properties (specifications) attached to categories.
- [[apps-csv-import]] — bulk-import categories from a spreadsheet (separate path from this screen).

## Open questions

- Exact "categories were modified" flag wording and trigger conditions (verify).
- Whether sibling-renumbering runs on transactional failure rollback or only on success (verify).
