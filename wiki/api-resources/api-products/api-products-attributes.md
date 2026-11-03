---
type: api-resource
resource_path: /api/v2/products
http_methods: [GET, POST, PATCH, DELETE]
related_entity: product
related_features: [products-products, products-inventory, products-variants-options]
aliases: ["Products API attributes", "products attribute reference", "products relationships", "/products attributes", "API продукти атрибути"]
tags: [api, json-api-v2, products]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---
# Products API — attributes & relationships

> Part of [[api-products]]. See the hub for the other aspects (filtering & sorting, side effects, examples).

## Purpose

This aspect is the **field reference** for the `products` resource: every writable / read-only attribute, the appendable sparse-field values, and the relationship table. Numeric-looking storefront values (per-variant price, stock, weight) live on the child [[api-variants|variants]] resource. For write behaviour (parameter validation, variant wipe, webhooks), see [[api-products-side-effects]]; for payloads, see [[api-products-examples]].

## Endpoint

- **URL base:** `<store-host>/api/v2/products/` — `GET` (collection), `GET /{id}`, `POST`, `PATCH /{id}`, `DELETE /{id}`. Auth / headers: see [[json-api-v2]].

## Attributes

| Attribute | Type | Writable POST | Writable PATCH | Required | Notes |
|---|---|---|---|---|---|
| `name` | string | yes | yes | **POST: required**, PATCH: optional | min 2 chars. Merchant-facing name. |
| `url_handle` | string | yes | yes | no | `alpha_dash`, max 191, unique across `products`. Auto-saved to redirect history on change. |
| `active` | enum `yes`/`no` | yes | yes | no | Storefront visibility. |
| `digital` | enum `yes`/`no` | yes | yes | no | POST default `no`. |
| `sale` | enum `yes`/`no` | yes | yes | no | POST default `no`. |
| `new` | enum `yes`/`no` | yes | yes | no | POST default `no`. |
| `tracking` | enum `yes`/`no` | yes | yes | no | Inventory tracking on / off. POST default `no`. See [[inventory-variant-model]]. |
| `shipping` | enum `yes`/`no` | yes | yes | no | Whether the product needs physical shipping. POST default `no`. |
| `draft` | enum `yes`/`no` | yes | yes | no | POST default `no`. |
| `continue_selling` | enum `yes`/`no` | yes | yes | no | Allow Add-to-Cart at stock = 0. See [[inventory-oversell]]. |
| `minimum` | numeric (decimal 20,3) | yes | yes | no | Minimum order quantity. DB default `1.000`. |
| `status_id` | integer / null | yes | yes | no | Must exist in the product-status catalog (see [[product-status]]). |
| `description`, `short_description`, `description_title` | text | yes | yes | no | Product copy. |
| `seo_title`, `seo_description` | string / text | yes | yes | no | SEO overrides. |
| `sort_order` | integer | yes | yes | no | Catalog-wide manual ordering. |
| `featured` | tinyint | yes | yes | no | Featured-products flag. |
| `featured_from`, `new_from`, `publish_date`, `active_to` | datetime | yes | yes | no | Scheduling fields. |
| `threshold` | integer | yes | yes | no | Per-product low-stock threshold (compared against the variant aggregate — see [[products-inventory]]). |
| `imported`, `app_import`, `xml_import_id`, `xml_import_product_id`, `xml_import_name` | strings | yes | yes | no | Import-source tracking — usually set by import wizards. |
| `out_of_stock_id` | integer | yes | yes | no | Alternative status applied when the product runs out of stock. |
| `per_row` | tinyint | yes | yes | no | Storefront layout hint. |
| `unit_short_name` | string | yes | yes | no | **Conditional**: only applied with the [[apps-grocery-store-overview-new\|Grocery Store]] app installed. Resolved into `unit_id` (see [[api-products-side-effects]]). |
| `p1`, `p2`, `p3`, `p1_id`, `p2_id`, `p3_id` | — | — | — | — | **Read-only.** Snapshots of the variant-parameter names + IDs — set via the `parameter1` / `parameter2` / `parameter3` relationships. |
| `category_id`, `vendor_id`, `image_id` | — | — | — | — | **Read-only.** Set via the `category` / `vendor` / `image` relationships. |
| `views` | integer | — | — | — | **Read-only.** Storefront view counter, maintained by analytics. |
| `price_from`, `price_to` | integer | — | — | — | **Read-only.** Computed from the variant set. Prices are integers in minor units (e.g., stotinki for BGN, cents for EUR). |
| `product_type` | string | — | — | — | **Read-only.** Type discriminator (e.g. `simple`, `bundle`, `digital`). |
| `unit_id` | integer / null | — | — | — | **Read-only.** Set indirectly via `unit_short_name` (Grocery Store app). |

