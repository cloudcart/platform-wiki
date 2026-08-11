---
type: feature
nav_path: "Apps → CSV Import → Mapping fields"
route_name: apps.csv_import.create
route_path: /admin/apps/csv_import (mapping step)
aliases: ["CSV Import mapping", "CSV Import — product fields", "CSV Import — variant fields", "CSV Import — variant.parent_id", "CSV Import — image URLs", "CSV Import — multi-column mapping", "CSV Import — import types", "CSV Import — products / customers / subscribers / redirects / blog"]
tags: [apps, imports, csv, mapping, fields]
plan_gates: []
created: 2026-06-10
updated: 2026-08-03
source_count: 1
---

> Part of [[apps-csv-import]]. See the hub for the other aspects (wizard, task detail, row pipeline, final statuses, side effects, plan gates).

# CSV Import — mappable fields

## Purpose

CSV Import is a multi-type pipeline — the same upload + map + run flow handles five import types: products, customers, subscribers, redirects, blog. Each type has its own catalogue of mappable fields and its own required-field validation. This page documents what can be mapped per type, the variant-specific column model, image-URL handling, and multi-column mapping. For how the mapping is captured see [[apps-csv-import-wizard]]; for what the mapping looks like post-save see [[apps-csv-import-task-detail]].

## Where to find it

Apps → CSV Import → upload → mapping step. The field picker is filtered by the import type selected at upload time.

## What the merchant can do here

- Map any CSV column index to any platform field allowed by the import type.
- Map **multiple CSV columns into one field** (e.g. `properties.name = [3, 5, 7]`) — the values get joined when the row is processed. Surfaced on the task-detail mapping card as `3, 5, 7` with sample values joined by ` | `. See [[apps-csv-import-task-detail]].
- Leave a field **unmapped** to fall back to the import-time publish defaults (for products — see [[apps-csv-import-wizard]]).
- Map variant-only columns (for `products` type) to attach variant rows to the same parent product.

## Settings & fields

### Multi-type pipeline — 5 import types

The `/admin/api/imports/...` endpoints handle FIVE distinct import types via the same upload + map + run flow:

| Type | What it imports | Routed to |
|---|---|---|
| `products` | Product catalog (the primary use case). | CSV Import manager. |
| `customers` | Customer accounts (with optional default group ID). | See [[customers-import]]. |
| `subscribers` | Newsletter subscribers. | CSV Import manager. |
| `redirects` | URL redirects. | CSV Import manager. |
| `blog` | Blog articles. | `BlogCsvImportManager` — see [[apps-blog-csv-import]]. |

The type is captured at upload time and drives the mapping picker.

### REQUIRED fields per import type

Each type has its own required-field validation. Importing the type without these mapped fails validation at the mapping step:

| Type | REQUIRED mapped fields |
|---|---|
| `products` | `product.id` + `product.name` (variant rows additionally require `variant.parent_id`). |
| `customers` | E-mail / identifier field per the customer importer. |
| `subscribers` | E-mail field. |
| `redirects` | `redirect.old_url` + `redirect.new_url`. |
| `blog` | Per `BlogCsvImportManager` — see [[apps-blog-csv-import]]. |

### Product fields

For `products`, the mapper exposes the full product attribute set: `product.id`, `product.name`, description, vendor, category, tags, price, SKU, barcode, weight, properties (custom fields), image URLs (`product_images.src`), and more. The full per-field list is presented in the wizard's mapping picker.

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

Practical consequence for support: when a merchant reports *"my import created a new product instead of updating mine"*, that is the expected behaviour — not a mis-mapping to fix. Steer them to the Google Sheets round-trip (or the product editor / bulk actions), and clean up the duplicates the attempts created.

### Image URLs — comma-separated, downloaded into CloudCart media library

The merchant puts image URLs in `product_images.src` (one or many, **comma-separated in a single cell**). The formatter splits on `,`, trims whitespace, and downloads each image into CloudCart's own S3 / CDN media library. **Not hot-linked** — the source URL is fetched once at import time and stored in CloudCart's own storage.

Variant-specific image URLs (rows where `variant.parent_id` is set) are attached to the variant; parent-product images appear on the parent.

### Multi-column mapping — N CSV columns into one field

A field can take MULTIPLE source columns. The merchant maps `properties.name = [3, 5, 7]` — at row-processing time the values from columns 3, 5, 7 get joined. The task-detail page's column-mapping card surfaces this verbatim as `3, 5, 7` with sample values joined by ` | `. See [[apps-csv-import-task-detail]].

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
