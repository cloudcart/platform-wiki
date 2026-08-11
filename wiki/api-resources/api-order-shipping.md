---
type: api-resource
resource_path: /api/v2/order-shipping
http_methods: [GET]
related_entity: order
related_features: [orders-details, orders-shipping-waybill]
aliases: ["Order shipping API", "Shipping selection API", "JSON-API v2 order-shipping", "/order-shipping"]
tags: [api, json-api-v2, orders, shipping]
plan_gates: []
created: 2026-05-26
updated: 2026-06-05
source_count: 3
---
# Order Shipping (JSON-API v2)

## Purpose

The `order-shipping` resource is the **read-only view of the shipping selection on every order** — the chosen shipping provider, the calculated shipping amount, the provider-side insurance, and the geo-zone classification used at order placement. External integrations use it to surface shipping context in ERP / fulfillment / accounting pipelines, reconcile shipping revenue per provider, and identify which orders are eligible for which couriers based on geo-zone match.

The order's shipping selection is set at storefront checkout and can be changed post-placement via the admin-panel **Change shipping provider** action (the pre-waybill step on [[orders-shipping-waybill]]). It is not modifiable through this API endpoint.

## Endpoint

| Method | Path | Status |
|---|---|---|
| `GET` | `/api/v2/order-shipping` | List every shipping row across every order on the store. Supports `filter[geo_zone_id]` / `filter[geo_zone_name]`. |
| `GET` | `/api/v2/order-shipping/{id}` | Fetch a single shipping row. |
| `POST` / `PATCH` / `DELETE` | `/api/v2/order-shipping[/{id}]` | **GET only — returns 405 Method Not Allowed.** To change an order's shipping provider, the merchant uses the admin-panel [[orders-shipping-waybill]] flow (pre-waybill step); there is no API equivalent. |

No app install or plan feature gates this resource. To scope the response to a single order, filter by `order_id` (auto-merged from the column list) or fetch via the parent with `?include=shipping.provider` on [[api-orders]].

## Attributes

All attributes are returned by GET only.

| Attribute | Type | Notes |
|---|---|---|
| `order_id` | integer | Parent order. |
| `provider_id` | integer | FK to [[shipping-provider\|Shipping Provider]] catalog. |
| `provider_name` | string | Provider display name snapshot. |
| `provider_amount` | integer | Shipping amount charged by the provider in store currency minor units. |
| `provider_insurance` | integer | Provider-side insurance amount (if any). |
| `order_amount_formatted`, `order_amount_input` (appended) | string | Order-side amount in human-readable / form-input formats. |
| `provider_amount_formatted`, `provider_insurance_formatted` (appended) | string | Provider-side amounts pre-formatted for display. |
| `order_has_insurance` | enum `yes` / `no` | Whether the customer opted into insurance at checkout. |
| `order_insurance` | integer | Insurance amount on the order side. |
| `geo_zone_id` (appended) | integer | Computed geo-zone match at order time (see [[geo-zone\|Geo Zone]]). |
| `geo_zone_name` (appended) | string | Geo-zone name snapshot. |

The schema declares no hidden fields. The `geo_zone_id` and `geo_zone_name` accessors are computed from the order's address + the merchant's geo-zone configuration.

**Sparse-field append values:** none configured — `geo_zone_id` and `geo_zone_name` are appended by default.

## Relationships

| Name | Cardinality | Type | Notes |
|---|---|---|---|
| `order` | belongsTo | order | Parent order. |
| `provider` | hasOne | shipping-providers | Catalog shipping-provider definition (linked via `provider_id`). |

**Allowed include paths:** `order`, `provider`.

## Filtering & sorting

**Allowed filtering parameters:**

| Parameter | Type | Behaviour |
|---|---|---|
| `filter[geo_zone_id]` | integer | Exact match on the computed geo-zone. |
| `filter[geo_zone_name]` | string | Exact match on the geo-zone name. |
| `filter[<any column>]` | per column | Framework auto-merged exact-equality filters on any column (e.g., `filter[order_id]`, `filter[provider_id]`). No comparison operators. |

**Allowed sort parameters:** none declared — natural insertion order applies.