System-managed columns NOT exposed for writing: `default_variant_id`, `price_percent`, `individual_price`, `price_type`, `is_hidden`, `date_added`, `date_modified`, `deleted_at`, `seo_generated_through_spinner`.

## Relationships

| Name | Type | Target | Writable | Notes |
|---|---|---|---|---|
| `variant` | hasOne | variants | system-managed | Default variant (lowest-priced, ID-tiebroken). Recomputed after variant saves. |
| `variants` | hasMany | variants | yes (relationship endpoint) | All child variants. See [[api-variants]]. |
| `image` | hasOne | images | yes | The default image. |
| `images` | hasMany | images | yes (relationship endpoint) | All product images. See [[api-images]]. |
| `category` | hasOne | categories | **required at POST** | Primary category — properties are scoped to it (see [[category-property]]). |
| `categories` | hasMany | categories | yes | Additional categories. |
| `vendor` | hasOne | vendors | yes | Brand / manufacturer. See [[api-vendors]]. |
| `parameter1` / `parameter2` / `parameter3` | hasOne | variant-parameters | yes | Up to 3 per product. **Order matters**: `parameter2` requires `parameter1`; `parameter3` requires both. Same parameter cannot fill two slots. See [[api-products-side-effects]]. |
| `property-options` | hasMany | property-options | yes | Per-product property values; validates `exists:properties_options,id`. See [[api-property-options]]. |
| `linked-products` | hasMany | products | yes | Related-products linkage. |
| `product-to-discount` | hasMany | product-to-discount | yes (sideload only) | Pivot to active product-level discounts. See [[api-product-to-discount]]. |

## Appendable sparse-field values

Request extra computed data via `?append[...]` — `products` accepts `meta`, `discount`; sideloaded `variants` accepts `discount`. Example: `?append[products]=meta,discount&append[variants]=discount`. Any other append value returns 422.

## Filtering & sorting

Filterable / sortable subsets of these attributes, the `url_handle` single-record mode, the SKU / barcode / property joins, and `include` paths: see [[api-products-filtering]].

## Side effects

Attribute writes run a save pipeline (parameter validation, boolean default fill, variant wipe on parameter change, change-log entry, bundle reprice, discount re-eval, search re-index). The key gotcha: `product.created` / `product.updated` do NOT fire for API writes. Full catalogue: see [[api-products-side-effects]].

## Equivalent UI

- [[products-products]] — manual create / edit; the attributes above map to editor form controls.
- [[products-inventory]] — bulk per-variant stock + price edits.
- [[products-variants-options]] — the `parameter1`–`parameter3` relationships.

## Related

- [[api-products]] — hub.
- [[json-api-v2]] — protocol contract (auth, rate limits, error envelope, pagination, includes).
- [[product]] — full product entity reference.
- [[api-variants]] — child variants resource (per-variant stock, SKU, price).
- [[api-images]] — image upload / delete.
- [[api-categories]] — category resource.
- [[api-vendors]] — vendor resource.
- [[api-properties]] / [[api-property-options]] — properties + per-option values.
- [[api-variant-parameters]] / [[api-variant-options]] — parameter dimensions + option values.
- [[product-status]] — `status_id` target catalog.
- [[inventory-variant-model]] — `tracking` / `continue_selling` / `threshold` semantics.

## Open questions

None at the attribute level — see [[api-products-side-effects]] for the parameter-wipe and webhook caveats still flagged for confirmation.
