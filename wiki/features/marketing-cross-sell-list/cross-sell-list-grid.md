---
type: feature
nav_path: "Marketing → UpSell & Cross-sell → Cross-Sell List → Grid & metrics"
route_name: admin.cross_sell.list
route_path: /admin/marketing-new/cross-sell
aliases: ["Cross-Sell list grid", "Cross-Sell list columns", "Cross-Sell sales metrics", "Cross-Sell success rate", "Cross-Sell offer table"]
tags: [marketing, cross-sell, list, metrics, grid]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[marketing-cross-sell-list]]. See the hub for the other aspects (actions, validation, plan budget).

# Cross-Sell List — grid & metrics

## Purpose

This aspect documents the **offer table itself** — the paginated grid that lists Cross-Sell offers (master records), its columns, the per-row data sources that populate them, and the rule that **all sales metrics are scoped to the individual offer record**.

## Where to find it

Sidebar → Marketing → **Cross-Sell** (`/admin/marketing-new/cross-sell`, route `admin.cross_sell.list`). The grid is the body of the list page. Each row is one **master** record (roots only, `parent = 1`), sorted by `id DESC` by default.

## What the merchant can do here

The grid is read-only at the cell level — the merchant browses, sorts by any sortable column, and clicks a row title to open that offer in the diagram editor (see [[cross-sell-list-actions]] for the click-through and toggle behaviours). The columns:

| Column | Source | Sortable | Description |
|---|---|---|---|
| **Title** (`global.th.title`) | `cross_sell.name` (internal title) | No | Link that opens the offer's diagram view at `admin.cross_sell.diagram/{id}`. |
| **Sales generated** (`up_sell.th.sales_generated` — the Cross-Sell list reuses the UpSell lang key) | Sales-generated subquery | Yes | Sum of revenue attributed to this Cross-Sell offer for orders in `pending`/`paid`/`completed`. Formatted as money. |
| **Total sales** (`up_sell.th.total_sales`) | Total-sales subquery | Yes | Distinct order count where the offer was applied. |
| **Added to cart** (`global.th.added_to_cart`) | `added_to_cart` column | Yes | Lifetime count of times customers accepted the offer and added the offered product(s) to cart. |
| **Total cancel** (`global.th.total_cancel`) | `total_cancel` column | Yes | Lifetime count of popup dismissals. Incremented by `site.cross_sell.discard`. |
| **Success rate** (`global.th.success_rate`) | Success-rate subquery | Yes | `(100 / (added_to_cart / total_orders)) * 100`, formatted as percent. |
| **Views** (`global.th.views`) | `views` column | Yes | Lifetime popup-display count. |
| **Active** (`global.th.active`) | `status` column | Yes | Toggle. Routes to `admin.cross_sell.status/{id}/{0|1}`. |

Notably absent (vs the UpSell list): **no "In stock" column** — a Cross-Sell offers multiple products, so stock filtering is handled per-product at customer-facing render time via the `hide_out_of_stock` setting (see [[marketing-cross-sell]]).

## Settings & fields

### Per-row data sources

The grid composes each row from a base master query plus several subqueries:

| Source | Adds | Notes |
|---|---|---|
| Master filter | Filters to roots only (`parent = 1`). | Same pattern as the UpSell list. |
| Sales-generated subquery | `sales_generated` from `orders_cross_sell` joined to orders. | One subquery per row. |
| Total-sales subquery | `total_sales` distinct count. | Sets `@total_orders` session var. |
| Success-rate subquery | `success_rate` derived from `@total_orders`. | Reuses the session var. |
| (No in-stock-offer column for Cross-Sell.) | — | Stock filtering happens at render time, not at the list. |

The `views`, `added_to_cart`, and `total_cancel` counters are stored columns updated in real time as customers interact with the popup — they are not subqueries.

## Business rules

### Sales metrics scoped to this record only

`sales_generated` and `total_sales` query `orders_cross_sell` filtered by `cross_sell_id`, so each offer's row reflects only its own conversions. (For legacy chains, each descendant kept its own separate `cross_sell_id` metrics — the root row never showed cumulative chain revenue.)

### Sales-generated is order-status filtered

The sales-generated subquery only counts revenue for orders in `pending`, `paid`, or `completed`. Orders in `cancelled`, `returned`, or other terminal-failure states are excluded. So "Sales generated" reflects gross attributed revenue, not net.

### Default sort & saved searches

The grid sorts by `id DESC` (newest first) by default; every metric column except Title is sortable. Saved searches are disabled for this list.

## Related

- [[marketing-cross-sell-list]] — hub.
- [[marketing-cross-sell]] — the engine; `hide_out_of_stock` per-product render filtering and the discount integration that feeds attributed revenue.
- [[marketing-up-sell-list]] — sister list whose `sales_generated` / `total_sales` lang keys this grid reuses.
- [[order]] — orders in `pending`/`paid`/`completed` are the ones counted in attributed sales.

## Open questions

No outstanding questions.
