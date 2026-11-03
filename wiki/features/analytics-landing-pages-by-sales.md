---
type: feature
nav_path: "Analytics → Landing pages by sales"
route_name: analytics
route_path: /admin/analytics
aliases: ["Landing pages by sales", "Top landing pages by sales", "Sales by landing page", "Entry pages by sales", "Целеви страници по продажби", "Лендинг страници по продажби"]
tags: [analytics, ccanalytics, orders, traffic, landing-pages-by-sales]
plan_gates: []
created: 2026-05-22
updated: 2026-06-10
source_count: 8
---
# Landing pages by sales

## Purpose

Answers: **which store pages start the journeys that end in a purchase?** Ranks the **entry pages** (the first page the buyer landed on before placing the order) by **total order revenue**. Different from "Sales by traffic source" — see [[analytics-sales-by-traffic-source]] — which credits the referrer (e.g., google.com); this box credits the **landing page on the merchant's store** itself (a product page, a category page, the home page).

Tooltip (EN / BG): *"Top landing pages where visitors entered your online store and placed an order, depend on selected order statuses in Settings."* / *"Най-популярните страници посещавани във Вашия онлайн магазин, на които е попаднал клиентът и е реализирал поръчка. Данните се визуализират спрямо избраните статуси на поръчки в Настройки."*

Unlike the Products / Bundles by-sales boxes (which use a hardcoded status set), this box honours the merchant's Settings → Analytics → Order statuses picker — see [[analytics]].

## Where to find it

Analytics dashboard. Box title: **"Landing pages by sales"** (EN+BG identical). Dashboard position `navigationSort` is 16.

The date picker only allows selection from **January 1, 2023 onwards** (`collectDataFrom = '2023-01-01'`) — data collection began on that date.

## What the merchant can do here

- See the **top 5** entry pages ranked by **order revenue** on the dashboard box.
- Click the box to open **Details** — a paginated table (page size 100) of all distinct landing pages that produced orders in the period.
- Click any row to open **ViewMore** — a per-date time-series of orders + revenue for that single landing page, with a chart.
- Click a page name to navigate to the actual landing page on the storefront.
- Filter Details by specific landing pages and export to CSV.
- Pick a period (Jan 1 2023 onwards) and compare against the previous period or previous year.

## Settings & fields

### Dashboard box (top 5)

Each row is one landing page, sorted by revenue DESC, limit 5:

- `name` — page title, or **"Home page"** for the home-page fallback row.
- `aggregate` — total revenue from orders that started on this page (`amount_without_shipping` — **shipping excluded**, same as the Sales-by-Source boxes).
- `meta.row1` — orders count, formatted "Order X / Orders X" (BG: "Поръчка X / Поръчки X").
- `device` — mobile / desktop order split.

### Details / ViewMore columns

| Column key | EN label | BG label |
|------------|----------|----------|
| `page_name` (Details) / `date` (ViewMore) | Name / Date | Заглавие / Дата |
| `sales` | Orders | Поръчки |
| `amount` | Amount | Сума |

Details lists landing pages (sort falls back to revenue DESC; the `page_name` cell is clickable to the storefront landing page); ViewMore lists dates for one page and plots `amount` as a chart (purple fill, dashed grey for the comparison period).

### Details / ViewMore toolbar controls

| Control | What it does | Gate |
|---------|--------------|------|
| **Date range picker** | Re-fetches. | Capped by `cc_analytics.compare_range` (default 12 months). |
| **Compare select** | `No comparison` / `Previous period` / `Previous year`. | Plan-gated by `cc_analytics.allow_period_compare`. |
| **Group select** | `Hourly` / `Daily` / `Weekly` / `Monthly` / `Quarterly` / `Yearly` / `None`. Shown on ViewMore, hidden on Details. | **Hourly hidden if range > 7 days**; **Daily hidden if range > 90 days**. |
| **Export link** | Triggers ExportModal + 2FA flow. | Hidden without perm `reports.reports_export`. |
| **Force-limit banner** | *"This report shows up to {total} results. To see all results, you can [Export]"* | Fires when ViewMore is capped at 1000 rows. |

The dashboard box itself shows no date / compare / group / export controls — those are page-wide. **No status-filter alert appears on this box** even though it is an orders box; the status filter is still applied behind the scenes. The box key is `landing-pages-by-sales`.

## Business rules

### Attribution is async — populated ~1 hour AFTER the order

Each order initially records its landing page as empty. A background job (queued with a **1-hour delay**) then looks up the buyer's traffic-source events, finds the first page-view, and back-fills the landing page. **Until that job completes, the order is invisible to this box** — new orders typically appear ~1 hour after completing, later than the visit-side boxes.

If the buyer has no recorded page-view events (cookie deleted, or tracking blocked), the job re-queues instead of writing an empty attribution. In effect, **orders from buyers with broken tracking never get attributed** — they appear in neither this box, nor [[analytics-sales-by-traffic-source]], nor [[analytics-orders-by-social-source]].

### Seven landing-page types

The tracker emits seven page-view event types, each mapping to a landing-page `record_type`:

| `record_type` | `record_id` |
|---------------|-------------|
| `home` | always `0` |
| `page` (Content Page) | page id |
| `category` | category id |
| `product` | product id |
| `collection` | collection id |
| `vendor` | vendor id |
| `search` | always `0` |

So the table can include any of the seven types, not only the home page + content pages. A search-results page where the buyer first landed shows as a `search` row.

### Home-page fallback

When no specific product / category page was recorded (`record_id == 0`), the row shows `page_name = 'Home page'` — **hardcoded, not translated** (it appears as "Home page" even in the BG admin) — with the URL being the store's primary frontend URL from [[settings-domains]]. Orders with no explicit landing page are still credited to this row.

### Status filter — driven by Settings → Analytics → Order statuses

The dashboard and Details views apply the merchant's status picker (unlike the by-sales Products / Bundles boxes). **ViewMore is asymmetric**: its per-date time-series ignores the status picker and shows **all** orders for that landing page, regardless of the selected statuses. Could be intentional (the full traffic story for one page) or a bug — flagged in Open questions.

Unlike the Products / Bundles boxes, Details runs the full unbounded paginated list (no force-limit cap).

### Export flow

1. Click **Export** → ExportModal opens (with an *"Include comparison data (separate csv file)"* checkbox when comparison is on; otherwise straight to 2FA).
2. **CC2FaAction** modal — see [[account-cc2fa]] — 6-digit code; auto-submits `cc` if 2FA is off on the account.
3. The export queues, with toast *"The export is being processed. You will receive an email with the download link."* (queue `export7`).
4. The CSV(s) generate async; the merchant gets an email with the download link; the file is listed in [[settings-import-history]].

Export queue limit: **150 000 rows**.

### Client-side cache

The dashboard box caches its result for **60 seconds**, keyed by route, box, date range, and comparison mode.

## Related

- [[analytics]] — parent hub; controls the order-status set this box uses.
- [[analytics-sales-by-traffic-source]] — sibling box, credits the referrer instead of the landing page.
- [[analytics-orders-by-social-source]] — sibling box, credits source / medium / campaign.
- [[analytics-top-order-products-by-sales]] — sibling Products box.
- [[settings-domains]] — primary frontend URL used for the home-page fallback.
- [[settings-import-history]] — where exported CSVs land.
- [[account-cc2fa]] — 2FA gate on export.
- [[product]] — `product` is the most common landing-page type.
- [[category]] — `category` is the second most common type.
- [[order]] — order entity page.

## Open questions

- ViewMore ignores the Settings → Analytics status picker while Dashboard / Details honour it — confirm whether this asymmetry is intentional.
