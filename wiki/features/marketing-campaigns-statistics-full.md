---
type: feature
nav_path: "Marketing → Campaigns → Statistics → Full / Revenue"
route_name: campaigns.statistics.full
route_path: /admin/campaigns/statistics
aliases: ["All-campaigns statistics", "Full statistics", "Revenue attribution", "Orders from campaigns", "Campaign revenue list", "Обща статистика", "Приходи от кампании", "Поръчки от кампания"]
tags: [marketing, campaigns, statistics, revenue, attribution]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-05-23
updated: 2026-06-10
source_count: 2
---
# Full statistics & revenue attribution

## Purpose

The **Full statistics** dashboard and the **Revenue** drill-downs are the merchant's "show me the money" views — they connect marketing activity to actual orders. Two questions:

- "Across ALL my campaigns combined, what's my open rate / click rate / conversion / revenue?" → **Full statistics** (`campaigns.statistics.full`). See [[campaigns-stats-full-dashboard]].
- "WHICH orders specifically came from a campaign, and which campaign / step?" → **Full revenue** (`campaigns.statistics.full.revenue`) or **per-campaign revenue** (`campaigns.statistics.revenue`). See [[campaigns-stats-full-revenue-panel]].

The full-statistics screen aggregates every campaign in the store into one combined dashboard with the same 5 KPI cards as [[marketing-campaigns-statistics|per-campaign statistics]], plus the same per-channel breakdown — but rolling up all campaigns instead of one. The revenue drill-downs are tables of the orders the platform attributes to campaign clicks, one row per order showing the last-touch campaign / step / channel.

This page is the **hub** for the cluster. It carries the common framing; each aspect below documents one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

## Sub-pages (in this cluster)

- [[campaigns-stats-full-dashboard]] — the all-campaigns combined KPI dashboard: 5 KPI cards, per-channel cards row, the aggregate formulae, and the hourly-lag-vs-live-revenue split.
- [[campaigns-stats-full-revenue-panel]] — the full + per-campaign revenue side-panels: table columns, the Campaign-column drop on the per-campaign variant, N/A fallbacks, step-number display, empty state vs zero data.
- [[campaigns-stats-full-attribution-metadata]] — the `orders_meta` rows stamped on each attributed order; what each parameter is used for; the subscriber-name snapshot; soft-deleted-campaign survival.
- [[campaigns-stats-full-attribution-mechanic]] — session-based last-touch attribution: the `cc_campaign` query param, the tracking middleware, the URL-cleanup redirect, the session-lifetime attribution window, and re-click overwrite.
- [[campaigns-stats-full-revenue-statuses]] — what counts as "revenue": the Segments app `revenue_statuses` setting, the main-status vs fulfillment-status split, the auto-computed negative-status exclusion.
- [[campaigns-stats-full-order-processing]] — the per-order attribution write: queued processing, the 6-source subscriber resolution, double-attribution guard, and the `MADE_ORDER` / `PURCHASE` side-effects on the per-step stats and per-send log.

## Where to find it

| Route name | Route path | Source | Purpose |
|------------|------------|--------|---------|
| `campaigns.statistics.full` | `/admin/campaigns/statistics` | Click Statistics from sidebar or campaigns landing | Combined dashboard for ALL campaigns. |
| `campaigns.statistics.full.revenue` | `/admin/campaigns/statistics/full/revenue` | Click Turnover card on full statistics page | All orders from any campaign. |
| `campaigns.statistics.revenue` | `/admin/campaigns/statistics/{id}/revenue` | Click Turnover card on per-campaign statistics page | Orders attributed to a specific campaign. |

These are **legacy Smarty** routes (no modern Vue equivalent for the all-campaigns full dashboard). The full dashboard is a full-screen content view; the two revenue routes open as side-panels (panel-class="wide"). All three routes are behind the campaign anti-spam policy gate; standard campaign permission applies.

## What the merchant can do here

Nothing is configurable on these views — they are read-only reporting. The merchant reads the combined KPIs on the dashboard, clicks the Turnover card to open the revenue list, and clicks an order number to open that order's detail. See [[campaigns-stats-full-dashboard]] and [[campaigns-stats-full-revenue-panel]] for the interactions.

## Settings & fields

The one setting that changes what these views report lives outside the cluster: the **Segments** app's `revenue_statuses` setting decides which order statuses qualify as "revenue". See [[campaigns-stats-full-revenue-statuses]]. The attribution metadata stamped per order is catalogued in [[campaigns-stats-full-attribution-metadata]].

## Business rules

- **Attribution is per-order, last-touch.** The whole order `price_total` is credited to one campaign — the last one the customer clicked. No first-touch, multi-touch, or split-credit. See [[campaigns-stats-full-attribution-mechanic]].
- **Revenue numbers are live; rate numbers are hourly-lagged.** Turnover is a real-time sum of order totals; open / click / conversion rates come from the hourly statistics store. See [[campaigns-stats-full-dashboard]].
- **What counts as revenue is merchant-configurable** via the Segments app, not hard-coded. See [[campaigns-stats-full-revenue-statuses]].
- **Cross-campaign comparison lives elsewhere.** The full dashboard shows no per-campaign comparison chart; for "Campaign A vs Campaign B" the merchant uses [[marketing-dashboard|Marketing Suite]] (Top Campaigns + Recent Campaigns tables).

## Related

- [[marketing-campaigns]] — parent hub; links to the full statistics dashboard.
- [[marketing-campaigns-statistics]] — per-campaign statistics; the Turnover KPI card there opens the per-campaign revenue panel.
- [[marketing-campaigns-statistics-log]] — per-send log; complementary view (per-send not per-order).
- [[marketing-dashboard]] — Marketing Suite hub; shows campaign rollups at the marketing level.
- [[order]] — Order entity (revenue rows are orders).
- [[settings-statuses]] — order-status configuration; what counts as "real revenue".
- [[campaign]] — Campaign entity.
- [[marketing-channels]] — channels referenced by the channel column.

## Open questions

No outstanding questions.
