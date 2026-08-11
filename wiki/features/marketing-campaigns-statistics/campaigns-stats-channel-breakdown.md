---
type: feature
nav_path: "Marketing → Campaigns → Statistics → Channel breakdown"
route_name: campaigns-statistics
route_path: /admin/marketing-new/campaigns/statistics/:id
aliases: ["Per-channel breakdown", "Campaign channel cards", "Email SMS Viber Web Push totals", "Greyed-out channel card"]
tags: [marketing, campaigns, statistics, channels]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-campaigns-statistics]]. See the hub for the other aspects (KPI cards, step table, attribution, aggregation, logs modal).

# Campaign statistics — per-channel breakdown

## Purpose

Below the headline KPI cards, the Campaign statistics page shows a **per-channel breakdown** — one card per channel the campaign actually uses, so the merchant can see how much volume each channel (Email / SMS / Viber / Web Push / Messenger) carried. This page documents what each channel card shows, the underlying per-channel counter fields, and why some channel cards appear greyed out.

## Where to find it

The per-channel cards are the second row on the Campaign statistics page (Sidebar → **Marketing** → **Campaigns** → Statistics icon on a row), directly below the five headline KPI cards ([[campaigns-stats-kpi-cards]]) and above the per-step table ([[campaigns-stats-step-table]]).

## What the merchant can do here

- **See per-channel send volume** at a glance — total sent vs successfully sent for each channel the campaign uses.
- **See which channels are wired into the campaign but have produced no data** — greyed-out cards.
- These cards are informational; the per-recipient detail lives in the per-step Logs modal ([[campaigns-stats-logs-modal]]).

## Settings & fields

One card per channel actually used by the campaign:

| Channel | Card content |
|---------|--------------|
| Email | "Total sent: N" / "Successfully sent: M" |
| SMS | Same shape |
| Viber | Same shape |
| Web Push | Same shape |
| Messenger | Same shape (legacy) |

The per-channel breakdown reads from a per-(campaign, channel) aggregation refreshed hourly. Counter fields:

| Field | Meaning |
|-------|---------|
| `total_sent` | Count of send attempts (any status). |
| `successfully_sent` | Count of SENT / DELIVERED / SEEN / CLICKED. |
| `seen_message` | Count of SEEN. |
| `opened_url` | Count of CLICKED. |
| `unsubscribed` | Count of UNSUBSCRIBED. |
| `abuse` | Count of ABUSE_REPORT. |
| `bounced` | Count of BOUNCED + HARD_BOUNCED. |
| `reached` | Unique subscribers reached. |

(The cards themselves surface `total_sent` and `successfully_sent`; the remaining fields feed the headline KPIs in [[campaigns-stats-kpi-cards]] and the per-step rows in [[campaigns-stats-step-table]].)

## Business rules

- **Channels with zero sends are greyed out, not hidden.** If a channel is a step in the campaign but has produced no sends (e.g., a Viber step the merchant added yesterday into a segment with no phone numbers), its card is rendered greyed-out via CSS `filter: grayscale(100%); opacity: 0.6` (applied to both the card title and the box-section). This lets the merchant see the channel is wired in while visually de-emphasising the empty data.
- **A card appears only for channels the campaign uses.** Channels never added as a step do not get a card at all — greying is reserved for added-but-empty channels.
- **The numbers lag by up to 60 minutes.** Like every aggregated figure on this page, the per-channel totals refresh hourly. See [[campaigns-stats-aggregation]].

## How it works

The per-channel cards are populated by the `statisticsChannels` JSON-API query, which returns per-channel totals scoped to this campaign (a separate aggregation that rolls the channel-log rows up by channel, returning `total_sent` + `successfully_sent` per channel — campaign-scoped, not the global per-channel stat). The query is independently loading-state aware: while it resolves, the row shows a skeleton placeholder, then populates. The same channel-log rows that back these totals are what the per-step Logs modal lists per recipient — see [[campaigns-stats-logs-modal]].

## Related

- [[marketing-campaigns-statistics]] — hub.
- [[campaigns-stats-kpi-cards]] — the headline KPIs the per-channel fields feed.
- [[campaigns-stats-step-table]] — the per-step rollup of the same channel-log data.
- [[campaigns-stats-aggregation]] — when the per-channel totals refresh.
- [[marketing-channels]] — channel-level reputation; bounces / spam here roll up to channel reputation.
- [[marketing-campaigns-statistics-log]] — the per-recipient delivery log behind these totals.

## Open questions

No outstanding questions.
