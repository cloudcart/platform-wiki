---
type: feature
nav_path: "Marketing → Campaigns → Statistics → Per-step table"
route_name: campaigns-statistics
route_path: /admin/marketing-new/campaigns/statistics/:id
aliases: ["Per-step table", "Campaign step statistics", "Per-action statistics", "Step funnel table", "Sent opened clicked per step"]
tags: [marketing, campaigns, statistics, steps]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-campaigns-statistics]]. See the hub for the other aspects (KPI cards, channel breakdown, attribution, aggregation, logs modal).

# Campaign statistics — per-step table

## Purpose

The bottom of the Campaign statistics page is a **per-step table** — one row per campaign step (action), breaking the headline numbers down step-by-step so the merchant can see WHICH part of the funnel performs and which doesn't. This is the difference between "the campaign converts at 3%" and "step 1's email converts at 5% but step 3's SMS converts at 0.2%, so step 3 needs work". This page documents every column, the zero-send guard, and which action types are excluded from the table.

## Where to find it

The per-step table is the bottom section of the Campaign statistics page (Sidebar → **Marketing** → **Campaigns** → Statistics icon on a row), below the headline KPI cards ([[campaigns-stats-kpi-cards]]) and the per-channel breakdown ([[campaigns-stats-channel-breakdown]]).

## What the merchant can do here

- **Read per-step performance** — sent / reached / opened / clicked / unsubscribed / spam / bounced / orders / revenue / conversion-rate for each step.
- **Open a step's per-recipient delivery log** — the **Step** column is a clickable link that opens the Statistics Logs Modal for that step. See [[campaigns-stats-logs-modal]].
- **Open a step's attributed-revenue list** — the per-step Turnover cell drills into [[marketing-campaigns-statistics-full]] scoped to that step.

## Settings & fields

One row per campaign step (action). Columns:

| Field | Label | Meaning |
|--------|-------|---------|
| `action_title` | Step | Rendered as a header + channel icon + step number (clickable → Logs modal). |
| `total` | Total sent | Total send attempts for this step. |
| `reached` | Reached subscribers | Unique successful recipients. |
| `opened` | Opened | Count of messages opened. |
| `clicked` | Clicks | Count of tracked link clicks. |
| `unsubscribed` | Unsubscribed | Count of unsubscribes from this step. |
| `abuse` | Spam | Count of spam complaints. |
| `bounced` | Bounced | Count of bounces. |
| `orders` | Orders | Orders attributed to this step. |
| `revenue` | Turnover | Money-formatted revenue from this step. |
| `conversion_rate` | Conversion rate | % calculated per step. |

The per-step conversion-rate uses the same 10000× storage multiplier as the headline KPIs — see [[campaigns-stats-kpi-cards]].

## Business rules

- **Zero-send guard.** Each row checks `total_sent > 0` before computing rates. If a step has zero sends, all its numeric columns are set explicitly to `0` (not null) and the conversion-rate shows "0.00%" — so the merchant sees a clean row of zeros, never an empty cell or NaN. This is the default state for a campaign that has launched but not yet fired any messages.
- **Only delivery channels appear.** The table shows only action types flagged as visible in statistics on their channel — the delivery channels Email, SMS, Viber, Web Push, Messenger. Non-delivery action types (set_tags, remove_from_campaign, set_customer_group) are excluded, because they have no "send statistics" to show.
- **Per-step orders / revenue are attributed by step.** A step's Orders and Turnover come from order attribution keyed on the per-step `cc_campaign_action_id` metadata — so an order attributed to "Step 3" rolls up to that step's row AND to the campaign's headline Turnover card. See [[campaigns-stats-attribution]].
- **The numbers lag by up to 60 minutes.** Per-step counters refresh hourly along with the rest of the page. See [[campaigns-stats-aggregation]].

## How it works

The per-step rows are populated by the `statisticsActions` JSON-API query. Unlike the headline cards (which read stored counters on the campaign record), the per-step grid is rolled up from the statistics store per campaign action — a smaller dataset than the whole campaign, so it stays fast. Each row merges its per-action send counters with per-step order attribution (the `cc_campaign_action_id` `orders_meta` join — see [[campaigns-stats-attribution]]), then renders the step header with its channel icon + step order. Clicking the Step link opens the per-recipient log for that action — see [[campaigns-stats-logs-modal]].

## Related

- [[marketing-campaigns-statistics]] — hub.
- [[campaigns-stats-kpi-cards]] — campaign-level rollup of the same metrics + the 10000× multiplier.
- [[campaigns-stats-channel-breakdown]] — per-channel rollup of the same channel-log data.
- [[campaigns-stats-attribution]] — how per-step Orders / Turnover are attributed.
- [[campaigns-stats-logs-modal]] — opened by clicking a step row.
- [[campaigns-stats-aggregation]] — when the per-step counters refresh.
- [[marketing-campaigns-statistics-full]] — per-step Turnover drill-down.

## Open questions

No outstanding questions.
