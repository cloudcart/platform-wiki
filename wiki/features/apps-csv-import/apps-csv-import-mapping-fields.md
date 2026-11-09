---
type: feature
nav_path: "Apps → CSV Import → Mapping fields"
route_name: apps.csv_import.create
route_path: /admin/apps/csv_import (mapping step)
aliases: ["CSV Import mapping", "CSV Import — product fields", "CSV Import — variant fields", "CSV Import — variant.parent_id", "CSV Import — image URLs", "CSV Import — multi-column mapping", "CSV Import — import types", "CSV Import — products / customers / subscribers / redirects / blog"]
tags: [apps, imports, csv, mapping, fields]
plan_gates: []
created: 2026-06-10
updated: 2026-11-09
source_count: 2
---

> Part of [[apps-csv-import]]. See the hub for the other aspects (wizard, task detail, row pipeline, final statuses, side effects, plan gates).

# CSV Import — mappable fields

## Purpose

One upload + map + run flow handles five import types (products, customers, subscribers, redirects, blog), each with its own mappable fields and required fields. Capturing the mapping: [[apps-csv-import-wizard]]; the saved mapping: [[apps-csv-import-task-detail]].

## Where to find it

Apps → CSV Import → upload → mapping step. The field picker is filtered by the import type selected at upload time.

## What the merchant can do here

- Map any CSV column index to any platform field allowed by the import type.
- Map **multiple CSV columns into one field** (e.g. `properties.name = [3, 5, 7]`) — the values get joined when the row is processed. See [[apps-csv-import-task-detail]].
- Leave a field **unmapped** to fall back to the import-time publish defaults (for products — see [[apps-csv-import-wizard]]).
- Map variant-only columns (for `products` type) to attach variant rows to the same parent product.

## Settings & fields

### Multi-type pipeline — 5 import types

Five import types share one flow:

| Type | What it imports | Routed to |
|---|---|---|
| `products` | Product catalog (the primary use case). | CSV Import manager. |
| `customers` | Customer accounts (with optional default group ID). | See [[customers-import]]. |
| `subscribers` | Newsletter subscribers. | CSV Import manager. |
| `redirects` | URL redirects. | CSV Import manager. |
| `blog` | Blog articles. | `BlogCsvImportManager` — see [[apps-blog-csv-import]]. |

### REQUIRED fields per import type

Without these mapped, validation fails at the mapping step:

| Type | REQUIRED mapped fields |
|---|---|
| `products` | `product.id` + `product.name` (variant rows additionally require `variant.parent_id`). |
| `customers` | E-mail / identifier field per the customer importer. |
| `subscribers` | E-mail field. |
| `redirects` | `redirect.old_url` + `redirect.new_url`. |
| `blog` | Per `BlogCsvImportManager` — see [[apps-blog-csv-import]]. |

### Product fields

For `products`, the mapper offers `product.id`, `product.name`, description, vendor, category, tags, price, SKU, barcode, weight, properties, image URLs (`product_images.src`), the **Not for parcel lockers** flag (`product.meta_no_locker`, see [[shipping-provider-mech-locker-fit]]) and more.

**Category cell**: without a category delimiter the whole cell is one main category name. With one, commas separate several categories and the delimiter separates levels (`Dogs > Food, Sale` with `>`): the first is the main category, the rest additional. A row with no category is imported as a draft.

**Other categories** ("Други категории", `categories.name`): comma-separated names, or paths when the delimiter is set. Each level matches by name under its parent (a bare name: top level only); missing ones are created. Extra categories in the main Category cell replace this column.

### Variant fields — `variant.parent_id` links variants to parents

Variant columns the merchant maps (for `products` type):

| Field | Required? | What it does |
|---|---|---|
| `variant.parent_id` | **REQUIRED** for variant rows | Points at the variant's parent product. Multiple CSV rows sharing the same `parent_id` get collapsed into one product with multiple variants. |
| `variant.external_record_key` | optional | External system's key for this variant row. |
| `variant.sku` | optional | Variant SKU. |
| `variant.barcode` | optional | Variant barcode. |
| `variant.price` | optional | Per-Variant price. |
| `variant.discount_price` | optional | Per-Variant discount price. |
| `variant.quantity` | optional | Per-Variant stock — see [[inventory-variant-model]]. |
| `variant.weight` | optional | Per-Variant weight. |
| `variant.v1` / `variant.v1_value` | optional (one per option group) | First option group — e.g. `Size: M`. |
| `variant.v2` / `variant.v2_value` | optional | Second option group — e.g. `Color: Red`. |
| `variant.v3` / `variant.v3_value` | optional | Third option group — e.g. `Material: Cotton`. |

