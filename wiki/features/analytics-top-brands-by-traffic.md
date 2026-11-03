---
type: feature
nav_path: "Analytics → Manufacturers by traffic"
route_name: analytics
route_path: /admin/analytics
aliases: ["Manufacturers by traffic", "Vendors by traffic", "Top vendors by traffic", "Top brands by traffic", "Производители по трафик", "Топ марки по посещения"]
tags: [analytics, ccanalytics, brands, vendors, traffic, top-brands-by-traffic]
plan_gates: []
created: 2026-05-22
updated: 2026-06-10
source_count: 7
---
# Manufacturers by traffic

## Purpose

Shows which brand / manufacturer pages bring the most visitors to your store — ranked by raw brand-page views (not orders, not revenue). This is the **vendor-page version** of the Products-by-traffic box: each time a shopper lands on a brand's landing page (the URL listing all products from a given vendor), one view is registered for that vendor.

Useful for catalogues with many brands: a brand ranking high here without corresponding [[analytics-top-brands-by-sales]] revenue signals shoppers click through to the brand listing but don't convert (flat product grid with no editorial content, expensive flagships driving bounces, many out-of-stock variants).

Tooltip (EN / BG): *"Top visits vendors in your online store."* / *"Най-посещавани производители във Вашия онлайн магазин."*

> **Naming note** — the platform uses **"brand", "vendor", "manufacturer"** interchangeably for the same [[vendor|Vendors]] entity. The UI label is "Manufacturers" (EN) / "Производители" (BG). The box key uses `brands`; the JS default title is `Vendors by traffic` (the EN lang file overrides it to "Manufacturers by traffic" in both languages).

## Where to find it

Analytics dashboard → **Manufacturers by traffic** (dashboard position `navigationSort: 13`). Box `key: "top-brands-by-traffic"`, rendered as a top-5 ranked table with per-row mobile/desktop tooltips.

`collectDataFrom: '2023-01-01'` — date ranges earlier than 2023-01-01 return no data.

Clicking the box title opens **Details**; clicking a brand row drills into **ViewMore** (per-date time-series chart for that one brand).

## What the merchant can do here

- See the top 5 most-viewed brands on the dashboard, with mobile/desktop split.
- Click the box title → **Details**: a paginated table (page size 100) of every brand viewed in the period.
- Click any brand row → **ViewMore**: a per-date traffic chart for that single brand.
- Change the **date range** (the box re-fetches); compare against the **previous period** (dashed overlay on the ViewMore chart).
- Filter Details by specific vendor ids; export Details / ViewMore as CSV.

## Settings & fields

### What the merchant sees

**Dashboard box (top 5)** — each row shows the brand name (linked), a `meta.row1` units chip ("Unit {value}"), a `meta.row4` views chip ("Views {value}"), and a per-device tooltip "Visits: {total}" (EN) / "Посещения: {total}" (BG). Sorted by total views DESC; capped at 5 rows. Date / compare / group / export controls are page-wide, not on the box itself.

**Details screen** — full table, default sort `views` DESC, one row per brand. Columns (column key → EN / BG label):

| Column key | EN label | BG label |
|------------|----------|----------|
| `page_name` | Name | Заглавие |
| `views` | Views / Sessions | Посещения / Сесии |
| `orders` | Orders | Поръчки |
| `quantity` | Units | Количество |
| `amount` | Amount | Сума |
| `conversion_rate` | Conversion rate | Conversion rate (untranslated) |

Column rendering is reused from [[analytics-top-brands-by-sales]], so the columns match that box exactly.

**ViewMore (per-brand over time)** — dates grouped by the period picker. Columns: Date / Name / Views/Sessions / Orders / Units / Amount / Conversion rate. A purple-filled area chart (`rgb(141, 88, 224)`) plots views over time; the previous-period overlay shows dashed grey when the compare picker is not `"no"`. Tooltip (EN): *"{count} view for {date}|{count} views for {date}"*; BG: *"{count} посещение за {date}|{count} посещения за {date}"*.

### Details / ViewMore toolbar

