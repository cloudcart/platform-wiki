---
type: feature
nav_path: "Marketing → Campaigns → Statistics → Hourly aggregation"
route_name: campaigns-statistics
route_path: /admin/marketing-new/campaigns/statistics/:id
aliases: ["Campaign statistics aggregation", "Hourly stats refresh", "Auto-archive completed campaign", "Statistics lag", "60-minute lag", "Stat counter refresh"]
tags: [marketing, campaigns, statistics, aggregation, jobs]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-campaigns-statistics]]. See the hub for the other aspects (KPI cards, channel breakdown, step table, attribution, logs modal).

# Campaign statistics — hourly aggregation

## Purpose

Every number on the Campaign statistics page (except the raw real-time sent count) is produced by a **scheduled aggregation that runs hourly**. This page documents the refresh cycle, the up-to-60-minute lag the merchant sees, the auto-archive of completed Regular campaigns, the 7-day post-archive window, and the storage / performance notes that explain why the dashboard renders fast.

## Where to find it

This is back-end behaviour, not a screen. Its visible surface is the info-tip line on the Campaign statistics page — *"The statistical information is updated every hour"* — and the fact that completed Regular campaigns silently appear on the [[marketing-campaigns-archive|Archived tab]]. The merchant consults this page to understand why numbers lag or why a finished campaign moved itself to Archived.

## What the merchant can do here

This is a reference page — no merchant actions. What the merchant needs to know:

- **Wait for the next hourly run** before trusting open / click / conversion / revenue numbers on a freshly-launched campaign.
- **Expect completed one-shot (Regular) campaigns to auto-archive** without any action.
- **Know that the raw sent count is near-real-time** even while aggregated figures lag — visible in [[marketing-campaigns-statistics-log]] immediately.

## Settings & fields

- **Refresh interval** — hourly (3600s), one execution cycle per platform, single-instance.
- **Lag** — aggregated open / click / conversion / revenue figures lag by up to 60 minutes. The raw `total_sent` updates as messages fire.
- **Counters refreshed** — `total_sent`, `successfully_sent`, `seen_message`, `opened_url`, `unsubscribed`, `abuse`, `bounced`, `reached`. These are stored on the campaign record itself and feed the headline KPI cards ([[campaigns-stats-kpi-cards]]).
- **Auto-archive condition** — a **Regular** campaign with `successfully_sent >= subscribers_to_campaign_count > 0` is marked `progress = 'completed'` and `archived_at = now`.
- **Post-archive eligibility window** — 7 days (recently-archived Regular campaigns still get hourly updates for a week).

## Business rules

- **Numbers lag by up to 60 minutes.** Between hourly runs, aggregated figures are stale; only the raw sent count is live. The info-tip line is the merchant's reminder. A merchant who launches a campaign and refreshes two minutes later sees partial numbers — they should wait for the next run.
- **Completed Regular campaigns auto-archive silently.** A Regular (one-shot) campaign that finishes dispatching to all enrolled subscribers moves to the Archived tab on the next hourly aggregation — with no merchant interaction. This is intentional: merchants don't need to manually archive completed one-shot campaigns. **Automated campaigns NEVER auto-archive** — they are considered always-running by design.
- **Recently-archived campaigns still update for a week.** The eligibility query includes Regular campaigns that are either not archived OR archived within the last 7 days — so a campaign auto-archived yesterday still gets one more hourly update, useful for catching late-arriving SEEN / CLICKED webhooks. After 7 days from archive the campaign is excluded to save processing on cold campaigns. Automated campaigns are always included regardless of archive state.
- **System / unscoped events are excluded.** The aggregation filters to real subscriber sends only (subscriber id greater than 0) — synthetic platform events with no subscriber do not pollute campaign counters.
- **Stat counters live on the campaign record.** After aggregation, the per-campaign counters are stored as columns on the campaign — so the headline KPI cards read straight from those columns with no live statistics query at view time. The per-step grid ([[campaigns-stats-step-table]]) still reads the (smaller) per-action dataset on demand.
- **Soft-deleted campaigns return 404, but their revenue survives.** The stats route respects the soft-delete scope (a deleted campaign returns 404). The attributed-orders list ([[marketing-campaigns-statistics-full]]) sidesteps this by reading from `orders_meta` directly, which survives the campaign delete — see [[campaigns-stats-attribution]].

## How it works

The hourly aggregation dispatches a per-site sub-job which queues one per-campaign job for each non-Draft campaign. Each per-campaign job runs an aggregation over the channel-statistics collection for all of the campaign's stat rows since its start-of-day, updates the campaign's counters, and — for completed Regular campaigns — flips the campaign to completed + archived.

Performance protections: the aggregation forces a specific statistics-history index (an explicit index hint) so the query planner uses a predictable plan even on a hot collection with many writers; and the per-channel summary is a separate campaign-scoped aggregation (no global stat). Note there is **no automated purge** of the statistics collection — over years of running an Automated campaign with thousands of subscribers it can grow large, and the aggregation reads the filtered collection per query, so very long-running campaigns may eventually see slower hourly runs. The index hint helps but is not a substitute for retention. **(verify whether any retention policy has since been added.)**

## Related

- [[marketing-campaigns-statistics]] — hub.
- [[campaigns-stats-kpi-cards]] — the stored counters this job refreshes.
- [[campaigns-stats-step-table]] — the per-action grid read on demand.
- [[campaigns-stats-attribution]] — why deleted campaigns keep a revenue list.
- [[marketing-campaigns-archive]] — the Archived tab where completed Regular campaigns land.
- [[marketing-campaigns-statistics-log]] — the near-real-time per-send log (no aggregation lag).

## Open questions

- Verify whether an automated retention / purge policy has since been added to the campaign-statistics collection.
