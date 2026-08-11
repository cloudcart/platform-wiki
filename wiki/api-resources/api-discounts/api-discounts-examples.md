---
type: api-resource
resource_path: /api/v2/discounts
http_methods: [GET, POST, PATCH, DELETE]
related_entity: discount
related_features: [marketing-discounts, marketing-discounts-flat, marketing-discounts-percent, marketing-discounts-shipping, marketing-discounts-fixed, marketing-discounts-code-pro]
aliases: ["Discounts API examples", "discounts curl examples", "discounts testing checklist", "discounts request response payloads"]
tags: [api, json-api-v2, discounts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 8
---
# Discounts API — worked examples & testing checklist

> Part of [[api-discounts]]. See the hub for the other aspects (attributes & target object, types & validation, side effects).

## Purpose

This aspect holds the **runnable curl requests**, the **JSON response shapes**, the **common 422 error payloads**, and the **end-to-end CRUD testing checklist** for the `discounts` resource. For the field meanings see [[api-discounts-attributes]]; for the validation rules behind the 422s see [[api-discounts-types]].

## Endpoint

- **URL base:** `<store-host>/api/v2/discounts/`
- **Methods covered here:** all — `GET`, `POST`, `PATCH /{id}`, `DELETE /{id}`.

All examples use `<store-host>` for the merchant store domain and `<YOUR_API_KEY>` for the API key. Replace numeric IDs with real values from your store. Base URL, auth, headers: see [[json-api-v2]].

## Attributes

These examples exercise the attributes documented on [[api-discounts-attributes]] — `name`, `discount_type`, `date_start` / `date_end`, `type_value`, `order_over`, `active`, and the `target` object.

## Relationships

No JSON-API relationships exist on this resource, so none of the examples use `?include=`. Child-record examples live on the companion resources: [[api-discount-codes]], [[api-discount-codes-pro]], [[api-product-to-discount]].

## Filtering & sorting

The GET example below filters by `filter[discount_type]` and sorts by `sort=-created_at`. Full filter / sort reference: see [[api-discounts-side-effects]].

## Side effects

Each POST / PATCH / DELETE below fires the webhook + regeneration + uses-recompute pipeline documented on [[api-discounts-side-effects]].

### Example requests

#### GET — list percent discounts, newest first

```bash
curl -X GET 'https://<store-host>/api/v2/discounts?filter[discount_type]=percent&sort=-created_at&page[size]=10' \
  -H 'X-CloudCart-ApiKey: <YOUR_API_KEY>' \
  -H 'Accept: application/vnd.api+json'
```

Expected: `200 OK`.

#### POST — create a flat discount (50 EUR off cart-wide)

```bash
curl -X POST 'https://<store-host>/api/v2/discounts' \
  -H 'X-CloudCart-ApiKey: <YOUR_API_KEY>' \
  -H 'Content-Type: application/vnd.api+json' \
  -H 'Accept: application/vnd.api+json' \
  -d '{
    "data": {
      "type": "discounts",
      "attributes": {
        "name": "Spring 50 EUR off",
        "discount_type": "flat",
        "date_start": "2026-06-01",
        "date_end": "2026-06-30",
        "type_value": 5000,
        "active": "yes",
        "target": { "type": "all" }
      }
    }
  }'
```

Expected: `201 Created`.

#### POST — create a percent discount (10% on selected products)

```bash
curl -X POST 'https://<store-host>/api/v2/discounts' \
  -H 'X-CloudCart-ApiKey: <YOUR_API_KEY>' \
  -H 'Content-Type: application/vnd.api+json' \
  -H 'Accept: application/vnd.api+json' \
  -d '{
    "data": {
      "type": "discounts",
      "attributes": {
        "name": "10% off Summer SKUs",
        "discount_type": "percent",
        "date_start": "2026-06-01",
        "date_end": "2026-08-31",
        "type_value": 10,
        "active": "yes",
        "target": {
          "type": "product",
          "products": [101, 102, 103]
        }
      }
    }
  }'
```

Expected: `201 Created`.

#### POST — create a free-shipping discount (order ≥ 100 EUR)

```bash
curl -X POST 'https://<store-host>/api/v2/discounts' \
  -H 'X-CloudCart-ApiKey: <YOUR_API_KEY>' \
  -H 'Content-Type: application/vnd.api+json' \
  -H 'Accept: application/vnd.api+json' \
  -d '{
    "data": {
      "type": "discounts",
      "attributes": {
        "name": "Free shipping over 100 EUR",
        "discount_type": "shipping",
        "date_start": "2026-06-01",
        "order_over": 10000,
        "active": "yes",
        "target": { "type": "order_over" }
      }
    }
  }'
```

Expected: `201 Created`.

#### POST — create a Fixed-price parent (per-variant overrides added later)

```bash
curl -X POST 'https://<store-host>/api/v2/discounts' \
  -H 'X-CloudCart-ApiKey: <YOUR_API_KEY>' \
  -H 'Content-Type: application/vnd.api+json' \
  -H 'Accept: application/vnd.api+json' \
  -d '{
    "data": {
      "type": "discounts",
      "attributes": {
        "name": "MSRP overrides 2026-Q3",
        "discount_type": "fixed",
        "date_start": "2026-07-01",
        "date_end": "2026-09-30",
        "active": "yes"
      }
    }
  }'
```

Expected: `201 Created`. Then attach per-variant prices via [[api-product-to-discount]].

#### POST — create a Code PRO parent (child codes added later)

```bash
curl -X POST 'https://<store-host>/api/v2/discounts' \
  -H 'X-CloudCart-ApiKey: <YOUR_API_KEY>' \
  -H 'Content-Type: application/vnd.api+json' \
  -H 'Accept: application/vnd.api+json' \
  -d '{
    "data": {
      "type": "discounts",
      "attributes": {
        "name": "Influencer codes Q3",
        "discount_type": "code-pro",
        "date_start": "2026-07-01",
        "active": "yes"
      }
    }
  }'
```

Expected: `201 Created`. Then attach child codes via [[api-discount-codes-pro]].

#### PATCH — toggle `active` off

```bash
curl -X PATCH 'https://<store-host>/api/v2/discounts/42' \
  -H 'X-CloudCart-ApiKey: <YOUR_API_KEY>' \
  -H 'Content-Type: application/vnd.api+json' \
  -H 'Accept: application/vnd.api+json' \
  -d '{
    "data": {
      "type": "discounts",
      "id": "42",
      "attributes": { "active": "no" }
    }
  }'
```

Expected: `200 OK`.

#### DELETE

```bash
curl -X DELETE 'https://<store-host>/api/v2/discounts/42' \
  -H 'X-CloudCart-ApiKey: <YOUR_API_KEY>' \
  -H 'Accept: application/vnd.api+json'
```

Expected: `204 No Content`.

### Example responses

#### GET collection (`200 OK`)

```json
{
  "data": [
    {
      "type": "discounts",
      "id": "42",
      "attributes": {
        "name": "10% off Summer SKUs",
        "discount_type": "percent",
        "date_start": "2026-06-01",
        "date_end": "2026-08-31",
        "type_value": 10,
        "order_over": null,
        "max_uses": null,
        "code": null,
        "code_apply": "0",
        "active": "yes",
        "timer_list": "0",
        "timer_details": "0",
        "is_container": "0",
        "discount_amount_type_in_label": "dont_change",
        "uses": 17,
        "settings": "product",
        "created_at": "2026-05-26T10:14:02+00:00",
        "updated_at": "2026-06-04T07:22:11+00:00"
      },
      "links": { "self": "https://<store-host>/api/v2/discounts/42" }
    },
    {
      "type": "discounts",
      "id": "41",
      "attributes": {
        "name": "Spring 50 EUR off",
        "discount_type": "flat",
        "date_start": "2026-06-01",
        "date_end": "2026-06-30",
        "type_value": 5000,
        "order_over": null,
        "max_uses": null,
        "code": null,
        "code_apply": "0",
        "active": "yes",
        "uses": 4,
        "settings": "all",
        "created_at": "2026-05-25T09:01:55+00:00",
        "updated_at": "2026-05-25T09:01:55+00:00"
      }
    }
  ],
  "meta": {
    "page": { "current-page": 1, "per-page": 10, "from": 1, "to": 2, "total": 2, "last-page": 1 }
  },
  "links": {
    "first": "https://<store-host>/api/v2/discounts?page[number]=1&page[size]=10",
    "last": "https://<store-host>/api/v2/discounts?page[number]=1&page[size]=10"
  }
}
```

#### POST 201 created (echoes server-generated fields)

```json
{
  "data": {
    "type": "discounts",
    "id": "67",
    "attributes": {
      "name": "10% off Summer SKUs",
      "discount_type": "percent",
      "date_start": "2026-06-01",
      "date_end": "2026-08-31",
      "type_value": 10,
      "active": "yes",
      "uses": 0,
      "settings": "product",
      "created_at": "2026-06-05T08:42:17+00:00",
      "updated_at": "2026-06-05T08:42:17+00:00"
    },
    "links": { "self": "https://<store-host>/api/v2/discounts/67" }
  }
}
```

#### 422 — missing `type_value` for percent

```json
{
  "errors": [
    {
      "status": "422",
      "title": "Unprocessable Entity",
      "detail": "The type value field is required when discount type is percent.",
      "source": { "pointer": "/data/attributes/type_value" }
    }
  ]
}
```

#### 422 — `order_over` target without `order_over` value

```json
{
  "errors": [
    {
      "status": "422",
      "title": "Unprocessable Entity",
      "detail": "The order over field is required when target.type is order_over.",
      "source": { "pointer": "/data/attributes/order_over" }
    }
  ]
}
```

#### 422 — `code` set on a `fixed` parent

```json
{
  "errors": [
    {
      "status": "422",
      "title": "Unprocessable Entity",
      "detail": "Cannot use discount code when discount type is fixed.",
      "source": { "pointer": "/data/attributes/code" }
    }
  ]
}
```

#### 422 — invalid `target.type`

```json
{
  "errors": [
    {
      "status": "422",
      "title": "Unprocessable Entity",
      "detail": "Invalid target type. List of valid target types: all, product, category, vendor, category_vendor, selection, order_over",
      "source": { "pointer": "/data/attributes/target.type" }
    }
  ]
}
```

#### 422 — invalid `target.products` IDs

```json
{
  "errors": [
    {
      "status": "422",
      "title": "Unprocessable Entity",
      "detail": "Invalid target products. No products found with ids: 7777, 8888",
      "source": { "pointer": "/data/attributes/target.products" }
    }
  ]
}
```

## Testing checklist

End-to-end sequence for an AI agent to verify CRUD parity against a real store:

```
1. GET /api/v2/discounts?page[size]=5
   → expect 200, confirm read access.
2. POST /api/v2/discounts with discount_type=percent, target={type:all}, type_value=10, date_start=<today>
   → expect 201, capture {id}.
3. GET /api/v2/discounts/{id}
   → expect 200; verify name, discount_type, type_value, target match the POST.
4. PATCH /api/v2/discounts/{id} with attributes.active="no"
   → expect 200.
5. GET /api/v2/discounts/{id}
   → expect 200; verify active="no".
6. POST /api/v2/discounts with discount_type=percent BUT no type_value
   → expect 422 with errors[0].source.pointer = /data/attributes/type_value.
7. POST /api/v2/discounts with discount_type=fixed AND code="FOO"
   → expect 422 detail "Cannot use discount code when discount type is fixed."
     with errors[0].source.pointer = /data/attributes/code.
     (Note: the code-on-non-allowed-type rule rejects ONLY fixed / code-pro; flat / percent / shipping accept a code.)
8. POST /api/v2/discounts with discount_type=shipping, target={type:order_over}, no order_over field
   → expect 422 with errors[0].source.pointer = /data/attributes/order_over.
9. DELETE /api/v2/discounts/{id}
   → expect 204.
10. GET /api/v2/discounts/{id}
    → expect 404.
```

Optional follow-ups:

- POST a parent with `discount_type=code-pro` and verify the returned record is suitable as the `discount_id` parent for [[api-discount-codes-pro]].
- POST a parent with `discount_type=fixed` and verify it is the required parent type for [[api-product-to-discount]] (non-fixed parents return 422 there).

## Equivalent UI

- [[marketing-discounts]] — admin-panel CRUD that mirrors these requests.
- [[marketing-discounts-flat]] / [[marketing-discounts-percent]] / [[marketing-discounts-shipping]] — per-type edit screens corresponding to the POST examples.
- [[discount]] — entity attribute reference.

## Related

- [[api-discounts]] — hub.
- [[json-api-v2]] — API hub: auth headers used in every example.
- [[api-discounts-attributes]] — field meanings behind the payloads.
- [[api-discounts-types]] — validation rules behind the 422 examples.
- [[api-product-to-discount]] — Fixed-parent follow-up.
- [[api-discount-codes-pro]] — Code-PRO-parent follow-up.

## Open questions

None.
