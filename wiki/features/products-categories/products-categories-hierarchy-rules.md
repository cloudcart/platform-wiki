---
type: feature
nav_path: "Products → Categories → Hierarchy rules"
route_name: categories.settings
route_path: /admin/products/categories
aliases: ["Category depth", "Category nesting", "Sibling uniqueness", "Tree drag-drop validation", "Materialized path", "category_path", "Категория — дълбочина", "Категория — родител"]
tags: [products, categories, taxonomy, hierarchy, tree, validation]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[products-categories]]. See the hub for the other aspects (list & organize, edit modal, cart restrictions, SEO/taxonomy, deletion rules, JSON-API/validation).

# Categories — Hierarchy rules

## Purpose

The structural rules the platform enforces on the category tree: the hard 6-level depth cap, the sibling-scoped name uniqueness rule, the full catalogue of drag-drop drop validations, the materialised-path table that makes deep storefront breadcrumbs fast, and the atomicity guarantee on every reorder. These are the rules the merchant hits as *"why was my drag rejected?"* errors and as *"why is my category showing up in the wrong place?"* support tickets.

## Where to find it

Sidebar → Products → **Categories** — on every drop in the Organize tab and on every Save in the Add / Edit modal. No dedicated UI; the rules surface as **inline validation errors**.

## What the merchant can do here

- Nest categories up to **6 levels deep**.
- Re-parent a category by dragging it onto another category (Organize tab) or by changing the **Parent category** dropdown (edit modal).
- Reorder siblings within the same parent by dragging on the Organize tab.
- Reuse the same name across different sibling groups (e.g., "Shoes" under "Men" and "Shoes" under "Women" — both allowed).

### What the merchant CANNOT do here

- Nest more than 6 levels — drops are rejected.
- Drop a category onto itself or one of its own descendants — rejected (would create a circular tree).
- Have two categories with the same name under the same parent — rejected on save and on drag.

## Settings & fields

There is no dedicated configuration surface for hierarchy rules — they apply to every category create / edit / drag. The fields that drive them are:

| Field | Where it lives | What it controls |
|-------|----------------|-------------------|
| **Parent category** | Add / Edit modal — see [[products-categories-edit-modal]] | The merchant's chosen `parent_id`. Empty = top-level. |
| **Category name** | Add / Edit modal | Validated for uniqueness within the parent's sibling group. |
| **Drop position** | Organize tab drag — see [[products-categories-list-organize]] | `before` / `after` (sibling of target) or `inside` (first child of target). |

### Internal `path` column (informational)

The `category` table stores each category's full ancestor path in a `path` column (e.g., `1/14/29`) so the tree can be traversed efficiently without recursive queries. The platform updates this column automatically on every create / parent-change / delete. Merchants never see or set this directly; it appears here because the **path-rebuild support tool** (see [[products-categories-deletion-rules]]) operates on it.

## Business rules

### Hierarchy depth — hard cap of 6 levels

The merchant can nest categories up to **6 levels deep**. Attempting to drag a category into a position that would create a 7-level subtree is rejected at the Organize-tab drop with an inline error *"Maximum nesting depth is 6"* (or *"Maximum depth is 6"*).

The platform calculates depth as `parent-count-from-root + max-child-depth-of-moved-subtree`, so moving a 3-level subtree under a 4-level parent (3+4 = 7) is blocked **even though each side alone fits the limit**. The XML import flow ([[apps-csv-import]] and XML imports) also truncates category trees that exceed 6 levels.

### Name uniqueness — scoped to siblings, not store-wide

Two categories can share the same name AS LONG AS they have different parents. *"Shoes"* under *"Men"* and *"Shoes"* under *"Women"* is allowed. *"Shoes"* twice under the same parent (or two top-level *"Shoes"*) is rejected at save with *"Category name is already taken"* (or *"This name is already taken"* on the older form). The rule applies on create, rename, and on tree-drag re-parenting.

The validation runs through a custom `name_available` validator scoped by `parent_id`.

### Tree drag-drop validations beyond depth

The Organize tab's drag-drop fires backend validations on every drop:

- **Cannot drop a category onto itself** — rejected with *"Target category cannot be the same as moved"*.
- **Cannot drop a category onto one of its own descendants** — rejected with *"Target is a child of moved"* (prevents circular trees).
- **Cannot drop onto a sibling-group that already has a category with the same name** — rejected with the name-taken error.
- **Position** must be `before`, `after`, or `inside` — `before`/`after` re-parents the moved category as a sibling of the target; `inside` places it as the first child.
- After every drop, the platform **renumbers all siblings** of both the source and destination parent so `order` values stay contiguous (1, 2, 3, ...) — no gaps even after many drops.

A loader overlay covers the affected row(s) until the response comes back; validation errors revert the visual move and surface an inline error.

### Tree-reorder atomicity

Every drag-drop drop runs inside a database transaction with these steps:

1. Validate the move (target exists, not self, not own descendant, depth ≤ 6, name unique in sibling group).
2. Bump sibling `order` values to make room.
3. Update the moved category's `order` + `parent_id`.
4. Renumber all siblings of the OLD and NEW parent contiguously.
5. Rebuild the materialised paths for the moved subtree.

A failure at any step rolls the whole drop back — the merchant sees the tree unchanged and an inline error.

### Materialised-path table (`category_path`) supports fast subtree reads

Behind the scenes the platform maintains a separate path table that stores **every (descendant, ancestor, level)** triple. When a category is created, the parent's paths are copied + the self-path added (one row per ancestor level). When a category is **re-parented** via the Organize tab, the platform rebuilds the paths for the moved category AND **recursively for every descendant** — this is what makes deep moves feel snappy on the storefront breadcrumbs / filter sidebars (no recursive joins at read time).

The `path` column on the `category` row itself is kept in sync with this table. The CloudCart-staff-only `category:path-rebuild` artisan command can repair drift between the two — see [[products-categories-deletion-rules]].

### Same rules apply on the JSON-API v2 path

POST / PATCH through [[api-categories]] hits the same depth cap, sibling-uniqueness check, and circular-tree check — invalid payloads return 422 with the same error messages. See [[products-categories-api-validation]].

### Permission

The reorder + parent-change actions require the products / categories permission section.

## Related

- [[products-categories]] — hub.
- [[products-categories-list-organize]] — the Organize tab is where the drag-drop validations surface.
- [[products-categories-edit-modal]] — the Parent-category dropdown is the other re-parenting path.
- [[products-categories-deletion-rules]] — the path-rebuild support tool repairs `path`-column drift.
- [[products-categories-api-validation]] — the same validations apply on JSON-API v2.
- [[apps-csv-import]] — XML import flow also enforces the 6-level cap by truncation.

## Open questions

- Whether sibling-renumbering runs on **transactional rollback** (it should not, since the whole transaction is rolled back, but verify the success-then-renumber sequence).
- Exact error wording when a drop is rejected for **multiple** reasons simultaneously (does the platform return all violations or just the first?) (verify).
