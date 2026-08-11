---
type: feature
nav_path: "Marketing → Dashboard → Data freshness & permissions"
route_name: marketing-dashboard
route_path: /admin/marketing-new/dashboard
aliases: ["Marketing dashboard freshness", "Marketing dashboard cache TTL", "6-hour collector job marketing", "Dashboard snapshot table", "Marketing dashboard moderator permissions", "Marketing API permissions", "Stale dashboard data", "Plan gating marketing dashboard"]
tags: [marketing, dashboard, caching, scheduled-job, freshness, permissions]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-dashboard]]. See the hub for the other aspects (welcome & steps, overview KPIs, channel performance, quick-launch tiles, campaigns & products, RFM & discounts).

# Dashboard — Data freshness & permissions

## Purpose

This aspect documents **how stale each module on the Marketing Suite can be** — the answer to *"I just placed a campaign / made a sale, why doesn't the dashboard show it?"*. Some modules read live with short caches; others read from a snapshot refreshed every 6 hours. This page is the cross-cutting reference for "missing" or "wrong" dashboard data and enumerates the full set of API endpoints behind the dashboard plus the moderator-permission gates that decide which rows render.

## Where to find it

Sidebar → **Marketing** → **Marketing suite** — this aspect documents cross-row behaviour rather than a specific row.

## What the merchant can do here

Nothing directly — this page documents the **timing** and **gating** of the modules elsewhere on the dashboard. The merchant cannot change cache TTLs or trigger the collector job from the UI.

## Settings & fields

### Module freshness table

| Row / module | Source mode | Effective freshness |
|--------------|-------------|---------------------|
| Welcome & steps | Live `steps-statuses` | Real-time |
| Overview KPIs (general) | Live + cached | **5 min** per (site, range, compare) tuple |
| Marketing-results KPIs | Live + cached | **1 h** per tuple |
| Channel performance | Live + cached | **10 min** per tuple |
| Campaigns (Top / Recent) | Snapshot table | **Up to 6 h** stale |
| Products (Favorite / Expected) | Snapshot table | **Up to 6 h** stale |
| BumpCart performance | Snapshot table | **Up to 6 h** stale |
| Cart rules performance | Snapshot table | **Up to 6 h** stale |
| RFM Analysis | Snapshot table | **Up to 6 h** stale |
| Product Reviews | Snapshot table | **Up to 6 h** stale |

### Full API endpoint enumeration

All endpoints sit under `/admin/api/core/marketing/`:

- Setup checklist — `GET /steps-statuses`, `POST /steps-statuses-update` ([[marketing-dashboard-welcome-steps]]).
- Overview KPIs — `GET /general-overview`, `/results`, `/results/{open-rate,click-rate,conversion-rate,marketing-sales,revenue}` ([[marketing-dashboard-overview-kpis]]).
- Channel performance — `GET /channel-performance`, `/channel-performance/{email,viber,sms_nth_message,web_push}` ([[marketing-dashboard-channel-performance]]).
- Campaigns + Products — `GET /campaigns-revenue`, `/campaigns-recent`, `/products-favorites`, `/products-expected` ([[marketing-dashboard-campaigns-products]]).
- RFM + Discounts + Reviews — `GET /bump-cart`, `/cart-rules`, `/rfm-analysis`, `/subscribers/settings`, `/reviews` ([[marketing-dashboard-rfm-discounts]]).

### Plan gates that affect dashboard rendering

| Plan feature | Affects |
|--------------|---------|
| `cc_analytics.rfm` | RFM heatmap (blurred + upsold when missing) |
| `cc_analytics.allow_period_compare` | Compare-period and compare-year deltas on Marketing-results tiles |

### Moderator API permission gates

| Permission key | Required to see |
|----------------|-----------------|
| `marketing` (broad) | Everything |
| `marketing.subscribers` (child) | RFM module |
| `marketing.discounts` (child) | Cart rules row |
| (other child permissions) | The relevant module |

Administrators always pass. Moderators are granted permissions from [[settings-staff]] → Access permissions.

## Business rules

### Live vs scheduled split

Two data-flow models coexist:

