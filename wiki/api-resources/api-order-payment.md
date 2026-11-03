---
type: api-resource
resource_path: /api/v2/order-payment
http_methods: [GET]
related_entity: order
related_features: [orders-details, orders-payment-mark-paid, orders-payment-capture, orders-payment-refund, orders-payment-manual]
aliases: ["Order payment API", "Payment record API", "JSON-API v2 order-payment", "/order-payment"]
tags: [api, json-api-v2, orders, payments]
plan_gates: []
created: 2026-05-26
updated: 2026-06-05
source_count: 3
---
# Order Payment (JSON-API v2)

## Purpose

The `order-payment` resource is the **read-only view of the payment record on every order** — the chosen payment provider, the amount, the provider's external reference IDs, the payment status (pending / authorized / completed / refunded / voided), and any provider-specific metadata. External integrations use it to reconcile orders against external payment-gateway accounts, pull provider reference IDs into accounting systems, and surface payment status in ERP dashboards.

Payment records are not manipulated through this endpoint. Capture, refund, mark-paid, void, manual-payment-add, and similar lifecycle actions go through the admin panel (see [[orders-payment-capture]], [[orders-payment-refund]], [[orders-payment-mark-paid]], [[orders-payment-manual]]) or arrive as gateway callbacks. The API exposes the resulting record for reading only.

## Endpoint

| Method | Path | Status |
|---|---|---|
| `GET` | `/api/v2/order-payment` | List every payment row across every order on the store. Supports `filter[start_date]` / `filter[end_date]`. |
| `GET` | `/api/v2/order-payment/{id}` | Fetch a single payment row. |
| `POST` / `PATCH` / `DELETE` | `/api/v2/order-payment[/{id}]` | **GET only — returns 405 Method Not Allowed.** Payment actions (capture, refund, mark-paid, manual-add, void) are admin-panel-only flows. |

No app install or plan feature gates this resource. To scope the response to a single order, filter by `order_id` (auto-merged from the column list) or fetch via the parent with `?include=payment` on [[api-orders]].

## Attributes

All attributes are returned by GET only.

| Attribute | Type | Notes |
|---|---|---|
| `order_id` | integer | Parent order. |
| `provider` | string | Provider machine key (e.g., `stripe`, `paypal`, `easypay`, `cod`). |
| `provider_name` | string | Provider display name snapshot. |
| `amount` | integer | Payment amount in store currency minor units. |
| `provider_reference_id` | string | The gateway's external transaction / order ID (used to reconcile with the provider's dashboard). |
| `down_payment` | number | If a partial / down-payment scheme applies (subscription orders, advance-pay). |
| `allow_capture_authorization` | bool / string | Whether the gateway supports a later capture call against the authorized amount (see [[orders-payment-capture]]). |
| `status` | string | Provider-side status (e.g., `pending`, `completed`, `authorized`, `refunded`, `voided`). |
| `payment_status` | string | Cross-provider normalised status (see [[payment-status]]). |
| `provider_data` | array (appended) | Provider-specific payload — provider reference IDs, capture amounts, authorize amounts, redirect URLs, etc. Surfaced via the appended `provider_data` accessor. |
| `date_created`, `date_modified` | datetime | Lifecycle timestamps. |

The schema declares no hidden fields. `provider_data` is the one appended accessor.

**Sparse-field append values:** none configured — `provider_data` is appended by default.

## Relationships

| Name | Cardinality | Type | Notes |
|---|---|---|---|
| `order` | belongsTo | order | Parent order. |

**Allowed include paths:** `order`.

## Filtering & sorting

**Allowed filtering parameters:**

| Parameter | Type | Behaviour |
|---|---|---|
| `filter[start_date]` | datetime | Internally rewritten to `WHERE date_added >= ?` on the payment's `date_added` column. |
| `filter[end_date]` | datetime | Internally rewritten to `WHERE date_added <= ?` on the payment's `date_added` column. |
| `filter[<any column>]` | per column | Framework auto-merged exact-equality filters on any column (e.g., `filter[order_id]`, `filter[provider]`, `filter[status]`). No comparison operators. |

**Allowed sort parameters:** none declared — natural insertion order applies.

**Pagination:** standard JSON:API `page[number]` / `page[size]` (1–100, default 20).

## Side effects

None. **`order-payment` is read-only — POST / PATCH / DELETE return 405 Method Not Allowed.** The actual payment lifecycle is driven by:

