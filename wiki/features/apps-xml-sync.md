---
type: feature
nav_path: "Apps → XML Sync"
route_name: apps.xml_sync
route_path: /admin/apps/xml_sync
aliases: ["XML Sync", "Xml Sync", "Recurring supplier feed sync", "Product feed sync", "no enable disable button", "app has no active toggle"]
tags: [apps, imports, xml, products, recurring, sync, plan-gated]
plan_gates: ["xml_sync_limit"]
created: 2026-05-22
updated: 2026-08-06
source_count: 8
---
# XML Sync (recurring supplier feed sync)

## Purpose

**XML Sync** integration — automatically **re-imports** product data from a supplier's XML feed on a recurring schedule. The merchant configures the feed URL + mapping ONCE, and the platform pulls fresh data on a cadence; differences from the catalog are detected and the platform updates / creates / deactivates products accordingly.

Different from [[apps-xml-import]] (one-time fire-and-forget) — XML Sync maintains **ongoing parity** with the supplier feed. It REUSES the XML Import pipeline architecture (parse → parse_single → insert on the shared `import1` queue) but adds recurring behaviour and a dedicated active-state model that tracks which tasks are currently in their re-sync window.

Used by merchants:

- Dropshipping from suppliers who publish a daily XML feed.
- Wholesale resellers whose inventory comes from a manufacturer's catalog.
- Multi-source merchants aggregating feeds from many suppliers.

The integration is **plan-gated** on task count via the `xml_sync_limit` plan feature — see [[apps-xml-sync-settings]].

> **No on/off control — this app has no "active / inactive" state.** Once it is installed it simply works; there is no Enable / Disable button and no "Activate application" switch on its screen. So *"the app is disabled"* is never the explanation for it not working — check its own settings, credentials, or plan access instead, and use **Uninstall** if the merchant genuinely wants it off.
>
> What *can* be switched off is an individual **sync task** — the task edit screen carries its own Activate / Deactivate button in the top-right.

## Where to find it

Sidebar → Apps → install → **XML Sync**.

The app exposes the standard CloudCart app shell plus the sync wizard. Six existing sub-pages document the screens:

| Sub-page | Purpose |
|----------|---------|
| Overview ([[apps-xml-sync-overview]]) | App status, recent sync runs. |
| Settings ([[apps-xml-sync-settings]]) | Global config + plan-driven cadence. |
| Features ([[apps-xml-sync-features]]) | Capability documentation. |
| Step 2 ([[apps-xml-sync-step2]]) | Field mapping + per-field Update checkboxes. |
| Step 3 ([[apps-xml-sync-step3]]) | Field mapping wizard step 3 (final). |
| Status ([[apps-xml-sync-status]]) | Per-task sync history + log. |

## Sub-pages (in this cluster)

