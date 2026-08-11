---
type: feature
nav_path: "Marketing → Segments → Rebuild mechanics"
route_name: segments.core_new.list
route_path: /admin/marketing-new/segments
aliases: ["Segment rebuild", "Segment cadence", "set_subscriber_to_segment", "set_subscribers_to_single_segment", "subscribers.max_id", "SegmentExists cache"]
tags: [marketing, segments, background-jobs, queues, events]
plan_gates: ["segments", "subscribers"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[marketing-segments]]. See the hub for related aspects (list page, types, conditions, inactive errors).

# Segments — rebuild mechanics

## Purpose

This aspect documents the **backend cadence** that keeps segments in sync: the 5-minute Automated sweep, the on-save single-segment rebuild, the per-event incremental job, the anti-duplication logic on attach, the pause-on-import behaviour, the `subscribers.max_id` cap mechanism that enforces the `subscribers` plan feature, the cached `SegmentExists` family checks, and the exact firing semantics of the output events.

## Where to find it

Mostly invisible to the merchant — surfaced indirectly via the **Last generated at** column on [[segments-list-page]], the orange spinner during `processing = true`, and the marketing-app notifications when a segment changes state.

## What the merchant can do here

- Trigger a One-time rebuild by saving an edit on [[marketing-segments-editor]] OR by clicking manual re-generate.
- Wait for the 5-minute sweep to catch Automated segments (no merchant action needed).
- Observe the **Last generated at** column to know when the last rebuild completed.

## Settings & fields

This aspect has no direct settings/fields — it documents background behaviour. The user-facing controls that influence rebuild cadence are:

- **Type** (One-time vs Automated) — see [[segments-types]].
- **Active** switch — inactive segments are excluded from sweeps.

## Business rules

### Automated-segment cadence — every 5 minutes

The recurring background sweep that rebuilds **Automated** segments fires every **300 seconds (5 minutes)** by default (the `set_subscriber_to_segment` task, `interval: 300`). The sweep filters segments to `channel = 'cloudcart' AND active = 1 AND type = 'automated'` — **One-time segments are excluded from this sweep entirely**. The cadence is shorter (60 seconds) on dev environments. There is no separate cron for Automated segments — this single recurring task IS the cadence.

When a single subscriber-side event fires (signup, order, opt-in change, etc.), an incremental job (`set_subscriber_to_segment_execute`) is enqueued with that one subscriber's id; it re-evaluates ALL active automated segments for that one subscriber rather than waiting for the next 5-minute sweep. This is what makes Automated segments feel "live" for individual subscribers while keeping full-population rebuilds on a slow cadence.

### One-time rebuild — triggered explicitly on save

When the merchant saves an edited segment (Create or Update), the API also dispatches `set_subscribers_to_single_segment` — this runs the rebuild for the just-saved segment **regardless of type** (One-time or Automated). So edits to a One-time segment DO cause a fresh rebuild — there is no separate manual "Generate" trigger needed after a conditions edit. The merchant manually re-generating later runs the same single-segment job again.

### Subscriber attach is anti-duplication-aware

The attach step will NOT re-add a subscriber that is already in the segment with `manual = 0` AND `resend = 0` — only new (or `resend = 1`) subscribers go through. Attach is also batched in **500-subscriber chunks**, and the `SubscribersAddedToSegment` event fires once per chunk with the IDs that were actually added (not all that were attempted).

### Pause-on-import — auto-restart with delay

If a CSV subscriber import is in flight (the bulk-import job on the `subscribers` queue), the segment-evaluator job **delays itself by 300 seconds** and restarts. Rationale: don't churn segments during a bulk insert. The merchant doesn't see this in the UI — it manifests as "Last generated at" not updating until the import finishes.

### Subscriber-cap implementation — `subscribers.max_id` setting

The plan's `subscribers` feature cap is enforced via a stored `subscribers.max_id` setting, NOT a per-query limit. A background job (`get_set_max_id_for_subscriber`, 10-minute interval) walks the marketable subscribers in signup order (`bounced = 0`, `unsubscribed = 0`, `marketing = 1`) and stores the id of the Nth one (where N = plan limit). Every segment rebuild then only considers subscribers up to that stored id. Consequences:

