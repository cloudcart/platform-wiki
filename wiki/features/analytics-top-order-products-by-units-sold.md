---
type: feature
nav_path: "Analytics → Products by units sold"
route_name: analytics
route_path: /admin/analytics
aliases: ["Products by units sold", "Top products by units sold", "Best-selling products by units", "Top sellers by quantity", "Продукти по количество", "Най-продавани продукти по количество"]
tags: [analytics, ccanalytics, orders, products, top-order-products-by-units-sold]
plan_gates: []
created: 2026-05-22
updated: 2026-06-10
source_count: 8
---
# Products by units sold

## Purpose

Answers: **which products move the most physical units?** Ranks the catalog by **total quantity** (sum of units across all matching order lines in the period). The companion box [[analytics-top-order-products-by-sales|Products by sales]] ranks by revenue instead. Use this box to see what is flying off the shelf irrespective of price — for inventory planning, restocking, and finding popular-but-cheap items that do not rank high on revenue.

Tooltip (EN / BG): *"Products with the most individual units sold. The data is visualized according to the following statuses of orders - Paid, Completed, Pending, Authorized payment, Fulfilled."* / *"Най-продавани продукти според продадено количество. Данните се визуализират спрямо следните статуси на поръчки - Платена, Изпълнена, Изчакваща, Оторизирано плащане, Изпратена."*

**The status set is platform-fixed** — the Settings → Analytics order-status picker does NOT control this box. It is the only Analytics box that surfaces its hardcoded-status policy in the UI: a permanent inline alert above the Details table reads (EN) *"Data is visualized according to the default statuses in Settings and cannot be changed → Paid, Completed, Pending, Authorized payment, Fulfilled"*.

## Where to find it

Analytics dashboard. Box title: **"Products by units sold"** (EN+BG, no BG translation). `navigationSort` is 10 — next to **Products by sales**.

## What the merchant can do here

- See the top 5 products by **physical units sold** on the dashboard — independent of price.
- Open the **Details** screen — paginated table of the top 1000 distinct products by quantity, with the inline platform-status alert.
- Open **ViewMore** on a product row — per-date time-series plotting **quantity** over time (instead of amount).
- Filter Details by product IDs (multi-select), sort by units / orders / amount / conversion rate, export to CSV.
- Compare against the previous period — the chart overlays a dashed comparison line.
- Use the view for inventory planning and restocking ([[inventory-tracking]]).

## What the merchant sees

### Dashboard box (top 5)

Each row is one product. The primary value (`aggregate`) is `quantity`; the meta row (`meta.row1`) is total revenue as money ("Amount X" EN / "Сума X" BG). This is **mirrored vs Products by sales**, where amount is primary and quantity is the meta. Sort: `quantity` DESC, then `sales` DESC. Limit 5.

### Details screen (full table)

Columns:

| Column key | EN label | BG label |
|------------|----------|----------|
| `product_name` | Name | Заглавие |
| `views` | Views / Sessions | Посещения / Сесии |
| `orders` | Orders | Поръчки |
| `quantity` | Units | Количество |
| `amount` | Amount | Сума |
| `conversion_rate` | Conversion rate | Conversion rate |

Default sort: `quantity` DESC, `sales` DESC. Page size 100, force-limited to 1000 distinct products. The status alert renders above the table.

### ViewMore (per-product time-series)

Per-date breakdown for one product. Columns match Details plus a leading `date` (Date / Дата) column. `hasViewMoreChart` is true, but the chart plots `quantity` instead of `amount` — the only chart difference from Products by sales. Tooltip (EN): *"{quantity} units from {count} order for {date}|{quantity} units from {count} orders for {date}"*.

### Toolbar controls (Details / ViewMore)

