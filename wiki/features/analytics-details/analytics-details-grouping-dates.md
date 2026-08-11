---
type: feature
nav_path: "Analytics → Details → Grouping & Dates"
route_name: analytics.details.subView
route_path: /admin/analytics/details/:box/:id
aliases: ["Details grouping", "Time grouping", "Hourly daily weekly monthly", "Auto-grouping", "Date range parsing", "Групиране по време", "Времеви интервал"]
tags: [ccanalytics, analytics, details, grouping, dates, timezone]
plan_gates: ["cc_analytics.compare_range"]
created: 2026-06-10
updated: 2026-06-10
source_count: 9
---
# Details — Grouping & Dates

> Part of [[analytics-details]]. See the hub for the drill-level model and the other aspects (chart & compare, export, access & limits).

## Purpose

This aspect covers the **time-grouping selector** (Hourly … Yearly / None) and how the Details screen parses the **date range** — including the server-side auto-grouping ladder that downgrades grouping for wide ranges and the store-timezone snapping that keeps date framing consistent across staff locations.

## Where to find it

Analytics dashboard → **View details** on a box → the **Group** dropdown and the **date-range picker** sit with the Compare control at the top of the Details screen.

## What the merchant can do here

- Pick a time grouping for the chart: Hourly, Daily, Weekly, Monthly, Quarterly, Yearly, or None.
- Pick a date range with the picker — refreshes both the chart and the table.
- Rely on the selector self-filtering its options as the range widens (so an impossible choice like Hourly over a year is never offered).

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| Group | `hourly` / `daily` / `weekly` / `monthly` / `quarterly` / `year` (Yearly) / `none`. | `hourly` (overridable from the URL). | Hidden when the box sets `details.group: false`. Options re-filter as the range changes: Hourly dropped above 7 days, Daily above 90 days. |
| Date range | Two dates (from/to). | The standard global default range (last 30 days). | Maximum look-back capped by `cc_analytics.compare_range` plan feature (12 months default). |

The group selector renders only if the box opts in via `details.group` (defaults to `true` for `chart`-type boxes).

## Business rules

### UI option filtering

The grouping selector re-filters its own options as the date range changes: **Hourly** is dropped above 7 days, **Daily** is dropped above 90 days. So the merchant cannot pick a grouping the range can't support.

### Server-side auto-grouping ladder

The merchant can pick `Hourly`, but the chart smartly downgrades if the range is wide. Server-side group-type guessing enforces:

| Range | Forced grouping |
|-------|-----------------|
| < 3 days | Hourly |
| 3 – 60 days | Daily |
| 61 – 90 days | Daily (capped — UI hides Hourly above 7) |
| 91 – 730 days | Monthly |
| > 730 days | Yearly |

If `group = auto` (the dashboard box default), the server picks one automatically by this same rule.

### Date-range parsing uses the store's primary timezone

The `dateFrom` / `dateTo` query parameters are parsed in the **store's timezone** (the `site.timezone` setting) — `startOfDay` / `endOfDay` snap to local midnight of that timezone. The values returned to the Vue (`dateFrom`, `dateTo` in the JSON envelope) come back as store-timezone-converted ISO8601 strings. So a staff member viewing the dashboard from a different timezone sees consistent date framing regardless of their browser locale.

### Re-fetch on change

Changing the date range, compare, or group debounces 500 ms then re-fetches and resets pagination to page 1, so a wider range can't surface stale page-2 data from a narrower one.

## Related

- [[analytics-details]] — hub.
- [[analytics-details-chart-compare]] — the grouping drives the chart's time axis; the previous-period math also depends on the range.
- [[settings-general]] — the store `site.timezone` setting used to parse the date range.
- [[plan-gates]] — `cc_analytics.compare_range` caps the maximum look-back.

## Open questions

_None._
