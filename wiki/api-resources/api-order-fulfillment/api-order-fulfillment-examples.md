---
type: api-resource
resource_path: /api/v2/order-fulfillment
http_methods: [GET, POST, PATCH, DELETE]
related_entity: order
related_features: [orders-shipping-waybill, orders-details]
aliases: ["Order fulfillment API examples", "order-fulfillment curl", "mark order shipped example", "order-fulfillment POST example", "order-fulfillment DELETE example", "order-fulfillment testing checklist", "order-fulfillment integrator notes"]
tags: [api, json-api-v2, orders, fulfillment, waybill]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 6
---
# Order Fulfillment API — examples & testing

> Part of [[api-order-fulfillment]]. See the hub for the other aspects (attributes & querying, side effects & failure modes).

## Purpose

This aspect holds the worked `curl` requests + JSON responses for GET / POST / PATCH / DELETE on the `order-fulfillment` resource, plus the end-to-end integrator testing checklist and the gotchas that catch most integrations (no courier call on POST, no partial fulfillment, silent courier-void failure on DELETE). Use it as the copy-paste reference once the attribute shape ([[api-order-fulfillment-attributes]]) and the side-effect cascade ([[api-order-fulfillment-side-effects]]) are understood.

## Endpoint

All examples below exercise `/api/v2/order-fulfillment`. The full method table lives on the hub [[api-order-fulfillment]]. Examples use `<store-host>` (e.g. `mystore.cloudcart.net`) and `<YOUR_API_KEY>` (64-char uppercase). Auth / header conventions: see [[json-api-v2]].

## Attributes

The request payloads below set the writable attributes (`shipping_tracking_url`, `shipping_tracking_number`, `shipping_date_expedition`, `shipping_date_delivery`) and the required `order` relationship documented on [[api-order-fulfillment-attributes]]. The responses echo the read-only `order_id`, `shipping_provider`, and `date_fulfilled` set by the platform.

## Relationships

The POST payload carries the single `order` relationship; `include=order` on a GET embeds the parent order in the response. See [[api-order-fulfillment-attributes]] for the include rules.

## Filtering & sorting

The GET examples below show `sort=-date_fulfilled` (descending) and `filter[order_id]=<id>` (scope to one order). The full filter / sort reference is on [[api-order-fulfillment-attributes]].

### GET collection (sort by date_fulfilled descending)

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-fulfillment?sort=-date_fulfilled&page[size]=20"
```

### GET collection scoped to one order

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-fulfillment?filter[order_id]=1042&include=order"
```