- **Live + cached** — Overview, Marketing-results, Channel performance. Source data queried on each page load (subject to the TTLs above). A freshly placed order appears in Orders / AOV within 5 min, in Conversion rate / Marketing sales within 1 h, in Channel performance within 10 min.
- **Scheduled snapshot** — Campaigns, Products, BumpCart, Cart rules, RFM, Reviews. Read from the `dashboard` snapshot table, refreshed only by the MarketingDashboard scheduled job every 6 hours. A campaign that just generated revenue, a product just favourited, a review just submitted — none appear until the next collector cycle.

### Collector job schedule

The MarketingDashboard job runs on a **6-hour interval**. It dispatches separate Collector workers per module (RFM, BumpCart, Reviews, Favorites, Expected, Cart Rules, Latest campaigns, Revenue campaigns, Segments, UTM, etc.). The controller then reads the latest stored payload per module from the `dashboard` table (keyed by metric name + site ID). Workers run independently — a failed RFM collector does NOT block the BumpCart payload on the same cycle.

### Collector skips disabled / lapsed / maintenance sites

The MarketingDashboard job loops through all sites but **skips** sites in the platform-level disabled list, sites where `plan_expired = true`, and sites in maintenance mode. Merchants on lapsed plans or in maintenance mode see stale data even on the slow modules — the collector never re-runs for their site until the underlying state clears. After plan renewal, the next collector cycle (up to 6 h) populates the snapshot.

### Cache keys are site + range + compare-range scoped

Cache keys use the form `marketing.general-overview.{site_id}.{range-hash}.{all|range}.{compare-range-hash|none}` (and analogous keys for the other live endpoints). Two merchants picking the same range get independent caches. The same merchant cycling "Yesterday → Last 7 days → Yesterday" hits the cache on the second yesterday lookup if within the TTL.

Date ranges snap to start-of-day in the site timezone before keying, so a "yesterday" range yields the same cache key whether the merchant looks at 10:00 or 17:00. The cache invalidates only when the TTL elapses.

### "All time" → "last year" cap

"All time" in any range picker is interpreted backend-side as `now - 1 year` to `now`. This is the defensive cap to prevent accidental full-table scans on long-running stores. For truly all-time analytics, the merchant uses [[analytics-total-sales]].

### Manually purging the cache is not exposed

There is **no merchant-facing "refresh now" button**. The correct support answer to *"my dashboard is wrong, refresh it"* is to explain the TTL / collector schedule and identify which module the merchant is looking at. Support engineering can purge the cache server-side, but this is not a self-service action.

## How it works

The dashboard is a thin composition layer over the marketing API. On mount it issues parallel queries for every row — live endpoints query their stores (orders, campaigns, subscribers, channels, customers) with the cache layer applied; snapshot endpoints read the latest row from the `dashboard` table for the requesting site.

The MarketingDashboard scheduled job is dispatched by the platform's recurring-jobs runner — see the `marketing_dashboard` entry on [[settings-queue-view-recurring-jobs]]. When it runs, it loops eligible sites, fans out 16 Collector workers per site, and writes each worker's output to the `dashboard` table under a per-module key.

## Recommended merchant use

- **Top rows refresh within minutes** — Overview, Channel performance.
- **Bottom rows refresh on a 6-hour schedule** — Campaigns table, Products tables, RFM, BumpCart, Cart rules, Reviews.
- **A "stale" dashboard right after an action is usually expected** — wait one collector cycle before assuming something is broken.

## Related

- [[marketing-dashboard]] — hub.
- [[marketing-dashboard-overview-kpis]] — the 5-min / 1-h live tiles.
- [[marketing-dashboard-channel-performance]] — the 10-min live tiles.
- [[marketing-dashboard-campaigns-products]] — snapshot-backed Campaigns and Products rows.
- [[marketing-dashboard-rfm-discounts]] — snapshot-backed RFM / BumpCart / Cart Rules / Reviews.
- [[settings-queue-view-recurring-jobs]] — where the `marketing_dashboard` schedule entry is visible to merchants on the right plan.
- [[settings-staff]] — where moderator marketing permissions are granted.
- [[analytics-total-sales]] — the uncapped revenue surface (no 1-year "All time" defensive cap).
- [[plan-gates]] — `cc_analytics.rfm`, `cc_analytics.allow_period_compare`.

## Open questions

No outstanding questions.
