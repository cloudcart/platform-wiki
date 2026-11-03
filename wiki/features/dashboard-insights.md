---
type: feature
nav_path: "Dashboard → Insights"
route_name: insights
route_path: /admin/insights
aliases: ["Insights", "Executive Insights", "Predictive Alerts", "Store health score", "Insights dashboard", "dead stock alert", "stuck orders alert", "executive insights page"]
tags: [dashboard, insights, analytics, recommendations, plan-gated]
plan_gates: ["smart_daily_actions"]
created: 2026-06-23
updated: 2026-06-23
source_count: 1
---
# Insights (Executive Insights)

## Purpose

The **Insights** page is an at-a-glance **executive summary of the store's health** — a single score, a set of **predictive alerts**, and a handful of metric panels (top products, stuck orders, dead stock, reviews, refunds/returns, revenue trend) computed from the store's own recent data. It is the analytical companion to the [[dashboard-smart-actions|Smart daily actions]] widget: Smart Actions says *"do this next"*, Insights shows *"here's how the store is doing and what's about to need attention"*. Both are gated by the same `smart_daily_actions` plan-feature.

## Where to find it

Sidebar → **Insights** (`/admin/insights`, route `insights`). Data comes from `GET admin.api.dashboard.insights`; an unsubscribed-teaser variant comes from `admin.api.dashboard.insights.teaser`.

## What the merchant can do here

- Read the store's **health score** and its month-over-month trend.
- Scan **predictive alerts** — early warnings about things that are about to need attention.
- Review the metric panels (top products, stuck orders, dead stock, reviews, refunds/returns) and jump to the relevant admin screen.

It is a read-only overview — there are no settings to configure here.

## Settings & fields

No merchant-configurable settings. The page is driven by the `smart_daily_actions` plan-feature (which decides full data vs the blurred teaser) and computed automatically from store data. The metric panels (verified in the backend):

| Panel | What it shows |
|---|---|
| **Health score** | An overall store-health score derived from the month-over-month trends. |
| **Trends** | Revenue this month vs last month (and related period-over-period movement). |
| **Predictive alerts** | Early warnings computed from the trends (e.g. metrics moving the wrong way). |
| **Top products** | Best-performing products for the current period. |
| **Stuck orders** | Orders sitting too long in a non-final state (need action). |
| **Dead stock** | Products with stock but no recent sales. |
| **Reviews pulse** | Recent review activity / rating signal. |
| **Refunds & returns** | Refund / return volume for the period. |

## Business rules

- **Gated by `smart_daily_actions`.** Subscribed stores get the full computed panels; unsubscribed stores get a **blurred teaser** — the `index` endpoint returns `enabled: false`, and the separate `teaser` endpoint returns just a `score` + an `alerts_count` to show the feature's value (a nudge to subscribe).
- **Cached per store.** The computed result is cached (`smart_daily_actions.index.<site_id>`) so the page loads fast and doesn't recompute the aggregates on every open.
- **Read-only + data-driven.** The merchant cannot author panels or change thresholds; the score, alerts and panels are platform-defined and computed from store data (orders, products, reviews, refunds over rolling windows).
- **Distinct from Smart daily actions.** Same plan-feature, different surface: [[dashboard-smart-actions]] is the actionable "do this next" widget on the home dashboard; Insights is the standalone analytical overview at `/admin/insights`.

## Related

- [[dashboard-smart-actions]] — the actionable recommendation widget (same `smart_daily_actions` plan-feature).
- [[dashboard]] — the admin home screen.
- [[analytics]] — the full reports/charts area (deeper, configurable analytics).
- [[plan-gates]] / [[plan-features]] — the `smart_daily_actions` plan-feature.

## Open questions

- The exact formula behind the health score and which signals weight the predictive alerts are platform-internal; documented here at the panel level (what each surfaces), not the scoring math.
