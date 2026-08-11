---
type: api-resource
resource_path: /api/v2/products
http_methods: [GET, POST, PATCH, DELETE]
related_entity: product
related_features: [products-products, products-inventory, products-variants-options]
aliases: ["Products API", "JSON-API v2 products", "API продукти", "/products"]
tags: [api, json-api-v2, products]
plan_gates: []
created: 2026-05-26
updated: 2026-06-10
source_count: 4
---
# Products (JSON-API v2)

## Purpose

A `products` resource is one merchant catalog item — a row in the store's product table that carries everything a storefront listing needs: name, URL handle, status flags, SEO copy, price boundaries (derived from variants), category / vendor links, default image and default variant. Most attributes that look numeric on the storefront (per-variant price, per-variant stock, weight) live on the child [[api-variants|variants]] resource — `products` holds the catalog-level metadata + relationships.

This is the endpoint external ERPs, accounting systems, supplier feeds, and Make / Zapier scenarios call to keep the storefront catalog in sync. POSTs create new catalog items; PATCHes flip flags (active / draft / sale / new) or rewrite SEO copy; DELETEs soft-delete the row (`deleted_at` is set; subsequent GETs return 404).

## Sub-pages (in this cluster)

This resource is split into 4 aspect pages. Drill into the one that matches the question.

- [[api-products-attributes]] — the full writable / read-only attribute table, the relationship table (`variant`, `variants`, `category`, `parameter1`–`parameter3`, etc.), and the appendable sparse-field values.
- [[api-products-filtering]] — the allowed `filter[...]` parameters (incl. the `url_handle` single-record mode and the SKU / barcode / property joins), the allowed `sort` columns, and the `include` sideload paths.
- [[api-products-side-effects]] — the POST / PATCH save pipeline, the DELETE behaviour, the webhook caveat (`product.created` / `product.updated` do NOT fire for API writes), the plan-feature slot caps (402), and the common 422 shapes.
- [[api-products-examples]] — worked curl requests + JSON responses for every method and the CRUD testing checklist.

## Endpoint

- **URL base:** `<store-host>/api/v2/products/`
- **GET collection** — `GET /api/v2/products` — list with filter / sort / include / page.
- **GET single** — `GET /api/v2/products/{id}`.
- **POST** — `POST /api/v2/products` — create. Requires `name` + the `category` relationship.
- **PATCH** — `PATCH /api/v2/products/{id}` — partial update.
- **DELETE** — `DELETE /api/v2/products/{id}` — soft delete.
- **Relationship endpoints** — `GET / POST / PATCH / DELETE /api/v2/products/{id}/relationships/<rel>` for each registered relationship (`variant`, `variants`, `image`, `images`, `category`, `categories`, `parameter1`, `parameter2`, `parameter3`, `property-options`, `linked-products`).
- No custom action routes.
- No app-install requirement — available to every store on every plan with API access (see [[settings-api-keys]]).

Auth, headers, rate limits: see [[json-api-v2]].

## Attributes

`products` holds catalog-level metadata: `name` (required at POST), `url_handle`, the storefront flags (`active`, `draft`, `sale`, `new`, `digital`, `shipping`, `tracking`, `continue_selling`), `minimum` order quantity, `status_id`, product copy + SEO fields, scheduling datetimes, and a per-product `threshold`. Read-only computed fields include `price_from` / `price_to` (minor units, derived from variants), `product_type`, `views`, and the `p1`–`p3` parameter snapshots. Full table + the appendable values (`meta`, `discount`): see [[api-products-attributes]].

## Relationships

`category` is **required at POST**; the rest are optional. Up to three ordered variant parameters (`parameter1`–`parameter3`) drive the variant grid, the `variant` hasOne is system-recomputed, and `variants` / `images` / `categories` / `property-options` / `linked-products` are writable via the relationship endpoints. Full table + parameter-ordering rules: see [[api-products-attributes]].

## Filtering & sorting

Validator allow-list filters: `sku`, `barcode`, `property_id`, `property_option_id`, `url_handle` (single-record mode), plus auto-allowed raw columns (`active`, `vendor_id`, `draft`, etc.). Sortable: `id`, `name`, `date_added`, `date_modified`, `sort_order`, `views`. Includes resolve the schema relationships plus `variant.images`, `variants.images`, `property-options.property`. Full reference + worked queries: see [[api-products-filtering]].

## Side effects

Writes are not silent: the save pipeline validates the `parameter*` ordering, fills boolean defaults on POST, **wipes all child variants when a parameter changes on PATCH**, records a change-log entry (`initiator = "api"`), reprices bundles, re-evaluates product discounts, and queues a search re-index. **Critical caveat:** `product.created` / `product.updated` webhooks do NOT fire for API writes — only `product.deleted` does. Slot caps can reject a write with 402. Full catalogue: see [[api-products-side-effects]].

## Equivalent UI

- [[products-products]] — manual product create / edit / list / delete.
- [[products-inventory]] — bulk per-variant stock + price edits.
- [[products-variants-options]] — variant parameter / options management.
- [[products-categories]] — category assignment.

## Related

- [[json-api-v2]] — protocol contract (auth, rate limits, error envelope, pagination, includes).
- [[product]] — full product entity reference.
- [[api-variants]] — child variants resource (per-variant stock, SKU, price).
- [[api-images]] — image upload / delete.
- [[api-categories]] — category resource.
- [[api-vendors]] — vendor resource.
- [[api-properties]] / [[api-property-options]] — properties + per-option values.
- [[api-variant-parameters]] / [[api-variant-options]] — parameter dimensions + option values.
- [[api-store-quantity]] — per-warehouse stock for multi-store merchants.
- [[settings-hooks]] — webhook subscriptions.
- [[settings-api-keys]] — authentication setup.
- [[plan-vs-feature-pack]] — plan-level slot caps.
- [[platform-rate-limits]] — per-plan rate limits.

## Open questions

None at the hub level — see each aspect's own Open questions ([[api-products-side-effects]] flags the parameter-wipe and webhook caveats).