**Up to 3 option groups per variant** are supported via the `v1` / `v2` / `v3` pairs.

The REQUIRED fields are `product.name`, `product.id`, and (for variant rows) `variant.parent_id`. Both `product.id` and `product.name` **must** be mapped — they cannot be left unmapped.

### 🔴 `product.id` is the FILE's identifier — NOT the CloudCart product ID

This is the single biggest source of failed "update" attempts. The mapped `product.id` column is **the identifier used inside the file**: it groups the file's rows into products (all rows sharing a `product.id` / `variant.parent_id` become one product with several variants) and is stored as the product's **import key** (`csv-…`).

It is **NOT** a pointer to an existing product in the store:

- Putting a product's **CloudCart ID** there (the number from the admin URL, e.g. `583`) does **not** update that product — the import **creates a new product**.
- Re-running an import for products that already exist **creates duplicates**, whatever value is in `product.id`.
- So there is **no "update existing product" mode** in CSV Import — see [[apps-csv-import]] for the tools to use instead ([[apps-google-sheets]] for mass edits).

So *"my import created a new product instead of updating mine"* is expected, not a mis-mapping. Steer the merchant to the Google Sheets round-trip (or the product editor / bulk actions) and clean up the duplicates.

### Image URLs — comma-separated, downloaded into CloudCart media library

Image URLs go in `product_images.src` (one or many, **comma-separated in a single cell**); the header name is free (no fixed template). In a comma-delimited file that cell must be wrapped in double quotes, as spreadsheet exports do. Each image is copied into CloudCart's storage, **not hot-linked**; formats and failed downloads: [[apps-csv-import-row-pipeline]].

Variant-specific image URLs (rows where `variant.parent_id` is set) are attached to the variant; parent-product images appear on the parent.

### Multi-column mapping — N CSV columns into one field

A field can take several source columns (e.g. `properties.name = [3, 5, 7]`); their values are joined per row. The task-detail page shows them as `3, 5, 7` with samples joined by ` | ` ([[apps-csv-import-task-detail]]).

## Business rules

### Variant rollup intentionally collapses rows

If the CSV has 100 rows but they're for 25 products × 4 variants each, the formatter collapses to 25 product records by deduplicating on `variant.parent_id`. This is the source of the `total < CSV rows` final-status outcome — see [[apps-csv-import-final-statuses]].

### Unmapped fields fall back to publish defaults (products)

For `products`, fields the merchant doesn't map fall back to the per-task publish defaults captured in the wizard: `publish_as_active`, `publish_as_featured`, `publish_as_new`, `require_shipping`, `quantity_tracking`, `continue_sell`. See [[apps-csv-import-wizard]]. Per-row overrides require mapping a CSV column to the relevant field.

### Empty `product.id` rows are silently filtered

Rows where the `product.id` column resolves to empty are filtered out before record creation. When EVERY row is filtered (mis-mapped column), the task ends in the `total = 0` failed-state — see [[apps-csv-import-final-statuses]].

### Mapping JSON is opaque per-task

The mapping is stored as a JSON column on the `csv_tasks` row. It is NOT reusable across tasks — see [[apps-csv-import-wizard]] for the "no clone-mapping" rule.

### `app_import` tag is written per row

Every product the import creates gets tagged with `app_import = 'csv-{taskId}-<source>'`. This is the foundation of post-import cleanup via the products-list filter `import=csv-{taskId}-`. See [[apps-csv-import-side-effects]].

## Related

- [[apps-csv-import]] — hub.
- [[apps-csv-import-wizard]] — captures the mapping; sets the publish defaults fallback.
- [[apps-csv-import-task-detail]] — surfaces the saved mapping on the task page.
- [[apps-csv-import-final-statuses]] — `total = 0` and variant-rollup outcomes are driven by this mapping.
- [[apps-csv-import-side-effects]] — `app_import` tag schema for filter-and-delete cleanup.
- [[apps-blog-csv-import]] — the `blog` type's separate manager.
- [[customers-import]] — the `customers` type's separate flow.
- [[inventory-variant-model]] — what `variant.quantity` and per-Variant SKU mean post-import.
- [[products-products]] — the product editor where imported fields land.

## Open questions

_None._
