---
type: concept
nav_path: "Concept → Import pipeline → History & recovery"
aliases: ["Import history", "Import audit log", "No undo on imports", "Import rollback", "Import recovery", "Imported with bulk delete", "Import history retention"]
tags: [ops, imports, audit, recovery, history, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[import-pipeline]]. See the hub for the other aspects (stages, concurrency lock, validation, upsert + provenance, plan gates + 2FA, XML Sync).

# Import pipeline — history & recovery

## Definition

Every import in CloudCart writes rows into the **shared import-history log** visible at [[settings-import-history]]. The history is **indefinitely retained** — there's no auto-purge after N days. Per-import aggregate counts (Created / Updated / No-action / Errors / Total) appear in the list; drilling into any import opens a per-record table with the action applied to each record and a "View detailed change log" modal showing the before/after field values.

There is **no built-in undo / rollback** for any import. Once products are created or customer records updated, the merchant has no one-click way to reverse the change. Recovery paths: use the **"Imported with" filter** ([[products-products]]) to find affected records and bulk-delete; restore from a [[backups-and-restore]] backup (loses unrelated changes); or run a **corrective upsert import** that overwrites the bad data.

## Scope

Covered:

- [[settings-import-history]] structure — aggregate counts + per-record drill-in + change-log modal.
- Indefinite retention and its storage implications.
- All-staff visibility (no per-staff filtering today).
- The three recovery paths when no undo exists.
- How "Imported with" + bulk delete works in practice.
- When to choose backup restore vs corrective import vs bulk delete.

Not covered here:

- The provenance fields that enable the "Imported with" filter — see [[import-upsert-and-provenance]].
- The validation outcomes that lead to error rows in history — see [[import-validation-and-errors]].
- Cancelled imports' partial-row behaviour — see [[import-concurrency-lock]].

## Contrasts

- **Audit log vs queue view** — [[settings-queue-view]] is the LIVE in-flight tracker (Stage 4 of [[import-pipeline-stages]]). [[settings-import-history]] is the POST-completion audit. Different screens, different timing.
- **Aggregate counts vs per-record drill-in** — the list view shows aggregates (Created / Updated / Errors / Total). Drilling in shows per-record actions with reasons.
- **Indefinite retention vs typical event logs** — most event logs in CloudCart auto-purge. Import history does NOT. Years of imports accumulate.
- **"Imported with" filter vs backup restore** — the filter is fast, surgical, but only finds records the importer tagged with provenance. Backup restore is broad-strokes but loses any unrelated changes since the backup. Corrective import is the third option — runs another upsert with the right values.

## Where it applies

[[settings-import-history]] is the central audit surface for the import pipeline. Every import — across every importer (customer CSV, product CSV, XML import, XML sync, JSON, blog CSV, ERP / accounting integrations) — writes rows into this shared log.

### History row contents

Per-import aggregate row shows:

- **Importer type** — Customers CSV / Products CSV / Products XML / etc.
- **Task ID** + **task name**.
- **Status** — Queued / Processing / Completed / Failed / Cancelled.
- **Aggregate counts** — Created, Updated, No-action, Errors, Total.
- **Start time** + **end time**.

Drilling into the row opens the **details view**, which shows:

- Per-record action (Create / Update / Skip / Error) with the matching identifier (email, SKU, product.id).
- A "View detailed change log" modal per record showing the before/after field values applied by the import.
- Per-record failure reason (for Error rows).

### Retention — indefinite

Past imports accumulate in [[settings-import-history]] indefinitely — there's no auto-purge after N days. A merchant running daily imports for years has years of history. Storage scales linearly; the UI handles browse-size via pagination, but the underlying records persist forever unless CloudCart support cleans them up via direct DB access.

The history view does **NOT auto-refresh** — the merchant manually reloads to see newly-completed imports.

### All-staff visibility, store-scoped

All staff see the same history — entries are store-scoped, not staff-scoped. The platform does NOT record which specific staff member ran a given import, so multi-staff stores cannot filter to "only my imports".

### Recovery paths — the three options

There is no rollback. The merchant picks among three recovery paths based on what went wrong:

**Path 1 — "Imported with" filter + bulk delete (preferred for products)**

1. Open [[settings-import-history]] → find the botched import → note the task ID.
2. Open [[products-products]] → apply the "Imported with" filter set to the task ID.
3. The list shows ALL products created or last-updated by that task.
4. Select-all → bulk-delete.

Pros: surgical, no impact on unrelated data. Cons: only available on [[products-products]] today (no equivalent on Customers list — see [[import-upsert-and-provenance]]). Doesn't recover the prior state of records that were UPDATED (only deletes; doesn't roll back field values).

**Path 2 — Backup restore**

CloudCart backups (per [[backups-and-restore]]) allow store-level rollback to a previous state. The merchant picks a backup from before the import and restores it.

Pros: full rollback of every field value to the pre-import state. Cons: loses ANY unrelated changes made since the backup (other admin edits, customer registrations, new orders, etc.). The merchant trades the bad import's data for everything else's data.

**Path 3 — Corrective upsert import**

Upload a new file that overwrites the bad data with the correct values (relies on the upsert behaviour — see [[import-upsert-and-provenance]]).

Pros: surgical, preserves unrelated changes, no data loss. Cons: only works if the merchant knows the correct values and can produce a clean file. Doesn't help if the import created records that shouldn't exist (those still need Path 1 deletion).

### Choosing the recovery path

- Created records that shouldn't exist → Path 1.
- Field values that need to be restored → Path 2 OR Path 3.
- Partial cancel mid-batch (see [[import-concurrency-lock]]) → typically Path 1.
- Disaster — entire database needs to come back → Path 2 always.

### Example — recovery after a botched product import

A bad XML sync misreads `<price>` as cents instead of euros and multiplies every product's price by 100 across 3,000 updated products. **Path 1 doesn't help** — the products already existed and were UPDATED, not created. **Path 2** (backup restore) recovers all prices but loses any other admin edits since the backup. **Path 3** (corrective import — fix the mapping and re-run) is usually the right call because the upsert overwrites the bad prices and preserves unrelated changes. Path 2 is the right call only if the supplier feed itself is corrupt and a clean dataset can't be produced.

## Related

- [[import-pipeline]] — hub.
- [[settings-import-history]] — the audit screen.
- [[settings-queue-view]] — live in-flight view (different from historical audit).
- [[import-upsert-and-provenance]] — the "Imported with" filter and per-record provenance.
- [[import-concurrency-lock]] — cancelled imports also land in history with their partial row counts.
- [[backups-and-restore]] — store-level backup / restore (Path 2 recovery).
- [[products-products]] — hosts the "Imported with" filter (Path 1 recovery).

## Open Questions

- Is there any plan-tier or admin-only auto-purge of very old import history (e.g., >2 years)? Currently documented as indefinite — confirm against current platform retention policy.
