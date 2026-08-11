---
type: api-resource
resource_path: /api/v2/discount-codes-pro
http_methods: [GET, POST, PATCH, DELETE]
related_entity: discount-code
related_features: [marketing-discounts-code-pro, marketing-discounts-code-pro-generator]
aliases: ["Discount Codes PRO API examples", "Code PRO API curl examples", "discount-codes-pro filtering", "discount-codes-pro testing checklist"]
tags: [api, json-api-v2, discounts, code-pro]
plan_gates: ["discount-code-pro"]
created: 2026-06-10
updated: 2026-06-10
source_count: 7
---
# Discount Codes PRO API — filtering, examples & testing checklist

> Part of [[api-discount-codes-pro]]. See the hub for the other aspects (attributes, generator, side effects).

## Purpose

This aspect is the **query reference + worked examples** for the `discount-codes-pro` resource: how to filter, sort, and include; copy-paste curl requests for every method; representative response payloads; and an end-to-end testing checklist an AI agent can run. For field semantics see [[api-discount-codes-pro-attributes]]; for the bulk generator see [[api-discount-codes-pro-generator]].

## Endpoint

All examples use `<store-host>` and `<YOUR_API_KEY>`. The parent Code PRO Discount (`discount_type = code-pro`) must already exist on [[api-discounts]] — use its id as `discount_id`. Every write request must use `Content-Type: application/vnd.api+json`. Base URL, auth, headers: see [[json-api-v2]].

## Attributes

Field-level semantics are documented on [[api-discount-codes-pro-attributes]]. The examples below show how those attributes appear on the wire in requests and responses.

## Relationships

The `discount` relationship is rendered in every response (see the `relationships.discount` blocks below) and set at create via the `discount_id` attribute. Definition: see [[api-discount-codes-pro-attributes]].

## Filtering & sorting

**Filtering** — `filter[discount_id]` is named in the validator. Plus the framework auto-allows `filter[<column>]` for every column on the `discounts_code_pro` table — useful: `filter[code]`, `filter[active]`, `filter[date_start]`, `filter[date_end]`, `filter[geo_zone_id]`, `filter[max_uses]`. Equality only.

**Sorting** — `id`, `name`, `code`, `active`, `date_start`, `date_end`, `uses`, `created_at`, `updated_at`; prefix with `-` for descending.

