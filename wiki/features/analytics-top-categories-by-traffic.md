---
type: feature
nav_path: "Analytics → Categories by traffic"
route_name: analytics
route_path: /admin/analytics
aliases: ["Categories by traffic", "Top categories by traffic", "Most visited categories", "Категории спрямо посещения", "Топ категории по трафик"]
tags: [analytics, ccanalytics, categories, traffic, top-categories-by-traffic]
plan_gates: []
created: 2026-05-22
updated: 2026-06-10
source_count: 7
---
# Categories by traffic

## Purpose

Shows you which category pages bring the most visitors to your store — ranked by raw category-page views (not orders, not revenue). Every time a shopper lands on a category listing page (the URL that shows all products in a given category) one view is registered for that category.

The "shop aisle" metric: if a category ranks high here but low in [[analytics-top-categories-by-sales]], shoppers are interested in browsing the aisle but not buying — usually a sign the category landing page has the wrong sort order, weak filters, or a confusing product mix. Pair this box with [[analytics-top-products-by-traffic]] to see whether traffic is being absorbed by category browsing or going straight to product detail pages.

Tooltip (EN / BG): *"Top visits categories in your online store."* / *"Най-посещавани категории във Вашия онлайн магазин."*

## Where to find it

Analytics dashboard → **Categories by traffic** box. `navigationSort: 15`.

Box `key: "top-categories-by-traffic"`, box `type: "table"` — top-5 ranked table with per-row mobile/desktop tooltips. Clicking the box opens Details; clicking a category row drills into a per-date time-series chart (ViewMore).

`collectDataFrom: '2023-01-01'` — date ranges earlier than 2023-01-01 return no data.

## What the merchant can do here

- See the top 5 most-viewed category landing pages on the dashboard, with mobile/desktop split.
- Open **Details** — a paginated table (page size 100) of every category page viewed in the period; filter it by specific category ids.
- Drill into **ViewMore** — a per-date traffic chart for one category.
- Change the **date range**, **compare** against the previous period / year, and **group** ViewMore by hour / day / week / month / quarter / year.
- Export Details / ViewMore data as CSV.

## What the merchant sees

### Dashboard box (top 5)

A title row (EN/BG both "Categories by traffic" — the BG title is untranslated and falls back to EN) over up to 5 rows, sorted by total views DESC and limited to 5 (the platform code). Each row shows the linked category name, a units chip ("Unit {value}"), a views chip ("Views {value}"), and a per-device split tooltip.

The dashboard box itself does NOT show date / compare / group / export controls — those are page-wide. The box caches client-side for 60 seconds keyed on route + box + date range + compare mode.

### Details screen (full table)

Columns (key — EN / BG): `page_name` — Name / Заглавие; `views` — Views/Sessions / Посещения/Сесии; `orders` — Orders / Поръчки; `quantity` — Units / Количество; `amount` — Amount / Сума; `conversion_rate` — Conversion rate (untranslated in BG).

Default sort: `views` DESC. Page size: `DETAILS_PAGINATION_LIMIT = 100`. One row per category (no roll-up). The Details column formatters are **reused** from [[analytics-top-categories-by-sales]] so the column rendering matches that box exactly.

### ViewMore (per-category over time)

Clicking a category row in Details opens a per-date breakdown for that single category. Columns: Date / Name / Views/Sessions / Orders / Units / Amount / Conversion rate. Dates are grouped by the period picker.

`hasViewMoreChart: true` — purple-filled area chart (`rgb(141, 88, 224)`) plots views over time. Comparison (previous period) overlay as dashed grey when the compare picker is not `"no"`. ViewMore is capped at `DETAILS_FORCE_LIMIT = 1000` date buckets.

ViewMore tooltip (EN): *"{count} view for {date}|{count} views for {date}"*. BG: *"{count} посещение за {date}|{count} посещения за {date}"*.

### Details / ViewMore toolbar

The Details / ViewMore toolbar carries four controls, all page-wide:

- **Date range picker** — re-fetches; capped by `cc_analytics.compare_range` (default 12 months).
- **Compare select** — `No comparison` / `Previous period` / `Previous year`; plan-gated by `cc_analytics.allow_period_compare` (always rendered).
- **Group select** — `Hourly` / `Daily` / `Weekly` / `Monthly` / `Quarterly` / `Yearly` / `None`; visible on ViewMore, hidden on Details. Auto-filters: **Hourly hidden if range > 7 days**, **Daily hidden if range > 90 days**.
- **Export link** (cloud-download) — triggers the ExportModal + 2FA flow; hidden when `allowExport: false` (perm `reports.reports_export`).

When ViewMore is capped at 1000 rows a banner shows above the table: *"This report shows up to {total} results. To see all results, you can [Export]"*. Traffic boxes have **no status-filter alert** (no order data involved).

### Export flow (modal / 2FA / queue)

1. Click **Export** → ExportModal opens with *"Include comparison data (separate csv file)"* checkbox when compare ≠ `no`; else straight to 2FA.
2. **CC2FaAction modal** ([[account-cc2fa]]) — 6-digit code (email/TOTP); auto-submits `cc` if 2FA off on account.
3. POST `/admin/api/import-export/export_analytics` → toast *"The export is being processed. You will receive an email with the download link."*
4. The export runs asynchronously, writes the CSV(s), and emails the merchant; the file lands in [[settings-import-history]].

Export row limit: **150 000 rows**.

## Settings & fields

### Box configuration

Box `key: "top-categories-by-traffic"`, `type: "table"`, `navigationSort: 15`, `collectDataFrom: "2023-01-01"`. It has Details (`hasDetails: true`) and per-row time-series drill-down (`viewMore: true`, `hasViewMoreChart: true`). `details.group: false` gives one row per category, sorted by views DESC; `details.viewMore.group: true` groups ViewMore dates by the period picker.

### Metric definition — what counts as a "view"

A "view" is **one `viewCategory` event**: one category landing page visit by one visitor. Repeats within the same hour by the same visitor on the same device count as **one** view — see the attribution model under Business rules.

## Business rules

### Attribution model — UUID × hour × device de-duplication

Views are bucketed per hour by `(visitor, hour, category, device)`. Repeat views of the same category by the same visitor on the same device within one hour collapse into a single view; the same visitor returning in a later hour adds another. So refreshing a category page 50 times in one hour → 1 view; coming back next hour → another.

Each bucket carries a `device` (`mobile` or `desktop`, fallback `desktop`); the dashboard rolls these into a `device: { mobile, desktop, total }` object consumed by the per-row tooltip.

### Excluded admin traffic

Visitor ids matching `/^admin-.*/i` are filtered out — admin-panel category previews do not pollute traffic metrics.

### Subcategories vs parent categories

Every category id is its own row — a parent category and its subcategory are two separate rows with no roll-up. Viewing the parent landing page increments the parent's count; viewing a subcategory landing page increments the subcategory's count. To see "all visits under category X including its subtree", filter Details with the full set of subcategory ids.

### Last-known category name / URL

The dashboard shows each category's **most recent** name and URL, so renamed categories display under their current name. Deleted categories keep their `category_id` and the drill-down link is preserved.

### Empty state behaviour

Stores with no category-page visits in the period return a blank card. Stores using flat catalogues (no categories) see this box permanently empty.

### Performance note

For stores with very large category catalogues this is the slowest of the three traffic boxes to load — the categories aggregation does not pin a specific lookup index the way brands-by-traffic and products-by-traffic do. This is a platform-wide property, not a per-store toggle.

### Apply

This box has no per-merchant or per-store overrides. The same hour-uuid-device deduplication, the same admin-traffic exclusion, and the same category definition apply across every store.

## Related

- [[analytics]] — parent hub.
- [[analytics-top-categories-by-sales]] — sister box, ranks categories by revenue (not views); provides the column formatters this box reuses.
- [[analytics-top-products-by-traffic]] — same logic at the product level.
- [[analytics-top-brands-by-traffic]] — same logic at the vendor level.
- [[analytics-top-landing-pages]] — page-level views (homepage + content pages).
- [[category]] — entity page.

## Open questions

_None._