- **Storefront checkout** — initial payment record creation when the customer completes payment.
- **Gateway callbacks / webhooks** — status updates from the provider (e.g., authorization → captured) flow through the platform's payment-provider mechanism (see [[payment-provider-mechanism]]).
- **Admin-panel actions** — [[orders-payment-mark-paid]], [[orders-payment-capture]] (gateway-supported only), [[orders-payment-refund]], [[orders-payment-manual]].

A status change on the parent [[api-orders]] resource can cascade into the payment record indirectly — for example moving to a negative status (cancelled, voided, refunded) auto-cancels open authorization holds across all supported gateways. See [[api-orders]] *Side effects* and [[order-processing-pipeline]] for the full cascade.

## Example requests

All examples use `<store-host>` (e.g., `mystore.cloudcart.net`) and `<YOUR_API_KEY>` (64-char uppercase).

### GET collection (date range)

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-payment?filter[start_date]=2026-06-01&filter[end_date]=2026-06-30&page[size]=20"
```

### GET collection scoped to one order

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-payment?filter[order_id]=1042"
```

### GET single

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-payment/801?include=order"
```

### POST / PATCH / DELETE blocked (405)

```bash
curl -s -X POST \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-payment" \
     -d '{"data":{"type":"order-payment","attributes":{"provider":"stripe","amount":12990}}}'
```

```bash
curl -s -X PATCH \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-payment/801" \
     -d '{"data":{"type":"order-payment","id":"801","attributes":{"status":"completed"}}}'
```

```bash
curl -s -X DELETE \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-payment/801"
```

## Example responses

### GET collection success

```json
{
  "data": [
    {
      "type": "order-payment",
      "id": "801",
      "attributes": {
        "order_id": 1042,
        "provider": "stripe",
        "provider_name": "Stripe",
        "amount": 12990,
        "provider_reference_id": "pi_3PaXyZ2eZvKYlo2C0qK8s5Lp",
        "down_payment": 0,
        "allow_capture_authorization": "no",
        "status": "completed",
        "payment_status": "completed",
        "provider_data": {
          "authorize_amount": 12990,
          "captured_amount": 12990,
          "currency": "BGN"
        },
        "date_created": "2026-06-04 14:22:11",
        "date_modified": "2026-06-04 14:22:14"
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

1. `GET /order-payment?filter[start_date]=2026-06-01&filter[end_date]=2026-06-30&page[size]=5` — confirm date-range read.
2. `GET /order-payment/{id}?include=order` — verify shape (provider_data appended by default).
3. `GET /order-payment?filter[provider]=stripe` — verify provider filter.
4. `POST /order-payment` — verify 405.
5. `PATCH /order-payment/{id}` — verify 405.
6. `DELETE /order-payment/{id}` — verify 405.
7. Confirm the resource cannot be modified directly — payment actions go through the admin-panel flows ([[orders-payment-mark-paid]], [[orders-payment-capture]], [[orders-payment-refund]]) or the gateway's own callbacks via [[payment-provider-mechanism]].

## Equivalent UI

- [[orders-payment-mark-paid]] — manual "mark as paid" action.
- [[orders-payment-capture]] — capture an authorized payment (gateway-supported only).
- [[orders-payment-refund]] — refund flow.
- [[orders-payment-manual]] — manual payment entry (COD confirmation, bank-transfer reconciliation).
- [[orders-details]] — single-order detail view showing the payment record inline.

## Related

- [[json-api-v2]] — API hub.
- [[api-orders]] — parent order resource (`?include=payment`).
- [[api-payment-providers]] — payment-provider catalog.
- [[payment-status]] — normalised payment status enum.
- [[payment-provider-mechanism]] — how the gateway lifecycle works.
- [[settings-hooks]] — webhooks subscribed to `order.paid`, `order.refunded`, etc.
- [[order-processing-pipeline]] — cascade when the parent order's status changes.

## Open questions

- Confirm whether `provider_data` is filtered to exclude sensitive fields (`card_token`, raw `cvv_check` results, etc.) before being surfaced via the API, or whether the full provider payload is returned.
- Verify whether webhook listeners (`order.paid`, `order.refunded`) fire on the underlying payment-status changes regardless of whether the change was driven by gateway callback vs admin-panel action (expected: yes, because events fire from the model layer).
