---
type: feature
nav_path: "Marketing → Discounts → Products → API access"
route_name: discounts-products
route_path: /admin/marketing-new/discounts/products/:id
aliases: ["Fixed discount API", "Fixed discount JSON-API v2", "Fixed discount GraphQL", "product-to-discount endpoint"]
tags: [marketing, discounts, fixed, api, json-api-v2, graphql]
plan_gates: ["discount_fixed", "total_discounts"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-discounts-fixed]]. See the hub for the other aspects (product modal, validation rules, row writes, plan gates, storefront display).

# Fixed discount — programmatic access (API)

## Purpose

This aspect documents how an **external integration** can manage Fixed discounts: the JSON-API v2 dual-resource model (parent `discounts` + per-variant `product-to-discount`), the GraphQL admin-session surface, the admin-panel discount-products REST endpoints, and the side-effect pipeline that runs identically regardless of which surface invokes a write.

For UI-side behaviour, see [[fixed-discount-product-modal]]. For what gets persisted, see [[fixed-discount-row-writes]]. For what's rejected, see [[fixed-discount-validation-rules]].

## Where to find it

There is no admin-panel UI for the API access itself. The merchant configures their API credentials at [[settings-api-keys]] (Site ID + API key for JSON-API v2) and uses them against the JSON-API v2 base path or the GraphQL admin-session endpoint. The admin-panel REST endpoints listed below are session-authenticated and called automatically by the modern Vue modal documented in [[fixed-discount-product-modal]].

## What the merchant can do here

- Drive Fixed-discount creation, updates, status toggles, and per-variant price assignment from an external integration (ERP, CSV-import tool, custom dashboard).
- Use the JSON-API v2 dual-resource pattern (parent `discounts` + per-variant `product-to-discount`) for a clean REST flow.
- Use GraphQL for batched create / update mutations.
- Listen for `discount.created` / `discount.updated` webhooks ([[settings-hooks]]) — the only post-write signal, since there is no audit log.

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

- **Parent record** at `<store>/api/v2/discounts` — see [[api-discounts]]. Carries the discount-level metadata (name, color, customer groups, dates, MSRP flag, etc.).
- **Per-variant attachment** at `<store>/api/v2/product-to-discount` — see [[api-product-to-discount]]. One row per variant carrying the replacement `price`, the customer-group association, and the denormalized `save` column. Read-only via this endpoint for some attributes (`discount_type`, `save`, `date_start`, `date_end` are computed / inherited from the parent — see [[fixed-discount-row-writes]] for the inheritance rule).

Authentication uses the standard Site ID + API key headers per [[settings-api-keys]]. The validator allows `type ∈ {flat, percent, shipping, fixed, code-pro}` on the parent endpoint.

#### Two-resource pattern in practice

The typical integration sequence is:

1. `POST /api/v2/discounts` with `type=fixed`, name, dates, MSRP flag, customer groups → creates the parent record. Returns the new `discount_id`.
2. For each variant the integration wants to discount: `POST /api/v2/product-to-discount` with `discount_id`, `product_id`, `variant_id`, `price`, optionally `msrp_price` → creates the per-variant attachment row.
3. (Optional) `PATCH /api/v2/discounts/{id}` flips `status` between `active` / `inactive` — subject to the 10-minute cooldown (see [[fixed-discount-plan-gates]]).

The customer-group fan-out described in [[fixed-discount-row-writes]] applies the same way when the rows are created via JSON-API v2 — one POST against `product-to-discount` produces one row per group when the parent has multiple groups assigned.

### GraphQL — admin admin-session endpoint

Resource: `Discount`. The relevant mutations are:

- `createDiscount` — create a new Fixed (or other-type) discount.
- `updateDiscount` — update the parent record.
- `discountsBulkDelete` — bulk-delete discounts.
- `changeDiscountsStatus` — flip the active flag (subject to the 10-minute cooldown).

GraphQL uses admin-session authentication, not the JSON-API v2 Site ID + key headers.

### Identical side effects regardless of source

A create / update through JSON-API v2 or GraphQL triggers the **same pipeline** as the admin-panel save:

- Per-variant rows in `product_to_discount` are created or updated identically. See [[fixed-discount-row-writes]].
- The denormalized `save` column is computed at write time (either `variant.price − fixed_price` standard mode, or `msrp_price − fixed_price` in MSRP mode).
- Auto-deactivate on subsequent catalog-price drops fires from the same product-update hook — see [[fixed-discount-row-writes]].
- The `discount_fixed` plan-feature usage counter consumes — overflow returns **HTTP 403 Forbidden** with *"Not supported by plan"*. See [[fixed-discount-plan-gates]].
- Per-product attachment regeneration runs (Fixed discounts ARE the attachment rows — the save flow itself is the regeneration).
- The `discount.created` / `discount.updated` webhooks emit (see [[settings-hooks]]).
- The 10-minute activation cooldown applies on subsequent status-toggle attempts — see [[fixed-discount-plan-gates]].

### No audit-log row for discount writes

There is **no audit-log row** captured for Fixed-discount create / update / delete operations, regardless of source (admin panel / JSON-API v2 / GraphQL). Older wiki phrasing claimed an `api2` audit source tag — that claim was incorrect; no audit log exists for discounts.

If an integration needs to track when discounts changed, the `discount.created` / `discount.updated` webhooks ([[settings-hooks]]) are the only emitted signal.

### API-path divergence on `fixed_price = variant.price`

The modern API does NOT carry the legacy admin form's silent-skip guard on `fixed_price >= variant.price`. An API-submitted row with `fixed_price = variant.price` WILL write a `save = 0` row, occupying an attachment slot. Integrators should validate per-variant prices client-side before submitting — see [[fixed-discount-validation-rules]] for the full equality-edge-case detail.

### Mode expression via API

The two pricing modes (single-price-for-all-variants vs different-price-per-variant) are expressed by either:

- **Common price** (`single`) — one shared row pushed N times (one per variant), all carrying the same `price`.
- **Multiple price** (`multiple`) — distinct rows with per-variant `price` values.

The API has no `price_type` flag — the storage shape is always per-variant. The MSRP flag's "save against MSRP, not catalog" semantic for the `save` column applies identically when invoked via the API.

### Endpoint summary table (all three surfaces)

| Operation | Admin panel REST | JSON-API v2 | GraphQL |
|---|---|---|---|
| Create parent Fixed discount | (via create form, not in the products page's API) | POST `/api/v2/discounts` | `createDiscount` |
| Add per-variant attachment | POST `/admin/api/core/discounts/products/{id}` | POST `/api/v2/product-to-discount` | (via parent update) |
| Toggle parent active | (parent list page) | PATCH `/api/v2/discounts/{id}` | `changeDiscountsStatus` |
| Toggle per-product active | POST `/admin/api/core/discounts/products/{id}/status` | (PATCH per-variant `product-to-discount`) | n/a |
| Remove product(s) | DELETE `/admin/api/core/discounts/products/{id}?ids[product_ids][]=…` | DELETE per-variant `product-to-discount` rows | (via parent update) |

## Related

- [[marketing-discounts-fixed]] — hub.
- [[api-discounts]] — JSON-API v2 parent resource.
- [[api-product-to-discount]] — JSON-API v2 per-variant attachment resource.
- [[fixed-discount-row-writes]] — what these endpoints persist + the customer-group fan-out + the auto-deactivation pipeline.
- [[fixed-discount-validation-rules]] — the `fixed_price = variant.price` equality edge case that produces `save = 0` rows via API.
- [[fixed-discount-plan-gates]] — `discount_fixed` cap + 10-minute cooldown enforced on the API path too.
- [[fixed-discount-product-modal]] — the admin UI that calls the same admin-panel REST endpoints.
- [[settings-api-keys]] — Site ID + API key authentication for JSON-API v2.
- [[settings-hooks]] — `discount.created` / `discount.updated` webhook destinations.
- [[json-api-v2]] — JSON-API v2 concept hub.

## Open questions

- Whether `PATCH /api/v2/product-to-discount/{id}` can flip an individual variant's `active` flag, or whether per-product toggling is only via the admin-panel REST endpoint (verify).
