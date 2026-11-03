---
type: feature
nav_path: "Concept → Analytics pipeline → Aggregation"
route_name: ""
route_path: ""
aliases: ["Analytics aggregation", "Hourly aggregation", "13 aggregation jobs", "EXECUTION_TIME_IN_HOURS", "Rollups", "Visitors aggregation"]
tags: [analytics, pipeline, aggregation]
plan_gates: []
created: 2026-06-10
updated: 2026-06-11
source_count: 3
---

> Part of [[analytics-pipeline]]. See the hub for the other aspects (event capture, event processing, dashboard reads, known gaps, backfill commands).

# Analytics — aggregation (hourly batch rollups)

## Purpose

This page covers the **slow lane**: the hourly batch job that reads raw visitor events plus the orders data and writes the summarised rollups the dashboard chart boxes read directly. This is why the merchant waits *up to* one hour for **Total Visits / Conversion Rate / Cart Conversion Funnel** to reflect new activity.

The CloudCart analytics stack is **NOT a real-time stream**. It is a periodic batch aggregation that ticks **once per hour** (`EXECUTION_TIME_IN_HOURS = 1`). The dashboard reads pre-aggregated rollups — no live scan over raw events ever runs at dashboard load.

## Where to find it

Invisible to the merchant. The job runs server-side; merchants see only the lag: visit / cart event boxes update at the top of every hour + 1 minute UTC.

## What the merchant can do here

Nothing directly — aggregation is fully automatic. What the merchant indirectly observes:

- A burst of visits during the current hour does NOT immediately move **Total Visits** — they wait until the next HH:01 UTC tick.
- A change to "primary industry" in the dashboard settings panel does NOT immediately update the comparison badge — the weekly industry-statistic job runs Monday 02:05 UTC, so up to **7 days lag**.
- 13 aggregation areas each feed specific dashboard boxes, listed below.

## Settings & fields

Not applicable — aggregation is automatic. The values that govern timing:

| Setting | Value | Effect |
|---------|-------|--------|
| `EXECUTION_TIME_IN_HOURS` | `1` | The hourly (3600-second) tick interval. |
| Industry-statistic interval | `604800` | The weekly industry-statistic recompute (7 days). |
| Store primary timezone | merchant's setting | Sets the hour / day bucket boundaries — see [[analytics-known-gaps]]. |

## Business rules

- **Whole hours only.** Each tick closes off complete hour buckets — it reads from the last checkpoint to that checkpoint + 1 hour, never "the last hour ending now". The current, still-open hour is invisible until it closes, so the dashboard never shows partial-hour data.
- **Single instance.** Only one aggregation tick runs at a time across the cluster.
- **No gaps, no double-counting.** A checkpoint records the "last execution date" after each window; the next tick resumes exactly where the previous one stopped.
- **Self-catch-up.** If the checkpoint falls more than an hour behind real time, the job re-queues itself so the next worker pass catches up across many hours in one go.
- **Weekly industry comparison uses fixed statuses.** The industry-comparison badge always counts orders in `Paid + Completed + Pending + Authorized + Fulfilled`, NOT the merchant's saved Settings status filter — see [[analytics-known-gaps]] for this comparison asymmetry.
- **Kill-switch aware.** The per-store enable / disable check runs at the top of every fan-out job, exactly as in [[analytics-event-processing]].
- **Admin previews excluded.** Aggregation drops sessions flagged as merchant logged-in / admin previews (visitor IDs beginning with `admin-`), on top of the bot filtering done earlier at capture. See [[analytics-known-gaps]] for the full layered bot-filtering model.

## The hourly tick

The recurring aggregation driver runs every **3600 seconds (1 hour)**, single-instance, and reschedules itself at the **top of the next hour + 1 minute UTC**. So aggregation runs at **HH:01 UTC** every hour, processing only events older than the previous tick. It always closes off whole hour buckets — see [[analytics-known-gaps]] for the DST-on-hour-bucket implications.

The driver and the fan-out work run on separate queue lanes, so the driver can re-schedule itself even when the fan-out backlog is heavy.

## The fan-out — 13 parallel jobs

On each tick the driver fans out **13 parallel jobs**, each writing one rollup:

| Aggregation area | Reads from | Boxes it powers |
|------------------|------------|-----------------|
| Visitors | visitor events | Total Visits, Online store sessions |
| Devices | visitor events | Sessions by device |
| Landing pages | visitor events | Landing pages by traffic |
| Products by traffic | visitor events | Top products by traffic |
| Categories by traffic | visitor events | Top categories by traffic |
| Vendors by traffic | visitor events | Top brands by traffic |
| Traffic source | visitor events | Sessions by Traffic Source (raw + grouped) |
| Visitors by country | visitor events | Sessions by Country |
| Orders rollup | orders data | Aggregate Total Orders box — the hourly snapshot, distinct from the per-order live updates in [[analytics-event-processing]] |
| Cart funnel | visitor events | Cart Conversion Rate, Cart Conversion Funnel, Abandoned Carts, Abandoned Checkouts |
| Top order products | visitor events + order data | Top Products by Sales (per-day and per-hour rolled-up views) |
| Order status fix | orders data | Housekeeping — patches order-status drift from missed events |

(That is 12 rows because traffic source and its grouped output count as one area; the count of 13 includes the chained grouped step.)

## How checkpointing works

Each job processes a single 1-hour window, then records the "last execution date" so the next tick picks up exactly where it left off — guaranteeing **no gaps and no double-counting**. For example, a run at 14:02 UTC with the last checkpoint at 13:00 UTC processes 13:00–14:00 UTC and writes 14:00 as the new checkpoint. The current hour (14:00–15:00 UTC) is not shown on the dashboard until the **next** run.

If the checkpoint is more than an hour behind real time, the job re-queues itself, letting a single worker pass catch up across many hours.

## Industry-statistic — weekly, not hourly

Separate from the 13 hourly jobs, the industry-statistic job runs once per **week** (604800 seconds), restarting every **Monday 02:05 UTC**. It produces the "above / below average for {industry}" comparison badges shown beneath the boxes that carry `hasIndustryCompare: true`.

When it computes each store's metrics for that comparison, it always uses a **fixed status set (Paid, Completed, Pending, Authorized, Fulfilled)** — not the merchant's saved Settings status filter (see [[analytics-dashboard-reads]]) — so cross-merchant comparison stays apples-to-apples. A merchant who has just changed their store's industry won't see the comparison badge update for **up to one week**.

## Effect on the merchant

If the merchant says *"I just got 500 visitors in the last hour but Total Visits hasn't moved"*, the answer is: the dashboard's visitor count updates once an hour, at the top of the next hour. The current hour's visitors won't show until that hour closes and the aggregation job runs at HH:01 UTC. This is also why the "current hour" never shows partial data — aggregation deliberately excludes the still-open hour bucket.

## Related

- [[analytics-pipeline]] — hub.
- [[analytics-event-capture]] — where the raw events being rolled up come from.
- [[analytics-event-processing]] — the fast lane (per-order documents) that runs alongside aggregation.
- [[analytics-dashboard-reads]] — how the dashboard reads the rolled-up data.
- [[analytics-known-gaps]] — DST in hour buckets, retention, kill switches, currency model.

## Open questions

None.
