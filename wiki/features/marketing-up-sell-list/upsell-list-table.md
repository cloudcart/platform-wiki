---
type: feature
nav_path: "Marketing → UpSell & Cross-sell → UpSell List → Offer table"
route_name: admin.up_sell.list
route_path: /admin/marketing-new/up-sell
aliases: ["UpSell offer table", "UpSell list columns", "UpSell list metrics", "UpSell status filter", "UpSell list empty state", "Колони на UpSell списъка"]
tags: [marketing, upsell, list, metrics, columns]
plan_gates: ["upsells"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[marketing-up-sell-list]]. See the hub for the other aspects (actions, validation, storefront firing, plan budget).

# UpSell List — the offer table

## Purpose

The **offer table** is the main body of the UpSell List: a server-side AJAX-paginated grid keyed on `admin.up_sell.list`, showing **one row per offer root** with eight aggregate-metric columns. It exists to give the merchant an at-a-glance scoreboard of which replacement offers are earning money and which are dead weight — without opening each one in [[marketing-up-sell-diagram]].

## Where to find it

Sidebar → Marketing → **UpSell** → the table fills the page body. Direct URL: `/admin/marketing-new/up-sell`. Rows are sorted by `id DESC` by default; most metric columns are click-sortable.

## What the merchant can do here

### Browse the offer table

Each row is one **master record** (only roots with `parent = 1` appear). Columns:

| Column | Source | Sortable | Description |
|---|---|---|---|
| **Title** (`global.th.title`) | `up_sell.name` (internal title) | No | A link that opens the offer's **diagram** view (NOT a flat edit form). |
| **Sales generated** (`up_sell.th.sales_generated`) | Sales-generated subquery | Yes | Total monetary value of order-line items attributed to this offer for orders in `pending`, `paid`, or `completed` status. Formatted as money. |
| **Total sales** (`up_sell.th.total_sales`) | Total-sales subquery | Yes | Distinct order-product count where this UpSell was applied. |
| **Added to cart** (`global.th.added_to_cart`) | `added_to_cart` column | Yes | Lifetime count of times a customer accepted this offer and added the offered variant to cart. |
| **Total cancel** (`global.th.total_cancel`) | `total_cancel` column | Yes | Lifetime count of times a customer dismissed the popup. Incremented by the storefront's `site.up_sell.discard` route. |
| **Success rate** (`global.th.success_rate`) | Success-rate subquery | Yes | Computed as `(100 / (added_to_cart / total_orders)) * 100`. Formatted as a percentage. |
| **In stock** (`up_sell.th.in_stock_offer`) | In-stock-offer subquery | Yes | "Yes" if the offer variant currently has inventory (or the product has continue-selling on); "No" otherwise. |
| **Views** (`global.th.views`) | `views` column | Yes | Lifetime count of times the popup was shown. Incremented every time the storefront's `site.upSell.proposal` route serves it. |
| **Active** (`global.th.active`) | `status` column | Yes | Toggle switch — flipping it calls `admin.up_sell.status/{id}/{0|1}`. See [[upsell-list-actions]]. |

### Filter the list

The filter dropdown exposes a single filter — **Status**:

- *"-- All --"* (default).
- **Active** (`filter.active`).
- **Inactive** (`filter.inactive`).

Saved searches are NOT enabled for this filter, and although the underlying framework supports text search, no explicit search bar is configured in the list template.

### Empty state

When the merchant has 0 UpSell records, the table is hidden and an empty-box card shows:

- Title: *"No UpSells yet"* (per `global.notify.no_records_yet`).
- Body: *"You haven't added any UpSell yet. Add your first one to get started."* (per `global.notify.no_records_info`).
- Help link: *"Need help? Visit our support center"* (per `global.notify.no_records_help` + `no_records_help_link`).

### What the merchant CANNOT do here

- **Filter by trigger product / offer product** — the only exposed filter is Status. Searching by product requires opening each row.
- **See per-row trigger / offer product columns** — the table shows aggregate metrics only. To see what an offer offers, the merchant clicks into it.
- **Bulk-edit offer fields** (e.g. bulk-change button color or expiry) — the only bulk action is delete; see [[upsell-list-actions]].

## Settings & fields

### Per-row data sources

| Source | What it adds | Joins / heavy ops |
|---|---|---|
| Master filter | Filters to root records only (`parent = 1`). | None. |
| Sales-generated subquery | Adds `sales_generated`: sum of `total * quantity` from `orders_products_up_sell` joined with orders in `pending/paid/completed`. | Subquery per row — slow at high volume. |
| Total-sales subquery | Adds `total_sales`: count distinct `order_product_id` per UpSell. Sets a database session variable `@total_orders`. | Subquery + session var. |
| Success-rate subquery | Adds `success_rate`: `(100 / (added_to_cart / @total_orders)) * 100`. | Reuses `@total_orders` if present. |
| In-stock-offer subquery | Adds `in_stock_offer` (boolean): TRUE if offer variant has stock or product has `continue_selling`. | Joins products + products_variants. |

The `views`, `added_to_cart`, and `total_cancel` columns are plain stored counters incremented storefront-side — see [[upsell-list-storefront-firing]].

## Business rules

### List shows master records only

The list applies a `master` filter (`parent = 1`), so it shows one row per offer. Offers created in the current UI are all masters. Any **legacy multi-step chain** (from the retired branch builder) shows only its root row here — the descendant records are not listed.

### Sales metrics aggregate per-record

The sales-generated and total-sales columns attribute against **only** the specific offer record (`up_sell_id`), so each offer's row reflects only its own accepted conversions. (For legacy chains, each descendant offer kept its own separate metrics — the root row never showed cumulative chain revenue.)

### Performance trade-off on large lists

Each row triggers 3-4 SQL subqueries via the data sources above. Stores with many UpSell offers see slower list-page loads — each subquery hits the orders + products tables.

### In-stock column mirrors the storefront gate

The **In stock** column runs the same in-stock-offer check that decides whether the popup actually fires for customers — an offer reading "No" is invisible to shoppers until restocked. See [[upsell-list-storefront-firing]].

## Related

- [[marketing-up-sell-list]] — hub.
- [[marketing-up-sell-diagram]] — opens when a row title is clicked.
- [[upsell-list-actions]] — the Active toggle + bulk operations driven from this table.
- [[upsell-list-storefront-firing]] — where the counter columns and the in-stock gate come from.
- [[products-products]] — products picked as trigger / offer variants.

## Open questions

No outstanding questions.
