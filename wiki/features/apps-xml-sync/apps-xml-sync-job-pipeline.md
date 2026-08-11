---
type: feature
nav_path: "Apps → XML Sync → Job pipeline"
route_name: apps.xml_sync
route_path: /admin/apps/xml_sync (background pipeline)
aliases: ["XML Sync job pipeline", "XML Sync parse insert pipeline", "XML Sync queue mappings", "XML Sync 12h tick", "XML Sync 1h gate", "XML Sync 250 chunk", "XML Sync auto-uninstall", "XML Sync 3-strike", "XML Sync manual trigger"]
tags: [apps, imports, xml, sync, recurring, queue, pipeline]
plan_gates: ["xml_sync_limit"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[apps-xml-sync]]. See the hub for the other aspects (update policy, discontinued handling, fetch transport, side effects).

# XML Sync — job pipeline

## Purpose

XML Sync runs as a **recurring background pipeline** that re-fetches the supplier feed on a cadence and writes the differences into the catalog. This page documents the three queue tasks, the timing model (the platform-wide tick + the per-task minimum gate), the insert chunk size, how the merchant re-triggers a run by hand, and the lifecycle rules that auto-deactivate failing tasks and auto-uninstall the app when nothing is left to sync.

The pipeline is **architecturally identical to [[apps-xml-import-job-pipeline]]** — the same parse → parse_single → insert structure on the same shared queue — but adds recurring behaviour and a dedicated active-state model. See [[apps-xml-sync]] for the import-vs-sync distinction.

## Where to find it

There is no merchant UI for the pipeline internals. The merchant interacts with it through:

- The task list at Sidebar → Apps → **XML Sync** — create / activate / deactivate tasks.
- The per-task Status page ([[apps-xml-sync-status]]) — run history, current state, `error` column, manual re-trigger.
- The wizard's final step ([[apps-xml-sync-step3]]) — saving it forces an immediate re-parse.

## What the merchant can do here

- Let the pipeline run on its plan-driven cadence (no per-task slider — see [[apps-xml-sync-settings]] for the cadence model).
- Re-trigger a run **manually** without waiting for the timer (two ways, below).
- Deactivate a task to pause its sync; reactivating resumes it.

What the merchant **cannot** do here:

- Set a per-task interval — cadence is plan-wide.
- Force a run more often than the per-task 1-hour minimum gate.
- Keep a task syncing after 3 consecutive failures without re-enabling it manually.

## Settings & fields

Three queue tasks (the app's queue mappings):

| Queue task | Role |
|------------|------|
| `xml_sync_parse` | Full-feed parse — reads + structures every row. |
| `xml_sync_parse_single` | Single-product re-parse — refresh one product (e.g. after an error). Runs via single-task execution with a 60-second timeout. |
| `xml_sync_insert` | DB insert / update job — writes the parsed rows. |

Separating parse from insert means a failure in one stage does not corrupt the other.

Defaults (queue config):

- **Parse interval: 43200 seconds (12 hours)** default.
- Force queue: **`import1`** — shared with [[apps-xml-import]].
- single = false (concurrent tasks allowed).

## Business rules

### 12h tick + per-task 1-hour gate

The platform tick checks every task on the 12h cadence (or a tighter plan-set `xml_sync-interval` — see [[apps-xml-sync-settings]]). On each tick a task is only eligible for re-parse if:

- `last_cron_update` is NULL, OR
- the last run is **more than 1 hour old** AND the task is `updatable = 1` (at least one field has the Update checkbox set in [[apps-xml-sync-step2]]).

So even with a tight plan-wide interval (e.g. hourly), each individual task still has a **hard 1-hour minimum** between re-parses. Multiple tasks belonging to the same merchant can run on the same tick — they queue in parallel up to the worker-pool concurrency.

### Shared `import1` queue

Both XML Sync and XML Import push to the **same `import1` queue**. Heavy XML Sync activity therefore affects XML Import latency and vice versa — they share the same execution slot.

### Per-batch insert chunk: 250 products per job

After parsing, the platform chunks products into batches of **250** and dispatches one `xml_sync_insert` job per chunk to `import1`. (XML Import uses chunks of 50.) The larger sync chunk reflects that sync runs typically only update price / inventory on already-existing products — a lighter per-row workload than full-create imports.

### `xml_hash` short-circuits unchanged feeds

There is **no Last-Modified / If-Modified-Since HTTP-header check** before fetching — the platform always fetches and parses. After parsing it computes a content hash over the feed and stores it on the task. When the next run produces the **same hash, downstream insertion is skipped**. Unchanged feeds still consume network + parsing but write nothing to the catalog. See [[apps-xml-sync-fetch-transport]] for the fetch transport itself.

### Manual trigger: save Step 3, or toggle Active OFF→ON

Saving [[apps-xml-sync-step3]] forces the next queue tick to re-parse the task **immediately** (without waiting for the 12h timer) by re-initialising the parser queue and clearing the feed hash. Toggling the task's Active switch off and then on triggers the same path. There is no separate "Run now" button — these are the two manual-trigger gestures.

### 3-strike auto-deactivate

Identical failure tracking to XML Import: every fetch / parse failure bumps the task's internal `job_id` counter. **On the 3rd consecutive failure the task is auto-deactivated** (active flips to 0). The merchant must investigate the captured `error` and re-enable manually. A successful run resets the counter. Failure strikes also push an in-CP **admin notification** ("alert") so the merchant sees the failure even without opening the Status page; empty-feed responses push an info-level alert separately. The alert carries the **app name + task name + the error text** but **no clickable link** to the task — to investigate, the merchant opens the XML Sync task list / [[apps-xml-sync-status|Status page]] (the task name links to its editor; the red-icon tooltip shows the last error). These strike alerts are in-CP only — no email is sent.

### Auto-uninstall when no active tasks remain

When the **last** sync task is deactivated or deleted, the platform automatically uninstalls the three `xml_sync_*` queue mappings — the app stops consuming queue resources. Creating or activating a new task re-installs them. The merchant does not have to click Uninstall to pause the app entirely; deactivating all tasks does it.

## Related

- [[apps-xml-sync]] — hub.
- [[apps-xml-sync-status]] — run history + manual re-trigger surface.
- [[apps-xml-sync-step2]] — the Update checkboxes that set `updatable`.
- [[apps-xml-sync-step3]] — saving it forces an immediate re-parse.
- [[apps-xml-sync-fetch-transport]] — how the feed is fetched + the `xml_hash` computation.
- [[apps-xml-sync-side-effects]] — what happens downstream of Insert.
- [[apps-xml-import-job-pipeline]] — the architecturally identical import pipeline (chunks of 50).
- [[background-queue-inventory]] — catalogue of background processes; the `import1` queue + recurring sync cadence.

## Open questions

_None._
