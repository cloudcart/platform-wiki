---
type: api-resource
resource_path: /api/v2/discount-codes
http_methods: [GET, POST, PATCH, DELETE]
related_entity: discount-code
related_features: [marketing-discounts-codes, marketing-discounts]
aliases: ["Discount Codes API examples", "Container codes curl examples", "discount-codes filtering", "discount-codes testing checklist"]
tags: [api, json-api-v2, discounts, container-codes]
plan_gates: ["discount_coupon"]
created: 2026-06-10
updated: 2026-06-10
source_count: 6
---
# Discount Codes API — filtering, examples & testing checklist

> Part of [[api-discount-codes]]. See the hub for the other aspects (attributes, side effects).

## Purpose

This aspect is the **query reference + worked examples** for the `discount-codes` resource: how to filter and sort; copy-paste curl requests for every method (including both content-type variants of `POST /generate`); representative response payloads; the common 422 errors; and an end-to-end testing checklist an AI agent can run. For field semantics see [[api-discount-codes-attributes]]; for write-time behaviour see [[api-discount-codes-side-effects]].

## Endpoint

All examples use `<store-host>` and `<YOUR_API_KEY>`. The parent Container Discount (a `percent` discount with `is_container = 1`) must already exist on [[api-discounts]] — the Container codes API does not require linking to it. Base URL, auth, headers: see [[json-api-v2]].

## Attributes

The payloads below show `code`, `value` (percent × 100), and `active` on the wire. Field-level semantics: see [[api-discount-codes-attributes]].

## Relationships

No relationship blocks appear in any response — this resource declares none. See [[api-discount-codes]] for the rationale.

## Filtering & sorting

**Filtering** — no named filters declared. The framework auto-allows `filter[<column>]` for every column on the `discount_codes` table — useful: `filter[code]`, `filter[active]`, `filter[value]`, `filter[type]` (always `percent` in practice). Equality only.

**Sorting** — `id`, `created_at`, `updated_at`, `active`, `code`; prefix with `-` for descending.

**Include paths** — none; no relationships declared.

**Sparse-field append values** — none. The schema's `$appends` list is commented out, so `?append[discount-codes]=...` returns 422.

## Example requests

### GET — filter by `value` (find all 10% codes)

```bash
curl -X GET 'https://<store-host>/api/v2/discount-codes?filter[value]=1000&page[size]=10' \
  -H 'X-CloudCart-ApiKey: <YOUR_API_KEY>' \
  -H 'Accept: application/vnd.api+json'
```

Expected: `200 OK`.

### POST — create a single Container code

```bash
curl -X POST 'https://<store-host>/api/v2/discount-codes' \
  -H 'X-CloudCart-ApiKey: <YOUR_API_KEY>' \
  -H 'Content-Type: application/vnd.api+json' \
  -H 'Accept: application/vnd.api+json' \
  -d '{
    "data": {
      "type": "discount-codes",
      "attributes": {
        "code": "SPRING2026X",
        "value": 1000,
        "active": 1
      }
    }
  }'
```

Expected: `201 Created`. `value: 1000` = 10%.

### POST /generate — bulk-generate 100 random 15%-off codes (vnd.api+json)

```bash
curl -X POST 'https://<store-host>/api/v2/discount-codes/generate' \
  -H 'X-CloudCart-ApiKey: <YOUR_API_KEY>' \
  -H 'Content-Type: application/vnd.api+json' \
  -H 'Accept: application/vnd.api+json' \
  -d '{
    "data": {
      "type": "discount-codes",
      "count": 100,
      "value": 1500
    }
  }'
```

Expected: `200 OK` with a collection of the freshly-inserted rows.

### POST /generate — same call with plain `application/json` (also accepted)

The `discount-codes` resource is registered with `contentNegotiator('json')`, so `application/json` is accepted on `POST /generate` (and on POST / PATCH on individual codes). This is the ONLY discount resource with this relaxation; [[api-discount-codes-pro]] still requires `application/vnd.api+json`.

```bash
curl -X POST 'https://<store-host>/api/v2/discount-codes/generate' \
  -H 'X-CloudCart-ApiKey: <YOUR_API_KEY>' \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json' \
  -d '{
    "data": {
      "type": "discount-codes",
      "count": 100,
      "value": 1500
    }
  }'
```

Expected: `200 OK`. Same response shape as the `application/vnd.api+json` variant.

### PATCH — deactivate one code (pre-burn before send)

```bash
curl -X PATCH 'https://<store-host>/api/v2/discount-codes/9001' \
  -H 'X-CloudCart-ApiKey: <YOUR_API_KEY>' \
  -H 'Content-Type: application/vnd.api+json' \
  -H 'Accept: application/vnd.api+json' \
  -d '{
    "data": {
      "type": "discount-codes",
      "id": "9001",
      "attributes": { "active": 0 }
    }
  }'
```

Expected: `200 OK`.

### DELETE

```bash
curl -X DELETE 'https://<store-host>/api/v2/discount-codes/9001' \
  -H 'X-CloudCart-ApiKey: <YOUR_API_KEY>' \
  -H 'Accept: application/vnd.api+json'
```

Expected: `204 No Content`.

## Example responses

### GET collection (`200 OK`)

