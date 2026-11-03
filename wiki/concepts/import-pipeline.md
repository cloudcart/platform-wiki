---
type: concept
nav_path: "Concept → Import pipeline"
aliases: ["Bulk import pipeline", "Import pipeline", "CSV import", "XML import", "Catalog import", "Customer import", "Bulk data load", "Spreadsheet import", "Импорт", "Качване от файл", "Масов импорт", "Импорт на каталог", "Импорт на клиенти"]
tags: [ops, imports, csv, xml, concepts]
plan_gates: []
created: 2026-05-23
updated: 2026-06-10
source_count: 1
---

# Import pipeline

## Definition

The **import pipeline** is the platform-wide pattern for loading bulk data into CloudCart from an external file or feed — CSV uploads for products, customers, blog articles, redirects, and subscribers; XML feeds from suppliers (one-time imports and recurring syncs); JSON payloads from app-specific integrations; and ERP / accounting connectors that pull data over their own protocols. Despite the variety of entry-points, every import path follows the same shape: **upload → preview → map columns → process asynchronously on a background queue → audit in [[settings-import-history]]**. The merchant kicks off the import from a specific source screen, then walks away — the heavy lifting happens behind the scenes and the merchant returns to verify the result.

The pipeline is **single-tenant locked**: only one import can be running per store at any time, across ALL importer types (customers, products, redirects, subscribers, blog articles, XML feeds). The block surfaces as HTTP 409 with *"There cannot be more than {N} imports running simultaneously."* — see [[import-concurrency-lock]].

Imports are **asynchronous**: the merchant's session does NOT block while rows are processed. The upload, mapping, and submit steps run synchronously (taking seconds), but the actual row-by-row processing happens on dedicated background queues (e.g., `import1` for XML, `import2` for customer CSV). A 10,000-row CSV typically completes in a few minutes; a 100,000-row XML feed might take 30+ minutes depending on store load. The merchant tracks progress in [[settings-queue-view]] (live queue counters) or [[settings-import-history]] (historical record + per-record drill-in).

There is **no built-in undo / rollback** for any import. Once products are created or customer records updated, the merchant has no one-click way to reverse the change — recovery is via the "Imported with" filter + bulk delete, backup restore, or a corrective upsert import. See [[import-history-and-recovery]].

## Sub-pages (in this cluster)

This concept is split into 7 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[import-pipeline-stages]] — the standard wizard shape (Upload → Map → Submit), background chunked processing, queue names (`import1`, `import2`), the three main import pathways.
- [[import-concurrency-lock]] — the single-import-at-a-time rule; HTTP 409 *"There cannot be more than {N} imports running simultaneously."*; why parallelism would corrupt state; cancel via [[settings-queue-view]].
- [[import-validation-and-errors]] — silent-skip vs counted-error vs abort per importer; failed-row tracking; how the merchant discovers skipped rows; re-import workflow.
- [[import-upsert-and-provenance]] — upsert match-by-identifier semantics (email / SKU / `product.id`); per-record provenance tags (`app_import`, `xml_import_id`); the "Imported with" filter on [[products-products]].
- [[import-plan-gates-and-2fa]] — plan-feature keys (`customer_import`, `xml_import_limit`, `xml_sync_limit`, `xml_sync-interval`); 2FA-gated customer CSV; file-format constraints (CSV/TXT, UTF-8, auto-delimiter); row-count caps.
- [[import-history-and-recovery]] — [[settings-import-history]] indefinite-retention audit log; aggregate counts + per-record drill-in; recovery paths when no undo exists ("Imported with" + bulk delete, [[backups-and-restore]], corrective upsert).
- [[import-xml-sync-recurring]] — [[apps-xml-sync]] specifics: recurring schedule (default 12 h), per-field update policies, feed-hash short-circuit, discontinued-product handling, HTTP/HTTPS-only transport constraints.

## Why it matters to the merchant

Three high-impact rules every merchant should internalise:

- **Async means results don't appear immediately.** The wizard's "Success" toast is the queue-acknowledgment, not row-level completion. [[settings-queue-view]] is the live-progress tracker. See [[import-pipeline-stages]].
- **Validation failures often skip silently.** Rows missing required fields or with invalid formats may be dropped without an inline error report. The merchant compares input row count to imported + error counts to detect skips. See [[import-validation-and-errors]].
- **There is no rollback.** Recovery is via the "Imported with" filter + bulk delete, [[backups-and-restore]], or a corrective upsert import. See [[import-history-and-recovery]].

## Scope

