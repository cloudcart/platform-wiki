---
type: feature
nav_path: "Settings → Import history"
route_name: import-history.settings
route_path: /admin/settings/import-history
aliases: ["Import history", "Import log", "Import results", "История на импорт", "История на качване"]
tags: [settings, import, history, csv, xml, products]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 9
---

# Import history

## Purpose

A read-only audit page that lists every product / catalog import job the merchant has ever run on the store, with per-job aggregate counts (records created, updated, no-action, errored, total). Drilling into any job opens a detail tab showing the individual records touched by that import, the action applied to each (create / update / skip / error), and a *View detailed change log* modal that shows the before/after values for each record. Useful when the merchant asks *"why didn't this import work?"*, *"which products did the latest XML sync update?"*, or *"my prices are wrong — did the import overwrite them?"*.

Import jobs themselves are triggered from other screens — CSV import ([[apps-csv-import]]), XML import ([[apps-xml-import-settings]]), JSON import ([[apps-json-import]]), and ERP integrations ([[apps-szamlazz]], [[apps-frisbo]], etc.). This page is purely the audit trail.

This feature is split into five aspect pages. The Assistant should drill into the aspect that matches the question, not read every page.

## Sub-pages (in this cluster)

- [[settings-import-history-list-view]] — the **List** tab: per-job columns, default sort, per-action drill-down (clicking *Errors=12* opens Details pre-filtered to errors), and the deliberate absence of any retry / delete / cancel affordance on this page.
- [[settings-import-history-details-view]] — the **Details** tab: per-record columns, the filter chip set (Action / Search / Save Filter), what fields the search actually scans (`name`, `compare_value`, payload SKU / barcode), and the saved-filter namespace.
- [[settings-import-history-change-log-modal]] — the *View Detailed Change Log* modal: field-by-field before/after diff, where error reasons surface, and why the format is identical across CSV / XML / JSON / ERP importers.
- [[settings-import-history-action-states]] — the per-record action taxonomy (Created / Updated / No action / Error / Pending), the synthetic `processed` chip, how Pending is detected, and how the merchant uses pending-tick-down as a manual progress indicator.
- [[settings-import-history-storage-and-retention]] — where history lives (a separate logging database), indefinite retention with no auto-cleanup, no in-app delete, server-side pagination, the cross-importer `mapping` codes shown in the Name column, and how the permission gate works.

## Where to find it

Sidebar → Settings → **Import history**.

The page's breadcrumb reads *"Settings → Import history"* (with the sub-tab label appended on the Details view). The route is `/admin/settings/import-history`. The header icon is the history icon.

### Sub-screens

Distinct routes within this feature.

| Label | Route name | Route path |
|-------|------------|------------|
| Import history (root) | `import-history.settings` | `/admin/settings/import-history` |
| List | `history-list` | `/admin/settings/import-history` (default) |
| Details | `product-list-details` | `/admin/settings/import-history/items/:id` |

## What the merchant can do here

- See every past import job (List tab) and drill into the per-record outcomes (Details tab) — see [[settings-import-history-list-view]] + [[settings-import-history-details-view]].
- Inspect the field-by-field before/after diff for any individual record via the change-log modal — see [[settings-import-history-change-log-modal]].
- Filter Details by action state (Created / Updated / Skip / Error / Pending / `processed`) and search by SKU even for rows that never matched an existing product — see [[settings-import-history-details-view]].
- Use the Pending count on the List view as a live progress indicator while an import runs — see [[settings-import-history-action-states]].

What the merchant **cannot** do here:

- Re-trigger an import from this page — re-imports happen on the originator screen (CSV / XML / JSON / ERP).
- Roll back / revert a completed import — there's no undo. Botched imports must be corrected via standard product / customer / order editing or a corrective import.
- Cancel a running import — controlled from the originator app's screen and / or [[settings-queue-view]].
- Compare two imports side-by-side.
- Delete history rows from the UI — see [[settings-import-history-storage-and-retention]] for the indefinite-retention rule and the unexposed API endpoint.

## Settings & fields

The full per-tab column lists, filter chips, and column-click semantics are documented on the aspect pages:

- List tab columns + drill-down — [[settings-import-history-list-view]].
- Details tab columns + filter chips + search scope — [[settings-import-history-details-view]].
- Change-log modal — [[settings-import-history-change-log-modal]].

## Business rules

Several cross-cutting rules apply across the whole feature; each is detailed on its aspect:

- **Read-only audit.** No row edit, no delete, no retry, no cancel on either tab — see [[settings-import-history-list-view]] for the deliberate absence of these affordances.
- **Five action states**, not four — Pending is a real fifth state surfaced in the badge column while a job runs — see [[settings-import-history-action-states]].
- **Imports run asynchronously** via the background queue. The merchant kicks off the import elsewhere; this page reads the resulting log tables only after the queue processes the records. See [[settings-queue-view]] for the live-queue view.
- **Indefinite retention** — history rows accumulate forever; no auto-cleanup; CloudCart support must clean up manually — see [[settings-import-history-storage-and-retention]].
- **Cross-importer aggregation** — CSV, XML, JSON, and every ERP integration write into the same history table; the Name column distinguishes them via the `mapping` code — see [[settings-import-history-storage-and-retention]].
- **Auto-refresh** — unlike [[settings-queue-view]], this page does NOT auto-refresh; the merchant manually reloads to see newly-completed imports.
- **Permission** — standard settings permission scope; no per-importer or per-staff permission — see [[settings-import-history-storage-and-retention]].

## Related

- [[settings]] — parent hub.
- [[settings-queue-view]] — sister page for actively-running and queued jobs.
- [[apps-csv-import]] — main CSV import entry point.
- [[apps-xml-import-settings]] — XML import entry point.
- [[apps-json-import]] — JSON import entry point.
- [[apps-szamlazz]], [[apps-fgo]], [[apps-flix-facts]], [[apps-smart-bill]] — ERP integration imports.
- [[apps-frisbo]] — fulfillment integration; may produce history entries.
- [[product]] — most imports target products.
- [[category]] — category-related imports.
- [[customer]] — customer-related imports.
- [[import-task]] — entity hub for the underlying import job records.
- [[import-pipeline]] — concept page on the bulk-import pipeline platform-wide.
- [[notification-delivery]] — concept page; `file_download` admin notification fires on aggregate downloads (not from this view).
- [[background-queue-inventory]] — catalogue of all background processes; explains the import queues this page surfaces history for.

## Open questions

None.
