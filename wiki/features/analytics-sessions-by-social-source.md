---
type: feature
nav_path: "Analytics → Traffic by Source / Medium"
route_name: analytics
route_path: /admin/analytics
aliases: ["Traffic by Source / Medium", "Sessions by UTM source", "UTM source breakdown", "По UTM", "Трафик по източник / средство"]
tags: [analytics, ccanalytics, visitors, sessions, sessions-by-social-source, utm]
plan_gates: []
created: 2026-05-22
updated: 2026-05-27
source_count: 9
---
# Traffic by Source / Medium

## Purpose

A table that breaks down the period's store sessions by the **UTM source/medium combination** that brought them in — `google/cpc`, `facebook/social`, `newsletter/email`, etc. This is the standard marketing-attribution view: which paid and unpaid campaigns are actually delivering traffic. Drill in (View More) to see Source / Medium / Campaign — the third UTM level.

This is the **marketing attribution diagnostic**. It pairs with [[analytics-sessions-by-traffic-source]] (which uses the HTTP referrer header instead of UTM tags) — together they answer "where is the traffic coming from?" from two different angles.

## Where to find it

Analytics dashboard → **Traffic by Source / Medium** box (`navigationSort: 17`, middle of the dashboard). Box `key: "sessions-by-social-source"`, `type: "table"`.

It has two drill-downs:
- **Details** (`hasDetails: true`) → [[analytics-details]] — paginated list of all UTM source/medium values with CSV export.
- **View More** (`viewMore: true`, `hasViewMoreChart: true`) → [[analytics-full]] — for a single source/medium, breaks it down by campaign + shows a time-series chart of visits.

## What the merchant can do here

- Read the **top 5 UTM source/medium values** for the period, ranked highest-traffic first. Per row: source/medium label, current count, percent of total, and a session-count meta-row ("Session {value}" / "Sessions {value}").
- See the **device split** (mobile/desktop) in a per-row tooltip: `Visits: {total}`.
- **Drill into campaigns in-card.** Click a row that has campaigns under it — the card body swaps to the campaigns table for that source/medium without leaving the dashboard, and the box title morphs from "Traffic by Source / Medium" to **"Traffic by {details}"** (e.g. "Traffic by google / cpc"). A back arrow (top-left) returns to the top-level list. Rows with zero campaigns are not clickable.
- Open the per-row **View more** link → [[analytics-full]] for that source/medium (Source / Medium / Campaign + inline chart).
- Open the **View details** link (top-right, shown when there are items) → the full [[analytics-details]] screen.
- Rows that carry an external URL show a small external-link icon.

### Card states

| State | When it appears | Message |
|-------|-----------------|---------|
| **Box tooltip** (dotted) | Hover | "Total visits, grouped by the type of traffic source linked them to your online store." |
| **No data** | Empty range | "No data available for the selected range." |
| **Period cutoff** | Selected start date before `2023-01-01` | "There is no data for the selected period. Please select a period after 01.01.2023 to view data." |
| **Timeout** | API returns HTTP 504 | "We cannot generate statistics for the selected period, please reduce it." |

### Dashboard Settings panel (cog icon)

- **Order statuses** — does NOT change traffic numbers (visit-event-driven box).
- **Industry** — no effect (no industry compare on this box).
- **Show devices** — toggling OFF hides per-row device badges/tooltips.
- **Show boxes sort** — drag/visibility tree.
- **Reset to default / Save / Cancel** — dashboard-wide semantics.

## Settings & fields

### Box configuration

| Property | Value | Meaning |
|----------|-------|---------|
| `key` | `sessions-by-social-source` | Box identifier. |
| `type` | `table` | Renders as a ranked table. |
| `collectDataFrom` | `2023-01-01` | Earliest date with UTM-source data. |
| `viewMore` | `true` | View More drill-down available per row. |
| `hasDetails` | `true` | Full Details screen available from the box header. |
| `hasViewMoreChart` | `true` | The View More screen has its own time-series chart. |
| `navigationSort` | `17` | Display position. |

### Detail / View More screen columns

The dashboard table shows Source / Medium, current count, and percent share. The Details and View More screens add: `page_name` ("Name"), `sales` ("Sales" / "Продажби"), `amount` ("Amount", currency), `views` ("Visitors / Sessions" / "Посетители / Сесии"), and `conversion_rate` ("Conversion rate" / "Процент на реализация"). View More also adds a per-date column and traces `views` over time, with an optional previous-period comparison overlay.

### Tooltip text (exact UI quote)

EN: `"Total visits, grouped by the type of traffic source linked them to your online store."`
BG: `"Общ брой посещения, групирани по тип източник на трафик, довел ги до Вашия онлайн магазин."`

Per-row tooltip: `Visits: {total}` (with device breakdown).

## Business rules

### What `utm_filter` is, and what's excluded

The box groups sessions by `utm_filter` — a normalised "UTM source / UTM medium" combination (e.g. `google / cpc`, `facebook / social`). The deeper `utm_filter_full` adds the campaign ("source / medium / campaign"). Missing components render as a literal `--` placeholder: a session arriving with only `utm_source=newsletter` shows as `newsletter / --`.

Only sessions that carry at least one UTM tag are counted (`utm_filter != null`). Untagged traffic — organic and direct — is excluded here; it appears in [[analytics-sessions-by-traffic-source]] under "Direct" or by-referrer instead.

Two further exclusions apply to every traffic-source box: internal page-to-page navigation within a store (tracker source `self`) is dropped, so only entry-point views are counted; and store-staff testing sessions (admin UUIDs) are filtered out, so testing with UTM links does not pollute the box.

### Campaign drill gate

Each source/medium row carries a count of the distinct UTM campaigns recorded under it. When that count is greater than zero the row is clickable (opens the in-card campaigns drill or View More); when it is zero the row is not clickable. The campaigns sub-view returns the top campaigns for the selected source/medium.

### Sorting and limits

Rows are sorted by session count, highest first.

| Surface | Limit |
|---------|-------|
| Dashboard box | 5 rows |
| Details paginator | 100 per page |
| Details / export hard cap | 1000 (CSV export bypasses the cap) |

A dedicated covering index keeps the query fast even on stores with millions of sessions.

### Data freshness — 1-hour cadence

This box is fed by the same hourly traffic-source aggregation as Total Visits: per-session rows are rolled up into the grouped per-source data on a 1-hour cadence, so a new UTM-tagged session appears within ~1-2 hours.

### Mobile vs desktop categorisation

Same as elsewhere on the dashboard: `device == 'mobile'` counts as mobile; everything else is desktop (tablet folded in).

### No per-store override

The UTM-attribution logic is identical for every CloudCart store — there is no per-store override of how the source/medium is composed, the campaign-count rule, or the click-into-campaigns gate.

## Related

- [[analytics]] — parent hub.
- [[analytics-online-store-sessions]] — the parent metric (total, no UTM split).
- [[analytics-sessions-by-traffic-source]] — same data via the HTTP referrer instead of UTM tags.
- [[analytics-sessions-by-country]] — sessions split by visitor country.
- [[analytics-sessions-by-device]] — sessions split by device type.
- [[analytics-details]] — the per-box drill-down screen.
- [[analytics-full]] — the View More time-series screen.

## Open questions

_None._
