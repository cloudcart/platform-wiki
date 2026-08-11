---
type: entity
nav_path: "Entity → Import Task → Provenance and recovery"
aliases: ["Import provenance tag", "Imported with filter", "app_import", "xml_import_id", "Import undo", "Import rollback", "Botched import cleanup", "Import recovery paths"]
tags: [entity, settings, ops, imports, provenance, recovery]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[import-task]]. See the hub for the other aspects (attributes, lifecycle, types + queues, processing model, history + webhooks).

# Import Task — Provenance and recovery

## Identity

How the platform **tags** every record an Import Task creates or updates so the merchant can later find them via the **"Imported with"** filter — and the three **recovery paths** available when an import goes wrong, because **there is NO undo / rollback button** on any importer. The provenance tag is the single most important cleanup tool the merchant has after a botched import.

## Aliases

- **Provenance tag** — the platform-wide term for the source-identifier field written on imported records.
- **`app_import`** — the field name on products imported via CSV.
- **`xml_import_id`** / **`xml_import_product_id`** / **`xml_import_name`** — the field names on products imported via XML.
- **"Imported with" filter** — the merchant-facing filter on [[products-products]] and [[customers]] that uses the provenance tag.

## Key Attributes

### The provenance tag on every imported record

Every record an Import Task creates or updates is tagged with the source Task ID:

| Entity | Provenance field(s) |
|--------|---------------------|
| **Products** (CSV imports) | `app_import = 'csv-{taskId}-<source>'` |
| **Products** (XML one-time) | `xml_import_id`, `xml_import_product_id`, `xml_import_name` |
| **Products** (XML sync recurring) | Same as XML one-time, refreshed on every scheduled run |
| **Products** (ERP integration) | App-specific fields (e.g., `frisbo_id`, `szamlazz_id`) |
| **Customers** | Import-source metadata (verify per importer — the specific field name varies) |
| **Subscribers** / **Blog articles** / **Redirects** | Similar provenance hints depending on the importer |

The tag is **written automatically** by the importer on every row processed — the merchant does NOT configure it. It persists on the record forever, even if the Task is later removed from [[settings-import-history]] (which doesn't happen automatically — see [[import-task-history-and-webhooks]]).

### The "Imported with" filter

The **"Imported with"** filter on [[products-products]] (and equivalent filters on [[customers]] / etc.) lets the merchant find ALL records from a specific Task by reading the provenance tag. This is **invaluable for bulk cleanup** if a botched Task needs to be reversed:

1. Merchant opens [[products-products]].
2. Filters by "Imported with" → picks the bad Task from a dropdown.
3. Sees every product that Task created / updated.
4. Selects all → bulk-deletes (or bulk-edits to correct).

The filter is granular to the Task ID for CSV imports (verify) — meaning the merchant can scope cleanup to exactly one bad import without affecting earlier imports from the same source. For XML sync (recurring), each scheduled run leaves its own tag, but they share the parent sync Task ID — making it harder to scope to one specific run.

### No undo / no rollback — recovery is manual

Once an Import Task commits its changes (products created, customers updated, etc.), there is **NO built-in undo**. No "rollback this import" button exists on any importer. The merchant has three recovery paths:

**Path 1 — Bulk delete via "Imported with" filter (self-service, fastest)**

- Use the "Imported with" filter on the relevant list screen ([[products-products]] / [[customers]] / etc.) to find all records from the bad Task.
- Bulk-select → bulk-delete.
- This is the **primary recovery tool** for merchants and works without support intervention.

**Path 2 — Restore from a backup (last resort, loses other changes)**

- Per [[backups-and-restore]], a full or partial restore can roll the store back to a pre-import state.
- **Caveat**: this loses any unrelated changes (orders, customer edits, settings tweaks) made since the backup. Use only when bulk-delete won't work (e.g., the import overwrote critical data on existing products and the original values can't be reconstructed from the source CSV).

**Path 3 — Run a corrective Import Task (when source data can fix it)**

- Upload a new file that overwrites the bad data with the correct values, relying on the **upsert behaviour** (see [[import-task-processing-model]]).
- The corrective Task creates its own provenance tag and history row — the original bad Task remains in [[settings-import-history]] as audit.
- Works when the merchant knows the correct values and can express them in a re-import.

### Why no undo?

The platform does NOT snapshot the **before** state of every record an Import Task touches. Reverting a Task would require knowing the pre-import value of every field, restoring them atomically, and handling records edited by other paths since the import. The platform deliberately optimises for **forward-fix** (filter + bulk-delete / corrective re-import / restore-from-backup) rather than **revert**.

### The Change log as forensic trail

Although there's no undo, every record an Import Task updates carries a **field-by-field change log** accessible from the record's detail page (e.g., [[products-change-log]] for products). The change log shows the **before** and **after** values for every field the Task touched, with timestamp and Initiator ("Import #N" or the import source app name). This lets the merchant **manually** reconstruct the pre-import value for any record, even though the platform won't auto-revert.

### Practical recovery workflow

When a merchant realises their import was wrong:

1. **Stop the import** if it's still running — Cancel from [[settings-queue-view]] (see [[import-task-lifecycle]]).
2. **Inspect the damage** — open [[products-products]] (or the affected list), filter by "Imported with" → the bad Task, count affected records.
3. **Choose recovery path**:
   - Small batch + create-only: bulk-delete via the filter.
   - Large batch + updates to existing records: corrective re-import with the correct values.
   - Catastrophic + recent backup available: restore from [[backups-and-restore]].
4. **Verify cleanup** — re-filter "Imported with" should return zero records (delete path) or the corrected values (corrective re-import path).

## Where it appears

- [[products-products]] — "Imported with" filter scopes to a specific Task ID.
- [[customers]] — equivalent filter for customers from a specific Task.
- [[products-change-log]] — per-product field-by-field audit including import-driven changes.
- [[settings-import-history]] — the Task ID the filter references is shown in the history list.
- [[backups-and-restore]] — last-resort recovery surface.

## Related

- [[import-task]] — hub.
- [[import-task-attributes]] — the provenance-tag field on the Task itself.
- [[import-task-processing-model]] — the upsert default that enables Path 3 (corrective re-import).
- [[import-task-lifecycle]] — Cancel mid-flight doesn't roll back; recovery still uses these paths.
- [[products-products]] — the "Imported with" filter UI.
- [[customers]] — the equivalent filter for customers.
- [[products-change-log]] — the forensic trail.
- [[backups-and-restore]] — last-resort recovery.
- [[import-pipeline]] — the platform-wide bulk-import pipeline includes provenance-tagging as a contract.

## Open Questions

- ⏸️ Whether the "Imported with" filter on [[products-products]] is granular to the Task ID or the source-app type — affects how usefully the merchant can scope cleanup. For CSV imports the tag includes the Task ID; for XML sync the question is whether per-run filtering is possible or only per-sync-Task filtering.
- ⏸️ The exact provenance field name on customers (verify per importer) — the customer CSV importer's tag field is not consistently documented.