This feature's mechanics are split into 5 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[apps-xml-sync-job-pipeline]] — the 3-queue parse → parse_single → insert pipeline; 12h tick + 1h per-task gate; shared `import1` queue; 250-product insert chunks; `xml_hash` short-circuit; manual re-trigger; 3-strike auto-deactivate; auto-uninstall when no active tasks remain.
- [[apps-xml-sync-update-policy]] — per-field Update checkboxes (stock-only mode); `product_map` matching column (`sku` / `barcode` / `id`); multi-feed "last sync wins"; image refresh by URL-hash comparison.
- [[apps-xml-sync-discontinued]] — `disable_missings` opt-in deactivation (never delete); `imports` / `imports_active` cross-feed scoping; symmetric re-activation when a product returns.
- [[apps-xml-sync-fetch-transport]] — HTTP/HTTPS URL only (no FTP / no header auth); `parameters` query-string escape hatch; 120s timeout; SSL peer verification off; browser User-Agent; encoding detection (CP1251 supported); no gzip auto-decompression.
- [[apps-xml-sync-side-effects]] — the search index async sync via `MakeSearchable` on `searchable-import4` (the #1 "sync ran but site didn't change" cause); webhooks per product; smart-collection re-eval; cache invalidation; no failure email.

## What the merchant can do here

### Workflow

1. **Create sync task** — point at the XML URL and set up mapping (same 3-step wizard as XML Import). See [[apps-xml-sync-fetch-transport]] for what URLs / auth are accepted.
2. **Configure update policy** — pick, per field, which fields a re-sync overwrites (price always; description maybe). See [[apps-xml-sync-update-policy]].
3. **Configure discontinued handling** — Deactivate vs Keep for products missing from the feed. See [[apps-xml-sync-discontinued]].
4. **Active monitoring** — see each run's results on [[apps-xml-sync-status]].

### What the merchant CANNOT do here

- Run more sync tasks than `xml_sync_limit` (plan-feature value) — see [[apps-xml-sync-settings]].
- Set a per-task interval — cadence is plan-wide. See [[apps-xml-sync-job-pipeline]].
- Use FTP / header-based auth / gzip feeds — see [[apps-xml-sync-fetch-transport]].
- Delete missing products (only Deactivate / Keep) — see [[apps-xml-sync-discontinued]].
- Roll back a run — there is no undo.

## Settings & fields

App key: `xml_sync`. Plan-feature keys: `xml_sync_limit` (max concurrent tasks) and `xml_sync-interval` (cadence override). Max concurrent tasks comes from `xml_sync_limit` — **different** from XML Import's `xml_import_limit`, so a merchant can run, e.g., 3 XML Import tasks plus 1 XML Sync task on the same plan. A post-subscription hook runs after a plan change and re-evaluates whether existing tasks still fit under the (possibly reduced) `xml_sync_limit` after a downgrade, deactivating excess tasks gracefully. The cadence detail lives on [[apps-xml-sync-settings]]; field-by-field configuration is documented per aspect — fetch options on [[apps-xml-sync-fetch-transport]], the Update checkboxes + matching on [[apps-xml-sync-update-policy]].

## Business rules

Each aspect documents its own rules. The cluster-level invariants:

- **Recurring pipeline parallel to XML Import** — same parse → parse_single → insert structure on the shared `import1` queue, plus recurring scheduling. See [[apps-xml-sync-job-pipeline]].
- **Per-field update policy** — the merchant chooses which fields a re-sync overwrites; "stock-only mode" keeps descriptions merchant-curated. See [[apps-xml-sync-update-policy]].
- **Discontinued = deactivate (opt-in) or keep (default), never delete** — scoped across feeds via `imports` / `imports_active`. See [[apps-xml-sync-discontinued]].
- **URL-only transport, no header auth, no gzip** — see [[apps-xml-sync-fetch-transport]].
- **Async storefront lag** — the storefront catches up via the search index after each run; "sync ran but site unchanged" is queue lag, not a bug. See [[apps-xml-sync-side-effects]].
- **Standard apps permission scope** for who can install / configure.

## Related

- [[apps]] — App Store.
- [[apps-xml-sync-overview]] / [[apps-xml-sync-settings]] / [[apps-xml-sync-features]] / [[apps-xml-sync-step2]] / [[apps-xml-sync-step3]] / [[apps-xml-sync-status]] — existing screen-level sub-pages.
- [[apps-xml-import]] — sibling ONE-TIME counterpart (architecturally parallel pipeline).
- [[apps-xml-feed]] / [[apps-xml-feed-generator]] — outbound counterparts (you publish a feed, sync consumes one).
- [[apps-suppliers]] — supplier records the feeds typically belong to.
- [[apps-csv-import]] — alternative file-based import.
- [[products-products]] — products synced.
- [[plan-gates]] — plan-gating concept.
- [[background-queue-inventory]] — catalogue of background processes; the recurring sync cadence + which queue tier it runs on.

## Open questions

_None._
