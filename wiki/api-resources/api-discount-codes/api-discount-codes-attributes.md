---
type: api-resource
resource_path: /api/v2/discount-codes
http_methods: [GET, POST, PATCH, DELETE]
related_entity: discount-code
related_features: [marketing-discounts-codes, marketing-discounts]
aliases: ["Discount Codes API attributes", "Container codes API attributes", "discount-codes generate", "discount-codes bulk-generator"]
tags: [api, json-api-v2, discounts, container-codes]
plan_gates: ["discount_coupon"]
created: 2026-06-10
updated: 2026-06-10
source_count: 6
---
# Discount Codes API — attributes, generator & gating

> Part of [[api-discount-codes]]. See the hub for the other aspects (side effects, examples).

## Purpose

This aspect is the **attribute reference** for the `discount-codes` resource: every writable / read-only field on a Container code row, the `POST /generate` bulk-generator and its validation, the content-negotiation relaxation, and how the `discount_coupon` plan-feature is metered. For single-code curl shapes see [[api-discount-codes-examples]]; for the write-time behaviour see [[api-discount-codes-side-effects]].

## Endpoint

- **URL base:** `<store-host>/api/v2/discount-codes/`
- **Methods covered here:** `POST` (single), `PATCH /{id}`, plus the `POST /api/v2/discount-codes/generate` bulk route.
- **Content-Type:** writes accept **plain `application/json` OR `application/vnd.api+json`** — the route is registered with `contentNegotiator('json')`, the only discount resource with this relaxation.

Base URL, auth, headers: see [[json-api-v2]].

## Attributes

| Attribute | Type | Writable POST | Writable PATCH | Required | Notes / validation |
|---|---|---|---|---|---|
| `code` | string | yes | yes | POST yes / PATCH `sometimes` | `alpha_num`, `max:20`, **unique on `discount_codes.code` platform-wide** (one namespace across every merchant). The literal redeemable string. Stored uppercase; case-insensitive at checkout. For programmatic creation; use `POST /generate` for bulk-random. |
| `value` | int | yes | yes | POST yes / PATCH `sometimes` | `min:1, max:10000`. The discount amount captured AT THE ROW. Since `type` is forced to `percent` (see below), the value is interpreted as the percent × 100 — `1000` = 10.00%, `100` = 1.00%. Storage convention follows the platform-wide rule "percent × 100, max 100% = 10000". |
| `active` | int `0` / `1` | yes | yes | POST yes / PATCH `sometimes` | `min:0, max:1`. Per-row enable flag. After redemption the platform flips the row to `0` (single-use). Setting `0` manually pre-burns or disables a code. |
| `type` | string | **read-only — server-forced** | **read-only — server-forced** | — | Internal column. The adapter overrides `type` to `"percent"` on every save (`saving` hook). The schema also hides this column from the JSON response, so it is neither writable nor readable. **Flat-type Container codes cannot be created through this endpoint** — use the admin-panel generator on [[marketing-discounts-codes]] for `flat` Container campaigns. |
| `created_at`, `updated_at` | timestamp | **read-only** | **read-only** | — | Standard timestamps. |

The table has no other columns — no `discount_id`, no `max_uses`, no `maxused_user`, no `customer_email`, no `code_apply`, no `code_format`, no `apply_regular_price`. All per-campaign behaviour lives on the parent Container Discount per [[api-discounts]] / [[marketing-discounts-codes]].

### `POST /generate` (bulk-generator)

`POST /api/v2/discount-codes/generate` creates `count` random codes in one INSERT, all sharing the same `value` and all forced to `type = "percent"` + `active = 1`. The generation routine picks each code string server-side; the body is the JSON-API collection of the freshly-inserted rows (ordered by `created_at DESC LIMIT count`).

Body (accepts `application/json` OR `application/vnd.api+json`):

```json
{
  "data": {
    "type": "discount-codes",
    "count": 500,
    "value": 1000
  }
}
```

Generate validation:

| Field | Validation | Notes |
|---|---|---|
| `count` | required, `int`, `min:1, max:1000` | Hard cap of **1,000 codes per request**. For larger batches, paginate. |
| `value` | required, `int`, `min:1, max:10000` | Discount percent × 100. Each successive batch can pass a different value, so the parent Container can host a mixed-value pool of codes (e.g., 500 codes at 10% + 500 codes at 15%). |

Defaults the controller hard-codes on every generated row: `type = 'percent'`, `active = 1`. There is no way to override either through the generate route.

## Relationships

This resource declares **no JSON-API relationships** — the `discount_codes` row has no FK column. The `discount_id` attribute is therefore NOT accepted on POST. To read the parent Container Discount, query [[api-discounts]] by `is_container = 1` + `type = percent`. See the hub [[api-discount-codes]] for the full rationale.

## Filtering & sorting

This aspect documents attributes only. For the filter / sort reference and worked queries, see [[api-discount-codes-examples]].

## Side effects

`type` is server-forced to `percent` on every save and hidden from the response; `active` flips to `0` on redemption. The broader write-time behaviour (no webhook, no audit log, the platform-wide unique `code` constraint, parent-level uses recompute) is catalogued on [[api-discount-codes-side-effects]].

## Plan-feature gating

This endpoint itself does NOT run a per-row plan-feature check. The `discount_coupon` plan-feature counter is consumed once when the parent Container Discount is created on [[api-discounts]] (with `is_container = 1` + `discount_type = percent` + no `code` set on the parent → the adapter's gate selects `discount_coupon`). Once the parent exists, generating or POSTing individual codes here is unmetered at the JSON-API v2 layer.

If the parent-Container plan-gate fails on a later call, the exception bubbles up as **HTTP 402 Payment Required** at the api2 handler — not HTTP 403. (Older wiki phrasing claimed 403; the api2 handler explicitly maps a plan-restriction error to HTTP 402.)

## Equivalent UI

- [[marketing-discounts-codes]] — admin-panel Container codes list / bulk-generator form (mirrors POST / POST /generate / PATCH; also supports `flat` Container campaigns that this endpoint cannot create).
- [[discount-code]] — entity attribute reference.

## Related

- [[api-discount-codes]] — hub.
- [[json-api-v2]] — API hub.
- [[api-discounts]] — parent Container Discount endpoint (set `is_container = 1` + `discount_type = percent`).
- [[api-discount-codes-pro]] — Code PRO codes (each carries its OWN terms — different pattern).
- [[discount-code]] — Discount Code entity reference.
- [[marketing-discounts-codes]] — admin-panel Container codes list / generator / export.

## Open questions

- Verify whether `code_format` (EAN-13 / EAN-8 barcode mode) configured on the parent Container Discount is honoured by the random generator on this endpoint, or whether `POST /generate` always emits 10-char alphanumeric strings. `(verify)`
- Confirm whether the bulk `generate` endpoint honours any per-merchant lifetime cap on Container code count (separate from the per-call `max:1000` cap). The validator caps a single call only; an integrator could loop until the parent's `discount_coupon` slot runs out — verify the failure mode at that limit. `(verify)`
