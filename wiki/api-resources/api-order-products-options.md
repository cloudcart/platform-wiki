---
type: api-resource
resource_path: /api/v2/order-products-options
http_methods: [GET]
related_entity: order
related_features: [orders-products, orders-details]
aliases: ["Order line-item options API", "Selected product options API", "JSON-API v2 order-products-options", "/order-products-options"]
tags: [api, json-api-v2, orders]
plan_gates: []
created: 2026-05-26
updated: 2026-06-05
source_count: 2
---
# Order Products Options (JSON-API v2)

## Purpose

The `order-products-options` resource is the **read-only view of every Product Option the customer chose on a line item** — for example "Engraving = Yes / text: Happy Birthday Pete", "Gift wrap = Yes", "Size = Large", "Add monogram = Yes / value: PI". Each row records the chosen option's name, value, and any price impact at order time. External integrations use it to pass custom-option choices (engraving text, monogram, gift message, special-handling notes) downstream into production / workshop / fulfillment systems.

Options are captured at storefront checkout based on the merchant's [[apps-product-options-settings-new|Product Options]] app configuration and snapshotted on the order. Changing the *available* options on a product happens in the admin panel; changing the *selected* options on a placed order is not a supported flow — those represent the customer's actual choice and stay immutable.

## Endpoint

| Method | Path | Status |
|---|---|---|
| `GET` | `/api/v2/order-products-options` | List every selected-option row across every order on the store. |
| `GET` | `/api/v2/order-products-options/{id}` | Fetch a single selected-option row. |
| `POST` / `PATCH` / `DELETE` | `/api/v2/order-products-options[/{id}]` | **GET only — returns 405 Method Not Allowed.** Selected options are captured at checkout; the API exposes them for reading, not mutation. |

No app install or plan feature gates this resource at the API layer. (Whether the merchant has any data here depends on whether they have the Product Options app installed and configured on at least one product.) To scope the response to a single line item, filter by `order_product_id` (auto-merged from the column list) or fetch via the parent with `?include=options` on [[api-order-products]].

## Attributes

All attributes are returned by GET only.

| Attribute | Type | Notes |
|---|---|---|
| `order_product_id` | integer | Parent line item ([[api-order-products]]). |
| `name` | string | Option name snapshot (e.g., "Engraving text"). |
| `value` | string | Customer's selected value snapshot (the actual engraving text, or "Large", or "Yes"). |
| `price` | integer | Per-option price impact in store currency minor units. `0` for non-priced options. |
| `discount_price` | integer | Discounted price impact (if a discount applied at order time). |
| `quantity` | float | If the option is quantity-multiplied (rarely). |

