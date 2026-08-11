---
type: api-resource
resource_path: /api/v2/discount-codes-pro/generate
http_methods: [POST]
related_entity: discount-code
related_features: [marketing-discounts-code-pro-generator, marketing-discounts-code-pro]
aliases: ["Discount Codes PRO generate", "Code PRO bulk generator API", "discount-codes-pro generate endpoint", "POST /discount-codes-pro/generate"]
tags: [api, json-api-v2, discounts, code-pro]
plan_gates: ["discount-code-pro", "discount-code-pro-generator"]
created: 2026-06-10
updated: 2026-06-10
source_count: 7
---
# Discount Codes PRO API — bulk generator (`POST /generate`)

> Part of [[api-discount-codes-pro]]. See the hub for the other aspects (attributes, side effects, examples).

## Purpose

`POST /api/v2/discount-codes-pro/generate` creates **many codes at once** under a single parent Code PRO Discount, all sharing the same generator defaults (terms, customer-groups, region, dates, caps). It is the bulk path for the single-code create documented on [[api-discount-codes-pro-attributes]]. Two modes — `random` (system-generated strings) and `range` (a numeric range materialised into literal code strings).

## Endpoint

- **URL:** `POST <store-host>/api/v2/discount-codes-pro/generate`
- **Content-Type:** `application/vnd.api+json` required.
- **Response:** `200 OK` with a collection of the newly-generated codes.

Base URL, auth, headers: see [[json-api-v2]].

### Random mode

```json
{
  "data": {
    "type": "discount-codes-pro",
    "discount_id": 42,
    "generator_type": "random",
    "limit": 1000,
    "length": 12,
    "structure": ["alpha", "numeric"],
    "date_start": "2026-06-01",
    "date_end": "2026-09-30",
    "max_uses": 1,
    "code_apply": 1,
    "conditions": [
      { "type": "percent", "setting": "all", "value": 1500 }
    ]
  }
}
```

### Range mode

```json
{
  "data": {
    "type": "discount-codes-pro",
    "discount_id": 42,
    "generator_type": "range",
    "range_from": 1000,
    "range_to": 2000,
    "date_start": "2026-06-01",
    "conditions": [
      { "type": "flat", "setting": "all", "value": 500 }
    ]
  }
}
```

## Attributes

| Field | Validation | Notes |
|---|---|---|
| `discount_id` | required, `int`, `exists:discounts,id` | Parent. The controller additionally enforces the platform code — a non-code-pro parent returns 404. |
| `generator_type` | required; `in:random,range` | Pick the mode. |
| `limit` | required when `generator_type = random`; `int, min:1, max:5000` | **Hard cap of 5,000 codes per request on this API endpoint — independent of the merchant's `discount-code-pro-generator` plan-feature value.** The admin-panel generator DOES read the plan-feature value (so it can exceed 5,000 on higher plans), but the JSON-API v2 endpoint is fixed at 5,000 regardless. For batches larger than 5,000, issue multiple sequential calls. |
| `length` | optional; `int, min:6, max:18` | Length of each random code. Default platform-defined when omitted. |
| `structure[]` | required when `generator_type = random`; each entry `in:alpha,numeric` | Character set. `["alpha","numeric"]` = alphanumeric; `["alpha"]` = letters only; `["numeric"]` = digits only. |
| `range_from` | required when `generator_type = range`; `int, min:1, max:999999999999999` | Start of the numeric range. |
| `range_to` | required when `generator_type = range`; `int, min:1, max:999999999999999`, `gt:range_from` | End of the range (inclusive). |
| `date_start` | required; `date_format:Y-m-d` | Date window opens for all generated codes. |
| `date_end` | nullable; `date_format:Y-m-d` | Date window closes. NULL = no expiration. |
| `max_uses`, `maxused_user` | nullable; `int, min:1, max:100000` | Same as individual-code attributes; applied to every generated code. |
| `code_apply`, `apply_regular_price`, `barcode_prefix`, `only_customer` | optional; `in:0,1` | Flags applied to every generated code. |
| `geo_zone_id` | nullable; `int`, `exists:geo_zones,id` | Region restriction for every generated code. |
| `customer_groups[]` | optional, each `exists:type__customer_groups,id` | Customer-group restriction for every generated code. |
| `conditions[]` | optional | Per-code terms — same structure as the single-create endpoint (see [[api-discount-codes-pro-attributes]]). |

### Range mode pre-check (no partial insertion)

When `generator_type = range`, the controller queries the platform code BEFORE attempting insertion. If ANY code in the range already exists, the request returns **422** *"Some of the codes in the specified range already exist."* with `pointer: /data/range_from`. No partial insertion — this is the bulk-generator's transactional safety guarantee.

### Range mode leading-zero loss

When `range_from = 1` and `range_to = 100`, the generator emits codes `1`, `2`, ..., `100` — NOT `001`, `002`, ..., `100`. Leading zeros are lost because the range is materialised via PHP's `range` integer expansion. For fixed-width zero-padded numeric codes use `generator_type = random` with `structure = ["numeric"]` + a specific `length`.

## Relationships

| Name | Cardinality | Target | Writable |
|---|---|---|---|
| `discount` | `hasOne` | [[api-discounts]] | Set for every generated code via the request's `discount_id`. Parent must be `type = code-pro`. |

## Filtering & sorting

Not applicable — `/generate` is a write-only action endpoint. To list the codes it created, use the collection `GET` documented on [[api-discount-codes-pro-examples]] with `filter[discount_id]`.

## Side effects

The bulk `generate` controller calls `$discount->customPush` inside a DB transaction, which DOES save the **parent** Discount — so this path can fire `discount.updated` (single-code PATCH does not). Generated codes get their `uses` counter wired into the recompute pipeline. Full catalogue: see [[api-discount-codes-pro-side-effects]].

## Equivalent UI

- [[marketing-discounts-code-pro-generator]] — admin-panel bulk-generator form. Note the admin generator respects the `discount-code-pro-generator` plan-feature cap, while this API endpoint is fixed at 5,000 codes per request.
- [[marketing-discounts-code-pro]] — list of the generated codes.

## Related

- [[api-discount-codes-pro]] — hub.
- [[api-discount-codes-pro-attributes]] — the `conditions[]` structure shared by the generator.
- [[json-api-v2]] — API hub.
- [[api-discounts]] — parent Code PRO Discount endpoint.
- [[geo-zone]] — region restriction entity.
- [[customers-custom-groups]] — customer-group restriction entity.

## Open questions

- Confirm the rollback semantics of the bulk `generate` controller — the controller wraps `$discount->customPush` in the platform code, but on partial failure it returns 422 with the exception message. Verify no rows are left behind in `discounts_code_pro` or `discounts_to_targets` on rollback. `(verify)`
- Confirm range-mode leading-zero behaviour is documented in the merchant-facing admin help, and that the random-mode workaround (`structure = ["numeric"]` + explicit `length`) is surfaced there. `(verify)`
