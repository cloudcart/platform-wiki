---
type: feature
nav_path: "Analytics → Bundles by sales"
route_name: analytics
route_path: /admin/analytics
aliases: ["Bundles by sales", "Top order bundles by sales", "Top bundles by sales", "Best-selling bundles", "Пакети по продажби", "Най-продавани пакети"]
tags: [analytics, ccanalytics, orders, bundles, top-order-bundles-by-sales]
plan_gates: []
created: 2026-05-22
updated: 2026-06-10
source_count: 8
---
# Bundles by sales

## Purpose

Answers: **which product bundles drive the most revenue?** Same shape as [[analytics-top-order-products-by-sales]] but ranks the [[bundles-list|bundle]] entity instead of individual products. A bundle is a fixed grouping of products the merchant offers as a single SKU with a single bundled price ("starter pack", "gift set"). This box tells the merchant which bundles convert into actual paid orders.

Tooltip (EN): *"Best-selling bundles by their total value from all orders. The data is visualized according to the following statuses of orders - Paid, Completed, Pending, Authorized payment, Fulfilled."* (no BG translation — bundle strings fall back to EN).

**The Settings → Analytics order-status picker does NOT control this box** — it uses the same hardcoded status set as the by-sales Products boxes (see Business rules).

## Where to find it

Analytics dashboard. Box title: **"Bundles by sales"** (EN+BG identical — `bundle` strings are not localised). Dashboard position is `navigationSort` 9 (same as Products by sales; sidebar order is then sub-sorted alphabetically by title).

## What the merchant can do here

- See the **top 5 revenue-generating bundles** on the Analytics dashboard.
- Click the box to open the **Details** screen — paginated table of the top 1000 distinct bundles by revenue, sortable by name / orders / units / amount, exportable to CSV, and filterable by specific bundle IDs (multi-select).
- Click a bundle row to open **ViewMore** — per-date time-series plotting revenue over time for that single bundle.
- Compare against the previous period — the chart overlays a dashed comparison line.

## What the merchant sees

### Dashboard box (top 5)

Each row is one bundle, identical layout to Products by sales: total bundle revenue (in store currency); units sold, formatted "Unit X / Units X" (BG: "Количество X") — **for bundles this is a line-count, not a unit-count**, see Business rules; and the mobile / desktop order split. Sorted by revenue DESC, limit 5. The dashboard box shows no date / compare / group / export controls — those are page-wide (Details / ViewMore only).

### Details screen (full table)

Columns: **Name** (Заглавие), **Views / Sessions** (Посещения / Сесии), **Orders** (Поръчки), **Units** (Количество), **Amount** (Сума), **Conversion rate**. Default sort by revenue DESC; page size 100, force-limited to 1000 distinct bundles. The "Views / Sessions" column renders blank for bundles (no per-bundle view tracking — see Business rules).

Above the table sits the permanent yellow alert: *"Data is visualized according to the default statuses in Settings and cannot be changed → Paid, Completed, Pending, Authorized payment, Fulfilled"* — literally true for this box. A force-limit banner appears when capped at 1000 rows: *"This report shows up to {total} results. To see all results, you can [Export]"*.

### ViewMore (per-bundle time-series)

Per-date breakdown for one bundle. Columns: **Date** (Дата), **Views / Sessions**, **Orders**, **Amount**, **Units**, **Conversion rate**. The chart plots revenue; empty days appear as zero-rows. Tooltip (EN): *"{amount} from {count} order for {date}|{amount} from {count} orders for {date}"*.

### Details / ViewMore toolbar (every UI control)

| Control | What it does | Plan / config gate |
|---------|--------------|----------------------|
| **Date range picker** | Re-fetches. | Capped by `cc_analytics.compare_range` (default 12 months). |
| **Compare select** | `No comparison` / `Previous period` / `Previous year`. | Plan-gated by `cc_analytics.allow_period_compare`. Always rendered. |
| **Group select** | `Hourly` / `Daily` / `Weekly` / `Monthly` / `Quarterly` / `Yearly` / `None`. Visible on ViewMore; hidden on Details. | **Hourly hidden if range > 7 days**, **Daily hidden if range > 90 days**. |
| **Export link** | Triggers ExportModal + 2FA flow. | Hidden when `allowExport: false` (perm `reports.reports_export`). |

