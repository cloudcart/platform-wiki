---
type: feature
nav_path: "Apps → Stores Sync → Real-time sync"
route_name: apps.stores-sync.overview
route_path: /admin/apps/stores-sync
aliases: ["Stores Sync real-time", "Stores Sync per-variant sync", "Stores Sync quantity dirty-flag", "Stores Sync import4 queue", "Stores Sync search re-index"]
tags: [apps, administration, multi-store, sync]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[apps-stores-sync]]. See the hub for the other aspects (sync model, full sync, API + conflicts).

# Stores Sync — real-time per-variant sync

## Purpose

This page explains the **automatic, real-time** half of Stores Sync: how a stock change on one participating store reaches the others within seconds, what does and does not trigger it, and the timing / failure behaviour the merchant should expect. The merchant does not press any button for this — it happens on every qualifying quantity change.

## Where to find it

There is no dedicated screen for real-time sync — it runs in the background once Stores Sync is active on the participating stores. The on-demand bulk equivalent is the **Full sync** button on [[apps-stores-sync-settings]]; see [[apps-stores-sync-full-sync]].

## What the merchant can do here

- Nothing manual — real-time sync is automatic.
- Indirectly control it by toggling the app on / off per store, and by the `tracking` flag (see [[apps-stores-sync-model]]).
- Trust that an order placed, a manual quantity edit, or a return on store A updates the matching SKU on every other participating store.

## Settings & fields

Real-time sync has no fields of its own. It inherits `compare_by` and `selectedSites` from [[apps-stores-sync-settings]] (documented on [[apps-stores-sync-model]]).

## Business rules

### Only a `quantity` change fires the sync

The platform watches Variant updates and **only** fires the sync when the `quantity` column is "dirty" (actually changed on the save). Edits to SKU, barcode, price, name, or status do **not** trigger sync. This is what makes the sync "real-time inventory only" — orders, manual stock edits, and returns all touch quantity and propagate; everything else stays local to the store.

### What happens on a qualifying change

When a variant's quantity changes on a participating site (an order is placed, the merchant edits the quantity, etc.), the platform queues a background sync task. That task loads the variant, finds the matching variant on each target site (per `compare_by`), and writes the new `quantity` value. It then re-fires the target's search indexing so stock-aware searches stay in step (see below).

### Queue routing: real-time on `import4`

Per-variant real-time sync tasks run on the `import4` queue. Full-sync orchestration runs on the slower-priority `import6` queue (see [[apps-stores-sync-full-sync]]). The two are intentionally separated so heavy bulk runs don't starve the real-time per-order syncs of workers.

### 180-second SLA per sync task

Each `cc_sync_quantities` queue task is dispatched with a **180-second timeout**. If a real-time sync takes longer than 3 minutes (slow network, busy target site), the platform considers it failed; subsequent quantity edits queue fresh tasks. There is no automatic retry of the failed task itself — the next quantity change is what re-syncs that variant.

### App must be ACTIVE on each side

The sync task short-circuits if the source-side or target-side has Stores Sync **deactivated**. Toggling the app off on any participating site stops sync **from** that site immediately — but other sites in the mesh still sync among themselves. Re-activating does **not** backfill missed updates; only future quantity changes resume syncing. To reconcile after a period with the app off, run a [[apps-stores-sync-full-sync|Full sync]].

### Search-index re-fire after each sync

After updating the target variant's quantity, the platform fires a search-engine re-index event on the **target** side. This re-indexes that product in the target store's search engine so stock-availability-aware searches return the new value. Without this, the target's search index would show stale stock until the next routine re-index. See [[inventory-tracking]] for the broader stock-change side-effects.

### Task-name isolation from Multilang

Stores Sync and [[apps-multilang]] share queue infrastructure but use **different task names**. The `cc_sync_quantities` task belongs to Stores Sync; the Multilang cleanup task (`multylang_sites`) belongs to Multilang. They don't conflict.

## Related

- [[apps-stores-sync]] — hub.
- [[apps-stores-sync-settings]] — supplies `compare_by` + `selectedSites`.
- [[apps-stores-sync-full-sync]] — on-demand bulk equivalent; the way to reconcile after the app was off.
- [[apps-stores-sync-model]] — what syncs + the tracking-flag gate.
- [[inventory-tracking]] — stock-change side-effects (search re-index, webhooks).
- [[apps-multilang]] — shares queue infrastructure, different task name.

## Open questions

None.
