---
type: api-resource
resource_path: /api/v2/discount-codes-pro
http_methods: [GET, POST, PATCH, DELETE]
related_entity: discount-code
related_features: [marketing-discounts-code-pro, marketing-discounts]
aliases: ["Discount Codes PRO API attributes", "Code PRO API attributes", "discount-codes-pro conditions", "discount-codes-pro customer_groups"]
tags: [api, json-api-v2, discounts, code-pro]
plan_gates: ["discount-code-pro"]
created: 2026-06-10
updated: 2026-06-10
source_count: 7
---
# Discount Codes PRO API — attributes & single-code CRUD

> Part of [[api-discount-codes-pro]]. See the hub for the other aspects (generator, side effects, examples).

## Purpose

This aspect is the **attribute reference** for the `discount-codes-pro` resource: every writable / read-only field, the nested `conditions[]` discount-terms structure, the `customer_groups[]` array semantics, the `discount` relationship, and the single-code create / read / update / delete shapes. For bulk creation use the generator instead — see [[api-discount-codes-pro-generator]].

## Endpoint

- **URL base:** `<store-host>/api/v2/discount-codes-pro/`
- **Methods covered here:** `GET` (collection), `GET /{id}`, `POST`, `PATCH /{id}`, `DELETE /{id}`.
- **Content-Type:** writes require `Content-Type: application/vnd.api+json`.

Base URL, auth, headers: see [[json-api-v2]].

## Attributes

| Attribute | Type | Writable POST | Writable PATCH | Required | Notes / validation |
|---|---|---|---|---|---|
| `discount_id` | int | yes | (immutable after create) | POST yes | Parent Code PRO Discount. Validated via `exists:discounts,id`. The validator's `validateDiscountType` after-hook then refuses any parent whose `type != "code-pro"` with *"The discount must be of type code-pro."* The schema hides the column from response serialization and exposes the parent through the `discount` relationship instead. |
| `code` | string | yes | yes | POST yes / PATCH `sometimes` | `alpha_num`, `max:20`, **unique on `discounts_code_pro.code` platform-wide** (one namespace across every merchant). Cannot reuse a code string across two PRO campaigns, even on different stores. |
| `name` | string | yes | yes | no | `max:191`. Internal-only label; when omitted on save, the adapter falls back to the code string itself. |
| `active` | enum `0` / `1` | yes | yes | no | Per-code enable flag. |
| `date_start` | date `Y-m-d` | yes | yes | POST yes / PATCH `sometimes` | When this code becomes redeemable. |
| `date_end` | date `Y-m-d` | yes | yes | no, nullable | When this code stops being redeemable. NULL = no expiration. |
| `max_uses` | int | yes | yes | no, nullable | `min:1, max:100000`. Total redemptions across all customers per code. |
| `maxused_user` | int | yes | yes | no, nullable | `min:1, max:100000`. Per-customer cap per code. Enforced at checkout per `customer_id` (NOT per email — see [[discount-stacking]] for guest-edge cases). |
| `code_apply` | enum `0` / `1` | yes | yes | no | Stacking flag. `1` allows the code on top of already-discounted lines; `0` (default) rejects. See [[discount-stacking]]. |
| `apply_regular_price` | enum `0` / `1` | yes | yes | no | Only meaningful when `code_apply = 1`. When `1`, the code re-evaluates against the catalog price, then the platform applies the **max of (already-applied-discount, this-code-against-regular-price)** — a max-of-two filter, NOT a blind override (see [[discount-stacking]]). |
| `code_format` | enum | yes | yes | no, nullable | `ean8` or `ean13`. When set, the code is treated as a barcode at checkout. |
| `barcode_prefix` | enum `0` / `1` | yes | yes | no | When `1`, the entered code acts as a prefix and the scanner appends the actual barcode digits. |
| `only_customer` | enum `0` / `1` | yes | yes | no | When `1`, the code is hidden from guest checkouts (logged-in customers only). |
| `geo_zone_id` | int | yes | yes | no, nullable | FK; validated via `exists:geo_zones,id`. Region restriction — see [[geo-zone]]. |
| `customer_groups[]` | array of int | yes | yes | no | Each ID validated via `exists:type__customer_groups,id`. Customer-group restriction — see [[customers-custom-groups]]. **PATCH semantics: omitting the key leaves the link table intact; sending an empty array clears it; sending an array re-creates the entire set transactionally** (delete-then-insert in `saved`). |
| `conditions[]` | array of objects | yes | yes | no | Per-code discount terms — see Conditions structure below. Same PATCH semantics as `customer_groups[]` — omit to leave intact, send `[]` to clear, send an array to replace. |
| `uses` | int | **read-only** | **read-only** | — | Per-code redemption counter, recomputed on related order status changes — see [[api-discount-codes-pro-side-effects]]. |
| `conditions` (in GET response) | array | **read-only** | — | — | Derived from the underlying `discounts_to_targets` rows; the schema appends it on response serialization. |

