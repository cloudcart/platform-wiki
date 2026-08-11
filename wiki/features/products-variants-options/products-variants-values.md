---
type: feature
nav_path: "Products → Variants → Values (per parameter)"
route_name: variants-index.new
route_path: /admin/products/variants
aliases: ["Variant values", "Variant options", "Per-parameter values", "Стойности на варианти", "Опции на параметър", "Enable Drag and drop sorting", "активиране на сортирането"]
tags: [products, variants, values, options, merge, sorting]
plan_gates: ["multi_variants"]
created: 2026-06-10
updated: 2026-07-09
source_count: 4
---

# Variants — values sub-page

> Part of [[products-variants-options]]. See the hub for the other aspects (list table, wizard, types, listing toggle, data model, API).

## Purpose

The per-parameter sub-page reached by clicking the Values count on a parameter row in [[products-variants-list-table]]. The Administrator adds, edits, reorders, and deletes option values for a single parameter (Red / Blue / Green for Colour; S / M / L / XL for Size), and opens the create-or-edit value modal (shape varies by parameter type). Consolidating duplicate values is a distinct, permanent operation covered on **[[products-variants-merge]]**.

## Where to find it

Sidebar → Products → **Variants** → click the **Values** count on a parameter row.

The breadcrumb appends the parameter name (e.g., "Products → Variants → Colour").

## What the merchant can do here

- See / manage the option values for the parameter.
- **Reorder values by drag-and-drop — but ONLY after clicking the "Enable Drag and drop sorting" button first** (top of the table). Until it is on, rows are static and dragging does nothing — this is the default, not a bug. See Business rules. Order controls display on the storefront variant picker and on the product editor.
- Click **Merge values** to consolidate values into a survivor — a permanent operation that also rewrites past orders and can move variants across parameters; full behaviour on [[products-variants-merge]].
- Click **+ Add variant value** to open the create-value modal. Fields depend on the parent parameter's type — see [[products-variants-types]].
- Click an existing value to open the same modal in edit mode (loads existing values via the find endpoint).
- For Image-sample values that already have a stored image, a **Delete image** link appears inside the modal.
- Bulk-delete values with confirmation (subject to "value in use" protection — see below).

## Settings & fields

### Per-parameter Values create-or-edit modal

Single-screen modal driven by the parent parameter's type:

| Parameter type | Fields shown |
|---|---|
| Select / Radio / 2D / Numeric alpha | Name only (max 150 chars; `numeric_alpha` rejects values not matching `<digits><letters>` pattern e.g. `36A`). |
| Image sample | Name + Image upload (jpg / jpeg / png / bmp / webp; checked against the store's storage quota at upload). |
| Color sample | Name + Color hex picker (default `#FFFFFF`, validated against `#[a-f0-9]{3,6}`). |

The same modal is used for Edit. Full per-type validation rules: see [[products-variants-types]]. Consolidating values is a separate operation — see [[products-variants-merge]].

## Business rules

### Value merging — permanent, on its own page

Consolidating values via **Merge values** is irreversible, rewrites past order history, and can even move variants across parameters. Full mechanics and rules: **[[products-variants-merge]]**.

### Parameter rename does NOT cascade to past orders

By contrast with value-merging: when the merchant renames a variant parameter (e.g., "Color" → "Colour") via the Edit modal in [[products-variants-wizard]], the rename cascades to all live products' parameter columns, but past order-lines are NOT auto-updated. Old orders still show the original parameter name. **Use Merge (not rename)** if the goal is to retroactively rebrand a value across order history.

### Value-text rename cascade on live variants

When the merchant renames a value (e.g., "Red" → "Crimson"), the text stored on each affected variant updates via a parameter-option rename cascade `(verify)`. Both the denormalised text value and the option ID stay aligned. Past order-lines are NOT updated by this path — use Merge for retroactive changes.

### Reordering requires "Enable Drag and drop sorting" first — static rows are NOT a bug

Drag-to-reorder does **nothing until the merchant clicks the "Enable Drag and drop sorting" button** at the top of the Values table (it toggles to **"Disable sorting"** once on). Until then the rows are **static** — dragging a row does not pick it up and no error appears — while delete, edit, and the other actions still work normally. This reads as "frozen / broken sorting" but is the intended default state, **not a defect**.

When the merchant enables it:

- A drag-mode disclaimer appears: *"Now you are in a drag mode and you can reorder the results in this table, when you are done disable the drag mode"*.
- The table reloads the **full value list unpaginated** (every value, not just the current 25-per-page page) so a value can be dragged across the whole list — essential for large parameters (e.g. a Size with 100+ values).
- The merchant drags a row by its handle; on drop the new order is saved immediately (optimistic re-order in the UI + a sort API call to persist it).
- Clicking the button again ("Disable sorting") leaves drag mode and returns to the normal paginated view.

The **same toggle** governs row reordering on the parent parameters list ([[products-variants-list-table]]) — that table is likewise drag-sortable only after this mode is enabled. A support answer that tells the merchant to "just drag the rows" without this first step is incomplete and produces false "sorting is broken" reports; before escalating a frozen-drag complaint as a bug, confirm the merchant pressed **Enable Drag and drop sorting**.

### Sort priority is auto-incrementing on create

A new value goes to the **bottom** of the value list for that parameter (sort defaults to `max(sort) + 1`). The merchant can then reorder it by drag-and-drop — after enabling sort mode (see above).

### Delete protection — must detach products first

Deleting an individual value fails if any variant uses it (parallel to parameter delete protection — see [[products-variants-data-model]]). The merchant can either reassign products to other values or use the Merge action to consolidate into a surviving value.

### Side effects on save

- **Search re-index** — adding / renaming values triggers a storefront search-engine resync.
- **Storefront cache invalidation** — variant pickers, product listings, and category-page caches are flushed.
- **No merchant webhook** for value CRUD — these changes don't fire `product.created` / `product.updated`.

## Related

- [[products-variants-options]] — hub.
- [[products-variants-types]] — per-type validation rules the value modal switches on.
- [[products-variants-list-table]] — list screen where the Values count opens this sub-page.
- [[products-variants-wizard]] — parameter Edit modal (rename / retype) that does NOT cascade to order history.
- [[products-variants-data-model]] — delete protection + the broader data-model rules.
- [[products-property]] — sister system; same merge semantics, same "permanent" caveats.

## Open questions

- Exact mechanism of the value-text rename cascade onto live variants (denorm refresh vs join-on-read) — `(verify)`.