| Control | What it does | Plan / config gate |
|---------|--------------|----------------------|
| **Date range picker** | Re-fetches the rows. | Capped by `cc_analytics.compare_range` (default 12 months). |
| **Compare select** | `No comparison` / `Previous period` / `Previous year`. | `cc_analytics.allow_period_compare`. |
| **Group select** | `Hourly` … `Yearly` / `None`. Visible only on ViewMore. | Hourly hidden if range > 7 days; Daily hidden if range > 90 days. |
| **Export link** | Triggers ExportModal + 2FA flow. | Hidden when `allowExport: false` (perm `reports.reports_export`). |
| **Force-limit banner** | *"This report shows up to {total} results. To see all results, you can [Export]"* | Fires when Details is capped at 1000 rows. |

The dashboard box shows no date / compare / group / export controls — those are page-wide.

### Export flow (modal / 2FA / queue)

1. Click **Export** → if compare ≠ `no`, ExportModal opens with checkbox *"Include comparison data (separate csv file)"*; if compare = `no`, straight to 2FA.
2. **CC2FaAction modal** ([[account-cc2fa]]) — 6-digit code (email or TOTP). If 2FA is disabled, auto-submits with code `cc`.
3. POST `/admin/api/import-export/export_analytics` → toast *"The export is being processed. You will receive an email with the download link."*
4. The export writes the CSV(s), emails the merchant; the file appears in [[settings-import-history]]. Row limit: **150 000 rows**.

The dashboard box caches results client-side for 60 seconds, invalidating on range/compare change or `cacheHash` update.

## Settings & fields

| Key | Value | Meaning |
|-----|-------|---------|
| `key` | `top-order-products-by-units-sold` | Box identifier |
| `type` | `table` | Table layout |
| `viewMore` | `true` | Has per-row time-series |
| `hasDetails` | `true` | Has Details screen |
| `hasViewMoreChart` | `true` | Time-series chart (plots quantity) |
| `navigationSort` | `10` | Position right after Products by sales |
| `details.defaultSorting` | `quantity` DESC, `sales` DESC | Default Details sort |
| `details.viewMore.group` | `true` | ViewMore groups by date bucket |

The box wires both a top-level `alerts.details` and an inline `details.alert` returning the same platform-status warning. Products by sales and [[analytics-top-order-bundles-by-sales|Bundles by sales]] reuse this box's alert and Details formatter blocks.

## Business rules

### Same data, different ranking

This box and Products by sales read from the **same** pre-aggregated daily collection. The only differences are the sort key (`quantity` here, `amount` there) and the primary/meta mapping. ViewMore uses the hourly series for hourly grouping, daily otherwise.

### Status filter is hardcoded at ingest

The set baked into the per-day aggregation is **Paid, Completed, Authorized payment, OR (Pending AND not fulfilled), OR Fulfilled**. There is no per-store override and the box cannot be widened from Settings → Analytics — the inline Details alert (quoted under Purpose) announces it.

### Force-limit at 1000 distinct products

If the period has more than 1000 distinct products, Details truncates to the top 1000 by quantity (`DETAILS_FORCE_LIMIT = 1000`).

### Product-ID filter

The multi-select `ids` parameter restricts to those product IDs; without it the query returns all products with a positive ID.

### Variants roll up into the parent product

Variants are aggregated at ingest; rows group by product only. A product with 10 colour variants shows as one row with the summed quantity — per-variant rankings are not surfaced here. See [[inventory-tracking]] for the per-variant stock model.

### Deleted products excluded

Order lines whose product no longer exists are ingested with a product ID of 0 and filtered out of every query — their units are silently dropped from this ranking.

### Empty state

When the period has no matching orders, the dashboard shows the standard "No data" placeholder and Details renders an empty table (`total = 0`). No first-sale carve-out for this box.

### Pagination count asymmetry

The Details count groups by product only (not by product + name like Products by sales). If the same product appears under two names in the period, the row count can differ by one between the two boxes — a minor support edge case.

## Related

- [[analytics]] — parent hub (does NOT control this box's status set).
- [[analytics-top-order-products-by-sales]] — sibling box, same data ranked by revenue.
- [[analytics-top-order-bundles-by-sales]] — sibling box for bundles.
- [[analytics-landing-pages-by-sales]] — sibling traffic box.
- [[product]] — entity page for products.
- [[inventory-tracking]] — practical use case for this box (restocking decisions).

## Open questions

_None._
