---
type: api-resource
resource_path: /api/v2/order-tax
http_methods: [GET]
related_entity: order
related_features: [orders-details, orders-invoice]
aliases: ["Order tax API", "Tax breakdown API", "JSON-API v2 order-tax", "/order-tax"]
tags: [api, json-api-v2, orders, tax]
plan_gates: []
created: 2026-05-26
updated: 2026-06-05
source_count: 2
---
# Order Tax (JSON-API v2)

## Purpose

The `order-tax` resource is the **read-only view of the per-bracket tax rows on an order** — each row records a tax bracket (VAT class, rate, name) and the amount accumulated for that bracket on this order. External integrations use it to feed tax breakdowns into accounting / invoicing systems, generate VAT declarations, reconcile per-rate totals against the platform's authoritative computation.

Tax rows are computed by the platform's tax engine at order placement and re-computed on every order recalculation (line-item edit, discount change, billing-address change that crosses a tax zone). They are not driven by the API itself.

## Endpoint

| Method | Path | Status |
|---|---|---|
| `GET` | `/api/v2/order-tax` | List every tax row across every order on the store. |
| `GET` | `/api/v2/order-tax/{id}` | Fetch a single tax row. |
| `POST` / `PATCH` / `DELETE` | `/api/v2/order-tax[/{id}]` | **GET only — returns 405 Method Not Allowed.** Tax computation is driven by the platform's tax engine ([[tax-computation]]); catalog tax classes are managed via [[settings-taxes]]. |

No app install or plan feature gates this resource. To scope the response to a single order, filter by `order_id` (auto-merged from the column list) or fetch via the parent with `?include=taxes` on [[api-orders]].

## Attributes

All attributes are returned by GET only.

| Attribute | Type | Notes |
|---|---|---|
| `order_id` | integer | Parent order. |
| `name` | string | Tax class name snapshot (e.g., "VAT 20%"). |
| `rate` | number | Tax rate snapshot (e.g., `20.00`). |
| `value` | integer | Tax amount accumulated on this row in store currency minor units. |
| `class_id` / `tax_id` | integer | FK to the catalog [[tax\|Tax]] class definition (may be null if class deleted after order). |
| `type` | string | Tax type classification (e.g., `included` vs `additional`). |

The schema declares no hidden fields and no appended accessors — every column on the `orders_tax` table is surfaced as-is.

**Sparse-field append values:** none configured — appending an unsupported key returns 422.

## Relationships

| Name | Cardinality | Type | Notes |
|---|---|---|---|
| `order` | belongsTo | order | Parent order. |

**Allowed include paths:** `order`.

## Filtering & sorting

**Allowed filtering parameters:** none specific to the resource — only the framework's auto-merged column filters (exact-equality on any column, e.g., `filter[order_id]=123`, `filter[name]=VAT%2020%25`). No comparison operators.

**Allowed sort parameters:** none declared — natural insertion order applies.

**Pagination:** standard JSON:API `page[number]` / `page[size]` (1–100, default 20).

## Side effects

None. **`order-tax` is read-only — POST / PATCH / DELETE return 405 Method Not Allowed.** Tax rows are computed by the tax engine on order create / edit (per [[tax-computation]]). They refresh automatically when the order recalculates (line-item edit, discount change, billing-address change with different tax zone, shipping change). This endpoint exposes the latest snapshot.

## Example requests

All examples use `<store-host>` (e.g., `mystore.cloudcart.net`) and `<YOUR_API_KEY>` (64-char uppercase).

### GET collection

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-tax?page[size]=20"
```

### GET collection scoped to one order

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-tax?filter[order_id]=1042"
```

### GET single

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-tax/7001?include=order"
```

### POST / PATCH / DELETE blocked (405)

```bash
curl -s -X POST \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-tax" \
     -d '{"data":{"type":"order-tax","attributes":{"name":"VAT 20%","value":2165}}}'
```

```bash
curl -s -X PATCH \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-tax/7001" \
     -d '{"data":{"type":"order-tax","id":"7001","attributes":{"value":2200}}}'
```

```bash
curl -s -X DELETE \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-tax/7001"
```

## Example responses

### GET collection success

```json
{
  "data": [
    {
      "type": "order-tax",
      "id": "7001",
      "attributes": {
        "order_id": 1042,
        "name": "VAT 20%",
        "rate": 20.00,
        "value": 2165,
        "class_id": 1,
        "tax_id": 1,
        "type": "included"
      },
      "relationships": {
        "order": { "data": { "type": "orders", "id": "1042" } }
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

1. `GET /order-tax?page[size]=5` — confirm read.
2. `GET /order-tax/{id}?include=order` — verify shape.
3. `GET /order-tax?filter[order_id]={id}` — verify per-order scoping.
4. `POST /order-tax` — verify 405.
5. `PATCH /order-tax/{id}` — verify 405.
6. `DELETE /order-tax/{id}` — verify 405.
7. Confirm the resource cannot be modified directly — tax rows are produced by the tax engine ([[tax-computation]]); catalog tax classes are managed via [[settings-taxes]] and refresh on the parent order recalculation cascade ([[order-processing-pipeline]]).

## Equivalent UI

- [[orders-details]] — single-order detail view showing tax breakdown inline.
- [[orders-invoice]] — invoice generation uses these rows to render VAT lines.
- [[settings-taxes]] — catalog tax-class management (the source of `class_id` definitions).

## Related

- [[json-api-v2]] — API hub.
- [[api-orders]] — parent order resource (`?include=taxes`).
- [[api-order-total]] — totals breakdown including tax-inclusive vs tax-exclusive lines.
- [[tax-computation]] — how VAT and other taxes are computed.
- [[tax]] — tax-class entity reference.
- [[order-processing-pipeline]] — recomputation cascade triggers.

## Open questions

- Document the exact `type` enumeration (e.g., `included_in_price` vs `added_to_price`) — affects how external invoicing systems should display the breakdown.
- Confirm whether multi-currency orders expose tax in the original currency vs the converted currency (per [[multi-currency]] behaviour).
