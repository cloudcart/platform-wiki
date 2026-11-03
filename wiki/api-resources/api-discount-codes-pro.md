---
type: api-resource
resource_path: /api/v2/discount-codes-pro
http_methods: [GET, POST, PATCH, DELETE]
related_entity: discount-code
related_features: [marketing-discounts-code-pro, marketing-discounts-code-pro-generator, marketing-discounts]
aliases: ["Discount Codes PRO API", "Code PRO API", "JSON-API v2 discount-codes-pro", "API кодове ПРО", "/discount-codes-pro"]
tags: [api, json-api-v2, discounts, code-pro]
plan_gates: ["discount-code-pro", "discount-code-pro-generator"]
created: 2026-05-26
updated: 2026-06-10
source_count: 7
---
# Discount Codes PRO (JSON-API v2)

## Purpose

`discount-codes-pro` is the JSON-API v2 resource for **Code PRO codes** — multi-code campaigns where each child code carries its OWN terms (per-code value, target, date window, customer-group restriction, region restriction, usage caps, barcode format). External integrations use the endpoint to provision per-influencer / per-partner / per-affiliate codes (each with their own commission split), to read per-code redemption status, and to bulk-generate codes from a marketing tool. Each row is, in effect, a mini-campaign linked to a parent Code PRO Discount through the `discount` relationship.

This is the "many codes per parent, each with independent terms" pattern — different from Container codes on [[api-discount-codes]] (where the parent owns the terms) and different from a single coupon `code` on a [[api-discounts|Discount]]. Use this endpoint for influencer campaigns (`INFLUENCER1` = 15% off, `INFLUENCER2` = 20% off), staff codes (capped per-employee), B2B partner codes (each with their own customer group + region), or any campaign where each code needs independent reporting + caps.

## Sub-pages (in this cluster)

This resource is split into 4 aspect pages. Drill into the one that matches the question.

- [[api-discount-codes-pro-attributes]] — full attribute table (`code`, `discount_id`, caps, flags, `code_format`), the `conditions[]` and `customer_groups[]` array PATCH semantics, the `discount` relationship, and single-code CRUD examples.
- [[api-discount-codes-pro-generator]] — the `POST /generate` bulk-generator: random vs range modes, the 5,000-per-request hard cap, range-mode collision pre-check, and leading-zero loss.
- [[api-discount-codes-pro-side-effects]] — the per-code `uses` recompute pipeline + parent-aggregate roll-up, webhook gaps, plan-feature gating, per-customer caps, and Container-vs-PRO cart exclusivity.
- [[api-discount-codes-pro-examples]] — filtering / sorting reference, worked request + response payloads, and the end-to-end testing checklist.

## Endpoint

- **URL base:** `<store-host>/api/v2/discount-codes-pro/`
- **Methods supported:** `GET` (collection), `GET /{id}`, `POST` (collection), `PATCH /{id}`, `DELETE /{id}` — full CRUD.
- **Custom route:** `POST /api/v2/discount-codes-pro/generate` — bulk-generate many codes under one parent (random or numeric-range mode). See [[api-discount-codes-pro-generator]].
- **Read-only:** no.
- **App-installation requirement:** the parent Code PRO Discount requires the `discount-code-pro` plan-feature ON. Codes inherit that gate from the parent — see [[api-discount-codes-pro-side-effects]].
- **Content negotiation:** unlike [[api-discount-codes]], this resource does NOT relax content negotiation — every write request must use `Content-Type: application/vnd.api+json`.

Base URL, auth, headers, and rate limits: see [[json-api-v2]].

## Attributes

Each code carries a `code` string (`alpha_num`, `max:20`, **platform-wide unique**), a parent `discount_id`, per-code date window, usage caps (`max_uses` total, `maxused_user` per-customer), stacking flags (`code_apply`, `apply_regular_price`), barcode settings (`code_format`, `barcode_prefix`), visibility (`only_customer`), region (`geo_zone_id`), customer-group restriction, and a read-only `uses` counter. Per-code discount terms travel in the `conditions[]` array. Full table, validation rules, and the array PATCH semantics: see [[api-discount-codes-pro-attributes]].

## Relationships

| Name | Cardinality | Target | Writable |
|---|---|---|---|
| `discount` | `hasOne` | [[api-discounts]] | Required at create via `discount_id`. Immutable thereafter — delete + recreate under a new parent. |

Details + the `discount_id` validation hook (parent must be `type = code-pro`): see [[api-discount-codes-pro-attributes]].

## Filtering & sorting

`filter[discount_id]` is named in the validator; the framework auto-allows `filter[<column>]` for every column (`code`, `active`, `date_start`, `date_end`, `geo_zone_id`, `max_uses` — equality only). Sortable: `id`, `name`, `code`, `active`, `date_start`, `date_end`, `uses`, `created_at`, `updated_at`. Include path: `discount`. Full reference + worked queries: see [[api-discount-codes-pro-examples]].

## Side effects

Writes are not silent: per-code `uses` is recomputed (not incremented) on related order status changes and the parent's `uses` is rolled up to `SUM(uses)`; `conditions[]` / `customer_groups[]` are rewritten transactionally in `saved`; there is no dedicated `discount_code_pro.*` webhook and no audit log; the `code` column is DB-unique platform-wide; and a Code PRO code and Container codes are mutually exclusive in one cart. Full catalogue: see [[api-discount-codes-pro-side-effects]].

## Equivalent UI

- [[marketing-discounts-code-pro]] — admin-panel Code PRO codes list / per-code edit (mirrors GET / POST / PATCH / DELETE).
- [[marketing-discounts-code-pro-generator]] — admin-panel bulk-generator form (mirrors `POST /generate`; the admin generator respects the `discount-code-pro-generator` plan-feature cap, while the API endpoint is fixed at 5,000 — see [[api-discount-codes-pro-generator]]).
- [[marketing-discounts-code-pro-export]] — admin-panel CSV export of codes + conditions.
- [[marketing-discounts]] — parent Discount type picker (set `discount_type = code-pro` on [[api-discounts]] for API parity).
- [[discount-code]] — entity attribute reference.

## Related

- [[json-api-v2]] — API hub.
- [[api-discounts]] — parent Code PRO Discount endpoint (set `discount_type = code-pro`).
- [[api-discount-codes]] — Container codes (each shares parent's terms — different pattern).
- [[discount-code]] — Code PRO code entity reference.
- [[discount-stacking]] — uses-recompute, parent-aggregate, `code_apply`, `apply_regular_price` max-of-two filter, mutually-exclusive cart slots.
- [[geo-zone]] — region restriction entity.
- [[customers-custom-groups]] — customer-group restriction entity.
- [[settings-hooks]] — `discount.*` events (no dedicated `discount_code_pro.*` event exists).

## Open questions

None at the hub level — see each aspect's own Open questions.
