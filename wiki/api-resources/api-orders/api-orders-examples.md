---
type: api-resource
resource_path: /api/v2/orders
http_methods: [GET, PATCH]
related_entity: order
related_features: [orders, orders-details, orders-status-change]
aliases: ["Orders API examples", "orders curl examples", "orders JSON responses", "orders testing checklist", "API поръчки примери"]
tags: [api, json-api-v2, orders]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---
# Orders API — examples & testing

> Part of [[api-orders]]. See the hub for the other aspects (attributes & querying, side effects & failure modes).

## Purpose

This aspect holds the worked **curl requests + JSON responses** for every operation on the `orders` resource (GET collection / single, the `/order-status` helper, PATCH status / invoice metadata / fulfill, and the blocked POST / DELETE verbs) plus the end-to-end **integration testing checklist** an integrator runs to validate their setup.

## Endpoint

All examples target `/api/v2/orders`, `/api/v2/orders/{id}`, `/api/v2/orders/{id}/fulfill`, and the `/api/v2/order-status` helper. They use `<store-host>` (e.g. `mystore.cloudcart.net`), `<YOUR_API_KEY>` (64-char uppercase), and a numeric resource id. Auth + headers: see [[json-api-v2]].

## Attributes

The PATCH examples write the four writable attributes (`status` via `status_id`, `invoice_number`, `invoice_date`, `usn`); the `/fulfill` example writes the fulfillment fields documented on [[api-order-fulfillment]]. Field-by-field reference: see [[api-orders-attributes]].

## Relationships

The GET-single example demonstrates the `?include=` paths — `products`, `payment`, `discounts`, `modifications`, `totals`, `taxes`, `shipping.provider`, `shipping-address`, `billing-address`. The allowed-include list + nesting limit: see [[api-orders-attributes]].

## Filtering & sorting

The GET-collection example below shows the `filter[start_date]` / `filter[end_date]` + `sort=-date_added` + `page[size]` combination. The full filter / sort reference: see [[api-orders-attributes]].

## Example requests

### GET collection (date range + sort)

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/orders?filter[start_date]=2026-06-01&filter[end_date]=2026-06-30&sort=-date_added&page[size]=20"
```

### GET single (with full envelope)

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/orders/1042?include=products,payment,discounts,modifications,totals,taxes,shipping.provider,shipping-address,billing-address"
```

### GET order-status helper (non-JSON:API shape)

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-status"
```

Search by slug:

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-status?filter=paid"
```

### PATCH change status

Use the id returned by `/order-status` for the target status key.

```bash
curl -s -X PATCH \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/orders/1042" \
     -d '{
       "data": {
         "type": "orders",
         "id": "1042",
         "attributes": {
           "status_id": 2
         }
       }
     }'
```

### PATCH set invoice metadata

```bash
curl -s -X PATCH \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/orders/1042" \
     -d '{
       "data": {
         "type": "orders",
         "id": "1042",
         "attributes": {
           "invoice_number": "0000001234",
           "invoice_date": "2026-06-05 10:00:00"
         }
       }
     }'
```

### PATCH custom fulfill action

```bash
curl -s -X PATCH \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/orders/1042/fulfill" \
     -d '{
       "data": {
         "type": "orders",
         "id": "1042",
         "attributes": {
           "shipping_tracking_url": "https://tracking.example.com/PKG123456789",
           "shipping_tracking_number": "PKG123456789",
           "shipping_date_expedition": "2026-06-05",
           "shipping_date_delivery": "2026-06-08"
         }
       }
     }'
```

### POST blocked (405)

```bash
curl -s -X POST \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/orders" \
     -d '{"data":{"type":"orders","attributes":{}}}'
```

### DELETE blocked (405)

```bash
curl -s -X DELETE \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/orders/1042"
```

## Example responses

### GET collection success

```json
{
  "data": [
    {
      "type": "orders",
      "id": "1042",
      "attributes": {
        "status": "paid",
        "status_id": 2,
        "currency": "BGN",
        "total": 12990,
        "subtotal": 10825,
        "tax": 2165,
        "discount": 0,
        "shipping_price": 590,
        "notify_customer": "yes",
        "status_fulfillment": "not_fulfilled",
        "customer_first_name": "Ivan",
        "customer_last_name": "Petrov",
        "customer_email": "ivan@example.com",
        "date_added": "2026-06-04 14:22:11",
        "updated_at": "2026-06-05 09:01:33"
      },
      "relationships": {
        "products": { "data": [{ "type": "order-products", "id": "5001" }] },
        "payment": { "data": { "type": "order-payment", "id": "801" } },
        "shipping": { "data": { "type": "order-shipping", "id": "812" } },
        "shipping-address":{ "data": { "type": "order-shipping-address", "id": "1042" } },
        "billing-address": { "data": { "type": "order-billing-address", "id": "1042" } }
      }
    }
  ],
  "meta": {
    "page": { "current-page": 1, "per-page": 20, "from": 1, "to": 20, "total": 318, "last-page": 16 }
  }
}
```

### GET single (with include)

