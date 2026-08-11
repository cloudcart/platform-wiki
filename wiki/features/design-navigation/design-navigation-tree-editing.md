---
type: feature
nav_path: "Design → Navigation → Tree editing"
route_name: admin.navigation.reorder
route_path: /admin/storefront/navigation/{group}/reorder
aliases: ["Navigation tree editing", "Menu drag and drop", "Menu reorder", "Menu nesting depth", "Delete menu item", "Преподреждане на меню"]
tags: [design, navigation, menus]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---
# Navigation — tree editing

> Part of [[design-navigation]]. See the hub for the other aspects (item types, item fields, menu groups, link resolution, side-effects).

## Purpose

This page documents how the merchant restructures a menu tree directly on the Navigation screen — drag-and-drop reordering and re-parenting, the maximum nesting depth, the no-cycle rule, and recursive deletion. These actions persist immediately, with no save button.

## Where to find it

Sidebar → **Design** → **Navigation**. Drag any node within the Main or Footer tree, or click a node's delete icon. Reorders POST to `/admin/storefront/navigation/{group}/reorder`; deletes hit `/admin/storefront/navigation/{group}/delete/{navigation_id}`.

## What the merchant can do here

- Drag any node to a new position — drop **before**, **after**, or **inside** (nest into) another node to reorder or re-parent it. Drag-and-drop persists immediately.
- Click a node to expand it and reveal child items. Trees auto-open on load.
- Click the delete icon on any node to remove it and all its children.

## What the merchant cannot do here

- Nest items more than 4 levels deep — the form and the drag both reject with *"Maximum depth is 4"*.
- Drop a node into one of its own descendants — rejected with *"The targeted is moved"*.
- Move a node under a parent where its name already exists — rejected with *"Name is taken"* (see [[design-navigation-item-fields]]).
- Partially delete a sub-tree — deleting any node removes its entire sub-tree (no "move children to parent" prompt).

## Settings & fields

Tree editing has no form fields of its own. The reorder endpoint takes a target node and a `position` value of `before`, `after`, or `inside`. The depth and name-uniqueness constraints it enforces are the same ones documented in the validation table on [[design-navigation-item-fields]].

## Business rules

### Drag-and-drop with three drop modes — `before`, `after`, `inside`

When the merchant drags a node onto another node, the position passed to the reorder endpoint is one of:

- `before` — the moved node becomes the previous sibling of the target.
- `after` — the moved node becomes the next sibling of the target.
- `inside` — the moved node becomes the first child of the target (nests it).

All three modes re-parent the node if the source and target have different parents, then re-number the `order` field for all siblings under the new parent.

### Max nesting depth is 4 levels

A menu item cannot be added or moved into a position where the total depth (its ancestor chain plus its descendant chain) exceeds 4. Enforced both server-side (the form rejects with *"Maximum depth is 4"*) and during drag-and-drop (the drop is rolled back if it would breach the limit).

### Re-parenting re-validates depth + name uniqueness

A `before` / `after` drop into a different parent re-checks both constraints: (1) the new combined depth must not exceed 4 (rolls back with *"Maximum depth is 4"*), and (2) the moved node's name must not collide with a sibling under the new parent (rolls back with *"Name is taken"*).

### Drop cannot move a parent inside its own descendant

Trying to drop a node into one of its own descendants is rejected with *"The targeted is moved"* — this prevents tree cycles.

### Deleting an item deletes all its children

Removing a menu item recursively deletes its entire sub-tree. There is no soft-delete and no "move children to parent" prompt — the merchant must rebuild the sub-menu by hand if they intended a partial delete.

### Reorder self-heals broken `order` values

When a reorder lands, the server re-numbers all siblings under the target parent (1, 2, 3, …). A half-corrupted `order` column (gaps or duplicates from a botched migration) therefore self-heals on the next reorder of any sibling. Deletion triggers the same re-numbering of surviving siblings under the old parent, so the `order` field stays gap-free.

### Each save invalidates the storefront menu cache

Every reorder / delete regenerates the merchant's site cache key, so the storefront rebuilds its cached menu HTML within seconds — there is no manual cache-clear button. The full cache mechanics are on [[design-navigation-side-effects]].

## Related

- [[design-navigation]] — hub.

## Open questions

None.
