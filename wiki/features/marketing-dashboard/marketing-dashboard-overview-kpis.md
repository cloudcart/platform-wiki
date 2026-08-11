---
type: feature
nav_path: "Marketing → Dashboard → Overview KPIs"
route_name: marketing-dashboard
route_path: /admin/marketing-new/dashboard
aliases: ["Marketing Overview KPIs", "Marketing-results KPIs", "Open rate dashboard", "Conversion rate dashboard", "Date range picker marketing", "Compare period", "Compare year", "KPI tiles", "Маркетинг KPI"]
tags: [marketing, dashboard, kpi, overview, results, date-range]
plan_gates: ["allow_period_compare"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-dashboard]]. See the hub for the other aspects (welcome & steps, channel performance, quick-launch tiles, campaigns & products, RFM & discounts, data freshness).

# Dashboard — Overview KPIs

## Purpose

The **Overview row** + **Marketing-results row** are the two-tier KPI grid the merchant scans first thing every morning. The top row carries the **general** numbers (Orders, AOV, Customers, Accepting marketing, Customer value) — what's going on in the store overall. The bottom row carries the **marketing-specific** results (Open rate, Click rate, Conversion rate, Marketing sales, Revenue) — what the merchant's campaigns are actually doing. Both rows share a single date-range picker and a "compare" selector that drives the up/down deltas next to every marketing-results tile.

## Where to find it

Sidebar → **Marketing** → **Marketing suite** — directly below the Welcome / Steps row.

## What the merchant can do here

- **Pick the analysis period** — a 2-handle date-range picker at the top of the Overview row. Future dates are visually disabled.
- **Pick a comparison mode** — a "compare" selector switches the deltas to **(none) / Previous period / Same period last year**.
- **Reset the picker to the default 1-month range** — a Clear button on the picker.
- **Read the general KPIs** — Orders, Average order value, Customers, Accepting marketing, Customer value.
- **Read the marketing-results KPIs** — Open rate, Click rate, Conversion rate, Marketing sales, Revenue. Each carries a comparison delta + "was X" footnote against the comparison period.

## Settings & fields

### Date-range picker

| Field | Default | Validation |
|-------|---------|------------|
| Range start | today minus 1 month | Must not be a future date |
| Range end | today | Must not be a future date |
| Localisation | from `serverSettings('language_cp')` | — |
| Format | `YYYY-MM-DD` | — |

The picker is a 2-handle date-picker (`type="date"`, `range`). The placeholder shows the currently-selected interval inline. The Clear button resets to the default 1-month-back range.

### Compare selector

| Value | Effect |
|-------|--------|
| (default) | No comparison — only current period |
| `period` | Previous equal-length period (e.g., previous 7 days for a 7-day range) |
| `year` | Same period last year (e.g., this week last year for a 7-day range) |

### Overview KPI tiles (top row)

| Key | Label | Source / formula |
|-----|-------|-------|
| `orders` | Orders | Count of orders in the selected range matching the store's analytics-counted statuses |
| `average_order_value` | Average order value | Total revenue / orders count (money-format) |
| `customers` | Customers | Count of unique customer accounts that placed orders in range |
| `subscribers_accepting_marketing` | Accepting marketing | Subscribers whose marketing opt-in flag is set |
| `customer_value` | Customer value | Total revenue / unique customer count |

### Marketing-results KPI tiles (bottom row)

| Key | Label | Definition |
|-----|-------|-----------|
| `open_rate` | Open rate | Opened messages / total successfully-sent messages |
| `click_rate` | Click rate | Clicked links / opened messages |
| `conversion_rate` | Conversion rate | Orders attributed to campaigns / total successfully-sent messages |
| `marketing_sales` | Marketing sales | Revenue from orders attributed to campaigns (in store currency) |
| `revenue` | Revenue | Total store revenue in the period (for context) |

Comparison deltas are direction-coded (`up`, `down`, `no_change`) and rendered with green / red / grey badges. Each marketing-results tile shows an up/down arrow + percentage change vs the comparison period plus a "was X" footnote.

## Business rules

### Date ranges snap to start-of-day in site timezone

Date ranges are converted from the merchant's site timezone to UTC and snapped to start-of-day / end-of-day before being used as cache key + query bounds. Cached results are stable for the whole day — a refresh at 10:00 and 17:00 returns the same cached payload until the TTL elapses.

### "All time" → "last year" cap, future dates blocked

"All time" is interpreted backend-side as `now - 1 year` to `now` (defensive cap against full-table scans on long-running stores). For truly all-time analytics, use [[analytics-total-sales]]. Future dates are visually disabled in the picker — the merchant cannot pick "next week" by accident.

### General overview is cached 5 minutes; results are cached 1 hour

- **General overview tiles** (Orders, AOV, Customers, Accepting marketing, Customer value) — cached **5 minutes** per (site, range, comparison-range) tuple.
- **Marketing-results tiles** (Open rate, Click rate, Conversion rate, Marketing sales, Revenue) — cached **1 hour** per tuple.

A freshly placed order will appear in Orders / AOV / Revenue within 5 minutes; the same order's attribution into Marketing sales / Conversion rate can take up to one hour. The full freshness table sits on [[marketing-dashboard-data-freshness]].

### Compare-period requires a plan feature

The compare selector's `period` and `year` modes require the `cc_analytics.allow_period_compare` plan feature. Plans without it see no compare selector (no deltas, just current-period numbers).

### Marketing sales vs Revenue distinction

Both money tiles answer different questions: **Revenue** = total store revenue in the period (all orders); **Marketing sales** = revenue from orders attributed to marketing campaigns via UTM / campaign tracking / abandoned-cart recovery / subscriber-to-campaign joins. Marketing sales is the campaign-ROI number; Revenue is context. A common confusion: Marketing sales well below Revenue is expected — the bulk of orders come from non-marketing acquisition (direct, SEO, repeat customers without UTM tags).

## How it works

The two rows query the marketing API. General overview hits `GET /admin/api/core/marketing/general-overview`; marketing results hit `GET /results` plus five per-rate endpoints (`/results/open-rate`, `/results/click-rate`, `/results/conversion-rate`, `/results/marketing-sales`, `/results/revenue`) — split so each tile can refresh independently. Caching uses composite keys: `marketing.general-overview.{site_id}.{range-hash}.{all|range}.{compare-range-hash|none}`. The dashboard syncs the chosen range across all modules in this row via the `useDashboardCompareQuery` composable.

## Recommended merchant use

- **Morning health check** — pick "Yesterday" + compare `period` to see how yesterday compared to the day before.
- **Weekly review** — pick "Last 7 days" + compare `period` for week-over-week.
- **Campaign post-mortem** — pick the exact campaign window and read Marketing sales / Conversion rate / Open rate together to gauge ROI.
- **Anomaly hunt** — when a delta tile turns red, the merchant drills into the underlying surface (e.g., [[marketing-dashboard-channel-performance]] for a channel-specific drop).

## Related

- [[marketing-dashboard]] — hub.
- [[marketing-dashboard-channel-performance]] — per-channel breakdown of the same Open / Click / Conversion / Revenue numbers.
- [[marketing-dashboard-data-freshness]] — cache TTLs + collector job summary.
- [[analytics-total-sales]] — the canonical revenue surface (uncapped, no 1-year defensive limit).
- [[campaign]] — Campaign entity that marketing-attributed orders join to.
- [[plan-gates]] — `cc_analytics.allow_period_compare` feature gate.

## Open questions

No outstanding questions.
