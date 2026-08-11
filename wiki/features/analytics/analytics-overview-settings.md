---
type: feature
nav_path: "Analytics → Settings panel"
route_name: analytics
route_path: /admin/analytics
aliases: ["Analytics settings", "Analytics settings panel", "Analytics statuses filter", "Show devices", "Show boxes sort", "Analytics cache hash", "Analytics reset to default"]
tags: [analytics, dashboard, settings, statuses, cache, ccanalytics]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[analytics]]. See the hub for the other aspects (dashboard shell, date & compare, box catalog, industry compare, data freshness).

# Analytics — Settings panel

## Purpose

This aspect covers the per-merchant **Settings panel** behind the cog icon (top right) of the Analytics dashboard. It decides which order statuses count toward the numbers, whether device-breakdown columns show, which industry the store benchmarks against, and the visibility + order of the boxes. It also covers how those preferences are saved, reset, and cached — including the `cacheHash` that invalidates downstream caches the moment the merchant saves.

## Where to find it

Cog icon at the top right of the Analytics dashboard (`/admin/analytics`). Opening it reveals the fields below. Settings are stored as merchant preferences (under the `cc_analytics` configuration group) — NOT in the analytics data store — and re-fetched on every dashboard load.

## What the merchant can do here

- Choose which order statuses count toward sales / orders / customers / conversion.
- Set the store's primary industry for the benchmark line.
- Toggle device-breakdown columns on or off.
- Reveal a drag-and-drop list to reorder and hide boxes.
- **Save** the panel (writes immediately) or **Reset to default** (wipes the whole `cc_analytics` group and restores platform defaults).

## Settings & fields

| Field | What it controls | Default |
|-------|------------------|---------|
| **Order statuses that will be included in the analyses** | Multi-select of order statuses (e.g., Paid, Completed, Pending, Authorized payment, Fulfilled). Only orders with the picked statuses count. The list cannot be empty (the multiselect has `canClear: false`). | The store's currently-used statuses (the statuses the store has actually applied to orders). |
| **Please select a primary branch, which is most suitable for your business** | The store's industry (single-select from `site.industries`). Used for the industry-average comparison line — see [[analytics-overview-industry-compare]]. | The current `site.main_industry`. |
| **Show devices** | Toggle — when ON, table boxes include a device breakdown column (desktop / mobile / tablet); when OFF, those columns are hidden. (Device values still depend on the 17-Jan-2023 cutoff — see [[analytics-overview-data-freshness]].) | ON |
| **Show boxes sort** | Reveals the drag-and-drop list of boxes with per-box visibility toggles. Persisted in a 30-day cookie called `showSorting`. | OFF (cookie unset) |
| **Default boxes sorting** | The full ordered list of boxes with a `visible` flag per box; supports nested children (e.g., the "Abandoned carts" parent holds "Abandoned checkout" as a child). See [[analytics-overview-box-catalog]]. | The platform's default box order. |

The footer of each box shows the current statuses filter as chip-text: *"Statuses: Paid, Completed, Pending, Authorized payment and Fulfilled"*. The last status is joined with "and" (per the `Statuses: {statuses}` translation and `and {value}` join), with proper plural / locale handling. This is read directly from the statuses selection above.

## Business rules

### Save vs Reset to default

The merchant's **Save** writes the preferences immediately to the `cc_analytics` configuration group. **Reset to default** wipes the whole `cc_analytics` group and restores the platform defaults (and deletes the cache hash). A 600-second client-side cache (the saved-settings cache) avoids the round-trip on quick re-renders.

### Cache hash

When the merchant saves Settings, a new 32-character random `cacheHash` is generated and stored. This hash is passed into every box render and into the API call query string — so downstream HTTP caches and the browser's response cache are invalidated immediately on settings change. Same effect on **Reset to default** (cache hash deleted along with the config).

### Cache hash + cache TTLs

| Cache | Where | TTL | Invalidation |
|-------|-------|-----|--------------|
| Saved-settings cache | Browser (per-merchant) | 600 s | On any Save / Reset in Settings panel |
| Plan-features cache | Browser (per-merchant) | 600 s | On Settings save (clearing the analytics features cache) |
| Period-compare feature cache | Browser, Details / ViewMore / MoreDetails screens | 600 s | On Settings save |
| Industry-averages cache | Browser | 3600 s | On Settings save / industry change |
| Each box's data | None server-side — every `/admin/api/analytics/dashboard/{box}` hit reads straight from the analytics store | n/a | The 32-char random `cacheHash` is appended to every box request so any saved Settings change invalidates browser-level HTTP / SW caches |

### Statuses filter scope

The statuses chosen here apply to the merchant's own dashboard numbers. They do NOT apply to the cross-store industry benchmark, which uses a fixed status set — see [[analytics-overview-industry-compare]].

## Related

- [[analytics]] — hub.
- [[analytics-overview-box-catalog]] — the boxes the sort list reorders.
- [[analytics-overview-industry-compare]] — where the industry selection feeds the benchmark line.
- [[analytics-overview-data-freshness]] — the device-breakdown cutoff that the Show devices toggle interacts with.
- [[settings-statuses]] — the order-status list the statuses filter draws from.
- [[settings-general-industry]] — the store's main industry selection.

## Open questions

_None._
