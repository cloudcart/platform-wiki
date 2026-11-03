---
type: concept
nav_path: "Concept → Import pipeline → Concurrency lock"
aliases: ["Single-import lock", "Import 409 error", "Concurrent imports lockout", "There cannot be more than imports running simultaneously", "Import working flag"]
tags: [ops, imports, concurrency, locks, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[import-pipeline]]. See the hub for the other aspects (stages, validation, upsert + provenance, plan gates + 2FA, history + recovery, XML Sync).

# Import pipeline — concurrency lock

## Definition

The **single-import lock** is the platform-wide rule that **only one import can be running per store at any time**, across ALL importer types — customers, products, redirects, subscribers, blog articles, XML feeds, JSON imports, and app-specific integrations. Trying to start a second import while one is already in flight returns HTTP 409 with the error message *"There cannot be more than {N} imports running simultaneously."* — the merchant has to wait for the running import to finish (or cancel it from [[settings-queue-view]]) before launching a new one.

The lock is **store-wide, not per-importer-type**: a customer CSV import blocks a product XML sync from starting (and vice versa). The lock isn't smart enough to allow parallelism between unrelated importers — the platform treats "any import running" as occupying the slot.

## Scope

Covered:

- The single-import-at-a-time rule and the HTTP 409 error string.
- Why parallelism is forbidden (resource races, staging-table collisions, search-index rebuild contention).
- The `working = true` flag pattern and lock-release on completion / cancellation.
- How the merchant cancels a stuck import to release the lock.
- What happens to already-imported rows when a cancel lands mid-batch.

Not covered here:

- The wizard stages that lead up to Submit — see [[import-pipeline-stages]].
- How the failed-row counts are surfaced — see [[import-validation-and-errors]].
- The retention of cancelled imports in the audit log — see [[import-history-and-recovery]].

## Contrasts

- **Single-import lock vs queue-job concurrency** — the lock is a logical "an import is running" flag, not a worker-count limit. The underlying queue workers can run other (non-import) jobs in parallel; only IMPORT jobs are mutually exclusive.
- **Store-wide vs per-importer-type** — the lock spans all importer types. A customer CSV blocks a product XML sync.
- **Cancel mid-batch vs full rollback** — cancelling releases the lock but does NOT undo already-imported rows. See "Cancel semantics" below.

## Where it applies

The lock applies at the **Submit** step of every import wizard ([[import-pipeline-stages]]). The merchant clicks Submit on the Map step; the platform checks the lock; if held, returns 409; if free, sets the `working = true` flag and enqueues the job. The lock releases when the job finalises (success OR failure) or when the merchant cancels it.

### Why the lock exists

Concurrent imports would race against each other for shared resources:

- **Temp tables** — customer CSV staging uses `csv_import_<timestamp>` tables that two concurrent customer imports would collide on.
- **ERP staging buffers** — apps that pipe imports into an ERP have a shared in-memory buffer per store.
- **Search index rebuild slots** — the search index re-indexing fans out per imported product; two concurrent product imports would double-enqueue the same SKUs into the `searchable-import4` queue (see [[background-queue-inventory]]).
- **`product.updated` webhook fan-out queue** — two concurrent imports would race to enqueue duplicate webhook deliveries.

Allowing parallelism would frequently corrupt one or both imports' state. The lock is the platform's protection against this class of bug.

### Lock lifecycle

1. **Merchant clicks Submit** on the wizard's Map step.
2. **Platform checks the lock.** If `working = true` is already set by another importer, return HTTP 409 with *"There cannot be more than {N} imports running simultaneously."*
3. **If free**, set `working = true` and enqueue the import job onto its queue (`import1`, `import2`, or app-specific).
4. **Worker picks up the job** and processes rows in chunks (see [[import-pipeline-stages]]).
5. **On completion** (success, failure, or cancel), the worker clears `working = false`. The lock is now free for the next import.

The lock is not a global cluster lock — it is scoped per store. Different stores can each run one import in parallel without contention.

### Cancel semantics — partial rows persist

The merchant can manually cancel a stuck import from [[settings-queue-view]] to release the lock. **Cancelling mid-batch does NOT roll back already-imported rows.** Importer jobs use append/upsert patterns without a transactional wrapper around the full batch — rows already inserted before the cancel command lands stay in the database.

Temp tables (used by customer CSV staging) are cleaned up by the cancel handler, but the inserts already committed into the live store tables remain. Recovery from a partial import requires the same cleanup path as a botched full import: use the "Imported with" filter (for products) or bulk-delete by criteria — see [[import-upsert-and-provenance]] and [[import-history-and-recovery]].

### Practical merchant impact

- **Sequencing required during launches.** A merchant kicking off an XML sync at 9 AM cannot also run a customer CSV import at 9:01 — the second click returns 409. They schedule one after the other. This matters most during store launches and seasonal updates when several types of bulk data are being loaded simultaneously.
- **Stuck imports must be cancelled to unblock.** If a worker hangs or a job fails to release the lock, the merchant goes to [[settings-queue-view]] and cancels the running job. The lock clears immediately.
- **No queueing of next-up imports.** The platform does NOT queue "try again when free" — the 409 is terminal for that attempt. The merchant must manually re-click Submit after the running import finishes.

### Example — concurrent-import lockout

1. Merchant starts a 50,000-row customer CSV import at 14:00 — task starts processing, ETA 8 minutes.
2. At 14:02 the merchant tries to start an XML sync — clicks the sync's "Run now" button.
3. Platform returns HTTP 409 with *"There cannot be more than 1 imports running simultaneously."*
4. Merchant waits for the customer CSV to finish (sees progress in [[settings-queue-view]]).
5. At 14:08 the customer CSV completes; the lock releases.
6. Merchant re-clicks the XML sync "Run now" button — this time it accepts and the XML sync starts.

## Related

- [[import-pipeline]] — hub.
- [[settings-queue-view]] — where the merchant sees and cancels the running import to release the lock.
- [[background-queue-inventory]] — the queue-tier model that runs import jobs in the background.
- [[settings-import-history]] — records cancelled imports in the audit log.

## Open Questions

None.
