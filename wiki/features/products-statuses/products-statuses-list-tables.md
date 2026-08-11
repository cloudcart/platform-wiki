---
type: feature
nav_path: "Products → Product statuses"
route_name: product-statuses-index
route_path: /admin/products/statuses
aliases: ["Product statuses list", "Conditional vs non-conditional statuses table", "Status priority sorting", "Status conflict indicator"]
tags: [products, statuses, stock, customer-facing]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 8
---
# Product statuses — the two list tables

## Purpose

This aspect documents the **list view** of the Product statuses screen: the two tables it shows (Conditional and Non-conditional), their columns, the drag-and-drop priority ordering of Conditional rules, and the conflict indicator that warns when two rules overlap.

> Part of [[products-statuses]]. See the hub for the related aspects (modal, operators/actions, evaluation, side-effects).

## Where to find it

Sidebar → Products → **Product statuses**. The two tables stack vertically on the same page: Conditional on top, Non-conditional below.

## What the merchant can do here

- Read the two tables at a glance to see which statuses fire automatically and which are manual.
- **Drag-and-drop** Conditional rows to reorder their priority.
- Open the Add / Edit modal (see [[products-statuses-modal]]) from the Add button or by clicking a row.
- Delete any row via its per-row Delete action.
- Spot conflicting Conditional rules via the error indicator in the Sorting column.

## Settings & fields

### Conditional table (top)

Info banner: *"Conditional statuses are applied automatically based on product stock quantity."*

Columns:

- **Name** — the customer-facing label.
- **If the quantity is** — the condition (operator + value) that triggers the status.
- **Actions** — which Buy-button behaviour fires (see [[products-statuses-operators-actions]]).
- **Sorting** — numeric priority plus an error indicator.

The table is **drag-sortable**. **Higher in the list = higher priority** — when multiple Conditional rules match the same product, the topmost one applies. Common ordering:

1. Special states first (Continue selling, Not tracked).
2. Specific quantity ranges next ("Lower than or equal to 5" → "Limited stock").
3. Catch-all rules last ("Greater than 0" → "In stock").

### Non-conditional table (bottom)

Info banner: *"Non-conditional statuses are applied manually per product. No quantity check."*

Columns: **Name**, **Actions**, Delete.

These statuses do NOT auto-apply — the merchant must explicitly assign them per product on the [[products-products]] Edit page, or via the bulk action *"Change product status 'Available' / 'Out of stock'"*.

### Which table a status lands in

A status is **Conditional** if it has a quantity operator set; **Non-conditional** if the operator is empty. The list page automatically sorts each status into the correct table on save — the merchant never moves a status between tables manually; they change the operator in the modal.

## Business rules

### The Sorting conflict indicator

The error indicator next to **Sorting** flags Conditional rules that overlap — for example, two rules both targeting "quantity = 0" with different actions, or a broad "Lower than 5" sitting above a narrower "Lower than or equal to 5". Because the platform applies the **topmost** matching rule by sort order, lower-priority overlapping rules will **never fire**. The indicator warns the merchant of this dead rule.

Resolution: either delete the lower rule, or tighten its condition so it no longer overlaps with the higher one. For the full priority chain the storefront applies, see [[products-statuses-evaluation]].

### New Conditional rows append to the bottom

When the merchant creates a new Conditional status (i.e., picks any operator), it is auto-appended to the bottom of the sorted list (highest existing sort value + 1). The merchant then drags it to the desired priority. Non-conditional statuses ignore the priority field entirely.

## Related

- [[products-statuses]] — hub.
- [[products-statuses-modal]] — the Add / Edit modal opened from this list.
- [[products-statuses-operators-actions]] — the operators + actions shown in the columns.
- [[products-products]] — where Non-conditional statuses are assigned per product.
- [[product-status-conditional-vs-non-conditional]] — the data-model view of the two-table split.

## Open questions

None.
