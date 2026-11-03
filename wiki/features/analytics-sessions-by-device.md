---
type: feature
nav_path: "Analytics → Online store sessions by device type"
route_name: analytics
route_path: /admin/analytics
aliases: ["Online store sessions by device type", "Sessions by device", "Sessions by device type", "По устройство", "Сесии по тип устройство"]
tags: [analytics, ccanalytics, visitors, sessions, sessions-by-device]
plan_gates: []
created: 2026-05-22
updated: 2026-05-27
source_count: 7
---
# Online store sessions by device type

## Purpose

A table that breaks down the period's store sessions by **device category** — mobile, desktop, tablet, etc. — and shows the absolute count + percentage of total visits coming from each. The "mobile vs desktop diagnostic" table: it lets the merchant see in one glance what fraction of traffic is on mobile vs desktop and whether that mix is shifting. Complements the **Total Visits** box ([[analytics-online-store-sessions]]) — same underlying data, exploded by device.

## Where to find it

Analytics dashboard → **Online store sessions by device type** box (`navigationSort: 25`, far down in the detail-table section).

## What the merchant can do here

- Read a **ranked table** of devices (sorted by session count descending), each with its **absolute count** and **percentage of total**.
- Compare the **current period vs previous period** counts in comparison mode.
- Change the **date range** and **grouping**; the table re-aggregates.
- Up to **5 rows** are shown.

The box has no Details drill-down — what you see is the full table.

### Box card surface (table-type)

| Surface | When it appears | What it does |
|---------|-----------------|--------------|
| **Box title** | Always | "Online store sessions by device type" (EN) / Bulgarian equivalent. Plain text — no children, no dropdown selector, no `title_details` morph. |
| **Box tooltip** | Not configured | This box does NOT define a `tooltip.boxTip` label, so no dotted-underline tooltip appears next to the title. |
| **Top 5 ranked rows** | Always | Up to 5 rows. Per row: device name (plain text), current count, percentage. |
| **Pie chart footer** (`device-diagram`) | When the dashboard returns the top-level mobile/desktop % object for this box | Two small pie-charts at the bottom of the card showing the desktop-vs-mobile share, each with its colored arc and the percentage below. |
| **No drill-down** | — | No back arrow, no "View details", no "View more" — the dashboard module is the only view. No industry-compare. |
| **No-data state** | Empty range | "No data available for the selected range." |
| **Period-cutoff alert** | `dateFrom` < `2023-01-01` | "There is no data for the selected period. Please select a period after 01.01.2023 to view data." |
| **504 timeout** | API HTTP 504 | "We cannot generate statistics for the selected period, please reduce it." |

### Dashboard Settings panel (cog icon)

- **Order statuses** / **Industry** — no effect (this box reads visit events, not orders, and has no industry-compare).
- **Show devices** — toggling OFF suppresses the pie-chart footer; the rows themselves (which ARE devices) remain visible.
- **Show boxes sort** — drag/visibility tree; can hide this card or move it within the table-type group.
- **Reset to default / Save / Cancel** — dashboard-wide semantics.

## Settings & fields

### Box configuration (Vue)

| Property | Value | Meaning |
|----------|-------|---------|
| `key` | `sessions-by-device` | Unique box identifier. |
| `type` | `table` | Renders as a sorted table, not a chart. |
| `collectDataFrom` | `2023-01-01` | Earliest date with traffic-source data. |
| `navigationSort` | `25` | Display position; near the bottom of the dashboard. |

### Table columns

| Column | Source field | Formatter | Notes |
|--------|--------------|-----------|-------|
| Device name | `name` (= `device`) | none | "mobile", "desktop", "tablet", "ipad", or whatever the tracker reported. |
| Current count | `aggregate` | `numberFormat` | Number of sessions in the period. |
| Percent | derived | `percentFormat` | This row's `aggregate` ÷ total of all rows. |

### Possible device values

| Device | Source |
|--------|--------|
| `mobile` | Tracker detected a mobile-phone user-agent. |
| `desktop` | Tracker detected a desktop browser. |
| `tablet` | Tracker detected a tablet user-agent (iPads, Android tablets). |
| (other) | Anything the tracker classified outside the standard three is passed through as the raw `device` string. |

NOTE: this box does **not** collapse tablet into desktop the way most other Analytics boxes do — it shows tablet as its own row.

## Business rules

### Hourly grouping counts unique visitors

Like [[analytics-online-store-sessions]], the metric behaves differently when the grouping is `hourly` vs everything else. On `hourly`, the same person visiting twice within one hour-bucket counts **once** (unique visitors per device). On all other groupings the number is a straight **session count**. This is the only behavioral difference a merchant will notice between the two modes.

### Top-N limit is fixed at 5

The dashboard module shows up to **5 rows**, sorted by session count descending — the device with the most sessions is the top row. The 5-row cap is platform-wide and **cannot be overridden** from the dashboard. Hidden rows beyond the top 5 are excluded from both the table AND the denominator used by the percent column — so the visible percentages sum to 100% across the displayed rows only.

### Admin-session exclusion

A merchant browsing their own store is excluded and does not appear here.

### Data freshness — 1-hour cadence

Same underlying traffic-source aggregations as [[analytics-online-store-sessions]], which run on a 1-hour cadence. A new visitor session shows up here within ~1-2 hours.

### Device classification is fixed (no per-store config)

Device classification comes from the storefront tracker's user-agent parser, not from any per-store setting. Every CloudCart store sees the same device buckets and the same sorting rule. The standard values are `mobile`, `desktop`, `tablet`; anything else the tracker reports passes through unchanged as its own row.

### Unrecognised devices silently merge into "desktop"

Any visit where the tracker did not set a device falls back to `desktop`. There is no separate "unknown" / "null" / "other" bucket — unclassified traffic merges into the `desktop` row. This affects the percent denominator: if 5% of traffic comes from a user-agent the tracker doesn't recognise, those 5% inflate the `desktop` row.

### Visits keep tablet; orders fold tablet into "mobile"

Visit tracking (this box) preserves `tablet` as its own row. Order-side device classification uses a **different** rule that folds tablet into `mobile`. So a session from an iPad appears as **`tablet`** here, but the order from that same iPad shows as **`mobile`** on the orders boxes. Merchants comparing this box to [[analytics-orders-by-country]]'s device split won't get a perfect tie.

This also differs from most other Analytics boxes, which report a binary mobile-vs-desktop ratio (folding tablet into desktop). This box preserves the raw device, so a tablet-heavy store sees `tablet` as its own row here while [[analytics-online-store-sessions]] would have counted those sessions as `desktop`.

## How it works (verified against backend)

The box reads the same pre-aggregated visit data as [[analytics-online-store-sessions]], grouped by device. On the `hourly` grouping it counts unique visitors per device; on every other grouping it sums an already-rolled-up session total per device. Rows are sorted by session count descending and capped at the top 5. Each row carries a device name and a session count; the percent column is derived from those counts.

## Related

- [[analytics]] — parent hub.
- [[analytics-online-store-sessions]] — the parent metric; same data source, no device breakdown.
- [[analytics-sessions-by-country]] — sessions broken down by visitor country instead.
- [[analytics-sessions-by-social-source]] — sessions broken down by UTM source/medium.
- [[analytics-sessions-by-traffic-source]] — sessions broken down by referrer.

## Open questions

_None._
