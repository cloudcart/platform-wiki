---
type: api-resource
resource_path: /api/v2/webhooks
http_methods: [GET, POST, PATCH, DELETE]
related_entity: webhook
related_features: [settings-hooks, settings-api-keys]
aliases: ["Webhooks API examples", "Webhook curl examples", "Webhook 422 errors", "Webhook testing checklist", "Webhook plan limit", "Webhook subscription cap"]
tags: [api, json-api-v2, infra, webhooks, examples]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---

> Part of [[api-webhooks]]. See the hub for the other aspects (CRUD surface, event catalog, delivery contract).

# Webhooks API — examples, errors & plan gating (JSON-API v2)

## Purpose

Copy-paste curl requests + JSON responses for every operation, the common-422 error table, the plan-feature gating rules (subscription cap, admin-permission key), and a 7-step testing checklist. Read this aspect to **try the endpoint** and to **decode an error**. The field semantics behind these examples are in [[api-webhooks-crud]]; the accepted events are in [[api-webhooks-event-catalog]].

## Endpoint

All examples below hit `/api/v2/webhooks` (collection) or `/api/v2/webhooks/{id}` (single) using `<store-host>` and `<YOUR_API_KEY>`. The method table is in [[api-webhooks-crud]].

## Attributes

The examples exercise `url`, `event`, `active`, `new_version`, `request_headers`, and `api_key_id` — full reference in [[api-webhooks-crud]]; the accepted `event` values in [[api-webhooks-event-catalog]].

### Example requests

#### GET collection

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/webhooks?page[size]=20&sort=event"
```

#### POST create — valid event from the 20-event catalogue

```bash
curl -s -X POST \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/webhooks" \
     -d '{
       "data": {
         "type": "webhooks",
         "attributes": {
           "url": "https://integration.example.com/cc/order-created",
           "event": "order.created",
           "active": "yes",
           "new_version": 1
         }
       }
     }'
```

When `api_key_id` is omitted, the adapter auto-fills with the **first** API key on the site. Multi-key stores should send `api_key_id` explicitly.

#### POST with custom headers

```bash
curl -s -X POST \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/webhooks" \
     -d '{
       "data": {
         "type": "webhooks",
         "attributes": {
           "url": "https://integration.example.com/cc/product-updated",
           "event": "product.updated",
           "request_headers": {
             "X-Signature": "hmac-sha256-token-abc",
             "X-Tenant": "merchant-7",
             "Authorization": "Bearer eyJhbGciOi..."
           }
         }
       }
     }'
```

**Headers are FULLY REPLACED on every save** (POST AND PATCH) — all existing header rows for the webhook are deleted and fresh ones created from the request. PATCHing one header in isolation drops the others — always re-send the full headers map on update (see [[api-webhooks-crud]]).

#### PATCH update headers (full-replace)

```bash
curl -s -X PATCH \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/webhooks/14" \
     -d '{
       "data": {
         "type": "webhooks",
         "id": "14",
         "attributes": {
           "request_headers": {
             "X-Signature": "hmac-sha256-token-NEW",
             "X-Tenant": "merchant-7",
             "Authorization": "Bearer eyJhbGciOi...",
             "X-Trace-Id": "req-1234"
           }
         }
       }
     }'
```

#### PATCH attempt to change `api_key_id` — 422

```bash
curl -s -X PATCH \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/webhooks/14" \
     -d '{
       "data": {
         "type": "webhooks",
         "id": "14",
         "attributes": { "api_key_id": 2 }
       }
     }'
