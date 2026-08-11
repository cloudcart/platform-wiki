---
type: feature
nav_path: "Analytics → Box catalog"
route_name: analytics
route_path: /admin/analytics
aliases: ["Analytics boxes", "Analytics box catalog", "Analytics box types", "Analytics box layout", "Analytics box sorting", "Dashboard cards"]
tags: [analytics, dashboard, boxes, charts, tables, ccanalytics]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[analytics]]. See the hub for the other aspects (dashboard shell, date & compare, settings panel, industry compare, data freshness).

# Analytics — box catalog & types

## Purpose

This aspect catalogues the **boxes** (cards) that make up the Analytics dashboard — what each measures, how it is rendered (chart / funnel / bar / table), how many rows a table box shows, and how the per-merchant box layout is built from the platform default merged with the merchant's saved order. It is the "what's on the dashboard and how it looks" page; the loading mechanics are in [[analytics-overview-dashboard]].

## Where to find it

The boxes are the body of the Analytics dashboard at `/admin/analytics`. Their order and visibility are controlled from the Settings panel's box-sort list — see [[analytics-overview-settings]].

## What the merchant can do here

- Read each box as a self-contained chart or table for the picked date range.
- Click `View details` on a box with `hasDetails: true` to drill in — see [[analytics-details]].
- Click "View more" on a table box to see beyond the top 5 rows — see [[analytics-full]].
- Reorder and hide boxes from the Settings panel.

## Settings & fields

Each box has a frontend configuration and a server-side Formatter. Configuration declares: `type` (`chart` / `funnel` / `bar` / `table`), `hasIndustryCompare` (whether the industry-average line is drawn — see [[analytics-overview-industry-compare]]), `hasDetails`, `viewMore`, and `navigationSort` (the position in the default sort).

### Box types

The `type` field controls which component renders the box:

| Type | Rendered as | Boxes |
|------|-------------|-------|
| `chart` | `DisplayChart` (line chart, single metric over time) | Total Sales, Total Orders, Total Customers, Total Visits, Conversion Rate, Customer Value, Average Order Value, Abandoned carts, Abandoned checkouts, Returns over time, Net revenue, Return rate |
| `funnel` | `DisplayFunnel` (funnel chart) | Conversion Funnel |
| `bar` | `DisplayBar` (bar chart) | Sales distribution |
| `table` | `DisplayTable` (table card with top-N rows) | All `top-*`, `*-by-*`, `landing-pages-*`, `orders-*`, `sessions-*`, `discount`-style boxes |

The chart boxes accept the date range, compare mode, and (when allowed) industry-compare; tables show the top **5 records** (`TABLE_RECORDS_LIMIT`) on the dashboard. To see more than 5, the merchant clicks "View more" → [[analytics-full]].

## Business rules

### Box catalog (35 boxes, grouped)

The boxes group naturally by what they measure:

| Category | Boxes |
|----------|-------|
| **Orders & sales** | Total Sales, Total Orders, Total Customers, Average Order Value, Customer Value, Sales distribution |
| **Returns** | Returns over time, Net revenue, Return rate — all three read one shared figure; see [[analytics-overview-returns-boxes]] |
| **Cart & funnel** | Conversion Rate, Conversion Funnel, Abandoned carts rate, Abandoned checkouts rate |
| **Visits** | Total Visits (Online store sessions), Online store sessions by device type, Visits by location, Visits by traffic source (referral), Traffic by Source / Medium |
| **Products** | Products by units sold, Products by sales, Products by traffic, Bundles by sales, Bundles by traffic |
| **Brands** | Vendors by sales, Vendors by traffic |
| **Categories** | Categories by sales, Categories by traffic |
| **Landing pages** | Landing pages by sales, Landing pages by visits |
| **Traffic & sources** | Sales by location, Sales by traffic source (referral), Sales by Source / Medium |
| **Discounts** | Order discounts, Product discounts |

Plus two boxes that ship `disabled: true` in the default sorting (`new-customers`, `returning-customers`) so they are filtered out before render; only CloudCart can re-enable them. The legacy `sessions-by-device` is commented out of `DEFAULT_BOXES_SORTING` and is therefore not shown on the dashboard by default.

### Per-merchant box layout

The boxes the merchant sees come from `DEFAULT_BOXES_SORTING` (the platform default) merged with any merchant-saved sort from the `cc_analytics` config (`defaultBoxesSorting`). If the merchant has saved a sort but the platform later adds a NEW box, the platform sort is appended at the end so the merchant doesn't miss it. Boxes with `disabled: true` in the default array (currently `new-customers`, `returning-customers`) are filtered out entirely. The merchant edits this list from the Settings panel — see [[analytics-overview-settings]].

## Related

- [[analytics]] — hub.
- [[analytics-overview-dashboard]] — how boxes load (async, progressive) and fail.
- [[analytics-overview-settings]] — where box order + visibility are configured.
- [[analytics-overview-industry-compare]] — the `hasIndustryCompare` overlay on chart boxes.
- [[analytics-details]] — the per-box drill-in (chart + table for one metric).
- [[analytics-full]] — the paginated full list for table boxes.
- [[analytics-total-sales]] / [[analytics-total-orders]] / [[analytics-total-customers]] — example per-box pages.

## Open questions

_None._