### GET single

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-fulfillment/2201?include=order"
```

### GET collection success (response)

```json
{
  "data": [
    {
      "type": "order-fulfillment",
      "id": "2201",
      "attributes": {
        "order_id": 1042,
        "shipping_provider": "Econt",
        "shipping_tracking_url": "https://tracking.example.com/PKG123456789",
        "shipping_tracking_number": "PKG123456789",
        "shipping_date_expedition": "2026-06-05",
        "shipping_date_delivery": "2026-06-08",
        "date_fulfilled": "2026-06-05 11:14:08"
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

## Side effects

The POST below runs the full 14-step shipment cascade and the DELETE runs the teardown — both documented in detail on [[api-order-fulfillment-side-effects]]. The examples here only show the request / response shapes; read that aspect before running them against a live order.

### POST minimal (mark order as shipped)

API POST records the fulfillment and runs the cascade — but it does **NOT** call the courier API to dispatch the package. The merchant's external ERP / integration is expected to have already booked the dispatch with the courier and to PATCH back the tracking info.

```bash
curl -s -X POST \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-fulfillment" \
     -d '{
       "data": {
         "type": "order-fulfillment",
         "attributes": {
           "shipping_tracking_url": "https://tracking.example.com/PKG123456789",
           "shipping_tracking_number": "PKG123456789",
           "shipping_date_expedition": "2026-06-05",
           "shipping_date_delivery": "2026-06-08"
         },
         "relationships": {
           "order": { "data": { "type": "orders", "id": "1042" } }
         }
       }
     }'
```

### POST 201 Created (response — snapshot returned, cascade fires)

```json
{
  "data": {
    "type": "order-fulfillment",
    "id": "2201",
    "attributes": {
      "order_id": 1042,
      "shipping_provider": "Econt",
      "shipping_tracking_url": "https://tracking.example.com/PKG123456789",
      "shipping_tracking_number": "PKG123456789",
      "shipping_date_expedition": "2026-06-05",
      "shipping_date_delivery": "2026-06-08",
      "date_fulfilled": "2026-06-05 11:14:08"
    },
    "relationships": {
      "order": { "data": { "type": "orders", "id": "1042" } }
    }
  }
}
```

### PATCH (update tracking after dispatch)

```bash
curl -s -X PATCH \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-fulfillment/2201" \
     -d '{
       "data": {
         "type": "order-fulfillment",
         "id": "2201",
         "attributes": {
           "shipping_tracking_url": "https://tracking.example.com/PKG999888777",
           "shipping_tracking_number": "PKG999888777",
           "shipping_date_delivery": "2026-06-09"
         }
       }
     }'
```

### DELETE (void the fulfillment)

```bash
curl -s -X DELETE \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-fulfillment/2201"
```

DELETE reverts the parent order: `status_fulfillment` → `not_fulfilled` and `status` → `paid` (if the last payment is completed) or `pending`. If `omniship_provider` + `bol_id` are set, the courier-void call may silently fail (e.g. Econt: *"Package already in transit"*) — the local fulfillment row is removed regardless. `order.updated` fires.

### Failure modes (responses)

```
HTTP 422 Unprocessable Entity (already fulfilled)
{"errors":[{"status":"422","source":{"pointer":"/data/relationships/order"},"detail":"This order is already fulfilled."}]}
```

```
HTTP 422 Unprocessable Entity (missing required relationship)
{"errors":[{"status":"422","source":{"pointer":"/data/relationships/order"},"detail":"The order field is required."}]}
```

```
HTTP 422 Unprocessable Entity (bad URL)
{"errors":[{"status":"422","source":{"pointer":"/data/attributes/shipping_tracking_url"},"detail":"The shipping tracking url format is invalid."}]}
```

```
HTTP 422 Unprocessable Entity (bad date format)
{"errors":[{"status":"422","source":{"pointer":"/data/attributes/shipping_date_delivery"},"detail":"The shipping date delivery does not match the format Y-m-d."}]}
```

## Testing checklist

1. `GET /order-fulfillment?filter[order_id]=<id>` — confirm read.
2. `POST /order-fulfillment` with `order` relationship + minimal payload — capture the id; verify the cascade kicks off ([[orders-history]] audit entry with `namespace="api2"` → "API", customer email if `notify_customer=yes`, inventory decrement, invoice / receipt numbers, `order.updated` webhook). Full cascade: [[api-order-fulfillment-side-effects]].
3. `GET /order-fulfillment/{id}` — verify the snapshot.
4. `PATCH /order-fulfillment/{id}` — update tracking; verify the new values persist and `order.updated` fires.
5. `DELETE /order-fulfillment/{id}` — verify the parent order's `status_fulfillment` reverts to `not_fulfilled` and `status` reverts to `paid` (if the last payment is completed) or `pending`; the courier-void call may silently fail; `order.updated` fires.

**Integrator notes:**

- API POST does **NOT** call the courier — the merchant's external integration must book the dispatch with the courier API first, then POST here with the returned tracking. Use [[orders-shipping-waybill]] (admin panel) instead if you want the courier integration leg.
- Partial fulfillment is not exposed — POST fulfills every shippable line item on the order at once. See [[api-order-fulfillment-attributes]].
- On DELETE, courier-void failures are silently swallowed (validated on [[orders-shipping-waybill]]) — verify with the courier dashboard when integrating.
- All mutations on other order sub-resources (line items, addresses, totals, taxes) go through the admin panel or the parent [[api-orders]] resource — `order-fulfillment` is the only writable order sub-resource.

## Equivalent UI

- [[orders-shipping-waybill]] — the admin-panel waybill flow; **Save** ≈ POST, **Remove** ≈ DELETE.
- [[orders-details]] — single-order detail view where the fulfillment record appears.

## Related

- [[api-order-fulfillment]] — hub.
- [[api-order-fulfillment-attributes]] — attribute + relationship + filter reference for these requests.
- [[api-order-fulfillment-side-effects]] — the cascade the POST / DELETE examples trigger.
- [[json-api-v2]] — API hub (auth, headers, status codes).
- [[api-orders]] — parent order resource.
- [[orders-history]] — audit-trail entries produced by these calls.
- [[orders-notify-customer]] — the customer-email gate.
- [[order]] — full order entity reference.

## Open questions

- Confirm whether partial-fulfillment support is on the roadmap (currently all-or-nothing: POST fulfills every shippable line item on the order at once). `(verify)`
- Document an end-to-end example where the external ERP books the courier dispatch first and then POSTs here — including how `bol_id` gets set so a later DELETE can void at the courier. `(verify)`
