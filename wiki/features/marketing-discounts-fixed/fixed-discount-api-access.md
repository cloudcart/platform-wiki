---
type: feature
nav_path: "Marketing → Discounts → Products → API access"
route_name: discounts-products
route_path: /admin/marketing/discounts/products/:id
aliases: ["Fixed discount API", "Fixed discount JSON-API v2", "Fixed discount GraphQL", "product-to-discount endpoint"]
tags: [marketing, discounts, fixed, api, json-api-v2, graphql]
plan_gates: ["discount_fixed", "total_discounts"]
created: 2026-06-10
updated: 2026-11-04
source_count: 3
---

> Part of [[marketing-discounts-fixed]]. See the hub for the other aspects (product modal, validation rules, row writes, plan gates, storefront display).

# Fixed discount — programmatic access (API)

## Purpose

This aspect documents how an **external integration** can manage Fixed discounts: the JSON-API v2 dual-resource model (parent `discounts` + per-variant `product-to-discount`), the Admin GraphQL API, the admin-panel discount-products REST endpoints, and what each surface checks and does on a write.

For UI-side behaviour, see [[fixed-discount-product-modal]]. For what gets persisted, see [[fixed-discount-row-writes]]. For what's rejected, see [[fixed-discount-validation-rules]].

## Where to find it

There is no admin-panel UI for the API access itself. The merchant configures their API credentials at [[settings-api-keys]] (Site ID + API key for JSON-API v2) and uses them against the JSON-API v2 base path; the Admin GraphQL API takes a personal access token from [[settings-pat-tokens]]. The admin-panel REST endpoints listed below are session-authenticated and called automatically by the modern Vue modal documented in [[fixed-discount-product-modal]].

## What the merchant can do here

- Drive Fixed-discount creation, updates, status toggles, and per-variant price assignment from an external integration (ERP, CSV-import tool, custom dashboard).
- Use the JSON-API v2 dual-resource pattern (parent `discounts` + per-variant `product-to-discount`) for a clean REST flow.
- Use GraphQL for batched create / update mutations.
- Listen for `discount.created` / `discount.updated` webhooks ([[settings-hooks]]) for changes to the discount record itself; changes to its products send none, and there is no audit log.

## Settings & fields

This aspect introduces no merchant-facing settings. The authentication credentials live at [[settings-api-keys]]; the per-resource attribute tables live at [[api-discounts]] and [[api-product-to-discount]].

## Business rules

### Admin-panel REST endpoints (the modern Vue modal's surface)

The modern Products page uses the discount-products API (not a dedicated `admin.discounts.fixed.*` route group):

| Action | Endpoint | Method |
|--------|----------|--------|
| List products on discount | `/admin/api/core/discounts/products/{id}` | GET |
| Add / edit per-product price | `/admin/api/core/discounts/products/{id}` | POST |
| Toggle status | `/admin/api/core/discounts/products/{id}/status` | POST (`{product_ids[], status}`) |
| Remove product(s) | `/admin/api/core/discounts/products/{id}?ids[product_ids][]=…` | DELETE |

These are admin-session-authenticated and called by the [[fixed-discount-product-modal]] from inside the admin panel.

### JSON-API v2 — REST endpoints (two resources)

Fixed discounts use TWO JSON-API v2 resources together:

- **Parent record** at `<store>/api/v2/discounts` — see [[api-discounts]]. Carries the discount-level metadata (name, color, customer groups, dates, etc.).
- **Per-variant attachment** at `<store>/api/v2/product-to-discount` — see [[api-product-to-discount]]. One row per variant carrying the replacement `price`, the customer-group association, and the denormalized `save` column. Read-only via this endpoint for some attributes (`discount_type`, `save`, `date_start`, `date_end` are computed / inherited from the parent — see [[fixed-discount-row-writes]] for the inheritance rule).

Authentication uses the standard Site ID + API key headers per [[settings-api-keys]]. The validator allows `type ∈ {flat, percent, shipping, fixed, code-pro}` on the parent endpoint.

#### Two-resource pattern in practice

The typical integration sequence is:

1. `POST /api/v2/discounts` with `type=fixed`, name, dates, customer groups → creates the parent record. Returns the new `discount_id`.
2. For each variant the integration wants to discount: `POST /api/v2/product-to-discount` with `discount_id`, `product_id`, `variant_id`, `price` → creates the per-variant attachment row.
3. (Optional) `PATCH /api/v2/discounts/{id}` sets `active` to `yes` or `no`; it takes effect immediately.

One POST against `product-to-discount` keeps one row: when the parent has several customer groups, the row carries the last group, not one row per group. The per-group rows in [[fixed-discount-row-writes]] come from the admin modal.

### GraphQL — Admin GraphQL API

Resource: `Discount`. The relevant mutations are:

