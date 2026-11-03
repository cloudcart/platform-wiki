---
type: feature
nav_path: "Apps → Stores Sync → Full sync"
route_name: apps.stores-sync.overview
route_path: /admin/apps/stores-sync
aliases: ["Stores Sync full sync", "Stores Sync initial sync", "Stores Sync 24-hour cooldown", "Stores Sync batch sync", "Stores Sync progress bar"]
tags: [apps, administration, multi-store, sync]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[apps-stores-sync]]. See the hub for the other aspects (sync model, real-time sync, API + conflicts).

# Stores Sync — full (bulk) sync

## Purpose

This page covers the **on-demand bulk sync** — the **Full sync** button. It walks every variant in the source store and pushes its `quantity` to all participating stores in one batched run. Merchants use it for the **initial** population of a new sync group and to **reconcile** after a period when the app was off or quantities drifted out of step.

## Where to find it

Sidebar → Apps → Stores Sync → settings → the **Full sync** button. See [[apps-stores-sync-settings]] for the surrounding settings screen.

## What the merchant can do here

- Trigger a full one-pass push of every variant's quantity from the source store to all participating stores.
- Watch a live progress bar (total / pending / completed counts + percent done).
- Close the page and return later — the run continues in the background.

## Settings & fields

The Full sync control has no configurable fields beyond the trigger button itself. It uses the same `compare_by` + `selectedSites` settings as real-time sync (documented on [[apps-stores-sync-model]]). One timestamp governs its availability:

| Field | Meaning |
|---|---|
| `last_full_sync` | Timestamp of the merchant's last full sync. Enforces the 24-hour cooldown (see below). |

## Business rules

### 24-hour cooldown per merchant

The Full sync button is rate-limited to **once per 24 hours** for the merchant (tracked via `last_full_sync`). CloudCart support / console users bypass this cap. The cooldown exists because a full sync queues one task per variant and is expensive at scale.

### How a full run is structured

Triggering Full sync dispatches a bulk-sync job that:

1. Pulls every variant ID in the source store.
2. Chunks them into groups of **100**.
3. Dispatches one bulk task per chunk into a tracked batch.
4. Each chunk task then syncs its variants one by one.

The batch tracks total / pending / completed counts; the settings-page progress bar streams these live to the merchant's open page. The orchestration runs on the slower-priority `import6` queue, kept separate from the real-time `import4` queue so a heavy bulk run doesn't starve per-order syncs — see [[apps-stores-sync-realtime]].

### A new full sync supersedes the previous one

Triggering a Full sync while a previous batch is still running **cancels the old batch in place**. The new batch starts fresh; in-flight tasks from the previous batch detect the cancellation and short-circuit. So the merchant does **not** get a "wait for previous to finish" error — the previous run is abandoned and the new one starts.

### Performance at scale

Each variant is one sync task. With 100k variants the platform queues 100k tasks into the batch; total runtime depends on the queue worker pool and inter-site network latency. The merchant doesn't wait at the screen — the progress bar updates live and the work continues after the merchant navigates away.

### The same gates apply as real-time sync

A full sync still honours the `tracking`-flag-on-both-sides rule and the active-app-on-both-sides rule from [[apps-stores-sync-model]] and [[apps-stores-sync-realtime]]. Variants that fail the `compare_by` match are skipped, exactly as in real-time sync.

## Related

- [[apps-stores-sync]] — hub.
- [[apps-stores-sync-settings]] — the settings screen hosting the Full sync button.
- [[apps-stores-sync-realtime]] — the automatic per-variant counterpart; explains the `import4` vs `import6` queue split.
- [[apps-stores-sync-model]] — what syncs + the match-key + tracking gates that a full run also obeys.

## Open questions

None.