**Include paths** — `discount` (auto-merged from the schema's `$relationships` list).

**Sparse-field append values** — none. The schema's `$appends = ['conditions']` is always included in the response, but `?append[discount-codes-pro]=...` returns 422.

## Example requests

### GET — list all codes under one parent

```bash
curl -X GET 'https://<store-host>/api/v2/discount-codes-pro?filter[discount_id]=42&page[size]=20&sort=-created_at' \
  -H 'X-CloudCart-ApiKey: <YOUR_API_KEY>' \
  -H 'Accept: application/vnd.api+json'
```

Expected: `200 OK`.

### POST — create a single Code PRO code with conditions + customer-group restriction

```bash
curl -X POST 'https://<store-host>/api/v2/discount-codes-pro' \
  -H 'X-CloudCart-ApiKey: <YOUR_API_KEY>' \
  -H 'Content-Type: application/vnd.api+json' \
  -H 'Accept: application/vnd.api+json' \
  -d '{
    "data": {
      "type": "discount-codes-pro",
      "attributes": {
        "discount_id": 42,
        "code": "INFLUENCER1",
        "name": "Anna 15% off",
        "active": 1,
        "date_start": "2026-06-01",
        "date_end": "2026-09-30",
        "max_uses": 100,
        "maxused_user": 1,
        "code_apply": 1,
        "apply_regular_price": 0,
        "only_customer": 0,
        "customer_groups": [1],
        "conditions": [
          { "type": "percent", "setting": "all", "value": 1500 }
        ]
      }
    }
  }'
```

Expected: `201 Created`. `value: 1500` = 15.00% (percent × 100).

### POST /generate — random and range modes

Both bulk-generator modes return `200 OK` with a collection of new codes. Request bodies, validation, and the leading-zero / collision rules are documented on [[api-discount-codes-pro-generator]].

### PATCH — toggle a single code off

```bash
curl -X PATCH 'https://<store-host>/api/v2/discount-codes-pro/501' \
  -H 'X-CloudCart-ApiKey: <YOUR_API_KEY>' \
  -H 'Content-Type: application/vnd.api+json' \
  -H 'Accept: application/vnd.api+json' \
  -d '{
    "data": {
      "type": "discount-codes-pro",
      "id": "501",
      "attributes": { "active": 0 }
    }
  }'
```

Expected: `200 OK`.

### DELETE

```bash
curl -X DELETE 'https://<store-host>/api/v2/discount-codes-pro/501' \
  -H 'X-CloudCart-ApiKey: <YOUR_API_KEY>' \
  -H 'Accept: application/vnd.api+json'
```

Expected: `204 No Content`.

## Example responses

### GET single (`200 OK`)

```json
{
  "data": {
    "type": "discount-codes-pro",
    "id": "501",
    "attributes": {
      "code": "INFLUENCER1",
      "name": "Anna 15% off",
      "active": 1,
      "date_start": "2026-06-01",
      "date_end": "2026-09-30",
      "max_uses": 100,
      "maxused_user": 1,
      "code_apply": 1,
      "apply_regular_price": 0,
      "code_format": null,
      "barcode_prefix": 0,
      "only_customer": 0,
      "geo_zone_id": null,
      "uses": 12,
      "conditions": [
        { "type": "percent", "setting": "all", "value": 1500 }
      ],
      "created_at": "2026-05-26T10:14:02+00:00",
      "updated_at": "2026-06-04T07:22:11+00:00"
    },
    "relationships": {
      "discount": { "data": { "type": "discounts", "id": "42" } }
    },
    "links": { "self": "https://<store-host>/api/v2/discount-codes-pro/501" }
  }
}
```

### POST `201 Created` — same shape with `uses: 0`

A successful create returns the row with `uses: 0` and matching `created_at` / `updated_at` timestamps, and the `discount` relationship pointing at the parent (`type: "discounts"`, `id: "42"`).

### Common 422 errors

```json
{
  "errors": [
    { "status": "422", "title": "Unprocessable Entity",
      "detail": "The discount must be of type code-pro.",
      "source": { "pointer": "/data/attributes/discount_id" } }
  ]
}
```

```json
{
  "errors": [
    { "status": "422", "title": "Unprocessable Entity",
      "detail": "Some of the codes in the specified range already exist.",
      "source": { "pointer": "/data/range_from" } }
  ]
}
```

```json
{
  "errors": [
    { "status": "422", "title": "Unprocessable Entity",
      "detail": "The limit may not be greater than 5000.",
      "source": { "pointer": "/data/limit" } }
  ]
}
```

The 5,000 cap is enforced at the API layer regardless of the merchant's `discount-code-pro-generator` plan-feature value — see [[api-discount-codes-pro-side-effects]].

## Side effects

The examples above trigger the write-time behaviour (uses recompute, transactional link-table rewrites, no dedicated webhook) catalogued on [[api-discount-codes-pro-side-effects]].

## Equivalent UI

- [[marketing-discounts-code-pro]] — admin-panel codes list / per-code edit (mirrors GET / POST / PATCH / DELETE).
- [[marketing-discounts-code-pro-export]] — CSV export of codes + conditions.

## Testing checklist

End-to-end sequence for an AI agent. Requires one parent Code PRO Discount (`discount_type = code-pro`) on [[api-discounts]] — use its id as `<DISCOUNT_ID>`. Also requires a non-code-pro parent id `<OTHER_DISCOUNT_ID>` for the negative test in step 7.

```
1. GET /api/v2/discount-codes-pro?filter[discount_id]=<DISCOUNT_ID>&page[size]=5
   → expect 200; confirm parent-Discount lookup works.
2. POST /api/v2/discount-codes-pro with discount_id=<DISCOUNT_ID>, code="TESTPRO01",
   date_start=<today>, max_uses=10, code_apply=1,
   conditions=[{type:"percent", setting:"all", value:1000}]
   → expect 201, capture {id_single}.
3. GET /api/v2/discount-codes-pro/{id_single}
   → expect 200; verify conditions[].value=1000, code_apply=1.
4. POST /api/v2/discount-codes-pro/generate (random mode) with discount_id=<DISCOUNT_ID>,
   generator_type="random", limit=10, length=12, structure=["alpha","numeric"],
   date_start=<today>, conditions=[{type:"percent", setting:"all", value:1500}]
   → expect 200; collection of 10 rows.
5. POST /api/v2/discount-codes-pro/generate (range mode) with discount_id=<DISCOUNT_ID>,
   generator_type="range", range_from=80000, range_to=80009, date_start=<today>,
   conditions=[{type:"flat", setting:"all", value:500}]
   → expect 200; codes "80000".."80009" inserted.
6. POST /api/v2/discount-codes-pro/generate same range AGAIN
   → expect 422 detail "Some of the codes in the specified range already exist."
     with errors[0].source.pointer = /data/range_from.
7. POST /api/v2/discount-codes-pro with discount_id=<OTHER_DISCOUNT_ID> (non-code-pro parent),
   code="WRONGPRO1", date_start=<today>
   → expect 422 detail "The discount must be of type code-pro."
     with errors[0].source.pointer = /data/attributes/discount_id.
8. POST /api/v2/discount-codes-pro/generate with limit=10000 (above 5,000 cap)
   → expect 422 detail "The limit may not be greater than 5000."
     with errors[0].source.pointer = /data/limit.
9. PATCH /api/v2/discount-codes-pro/{id_single} with attributes.active=0
   → expect 200.
10. GET /api/v2/discount-codes-pro/{id_single}
    → expect 200; verify active=0.
11. DELETE /api/v2/discount-codes-pro/{id_single}
    → expect 204.
12. GET /api/v2/discount-codes-pro/{id_single}
    → expect 404.
```

## Related

- [[api-discount-codes-pro]] — hub.
- [[api-discount-codes-pro-attributes]] — field semantics behind these payloads.
- [[api-discount-codes-pro-generator]] — the `/generate` request bodies.
- [[json-api-v2]] — API hub.
- [[api-discounts]] — parent Code PRO Discount endpoint.

## Open questions

None.