Covered across the 7 sub-pages: the wizard shape (Upload → Map → Submit); background processing on `import1` / `import2` / app-specific queues with row chunking; the single-import lock; validation handling per importer; upsert + provenance; plan-feature gates and 2FA on customer CSV; file-format constraints; [[settings-import-history]] retention; recovery paths; recurring XML Sync.

Not covered: per-importer UI mechanics (see the importer's own feature page — [[customers-import]], [[apps-csv-import]], [[apps-xml-import]], [[apps-xml-sync]], [[apps-json-import]], [[apps-blog-csv-import]]); per-app integration behaviour (Szamlazz, FGO, SmartBill, Profics, FlixFacts); multilang sync ([[apps-multilang]] / [[multi-language]]); bulk EXPORT; in-admin bulk actions on existing records.

## Contrasts

- **Customer CSV vs Product CSV** — Customer CSV is 2FA-gated and capped by `customer_import`; Product CSV is not 2FA-gated and has no specific plan gate. See [[import-plan-gates-and-2fa]].
- **One-time XML import vs recurring XML sync** — [[apps-xml-import]] is fire-and-forget; [[apps-xml-sync]] is recurring. See [[import-xml-sync-recurring]].
- **CSV vs XML mapping** — CSV uses spreadsheet column-to-field mapping; XML uses structure mapping against the parsed feed.
- **Synchronous wizard vs asynchronous processing** — wizard takes seconds; row processing takes minutes. See [[import-pipeline-stages]].
- **Silent skip vs counted error vs abort** — see [[import-validation-and-errors]].
- **Import pipeline vs in-admin bulk actions** — bulk actions ([[products-inventory]], [[orders]]) operate on EXISTING records, synchronously. The import pipeline targets external files / feeds and can create new records.
- **Import pipeline vs order-side flows** — this concept covers data INGESTION; [[checkout-flow]] / [[cart-vs-order-lifecycle]] cover the customer's purchase journey.

## Where it applies

The import pipeline spans many source screens, a central monitoring layer, and cleanup affordances scattered across list screens. Each sub-page documents its own application surface. The cross-cutting touch-points are:

- **Source screens** — [[customers-import]], [[apps-csv-import]], [[apps-xml-import]], [[apps-xml-sync]], [[apps-json-import]], [[apps-blog-csv-import]], plus ERP / accounting integrations.
- **Monitoring** — [[settings-queue-view]] (live in-flight) + [[settings-import-history]] (historical audit).
- **Cleanup** — "Imported with" filter on [[products-products]]; [[backups-and-restore]] as last-resort rollback.
- **Downstream effects** — every imported record fires webhooks ([[settings-hooks]] — `product.updated`, `customer.created`, etc.) and re-indexes the search index when applicable. See [[background-queue-inventory]] for queue tiers and [[inventory-tracking]] for the downstream stock-decrement / restock implications of `variant.quantity` changes.

## Related

- [[customers-import]] — customer CSV import (2FA-gated, `customer_import` plan-gated).
- [[apps-csv-import]] — product CSV / Excel import.
- [[apps-xml-import]] — one-time product XML import.
- [[apps-xml-import-wizard]] — the 3-step XML wizard: **where the supplier feed URL is entered** (Step 1) + the per-step toggles, field mapping, and category/tax/vendor options.
- [[apps-xml-sync]] — recurring product XML sync (plan-gated cadence + task count).
- [[apps-json-import]] — JSON-format import.
- [[apps-blog-csv-import]] — blog article CSV import.
- [[apps-multilang]] — multilang sync tasks (translation + copy).
- [[settings-import-history]] — historical audit of all past imports (indefinite retention).
- [[settings-queue-view]] — live in-flight queue progress.
- [[plan-gates]] — `customer_import`, `xml_import_limit`, `xml_sync_limit`, `xml_sync-interval` plan features.
- [[backups-and-restore]] — last-resort rollback path when no undo is available.
- [[product]] — Product entity; carries import provenance.
- [[variant]] — Variant entity; carries per-SKU stock / price / barcode that imports populate.
- [[customer]] — Customer entity; updated / created by customer CSV.
- [[import-task]] — entity page for the import-task record.
- [[settings-hooks]] — webhooks fire per imported / updated record.
- [[inventory-tracking]] — imports that change `variant.quantity` flow through the same decrement / restock logic as orders.
- [[variants-model]] — Parameter / Option / Variant structure; product imports map onto this.
- [[background-queue-inventory]] — catalogue of all background processes; explains which import-queue tiers exist per plan.

## Open Questions

No outstanding questions — all previously-flagged items resolved or distributed to sub-pages.
