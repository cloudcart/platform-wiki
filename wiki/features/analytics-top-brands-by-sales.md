---
type: feature
nav_path: "Analytics → Vendors by sales"
route_name: analytics
route_path: /admin/analytics
aliases: ["Vendors by sales", "Brands by sales", "Top brands by sales", "Top vendors by sales", "Best-selling vendors", "Производители по продажби", "Марки по продажби", "Най-продавани производители"]
tags: [analytics, ccanalytics, orders, brand, vendor, top-brands-by-sales]
plan_gates: []
created: 2026-05-22
updated: 2026-05-27
source_count: 8
---
# Vendors by sales (top brands by sales)

## Purpose

A ranked table of the merchant's **best-selling vendors (brands)** by revenue for the selected time range. Answers: *"Which brands actually drive my sales — by amount, not just units?"* Surfaces the top 5 vendors on the dashboard, each with total amount, units sold, number of orders, mobile/desktop split, and a drill-down to the per-vendor revenue trend.

**Naming gotcha** — the box URL slug is `top-brands-by-sales`, but everything in the data is named after `vendor` (the `vendor_id` / `vendor_name` fields). The English UI title shown to merchants is literally **"Vendors by sales"** (not "Brands by sales"). This is intentional — "vendor" is CloudCart's canonical name for what merchants call a "brand" (see [[vendor]]). The `top-brands-by-sales` slug is kept for backwards compatibility with old layout configurations.

## Where to find it

Sidebar → **Analytics** dashboard. The box title is **"Vendors by sales"** (EN literal — same wording in BG locale, not translated). It sits between Bundles and Categories in the default sort, with `top-brands-by-traffic` as its visible child box.

Actions:
- Click a vendor name → opens the storefront vendor page.
- Click **View more →** → opens the per-vendor revenue trend chart.
- Click **See details** → `/admin/analytics/details/top-brands-by-sales` for the full paginated table and export.

## What the merchant can do here

### Dashboard card

Top 5 vendors ranked by amount desc, then sales (orders) desc. Each row:

| Field | What it shows |
|-------|---------------|
| Name | Vendor name (last-known) — hyperlinked to vendor storefront URL |
| "Units {value}" | Units of products from this vendor sold in the period |
| Amount (current) | Total sales amount for the vendor, in store currency |
| "Sales {value}" | Number of orders containing the vendor (formatted as money) |
| Device | Mobile/desktop split of orders for this vendor |
| Drill-down | Available only for live vendors; suppressed for deleted ones |

### Tooltip (box-level)

**EN**: *"Best-selling vendors of the total value of the products as an amount. The data is visualized according to the following statuses of orders - Paid, Completed, Pending, Authorized payment, Fulfilled."*

**BG**: *"Най-продавани производители от общата стойност на продуктите като сума. Данните се визуализират спрямо следните статуси на поръчки - Платена, Изпълнена, Изчакваща, Оторизирано плащане, Изпратена."* (BG uses "производители" — the local equivalent of "vendors".)

### Details — `/admin/analytics/details/top-brands-by-sales`

Paginated 100/page, 1 000-row hard cap. Columns:

| EN label | BG label | What it shows |
|----------|----------|---------------|
| Name | Заглавие | Hyperlinked vendor name |
| Views / Sessions | Посещения / Сесии | Sessions for vendor pages |
| Orders | Поръчки | Distinct orders containing this vendor |
| Units | Количество | Units sold |
| Amount | Сума | Total amount (money) |
| Conversion rate | Конв. процент | orders / views |

Default sort: amount desc, sales desc. Period comparison supported. The Details table carries the same permanent status-filter alert as the box tooltip (see Business rules below).

### View More — `/admin/analytics/full/top-brands-by-sales/:vendor_id`

Line chart of the chosen vendor's amount over time, grouped by the selected period granularity. Tooltip: *"{amount} from {count} order for {date}"*.

### Details / ViewMore toolbar (page-wide controls)

These controls live on the Details and View More pages, not on the dashboard card:

