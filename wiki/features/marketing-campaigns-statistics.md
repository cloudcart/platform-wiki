---
type: feature
nav_path: "Marketing → Campaigns → Statistics"
route_name: campaigns-statistics
route_path: /admin/marketing-new/campaigns/statistics/:id
aliases: ["Campaign statistics", "Campaign analytics", "Performance dashboard (per campaign)", "Open rate / click rate / conversion rate", "Статистика на кампания", "Аналитика на кампания"]
tags: [marketing, campaigns, statistics, analytics]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-05-23
updated: 2026-06-10
source_count: 3
---
# Campaign statistics

## Purpose

The **Campaign statistics** page is the merchant's per-campaign performance dashboard — the answer to "how is this campaign doing?". It aggregates every send the campaign has made across every step + every channel into five headline KPIs (reached subscribers, open rate, click rate, conversion rate, revenue), then breaks the numbers down per channel and per step so the merchant can see WHICH part of the funnel is working and which isn't.

This is where the merchant decides whether to keep a campaign running, pause it, tweak a step's message, or copy it as a template for next quarter. The data updates hourly — so a campaign that started ten minutes ago will show partial numbers; the merchant should refresh after the next hourly aggregation runs (see [[campaigns-stats-aggregation]]).

## Where to find it

Sidebar → **Marketing** → **Campaigns** → on any tab → click the **Statistics** indicator on a row (the small Logs / chart icon in the row actions).

The route is per-campaign:

| Route name | Method | Route path |
|------------|--------|------------|
| `campaigns-statistics` (Vue page) | — | `/admin/marketing-new/campaigns/statistics/:id` |

The page is a full-screen content view (not a side-panel). The breadcrumb reads: **Campaigns → Statistics → {campaign title}**.

## What the merchant can do here

- **Read the 5 headline KPI cards** — reached subscribers, open rate, click rate, conversion rate, turnover. See [[campaigns-stats-kpi-cards]].
- **Read the per-channel breakdown** — one card per channel (Email / SMS / Viber / Web Push / Messenger), with empty channels greyed out. See [[campaigns-stats-channel-breakdown]].
- **Read the per-step table** — one row per campaign step with sent / opened / clicked / unsubscribed / spam / bounced / orders / revenue / conversion-rate columns. See [[campaigns-stats-step-table]].
- **Drill into revenue** — click the Turnover KPI card (or a step's Turnover cell) to open the attributed-orders revenue list, [[marketing-campaigns-statistics-full]].
- **Drill into a step's per-recipient delivery log** — click a step row to open the Statistics Logs Modal. See [[campaigns-stats-logs-modal]].

## Sub-pages (in this cluster)

This feature is split into 6 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[campaigns-stats-kpi-cards]] — the 5 headline KPI cards (reached subscribers, open rate, click rate, conversion rate, turnover), the rate formulae, and the 10000× storage multiplier.
- [[campaigns-stats-channel-breakdown]] — the per-channel summary cards, the per-channel counter fields, and the greyed-out state for channels with no sends.
- [[campaigns-stats-step-table]] — the per-step (action) table: every column, the zero-send guard, and which action types are excluded as non-delivery steps.
- [[campaigns-stats-attribution]] — the conversion-attribution model: `cc_campaign_id` / `cc_campaign_action_id` `orders_meta` keys, session-based last-touch, and the `revenue_statuses` filter.
- [[campaigns-stats-aggregation]] — the hourly aggregation job, auto-archive of completed Regular campaigns, the 7-day post-archive window, and statistics-store / performance notes.
- [[campaigns-stats-logs-modal]] — the Statistics Logs Modal opened from a step row, and its two nested sub-modals (preview-message + subscriber-details).

## Settings & fields

This page has no merchant-editable settings — it is read-only reporting. The numbers it shows are produced by the hourly aggregation ([[campaigns-stats-aggregation]]) and read from the campaign's own stored counters. The merchant's only inputs are the drill-down clicks (Turnover card, step row) and the filter bar inside the Logs modal ([[campaigns-stats-logs-modal]]). The KPI definitions and their formulae are documented on [[campaigns-stats-kpi-cards]]; the per-channel and per-step counter fields on [[campaigns-stats-channel-breakdown]] and [[campaigns-stats-step-table]].

An info-tip line below the per-channel cards reads *"The statistical information is updated every hour"* — the merchant's reminder that the numbers are not real-time.

## Business rules

The high-level rules — detailed in the sub-pages:

- **Numbers lag by up to 60 minutes.** Aggregated open / click / conversion / revenue figures refresh hourly; only the raw sent count is near-real-time (visible immediately in [[marketing-campaigns-statistics-log]]). See [[campaigns-stats-aggregation]].
- **Conversion is last-touch, session-scoped.** An order is credited to the campaign whose tracked link was clicked most recently before purchase, via an `orders_meta` row — and only if the order is in a revenue status. See [[campaigns-stats-attribution]].
- **Completed Regular campaigns auto-archive.** When a Regular (one-shot) campaign finishes dispatching to all enrolled subscribers, the next hourly aggregation marks it completed and silently moves it to the Archived tab. Automated campaigns never auto-archive. See [[campaigns-stats-aggregation]].
- **Soft-deleted campaigns return 404.** The route respects the soft-delete scope; a stale link to a deleted campaign gets a 404. The revenue list ([[marketing-campaigns-statistics-full]]) survives the delete because it reads from `orders_meta` directly.
- **Only delivery channels appear in the per-step table.** Non-delivery action types (set_tags, remove_from_campaign, set_customer_group) are excluded — they have no send statistics. See [[campaigns-stats-step-table]].
- **Permission + anti-spam gate.** Standard campaign permission applies, and the route is behind the campaign anti-spam policy gate (the same gate that protects every campaigns endpoint).

## How it works

The page fetches its data in four parallel JSON-API queries (no AJAX-on-paint pattern): `statisticsOverview` (the 5 headline cards — see [[campaigns-stats-kpi-cards]]), `statisticsChannels` (per-channel totals — see [[campaigns-stats-channel-breakdown]]), `statisticsActions` (per-step rows — see [[campaigns-stats-step-table]]), and `statisticsLogs` (the paginated per-recipient log, fetched on-demand when a step's Logs modal opens — see [[campaigns-stats-logs-modal]]).

Each query is independently loading-state aware — while overview / channels / actions are still loading, the page shows skeleton placeholders, and each row populates as its query resolves. So the page paints progressively rather than waiting for everything.

All the displayed numbers (except the per-step grid) come from counters stored on the campaign record itself, refreshed hourly by the aggregation job documented in [[campaigns-stats-aggregation]] — which is why the dashboard renders fast even on very large campaigns.

## Related

- [[marketing-campaigns]] — parent hub; the statistics chip on each row opens this page.
- [[marketing-campaigns-edit]] — campaign editor; performance numbers seen here inform message tweaks made there.
- [[marketing-campaigns-statistics-full]] — revenue side-panel; opens via the Turnover KPI card click.
- [[marketing-campaigns-statistics-log]] — per-send log hub; opens via clicking a step row.
- [[marketing-campaigns-subscribers]] — per-subscriber funnel state.
- [[marketing-dashboard]] — Marketing Suite hub; aggregates campaign performance across all campaigns.
- [[marketing-channels]] — channel reputation; bounces and spam shown here roll up to channel reputation.
- [[campaign]] — Campaign entity (carries the aggregated counters).

## Open questions

No outstanding questions.
