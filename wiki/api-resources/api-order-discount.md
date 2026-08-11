---
type: api-resource
resource_path: /api/v2/order-discount
http_methods: [GET]
related_entity: order
related_features: [orders-discount-add, orders-details]
aliases: ["Order discount API", "Applied discount API", "JSON-API v2 order-discount", "/order-discount"]
tags: [api, json-api-v2, orders, discounts]
plan_gates: []
created: 2026-05-26
updated: 2026-06-05
source_count: 3
---
# Order Discount (JSON-API v2)

## Purpose

The `order-discount` resource is the **read-only view of every discount applied to an order** — both order-level discounts (e.g., a coupon the customer entered at checkout) and product-level discounts attached to specific line items. Each row records the discount's name, code, type, value, and which line item it targets (if any). External integrations use it to attribute orders to specific promotions, reconcile commission calculations, and audit discount usage against the [[discount|Discount entity]] usage counters.

The catalog-level discount *definitions* live on the separate [[api-discounts]] resource. The rows here are per-order *applications* of those definitions: snapshot data so a renamed or deleted catalog discount still appears on the historical order under the name and value it had when applied.

## Endpoint

| Method | Path | Status |
|---|---|---|
| `GET` | `/api/v2/order-discount` | List every applied-discount row across every order on the store. |
| `GET` | `/api/v2/order-discount/{id}` | Fetch a single applied-discount row. |
| `POST` / `PATCH` / `DELETE` | `/api/v2/order-discount[/{id}]` | **GET only — returns 405 Method Not Allowed.** Discount application happens at storefront checkout (when the customer enters a code) or via the admin-panel [[orders-discount-add]] action on a placed order. Removal happens via the admin-panel per-discount remove action. There is no API mutation path. |

No app install or plan feature gates this resource. To scope the response to a single order, filter by `order_id` (auto-merged from the column list) or fetch via the parent with `?include=discounts` on [[api-orders]].

## Attributes

All attributes are returned by GET only.