### Conditions structure

Each entry in the `conditions[]` array carries:

| Key | Validation | Notes |
|---|---|---|
| `type` | required with `conditions`; `in:flat,percent,shipping` | The discount mechanic for this condition. |
| `setting` | required with `conditions`; `in:all,product,category,vendor,category_vendor,selection,order_over` | The target for this condition. |
| `value` | required when `type` is `flat` OR `percent`; `int, min:1` | Discount amount. For `flat` = cents (flat amount). For `percent` = percent × 100, max 10000 (= 100%). |
| `order_over` | nullable; `int, min:1` | Required when `setting = order_over`. Minimum cart total in cents. |

The adapter divides `value` and `order_over` by 100 before save (`convertConditionPricesFromCents`); the model's `setConditions` then converts back to integer cents via the platform code. Each condition row creates one underlying target / setting row on the code.

## Relationships

| Name | Cardinality | Target | Writable |
|---|---|---|---|
| `discount` | `hasOne` | [[api-discounts]] | Required at create via the `discount_id` attribute. Immutable thereafter (PATCHing the relationship is not supported — delete + recreate under a new parent). |

The parent must be a Discount of type `code-pro`; any other type is rejected at validation with *"The discount must be of type code-pro."*

## Filtering & sorting

This aspect documents attributes only. For the full filter / sort / include reference and worked queries, see [[api-discount-codes-pro-examples]].

## Side effects

Bool fields (`active`, `code_apply`, `apply_regular_price`, `barcode_prefix`, `only_customer`) are cast to int on save; `name` defaults to `code` when empty; `conditions[]` and `customer_groups[]` rewrite their link tables transactionally in `saved`. Full side-effect catalogue (uses recompute, webhooks, audit, cart exclusivity): see [[api-discount-codes-pro-side-effects]].

## Equivalent UI

- [[marketing-discounts-code-pro]] — admin-panel per-code edit form (mirrors these attributes).
- [[discount-code]] — entity attribute reference.

## Related

- [[api-discount-codes-pro]] — hub.
- [[json-api-v2]] — API hub.
- [[api-discounts]] — parent Code PRO Discount endpoint.
- [[discount-code]] — Code PRO code entity reference.
- [[discount-stacking]] — `code_apply` / `apply_regular_price` max-of-two filter; per-customer cap edge cases.
- [[geo-zone]] — region restriction entity.
- [[customers-custom-groups]] — customer-group restriction entity.

## Open questions

- Verify whether bool-cast in the adapter's `saving` hook accepts string forms like `"true"` / `"false"`, or whether only `0` / `1` / `true` / `false` literals work cleanly. The validator's `in:0,1` rule rejects others upstream, but the cast happens after validation passes.
- Verify whether `code_format = ean13` / `ean8` validates the EAN check-digit at checkout for codes created via this API endpoint (the admin-panel form does the validation; API-created codes may or may not be re-validated at write time). `(verify)`
- Confirm whether `code_prefix` (set in the adapter from `code_format`) is exposed read-side or hidden — the column appears in the adapter's `saving` hook but is not in the validator's `rules` block. `(verify)`
