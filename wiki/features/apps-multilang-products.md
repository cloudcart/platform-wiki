---
type: feature
nav_path: "Apps → Multilang → Products"
route_name: apps.multilang.products
route_path: /admin/apps/multilang/products
aliases: ["Multilang Products", "Per-product translation status", "Multilang product list"]
tags: [apps, administration, multilang, products, translation]
plan_gates: []
created: 2026-05-21
updated: 2026-05-27
source_count: 3
---
# Multilang → Products

## Purpose

The **Products** tab shows the **per-product translation status across all sister sites**. The merchant sees, for each product:
- Whether translations are complete / partial / missing per sister site.
- Last translation timestamp.
- Source language values vs translated values.
- Per-product action to trigger / re-run translation.

Useful for auditing which products are ready to launch on each sister site — finding gaps in translation coverage.

For the full Multilang feature set, see [[apps-multilang]].

## Where to find it

Sidebar → Apps → Multilang → **Products tab**. Route: `/admin/apps/multilang/products`.

## What the merchant can do here

### Products data table

Standard table with per-row data (per `IndexHelpers/` components):

| Column | Source |
|---|---|
| **Product name** (`ProductName`) | The master product name. |
| **Language** / coverage (`Feature`) | Per-site translation status indicators. |
| **Product copy** (`ProductCopy`) | Whether the product was copied to each sister site (without translation). |
| **Actions** (`Actions`) | Re-translate, view per-site values, manual edit. |

### Filter / search

Standard table filters:
- Filter by translation status (Complete / Partial / Missing).
- Filter by sister site.
- Search by product name.
- Filter by date range (last translation).

### Bulk actions

Multi-select products + bulk actions:
- **Bulk re-translate** — queue all selected for re-translation.
- **Bulk copy** — copy without translation (SYNC_COPY pattern).
- **Bulk delete from sister sites** — remove the translated copies (master stays).

### Per-product detail

Click a row → opens a detail view showing:
- Master language values per field.
- Sister site values per field (per language).
- Quality indicators (AI-translated / merchant-edited / missing).
- Manual edit per field per language.

### What the merchant CANNOT do here
- Edit the master product's source data — that's [[products-products]] (the regular product editor).
- Add new products from this view — products are added via the catalog editor; this view tracks their translations.
- Change a product's source language — master language is global.

## Settings & fields

### Per-row data

| Field | Notes |
|---|---|
| **product_id** | CloudCart product ID. |
| **master_name** | Product name in source language. |
| **translation_coverage** | Per-site coverage percentage. |
| **last_translated_at** | When the most recent translation completed. |
| **status_per_site** | Map of site_id → status (complete / partial / missing). |

### Status indicators

Visual badges per row showing translation state per sister site — icons or colored chips per language flag.

## Business rules

### Coverage calculation

Per-product translation coverage = (translated fields / total mandatory fields) per sister site, e.g. "100% on EN, 60% on RO" means RO is missing 40% of fields.

### Distinction between Translate and Copy

The Products table surfaces the **Translate** vs **Copy** distinction (`SYNC_TRANSLATE` vs `SYNC_COPY`) so the merchant can tell apart "translated" from "copied" rows. For what each operation does, see [[apps-multilang-main-translation-engine]].

### Re-translate impact

Triggering re-translate may OVERWRITE manual edits, and a confirm dialog warns before it does. For the full conflict-resolution rule, see [[apps-multilang-main-model]].

### Permission
Standard apps permission scope.

## Related

- [[apps-multilang]] — Multilang hub.
- [[apps-multilang-stores]] — sister sites referenced by per-site status.
- [[apps-multilang-progress]] — overall sync progress (this page is per-product detail).
- [[apps-multilang-settings]] — feature toggles (which fields get translated).
- [[products-products]] — master products being translated.
- [[apps-cloudio-overview]] — AI engine that may power auto-translation.

## How it works (verified against backend)

### Bulk operations: per-batch via individual calls + a "bulk add all" that chunks at 300

Two bulk endpoints handle copying products to sister sites:
- `POST /api/multilang/products/bulk/add` — multi-select N products from the queue and copy them all. The merchant's selected IDs are dispatched as a `multylang_add_products` queue task per sister site.
- `POST /api/multilang/products/bulk/add-all` — copy EVERY pending product. The platform chunks by 300 and dispatches a queue task per chunk per sister site.

There's no explicit cap on bulk size — the merchant can "add all" thousands of products at once, and the platform splits them into 300-item chunks for the queue. Throughput is governed by the platform's general queue config, not a Multilang-specific rate limit.

### Re-translation is WHOLE-product, not per-field

The re-translate action takes a product ID and triggers translation of ALL fields enabled in the sister's [[apps-multilang-settings]] (title, description, meta, category, alt tags, etc.). **There is no "re-translate only the description, leave the title alone" per-field action.** If the merchant manually polished the title and re-runs translate, they lose the polish — see [[apps-multilang-main-model]] for the overwrite rule.

### Cost preview happens at the wizard step, not on the Products tab

The price-and-count summary (X products, Y symbols, estimated cost in BGN) is shown at the wizard's payment step BEFORE the merchant commits. **The Products tab itself has no inline "this bulk re-translate will cost X" preview** — cost is drawn from the pre-purchased quota as jobs run (quota + accounting: [[apps-multilang-main-translation-engine]]).

### Search is by product name, not by translated content

The Products tab filters by the master product's name + status + date. **There is no full-text search across the translated content** (i.e., the merchant cannot query "find all sister-Bulgarian products that say 'безжичен' in their translated description"). The merchant searches the master catalogue, then drills into a product to see its sister-site translations.

### How to stop a product re-syncing

There is no translation-locked flag on translated entities. A sister-side manual edit is saved, but a later re-translate from the master OVERWRITES it ([[apps-multilang-main-model]]). To stop auto-updates entirely, the merchant must DELETE the product from the sync queue (the delete action removes it from the temporary sync table so it won't be re-synced).

### Single-product copy → "Temporary" staging table

Selected products aren't pushed immediately. They accumulate in a `multilang_temporary` table on the master, tagged `type = 'insert'` (written by the `add` and `bulk add` endpoints). Only on confirm (or `bulk/add-all`) does the platform read staging, chunk by 300, and dispatch the `multylang_add_products` task per sister site per chunk; the staging rows are then deleted. The merchant can preview/cancel by clearing staging before confirming.

### Bulk delete also runs through staging

The `bulk/delete` and `bulk/delete-all` actions add `type = 'delete'` rows to the same staging table, then dispatch the delete-products job per sister site. Symmetric to bulk add. Per-sister: when the sister site has the `delete` flag enabled on its settings (per [[apps-multilang-settings]]), the master's delete pushes through; otherwise the delete is skipped for that sister.

### Per-job retry and translate batching

A failed record is retried up to 3 attempts then left pending; the merchant re-triggers it from this page. Batching is per-entity (one record = one product/category regardless of symbol count), not per-symbol. Both rules live on [[apps-multilang-main-translation-engine]].

### Single-product copy endpoint is one record per call

The `/api/multilang/products/copy/{product_id}` endpoint copies ONE product (queued, but per call). The merchant uses this for ad-hoc one-off copies; the bulk endpoints handle multi-selects more efficiently.

### Slug uniqueness preserved on sister side

When a re-translation generates a fresh URL handle and it collides on the sister, the platform appends `-<product_id>` for uniqueness; merchant-edited sister slugs are NOT touched on subsequent re-translations. Full slug rules: [[apps-multilang-main-translation-engine]] (de-dup) and [[apps-multilang-main-model]] (per-site slugs).

## Open questions

