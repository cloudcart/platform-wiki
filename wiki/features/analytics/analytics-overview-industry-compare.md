---
type: feature
nav_path: "Analytics → Industry comparison"
route_name: analytics
route_path: /admin/analytics
aliases: ["Industry comparison", "Industry average line", "Analytics benchmark", "Industry average", "hasIndustryCompare", "Cross-store comparison"]
tags: [analytics, dashboard, industry, benchmark, ccanalytics, plan-gates]
plan_gates: ["cc_analytics.allow_industry_compare"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[analytics]]. See the hub for the other aspects (dashboard shell, date & compare, settings panel, box catalog, data freshness).

# Analytics — industry-average comparison

## Purpose

This aspect covers the **industry-average comparison line** — the dotted benchmark overlay that lets a merchant see how their store performs against the platform average for stores in the same industry. It explains when the line is drawn, which boxes support it, how often the benchmark recalculates, and the important rule that the benchmark ignores the merchant's own statuses filter.

## Where to find it

The benchmark line appears inline on supported chart boxes on the Analytics dashboard (`/admin/analytics`) when the `cc_analytics.allow_industry_compare` plan feature is on. The industry it compares against is set in the Settings panel — see [[analytics-overview-settings]].

## What the merchant can do here

- Set the store's primary industry in the Settings panel so the benchmark is relevant.
- Read the dotted industry-average line on chart boxes that declare `hasIndustryCompare: true`.
- Hover a data point to see how far above or below the industry average the value sits.

## Settings & fields

| Field / Control | What it does | Notes |
|-----------------|--------------|-------|
| Industry (Settings panel) | Selects which industry's average the benchmark uses. | Drawn from `site.industries`; defaults to `site.main_industry`. See [[settings-general-industry]]. |
| `cc_analytics.allow_industry_compare` (plan gate) | Enables the benchmark line and triggers the `/admin/api/analytics/statistic` fetch. | When off, the industry line is hidden. CloudCart employees always have it on. See [[plan-gates]]. |
| `hasIndustryCompare` (per box) | Whether a given box draws the industry line at all. | Set per box in the box configuration — see [[analytics-overview-box-catalog]]. |

## Business rules

### Industry-average comparison

When `cc_analytics.allow_industry_compare` is on, the dashboard fetches `GET /admin/api/analytics/statistic` to get the cross-store industry averages for the configured `mainIndustry`. The result is cached client-side for 3600 seconds (`analytics.statistic`). Charts with `hasIndustryCompare: true` then overlay a dotted "industry average" line. Hovering shows: *"For period {period} {title}: {value} where is {percent} above the average for {industry}"* (or "below").

### Weekly recalculation

The industry statistic recalculates platform-wide once a week (`cc_analytics_site_industry_statistic` job, 604800-second interval). Changing the store's industry won't show new values until the start of next week — a common source of "I changed my industry but the benchmark didn't move" tickets.

### Industry comparison uses platform-default statuses, not the merchant's filter

When the industry-statistic recurring job calculates the cross-store averages it uses a **fixed set of statuses (Paid, Completed, Pending, Authorized, Fulfilled)** — NOT the merchant's saved Settings-panel selection. So a merchant who unticks "Pending" from their analytics statuses (see [[analytics-overview-settings]]) still gets compared to industry peers whose Pending orders are counted. This is intentional: it keeps the cross-merchant comparison apples-to-apples regardless of each merchant's status preferences. It also means the merchant's own line and the benchmark line can be computed over slightly different status sets — expected, not a bug.

### Distinct from the Compare overlay

The industry-average line is a **cross-store** benchmark. It is different from the **Compare: Previous period / year** overlay, which plots the same store's own prior data and is gated by a different plan feature — see [[analytics-overview-date-compare]].

## Related

- [[analytics]] — hub.
- [[analytics-overview-date-compare]] — the separate same-store Compare overlay and its plan gate.
- [[analytics-overview-settings]] — where the industry and statuses are chosen.
- [[analytics-overview-box-catalog]] — `hasIndustryCompare` per box.
- [[settings-general-industry]] — the store's main industry selection.
- [[settings-queue-view]] — the weekly `cc_analytics_site_industry_statistic` recurring job.
- [[plan-gates]] — `cc_analytics.allow_industry_compare` plan feature.

## Open questions

_None._
