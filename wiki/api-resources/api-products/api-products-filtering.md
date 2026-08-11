---
type: api-resource
resource_path: /api/v2/products
http_methods: [GET, POST, PATCH, DELETE]
related_entity: product
related_features: [products-products, products-inventory, products-variants-options]
aliases: ["Products API filtering", "products sorting", "products include paths", "products query parameters", "/products filter", "API продукти филтри"]
tags: [api, json-api-v2, products]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---
# Products API — filtering, sorting & includes

> Part of [[api-products]]. See the hub for the other aspects (attributes & relationships, side effects, examples).

## Purpose

This aspect is the **read-query reference** for the `products` resource: which `filter[...]` parameters the validator accepts, the special single-record and join-backed filters, the allowed `sort` columns, and the `include` (sideload) paths. For the field meanings behind these filters, see [[api-products-attributes]]. For worked curl queries, see [[api-products-examples]].

## Endpoint

- **URL base:** `<store-host>/api/v2/products/`
- **Methods covered here:** `GET` (collection) + `GET /{id}` — query parameters apply to reads.

Base URL, auth, headers, rate limits: see [[json-api-v2]].

## Attributes

Filtering and sorting operate over the attributes documented on [[api-products-attributes]]. The filterable and sortable subsets are listed below; they do not introduce new fields.

## Relationships

The `include` paths below resolve the relationships declared on [[api-products-attributes]] (`variants`, `variant`, `images`, `image`, `category`, `categories`, `vendor`, `parameter1`–`parameter3`, `property-options`, `linked-products`, `product-to-discount`).

## Filtering & sorting

**Allowed filtering parameters** — validator allow-list: `sku`, `barcode`, `property_id`, `property_option_id`, `url_handle`. All raw columns on the `products` table are also auto-allowed by the framework (e.g., `filter[active]=yes`, `filter[vendor_id]=12`, `filter[draft]=no`).

Special cases:

- `filter[url_handle]` — must match `filled|alpha_dash`. When present, the adapter switches to **single-record mode** and returns one resource object directly (not a collection). Useful for resolving a storefront URL slug to its product without knowing the numeric id.
- `filter[sku]` / `filter[barcode]` — joined against the variants table. Matching on a child variant's SKU / barcode returns the parent product. Pair with `include=variants` to get the matched SKU back in the response.
- `filter[property_id]` / `filter[property_option_id]` — joined against the property-options pivot. Returns products carrying that property / option value.

**Allowed sort parameters** — `id`, `name`, `date_added`, `date_modified`, `sort_order`, `views`. Prefix with `-` for descending (e.g., `sort=-date_added`). Sorting on any other column returns **422**.

**Allowed include paths** — auto-allowed from schema relationships: `variants`, `variant`, `images`, `image`, `category`, `categories`, `vendor`, `parameter1`, `parameter2`, `parameter3`, `property-options`, `linked-products`, `product-to-discount`. Additional nested paths allowed by the validator: `variant.images`, `variants.images`, `property-options.property`. Requesting an include path outside this set returns 422.

**Pagination** — standard JSON-API v2 `page[size]` / `page[number]`; the response `meta.page` block carries `current-page`, `per-page`, `from`, `to`, `total`, `last-page`. Detail in [[json-api-v2]].

**Sparse-field appends** — `?append[products]=meta,discount` and `?append[variants]=discount` (when variants are sideloaded). Any other append value returns 422. See [[api-products-attributes]] for the appendable-value table.

## Side effects

Reads have no write side effects. The query-parameter validation failures above all surface as **422 Unprocessable Entity** (bad sort column, bad include path, bad append value). For write-time side effects see [[api-products-side-effects]].

## Equivalent UI

- [[products-products]] — the admin product list with its search box, status filters, and column sort mirror the `filter[...]` / `sort` parameters here.
- [[products-inventory]] — the inventory list filters by SKU / barcode, equivalent to `filter[sku]` / `filter[barcode]`.

## Related

- [[api-products]] — hub.
- [[json-api-v2]] — pagination, include semantics, 422 error envelope.
- [[api-products-attributes]] — field definitions behind the filters.
- [[api-variants]] — the variants table that `filter[sku]` / `filter[barcode]` join against.
- [[api-property-options]] — the pivot that `filter[property_id]` / `filter[property_option_id]` join against.
- [[products-products]] — admin list with equivalent filter / sort controls.

## Open questions

None.
