---
type: feature
nav_path: "Analytics → Dashboard shell"
route_name: analytics
route_path: /admin/analytics
aliases: ["Analytics dashboard shell", "Analytics boxes loading", "Analytics service unavailable", "Analytics empty state", "Analytics kill switch"]
tags: [analytics, dashboard, ccanalytics, loading, kill-switch]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[analytics]]. See the hub for the other aspects (date & compare, settings panel, box catalog, industry compare, data freshness).

# Analytics — dashboard shell & box loading

## Purpose

This aspect covers the **shell** of the Analytics dashboard at `/admin/analytics` — the container that decides whether the dashboard mounts at all, how the individual boxes load, what the merchant sees while they load or fail, and the platform-wide switches that can take the whole dashboard offline. It is the "is the screen even working" page; what each box *contains* is in [[analytics-overview-box-catalog]].

## Where to find it

Top-level sidebar entry **Analytics**, route `/admin/analytics`. The shell renders the dashboard only when `disabled.cca` is NOT set on the server config; otherwise it short-circuits to the service-unavailable banner described below.

## What the merchant can do here

- See the dashboard boxes appear progressively as each loads its own data.
- Read a per-box error message if one box's query is too heavy for the selected period.
- Encounter the service-unavailable banner if ops has switched the dashboard off.

## Settings & fields

The shell itself has no configurable fields — the date picker, Compare selector and Settings cog are documented in [[analytics-overview-date-compare]] and [[analytics-overview-settings]]. The shell's observable states are:

| State | Trigger | What the merchant sees |
|-------|---------|------------------------|
| Normal | `disabled.cca` unset, data exists | Boxes render progressively. |
| Per-box timeout | One box's query exceeds the platform 504 threshold | *"We cannot generate statistics for the selected period, please reduce it."* on that box only. |
| Empty | Aggregation has not yet produced data for the range | *"No data available for the selected range."* per box. |
| Service unavailable | A kill switch is active (see Business rules) | A banner instead of (or covering) the boxes. |

## Business rules

### Async box loading

The dashboard does NOT load every box's data eagerly. The shell loads the box configuration first (sort, statuses, hash); each box then fetches its own data via `GET /admin/api/analytics/dashboard/{box}?dateFrom=...&dateTo=...&compare=...` independently. Boxes appear progressively and a slow one doesn't block the others.

If a box query takes longer than the platform's 504 threshold, that box (and only that box) shows: *"We cannot generate statistics for the selected period, please reduce it."* The fix the merchant should try is narrowing the date range.

### Empty-state UX for new stores

If the analytics aggregation has not yet produced data (a brand-new store, or one where the aggregation hasn't completed its first run after install), each box shows the standard no-data message: *"No data available for the selected range."* No skeletons, no spinners after the first paint — just the empty alert.

The aggregation runs hourly (the `cc_analytics_aggregation` recurring job visible in [[settings-queue-view]], on a one-hour cycle). So a brand-new store will see boxes start filling in within ~1 hour of the first order / visit. The full timing model is in [[analytics-overview-data-freshness]] and the end-to-end pipeline in [[analytics-pipeline]].

### Platform-wide kill switches

Two ops-level switches can take the entire dashboard offline (three behaviours):

| Switch | Effect | Where the merchant sees it |
|--------|--------|----------------------------|
| `disabled.cca` server config flag | The Vue shell short-circuits BEFORE the dashboard mounts | *"Due to technical reasons, the service is temporarily unavailable. We appreciate your patience and understanding."* (alert at the top, no boxes load) |
| `uuid.disableInSiteCp` (global disable message in the analytics service config) | The API returns a 400 with the message for every dashboard / details / view-more / more-details / industry-statistic call | Same banner, but specifically when the API responds — not the Vue gate |
| `uuid.disabled_sites` (an array of site IDs in the ops config) | Per-site opt-out — every read AND every write short-circuits. Per-order analytics jobs log a warning and skip the upsert. | The dashboard mounts but every box is empty / "No data available" |

These are NOT merchant-configurable. Currently the `disabled_sites` array contains a single internal test site; the `disableMessage` is empty. If a merchant reports "Analytics is down / all empty" and nothing changed on their side, these switches are the first thing for support to check.

## Related

- [[analytics]] — hub.
- [[analytics-overview-box-catalog]] — what each box contains and how they render.
- [[analytics-overview-data-freshness]] — the hourly aggregation that fills empty boxes.
- [[analytics-pipeline]] — end-to-end data flow + per-box latency table.
- [[analytics-details]] — drill into a single box.

## Open questions

_None._