- The first N **chronologically-earliest** opt-ins are eligible; later signups are silently excluded from segment evaluations until the merchant upgrades.
- If a merchant prunes old subscribers (bulk-delete bounced/unsubscribed), the next 10-minute job re-runs the max-id calculation and admits previously-blocked newer subscribers.
- This is per-store and runs as a single-flighted job (no duplicate runs).

### Cached "are there any segments using condition X?" checks

The platform caches an aggregate per condition family (`SegmentExists`) for **24 hours**. The cache keys it tracks: `cart`, `order`, `cart_order`, `last_active`, `payment`, `shipping`, `form`. Used to short-circuit downstream pipelines — e.g., a subscribe-form submission only queues `set_subscriber_to_segment_execute` if at least one segment uses the `form` condition. When a segment is created or deleted, the cache for any condition family it references is invalidated immediately.

### Output events — exactly when each fires

- **`SubscribersAddedToSegment`** — fires inside the attach step once per 500-subscriber batch, carrying the actual added subscriber IDs (not all attempted). Listened to by the subscriber-log listener which queues `add_subscriber_to_segment_log` (writes a row to the segment log store on the `segments1` queue, single-flighted) — feeds [[marketing-segments-log]].
- **`SubscribersRemovedFromSegment`** — fires once per 500-subscriber batch of removals. Same log-write pipeline.
- **`SubscribersResendFromSegment`** — fires when subscribers' `resend` flag is reset (after a campaign send completes); does NOT write to the segment log store by default.
- **`SegmentCreated`** / **`SegmentUpdated`** — fire after the save commits, before the rebuild job is enqueued.
- **`SegmentPopulated`** — fires after a rebuild completes (success OR mid-rebuild auto-disable — see [[segments-inactive-errors]]).
- **`SegmentDeleted`** — fires after the segment is permanently deleted (after a soft-delete first); deletion also detaches every subscriber's segment membership. The segment log store is cleared only when the segment is permanently deleted (when its `deleted_at` timestamp is set).

These events feed [[marketing-campaigns]] (re-trigger sends), the customer marketing-change log, and any installed app listening for them.

### Allowed-combinations check at evaluation time, not just save

When the evaluator runs, it ALSO calls the disable-check. If the result is non-empty, the segment self-disables mid-rebuild — see [[segments-inactive-errors]] for the full flow.

### Segment delete cascade

Deleting a segment detaches every subscriber's membership in it, then fires `SegmentDeleted`. The segment log store is cleared only on the permanent-delete path (when the `deleted_at` timestamp is already set AND the segment is being hard-deleted). Soft-deleted segments retain their logs.

### Cache placeholder while filtering

For large stores, recomputation is chunked (500-row batches). The merchant sees the placeholder *"Your subscribers are currently being filtered, please check again later"* while a job is in flight; the **Last generated at** timestamp updates on completion. The [[segments-list-page]] orange-spinner indicator is driven by the same `processing = true` flag.

## Related

- [[marketing-segments]] — hub.
- [[segments-types]] — One-time vs Automated decides cadence.
- [[segments-list-page]] — shows the spinner / **Last generated at** that this aspect drives.
- [[segments-inactive-errors]] — the mid-rebuild self-disable path.
- [[segments-api-and-plan-gates]] — the `subscribers` cap that `subscribers.max_id` enforces.
- [[marketing-segments-log]] — the segment log store written by `add_subscriber_to_segment_log`.
- [[marketing-campaigns]] — consumes the output events for re-sends.
- [[background-queue-inventory]] — full catalogue of background processes; covers the 300-second automated-segment rebuild and 10-minute subscriber-cap recomputation.

## Open questions

- 📡 **Subscriber-side events that trigger incremental rebuild.** The exact list of events that enqueue `set_subscriber_to_segment_execute` for a single subscriber (verify).
