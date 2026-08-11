---
type: api-resource
resource_path: /api/v2/order-modification
http_methods: [GET]
related_entity: order
related_features: [orders-products, orders-details, orders-history]
aliases: ["Order modification API", "Order adjustments API", "JSON-API v2 order-modification", "/order-modification"]
tags: [api, json-api-v2, orders]
plan_gates: []
created: 2026-05-26
updated: 2026-06-05
source_count: 2
---
# Order Modification (JSON-API v2)

## Purpose

The `order-modification` resource is the **read-only view of post-placement modifications recorded on an order** — the manual adjustments the merchant made after the order was first created (price overrides, quantity changes, custom adjustments) that are tracked separately from the original line items for audit. External integrations use it to surface "what changed since the customer placed this order" in ERP / accounting / reporting pipelines, distinct from the original-items snapshot on [[api-order-products]].

Modification rows are produced as a side effect of admin-panel order-edit actions ([[orders-products]] → Edit line item, change quantity, override price) and recorded alongside an entry on [[orders-history]]. They are not driven by the API itself.

## Endpoint

| Method | Path | Status |
|---|---|---|
| `GET` | `/api/v2/order-modification` | List every modification row across every order on the store. |
| `GET` | `/api/v2/order-modification/{id}` | Fetch a single modification row. |
| `POST` / `PATCH` / `DELETE` | `/api/v2/order-modification[/{id}]` | **GET only — returns 405 Method Not Allowed.** Modifications are produced by admin-panel order-edit actions ([[orders-products]]); there is no API equivalent for editing a placed order's line items. |

No app install or plan feature gates this resource. To scope the response to a single order, filter by `order_id` (auto-merged from the column list) or fetch via the parent with `?include=modifications` on [[api-orders]].

## Attributes

All attributes are returned by GET only. Common fields recorded per modification row:

| Attribute | Type | Notes |
|---|---|---|
| `order_id` | integer | Parent order. |
| `name` | string | Modification label (what was changed, e.g., "Manual price adjustment"). |
| `type` | string | Modification type (the model's internal classification). |
| `value` | number | The numeric value of the adjustment in store currency minor units (price delta etc.). |
| `quantity` | float | Affected quantity (when relevant). |

The exact column set tracks whatever the platform needs to reconstruct what changed — consult [[order]] for the full attribute reference. The schema declares no hidden fields and no appended accessors, so every column on the `orders_modification` table is surfaced as-is.

**Sparse-field append values:** none configured — appending an unsupported key returns 422.

## Relationships

| Name | Cardinality | Type | Notes |
|---|---|---|---|
| `order` | belongsTo | order | Parent order. |

**Allowed include paths:** `order`.

## Filtering & sorting

**Allowed filtering parameters:** none specific to the resource — only the framework's auto-merged column filters (exact-equality on any column, e.g., `filter[order_id]=123`). No comparison operators.

**Allowed sort parameters:** none declared — natural insertion order applies.

**Pagination:** standard JSON:API `page[number]` / `page[size]` (1–100, default 20).

## Side effects

None. **`order-modification` is read-only — POST / PATCH / DELETE return 405 Method Not Allowed.** Modifications are produced when the merchant edits a placed order in the admin panel ([[orders-products]] line-item edit, quantity change, price override). The platform writes the modification row + an [[orders-history]] entry as part of the same edit; this endpoint exposes the recorded row for downstream reading.

Edits also recompute [[api-order-total]] / [[api-order-tax]] rows on the parent order (per [[order-processing-pipeline]]). Reading this resource always returns the latest snapshot.

## Example requests

All examples use `<store-host>` (e.g., `mystore.cloudcart.net`) and `<YOUR_API_KEY>` (64-char uppercase).

### GET collection

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-modification?page[size]=20"
```

### GET collection scoped to one order

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-modification?filter[order_id]=1042"
```

### GET single

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-modification/3301?include=order"
```

### POST / PATCH / DELETE blocked (405)

```bash
curl -s -X POST \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-modification" \
     -d '{"data":{"type":"order-modification","attributes":{"name":"adjust","value":500}}}'
```

```bash
curl -s -X PATCH \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-modification/3301" \
     -d '{"data":{"type":"order-modification","id":"3301","attributes":{"value":750}}}'
```

```bash
curl -s -X DELETE \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-modification/3301"
```

## Example responses

### GET collection success

```json
{
  "data": [
    {
      "type": "order-modification",
      "id": "3301",
      "attributes": {
        "order_id": 1042,
        "name": "Manual price adjustment",
        "type": "price_override",
        "value": -500,
        "quantity": 1
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

1. `GET /order-modification?page[size]=5` — confirm read.
2. `GET /order-modification/{id}?include=order` — verify shape.
3. `GET /order-modification?filter[order_id]={id}` — verify per-order scoping.
4. `POST /order-modification` — verify 405.
5. `PATCH /order-modification/{id}` — verify 405.
6. `DELETE /order-modification/{id}` — verify 405.
7. Confirm the resource cannot be modified directly — modifications are produced by admin-panel order-edit actions on [[orders-products]]; they cascade through [[order-processing-pipeline]] and are recorded in [[orders-history]].

## Equivalent UI

- [[orders-products]] — line-item edit actions that produce modification rows (merchant flow).
- [[orders-details]] — single-order detail view showing modifications inline.
- [[orders-history]] — full audit trail, including modification events.

## Related

- [[json-api-v2]] — API hub.
- [[api-orders]] — parent order resource (`?include=modifications`).
- [[api-order-products]] — original line items snapshot (modifications express the delta from this snapshot).
- [[api-order-total]] — recomputed totals reflecting modifications.
- [[order]] — full order entity reference.
- [[order-processing-pipeline]] — totals recompute when modifications are added.
- [[orders-history]] — merchant-visible audit trail.

## Open questions

- Document the exact `type` classification (the platform tracks several modification kinds — price-override, quantity-change, custom-adjustment — and the full enumeration needs to be confirmed from the schema).
- Confirm whether removing a modification (via the admin panel) deletes the row or marks it inactive; the API view of the audit trail differs accordingly.