```json
{
  "data": {
    "type": "orders",
    "id": "1042",
    "attributes": {
      "status": "paid",
      "status_id": 2,
      "total": 12990,
      "currency": "BGN",
      "status_fulfillment": "not_fulfilled",
      "invoice_number": null,
      "invoice_date": null,
      "usn": null,
      "date_added": "2026-06-04 14:22:11"
    },
    "relationships": {
      "products": { "data": [{ "type": "order-products", "id": "5001" }] },
      "totals": { "data": [{ "type": "order-total", "id": "9011" }] },
      "taxes": { "data": [{ "type": "order-tax", "id": "7001" }] },
      "payment": { "data": { "type": "order-payment", "id": "801" } }
    }
  },
  "included": [
    { "type": "order-products", "id": "5001", "attributes": { "name": "Cotton T-Shirt", "sku": "TSHIRT-M-RED", "quantity": 1, "price": 9990, "order_price": 9990 } },
    { "type": "order-total", "id": "9011", "attributes": { "code": "grand_total", "title": "Total", "value": 12990 } },
    { "type": "order-tax", "id": "7001", "attributes": { "name": "VAT 20%", "rate": 20.00, "value": 2165 } },
    { "type": "order-payment", "id": "801", "attributes": { "provider": "stripe", "amount": 12990, "status": "completed" } }
  ]
}
```

### GET /order-status response (non-JSON:API)

```json
{
  "data": [
    { "id": 1, "name": "Pending", "slug": "pending", "status_type": "default" },
    { "id": 2, "name": "Paid", "slug": "paid", "status_type": "default" },
    { "id": 3, "name": "Fulfilled", "slug": "fulfilled", "status_type": "default" },
    { "id": 4, "name": "Completed", "slug": "completed", "status_type": "default" },
    { "id": 5, "name": "Cancelled", "slug": "cancelled", "status_type": "default" }
  ]
}
```

### Failure modes

```
HTTP 422 Unprocessable Entity
{"errors":[{"status":"422","source":{"pointer":"/data/attributes/status_id"},"detail":"Invalid status. You can use one of: pending, paid, fulfilled, completed, cancelled"}]}
```

```
HTTP 405 Method Not Allowed (POST /orders)
{"errors":[{"status":"405","title":"Method Not Allowed"}]}
```

```
HTTP 405 Method Not Allowed (DELETE /orders/{id})
{"errors":[{"status":"405","title":"Method Not Allowed"}]}
```

```
HTTP 422 Unprocessable Entity (invoice_number reused)
{"errors":[{"status":"422","source":{"pointer":"/data/attributes/invoice_number"},"detail":"The invoice number has already been taken."}]}
```

The full 422 / 405 catalogue + the cascade each PATCH triggers: see [[api-orders-side-effects]].

## Filtering & sorting

(Covered above under *Filtering & sorting* — the GET-collection example demonstrates the date-range + sort + page combination; the reference table is on [[api-orders-attributes]].)

## Side effects

The PATCH and `/fulfill` examples above fire the full status-transition / fulfillment cascade. Run them against a sandbox order first — see [[api-orders-side-effects]] for the complete catalogue before executing in production.

## Equivalent UI

- [[orders]] — the list view a GET-collection call mirrors.
- [[orders-details]] — the detail view a GET-single (with includes) call mirrors.
- [[orders-status-change]] — the UI equivalent of the PATCH-status example.

## Testing checklist

1. `GET /order-status` — get the catalog of valid statuses; capture target status id.
2. `GET /orders?filter[start_date]=2026-06-01&page[size]=5` — confirm read.
3. `GET /orders/{id}?include=products,payment,totals,taxes` — verify shape.
4. `PATCH /orders/{id}` — change `status_id` to the captured id; verify webhook fires (`order.updated`) and [[orders-history]] records `namespace="api2"` ("API").
5. `PATCH /orders/{id}` — set `invoice_number`; verify the uniqueness gate (try the same number on a second order → 422).
6. `POST /orders` — verify 405 (creation blocked — orders are placed via storefront checkout or [[orders-add]]).
7. `DELETE /orders/{id}` — verify 405 (cancellation goes through status change; long-term cleanup via [[orders-archive]]).
8. `PATCH /orders/{id}/fulfill` — verify the fulfill cascade ([[api-order-fulfillment]] row created, `order.updated` fires, [[order-processing-pipeline]] runs).

**Integrator notes:**

- POST is blocked because order creation must go through storefront checkout or the admin-panel manual-order flow ([[orders-add]]). The custom `PATCH /{id}/fulfill` is the only "create-like" call.
- `invoice_number` is a one-shot gate — once set on any order, attempting the same number on another order returns 422.
- `filter[start_date]` / `filter[end_date]` rewrite to `WHERE date_added >= / <= ?` with a forced index hint — use these for bulk-fetch loops rather than synthesising column filters.
- Every status PATCH fires the full cascade — see [[api-orders-side-effects]] and [[order-processing-pipeline]] for the side-effect catalogue.

## Related

- [[api-orders]] — hub.
- [[api-orders-attributes]] — field-by-field reference for the PATCH payloads.
- [[api-orders-side-effects]] — the cascade + full failure catalogue.
- [[json-api-v2]] — auth, headers, status codes.
- [[api-order-fulfillment]] — the `/fulfill` action target resource.
- [[order-processing-pipeline]] — what a status PATCH runs end to end.
- [[orders-history]] — the `api2` audit entry to verify after a PATCH.
- [[orders-add]] / [[orders-archive]] — admin-panel flows for the blocked POST / DELETE verbs.

## Open questions

- Add a worked example of a multi-status-boundary PATCH (e.g. crossing `pending → paid → fulfilled → completed` via auto-promotion) once the webhook-fan-out behaviour is confirmed on [[api-orders-side-effects]]. `(verify)`
