---
type: feature
nav_path: "Analytics → Categories by sales"
route_name: analytics
route_path: /admin/analytics
aliases: ["Categories by sales", "Top categories by sales", "Best-selling categories", "Категории по продажби", "Най-продавани категории"]
tags: [analytics, ccanalytics, orders, category, top-categories-by-sales]
plan_gates: []
created: 2026-05-22
updated: 2026-06-10
source_count: 8
---
# Categories by sales

## Purpose

A ranked table of the merchant's **best-selling product categories by revenue** for the selected time range. Answers: *"Which categories actually drive my sales — by amount, not just units?"* The dashboard box surfaces the top 5 categories with each category's total amount, units sold, order count, and a mobile/desktop split, plus a drill-down to a per-day revenue-trend chart.

It is the sales-amount counterpart to its sibling **"Top categories by traffic"** (sessions / views); merchants compare the two to spot under-monetised traffic.

## Where to find it

Sidebar → **Analytics** dashboard. The box is titled **"Categories by sales"** and sits between Brands (Vendors) and Landing pages in the default layout (`navigationSort: 14`), with its child box **"Top categories by traffic"** directly beneath it.

From the box the merchant can click a category name (opens its storefront page), **View more →** on a row (per-category revenue-over-time chart), or **See details** (the full **Details** screen with paginated list and CSV/Excel export).

## What the merchant can do here

### Dashboard card

Lists the **top 5 categories** ranked by sales amount descending (units sold as secondary sort). Each row shows:

| Field | What it shows |
|-------|---------------|
| Name | Category name (last-known — a renamed category shows its most recent name), linking to the storefront category page. |
| Units | Product units sold within the category. |
| Sales | Total sales amount, in the store's currency. |
| Orders | Orders that contained the category, with a mobile/desktop split bar (tooltip "Orders: {total}"). |

Deleted categories still appear (see Business rules) but are not drill-down enabled.

### Tooltip (box-level)

**EN**: *"Best-selling categories of the total value of the products as an amount. The data is visualized according to the following statuses of orders - Paid, Completed, Pending, Authorized payment, Fulfilled."*

**BG**: *"Най-продавани категории от общата стойност на продуктите като сума. Данните се визуализират спрямо следните статуси на поръчки - Платена, Изпълнена, Изчакваща, Оторизирано плащане, Изпратена."*

### Details (full list) — `/admin/analytics/details/top-categories-by-sales`

Paginated table (100/page, hard cap **1 000** rows). Columns:

| EN label | BG label | What it shows |
|----------|----------|---------------|
| Name | Заглавие | Hyperlinked category name |
| Views / Sessions | Посещения / Сесии | Sessions for this category over the period |
| Orders | Поръчки | Distinct orders containing the category |
| Units | Количество | Units sold (sum) |
| Amount | Сума | Total sales amount |
| Conversion rate | Конв. процент | Orders ÷ Views, as a percentage |

Default sort: amount desc, then orders desc. Period-over-period comparison is supported (when Compare ≠ `No comparison`); previous-period figures show alongside.

A permanent yellow alert above the table reads (EN): *"Data is visualized according to the default statuses in Settings and cannot be changed → Paid, Completed, Pending, Authorized payment, Fulfilled"* — accurate for this box (see Business rules).

### View More (per-category trend) — `/admin/analytics/full/top-categories-by-sales/:category_id`

Line chart of the chosen category's amount over time, grouped by hour / day / week / month / quarter / year depending on the date range. Tooltip: *"{amount} from {count} order for {date}"* (singular/plural aware). The compared period overlays as a dashed line when enabled.

### Page-header controls (Details / View More)

These live on the Analytics page header, not on the dashboard card:

| Control | Options / behaviour | Gate |
|---------|---------------------|------|
| **Date range** | Re-fetches for the chosen period. | Capped by `cc_analytics.compare_range` (default 12 months). |
| **Compare** | `No comparison` / `Previous period` / `Previous year`. | `cc_analytics.allow_period_compare`. |
| **Group** | `Hourly` … `Yearly` / `None`. Shown on View More, hidden on Details. | Hourly hidden if range > 7 days; Daily hidden if range > 90 days. |
| **Export** | Opens the export flow. | `reports.reports_export` permission. |

A **force-limit banner** (*"This report shows up to {total} results. To see all results, you can [Export]"*) appears when Details hits the 1 000-row cap.

### Export flow

**Export** opens a modal (with a *"Include comparison data (separate csv file)"* checkbox when a comparison is active), then requires a 6-digit two-factor code ([[account-cc2fa]]) — auto-submitted if 2FA is off. The export is queued (*"The export is being processed. You will receive an email with the download link."*) and the finished CSV(s) are emailed and listed in [[settings-import-history]]. Export row limit: **150 000 rows**.

The dashboard card caches its result for **60 seconds** on the client.

## Settings & fields

The box has no merchant-configurable settings of its own. It is driven by the Analytics page-header controls above (date range, compare, group, currency). Amounts inherit the store currency.

Whether the box is shown is governed by the per-user **Analytics dashboard layout** preference (Settings → Analytics → Dashboard layout), stored under `cc_analytics.defaultBoxesSorting`.

## Business rules

### Status filter is fixed for this box

The data is pre-filtered to orders matching `Paid`, `Completed`, `Authorized`, `Pending` (with `not_fulfilled` fulfillment), or `Fulfilled` fulfillment. Unlike most analytics boxes, the **Settings → Analytics "used statuses" choice does NOT affect this box** — the filter is baked into the source data, so the in-box alert ("cannot be changed") is literally accurate here. Contrast [[analytics-top-order-discounts]], which DOES honour the Settings value.

### Amount is per category-line, not per order

A category's amount equals the revenue of that category's product lines, not whole-order subtotals. An order spanning 3 categories splits its revenue across 3 rows; there is no "primary category" rollup. Each product line is recorded under exactly ONE category — the product's assigned-at-order-time category — even if the product belongs to several categories in the catalogue.

### Uncategorised and deleted categories

Products ordered with no category are recorded under `category_id = 0` and excluded from the ranking — stores that allow uncategorised products see that revenue silently disappear. A renamed or removed category keeps appearing under its last-seen name/URL (the one on its last order); a deleted category loses its drill-down link.

### Conversion rate is computed, not stored

Conversion rate is Orders ÷ Views as a percentage, where Views come from the per-category sessions data. If Views = 0 the rate shows `0%` even when there were orders (treated as no-traffic / direct-link rows).

### Caps, fixed top-5, no subcategory rollup

The dashboard card always shows 5 rows; Details returns at most 1 000 categories (top by amount desc, then orders desc) and silently truncates the rest, while Export can return the full set. By-sales does NOT roll subcategory revenue up into parent categories (that applies only to the traffic box).

### Empty state

Stores with no orders in the matching statuses — or selling only uncategorised products — show a "No data" placeholder.

## Related

- [[analytics]] — parent hub.
- [[analytics-details]] — generic Details sub-screen layout.
- [[analytics-full]] — generic View More sub-screen layout.
- [[analytics-top-brands-by-sales]] — sister "Vendors by sales" box (same shape, different group field).
- [[analytics-top-order-discounts]] — box that DOES honour the Settings used-statuses choice (contrast).
- [[apps-brands-distribution]] — sales-by-vendor surface in the brands app.
- [[category]] — entity.
- [[products-categories]] — parent merchant-facing page for managing categories.
- [[settings-statuses]] — order statuses included in the "used statuses" filter.
- [[account-cc2fa]] — two-factor step in the export flow.
- [[settings-import-history]] — where finished exports land.

## Open questions

_None._