```json
{
  "data": [
    {
      "type": "discount-codes",
      "id": "9001",
      "attributes": {
        "code": "SPRING2026X",
        "value": 1000,
        "active": 1,
        "created_at": "2026-06-05T08:12:00+00:00",
        "updated_at": "2026-06-05T08:12:00+00:00"
      },
      "links": { "self": "https://<store-host>/api/v2/discount-codes/9001" }
    },
    {
      "type": "discount-codes",
      "id": "9002",
      "attributes": {
        "code": "NEWSLTRABC1",
        "value": 1000,
        "active": 1,
        "created_at": "2026-06-05T08:12:00+00:00",
        "updated_at": "2026-06-05T08:12:00+00:00"
      }
    }
  ],
  "meta": {
    "page": { "current-page": 1, "per-page": 10, "from": 1, "to": 2, "total": 2, "last-page": 1 }
  }
}
```

### GET single (`200 OK`)

```json
{
  "data": {
    "type": "discount-codes",
    "id": "9001",
    "attributes": {
      "code": "SPRING2026X",
      "value": 1000,
      "active": 1,
      "created_at": "2026-06-05T08:12:00+00:00",
      "updated_at": "2026-06-05T08:12:00+00:00"
    },
    "links": { "self": "https://<store-host>/api/v2/discount-codes/9001" }
  }
}
```

### POST `201 Created`

```json
{
  "data": {
    "type": "discount-codes",
    "id": "9100",
    "attributes": {
      "code": "SPRING2026X",
      "value": 1000,
      "active": 1,
      "created_at": "2026-06-05T08:42:17+00:00",
      "updated_at": "2026-06-05T08:42:17+00:00"
    },
    "links": { "self": "https://<store-host>/api/v2/discount-codes/9100" }
  }
}
```

### POST /generate (`200 OK`) — collection of the newly-generated codes

```json
{
  "data": [
    {
      "type": "discount-codes",
      "id": "9201",
      "attributes": {
        "code": "K7HAQ2RX9B",
        "value": 1500,
        "active": 1,
        "created_at": "2026-06-05T08:43:00+00:00",
        "updated_at": "2026-06-05T08:43:00+00:00"
      }
    },
    {
      "type": "discount-codes",
      "id": "9202",
      "attributes": {
        "code": "MX2L8PZ4QC",
        "value": 1500,
        "active": 1,
        "created_at": "2026-06-05T08:43:00+00:00",
        "updated_at": "2026-06-05T08:43:00+00:00"
      }
    }
  ],
  "meta": { "page": { "total": 100 } }
}
```

### Common 422 errors

```json
{
  "errors": [
    {
      "status": "422",
      "title": "Unprocessable Entity",
      "detail": "The code has already been taken.",
      "source": { "pointer": "/data/attributes/code" }
    }
  ]
}
```

```json
{
  "errors": [
    {
      "status": "422",
      "title": "Unprocessable Entity",
      "detail": "The value may not be greater than 10000.",
      "source": { "pointer": "/data/attributes/value" }
    }
  ]
}
```

```json
{
  "errors": [
    {
      "status": "422",
      "title": "Unprocessable Entity",
      "detail": "The count may not be greater than 1000.",
      "source": { "pointer": "/data/count" }
    }
  ]
}
```

The duplicate-`code` 422 reflects the platform-wide unique constraint, and the `count` 422 reflects the 1,000-per-request cap — both documented on [[api-discount-codes-attributes]] and [[api-discount-codes-side-effects]].

## Side effects

The writes above trigger the redemption / no-webhook / no-audit behaviour catalogued on [[api-discount-codes-side-effects]].

## Equivalent UI

- [[marketing-discounts-codes]] — admin-panel Container codes list / bulk-generator form / export (mirrors GET / POST / POST /generate / PATCH / DELETE).
- [[marketing-discounts]] — parent Discount type picker.

## Testing checklist

End-to-end sequence for an AI agent. Assumes a parent Container Discount (`discount_type = percent` + `is_container = 1`) already exists on [[api-discounts]] — the Container codes API does not require linking to it.

```
1. GET /api/v2/discount-codes?page[size]=5
   → expect 200, confirm read access.
2. POST /api/v2/discount-codes with code="TESTCODE1", value=1000, active=1
   → expect 201, capture {id_single}.
3. GET /api/v2/discount-codes/{id_single}
   → expect 200; verify code, value, active match.
4. POST /api/v2/discount-codes/generate with count=10, value=1500
   (use Content-Type: application/vnd.api+json)
   → expect 200; collection of 10 freshly-generated rows; capture meta.page.total or the data[].id values.
5. POST /api/v2/discount-codes/generate with count=10, value=1500
   (use Content-Type: application/json — same body)
   → expect 200; confirm plain-JSON content type is accepted (relaxation only present on this resource).
6. POST /api/v2/discount-codes/generate with count=1500, value=1000
   → expect 422 with errors[0].source.pointer = /data/count
     and detail "The count may not be greater than 1000."
7. POST /api/v2/discount-codes with code="TESTCODE1" (duplicate)
   → expect 422 with errors[0].source.pointer = /data/attributes/code
     and detail "The code has already been taken."
8. PATCH /api/v2/discount-codes/{id_single} with attributes.active=0
   → expect 200; verify single-row deactivation works.
9. GET /api/v2/discount-codes/{id_single}
   → expect 200; verify active=0.
10. DELETE /api/v2/discount-codes/{id_single}
    → expect 204.
11. GET /api/v2/discount-codes/{id_single}
    → expect 404.
```

## Related

- [[api-discount-codes]] — hub.
- [[api-discount-codes-attributes]] — field semantics behind these payloads.
- [[api-discount-codes-side-effects]] — write-time / redemption behaviour.
- [[json-api-v2]] — API hub.
- [[api-discounts]] — parent Container Discount endpoint.

## Open questions

None.
