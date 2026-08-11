---
type: feature
nav_path: "Analytics → Data freshness & storage"
route_name: analytics
route_path: /admin/analytics
aliases: ["Analytics data freshness", "Analytics aggregation", "Analytics the analytics store", "Why doesn't my order show", "Device breakdown cutoff", "Analytics permissions", "Analytics retention"]
tags: [analytics, dashboard, ccanalytics, the analytics store, aggregation, permissions]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[analytics]]. See the hub for the other aspects (dashboard shell, date & compare, settings panel, box catalog, industry compare).

# Analytics — data freshness, storage & permissions

## Purpose

This aspect answers the most common Analytics question — *"why doesn't my new order / visit show up yet?"* — by explaining that the dashboard reads **precomputed aggregations** on a roughly hourly cycle rather than querying live store data. It also covers where the data physically lives, how long it is kept, the device-breakdown date cutoff, and the staff permissions that gate the screen.

## Where to find it

This behaviour is invisible on the screen itself — it explains the *numbers* the merchant sees at `/admin/analytics`. For the full end-to-end ingest model (storefront events → raw events → aggregations → boxes) with a per-box latency table, see the concept hub [[analytics-pipeline]].

## What the merchant can do here

- Understand why a just-placed order may not appear in the boxes for up to an hour.
- Know that very old date ranges are still available (data is kept indefinitely).
- Understand why device columns read "N/A" for ranges starting before 17 Jan 2023.
- Know which staff role permissions are required to see the dashboard and its drill-ins.

## Settings & fields

There are no merchant-editable fields in this aspect — it is behaviour, not configuration. The relevant staff permissions are:

| Permission | Gates |
|------------|-------|
| `reports,reports.analytics` | The dashboard and the `GET /admin/api/analytics/dashboard/{box}` endpoint. Staff without it don't see the Analytics sidebar entry. |
| `reports,reports.reports` | The drill-in to [[analytics-details]]. |
| `reports,reports.analytics_settings` | Saving / deleting the Settings panel (see [[analytics-overview-settings]]). |

These are assigned in [[settings-staff]].

## Business rules

### How it works — precomputed, not live

The Analytics dashboard is NOT a live query against the merchant's store data. It's a precomputed cache:

1. The **`cc_analytics_aggregation` recurring job** (visible in [[settings-queue-view]]) runs once per hour. It reads recent orders, visits, products, etc. from the live store, transforms them, and writes denormalised summaries (orders, total orders, top products, visitors, etc.) into the dedicated analytics store.
2. The dashboard hits `GET /admin/api/analytics/dashboard/{box}` for each box; the box reads the matching summary from the analytics store for the date range, applies the merchant's status filter + device toggle, and returns the chart / table payload.
3. The boxes render the result (line chart / bar / funnel / table).
4. Settings (statuses, sorting, devices, industry) are stored as merchant preferences under the `cc_analytics` configuration group — NOT in the analytics store — because they're preferences, not data. See [[analytics-overview-settings]].

So if the merchant adds an order at 10:05 and the aggregation last ran at 10:00, that order won't show until the 11:00 run. The job runs more often in practice (the system picks it up as soon as it's free to run again), but **1 hour is the worst-case freshness expectation**. The per-box latency detail is in [[analytics-pipeline]].

### Where the analytics data physically lives

Aggregations live in a dedicated analytics store — separate from the main store database and from the platform's other data stores. This isolation means:

- Heavy dashboard queries cannot starve the live storefront database.
- A store-database incident does not blank the dashboards (cached aggregations keep showing).
- Conversely, an analytics-cluster incident does NOT affect order placement / checkout (the per-order job just queues up and catches up later).

The aggregation collections are **kept indefinitely** — there is no TTL on the rolled-up data. A merchant on the platform for 5 years can chart 5 years back. The trade-off is that aggregation indexes grow linearly with merchant lifetime.

### Device breakdowns require period to start on or after 17 Jan 2023

The device-breakdown columns (desktop / mobile / tablet — toggled by Show devices in [[analytics-overview-settings]]) are only meaningful if the date range starts on or after **17 January 2023** — the day the storefront tracker started recording the device of each visit. If the picked period starts earlier, every device value on every box is replaced with literal **"N/A"** for the whole period.

This is silent: the columns still appear, just filled with N/A. A merchant who picks "All time since 2020" on a long-running store sees N/A for devices on every row — the fix is to set `dateFrom >= 2023-01-17`.

## Related

- [[analytics]] — hub.
- [[analytics-pipeline]] — concept hub on the end-to-end pipeline + per-box latency table.
- [[analytics-overview-dashboard]] — the empty-state UX shown until the first aggregation completes.
- [[analytics-overview-settings]] — the Show devices toggle that interacts with the 17-Jan-2023 cutoff.
- [[settings-staff]] — staff role permissions for `reports.analytics`, `reports.reports`, `reports.analytics_settings`.
- [[settings-queue-view]] — the `cc_analytics_aggregation` recurring job.

## Open questions

_None._