| Attribute | Type | Notes |
|---|---|---|
| `order_id` | integer | Parent order. |
| `discount_id` | integer | FK to the catalog [[discount\|Discount]] definition (nullable if the catalog row was deleted after order — snapshot fields below survive). |
| `order_product_id` | integer | Nullable — set when the discount targets a specific line item; `null` for order-level discounts. |
| `parent_id` | integer | Nullable — chains targets for multi-target discounts; when a parent `order-discount` row is deleted, all `parent_id`-children rows are deleted too (per the model's `deleting` hook). |
| `name` | string | Discount name snapshot at order time. |
| `code` | string | Discount code snapshot (the code the customer typed at checkout, if any). |
| `discount_type` | string (appended) | The discount classification — `flat` (fixed-amount), `percent`, `shipping` (free / discounted shipping), `fixed` (fixed-price override). Mapped from the underlying `type` column (which is hidden on the response). |
| `type_value` | number | The discount value (`10` for 10%, `5.00` for €5 off, etc.). |
| `order_over` | number | Minimum order subtotal for the discount to apply (snapshot). |
| `apply_regular_price` | enum `yes` / `no` | Whether the discount applied on the regular price or the already-discounted price (per [[discount-stacking]]). |

**Hidden by default:** `type` (the raw column — surfaced as `discount_type` via the appended accessor instead).

**Sparse-field append values:** none configured — appending an unsupported key returns 422.

## Relationships

| Name | Cardinality | Type | Notes |
|---|---|---|---|
| `order` | belongsTo | order | Parent order. |
| `discount` | belongsTo | discount | Catalog discount definition (may be null if the catalog row was deleted after the order). |

**Allowed include paths:** `order`, `discount`.

## Filtering & sorting

**Allowed filtering parameters:** none specific to the resource — only the framework's auto-merged column filters (exact-equality on any column, e.g., `filter[order_id]=123`, `filter[discount_id]=45`, `filter[code]=SUMMER20`). No comparison operators.

**Allowed sort parameters:** none declared — natural insertion order applies.

**Pagination:** standard JSON:API `page[number]` / `page[size]` (1–100, default 20).

## Side effects

None. **`order-discount` is read-only — POST / PATCH / DELETE return 405 Method Not Allowed.** Discount application happens at storefront checkout or via the admin-panel [[orders-discount-add]] flow; removal happens via the admin-panel per-discount remove action.

The catalog-level discount-usage counter on [[discount]] is recomputed on every parent-order status change via a 10-second-delayed `DiscountUsageSync` job on the `order-events6` queue (per [[api-orders]] side effects and [[order-processing-pipeline]]). Reading this resource always returns the latest snapshot.

## Example requests

All examples use `<store-host>` (e.g., `mystore.cloudcart.net`) and `<YOUR_API_KEY>` (64-char uppercase).

### GET collection

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-discount?page[size]=20"
```

### GET collection scoped to one order

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-discount?filter[order_id]=1042&include=discount"
```

### GET single

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-discount/4501?include=order,discount"
```

### POST / PATCH / DELETE blocked (405)

```bash
curl -s -X POST \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-discount" \
     -d '{"data":{"type":"order-discount","attributes":{"name":"x","type_value":10}}}'
```

```bash
curl -s -X PATCH \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-discount/4501" \
     -d '{"data":{"type":"order-discount","id":"4501","attributes":{"type_value":15}}}'
```

```bash
curl -s -X DELETE \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-discount/4501"
```

## Example responses

### GET collection success

```json
{
  "data": [
    {
      "type": "order-discount",
      "id": "4501",
      "attributes": {
        "order_id": 1042,
        "discount_id": 88,
        "order_product_id": null,
        "parent_id": null,
        "name": "Summer 20% off",
        "code": "SUMMER20",
        "discount_type": "percent",
        "type_value": 20,
        "order_over": 0,
        "apply_regular_price": "yes"
      },
      "relationships": {
        "order": { "data": { "type": "orders", "id": "1042" } },
        "discount": { "data": { "type": "discounts", "id": "88" } }
      }
    }
  ],
  "meta": {
    "page": { "current-page": 1, "per-page": 20, "from": 1, "to": 1, "total": 1, "last-page": 1 }
  }
}
```

### Failure mode

```
HTTP 405 Method Not Allowed
{"errors":[{"status":"405","title":"Method Not Allowed"}]}
```

## Testing checklist

1. `GET /order-discount?page[size]=5` — confirm read.
2. `GET /order-discount/{id}?include=discount,order` — verify shape (snapshot fields present even if the catalog discount was later deleted).
3. `GET /order-discount?filter[code]=SUMMER20` — verify attribution by code.
4. `POST /order-discount` — verify 405.
5. `PATCH /order-discount/{id}` — verify 405.
6. `DELETE /order-discount/{id}` — verify 405.
7. Confirm the resource cannot be modified directly — discount application goes through storefront checkout or the admin-panel [[orders-discount-add]] flow.

## Equivalent UI

- [[orders-discount-add]] — manual discount application on a placed order (admin panel).
- [[orders-details]] — single-order detail view showing applied discounts inline.
- [[marketing-discounts]] — catalog-level discount definitions (managed via [[api-discounts]]).

## Related

- [[json-api-v2]] — API hub.
- [[api-orders]] — parent order resource (`?include=discounts`).
- [[api-discounts]] — catalog discount definitions (the source of `discount_id`).
- [[api-discount-codes]] / [[api-discount-codes-pro]] — discount-code management.
- [[discount]] — discount entity reference.
- [[discount-stacking]] — how discounts combine on an order.
- [[order-processing-pipeline]] — discount-usage recompute timing.

## Open questions

- Verify whether deleting an `order-discount` row through admin actions cascades to the `order_total` rows accurately (totals recompute, but the relationship between the discount-row deletion and the resulting [[api-order-total]] adjustments is subtle).
- Confirm exact semantics of `parent_id` for multi-target discounts (e.g., a single 10%-off-everything discount that creates separate per-line-item child rows linked to one parent row).
