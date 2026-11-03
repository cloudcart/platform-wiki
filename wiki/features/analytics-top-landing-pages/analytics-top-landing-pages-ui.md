---
type: feature
nav_path: "Analytics → Landing pages by visits"
route_name: analytics
route_path: /admin/analytics
aliases: ["Landing pages by visits UI", "Landing pages dashboard box", "Landing pages Details table", "Landing pages ViewMore chart", "Целеви страници — интерфейс"]
tags: [analytics, ccanalytics, landing-pages, traffic, top-landing-pages]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 7
---

> Part of [[analytics-top-landing-pages]]. See the hub for the other aspects (data source / attribution, export + cache).

# Landing pages by visits — UI surface

## Purpose

Documents everything the merchant sees and clicks in the **Landing pages by visits** box: the dashboard top-5 table, the full Details table, the per-page ViewMore chart, and the page-wide date / compare / group / export toolbar. What a "view" means and where the numbers come from is in [[analytics-top-landing-pages-data-source]]; the CSV export flow is in [[analytics-top-landing-pages-export]].

## Where to find it

Analytics dashboard → **Landing pages by visits** box. `navigationSort: 16.1`. Box `key: "landing-pages"`, box `type: "table"` — a top-5 ranked table with per-row mobile/desktop tooltips. Clicking the box title opens **Details**; clicking a page row drills into a per-date time-series chart (**ViewMore**).

## What the merchant can do here

- See the top 5 most-visited content pages (homepage + content pages) on the Analytics dashboard, with mobile/desktop split.
- Click the box title to open **Details** — a paginated table of every page visited in the period.
- Click any page row (including the homepage) to drill into **ViewMore** — a per-date traffic chart for that single page.
- Change the **date range** — the box re-fetches.
- Compare against the **previous period** (dashed-line overlay on the ViewMore chart).
- Filter Details by specific page ids (passing `[0]` shows only the homepage).
- Export Details / ViewMore data as CSV (see [[analytics-top-landing-pages-export]]).

## Settings & fields

### Dashboard box (top 5)

| Element | What it is |
|---------|------------|
| Title row | EN: "Landing pages by visits" / BG: "Landing pages by visits" (BG title not translated — falls back to EN) |
| Each of the top 5 rows | Page name (linked), `meta.row4` views chip ("Views {value}"), per-device split tooltip |
| Row sort | Total views DESC |
| Row count limit | 5 (the platform code) |

The "Home page" row is a special case (page-id `0`, rendered with the store's primary site URL) — see [[analytics-top-landing-pages-data-source]].

### Details screen (full table)

Columns shown (EN labels with BG):

| Column key | EN label | BG label |
|------------|----------|----------|
| `page_name` | Name | Заглавие |
| `views` | Views / Sessions | Посещения / Сесии |

Default sort: `views` DESC. Page size: `DETAILS_PAGINATION_LIMIT = 100`. `details.group = false` (one row per page).

The Details and ViewMore for landing pages have **only views columns** (no orders / units / amount / conversion_rate) — this box does not join with the orders dataset. For revenue-side data on the same page dimension, see [[analytics-landing-pages-by-sales]].

The `page_name` column uses the `PageLink` helper for linking. The `views` column is currently a plain number cell (a commented `VisitsLink` component exists in the JS source — replacement is planned per the inline comment). (verify)

### ViewMore (per-page over time)

Clicking a page row in Details opens a per-date breakdown for that single page. Columns:

| Column key | EN label | BG label |
|------------|----------|----------|
| `date` | Date | Дата |
| `views` | Views / Sessions | Посещения / Сесии |

`hasViewMoreChart: true` — purple-filled area chart (`rgb(141, 88, 224)`) plots views over time. Comparison (previous period) overlay renders as dashed grey when the compare picker is not `"no"`. The Date column uses the `DateGroup` component, formatted via the dateFormat helper per the period picker.

ViewMore tooltip (EN): *"{count} view for {date}|{count} views for {date}"*. BG: *"{count} посещение за {date}|{count} посещения за {date}"*.

### Vue box configuration

| Key | Value | Meaning |
|-----|-------|---------|
| `key` | `landing-pages` | Box identifier. |
| `type` | `table` | Renders as ranked table. |
| `collectDataFrom` | `2023-01-01` | Earliest date where data exists. |
| `viewMore` | `true` | Has per-row time-series drill-down. |
| `hasDetails` | `true` | Has Details paginated screen. |
| `hasViewMoreChart` | `true` | Charts views over time. |
| `navigationSort` | `16.1` | Position on dashboard. |
| `details.group` | `false` | One row per page. |
| `details.defaultSorting` | views DESC | Default Details sort. |

### Details / ViewMore toolbar (every UI control)

| Control | Where | What it does | Plan / config gate |
|---------|-------|--------------|----------------------|
| **Date range picker** | Top-left toolbar | Re-fetches. | Capped by `cc_analytics.compare_range` (default 12 months). |
| **Compare select** | Next to date picker | `No comparison` / `Previous period` / `Previous year`. | Plan-gated by `cc_analytics.allow_period_compare`. Always rendered. |
| **Group select** | Next to compare | `Hourly` / `Daily` / `Weekly` / `Monthly` / `Quarterly` / `Yearly` / `None`. Visible on ViewMore; hidden on Details (`details.group: false`). | Auto-filters: **Hourly hidden if range > 7 days**, **Daily hidden if range > 90 days**. |
| **Export link** | Top-right (cloud-download) | Triggers ExportModal + 2FA flow — see [[analytics-top-landing-pages-export]]. | Hidden when `allowExport: false` (perm `reports.reports_export`). |
| **Force-limit banner** | Above table | *"This report shows up to {total} results. To see all results, you can [Export]"* | Fires when ViewMore is capped at 1000 rows (the landing-pages ViewMore explicitly slices intervals at `DETAILS_FORCE_LIMIT`). |

## Business rules

- **Traffic boxes have no status-filter alert** — no order data is involved, so the order-status filter banner that appears on sales boxes is absent here.
- **The dashboard box itself shows no date / compare / group / export controls** — those controls are page-wide and only appear on the Details / ViewMore screens.
- **The homepage row is drillable** — unlike some sibling boxes, the homepage (page-id `0`) has a non-null `viewMore` value and can be clicked into a ViewMore chart. See [[analytics-top-landing-pages-data-source]] for why.
- **ViewMore caps at 1000 rows** — intervals are pre-generated date buckets sliced at `DETAILS_FORCE_LIMIT = 1000`; beyond that the merchant is steered to Export.

## Related

- [[analytics-top-landing-pages]] — hub.
- [[analytics-top-landing-pages-data-source]] — what a "view" means + where the numbers come from.
- [[analytics-top-landing-pages-export]] — CSV export modal / 2FA / queue / client cache.
- [[analytics-landing-pages-by-sales]] — sister box; same page dimension ranked by revenue.
- [[account-cc2fa]] — 2FA modal used by the export flow.
- [[settings-import-history]] — where finished export files land.
- [[analytics]] — parent hub.

## Open questions

_None._
