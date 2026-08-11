---
type: feature
nav_path: "Analytics"
route_name: analytics
route_path: /admin/analytics
aliases: ["Analytics dashboard", "Reports", "Stats", "Sales analytics", "Анализи", "Анализ"]
tags: [analytics, hub, dashboard, ccanalytics, reports]
plan_gates: ["cc_analytics.allow_period_compare", "cc_analytics.allow_industry_compare", "cc_analytics.compare_range"]
created: 2026-05-21
updated: 2026-06-10
source_count: 8
---
# Analytics

## Purpose

The Analytics dashboard is the merchant's main reporting hub — a single screen of **boxes** (cards) summarising sales, orders, customers, visits, conversion, top products, top brands, top categories, landing pages, traffic sources, and geographic distribution for a date range the merchant picks. Each box is a self-contained chart or table built from the store's own data; together they form what most merchants think of as "the dashboard".

The breadcrumb at the top reads simply "Analytics". The page is powered by a separate **analytics subsystem** (its own aggregation pipeline, backed by a dedicated analytics store) — it does NOT query the live store data directly. Data refreshes on a one-hour aggregation cycle, so a sale placed in the last hour may not yet appear in the boxes — see [[analytics-overview-data-freshness]].

This page is the **hub** for the Analytics dashboard cluster. The dashboard is interactive in three layers: the **date-range picker** controls the period for ALL boxes, the **Compare** selector overlays prior-period or prior-year data, and a per-merchant **Settings panel** picks which order statuses to include, whether to show device breakdowns, the store's industry for benchmarking, and the visibility + order of the boxes. Each layer has its own aspect page below.

## Where to find it

Top-level sidebar entry **Analytics**. The route is `/admin/analytics`. The shell displays the dashboard unless the `disabled.cca` server config flag is set, in which case it shows: *"Due to technical reasons, the service is temporarily unavailable. We appreciate your patience and understanding."* See [[analytics-overview-dashboard]] for the shell + kill-switch behaviour.

URL query parameters round-trip into the URL bar: `dateFrom`, `dateTo`, `compare` — so a merchant can bookmark or share a specific view.

## What the merchant can do here

- **Pick a date range** at the top — refreshes ALL visible boxes. See [[analytics-overview-date-compare]].
- **Pick a Compare mode** — `No comparison` (default), `Compare: Previous period`, or `Compare: Previous year`. See [[analytics-overview-date-compare]].
- **Open the Settings panel** (cog icon, top right) to configure statuses, device breakdowns, industry, and box layout. See [[analytics-overview-settings]].
- **Drill into any box** via its `View details` action (only on boxes with `hasDetails: true`) — see [[analytics-details]].
- **Reorder + hide boxes** — see [[analytics-overview-box-catalog]].

## Settings & fields

The dashboard's controls split across three aspect pages:

| Control group | What it covers | Aspect |
|---------------|----------------|--------|
| Date range + Compare | Period picker, prior-period / prior-year overlay, look-back cap, timezone | [[analytics-overview-date-compare]] |
| Settings panel (cog) | Statuses filter, industry, device toggle, box sort, Save / Reset, caches | [[analytics-overview-settings]] |
| Box catalog | The 35 boxes, their types (chart / funnel / bar / table), per-merchant layout | [[analytics-overview-box-catalog]] |
| Returns boxes | Returns over time, Net revenue, Return rate — what the shared returns figure counts | [[analytics-overview-returns-boxes]] |

## Business rules

- The dashboard reads **precomputed aggregations** from the analytics store, not live store data; freshness is up to one hour. See [[analytics-overview-data-freshness]].
- Three **plan features** gate comparisons (`allow_period_compare`, `allow_industry_compare`, `compare_range`); CloudCart employees get all three unlocked. See [[analytics-overview-date-compare]].
- The **industry-average** comparison line uses a fixed status set platform-wide and recalculates weekly. See [[analytics-overview-industry-compare]].
- Boxes load **asynchronously and independently**; a slow box doesn't block the others. See [[analytics-overview-dashboard]].
- The dashboard is gated by staff permission `reports,reports.analytics`. See [[analytics-overview-data-freshness]] + [[settings-staff]].

## Sub-pages (in this cluster)

This screen is split into 7 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[analytics-overview-dashboard]] — the dashboard shell + async box loading; progressive render; per-box 504 timeout message; empty-state UX for new stores; platform-wide kill switches (`disabled.cca`, `disableInSiteCp`, `disabled_sites`).
- [[analytics-overview-date-compare]] — the date-range picker; the `compare` modes (none / previous period / previous year); the three plan gates (`allow_period_compare`, `allow_industry_compare`, `compare_range`); the look-back cap; the store-timezone rule.
- [[analytics-overview-settings]] — the cog Settings panel: statuses filter, industry, Show devices, box sort; Save vs Reset to default; the `cacheHash` + the client-side cache TTL table; the footer statuses chip.
- [[analytics-overview-box-catalog]] — the 35-box catalogue grouped by what they measure; the four box types (chart / funnel / bar / table); the table top-5 limit; per-merchant box layout + how new platform boxes are appended.
- [[analytics-overview-returns-boxes]] — the three returns boxes (Returns over time, Net revenue, Return rate) and the one figure they share: partial returns only, why full returns and cancellations are excluded, why past periods keep their old numbers, and the offset-exchange rule.
- [[analytics-overview-industry-compare]] — the industry-average overlay line; `hasIndustryCompare` per box; the weekly recalculation job; why industry comparison uses platform-default statuses, not the merchant's filter.
- [[analytics-overview-data-freshness]] — how the dashboard reads precomputed aggregations (hourly cycle); where the data physically lives (a dedicated analytics store, kept indefinitely); the 17-Jan-2023 device-breakdown cutoff; staff permissions.

## Related

- [[analytics-pipeline]] — concept hub on the end-to-end data flow (storefront events → raw behavioural events → hourly aggregations → these dashboard boxes). Read this to answer "why doesn't my new order show up yet?" — has the verified per-box latency table.
- [[analytics-details]] — drill into one box (chart + table for that single metric).
- [[analytics-full]] — full paginated list for table boxes (View more).
- [[analytics-more-details]] — third-level drill (e.g., Sales by Source / Medium / Campaign).
- [[settings-staff]] — staff role permissions for `reports.analytics`, `reports.reports`, `reports.analytics_settings`, `reports.reports_export`.
- [[settings-statuses]] — the list of order statuses the merchant can include in the analytics.
- [[settings-general-industry]] — industry selection (the main industry feeds the industry-average line).
- [[settings-queue-view]] — see the `cc_analytics_aggregation` and `cc_analytics_site_industry_statistic` recurring jobs there.
- [[order]] — source data for sales / orders boxes.
- [[customer]] — source data for customer / customer-value boxes.
- [[product]] — source data for product boxes.
- [[category]] — source data for category boxes.
- [[vendor]] — source data for brand (vendor) boxes.
- [[plan-gates]] — concept page on plan-feature flags (`cc_analytics.allow_period_compare`, `allow_industry_compare`, `compare_range`).
- [[plan]] — entity page for the merchant's plan.
- [[multi-currency]] — the store-currency model behind the revenue / sales boxes (and the EUR conversion shown on money figures).
- [[analytics-returning-customers]] — returning-customers box (Total Customers).

- [[analytics-online-store-sessions]]
- [[analytics-percentage-of-orders]]
- [[analytics-sessions-by-country]]
- [[analytics-sessions-by-device]]
- [[analytics-sessions-by-social-source]]
- [[analytics-total-customers]]

## Open questions

_None._