- **Date range picker** — re-fetches the rows; capped at 12 months by `cc_analytics.compare_range`.
- **Compare select** — `No comparison` / `Previous period` / `Previous year`; plan-gated by `cc_analytics.allow_period_compare`, always rendered.
- **Group select** — `Hourly` / `Daily` / `Weekly` / `Monthly` / `Quarterly` / `Yearly` / `None` (View More only). Hourly is hidden when the range > 7 days; Daily when > 90 days.
- **Export link** — top-right cloud-download icon; starts the export + 2FA flow. Hidden without permission `reports.reports_export`.
- **Force-limit banner** — *"This report shows up to {total} results. To see all results, you can [Export]"* — fires when Details hits the 1 000-row cap.

The dashboard box itself shows no date / compare / group / export controls.

### Export flow (modal / 2FA)

Clicking **Export** opens a modal (with an *"Include comparison data (separate csv file)"* checkbox when a comparison is active), then a 2FA step ([[account-cc2fa]]) requiring a 6-digit email/TOTP code — auto-submitted as `cc` when 2FA is disabled. The CSV is then generated asynchronously, the merchant gets an email, and the file appears in [[settings-import-history]]. Export limit: **150 000 rows**. The dashboard card caches its data for **60 seconds**, invalidating on any range/compare change.

## Settings & fields

This box has **no box-specific settings**. It inherits the page-wide Date range, Compare, and Group controls described under the toolbar above. Its visibility and position are controlled through the dashboard layout configuration (shown/hidden, reordered) like any other Analytics box.

## Business rules

### Status filter is fixed for this box (the alert is literally true)

The permanent alert *"Data is visualized according to the default statuses in Settings and cannot be changed → Paid, Completed, Pending, Authorized payment, Fulfilled"* is accurate for this box. The vendor figures are pre-aggregated with that exact, fixed status set (`paid OR completed OR authorized OR (pending AND not_fulfilled) OR fulfilled`), so changing Settings → Analytics → used statuses does **not** widen this report. This differs from boxes such as [[analytics-top-order-discounts]], where the Settings status list does apply.

### Deleted and no-vendor products

- **Deleted / renamed vendors still appear** under their last-known name, but their drill-down link is suppressed (no live vendor page to open).
- **Products with no vendor are excluded entirely** — their revenue silently does not appear in this ranking. A store selling only no-vendor products sees this box permanently empty.

### Amount aggregates by product line-item

The amount sums product line-item amounts, not full order subtotals — so a single order touching multiple vendors contributes **proportionally** to each vendor's row. The same order line also feeds the per-product and per-category sales boxes (see [[analytics-top-categories-by-sales]]); they share one source, grouped by a different field. The View More chart pre-generates every date bucket, so zero-sales days appear as 0-amount points rather than gaps.

### Details sessions come from a separate data source

The **Views / Sessions** column on Details is fetched from vendor-page traffic data, populated independently of the sales figures. If the traffic ingest is lagging, the conversion rate can look inconsistent for the most recent days. Verify against ingest status before treating a low recent conversion rate as real.

### Empty state and fixed limits

A store with no orders in the used statuses returns no rows and the card shows a "No data" placeholder. The top-5 count, the 1 000-row Details cap, and the 150 000-row export limit are all fixed — none are merchant-adjustable.

## How it works

Slug `top-brands-by-sales` provides three views — Dashboard, Details, and View More — all reading the same pre-aggregated vendor-sales data, under permission `reports` / `reports.analytics` (and `reports` / `reports.reports`). Endpoints (same shape as Categories):

- `GET /admin/api/analytics/dashboard/top-brands-by-sales`
- `GET /admin/api/analytics/details/top-brands-by-sales`
- `GET /admin/api/analytics/details/top-brands-by-sales/extended/{vendor_id}`

## Related

- [[analytics]] — parent hub.
- [[analytics-top-categories-by-sales]] — structurally identical sister box, grouped by category_id instead of vendor_id.
- [[analytics-details]] — generic Details sub-screen.
- [[analytics-full]] — generic View More sub-screen.
- [[apps-brands-distribution]] — separate brands-distribution app feature.
- [[vendor]] — entity (canonical "brand" in CloudCart).
- [[settings-statuses]] — defines the order statuses included in the "used statuses" filter.


## Open questions

_None._
