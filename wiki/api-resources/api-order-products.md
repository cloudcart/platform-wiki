---
type: api-resource
resource_path: /api/v2/order-products
http_methods: [GET]
related_entity: order
related_features: [orders-products, orders-ordered-products, orders-details]
aliases: ["Order products API", "Order line items API", "JSON-API v2 order-products", "/order-products"]
tags: [api, json-api-v2, orders]
plan_gates: []
created: 2026-05-26
updated: 2026-06-05
source_count: 3
---
# Order Products (JSON-API v2)

## Purpose

The `order-products` resource is the **read-only view of every line item the customer purchased** — one row per product on every order, snapshotted at checkout time. External integrations pull this resource into ERP / fulfillment / accounting systems to surface what was ordered, compute per-line revenue and tax, attribute commission, and reconcile inventory decrements against ordered quantities. It is the JSON-API counterpart of the per-order line-items list ([[orders-products]]) and the cross-order ordered-products report ([[orders-ordered-products]]).

Snapshot fields (`name`, `sku`, `barcode`, `price`, `vendor_name`, `category_name`, parameter labels) survive later catalog edits — a renamed product or deleted variant still appears here under the name and price it had when the customer ordered it. To modify line items, the merchant uses the admin-panel order-product flow ([[orders-products]] → Add / Edit / Remove product on order); the resulting per-edit delta is recorded as an [[api-order-modification]] row.

## Endpoint

| Method | Path | Status |
|---|---|---|
| `GET` | `/api/v2/order-products` | List every line item across every order on the store. Supports sort, page, include. |
| `GET` | `/api/v2/order-products/{id}` | Fetch a single line item. |
| `POST` / `PATCH` / `DELETE` | `/api/v2/order-products[/{id}]` | **GET only — returns 405 Method Not Allowed.** Mutations on a placed order's line items go through the admin-panel [[orders-products]] flow; there is no API equivalent. |