- `createDiscount` — create a new Fixed (or other-type) discount.
- `updateDiscount` — update the parent record.
- `discountsBulkDelete` — bulk-delete discounts.
- `changeDiscountsStatus` — flip the active flag; it takes effect immediately.
- `addFixedDiscountProducts` / `updateFixedDiscountProduct` / `changeFixedProductsStatus` / `deleteFixedDiscountProducts` — manage the per-variant prices. `updateFixedDiscountProduct` replaces the product's rows on this discount only.

GraphQL takes a personal access token created at [[settings-pat-tokens]], not the JSON-API v2 Site ID + key headers.

### What each path checks and does

The paths have separate validation and side effects:

| Path | Price check | What a product write does |
|---|---|---|
| Admin modal | From 0.01 up to and including the catalog price; a higher one fails the whole save. | An edit removes the product's rows from every discount, then writes this one. One row per customer group. Product-updated and search-engine-sync events. |
| JSON-API v2 `product-to-discount` | `price` must be an integer; it is not compared with the catalog price. | Replaces that variant's rows on this discount only and keeps one row. Search-engine-sync event. |
| Admin GraphQL API | Not compared with the catalog price. | `updateFixedDiscountProduct` replaces the product's rows on this discount only. One row per customer group. Product-updated and search-engine-sync events. |

On every path:

- The denormalized `save` column is computed at write time (`variant.price − price`).
- Auto-deactivate on subsequent catalog-price drops fires from the product save — see [[fixed-discount-row-writes]].
- `discount.created` / `discount.updated` webhooks fire when the discount record itself is saved; changes to its products send none (see [[settings-hooks]]).

Creating the parent discount through an API is checked against the `discount_fixed` quota; JSON-API v2 returns **HTTP 402 Payment Required**. See [[fixed-discount-plan-gates]].

### No audit-log row for discount writes

There is **no audit-log row** captured for Fixed-discount create / update / delete operations, regardless of source (admin panel / JSON-API v2 / GraphQL).

If an integration needs to track when discounts changed, the `discount.created` / `discount.updated` webhooks ([[settings-hooks]]) signal changes to the discount record; changes to its products emit nothing.

### No catalog-price check on the API

`POST /api/v2/product-to-discount` accepts any integer `price`: it is not compared with the catalog price. Integrators should validate per-variant prices before submitting. A `price` equal to the catalog price writes a `save = 0` row, as in the admin — see [[fixed-discount-validation-rules]].

### Mode expression via API

The two pricing modes (single-price-for-all-variants vs different-price-per-variant) are expressed by either:

- **Common price** (`single`) — one shared row pushed N times (one per variant), all carrying the same `price`.
- **Multiple price** (`multiple`) — distinct rows with per-variant `price` values.

The API has no `price_type` flag — the storage shape is always per-variant.

### Endpoint summary table (all three surfaces)

| Operation | Admin panel REST | JSON-API v2 | GraphQL |
|---|---|---|---|
| Create parent Fixed discount | (via create form, not in the products page's API) | POST `/api/v2/discounts` | `createDiscount` |
| Add per-variant attachment | POST `/admin/api/core/discounts/products/{id}` | POST `/api/v2/product-to-discount` | `addFixedDiscountProducts` |
| Toggle parent active | (parent list page) | PATCH `/api/v2/discounts/{id}` | `changeDiscountsStatus` |
| Toggle per-product active | POST `/admin/api/core/discounts/products/{id}/status` | (PATCH per-variant `product-to-discount`) | `changeFixedProductsStatus` |
| Remove product(s) | DELETE `/admin/api/core/discounts/products/{id}?ids[product_ids][]=…` | DELETE per-variant `product-to-discount` rows | `deleteFixedDiscountProducts` |

## Related

- [[marketing-discounts-fixed]] — hub.
- [[api-discounts]] — JSON-API v2 parent resource.
- [[api-product-to-discount]] — JSON-API v2 per-variant attachment resource.
- [[fixed-discount-row-writes]] — what these endpoints persist + the customer-group fan-out + the auto-deactivation pipeline.
- [[fixed-discount-validation-rules]] — the admin price rules and the `save = 0` edge case.
- [[fixed-discount-plan-gates]] — `discount_fixed` quota checked on API create.
- [[fixed-discount-product-modal]] — the admin UI that calls the same admin-panel REST endpoints.
- [[settings-api-keys]] — Site ID + API key authentication for JSON-API v2.
- [[settings-hooks]] — `discount.created` / `discount.updated` webhook destinations.
- [[json-api-v2]] — JSON-API v2 concept hub.

## Open questions

- Whether `PATCH /api/v2/product-to-discount/{id}` can flip an individual variant's `active` flag, or whether per-product toggling is only via the admin-panel REST endpoint (verify).
