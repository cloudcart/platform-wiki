---
type: api-resource
resource_path: /api/v2/order-total
http_methods: [GET]
related_entity: order
related_features: [orders-details, orders-invoice]
aliases: ["Order total API", "Order totals breakdown API", "JSON-API v2 order-total", "/order-total"]
tags: [api, json-api-v2, orders]
plan_gates: []
created: 2026-05-26
updated: 2026-06-05
source_count: 2
---
# Order Total (JSON-API v2)

## Purpose

The `order-total` resource is the **read-only view of the totals breakdown on an order** — each row records a category (subtotal, shipping, tax, discount, grand total, etc.) and its accumulated amount. External integrations use it to render order-summary lines in ERP / accounting / receipt systems, validate downstream totals against the platform's authoritative computation, and reconcile shipping / discount entries against the parent order.

Totals are computed by the platform's order-calculation engine on every order recalculation (line-item edit, discount change, shipping change, billing-address change). They are not driven by the API itself.

## Endpoint

| Method | Path | Status |
|---|---|---|
| `GET` | `/api/v2/order-total` | List every total row across every order on the store. |
| `GET` | `/api/v2/order-total/{id}` | Fetch a single total row. |
| `POST` / `PATCH` / `DELETE` | `/api/v2/order-total[/{id}]` | **GET only — returns 405 Method Not Allowed.** Totals are driven by the order-calculation engine; merchants modify totals indirectly by adding / editing line items ([[orders-products]]), applying discounts ([[orders-discount-add]]), or changing shipping. |

No app install or plan feature gates this resource. To scope the response to a single order, filter by `order_id` (auto-merged from the column list) or fetch via the parent with `?include=totals` on [[api-orders]].

## Attributes

All attributes are returned by GET only.

| Attribute | Type | Notes |
|---|---|---|
| `order_id` | integer | Parent order. |
| `code` | string | Total-line code (e.g., `subtotal`, `shipping`, `tax`, `discount`, `total`, `grand_total`). |
| `title` | string | Display label snapshot (localised to the order's language at order time). |
| `value` | integer | Accumulated amount in store currency minor units. |
| `sort_order` | integer | Display order for renderers (matches the merchant-visible order summary). |

Common codes: `subtotal`, `shipping`, `discount`, `tax`, `grand_total`, plus any additional per-app or per-modification codes the platform inserts (Product Options, Bundles, Cross-Sells, Up-Sells each may add their own codes when active).

The schema declares no hidden fields and no appended accessors — every column on the `orders_total` table is surfaced as-is.

**Sparse-field append values:** none configured — appending an unsupported key returns 422.

## Relationships

| Name | Cardinality | Type | Notes |
|---|---|---|---|
| `order` | belongsTo | order | Parent order. |

**Allowed include paths:** `order`.

## Filtering & sorting

**Allowed filtering parameters:** none specific to the resource — only the framework's auto-merged column filters (exact-equality on any column, e.g., `filter[order_id]=123`, `filter[code]=grand_total`). No comparison operators.

**Allowed sort parameters:** none declared — natural insertion order applies. The merchant-visible order summary follows the `sort_order` column.

**Pagination:** standard JSON:API `page[number]` / `page[size]` (1–100, default 20).

## Side effects

None. **`order-total` is read-only — POST / PATCH / DELETE return 405 Method Not Allowed.** Totals are recomputed by the order-calculation engine on every order change (line-item edit, discount change, shipping change, billing-address change with different tax zone). This endpoint exposes the latest snapshot.

## Example requests

All examples use `<store-host>` (e.g., `mystore.cloudcart.net`) and `<YOUR_API_KEY>` (64-char uppercase).

### GET collection

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-total?page[size]=20"
```

### GET collection scoped to one order

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-total?filter[order_id]=1042"
```

### GET single

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-total/9011?include=order"
```

### POST / PATCH / DELETE blocked (405)

```bash
curl -s -X POST \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-total" \
     -d '{"data":{"type":"order-total","attributes":{"code":"grand_total","value":12990}}}'
```

```bash
curl -s -X PATCH \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-total/9011" \
     -d '{"data":{"type":"order-total","id":"9011","attributes":{"value":13500}}}'
```

```bash
curl -s -X DELETE \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-total/9011"
```

## Example responses

### GET collection success

```json
{
  "data": [
    {
      "type": "order-total",
      "id": "9008",
      "attributes": {
        "order_id": 1042,
        "code": "subtotal",
        "title": "Subtotal",
        "value": 10825,
        "sort_order": 1
      },
      "relationships": { "order": { "data": { "type": "orders", "id": "1042" } } }
    },
    {
      "type": "order-total",
      "id": "9009",
      "attributes": {
        "order_id": 1042,
        "code": "shipping",
        "title": "Shipping",
        "value": 590,
        "sort_order": 2
      },
      "relationships": { "order": { "data": { "type": "orders", "id": "1042" } } }
    },
    {
      "type": "order-total",
      "id": "9010",
      "attributes": {
        "order_id": 1042,
        "code": "tax",
        "title": "VAT 20%",
        "value": 2165,
        "sort_order": 3
      },
      "relationships": { "order": { "data": { "type": "orders", "id": "1042" } } }
    },
    {
      "type": "order-total",
      "id": "9011",
      "attributes": {
        "order_id": 1042,
        "code": "grand_total",
        "title": "Total",
        "value": 12990,
        "sort_order": 99
      },
      "relationships": { "order": { "data": { "type": "orders", "id": "1042" } } }
    }
  ],
  "meta": {
    "page": { "current-page": 1, "per-page": 20, "from": 1, "to": 4, "total": 4, "last-page": 1 }
  }
}
```

### Failure mode

```
HTTP 405 Method Not Allowed
{"errors":[{"status":"405","title":"Method Not Allowed"}]}
```

## Testing checklist

1. `GET /order-total?page[size]=5` — confirm read.
2. `GET /order-total/{id}?include=order` — verify shape.
3. `GET /order-total?filter[order_id]={id}&filter[code]=grand_total` — verify code filter.
4. `POST /order-total` — verify 405.
5. `PATCH /order-total/{id}` — verify 405.
6. `DELETE /order-total/{id}` — verify 405.
7. Confirm the resource cannot be modified directly — totals are driven by the calculation engine and refresh on the parent order recalculation cascade ([[order-processing-pipeline]]).

## Equivalent UI

- [[orders-details]] — single-order detail view showing the totals breakdown inline.
- [[orders-invoice]] — invoice generation uses these rows for the summary section.
- [[orders-products]] — line-item edits cause totals to recompute.
- [[orders-discount-add]] — applying a discount cascades through totals.

## Related

- [[json-api-v2]] — API hub.
- [[api-orders]] — parent order resource (`?include=totals`).
- [[api-order-tax]] — tax-row breakdown.
- [[api-order-discount]] — discount-row breakdown.
- [[api-order-shipping]] — shipping-row breakdown.
- [[tax-computation]] — how the `tax` total is computed.
- [[shipping-calculation]] — how the `shipping` total is computed.
- [[order-processing-pipeline]] — recomputation cascade triggers.

## Open questions

- Document the exhaustive list of `code` values produced by the calculation engine across all active apps (Bundles, Cross-Sells, Up-Sells, Product Options each may insert additional codes).
- Confirm whether multi-currency orders expose totals in the original currency vs the converted currency (per [[multi-currency]]).