**Hidden by default** (VAT breakdowns are aggregated on the parent order's [[api-order-tax]] / [[api-order-total]] rows): `type`, `price_vat`, `price_with_vat`, `price_without_vat`, `discount_price_vat`, `discount_price_with_vat`, `discount_price_without_vat`, `new_format`.

There are no sparse-field append values configured for this resource.

## Relationships

| Name | Cardinality | Type | Notes |
|---|---|---|---|
| `order_product` | belongsTo | order-products | Parent line item. There is no direct `order` relationship at this level — traverse via `order_product → order`. |

**Allowed include paths:** none — the validator declares `$allowedIncludePaths = []`. Use the include from the parent instead: `GET /api/v2/order-products/{id}?include=options`.

## Filtering & sorting

**Allowed filtering parameters:** none specific to the resource — only the framework's auto-merged column filters (exact-equality on any column on the underlying table, e.g., `filter[order_product_id]=5001`). No comparison operators.

**Allowed sort parameters:** none declared — natural insertion order applies (typically by `id` ASC).

**Pagination:** standard JSON:API `page[number]` / `page[size]` (1–100, default 20).

## Side effects

None. **`order-products-options` is read-only — POST / PATCH / DELETE return 405 Method Not Allowed.** Selected-option rows are produced by storefront checkout (or by the admin-panel manual-order flow [[orders-add]] when the merchant builds an order on the customer's behalf) based on the merchant's [[apps-product-options-settings-new|Product Options]] app configuration. They cannot be created, edited, or deleted via the API.

When a line item is edited and the merchant changes the selected options through the admin-panel order-edit flow, the rows here update accordingly and the parent order's [[api-order-total]] / [[api-order-tax]] rows recompute (per [[order-processing-pipeline]]). Reading this resource always returns the latest snapshot.

## Example requests

All examples use `<store-host>` (e.g., `mystore.cloudcart.net`) and `<YOUR_API_KEY>` (64-char uppercase).

### GET collection

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-products-options?page[size]=20"
```

### GET collection scoped to one line item

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-products-options?filter[order_product_id]=5001"
```

### GET single

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-products-options/9101"
```

### POST / PATCH / DELETE blocked (405)

```bash
curl -s -X POST \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-products-options" \
     -d '{"data":{"type":"order-products-options","attributes":{"name":"Engraving","value":"Hi"}}}'
```

```bash
curl -s -X PATCH \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-products-options/9101" \
     -d '{"data":{"type":"order-products-options","id":"9101","attributes":{"value":"new"}}}'
```

```bash
curl -s -X DELETE \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-products-options/9101"
```

## Example responses

### GET collection success

```json
{
  "data": [
    {
      "type": "order-products-options",
      "id": "9101",
      "attributes": {
        "order_product_id": 5001,
        "name": "Engraving text",
        "value": "Happy Birthday Pete",
        "price": 500,
        "discount_price": 0,
        "quantity": 1
      },
      "relationships": {
        "order_product": { "data": { "type": "order-products", "id": "5001" } }
      }
    },
    {
      "type": "order-products-options",
      "id": "9102",
      "attributes": {
        "order_product_id": 5001,
        "name": "Gift wrap",
        "value": "Yes",
        "price": 200,
        "discount_price": 0,
        "quantity": 1
      },
      "relationships": {
        "order_product": { "data": { "type": "order-products", "id": "5001" } }
      }
    }
  ],
  "meta": {
    "page": { "current-page": 1, "per-page": 20, "from": 1, "to": 2, "total": 2, "last-page": 1 }
  }
}
```

### Failure mode

```
HTTP 405 Method Not Allowed
{"errors":[{"status":"405","title":"Method Not Allowed"}]}
```

## Testing checklist

1. `GET /order-products-options?page[size]=5` — confirm read.
2. `GET /order-products-options/{id}` — verify shape.
3. `GET /order-products/{order_product_id}?include=options` — verify the include traversal.
4. `POST /order-products-options` — verify 405.
5. `PATCH /order-products-options/{id}` — verify 405.
6. `DELETE /order-products-options/{id}` — verify 405.
7. Confirm the resource cannot be modified directly — selected options are captured at checkout or via the admin-panel order-edit flow on the parent line item ([[api-order-products]]).

## Equivalent UI

- [[orders-products]] — per-order line-item list (selected options are shown inline under each line item).
- [[orders-details]] — single-order detail view.
- [[apps-product-options-settings-new]] — Product Options app configuration (the source of *which* options exist on a product; this endpoint exposes only the *selected* values at order time).

## Related

- [[json-api-v2]] — API hub.
- [[api-order-products]] — parent line item (`?include=options` returns this resource embedded).
- [[api-orders]] — parent order envelope.
- [[apps-product-options-settings-new]] — Product Options app reference.
- [[order-processing-pipeline]] — totals recompute when options change.

## Open questions

- Confirm exact behaviour when a Product Option is later renamed in the app — whether the row here reflects the original name (snapshot, per the platform's usual snapshot convention) or the new name (live).
- Verify whether attaching a discount to a Product Option populates `discount_price` here vs surfacing only on [[api-order-discount]].
