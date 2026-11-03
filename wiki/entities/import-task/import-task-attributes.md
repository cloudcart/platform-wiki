---
type: entity
nav_path: "Entity → Import Task → Attributes"
aliases: ["Import task attributes", "Import task fields", "Import task schema", "Import task columns", "Field mapping", "Source filename"]
tags: [entity, settings, ops, imports, attributes]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[import-task]]. See the hub for the other aspects (lifecycle, types + queues, processing model, provenance + recovery, history + webhooks).

# Import Task — Attributes

## Identity

The complete per-field schema of the Import Task record — what the merchant sets, what the worker writes, and what's visible on the list and detail surfaces of [[settings-import-history]] and [[settings-queue-view]]. The fields together capture the **type** of data being imported, the **source** (filename or feed URL), the merchant's **column-to-field mapping**, current **status**, **progress counters**, the **action breakdown** by record, **timestamps**, the **creator**, and the **queue** the Task is running on.

## Aliases

- **Import task attributes** — the full per-field schema.
- **Import task fields** — same thing in merchant-facing phrasing.
- **Field mapping** — specifically the per-column / per-field assignment the merchant configures in Step 2 of the wizard.

## Key Attributes

| Attribute | What the merchant controls | Notes |
|-----------|----------------------------|-------|
| **Type** | Set by the source app (not editable on the Task itself) | One of: `customers`, `products`, `redirects`, `subscribers`, `blog_articles`, `xml_import`, `xml_sync`, `json_import`, plus app-specific types (`szamlazz`, `fgo`, `smart_bill`, `profics`, `flix_facts`, `frisbo`, etc.). Drives which screen the Task surfaces under and which queue it runs on — see [[import-task-types-and-queues]]. |
| **Source filename** / **feed URL** | Picked by the merchant at upload / configuration | For CSV imports — the original filename. For XML sync — the feed URL + parameters. For ERP integrations — the integration's own identifier. The Task itself does NOT store the raw source file for CSV — the file is staged into a `csv_import_<timestamp>` temp table at upload time and read by the worker from there. For XML sync, the feed is re-fetched on every scheduled run; the Task stores only the configuration. |
| **Field mapping** | Set by the merchant in Step 2 of the wizard | Per-column / per-field assignment (e.g., `column_3` → `product.name`). Stored on the Task row for resume support; **NOT reusable across imports** — each new Task starts mapping from scratch. The merchant's workaround: keep the source spreadsheet with the SAME column order across imports — the mapping is then identical each time and the merchant only spends a few seconds re-picking it. XML sync Tasks are different — once configured, they reuse the mapping for every scheduled run. |
| **Status** | n/a (driven by the worker) | One of `pending`, `processing`, `completed`, `failed`, `cancelled`. The single-import lock checks "is any Task in `processing` for this Site?" — see [[import-task-lifecycle]] for the full state machine. |
| **Total rows** | n/a (computed at parse time) | The number of records in the source file / feed. Visible after Step 1 (upload + parse). |
| **Processed rows** | n/a (incremented per chunk) | Updated by the worker after each 500-row chunk; drives the progress indicator in [[settings-queue-view]]. See [[import-task-processing-model]] for the chunking mechanics. |
| **Action counts** (Created / Updated / No-action / Errors) | n/a (computed during processing) | The per-record buckets shown in [[settings-import-history]]'s list view. The `Total` column is the sum of the four. Drives the merchant's "did the import do what I expected?" check. |
| **Started at** / **Finished at** | n/a (auto-set on queue pickup / completion) | Used by the merchant to see when an import ran and how long it took. The list-view `Date` column shows the creation time (when the merchant kicked it off), not the finish time. |
| **Created by** (`user_id`) | n/a (set to the admin who launched the import) | Stored on the Task but **NOT surfaced as a list-view filter** — every staff member sees every Task. See [[import-task-history-and-webhooks]] for the shared-history rule. |
| **Worker / queue** | n/a (set by dispatcher) | `import1` (products / XML), `import2` (customer CSV), app-specific queue otherwise. Visible in [[settings-queue-view]]. See [[import-task-types-and-queues]] for the full queue assignment table. |
| **Wizard step / mapping persistence** | Yes (resume support) | If the merchant closes the wizard mid-mapping, the Task is in `pending` state with the partial mapping saved — they can reopen and continue. Closing the browser doesn't lose the configured mapping. |
| **Provenance tag (on imported records)** | n/a (auto-written on every created / updated record) | `app_import = 'csv-{taskId}-<source>'` for CSV products, `xml_import_id` / `xml_import_product_id` / `xml_import_name` for XML, app-specific fields for other integrations. Drives the "Imported with" filter — see [[import-task-provenance-and-recovery]]. |

### Field mapping in detail

The Step 2 wizard asks the merchant to map each source column to a CloudCart field:

- For **CSV imports**, the merchant sees a row of dropdowns — one per detected column. Each dropdown lists the available target fields (`product.name`, `product.price`, `variant.sku`, etc.) and `(ignore)` for columns to skip.
- For **XML imports**, the mapping is path-based — XPath expressions or feed-attribute names mapped to CloudCart fields. More complex; usually configured once and forgotten.
- For **ERP integrations** (Szamlazz, FGO, etc.), the mapping is built-in — the merchant doesn't configure it; the app's developer has hard-coded the mapping for that specific ERP's payload shape.

The mapping is **NOT a reusable preset** — there is no "save mapping as template" affordance. Every new Task starts fresh. (verify) Some apps may persist last-used mapping per-store; this isn't a platform-wide guarantee.

### Status values in detail

The five status values cover the full lifecycle:

- **`pending`** — Task row exists; either the merchant is still in the wizard, OR the Task is queued and waiting for a worker.
- **`processing`** — a worker picked up the Task; rows are being iterated.
- **`completed`** — all rows processed (successfully or with per-row errors counted in the action breakdown).
- **`failed`** — a critical error aborted the entire batch.
- **`cancelled`** — the merchant cancelled the in-flight Task from [[settings-queue-view]].

See [[import-task-lifecycle]] for the full state-transition diagram and lock behaviour.

## Where it appears

- [[settings-queue-view]] — surfaces `processing` Tasks with live progress (`Processed rows / Total rows` + status badge).
- [[settings-import-history]] — surfaces every Task ever run on this Site; columns include Date, Type, Source filename, Created / Updated / No-action / Errors / Total, Status.
- [[customers-import]] / [[apps-csv-import]] / [[apps-xml-import]] / [[apps-xml-sync]] / [[apps-json-import]] / [[apps-blog-csv-import]] — source apps where the merchant sets Type, Source filename, and Field mapping at Task creation.

## Related

- [[import-task]] — hub.
- [[import-task-lifecycle]] — the status state machine in detail.
- [[import-task-types-and-queues]] — the Type → queue mapping.
- [[import-task-processing-model]] — how Processed-rows counter increments.
- [[import-task-provenance-and-recovery]] — the provenance-tag column on every imported record.
- [[settings-import-history]] — where the attributes are surfaced as columns.
- [[settings-queue-view]] — where live progress reads `processed_rows` / `total_rows`.

## Open Questions

- ⏸️ Whether some apps persist last-used field mapping per-store as a convenience — this isn't a platform-wide guarantee, only some integrations may do it.
