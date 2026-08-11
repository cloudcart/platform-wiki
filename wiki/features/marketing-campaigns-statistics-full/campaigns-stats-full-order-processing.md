---
type: feature
nav_path: "Marketing → Campaigns → Statistics → Order processing"
route_name: campaigns.statistics.full.revenue
route_path: /admin/campaigns/statistics/full/revenue
aliases: ["Campaign order processing", "Attribution write job", "Subscriber resolution", "MADE_ORDER stat", "PURCHASE log status", "Обработка на поръчка от кампания"]
tags: [marketing, campaigns, attribution, orders, statistics]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-05-23
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-campaigns-statistics-full]]. See the hub for the other aspects (dashboard, revenue panel, attribution metadata, attribution mechanic, revenue statuses).

# Per-order attribution processing & side-effects

## Purpose

This page documents what happens **when an attributed order is placed** — the queued processing, how the platform figures out which subscriber the order belongs to, the guard against double-attribution, and the two statistical side-effects (`MADE_ORDER` increment and `PURCHASE` log status) that feed the per-step statistics and the per-send log.

## Where to find it

This is back-of-house order processing, not a screen. Its results surface on [[marketing-campaigns-statistics|per-campaign statistics]] (the per-step `orders` column) and the [[marketing-campaigns-statistics-log|per-send log]] (the `PURCHASE` rows).

## What the merchant can do here

Nothing is configurable. The merchant observes the outcome: a guest-checkout order from a campaign click still gets attributed (just without a subscriber name), and per-step order counts appear on the statistics page.

## Settings & fields

No settings. The behaviour described below is a platform invariant triggered automatically on order creation.

## Business rules

### Attribution runs as a queued job, not inline

When an order is placed, the campaign meta-write happens via a **queued** order-processing job, not synchronously inside the order-create flow. So there is a small delay (typically seconds) between order creation and the `orders_meta` rows appearing — a window during which the order is "attributed but not yet stamped". Revenue queries running in that window briefly miss the order. In practice this is invisible to merchants because the dashboard's rate columns are hourly-lagged anyway (see [[campaigns-stats-full-dashboard]]); the meta rows written are catalogued in [[campaigns-stats-full-attribution-metadata]].

### Double-attribution guard

If the order already carries a `campaignData` meta-row, the job aborts cleanly (an `EXECUTE_DESTROY` outcome) — preventing double-attribution. The first run sets `campaignData`; any retry or duplicate dispatch sees the existing meta and exits.

### Subscriber resolution tries up to 6 candidate sources

If the order itself has no `subscriber_id`, the job tries, in order:

1. `campaignData.subscriber_id` from the captured session data.
2. The campaign UUID lookup (subscriber-by-UUID).
3. The channel + identifier lookup (subscriber-by-channel).
4. The order's customer email matched against an EMAIL_CHANNEL row.
5. The order's shipping / billing phone matched against a PHONE_CHANNEL row.

If all fail, the order is attributed as "non-self" (anonymous — meta is still written, but no subscriber linkage). So a **guest-checkout order from a campaign click is still attributed**; the merchant just doesn't see a subscriber name on the revenue table.

### `MADE_ORDER` per-step stat increment

When attribution succeeds AND an action (step) ID is present, the platform increments the per-step `MADE_ORDER` field for that (subscriber, campaign, action) tuple. This is the source of the per-step `orders` column on [[marketing-campaigns-statistics|per-campaign statistics]] — orders attributed to a SPECIFIC step, not just to the campaign as a whole.

### `PURCHASE` log status on the per-send log

After attribution, the platform finds the per-(subscriber, campaign, step) log row and sets its `status` to **`PURCHASE`** — a synthetic status, not from any provider webhook. So the [[marketing-campaigns-statistics-log|per-send log]] shows "PURCHASE" rows for sends that led to orders. The original delivery status (DELIVERED / SEEN / CLICKED) is preserved in `status_archive`, so the timeline tooltip still shows the full lifecycle.

### Click / open events also advance gated steps

Independently of order placement, the same processing path drives drip-campaign progression:

- If a campaign action's completion condition is `link_clicked`, a **click** event sets `continue_condition_date_executed = now` and `condition_is_completed = 1` — immediately unblocking the next step in an Automated campaign. The merchant doesn't wait for a separate scheduler.
- If the condition is `message_read`, the email `SEEN` event applies the same log update. This lets a drip campaign delay Step 2 until the customer opens Step 1's email, rather than N hours after Step 1 is merely sent.

## Related

- [[marketing-campaigns-statistics-full]] — hub.
- [[campaigns-stats-full-attribution-metadata]] — the meta rows this job writes.
- [[campaigns-stats-full-attribution-mechanic]] — how the session data this job consumes was captured.
- [[marketing-campaigns-statistics]] — per-campaign statistics; the per-step `orders` column comes from `MADE_ORDER`.
- [[marketing-campaigns-statistics-log]] — per-send log; shows the `PURCHASE` rows.
- [[order]] — Order entity being processed.
- [[subscriber]] — subscriber resolution target.

## Open questions

No outstanding questions.
