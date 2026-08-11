---
type: feature
nav_path: "Marketing → Campaigns → Statistics → Attribution metadata"
route_name: campaigns.statistics.full.revenue
route_path: /admin/campaigns/statistics/full/revenue
aliases: ["Campaign attribution metadata", "orders_meta campaign rows", "cc_campaign meta", "Attribution snapshot", "Поръчка — метаданни за кампания"]
tags: [marketing, campaigns, statistics, attribution, orders-meta]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-05-23
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-campaigns-statistics-full]]. See the hub for the other aspects (dashboard, revenue panel, attribution mechanic, revenue statuses, order processing).

# Attribution metadata stamped per order

## Purpose

When a campaign click leads to an order, the platform writes a fixed set of `orders_meta` rows to that order. These rows are the **source data** for every Campaign / Subscriber / Channel / Step column on the revenue panels — they are what make per-campaign and per-step attribution possible. This page is the canonical catalogue of those rows and why each one is a point-in-time **snapshot**.

## Where to find it

The metadata is not a screen — it backs the [[campaigns-stats-full-revenue-panel]] columns. Support agents reading raw order data will see these as `orders_meta` parameter rows on an attributed order.

## What the merchant can do here

Nothing is editable. The merchant consumes this metadata indirectly through the revenue panels and the per-campaign / per-step statistics. The value to the merchant: even if a campaign is later renamed, deleted, or the customer deletes their profile, the order keeps its original attribution.

## Settings & fields

### The meta rows written per attributed order

The attribution write (via the queued order-processing job — see [[campaigns-stats-full-order-processing]]) batches these `orders_meta` rows:

| Parameter | Value | Set when |
|-----------|-------|----------|
| `cc_campaign_id` | Campaign ID | Always (subscriber-attribution path) — per-campaign attribution lookup. |
| `cc_campaign_name` | Campaign title snapshot | Always — display fallback if campaign is renamed/deleted. |
| `cc_campaign_subscriber_name` | Subscriber full name | Always — keeps the subscriber name on the revenue table even after profile deletion. |
| `referer` | Campaign title (legacy "referer" meta) | Always. |
| `cc_campaign_action_id` | Step (CampaignAction) ID | Only if `action` is set in campaignData — per-step attribution lookup. |
| `cc_campaign_action_order` | Step order (0-based) | Only if `action` is set — displayed +1 for 1-based step numbering. |
| `cc_campaign_action_type` | Action type string (e.g. `email`) | Only if `action` is set. |
| `cc_campaign_channel` | Channel mapping (same as action_type for delivery channels) | Only if `action` is set — drives the Channel column. |

## Business rules

### Everything is a snapshot at click time

The metadata snapshots the campaign's state at the moment of the click. So even if the campaign is later renamed or the step is deleted, the order keeps its attribution exactly as it was. This is why:

- The Campaign column reads from `cc_campaign_name` (the snapshot), not the live campaign title.
- The Subscriber column survives profile deletion via `cc_campaign_subscriber_name`.
- Soft-deleted campaigns still show on the revenue list with their snapshot name — see [[campaigns-stats-full-revenue-panel]].

### Action-level rows are conditional

The four `cc_campaign_action_*` / `cc_campaign_channel` rows are written **only if an action (step) was identified** in the captured campaign data. Orders attributed to a campaign without a resolved action carry only the campaign-level rows; the Step and Channel columns then fall back to "N/A".

### Step order is 0-based in storage

`cc_campaign_action_order` is stored **0-based**. Every display surface adds +1 — see [[campaigns-stats-full-revenue-panel]].

### Channel mapping mirrors the action type

For delivery channels, `cc_campaign_channel` equals the action type (e.g. `email`). The revenue panel resolves it to a channel name, falling back to "N/A" if the row is missing (legacy orders pre-dating channel tracking).

## Related

- [[marketing-campaigns-statistics-full]] — hub.
- [[campaigns-stats-full-revenue-panel]] — the table whose columns this metadata populates.
- [[campaigns-stats-full-attribution-mechanic]] — how the campaign data gets captured before this write.
- [[campaigns-stats-full-order-processing]] — the job that writes these rows.
- [[order]] — Order entity that carries the meta rows.
- [[campaign]] — Campaign entity (the snapshotted name / id).

## Open questions

No outstanding questions.
