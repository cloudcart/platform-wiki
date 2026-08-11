---
type: feature
nav_path: "Marketing → Segments → Editor → Condition builder"
route_name: segments.core_new.list
route_path: /admin/marketing-new/segments
aliases: ["Segment condition group", "Segment condition row", "Segment tree builder", "Nested conditions", "Composite key disambiguation", "parent::child"]
tags: [marketing, segments, editor, condition-builder, tree]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-segments-editor]]. See the hub for the other aspects (modal layout, operators-and-values, create popup, validation, save pipeline, plan gates).

# Segment editor — condition builder

## Purpose

The conditions tree is the actual rule structure the merchant builds. Each top-level row is one condition; conditions can have nested children; the whole tree is evaluated with **logical AND**. This page documents the **row module** (`SegmentConditionGroup`), the **tree mechanics** (nesting, collapse, scroll-into-view), and the **composite `parent::child` key disambiguation** that lets the same condition word (e.g. `product`) live under multiple subtrees.

The operator + value vocabulary is on [[segments-editor-operators-and-values]]. The modal shell is on [[segments-editor-modal-layout]].

## Where to find it

Inside the Segment editor modal, below the conditions banner. Each top-level row is a `SegmentConditionGroup` instance; nested rows are child `SegmentConditionGroup` instances rendered inside their parent's `<ul class="cc-tree">`.

## What the merchant can do here

- **Add a top-level condition** via **Add condition** on the toolbar (see [[segments-editor-modal-layout]]). A new empty row appears with the picker auto-opened and scrolled into view.
- **Pick a condition type** from the searchable grouped dropdown — see [[segments-editor-operators-and-values]] for the operator + value vocabulary.
- **Add a nested child** via the green plus on a row whose schema declares `sub_conditions`.
- **Collapse / expand** a condition group with the chevron at the row's left edge.
- **Remove** any row with the red trash icon (no confirmation; final removal happens on Save).
- Build trees like `Order → Times > 1 AND Order → Average > 500` ("Loyal customers" template) or `View → Product (Any) → Times > 2` ("Special product fans") — see [[segments-editor-create-popup]].

## Settings & fields

### Condition group module (`SegmentConditionGroup`)

Each top-level condition is a `SegmentConditionGroup`. When a group has a chosen `key`, the row gains:

- A **chevron button** at the left edge — toggles `collapsed` (rotates 180°); title alternates between "Collapse" and "Expand". Auto-expands when any nested condition has a validation error (so the merchant can see the error). Collapse state is local per instance — collapsing one parent does not collapse its siblings.
- The condition's **type label** (e.g., "Subscriber → Channel") in place of the picker dropdown.
- Where the condition's schema declares `allow_value = true`: the **operator + value controls** inline. If `allow_value = false` (e.g. some grouping-only parent conditions), the operator and value parts are hidden — the row is just a parent for nested children.
- The **green plus** (only when `hasSubConditions` — i.e., the condition's schema declares `sub_conditions`) — adds a nested child below.
- The **red trash icon** — removes this row (no confirmation; final removal happens on Save).

When the merchant adds a new root condition, the editor scrolls the new row into view (`scrollIntoView({behavior: 'smooth', block: 'nearest'})`) and the picker dropdown auto-opens for ~100ms via `newlyAddedRootIndex`. Same scroll-and-focus pattern applies to nested-add via the green plus.

Children render inside a `<ul class="cc-tree">` with vertical / horizontal connector lines (see `Tree.scss`) — the tree visualisation makes nested rules read as a hierarchy. The Header toolbar's static "Subscriber" label is the implicit root above all top-level conditions.

### Condition row anatomy

Each row has up to four parts:

| Part | Component | What it controls |
|------|-----------|------------------|
| **Condition key** | Searchable grouped dropdown | The condition type (e.g. `subscriber.channel`, `order.last`, `product`). Groups visible in the picker: Subscriber / Customer / Country / Date / Order / Cart / Product / View / Wishlist / Quantity / UTM / Shipping / Payment / Discount / Tag / Others / App-provided. |
| **Operator** | Select (no clear) | The comparison operator. The available options depend on the condition's value kind — see the operator table on [[segments-editor-operators-and-values]]. |
| **Value** | One of many components depending on the condition | The right-hand side of the rule — see the value-control table on [[segments-editor-operators-and-values]]. |
| **Actions** | Two icon buttons (right edge) | A green plus to add a nested condition (only on rows whose schema allows children, and not on root rows that do not support nesting); a trash icon to remove the row. |

### Nesting examples

The tree shape determines which conditions are children of which:

- An `Order` parent can have nested `Times` / `Amount` / `Average` / `Status` / `Product` children.
- A `View` parent can have nested `Product (Any)` / `Times` children — e.g. "Viewed any product more than 2 times".
- A `Cart` parent can have nested `Cart abandoned` / `Product` / `Quantity` children.

Children that the schema does not allow under a given parent simply do not appear in that subtree's picker.

### Composite-key disambiguation — `parent::child`

Some condition keys (e.g. `product`, `times`) exist in multiple subtrees (`view → product`, `subscriber → product`, `order → product`). When a merchant picks a nested child like "Product viewed N times", the editor stores the key as a **composite** `parent::child` — e.g. the platform code.

On save, the composite key is unwrapped: the editor produces a top-level `view` condition with a nested `product` child. This ensures the backend resolves the right subtree (e.g. `view_product_times` mapping rather than `product_times`).

When the merchant picks a condition that exists in multiple subtrees, the editor optionally fetches a **scoped** schema via `/admin/api/core/marketing/segments/condition/:key` with a `parent` query param — this disambiguates `module_id` values that exist in multiple subtrees (e.g. `product` under `view` vs under `subscriber`). See [[segments-editor-validation]] for the meta-endpoint behaviour.

### AI / template create wraps unknown sub-keys

When AI or a template emits a condition that is a nested child but at top level (e.g. `marketing.segments.conditions.page` without a parent), the save-payload builder wraps it in the correct parent module — except when the parent is `subscriber` (the root), in which case unwrapping is allowed. This guarantees a strict hierarchy regardless of how the AI / template flattens the structure. See [[segments-editor-create-popup]] for the AI / template flows and [[segments-editor-save-pipeline]] for the payload-build step.

## Business rules

- **Chevron auto-expands on nested error.** If a nested condition has a validation error, its parent group auto-expands so the merchant can see the failing field. See [[segments-editor-validation]] for how errors map to fields.
- **Removal is local until Save.** Clicking the red trash removes the row from the in-memory tree but does not call any endpoint — the segment is only re-persisted when Save runs.
- **Tree visualisation requires the `cc-tree` connectors.** Without the `<ul class="cc-tree">` wrapper, nested rows lose the visual hierarchy; the data structure works either way but is much harder to read.
- **No drag-reorder.** Conditions are evaluated set-wise (AND), so ordering does not affect semantics; the editor does not expose reorder controls.
- **Grouping-only conditions hide operator + value.** When `allow_value = false`, the row becomes a pure container for its children.

## Related

- [[marketing-segments-editor]] — hub.
- [[segments-editor-modal-layout]] — the modal shell that wraps the conditions tree.
- [[segments-editor-operators-and-values]] — operator + value-control vocabulary referenced by every row.
- [[segments-editor-validation]] — how invalid rows surface inline errors + how meta + scoped schema endpoints are fetched.
- [[segments-editor-create-popup]] — AI / template flows produce trees this module then renders.
- [[segments-editor-save-pipeline]] — how the in-memory tree is serialised on Save (composite-key unwrap, value normalisation).

## Open questions

No outstanding questions.
