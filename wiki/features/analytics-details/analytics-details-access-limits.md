---
type: feature
nav_path: "Analytics → Details → Access & Limits"
route_name: analytics.details.subView
route_path: /admin/analytics/details/:box/:id
aliases: ["Details permissions", "Analytics access", "Details pagination", "Compare 404", "Analytics kill switch", "Device N/A cutoff", "Достъп до детайли"]
tags: [ccanalytics, analytics, details, permissions, pagination, limits]
plan_gates: ["cc_analytics.allow_period_compare"]
created: 2026-06-10
updated: 2026-06-10
source_count: 9
---
# Details — Access & Limits

> Part of [[analytics-details]]. See the hub for the drill-level model and the other aspects (chart & compare, export, grouping & dates).

## Purpose

This aspect covers the gates and hard limits around the Details screen: which **permission** reaches it, the **fixed pagination** size, the **strict `compare` validation** that 404s on a bad value, the **global kill switches** the screen inherits from the dashboard, and the **device-data cutoff** that blanks device columns before 17 January 2023.

## Where to find it

These rules apply to every Details fetch — `/admin/analytics/details/:box`, the sub-view, and the view-more table. They are evaluated server-side per request, so a merchant cannot bypass them by hand-editing the URL.

## What the merchant can do here

- Reach Details with the `reports.reports` permission (Export needs the additional `reports.reports_export`).
- Page through the table with the standard footer control.
- (Nothing else configurable here — this aspect is the guardrails, not a control surface.)

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| Page | Pagination page index for the table. | 1 | Page size fixed server-side at the platform code rows / page. Persisted in the URL (`?page=N` for `N > 1`). |
| Compare (validation) | Accepts only `no` / `period` / `year`. | `no` | Any other value → HTTP 404 for the whole fetch. |

## Business rules

### Permission

Reaching Details requires `hasApiPermission:reports,reports.reports`. The Export action requires the additional `reports.reports_export`. Both gates are evaluated server-side per request, so a staff member without permission can still try the URL but gets a 403 from the API. See [[settings-staff]].

### Pagination

Server-side pagination is fixed at `DETAILS_PAGINATION_LIMIT = 100` rows / page; the table footer shows the standard pagination control. The page index is persisted in the URL (`?page=N` for `N > 1`), so bookmark / share preserves position.

### Compare validation — only `no`, `period`, `year`

The `compare` query parameter is server-validated: any value other than `no`, `period`, or `year` returns **HTTP 404** for the whole details fetch. A hand-tampered URL like `?compare=quarterly` produces an immediate 404; the screen renders empty with no fallback. (Same on [[analytics-full]] and [[analytics-more-details]].) The Compare control itself is plan-gated by `cc_analytics.allow_period_compare` — see [[analytics-details-chart-compare]].

### Same kill switches as the dashboard

The Details endpoint inherits the dashboard's global kill switches:

- `disabled.cca` (server config) → the Vue Index shell short-circuits before mount.
- `uuid.disableInSiteCp` (analytics service message) → the API returns 400 with the message.
- `uuid.disabled_sites` containing the site_id → no merchant-visible message specifically here, but the per-order chain that fed the data was already short-circuited, so the table is empty with "No data".

### Device columns show "N/A" before 17 Jan 2023

If the picked range starts before **17 January 2023** (the day device data started flowing into the events collection), every device-breakdown cell on every table row is replaced with literal "N/A". The columns still appear; they're just unfilled for that period. The boundary is checked on the *period start*, so a range of `2022-12-15 → 2024-03-01` shows N/A devices for the entire range (not just the portion before the cutoff).

## Related

- [[analytics-details]] — hub.
- [[settings-staff]] — `reports.reports` and `reports.reports_export` permissions.
- [[analytics-details-chart-compare]] — the Compare control whose value this aspect validates.
- [[analytics-full]] / [[analytics-more-details]] — share the same compare validation and kill switches.
- [[settings-statuses]] — the order-statuses filter that controls which orders count toward the table.

## Open questions

_None._
