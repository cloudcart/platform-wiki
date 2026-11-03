---
type: feature
nav_path: "Analytics → Products by sales → UI surface"
route_name: analytics
route_path: /admin/analytics
aliases: ["Products by sales dashboard box", "Products by sales Details table", "Products by sales ViewMore", "Продукти по продажби — изглед"]
tags: [analytics, ccanalytics, orders, products, top-order-products-by-sales, ui]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 9
---
> Part of [[analytics-top-order-products-by-sales]]. See the hub for the other aspects (status filter, data source, export).

# Products by sales — UI surface

## Purpose

Documents everything the merchant **sees** in the "Products by sales" report across its three drill-down levels — the dashboard top-5 box, the full Details table, and the per-product ViewMore time-series — plus the page-wide toolbar controls (date / compare / group / export) that drive all of them.

## Where to find it

Analytics dashboard. The box titled **"Products by sales"** sits high on the dashboard (`navigationSort` 9). Clicking the box opens **Details**; clicking a product row in Details opens **ViewMore**.

## What the merchant can do here

- Read the top 5 revenue-generating products at a glance on the dashboard.
- Open the Details table for the full ranking (up to 1000 products), sort it, and filter to specific products.
- Drill into one product's ViewMore chart to see its revenue over time.
- Change the date range, add a comparison period, and re-bucket the ViewMore series by hour / day / week / month.

## What the merchant sees

### Dashboard box (top 5)

Each row is one product. `aggregate` is total amount (divided by 100 = currency units). `meta.row1` is `quantity` (units sold), formatted via the `units` translation ("Unit X / Units X" EN, "Количество X / Количество X" BG). The dashboard shows up to 5 rows (`TABLE_RECORDS_LIMIT`), sorted by amount DESC, then sales DESC.

Each row has a `viewMore` field that equals the `product_id` whenever the id is `> 0`, otherwise null. `device` carries the mobile/desktop split for the row's order count. The dashboard box itself does NOT show date / compare / group / export controls — those are page-wide.

### Details screen (full table)

| Column key | EN label | BG label |
|------------|----------|----------|
| `product_name` | Name | Заглавие |
| `views` | Views / Sessions | Посещения / Сесии |
| `orders` | Orders | Поръчки |
| `quantity` | Units | Количество |
| `amount` | Amount | Сума |
| `conversion_rate` | Conversion rate | Conversion rate |

Default sort: `amount` DESC, `sales` DESC. Page size 100. The `product_name` cell renders the `ProductLink` Vue component (clickable link to the product's storefront page). The `quantity` cell uses the `Quantity` Vue component. The Details table is capped at 1000 distinct products — see [[analytics-top-order-products-sales-data-source]] for the force-limit and the related banner.

### ViewMore (per-product time-series)

The per-date breakdown for one product id. Groups by date bucket (hourly / daily / weekly / monthly per the period picker). Columns: `date`, `views`, `orders`, `amount`, `quantity`, `conversion_rate` (same labels as Details, with `date` = Date / Дата).

`hasViewMoreChart` is true — an area line chart of `amount` over time, with an optional dashed comparison line. ViewMore tooltip (EN): *"{amount} from {count} order for {date}|{amount} from {count} orders for {date}"*.

### Details / ViewMore toolbar (every UI control)

| Control | Where | What it does | Plan / config gate |
|---------|-------|--------------|----------------------|
| **Date range picker** | Top-left toolbar | Re-fetches the rows. | Capped by `cc_analytics.compare_range` (default 12 months back). |
| **Compare select** | Next to date picker | `No comparison` / `Previous period` / `Previous year`. | Plan-gated by `cc_analytics.allow_period_compare`. Box does NOT set `details.compare: false`, so the dropdown is present. |
| **Group select** | Next to compare | `Hourly` / `Daily` / `Weekly` / `Monthly` / `Quarterly` / `Yearly` / `None`. Box config `details.viewMore.group: true` enables this for ViewMore; on first-level Details it's hidden because `details.group: false` (one row per product, no time bucketing). | Auto-filters: **Hourly hidden if range > 7 days**, **Daily hidden if range > 90 days**. |
| **Export link** | Top-right | Triggers ExportModal + 2FA flow — see [[analytics-top-order-products-sales-export]]. | Hidden when `allowExport: false` (perm: `reports.reports_export`). |
| **Force-limit banner** | Above table | *"This report shows up to {total} results. To see all results, you can [Export]"* | Fires when Details is capped at 1000 rows. |

## Settings & fields

The UI is driven entirely by the box's Vue config (no merchant-editable settings). The fields most relevant to what renders:

| Key | Value | UI effect |
|-----|-------|-----------|
| `type` | `table` | Table layout for the box + Details. |
| `viewMore` | `true` | Each Details row is clickable into ViewMore. |
| `hasViewMoreChart` | `true` | Renders the area chart in ViewMore. |
| `details.defaultSorting` | `amount` DESC, `sales` DESC | Initial Details sort order. |
| `details.group` | `false` | No date-bucketing on first-level Details. |
| `details.viewMore.group` | `true` | Date-bucket select available in ViewMore. |

The full config table and the chart `tableToChart` override are on the hub [[analytics-top-order-products-by-sales]].

## Business rules

- The chart and rankings plot **revenue** (`amount`), distinguishing this box from the sibling [[analytics-top-order-products-by-units-sold]] which plots `quantity`.
- Rows with `product_id = 0` (deleted / orphan products) never appear here — see [[analytics-top-order-products-sales-data-source]].
- The yellow status alert above the Details table is covered in [[analytics-top-order-products-sales-status-filter]].

## Related

- [[analytics-top-order-products-by-sales]] — hub.
- [[analytics-top-order-products-sales-export]] — what the Export link triggers.
- [[analytics-top-order-products-sales-data-source]] — where the rows come from + the 1000-row force-limit banner.
- [[analytics-top-order-products-by-units-sold]] — sibling box ranked by quantity.
- [[product]] — product entity (the `ProductLink` cell target).

## Open questions

_None._