No app install or plan feature gates this resource — every store has it available. To scope the response to a single order, filter by `order_id` (auto-merged from the model's column list) or fetch the parent with `?include=products` on [[api-orders]].

## Attributes

All attributes are returned by GET only — there is no writable surface.

| Attribute | Type | Notes |
|---|---|---|
| `order_id` | integer | Parent order. |
| `product_id` | integer | Catalog product reference (may be null if the product was hard-deleted post-order — snapshot fields survive). |
| `variant_id` | integer | Catalog variant reference. |
| `name` | string | Product name **snapshotted at order-create time** — survives later catalog renames. |
| `sku` | string | Variant SKU snapshot. |
| `barcode` | string | Variant barcode snapshot. |
| `quantity` | float | Ordered quantity (float to support fractional grocery units — see the [[apps-grocery-store-overview-new\|Grocery Store]] app). |
| `weight` | integer | Per-unit weight at order time. |
| `price` | integer | Per-unit price in store currency minor units, before discounts. |
| `order_price` | integer | Final per-unit price after order-level discounts. |
| `order_discount_id` | integer | FK to the applied [[api-order-discount]] row, if any. |
| `order_fulfillment_id` | integer | FK to the [[api-order-fulfillment]] record once the order is shipped. |
| `p1` / `p2` / `p3` | string | Variant parameter name snapshots (e.g., "Color", "Size"). |
| `v1` / `v2` / `v3` | string | Variant parameter value snapshots (e.g., "Red", "Large"). |
| `vendor_id`, `vendor_name` | int, string | Vendor reference + snapshot. |
| `category_id`, `category_name` | int, string | Primary-category reference + snapshot. |
| `sale`, `new` | enum `yes` / `no` | Badge state at order time. |
| `digital` | enum `yes` / `no` | Whether the line item is digital (affects fulfillment requirements). |
| `tracked` | enum `yes` / `no` | Whether inventory tracking was on for this variant at order time. |
| `unit_id`, `unit_value`, `units` | various | Grocery-store unit-of-measure snapshots. |

**Hidden by default** (not returned to keep payloads small; aggregated breakdowns live on the parent order's [[api-order-total]] / [[api-order-tax]] rows): `new_format`, `exclude_vat`, `price_vat`, `price_with_vat`, `price_without_vat`, `discount_price`, `discount_price_vat`, `discount_price_with_vat`, `discount_price_without_vat`, `options_price`, `options_price_vat`, `options_price_with_vat`, `options_price_without_vat`, `options_discount_price`, `options_discount_price_vat`, `options_discount_price_with_vat`, `options_discount_price_without_vat`.

There are no sparse-field append values configured for this resource.

## Relationships

| Name | Cardinality | Type | Notes |
|---|---|---|---|
| `order` | belongsTo | order | Parent order. |
| `options` | hasMany | order-products-options | Selected Product Options on this line item (see [[api-order-products-options]]). |

**Allowed include paths:** `order`, `options`.

## Filtering & sorting

**Allowed filtering parameters:** none specific to the resource — only the framework's auto-merged column filters (exact-equality on any column on the underlying table, e.g., `filter[order_id]=123`, `filter[product_id]=45`). No comparison operators.

**Allowed sort parameters:** `order_id`, `quantity`, `product_id`, `variant_id`, `name`, `weight`, `price`, `order_price`, `vendor_id`, `vendor_name`, `category_id`, `category_name`. Prefix with `-` for descending. Sorting on an unlisted column returns 422.

**Pagination:** standard JSON:API `page[number]` / `page[size]` (1–100, default 20).

## Side effects

None. **`order-products` is read-only — POST / PATCH / DELETE return 405 Method Not Allowed.** Line-item rows are produced by storefront checkout (when the cart is converted to an order) and by admin-panel actions on [[orders-products]] (Add / Edit / Remove product on a placed order). API integrators that need to change line items must go through the admin panel; the API does not expose a path for it.

When a line item is edited via the admin panel, the parent order's `order-modification` rows ([[api-order-modification]]), `order-total` rows ([[api-order-total]]), `order-tax` rows ([[api-order-tax]]), and (post-fulfillment) `order_fulfillment_id` link are all recomputed — see [[order-processing-pipeline]] for the cascading recalculation steps. Reading this resource always returns the latest snapshot.

## Example requests

All examples use `<store-host>` (e.g., `mystore.cloudcart.net`) and `<YOUR_API_KEY>` (64-char uppercase).

### GET collection (sort by quantity descending)

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-products?sort=-quantity&page[size]=20"
```

### GET collection scoped to one order (sort by price)

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-products?filter[order_id]=1042&sort=-price&include=options"
```

### GET single

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-products/5001?include=options,order"
```

### POST / PATCH / DELETE blocked (405)

```bash
curl -s -X POST \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-products" \
     -d '{"data":{"type":"order-products","attributes":{"name":"x","quantity":1}}}'
```

```bash
curl -s -X PATCH \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-products/5001" \
     -d '{"data":{"type":"order-products","id":"5001","attributes":{"quantity":2}}}'
```

```bash
curl -s -X DELETE \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-products/5001"
```

## Example responses

### GET collection success

```json
{
  "data": [
    {
      "type": "order-products",
      "id": "5001",
      "attributes": {
        "order_id": 1042,
        "product_id": 42,
        "variant_id": 101,
        "name": "Cotton T-Shirt",
        "sku": "TSHIRT-M-RED",
        "barcode": "3800100200013",
        "quantity": 2,
        "weight": 220,
        "price": 1999,
        "order_price": 1999,
        "order_discount_id": null,
        "order_fulfillment_id": null,
        "p1": "Size", "v1": "M",
        "p2": "Color", "v2": "Red",
        "vendor_id": 3, "vendor_name": "ACME",
        "category_id": 1,"category_name": "Shirts",
        "sale": "no",
        "new": "yes",
        "digital": "no",
        "tracked": "yes"
      },
      "relationships": {
        "order": { "data": { "type": "orders", "id": "1042" } },
        "options": { "data": [] }
      }
    }
  ],
  "meta": {
    "page": { "current-page": 1, "per-page": 20, "from": 1, "to": 20, "total": 1284, "last-page": 65 }
  }
}
```

### Failure mode

```
HTTP 405 Method Not Allowed
{"errors":[{"status":"405","title":"Method Not Allowed"}]}
```

## Testing checklist

1. `GET /order-products?page[size]=5` — confirm read.
2. `GET /order-products/{id}?include=order,options` — verify shape (snapshot fields present).
3. `GET /order-products?filter[order_id]={id}&sort=-quantity` — verify per-order scoping and sort.
4. `POST /order-products` — verify 405.
5. `PATCH /order-products/{id}` — verify 405.
6. `DELETE /order-products/{id}` — verify 405.
7. Confirm the resource cannot be modified directly — line-item mutations go through the admin-panel [[orders-products]] flow, which produces a recorded [[api-order-modification]] row plus recomputed [[api-order-total]] / [[api-order-tax]] rows.

## Equivalent UI

- [[orders-products]] — per-order line-items list with Add / Edit / Remove product actions (the only surface where line items are managed).
- [[orders-ordered-products]] — cross-order ordered-products report (mirrors `GET /api/v2/order-products` with filters across all orders).
- [[orders-ordered-products-export]] — CSV export equivalent.
- [[orders-details]] — single-order detail showing the line items inline.

## Related

- [[json-api-v2]] — API hub.
- [[api-orders]] — parent order resource (`?include=products` returns this resource embedded).
- [[api-order-products-options]] — selected Product Options per line item.
- [[api-order-discount]] — applied discount on a line item (`order_discount_id`).
- [[api-order-fulfillment]] — fulfillment record covering this line item (`order_fulfillment_id`).
- [[api-order-modification]] — recorded post-placement modifications.
- [[order]] — full order entity reference.
- [[order-processing-pipeline]] — cascading recalculation when a line item is edited.

## Open questions

- Confirm whether the per-line VAT-breakdown hidden fields can be exposed via a sparse-field append in a future API version (currently no `append` is configured, so VAT breakdowns are only reachable via the aggregated [[api-order-tax]] / [[api-order-total]] resources).
- Verify whether digital-product downloadable-file URLs are surfaced anywhere through JSON-API v2 or remain admin-panel-only.