**Pagination:** standard JSON:API `page[number]` / `page[size]` (1–100, default 20).

## Side effects

None. **`order-shipping` is read-only — POST / PATCH / DELETE return 405 Method Not Allowed.** The shipping selection is set at checkout (storefront) and can be changed pre-waybill via the admin-panel flow ([[orders-shipping-waybill]] — Change shipping provider). Once a waybill is generated against the selected provider (see [[api-order-fulfillment]]), changing providers requires removing the waybill first.

## Example requests

All examples use `<store-host>` (e.g., `mystore.cloudcart.net`) and `<YOUR_API_KEY>` (64-char uppercase).

### GET collection (geo-zone filter)

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-shipping?filter[geo_zone_id]=2&page[size]=20"
```

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-shipping?filter[geo_zone_name]=Bulgaria"
```

### GET collection scoped to one order

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-shipping?filter[order_id]=1042&include=provider"
```

### GET single

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-shipping/812?include=order,provider"
```

### POST / PATCH / DELETE blocked (405)

```bash
curl -s -X POST \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-shipping" \
     -d '{"data":{"type":"order-shipping","attributes":{"provider_name":"Econt","provider_amount":590}}}'
```

```bash
curl -s -X PATCH \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-shipping/812" \
     -d '{"data":{"type":"order-shipping","id":"812","attributes":{"provider_amount":700}}}'
```

```bash
curl -s -X DELETE \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-shipping/812"
```

## Example responses

### GET collection success

```json
{
  "data": [
    {
      "type": "order-shipping",
      "id": "812",
      "attributes": {
        "order_id": 1042,
        "provider_id": 5,
        "provider_name": "Econt",
        "provider_amount": 590,
        "provider_insurance": 0,
        "order_amount_formatted": "5.90 BGN",
        "order_amount_input": "5.90",
        "provider_amount_formatted": "5.90 BGN",
        "provider_insurance_formatted": "0.00 BGN",
        "order_has_insurance": "no",
        "order_insurance": 0,
        "geo_zone_id": 2,
        "geo_zone_name": "Bulgaria"
      },
      "relationships": {
        "order": { "data": { "type": "orders", "id": "1042" } },
        "provider": { "data": { "type": "shipping-providers", "id": "5" } }
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

1. `GET /order-shipping?filter[geo_zone_id]=2&page[size]=5` — confirm geo-zone filter.
2. `GET /order-shipping?filter[geo_zone_name]=Bulgaria` — confirm name filter.
3. `GET /order-shipping/{id}?include=order,provider` — verify shape.
4. `POST /order-shipping` — verify 405.
5. `PATCH /order-shipping/{id}` — verify 405.
6. `DELETE /order-shipping/{id}` — verify 405.
7. Confirm the resource cannot be modified directly — shipping selection happens at checkout or via the admin-panel pre-waybill step on [[orders-shipping-waybill]]; once a waybill is generated, the provider is locked until [[api-order-fulfillment]] DELETE removes it.

## Equivalent UI

- [[orders-details]] — single-order detail view showing the shipping selection inline.
- [[orders-shipping-waybill]] — change shipping provider + waybill generation flow.
- [[shipping]] — catalog shipping-provider configuration (admin panel).

## Related

- [[json-api-v2]] — API hub.
- [[api-orders]] — parent order resource (`?include=shipping.provider`).
- [[api-shipping-providers]] — catalog shipping-provider resource.
- [[api-order-shipping-address]] — recipient address used to compute shipping.
- [[api-order-fulfillment]] — waybill / tracking record produced once shipped.
- [[shipping-provider]] — shipping-provider entity reference.
- [[geo-zone]] — geo-zone entity reference.
- [[shipping-calculation]] — how shipping amounts are computed.
- [[shipping-provider-mechanism]] — multi-carrier-aggregator pattern.

## Open questions

- Confirm whether `provider_insurance` reflects the courier's insurance product specifically vs the merchant's own insurance line — the distinction matters for multi-carrier-aggregator providers (per [[shipping-provider-mechanism]]).
- Verify the exact semantics of `order_amount_input` (intended for re-population in an edit form vs displayed amount).
