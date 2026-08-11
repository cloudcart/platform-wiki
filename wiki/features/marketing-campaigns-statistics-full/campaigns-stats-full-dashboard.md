---
type: feature
nav_path: "Marketing → Campaigns → Statistics → Full (dashboard)"
route_name: campaigns.statistics.full
route_path: /admin/campaigns/statistics
aliases: ["Full statistics dashboard", "All-campaigns dashboard", "Combined campaign KPIs", "Обща статистика на кампании"]
tags: [marketing, campaigns, statistics, kpi, dashboard]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-05-23
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-campaigns-statistics-full]]. See the hub for the other aspects (revenue panel, attribution metadata, attribution mechanic, revenue statuses, order processing).

# Full statistics — the combined dashboard

## Purpose

The **Full statistics** dashboard (`campaigns.statistics.full`) rolls up every campaign in the store into one combined KPI view. It answers "across ALL my campaigns combined, what's my open rate / click rate / conversion / revenue?" — the same shape as [[marketing-campaigns-statistics|per-campaign statistics]], but aggregated instead of scoped to a single campaign.

## Where to find it

Route `campaigns.statistics.full` at `/admin/campaigns/statistics`, reached by clicking **Statistics** from the sidebar or the campaigns landing page. This is a **legacy Smarty** full-screen content view (no modern Vue equivalent for the all-campaigns dashboard). It is behind the campaign anti-spam policy gate; standard campaign permission applies.

## What the merchant can do here

- Read the 5 KPI cards: **Reached subscribers**, **Open rate**, **Click rate**, **Conversion rate**, **Turnover**.
- Read the per-channel cards row (Email / SMS / Viber / Web Push, each showing total sent + successfully sent for that channel).
- Click the **Turnover** KPI card to open the full revenue side-panel — see [[campaigns-stats-full-revenue-panel]].

The Turnover card subtitle differs from the per-campaign page: *"Revenue from orders made through all campaigns"* (vs the per-campaign *"Revenue from orders made through this campaign"*).

## Settings & fields

The dashboard is read-only — nothing is configured here. The one external setting that changes what the Turnover figure includes is the Segments app `revenue_statuses` setting; see [[campaigns-stats-full-revenue-statuses]].

### KPI formulae (aggregated across all campaigns)

Identical formulae to per-campaign statistics, but summed across every (campaign, channel) row in the statistics store:

- **Open rate** — `(seen_message / successfully_sent) * 10000`.
- **Click rate** — `(opened_url / successfully_sent) * 10000`.
- **Conversion rate** — `(orders_count / successfully_sent) * 10000`.
- **Revenue** — sum of `price_total` for orders attributed to any campaign.

The order query joins to `orders_meta` filtered only by `parameter=cc_campaign_id` (no value filter) — so every order attributed to ANY campaign counts. The dashboard renders the KPI cards only when `total_sent > 0`; otherwise the rate cards show their zero state.

## Business rules

### Revenue is live; rates are hourly-lagged

This is the single most important nuance to communicate to merchants. The dashboard mixes two data sources with different freshness:

- **Turnover (revenue)** — a **live** lookup of orders plus their attribution metadata. These numbers are real-time.
- **Open / click / conversion rates** — read from the **hourly statistics store** updated by the hourly aggregation job. These lag by up to an hour.

So a campaign that just sent 1000 emails and got 10 orders will show **10 orders in revenue immediately**, while the open rate may still read **0%** until the hourly aggregation runs. The Turnover KPI card itself combines both: a live `revenue` SUM with an hourly-lagged `conversion_rate` (which depends on the `successfully_sent` counter).

### No per-campaign comparison breakdown

The full dashboard does NOT show a per-campaign comparison (e.g. a chart of "Campaign A vs Campaign B revenue"). For that, the merchant uses [[marketing-dashboard|Marketing Suite]], which has the Top Campaigns + Recent Campaigns tables.

### Clicks back-fill delivery counters

The platform increments `successfully_sent` AND `opened_url` on click events too — not just on opens. A click implicitly means the message was delivered AND read, so both counters move together. This is why a campaign's aggregated "successfully sent" count can exceed the raw delivery-event count: clicks back-fill missing delivery confirmations. See [[campaigns-stats-full-order-processing]] for the matching per-step stat increments.

## Related

- [[marketing-campaigns-statistics-full]] — hub.
- [[marketing-campaigns-statistics]] — per-campaign statistics (same card shape, single-campaign scope).
- [[marketing-dashboard]] — Marketing Suite; the place for cross-campaign comparison.
- [[marketing-channels]] — channels referenced by the per-channel cards row.
- [[order]] — Order entity; revenue rows are orders.

## Open questions

No outstanding questions.
