---
type: feature
nav_path: "Marketing → Campaigns → Statistics → KPI cards"
route_name: campaigns-statistics
route_path: /admin/marketing-new/campaigns/statistics/:id
aliases: ["Campaign KPI cards", "Reached subscribers", "Open rate", "Click rate", "Conversion rate", "Turnover card", "Headline campaign metrics"]
tags: [marketing, campaigns, statistics, kpi]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-campaigns-statistics]]. See the hub for the other aspects (channel breakdown, step table, attribution, aggregation, logs modal).

# Campaign statistics — headline KPI cards

## Purpose

The top row of the Campaign statistics page is **five headline KPI cards** — the at-a-glance scorecard for the whole campaign. They answer "how many people did we reach, how many opened, how many clicked, how many bought, and how much did we make?" in one glance. This page documents what each card measures, how each rate is computed, and the (deliberate) 10000× multiplier the platform uses to store percentages.

## Where to find it

The five cards are the first thing the merchant sees on the Campaign statistics page (Sidebar → **Marketing** → **Campaigns** → Statistics icon on a row). They sit above the per-channel breakdown ([[campaigns-stats-channel-breakdown]]) and the per-step table ([[campaigns-stats-step-table]]).

## What the merchant can do here

- **Read the five headline numbers** for the whole campaign.
- **Click the Turnover card** → opens [[marketing-campaigns-statistics-full]], the list of actual orders attributed to this campaign. This is the only clickable card; hovering it reveals a "View more" hint.
- The other four cards (Reached / Open / Click / Conversion) are static — informational only.

## Settings & fields

The five cards, in order:

| KPI | What it measures | Subtitle shown |
|-----|-------------------|----------------|
| **Reached subscribers** | Total unique subscribers who successfully received at least one message from this campaign. Source: the campaign's `successfully_sent` counter. | "Total unique subscribers" |
| **Open rate** | % of successfully-sent messages that were opened. | "Messages open rate in %" |
| **Click rate** | % of successfully-sent messages where a tracked link was clicked. | "Clicked links from the messages in %" |
| **Conversion rate** | % of successfully-sent messages that resulted in an order. | "Total number of orders divided by all sent messages" |
| **Turnover** | Revenue from orders attributed to this campaign — Money-formatted. Clickable → revenue list. | "Revenue from orders made through this campaign" |

Each card shows an icon, a big number, a label, and the one-line subtitle.

### Rate formulae

- **Open rate** = `(seen_message / successfully_sent) * 10000`
- **Click rate** = `(opened_url / successfully_sent) * 10000`
- **Conversion rate** = `(orders_count / successfully_sent) * 10000`

Where:

- `successfully_sent` = count of the campaign's channel-log rows in DELIVERED / SEEN / CLICKED status.
- `seen_message` = count of rows in SEEN status.
- `opened_url` = count of rows where a tracked link was clicked (CLICKED status).
- `orders_count` = attributed orders — see [[campaigns-stats-attribution]] for the exact join + revenue-status filter.

## Business rules

- **The 10000× multiplier is intentional — not a bug.** The platform stores each rate as `(count / total) * 10000`, so a ratio of 0.523 becomes 5230. The percent formatter then divides by 100 and formats with the locale-appropriate decimal separator → "52.30%". This avoids float-precision issues when storing percentages and appears across all four rate fields (and the per-step conversion-rate cells in [[campaigns-stats-step-table]]).
- **Only the Turnover card is clickable.** It is wrapped in a link that opens [[marketing-campaigns-statistics-full]] as a wide side-panel. The other four cards are static.
- **Numbers come from stored counters, refreshed hourly.** The card values read straight from columns on the campaign record (`total_sent`, `successfully_sent`, `seen_message`, `opened_url`, etc.) — no live query at view time. They lag real sends by up to 60 minutes. See [[campaigns-stats-aggregation]].
- **A just-launched campaign shows partial / zero numbers.** Because the aggregation runs hourly, a campaign refreshed minutes after launch shows incomplete figures; the merchant should wait for the next run.

## How it works

The five cards are populated by the `statisticsOverview` JSON-API query, which returns the campaign metadata plus the stored KPI counters. The rates are derived from those counters using the formulae above; `successfully_sent` is the denominator for all three rate KPIs. Because the values live on the campaign record (not recomputed from the statistics store at view time), the cards render fast even for very large campaigns. The Turnover figure and `orders_count` derive from order attribution metadata — see [[campaigns-stats-attribution]].

## Related

- [[marketing-campaigns-statistics]] — hub.
- [[marketing-campaigns-statistics-full]] — revenue list opened by the Turnover card.
- [[campaigns-stats-step-table]] — per-step breakdown of the same metrics.
- [[campaigns-stats-attribution]] — how `orders_count` / Turnover are attributed.
- [[campaigns-stats-aggregation]] — when the counters refresh.
- [[campaign]] — Campaign entity carrying the counters.

## Open questions

No outstanding questions.