```

`api_key_id` is **read-only on PATCH**. To rebind, DELETE + POST.

#### DELETE

```bash
curl -s -X DELETE \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/webhooks/14"
```

(Returns 204.)

### Example responses

#### GET collection success

```json
{
  "data": [
    {
      "type": "webhooks",
      "id": "14",
      "attributes": {
        "url": "https://integration.example.com/cc/order-created",
        "event": "order.created",
        "active": "yes",
        "new_version": 1,
        "request_headers": { "X-Signature": "hmac-sha256-token-abc" },
        "created_at": "2026-05-12T08:30:00+00:00",
        "updated_at": "2026-05-30T11:02:14+00:00"
      }
    }
  ],
  "meta": {
    "page": { "current-page": 1, "per-page": 20, "from": 1, "to": 1, "total": 1, "last-page": 1 }
  }
}
```

#### POST 201 Created

```json
{
  "data": {
    "type": "webhooks",
    "id": "14",
    "attributes": {
      "url": "https://integration.example.com/cc/order-created",
      "event": "order.created",
      "active": "yes",
      "new_version": 1,
      "request_headers": {}
    }
  }
}
```

#### 422 — unknown event (NOT in the 20-event catalogue)

```
HTTP 422 Unprocessable Entity
{"errors":[{"status":"422","source":{"pointer":"/data/attributes/event"},"detail":"List of valid events: category.created, category.updated, category.deleted, vendor.created, vendor.updated, vendor.deleted, product.created, product.updated, product.deleted, discount.created, discount.updated, discount.deleted, customer.created, customer.updated, customer.deleted, order.created, order.updated, subscriber.created, subscriber.updated, subscriber.deleted"}]}
```

`order.deleted` is commented out of the catalogue — sending it returns the 422 above (20 events, not 21). See [[api-webhooks-event-catalog]].

### Common 422 cases

| Condition | `source.pointer` | `detail` |
|---|---|---|
| Missing `url` on POST | `/data/attributes/url` | *"The url field is required"* |
| `url` not a valid URL | `/data/attributes/url` | *"The url format is invalid"* |
| Missing `event` on POST | `/data/attributes/event` | *"The event field is required"* |
| `event` not in the supported set | `/data/attributes/event` | *"List of valid events: category.created, …, subscriber.deleted"* |
| PATCH attempts to change `api_key_id` | `/data/attributes/api_key_id` | *"The api key id field is read-only"* |
| Delete rejected by model layer | n/a (top-level error) | *"Not Deletable"* with the underlying domain message. |
| Plan-expired (402, not 422) | n/a | *"Payment Required"* — the merchant's plan is past-due. |
| Webhook subscription cap exceeded | n/a | Plan-feature limit response — see Plan-feature gating below. |

## Relationships

None — the examples never use `?include=`, since no relationships are exposed. See [[api-webhooks-crud]].

## Filtering & sorting

The GET-collection example uses `sort=event` and `page[size]=20`. Add `filter[active]=0` to list disabled subscriptions, `filter[event]=order.created` to list by event — full rules in [[api-webhooks-crud]].

## Side effects

### Plan-feature gating

- **Per-plan limit on number of webhook subscriptions** — the `hooks` plan-feature counter caps how many active webhook rows a store may hold. Hitting the cap returns 422 at POST with a plan-feature-exceeded message (or 402 if the plan itself is past-due). See [[plan-vs-feature-pack]].
- **Cross-resource webhook firing from JSON-API v2 writes** — historically, REST API writes did NOT always fire `product.*` / `customer.*` / `category.*` webhooks (admin-panel saves did). This is gradually being closed; verify on a test store per resource. Order events are well-established as firing on every save regardless of source.
- **`marketing.hooks` admin permission** — admin-panel CRUD on [[settings-hooks]] is gated by this key. API-key permissioning is **separate** — any active API key has full access to this endpoint.

### Testing checklist

1. `GET /webhooks` — confirm read.
2. `POST /webhooks` with `event=order.created` + a valid receiver URL — capture `data.id`.
3. `POST /webhooks` with `event=order.deleted` — expect 422 (`order.deleted` is commented out of the 20-event catalogue).
4. `PATCH /webhooks/{id}` setting `api_key_id` — expect 422 *"The api key id field is read-only"*.
5. `PATCH /webhooks/{id}` with `request_headers` — verify ALL previously stored headers are replaced (NOT merged). Re-GET to confirm the header map matches the request exactly.
6. Trigger the subscribed event (e.g., create a test order for `order.created`) and verify the receiver gets `POST <url>` with `Content-Type: application/json`, the `X-CloudCart-ApiKey` header, and any custom `request_headers` (see [[api-webhooks-delivery-contract]]).
7. `DELETE /webhooks/{id}` — expect 204.

## Equivalent UI

- [[settings-hooks]] — the admin-panel CRUD page; same validation and error messages.
- [[settings-api-keys]] — API keys page used to obtain `<YOUR_API_KEY>`.

## Related

- [[api-webhooks]] — hub.
- [[json-api-v2]] — API hub (auth, status codes, pagination).
- [[settings-hooks]] — admin-panel surface.
- [[settings-api-keys]] — API keys.
- [[plan-vs-feature-pack]] — plan-feature limit model behind the subscription cap.
- [[webhook]] — entity reference.

## Open questions

- **Webhook subscription cap value** — the exact per-plan `hooks` counter limit is not enumerated here; confirm against the plan-feature matrix. (verify)
- **Cross-resource firing from REST writes** — whether JSON-API v2 writes fire non-order webhooks is unconfirmed; verify per resource on a test store. (verify)
