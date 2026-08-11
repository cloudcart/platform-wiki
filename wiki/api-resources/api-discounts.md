---
type: api-resource
resource_path: /api/v2/discounts
http_methods: [GET, POST, PATCH, DELETE]
related_entity: discount
related_features: [marketing-discounts, marketing-discounts-flat, marketing-discounts-percent, marketing-discounts-shipping, marketing-discounts-fixed, marketing-discounts-code-pro]
aliases: ["Discounts API", "JSON-API v2 discounts", "API отстъпки", "/discounts"]
tags: [api, json-api-v2, discounts]
plan_gates: ["discount_global", "discount_coupon", "discount_fixed", "discount-code-pro"]
created: 2026-05-26
updated: 2026-06-10
source_count: 8
---
# Discounts (JSON-API v2)

## Purpose

`discounts` is the JSON-API v2 resource for the **parent promotion record** in CloudCart — every percent-off, flat-amount-off, free-shipping, per-product Fixed-price, and Code PRO campaign starts as one row in this table. External integrations use the endpoint to **provision Black Friday / holiday campaigns from a marketing tool**, **toggle promotions from an outside scheduler**, and **read the active promotion catalogue** for a partner dashboard or analytics export.

This resource creates ONLY the parent. The child records that some discount types need live on companion resources: [[api-discount-codes]] for Container child codes, [[api-discount-codes-pro]] for per-code Code PRO terms, and [[api-product-to-discount]] for per-variant Fixed-price overrides. Writes here run the same lifecycle as the admin-panel save under [[marketing-discounts]] — same validation, same plan-feature gating, same `discount.*` webhooks, same downstream pipelines described in [[discount-stacking]].

## Sub-pages (in this cluster)

This resource is split into 4 aspect pages. Drill into the one that matches the question.

- [[api-discounts-attributes]] — the full writable / read-only attribute table, the polymorphic `target` object (the seven `target.type` values), and the no-JSON-API-relationships rule.
- [[api-discounts-types]] — the five accepted `discount_type` values, the type-specific required fields, the mutually-exclusive validation rules, the plan-feature gate (HTTP 402, not 403), and the common 422 error shapes.
- [[api-discounts-side-effects]] — the webhook + attachment-regeneration + listing-engine + uses-recompute pipeline, the no-audit-log gap, and the full filtering / sorting / include reference.
- [[api-discounts-examples]] — worked curl requests + JSON responses for every type, and the end-to-end CRUD testing checklist.

## Endpoint

- **URL base:** `<store-host>/api/v2/discounts/`
- **Methods supported:** `GET` (collection), `GET /{id}`, `POST` (collection), `PATCH /{id}`, `DELETE /{id}` — full CRUD.
- **Read-only:** no.
- **Custom routes:** none.
- **App-installation requirement:** none — the resource is always registered. Per-call success is gated by plan-features at create time — see [[api-discounts-types]].

Base URL, auth, headers, and rate limits: see [[json-api-v2]].

## Attributes

Each Discount carries a `name`, a `discount_type` (one of `flat`, `percent`, `shipping`, `fixed`, `code-pro`), a date window (`date_start` / `date_end`), a `type_value` (amount or percent, type-dependent), an `order_over` threshold, usage caps (`max_uses` + read-only `uses`), a coupon `code`, stacking + container flags (`code_apply`, `is_container`), countdown-timer flags (`timer_list`, `timer_details`), and a polymorphic `target` object. Full table + the `target` object reference: see [[api-discounts-attributes]].

## Relationships

This resource declares **no JSON-API relationships**. The companion resources that link back to a Discount each have their own top-level endpoint — [[api-discount-codes]] (Container child codes), [[api-discount-codes-pro]] (Code PRO codes), and [[api-product-to-discount]] (per-variant Fixed-price overrides). Detail: see [[api-discounts-attributes]].

## Filtering & sorting

No named filters are declared; the framework auto-allows `filter[<column>]` for every column on the `discounts` table (equality only). Sortable: `id`, `date_start`, `date_end`, `created_at`, `updated_at`. No `?include=` (no schema relationships). Full reference + worked queries: see [[api-discounts-side-effects]].

## Side effects

Writes are not silent: `discount.created` / `discount.updated` / `discount.deleted` webhooks fire identically for admin and API writes; per-product attachment regeneration + listing-engine re-index run after save; `uses` is recomputed (not incremented) on related order status changes; and there is **no audit log** for discounts. Full catalogue: see [[api-discounts-side-effects]].

## Equivalent UI

- [[marketing-discounts]] — admin-panel master discount list / type picker / CRUD (mirrors GET / POST / PATCH / DELETE on this endpoint).
- [[marketing-discounts-flat]] / [[marketing-discounts-percent]] / [[marketing-discounts-shipping]] — per-type edit screens (correspond to `discount_type = flat` / `percent` / `shipping`).
- [[marketing-discounts-fixed]] — Fixed discount parent edit; per-variant overrides flow through [[api-product-to-discount]].
- [[marketing-discounts-code-pro]] — Code PRO parent edit; child codes through [[api-discount-codes-pro]].
- [[marketing-discounts-codes]] — Container parent + bulk codes manager; child codes through [[api-discount-codes]].
- [[discount]] — entity attribute reference.

## Related

- [[json-api-v2]] — API hub: auth, headers, status codes, webhook side-effect principle.
- [[api-discount-codes]] — Container child-code endpoint.
- [[api-discount-codes-pro]] — Code PRO child-code endpoint (with bulk `generate`).
- [[api-product-to-discount]] — per-variant Fixed-discount price overrides.
- [[discount]] — full Discount entity reference.
- [[discount-code]] — child-code entity.
- [[discount-stacking]] — `code_apply`, `apply_regular_price`, uses-recompute, ordering rules.
- [[marketing-discounts]] — admin-panel master list / type picker.
- [[marketing-discounts-flat]] / [[marketing-discounts-percent]] / [[marketing-discounts-shipping]] / [[marketing-discounts-fixed]] / [[marketing-discounts-code-pro]] — per-type admin edit screens.
- [[settings-hooks]] — `discount.created` / `discount.updated` / `discount.deleted` event subscriptions.
- [[plan-gates]] — `discount_global` / `discount_coupon` / `discount_fixed` / `discount-code-pro` counters.
- [[products-smart-collections]] — target type `selection`.

## Open questions

None at the hub level — see each aspect's own Open questions.