### Export flow (modal / 2FA / queue)

1. Click **Export** → ExportModal *"Include comparison data (separate csv file)"* checkbox when comparing; else straight to 2FA.
2. **CC2FaAction modal** ([[account-cc2fa]]) — 6-digit code; auto-submits if 2FA is off on the account.
3. Toast: *"The export is being processed. You will receive an email with the download link."*
4. The CSV(s) are written asynchronously; the merchant gets an email and the file appears in [[settings-import-history]].

Export row limit: **150 000 rows**. The dashboard box caches client-side for **60 seconds** per date-range + compare combination.

## Settings & fields

| Key | Value | Meaning |
|-----|-------|---------|
| `key` | `top-order-bundles-by-sales` | Box identifier |
| `type` | `table` | Table layout |
| `viewMore` | `true` | Has per-row time-series |
| `hasDetails` | `true` | Has Details screen |
| `hasViewMoreChart` | `true` | Time-series chart (plots amount) |
| `navigationSort` | 9 | Dashboard position |
| `details.defaultSorting` | `amount` DESC, `sales` DESC | Default Details sort |

This box reuses the [[analytics-top-order-products-by-units-sold]] column formatters (including its hardcoded-status alert), but shows units as the primary metric with amount as meta (inverse of the units-sold layout) and plots revenue in the ViewMore chart.

## Business rules

### Status filter is hardcoded — Settings has no effect

The status set is fixed when the bundle data is pre-aggregated: **Paid OR Completed OR Authorized payment OR (Pending AND not fulfilled) OR Fulfilled**. The Settings → Analytics → Order statuses picker does NOT change this box. Same fixed set as the by-sales Products boxes.

### Amount is the bundle line value

Revenue is the **bundle line value** (price × bundle quantity), summed across the order's bundle line-items.

### A bundle is treated as one entity — and double-counts with Products

When a customer buys a bundle, the order carries multiple line-items (one per constituent product). This box groups those lines into **one row per bundle sale** and sums their line totals. The constituent products ALSO appear individually in [[analytics-top-order-products-by-sales]], so **a single bundle sale contributes to BOTH boxes**. "Total sales of bundle X" and "sum of sales of the products inside bundle X" therefore do not cancel out — they double-count. This is intentional.

### Bundle "units" = line-count, not purchase-count

The Units metric for a bundle counts the **number of constituent product lines**, not how many bundles were bought. A "Starter Pack × 1" containing 3 products reports Units = 3, not 1. So "Unit X" on the dashboard means **product lines included**, not units of the bundle sold.

### No per-bundle view tracking

Storefront visits to a bundle are recorded against the underlying product page, so the "Views / Sessions" column is always blank for bundles.

### Bundle ID filtering & deleted bundles

Without a filter the box includes every bundle with a valid ID; the multi-select Details filter restricts to chosen bundle IDs. Bundles with no valid ID are excluded from the dashboard. If a bundle's base product is later deleted, its historical sales still appear (recorded against the order-time bundle ID); renamed bundles display their most recent name.

### Empty state

Empty period → blank card. Stores that don't use bundles see this box permanently empty unless hidden via Settings → Analytics → Dashboard layout.

## Related

- [[analytics]] — parent hub; does NOT control this box's status set.
- [[analytics-top-order-products-by-sales]] — sibling box, products instead of bundles; a bundle sale double-counts into it.
- [[analytics-top-order-products-by-units-sold]] — sibling box; source of the inherited column formatters.
- [[bundles-list]] — bundle entity listing.
- [[apps-bundles-overview-new]] — Bundles app overview.
- [[account-cc2fa]] — 2FA step in the export flow.
- [[settings-import-history]] — where exported CSV files land.
- [[order]] — order entity page.

## Open questions

_None._
