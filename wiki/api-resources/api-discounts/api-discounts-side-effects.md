---
type: api-resource
resource_path: /api/v2/discounts
http_methods: [GET, POST, PATCH, DELETE]
related_entity: discount
related_features: [marketing-discounts]
aliases: ["Discounts API side effects", "discounts webhooks", "discounts uses recompute", "discounts filtering sorting", "discounts no audit log"]
tags: [api, json-api-v2, discounts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 8
---
# Discounts API — side effects & filtering

> Part of [[api-discounts]]. See the hub for the other aspects (attributes & target object, types & validation, examples).

## Purpose

This aspect catalogues what happens **after** a write to the `discounts` resource — webhooks, per-product attachment regeneration, listing-engine re-index, the `uses` recompute pipeline, the Code-PRO parent aggregation, and the no-audit-log gap. It also holds the full **filtering / sorting / include** reference for reads.

## Endpoint

- **URL base:** `<store-host>/api/v2/discounts/`
- **Methods covered here:** read filters/sorts apply to `GET`; side effects fire on `POST` / `PATCH` / `DELETE`.

Base URL, auth, headers: see [[json-api-v2]].

## Attributes

The read-only `uses` and `settings` attributes are the two that this aspect's pipelines maintain. `uses` is recomputed on related order status changes (see Side effects below); `settings` is the internal target-type column the adapter writes from `target.type`. Full attribute table: see [[api-discounts-attributes]].

## Relationships

No JSON-API relationships are declared, so there is no relationship-write side effect on this resource. Child records on the companion resources ([[api-discount-codes]] / [[api-discount-codes-pro]] / [[api-product-to-discount]]) run their own lifecycles.

## Filtering & sorting

**Filtering** — no named filters are declared in the validator. The framework auto-allows `filter[<column>]` for **every column on the `discounts` table** — common useful filters: `filter[type]`, `filter[active]`, `filter[code]`, `filter[is_container]`, `filter[date_start]`, `filter[date_end]`, `filter[order_over]`, `filter[max_uses]`, `filter[geo_zone_id]`. Equality only — no `>=` / `<` / `like` / `in` operators (see [[json-api-v2]] for the platform-wide rule).

> Note: `discount_type` is the on-the-wire name; the underlying column is `type`, so filter on `filter[type]` (not `filter[discount_type]`) when narrowing by type.

**Sorting** — `id`, `date_start`, `date_end`, `created_at`, `updated_at`; prefix with `-` for descending. Sorting on any other column returns 422.

**Include paths** — none. The resource has no schema relationships, so `?include=` is not usable. To fetch child codes / per-product overrides, call the companion resource endpoints directly.

**Sparse-field append values** — none; `?append[discounts]=...` returns 422. The `discount_type` accessor is appended unconditionally by the schema and is always present in the response.

## Side effects

- **`discount.created` / `discount.updated` / `discount.deleted` webhooks** fire from the Discount model's lifecycle. Both admin-panel and JSON-API v2 writes trigger them identically. Subscribed receivers under [[settings-hooks]] receive them via [[notification-delivery]].
- **Per-product attachment regeneration** runs after save for Global / Fixed / Quantity / Countdown discounts. The platform rebuilds the `product_to_discount` join table that drives the storefront's "from X / now Y" badges. On 10,000+-product catalogues this can take minutes; the merchant sees a *"Last update"* badge until it finishes.
- **Listing-engine re-index** — products affected by this discount re-flow through the search engine / Algolia / Listing Engine queue (see [[apps-listing-engine]]). Storefront price labels reflect the change within a few minutes.
- **Discount-uses recompute** — every related order's status change re-tallies `uses` (recompute, not increment) with a 10-second delay. Cancelled / refunded orders auto-decrement the counter, so a previously-`max_uses`-exhausted discount can become available again — see [[discount-stacking]].
- **Code-PRO parent aggregation** — when the parent is `code-pro`, the parent's `uses` is set to `SUM(uses)` across all child Code PRO codes on every recompute.
- **No audit log** — the platform records no actor / no diff history / no created_by / no updated_by for discounts. Only the standard `created_at` / `updated_at` are written. Merchants who need a compliance trail for promotion changes must keep their own log externally. (Only orders + products / variants have per-resource actor capture — see [[json-api-v2]].)

## Equivalent UI

- [[marketing-discounts]] — admin-panel save runs the SAME regeneration + webhook + uses-recompute pipeline as the API write.
- [[settings-hooks]] — webhook subscription manager for the `discount.*` events.
- [[discount]] — entity attribute reference.

## Related

- [[api-discounts]] — hub.
- [[json-api-v2]] — API hub: equality-only filter rule, audit-capture policy.
- [[api-discounts-attributes]] — `uses` / `settings` read-only fields.
- [[discount-stacking]] — uses-recompute mechanics + cancel/refund auto-free.
- [[settings-hooks]] — `discount.created` / `discount.updated` / `discount.deleted` subscriptions.
- [[notification-delivery]] — webhook delivery path.
- [[apps-listing-engine]] — the search engine / Algolia re-index queue.

## Open questions

- Confirm whether the 10-minute `active`-toggle cooldown that applies to admin-panel saves also applies to JSON-API v2 PATCHes. [[discount-stacking]] notes the cooldown is bypassed in dev / CLI contexts — the API context is not explicitly listed. `(verify)`
