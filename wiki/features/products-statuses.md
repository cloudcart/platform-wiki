---
type: feature
nav_path: "Products → Product statuses"
route_name: product-statuses-index
route_path: /admin/products/statuses
aliases: ["Product statuses", "Stock statuses", "Statuses (Products)", "Статуси на продукта", "Налични", "Изчерпан"]
tags: [products, statuses, stock, customer-facing]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 8
---
# Product statuses

## Purpose

The screen where the merchant defines **stock-based product status labels** that customers see on the storefront product cards and product detail pages — *"In stock"*, *"Out of stock"*, *"Limited stock — only 3 left"*, *"Coming soon"*, *"Request a quote"*, etc. Each status carries a **name** (what the customer sees), an optional **quantity condition** (the rule that triggers it — e.g., "when quantity is ≤ 0"), and an **action type** (what happens to the Buy button — show it, hide it, change it to a Request button, or change it to a Subscribe-for-quantity button).

The page splits statuses into two groups: **Conditional** (triggered automatically based on the product's current stock quantity, priority drag-sortable) and **Non-conditional** (manually assigned to products by the merchant). This is distinct from the Order / Payment / Shipping statuses configured in [[settings-statuses]] — those govern order lifecycle. This page is about **product availability** as customers see it.

This hub is slim by design. The detail lives in the aspect pages below. For the underlying data model (not the screen), see the [[product-status]] entity cluster.

## Where to find it

Sidebar → Products → **Product statuses**.

The breadcrumb reads "Products → Product statuses". The route is `/admin/products/statuses`. The header icon is the box-check icon.

## What the merchant can do here

- View two tables: **Conditional** (top) and **Non-conditional** (bottom) — see [[products-statuses-list-tables]].
- **Drag-and-drop** Conditional rows to reorder priority; the topmost matching rule wins.
- Add a status (Add / Edit modal) — see [[products-statuses-modal]].
- Edit or Delete any existing status.
- Choose a **quantity operator** (8 options) and an **action type** (4 options) — see [[products-statuses-operators-actions]].
- Leave the operator EMPTY to make a status **Non-conditional** (manual assignment only via [[products-products]]).

What the merchant **cannot** do here: build multi-condition rules (only ONE condition per status), style the badge (theme-controlled), import statuses from CSV, or schedule a status to dates/times (statuses are evaluated in real time against current stock).

## Settings & fields

The screen's controls are catalogued across the aspect pages:

- The **two list tables**, their columns, drag-sort priority, and the conflict indicator — see [[products-statuses-list-tables]].
- The **Add / Edit modal** with its dynamic field visibility, save-enable rule, and quantity-value minimums — see [[products-statuses-modal]].
- The **8 quantity operators** and **4 action types** (the field catalogue) — see [[products-statuses-operators-actions]].
- The **`button_text`** field appears only for the Request / Subscribe actions; the **Continue selling alert** appears only for the Continue-selling operator — both documented in [[products-statuses-modal]].

## Business rules

The business behaviour is split into two aspect pages:

- **How a status fires** — per-variant evaluation, the manual `status_id` / `out_of_stock_id` overrides, priority order, one badge per product, bundle bypass — see [[products-statuses-evaluation]].
- **Side effects of saving / deleting** — storefront cache flush, the delete cascade that NULLs product references, the implicit normalisations on save, the globally-unique name constraint — see [[products-statuses-side-effects]].

## Sub-pages (in this cluster)

- [[products-statuses-list-tables]] — the two-table list view (Conditional vs Non-conditional), columns, drag-sort priority, the Sorting conflict indicator.
- [[products-statuses-modal]] — the Add / Edit modal: dynamic field visibility, the Save-enable rule, quantity-value minimums, the Continue-selling alert.
- [[products-statuses-operators-actions]] — the 8 quantity operators (with stored IDs) + the 4 Buy-button action types.
- [[products-statuses-evaluation]] — how a status is chosen at storefront time: per-variant matching, manual overrides, priority, bundle bypass.
- [[products-statuses-side-effects]] — save / delete side effects, normalisations, the unique-name constraint, plan gates + permission.

## Related

- [[products]] — parent hub.
- [[product-visibility]] — the full "why isn't my product showing" checklist (active / draft / hidden / window / stock / geo); these stock labels are one input.
- [[product-status]] — the underlying entity (data model) for product availability labels.
- [[products-products]] — products are assigned a status; the Edit page and bulk actions handle per-product overrides.
- [[products-inventory]] — "Continue selling when sold out" flag, evaluated by the Continue-selling operator on this page.
- [[products-missing-product]] — subscribers waiting for "Notify me when in stock" emails (driven by the "Show as subscribe" action).
- [[settings-statuses]] — separate Order / Payment / Shipping status taxonomy (distinct from product status).
- [[inventory-tracking]] — the inventory model; stock changes re-trigger status evaluation.
- [[settings-cart]] — `order_status_for_quantity_decrease` controls WHEN stock is decremented; affects when these statuses fire.
- [[settings-hooks]] — `product.updated` webhook fires on stock changes that trigger status reevaluation.
- [[product]] — entity page.
- [[variant]] — entity page.

## Open questions

None.
