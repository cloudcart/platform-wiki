---
type: feature
nav_path: "Apps → XML Import"
route_name: apps.xml_import
route_path: /admin/apps/xml_import
aliases: ["XML Import", "Xml Import", "Product feed import", "Supplier feed import (one-time)", "no enable disable button", "app has no active toggle"]
tags: [apps, imports, xml, products, plan-gated]
plan_gates: ["xml_import", "xml_import_limit", "xml_import_total_products"]
created: 2026-05-22
updated: 2026-08-06
source_count: 9
---
# XML Import (one-time supplier feed import)

## Purpose

**XML Import** integration — imports product data from a supplier's XML feed into the merchant's catalog. ONE-TIME operation in spirit: the merchant points the integration at a URL, maps the XML fields to CloudCart product fields, and the platform creates / updates products. After import the connection can be left in place (re-parse every 12h) or torn down.

Used by merchants:

- Migrating from a competitor platform (export from old store → import to CloudCart).
- Bootstrapping a new store with supplier-provided catalog.
- Adding a new product line from a one-time XML feed.

Different from [[apps-xml-sync]] (recurring sync with stronger refresh guarantees) — XML Import is fire-and-forget catalog bootstrap with a long-cadence re-parse on the side.

The integration is **plan-gated** with task-count caps + per-plan priority — see [[apps-xml-import-plan-gates]].

> **No on/off control — this app has no "active / inactive" state.** Once it is installed it simply works; there is no Enable / Disable button and no "Activate application" switch on its screen. So *"the app is disabled"* is never the explanation for it not working — check its own settings, credentials, or plan access instead, and use **Uninstall** if the merchant genuinely wants it off.
>
> What *can* be switched off is an individual **import task** — the task edit screen carries its own Activate / Deactivate button in the top-right.

## Where to find it

Sidebar → Apps → install → **XML Import**.

The app exposes the standard CloudCart app shell plus the import wizard. Six existing sub-pages document the screens:

| Sub-page | Purpose |
|----------|---------|
| Overview ([[apps-xml-import-overview]]) | App status, recent tasks. |
| Settings ([[apps-xml-import-settings]]) | Global config. |
| Features ([[apps-xml-import-features]]) | Capability documentation. |
| Step 2 ([[apps-xml-import-step2]]) | Field mapping wizard step 2. |
| Step 3 ([[apps-xml-import-step3]]) | Field mapping wizard step 3 (final). |
| Status ([[apps-xml-import-status]]) | Per-task progress / log. |

## Sub-pages (in this cluster)

This feature is split into 6 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[apps-xml-import-wizard]] — the 3-step task-creation flow (URL + toggles → tag mapping → finalisation); update-checkbox model; per-task mapping persistence; `track_inventory`, `continue_selling`, `disable_missings`, `category_id` toggles.
- [[apps-xml-import-job-pipeline]] — Parse → ParseSingle → Insert background pipeline; 12h queue tick + 1h per-task gate; `import1` dedicated queue; 50-product insert chunks; manual re-trigger via Status page.
- [[apps-xml-import-fetch-transport]] — URL-only source; Guzzle 120s timeout; SSL peer verification off; fake-browser User-Agent; encoding detection from `<?xml... ?>` preamble; the platform code pre-check; `xml_hash` short-circuit; 3-strike auto-deactivate.
- [[apps-xml-import-mapping-fields]] — what fields can be mapped (name, price, SKU, description, images, categories, variants, tags, custom data); 3 variant structural patterns (multilevel / singlelevel / template); category auto-creation; per-field Update checkbox; HTML sanitisation; base64-image rejection.
- [[apps-xml-import-plan-gates]] — three gates: `xml_import` (install gate), `xml_import_limit` (max concurrent tasks → HTTP 402), `xml_import_total_products` (cumulative product cap); feature-pack extension semantics.
- [[apps-xml-import-side-effects]] — the search index async sync via `MakeSearchable` (#1 source of "I imported and don't see it" tickets); webhooks; smart-collection re-evaluation; cache invalidation; no rollback / undo.

## What the merchant can do here

- Create import tasks pointing at a supplier XML URL — see [[apps-xml-import-wizard]] for the 3-step flow.
- Toggle each task active / inactive; monitor per-task progress in real time.
- Re-trigger the parse manually (toggle Active or save Step 3 again) — see [[apps-xml-import-job-pipeline]].
- Cancel a running task mid-flight (partial imports retain whatever was written before cancel).
- Edit the URL, mapping, or category — automatically clears the feed hash and forces re-parse.

What the merchant **cannot** do here:

- Run more tasks than the plan's `xml_import_limit` allows (HTTP 402 on create / activate). See [[apps-xml-import-plan-gates]].
- Exceed the cumulative `xml_import_total_products` cap across the lifetime of all tasks combined.
- Roll back / undo an import — there is no built-in undo. See [[apps-xml-import-side-effects]].
- Upload a file directly — only HTTP/HTTPS URLs are accepted. For file-based imports use [[apps-csv-import]] instead. See [[apps-xml-import-fetch-transport]].

## Settings & fields

App key: `xml_import`. Plan-feature keys: `xml_import`, `xml_import_limit`, `xml_import_total_products`. The integration honours plan-driven **priority** (higher plans run first) and plan-driven **cadence** (shorter intervals on higher plans). Field-by-field configuration is documented per aspect — the wizard fields on [[apps-xml-import-wizard]], the fetch transport options (URL, timeouts, encoding) on [[apps-xml-import-fetch-transport]], and the mapping fields on [[apps-xml-import-mapping-fields]].

## Business rules

Each aspect documents its own rules. The cluster-level invariants:

- **Wizard-driven mapping** — XML structures vary widely; the merchant maps tags to CloudCart fields once, and the same mapping is reused on every re-parse. See [[apps-xml-import-wizard]].
- **Per-task progress tracking** — useful for long-running imports (hours for 100k+ products). See [[apps-xml-import-job-pipeline]].
- **Plan-tier caps** — task count, priority, cadence all driven by plan. See [[apps-xml-import-plan-gates]].
- **No rollback / undo** — destructive operations cannot be reversed; merchants should test on a small mapping first. See [[apps-xml-import-side-effects]].
- **Standard apps permission scope** for who can install / configure.

## Related

- [[apps]] — App Store.
- [[apps-xml-import-overview]] / [[apps-xml-import-settings]] / [[apps-xml-import-features]] / [[apps-xml-import-step2]] / [[apps-xml-import-step3]] / [[apps-xml-import-status]] — existing screen-level sub-pages.
- [[apps-xml-sync]] — sibling RECURRING sync (different cadence model).
- [[apps-csv-import]] — alternative file-based import.
- [[products-products]] — products created / updated.
- [[plan-gates]] — plan-gating concept.
- [[plan-features]] — per-feature upsell screen.
- [[plan-vs-feature-pack]] — feature-pack extension mechanism.
- [[background-queue-inventory]] — catalogue of all background processes; covers the XML-import parse → insert pipeline timing and where to track in-flight tasks.
- [[storefront-architecture]] — the search index read-side (why the storefront can lag after the import finishes).

## Open questions

_None._