| Control | What it does | Gate |
|---------|--------------|------|
| **Date range picker** | Re-fetches. | Capped by `cc_analytics.compare_range` (default 12 months). |
| **Compare select** | `No comparison` / `Previous period` / `Previous year`. | Plan-gated by `cc_analytics.allow_period_compare`; always rendered. |
| **Group select** | `Hourly` / `Daily` / `Weekly` / `Monthly` / `Quarterly` / `Yearly` / `None`. Visible on ViewMore; hidden on Details. | **Hourly hidden if range > 7 days**, **Daily hidden if range > 90 days**. |
| **Export link** | Triggers the export modal + 2FA flow. | Hidden when the `reports.reports_export` permission is absent. |
| **Force-limit banner** | *"This report shows up to {total} results. To see all results, you can [Export]"* | Fires when ViewMore is capped at 1000 rows. |

Traffic boxes have **no status-filter alert** (no order data involved).

### Box configuration keys

| Key | Value | Meaning |
|-----|-------|---------|
| `key` | `top-brands-by-traffic` | Box identifier. |
| `type` | `table` | Renders as a ranked table. |
| `collectDataFrom` | `2023-01-01` | Earliest date with data. |
| `viewMore` | `true` | Has per-row time-series drill-down. |
| `hasDetails` | `true` | Has the Details paginated screen. |
| `hasViewMoreChart` | `true` | Charts views over time. |
| `navigationSort` | `13` | Dashboard position. |
| `details.group` | `false` | One row per brand. |
| `details.viewMore.group` | `true` | ViewMore groups dates by the period picker. |
| `details.defaultSorting` | views DESC | Default Details sort. |

### Export flow

1. Click **Export** → if compare ≠ `no`, a modal opens with an *"Include comparison data (separate csv file)"* checkbox; otherwise straight to 2FA.
2. **CC2FaAction modal** ([[account-cc2fa]]) — 6-digit code (email/TOTP); if 2FA is off on the account, it auto-submits with code `cc`.
3. The export is queued; a toast shows *"The export is being processed. You will receive an email with the download link."*
4. The merchant gets an email with the CSV(s); the file also appears in [[settings-import-history]].

Export limit: **150 000 rows**.

## Business rules

### What counts as a "view"

A "view" is **one brand-page visit** captured by visitor tracking, deduplicated per **visitor × hour × device**: one visitor refreshing the brand page 50 times within one hour counts as **one** view; coming back the next hour adds another.

### Mobile / desktop split

Each view carries a `device` value (`mobile` or `desktop`; `desktop` is the fallback when the browser device is unknown), rolled into the per-row "Visits" tooltip.

### Excluded admin traffic

Admin previews of brand pages are filtered out and do not inflate vendor traffic.

### Renamed vendors show the most recent name

Rows display the **last-recorded** name and storefront URL. If a vendor is renamed mid-period, the row shows the most recent name and slug.

### Deleted vendors keep their drill-down

A deleted vendor keeps the id recorded at view time, so its ViewMore drill-down still works. This differs from the by-sales (orders) data, where a hard-deleted catalogue entity can collapse to a `-1` vendor id.

### Empty state

Stores with no vendor-page visits in the period show a blank card with a "No data" placeholder. Stores that don't use vendors as a catalogue concept see this box permanently empty.

### Drill-down levels and caps

| Level | Returns |
|-------|---------|
| Dashboard | Top 5 brands |
| Details | Full paginated table (page size 100) of all viewed brands in the period |
| ViewMore | Per-date series for one vendor, capped at 1000 rows |
| Details / ViewMore export | Unpaginated CSV |

The dashboard box caches its result for 60 seconds. This box has no per-merchant or per-store overrides — the same deduplication and admin-exclusion rules apply across every store.

## Related

- [[analytics]] — parent hub.
- [[analytics-top-brands-by-sales]] — sister box, ranks brands by revenue (not views); provides the column formatters this box reuses.
- [[analytics-top-products-by-traffic]] — same logic at the product level.
- [[analytics-top-categories-by-traffic]] — same logic at the category level.
- [[analytics-top-landing-pages]] — page-level views (homepage + content pages).
- [[vendor]] — entity page (a.k.a. brand / manufacturer).

## Open questions

_None._
