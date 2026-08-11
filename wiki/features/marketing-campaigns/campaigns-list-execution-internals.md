---
type: feature
nav_path: "Marketing → Campaigns → Execution internals"
route_name: campaigns
route_path: /admin/marketing-new/campaigns
aliases: ["Campaign enrolment pipeline", "Campaign send pipeline", "Campaign statistics aggregation", "Campaign queue internals", "Campaign statistics store"]
tags: [marketing, campaigns, queue, statistics, internals]
plan_gates: ["campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[marketing-campaigns]]. See the hub for the other aspects (tabs & filters, create modal, AI assistant, row actions, types & actions, rules).

# Campaigns — execution and statistics internals

## Purpose

This aspect documents the queue-driven enrolment and send pipeline that runs once a campaign is launched, the batching parameters that control ramp-up speed, and the separate statistics store that backs the log + statistics surfaces. Useful for support agents diagnosing *"my campaign launched 30 minutes ago but no messages went out yet"* or *"the orders column on the list page is stale"*.

## Where to find it

This logic is invisible to the merchant directly. The merchant sees its effects on:

- The Campaigns list `reached` / `orders` / `turnover` columns (hourly aggregation).
- The per-campaign [[marketing-campaigns-statistics]] dashboard.
- The per-message [[marketing-campaigns-statistics-log]] view.
- The [[background-queue-inventory]] Queue View page.

## What the merchant can do here

Nothing directly — the merchant configures the campaign and clicks Start; the rest is platform-internal. The merchant CAN observe ramp-up via the Queue View ([[background-queue-inventory]]).

## Settings & fields

This aspect has no merchant-configurable settings. The list of pipeline stages and the statistics-store roles are documented below for reference.

## Business rules

### List tabs share one query pipeline

Status values are integer-based (Active = 1, Inactive = 0, Draft = 2). Each list tab is just a pre-set filter over the same campaign data — `active`, `inactive`, `draft`, `archived`, `notArchived`, `regular`, `automated` — plus counters that attach `actions_count` and `subscribers_count`.

The list tabs are thin wrappers around one shared list pipeline that runs the grid query and per-row formatting. There are five lists, all backed by the same campaign data and the same filters:

- Active list — campaigns that are active and not archived.
- Inactive list — campaigns that are inactive and not archived.
- Archived list — campaigns with an archive date set.
- Draft list — campaigns in Draft (`active = 2`). Does NOT compute order statistics (drafts have no orders).

Each row is enriched with statistics from the order-attribution lookup — which loads orders tagged with this campaign's ID (the `cc_campaign_id` order tag).

### Banned-reason calculation per row

The list-row formatter computes per-row `banned` reasons by walking each action's channel:

- If the action references a missing channel mapping → *"Missing channel type: {name}"*.
- If the channel itself has a current suspension reason → that reason (see [[campaigns-list-rules]] suspension-reasons table).

These badge into the title cell so the merchant sees "why this campaign is broken" right in the list. Full surface: [[marketing-campaigns-banned-info]].

### Send pipeline is queue-driven

Backend execution is queue-driven:

1. **Enrolment jobs** add subscribers to the campaign (build its subscriber-enrolment list).
2. **Execution jobs** process steps (advance subscribers through the action graph).
3. **Per-channel message-send jobs** deliver (one job per channel per batch).

Aggregated stats are written by the hourly statistics job; per-channel reputation by a reputation job. The list-page `reached` / `orders` / `turnover` columns therefore reflect the **last completed aggregation run**, not live state.

### Insert batch size for enrolment

When a Regular or Automated campaign launches with **Execute campaign for existing subscribers in segment** ON, the platform builds the enrolment list and adds subscribers in batches of **500 per insert**. Subsequent action-processing then chunks subscribers into batches of **50 per execute-parts queue job**. For a 10 000-subscriber segment this means 20 inserts followed by 200 execute-parts jobs — the campaign appears to "ramp up" rather than fire all messages at once.

### The statistics store backing logs + statistics

Campaign logs and stats live in a separate statistics store (not the main store database), split into five role-based areas:

| Store area | Grain | Used by |
|-----------------|-------|---------|
| Channel logs | One entry per (campaign, subscriber, channel) delivery attempt | [[marketing-campaigns-statistics-log]] |
| Channel statistics | Aggregated counters per (campaign, channel) | [[marketing-campaigns-statistics]] |
| Channel statistics history | Historical snapshots | [[marketing-campaigns-statistics]] time-series |
| Channel counter | Fast real-time increments | Real-time send count |
| Statistic missing-mapping | Diagnostic entries for unresolvable subscribers | Support diagnosis |

(These are role-based descriptions of what each area holds, not internal names.)

### Auto-archive on completion (Regular only)

A Regular campaign auto-archives on completion (sets `progress = completed` AND `archived_at = now`). Automated campaigns can keep running indefinitely. The auto-archive happens at the end of the final send batch — not as a separate scheduled job.

### Order attribution via the `cc_campaign_id` order tag

Orders are linked to campaigns by a `cc_campaign_id` tag stored against the order. The list-row order-statistic lookup reads this tag to compute the `orders` and `turnover` columns. The campaign ID stamped onto the order is the **last-touch** value from the customer's session at order-place time — see [[marketing-campaigns-statistics-full]] for the full attribution mechanic.

### Aggregation lag = 60 minutes max

The reached / opened / clicked / orders / turnover columns are populated by the hourly campaign-statistics aggregation job. The list table tooltip explicitly states: *"The statistical information is updated every hour"*. Real-time delivery numbers (sent count) update faster via the real-time channel counter, but engagement metrics (open / click / conversion) lag by up to 60 minutes.

## Related

- [[marketing-campaigns]] — hub.
- [[campaigns-list-rules]] — channel-suspension reasons table referenced by the banned-row calculation.
- [[marketing-campaigns-banned-info]] — banned-reason title-cell badges.
- [[marketing-campaigns-statistics]] — per-campaign statistics dashboard (reads Channel statistics).
- [[marketing-campaigns-statistics-log]] — per-message log view (reads Channel logs).
- [[marketing-campaigns-statistics-full]] — full last-touch attribution mechanic.
- [[background-queue-inventory]] — Queue View — observe enrolment + execute-parts + send jobs in flight.
- [[notification-delivery]] — outbound delivery internals (the per-channel send jobs).

## Open questions

- Exact internal names of the five statistics-store areas (the descriptions above are role-based; confirm against current backend before quoting verbatim). (verify)
- Whether the 500 / 50 batch sizes are configurable per merchant or platform-fixed. (verify)
