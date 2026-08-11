---
type: feature
nav_path: "Analytics → Products by traffic → UI surface"
route_name: analytics
route_path: /admin/analytics
aliases: ["Products by traffic dashboard box", "Products by traffic Details table", "Products by traffic ViewMore", "Продукти спрямо посещения — изглед"]
tags: [analytics, ccanalytics, products, traffic, top-products-by-traffic, ui]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 8
---
> Part of [[analytics-top-products-by-traffic]]. See the hub for the other aspects (data source / attribution, export).

# Products by traffic — UI surface

## Purpose

Documents everything the merchant **sees** in the "Products by traffic" report across its three drill-down levels — the dashboard top-5 box, the full Details table, and the per-product ViewMore time-series — plus the page-wide toolbar controls (date / compare / group / export) that drive all of them. The ranking metric is raw product-page views; what those views *mean* (the dedup model) lives on [[analytics-top-products-traffic-data-source]].

## Where to find it

Analytics dashboard → **Products by traffic** box. `navigationSort: 11`, so it sits in the products cluster of the dashboard. Clicking the box opens **Details** (`/admin/analytics/details/top-products-by-traffic`); clicking a product row in Details opens **ViewMore** (`/admin/analytics/details/top-products-by-traffic/extended/{product_id}`). Both share the [[analytics-details]] / [[analytics-full]] shell.

## What the merchant can do here

- Read the top 5 most-viewed products at a glance on the dashboard, with a per-device (mobile vs desktop) tooltip.
- Open the Details table for the full paginated ranking of every product viewed in the period; sort it and filter to specific product ids.
- Drill into one product's ViewMore chart to see its views over time.
- Change the date range, add a comparison period (overlaid as a dashed line on the ViewMore chart), and re-bucket the ViewMore series by hour / day / week / month.

## What the merchant sees

### Dashboard box (top 5)

| Element | What it is |
|---------|------------|
| Title row | EN: "Products by traffic" / BG: "Products by traffic" (BG title not translated — falls back to EN) |
| Each of the top 5 rows | Product name (linked), the `meta.row1` units chip ("Units {value}"), the `meta.row4` views chip ("Views {value}"), and a per-device split tooltip (mobile vs desktop) |
| Row sort | Total views DESC |
| Row count limit | 5 (the platform code) |

The per-device tooltip uses the localised "Visits: {total}" string (EN) / "Посещения: {total}" (BG). The dashboard box itself does NOT show date / compare / group / export controls — those are page-wide.

### Details screen (full table)

| Column key | EN label | BG label |
|------------|----------|----------|
| `product_name` | Name | Заглавие |
| `views` | Views / Sessions | Посещения / Сесии |
| `orders` | Orders | Поръчки |
| `quantity` | Units | Количество |
| `amount` | Amount | Сума |
| `conversion_rate` | Conversion rate | Conversion rate (untranslated) |

Default sort: `views` DESC, then `sales` DESC. Page size: `DETAILS_PAGINATION_LIMIT = 100`. `details.group = false` (one row per product — not grouped by date).

The Details column formatters are **reused** from [[analytics-top-order-products-by-units-sold]] — `details: ByUnits['top-order-products-by-units-sold'].formatters.details` — so the column rendering (links, number formatting, conversion-rate cells) is identical to the units-sold box. Only the underlying ranking metric differs.

### ViewMore (per-product over time)

Clicking a product row in Details opens a per-date breakdown for that single product. Columns:

| Column key | EN label | BG label |
|------------|----------|----------|
| `date` | Date | Дата |
| `views` | Views / Sessions | Посещения / Сесии |
| `orders` | Orders | Поръчки |
| `amount` | Amount | Сума |
| `quantity` | Units | Количество |
| `conversion_rate` | Conversion rate | Conversion rate |

`hasViewMoreChart: true` — a purple-filled area chart (`rgba(141, 88, 224, 0.1)` / `rgb(141, 88, 224)`) plots `views` per period above the table. Comparison (previous period) is overlaid as a dashed grey line when the compare picker is not `"no"`.

ViewMore tooltip (EN): *"{count} view for {date}|{count} views for {date}"*. BG: *"{count} посещение за {date}|{count} посещения за {date}"*.

### Details / ViewMore toolbar (every UI control)

| Control | Where | What it does | Plan / config gate |
|---------|-------|--------------|----------------------|
| **Date range picker** | Top-left toolbar | Re-fetches the rows. | Maximum look-back capped by `cc_analytics.compare_range` plan feature (default 12 months back). |
| **Compare select** | Next to date picker | `No comparison` / `Previous period` / `Previous year`. Adds previous-period columns to the table. | Plan-gated by `cc_analytics.allow_period_compare`. Hidden if `details.compare: false` (this box does not set it, so the dropdown is always present in Details). |
| **Group select** | Next to compare | `Hourly` / `Daily` / `Weekly` / `Monthly` / `Quarterly` / `Yearly` / `None`. Shown on Details only when `details.group !== false`; on ViewMore controls the time-bucket for the chart and table. | Auto-filters its own options as the date range changes: **Hourly hidden if range > 7 days**, **Daily hidden if range > 90 days**. |
| **Export link** | Top-right (cloud-download icon) | Triggers the export flow — see [[analytics-top-products-traffic-export]]. | Hidden when `allowExport` is `false` (backend permission `reports.reports_export` denied). Hidden during loading. |
| **Force-limit warning banner** | Above the table | Yellow alert *"This report shows up to {total} results. To see all results, you can [Export]"* — shown when the table is capped at `DETAILS_FORCE_LIMIT = 1000` rows. | Only fires when the backend returns `force_limit` (Products-by-traffic ViewMore can hit this when the period has > 1000 date buckets). See [[analytics-top-products-traffic-data-source]]. |

The dashboard box does NOT carry the date / compare / group / export controls — those are page-wide (set once at the dashboard top) and inherit into each box. Export is only available on Details / ViewMore.

## Settings & fields

The UI is driven entirely by the box's Vue config (no merchant-editable settings). The fields most relevant to what renders:

| Key | Value | UI effect |
|-----|-------|-----------|
| `type` | `table` | Table layout for the box + Details. |
| `viewMore` | `true` | Each Details row is clickable into ViewMore. |
| `hasViewMoreChart` | `true` | Renders the purple area chart in ViewMore. |
| `details.group` | `false` | One row per product on first-level Details (no date bucketing). |
| `details.defaultSorting` | views DESC, sales DESC | Initial Details sort order. |

The full config table is on the hub [[analytics-top-products-by-traffic]].

## Business rules

- The chart and rankings plot **raw views**, distinguishing this box from the sibling [[analytics-top-order-products-by-sales]] (revenue) and [[analytics-top-order-products-by-units-sold]] (units sold).
- A product that ranks high here but is absent from the sales boxes is the obvious "interest but no conversion" candidate to investigate.
- The empty state — no views in the period — renders a "No data" placeholder; ViewMore still renders zero-rows for every pre-generated date bucket. See [[analytics-top-products-traffic-data-source]].

## Related

- [[analytics-top-products-by-traffic]] — hub.
- [[analytics-top-products-traffic-data-source]] — where the rows come from + the dedup attribution + the 1000-bucket force-limit banner.
- [[analytics-top-products-traffic-export]] — what the Export link triggers.
- [[analytics-details]] / [[analytics-full]] — the shared Details / ViewMore shell.
- [[analytics-top-order-products-by-units-sold]] — sibling box; provides the column formatters this box reuses.
- [[product]] — product entity (the linked-name cell target).

## Open questions

_None._
