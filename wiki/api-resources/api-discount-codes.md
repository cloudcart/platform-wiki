---
type: api-resource
resource_path: /api/v2/discount-codes
http_methods: [GET, POST, PATCH, DELETE]
related_entity: discount-code
related_features: [marketing-discounts-codes, marketing-discounts]
aliases: ["Discount Codes API", "Container codes API", "JSON-API v2 discount-codes", "API кодове за отстъпка", "/discount-codes"]
tags: [api, json-api-v2, discounts, container-codes]
plan_gates: ["discount_coupon"]
created: 2026-05-26
updated: 2026-06-10
source_count: 6
---
# Discount Codes (JSON-API v2)

## Purpose

`discount-codes` is the JSON-API v2 resource for the **single-use Container coupon strings** — the thousands of bulk-generated codes that sit under a parent Container Discount and get redeemed once each (typical pattern: *"Black Friday: 1,000 unique 10%-off codes for our newsletter list"*). Each row is just a literal redeemable string with a value and an active flag; the parent campaign's terms (target, customer-group restriction, date window, `code_apply` stacking flag) come from the **parent Container Discount** described in [[marketing-discounts-codes]] — NOT from these rows.

This is the "thousands of one-time codes under one campaign" pattern — different from a single `code` on a [[api-discounts|Discount]] (one code per discount) and different from [[api-discount-codes-pro]] (where each code carries its OWN terms). Use this endpoint to bulk-generate codes for a mass-mail send, to read which codes have been redeemed (`active = 0` after redemption), and to deactivate / delete individual codes.

**Important schema note:** the underlying `discount_codes` table has only `id`, `code`, `type`, `value`, `active`, `created_at`, `updated_at` columns — there is **no `discount_id` FK** on a Container code row. The platform doesn't carry parent linkage on the row itself; the checkout engine resolves the parent Container Discount by other means at redemption time. Practical implication: this API endpoint does **not** accept a `discount_id` attribute, and a POST creates a code with no parent linkage in this table. Use the admin-panel generator on [[marketing-discounts-codes]] when parent linkage is required upfront.

## Sub-pages (in this cluster)

This resource is split into 3 aspect pages. Drill into the one that matches the question, rather than reading every page.

- [[api-discount-codes-attributes]] — the attribute table (`code`, `value`, `active`; server-forced `type = percent`), the `POST /generate` bulk-generator (`count` + `value`, 1,000-per-request cap), the content-negotiation relaxation, and plan-feature gating.
- [[api-discount-codes-side-effects]] — single-use consumption at checkout, parent-controlled stacking, the parent-level uses recompute, the platform-wide DB-unique `code` constraint, and the no-webhook / no-audit gaps.
- [[api-discount-codes-examples]] — filtering / sorting reference, copy-paste curl requests + response payloads, the common 422 errors, and the end-to-end testing checklist.

## Endpoint

- **URL base:** `<store-host>/api/v2/discount-codes/`
- **Methods supported:** `GET` (collection), `GET /{id}`, `POST` (collection), `PATCH /{id}`, `DELETE /{id}` — full CRUD.
- **Custom route:** `POST /api/v2/discount-codes/generate` — bulk-generate `count` random codes in one transaction. See [[api-discount-codes-attributes]].
- **Content negotiation relaxation:** the route is registered with `contentNegotiator('json')`, so it **accepts plain `application/json`** on POST / PATCH bodies, not only `application/vnd.api+json`. This is the only discount resource with this relaxation; [[api-discount-codes-pro]] still requires `application/vnd.api+json`.
- **Read-only:** no.
- **App-installation requirement:** none — gated by `discount_coupon` plan-feature at parent-Container create time, not per code. See [[api-discount-codes-side-effects]].

Base URL, auth, headers, and rate limits: see [[json-api-v2]].

## Attributes

Each row carries just three writable fields — `code` (the literal redeemable string; `alpha_num`, `max:20`, platform-wide unique), `value` (the discount percent × 100; `min:1, max:10000`), and `active` (`0` / `1`, flipped to `0` on redemption). `type` is server-forced to `percent` and hidden; `created_at` / `updated_at` are read-only. The table has no `discount_id`, `max_uses`, `code_apply`, or `code_format` — all per-campaign behaviour lives on the parent Container Discount. Full table + the `POST /generate` validation: see [[api-discount-codes-attributes]].

## Relationships

This resource declares **no JSON-API relationships**. There is no FK column on the row to expose as one. Parent-Container linkage is established by the admin-panel flow, not surfaced here. To read the parent Container Discount, query [[api-discounts]] separately by `is_container = 1` + `type = percent`.

## Filtering & sorting

The framework auto-allows `filter[<column>]` for every column on the `discount_codes` table (equality only) — useful: `filter[code]`, `filter[active]`, `filter[value]`, `filter[type]`. Sortable: `id`, `created_at`, `updated_at`, `active`, `code`. No include paths (no relationships) and no `?append[...]` values. Worked queries: see [[api-discount-codes-examples]].

## Side effects

A write here fires no webhook of its own (the `discount.*` events fire from the parent Discount only) and writes no audit log. At checkout the redeemed row's `active` flips to `0` (single-use); stacking and the parent's `uses` counter are controlled at the parent-Container level; and the `code` column is DB-unique across the ENTIRE platform. Full catalogue: see [[api-discount-codes-side-effects]].

## Equivalent UI

- [[marketing-discounts-codes]] — admin-panel Container codes list / bulk-generator form / export (mirrors GET / POST / POST /generate / PATCH / DELETE on this endpoint).
- [[marketing-discounts]] — parent Discount type picker (set `is_container = 1` + `discount_type = percent` on [[api-discounts]] for API parity).
- [[discount-code]] — entity attribute reference.

## Related

- [[json-api-v2]] — API hub.
- [[api-discounts]] — parent Container Discount endpoint (set `is_container = 1` + `discount_type = percent`).
- [[api-discount-codes-pro]] — Code PRO codes (each carries its OWN terms — different pattern).
- [[discount-code]] — Discount Code entity reference.
- [[marketing-discounts-codes]] — admin-panel Container codes list / generator / export.
- [[marketing-discounts]] — parent Discount type picker.
- [[discount-stacking]] — Container parent-controlled stacking, sequential redemption, uses-recompute.
- [[settings-hooks]] — `discount.*` events (no dedicated `discount_code.*` event exists).

## Open questions

None at the hub level — see each aspect's own Open questions. The two cross-cutting items (how parent-Container linkage is resolved at redemption time given the row carries no `discount_id` FK, and whether a per-merchant lifetime cap exists beyond the per-call `max:1000`) are tracked on [[api-discount-codes-side-effects]]; the generator behaviour items (barcode `code_format`, leading-zero handling) are tracked on [[api-discount-codes-attributes]].
