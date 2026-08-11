---
type: feature
nav_path: "Products → Variants → Programmatic access (JSON-API v2)"
route_name: variants-index.new
route_path: /admin/products/variants
aliases: ["Variants API", "Variant parameters API", "Variant options API", "JSON-API v2 variants", "API за варианти"]
tags: [products, variants, api, json-api-v2]
plan_gates: ["multi_variants", "variants.listing"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Variants — programmatic access (JSON-API v2)

> Part of [[products-variants-options]]. See the hub for the other aspects (list table, wizard, types, values, listing toggle, data model).

## Purpose

The same data the **Products → Variants** screen manages can be read, created, updated, or deleted via JSON-API v2. This page summarises the merchant-relevant integration behaviour — the API endpoints, what side effects fire, what validations still apply, and which webhooks are (and are not) sent.

The detailed JSON-API v2 contract per resource lives on the API resource pages — see Related.

## Where to find it

API-only — no UI surface. External integrations call:

- `/api/v2/variant-parameters` — store-wide parameter definitions (Color, Size, Material). See [[api-variant-parameters]].
- `/api/v2/variant-options` — option values under each parameter (Red, Blue, Green; S, M, L, XL). See [[api-variant-options]].
- `/api/v2/variants` — per-product variant matrix (SKU, barcode, price, quantity per combination). See [[api-variants]].

JSON-API v2 authentication, rate limits, pagination, and side-effects principle: see [[json-api-v2]].

## What the merchant can do here

- Read parameters, options, and per-product variants programmatically (typical for ERP sync, marketplace bridges, AI-powered cataloguing).
- Create / rename / delete parameters and options via PATCH / POST / DELETE.
- Bulk-update the per-product variant matrix (price, quantity, barcode, SKU per row).
- Wire imports / ERP syncs that touch variants — subject to the same validation + side effects as the admin screen.

## Settings & fields

### Endpoints summary

| Resource | Route | Per-page page |
|---|---|---|
| Variant parameters | `/api/v2/variant-parameters` | [[api-variant-parameters]] |
| Variant options | `/api/v2/variant-options` | [[api-variant-options]] |
| Variants (per product) | `/api/v2/variants` | [[api-variants]] |

### Validation that still applies on the API path

All the data-model rules from [[products-variants-data-model]] apply equally:

- 3-parameter-per-product hard cap.
- 500-variants-per-product hard cap.
- Per-product cross-parameter limits (at most 1 `numeric_alpha`, at most 2 `2d`, combined check).
- Parameter type locked once products use it.
- Name max 150 chars + unique store-wide.
- Value validation per type — `numeric_alpha` requires `<digits><letters>`; `color` requires `#[a-f0-9]{3,6}`.
- The 24-hour throttle on the "Show as separate product in listing" + "Include variant name in product title" toggles applies on both the admin form AND the API endpoint.

Invalid payloads return 422.

## Business rules

### Same side effects as the admin screen

Creating or renaming a parameter via JSON-API v2 fires the **same storefront search re-index and storefront cache invalidation** as the admin screen. There is no "API-only fast path" that bypasses these effects.

### Plan gates apply

- `multi_variants` — when locked, calls to variant endpoints are rejected. Listed in the resource page's gate section.
- `variants.listing` — the per-parameter listing toggle is rejected if the feature is not active, regardless of caller.

### No merchant webhook for parameter / value CRUD on either path

Parameter and option changes don't fire `product.created` / `product.updated` webhooks — neither from the admin form nor from the API. Subscribed receivers won't be notified until a product using the parameter is itself saved.

JSON-API v2 saves to **variants themselves** do touch their parent product (so the product's `date_modified` ticks and search re-index runs), but the merchant-visible product webhooks still only fire on admin-panel product saves and on product-level API writes that touch the parent product.

### Audit-log / Change-log

Variant `diff` tracking applies regardless of caller — saves through the API produce the same per-variant `diff` history seen on the product's [[products-change-log|Change log]].

### Type still locked after products use the parameter

The API enforces the same "type locked once in use" rule the Edit modal does. Trying to PATCH a parameter's type after products reference it returns 422.

### Side effects on save

- **Search re-index** — adding / activating a variant parameter triggers a storefront search engine resync.
- **Storefront cache invalidation** — variant pickers, product listings, and category-page caches are flushed.
- **No merchant webhook for parameter / value CRUD.**

## Related

- [[products-variants-options]] — hub.
- [[api-variant-parameters]] — parameter definitions resource.
- [[api-variant-options]] — option values resource.
- [[api-variants]] — per-product variant matrix resource.
- [[json-api-v2]] — auth, rate-limit, and side-effects principle.
- [[settings-hooks]] — webhook subscription surface (no parameter/value CRUD events).
- [[products-variants-data-model]] — the caps + validation the API enforces.
- [[products-variants-listing-toggle]] — the 24-hour throttle the API also applies.
- [[apps-csv-import]] / [[apps-xml-sync]] — bulk imports that hit the same validation.

## Open questions

None.
