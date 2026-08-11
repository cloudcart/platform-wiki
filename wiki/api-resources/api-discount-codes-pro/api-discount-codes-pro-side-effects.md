---
type: api-resource
resource_path: /api/v2/discount-codes-pro
http_methods: [POST, PATCH, DELETE]
related_entity: discount-code
related_features: [marketing-discounts-code-pro, marketing-discounts]
aliases: ["Discount Codes PRO side effects", "Code PRO uses recompute", "discount-codes-pro plan gating", "Code PRO cart exclusivity", "discount-codes-pro webhooks"]
tags: [api, json-api-v2, discounts, code-pro]
plan_gates: ["discount-code-pro", "discount-code-pro-generator"]
created: 2026-06-10
updated: 2026-06-10
source_count: 7
---
# Discount Codes PRO API — side effects, plan gating & cart exclusivity

> Part of [[api-discount-codes-pro]]. See the hub for the other aspects (attributes, generator, examples).

## Purpose

This aspect documents everything that happens **around** a Code PRO write that isn't captured in the request/response shape: the per-code `uses` recompute pipeline and parent-aggregate roll-up, the transactional link-table rewrites, the absence of dedicated webhooks and audit history, the plan-feature gating, the per-customer cap enforcement, and the Container-vs-PRO mutual exclusivity in the cart.

## Endpoint

Applies to all write methods on `<store-host>/api/v2/discount-codes-pro/` (`POST`, `PATCH /{id}`, `DELETE /{id}`) and `POST /api/v2/discount-codes-pro/generate`. Base URL, auth, headers: see [[json-api-v2]].

## Attributes

This aspect does not introduce new attributes; it describes the behaviour of the read-only `uses` counter and the write hooks that fire on save. The attribute reference lives on [[api-discount-codes-pro-attributes]].

## Relationships

The parent `discount` relationship is central to the side-effect behaviour: the per-code `uses` recompute also rolls up to the parent Discount's `uses`, and the bulk generator's save touches the parent (see Side effects below). Relationship definition: see [[api-discount-codes-pro-attributes]].

## Filtering & sorting

Not applicable — this aspect covers write-time behaviour. Query reference: see [[api-discount-codes-pro-examples]].

## Side effects

- **Discount-uses recompute pipeline (per code)** — each code's `uses` counter is **recomputed (not incremented)** on every related order's status change via a 10-second-delayed job on the `order-events6` queue. The **parent Code PRO Discount's `uses` is then set to `SUM(uses)`** across all child codes — one order status change triggers a per-code re-tally + parent-aggregate update. Cancelled orders free the slot back up — see [[discount-stacking]].
- **Targets and customer-groups are written transactionally in `saved`** — every `conditions[]` write deletes existing `targets` rows then re-inserts; same for `customer_groups[]`. A PATCH that omits `conditions` leaves them intact; `conditions: []` clears them; an array replaces the entire set. (Detailed PATCH semantics on [[api-discount-codes-pro-attributes]].)
- **Bool fields are cast to int on save** — `active`, `code_apply`, `apply_regular_price`, `barcode_prefix`, `only_customer` are cast via `(int)` in the adapter's `saving` hook regardless of input shape.
- **`name` defaults to `code`** — when `name` is supplied but empty, the adapter falls back to the code string itself.
- **No dedicated webhook event** for Code PRO CRUD. The platform's `HookEvent` enum exposes only `discount.created` / `discount.updated` / `discount.deleted`, fired from the parent Discount model. A PATCH on a single Code PRO code does NOT fire any of those events directly (the parent's `updated_at` isn't touched by a child-code write). The bulk `generate` controller calls `$discount->customPush` inside a DB transaction, which DOES save the parent — that path can fire `discount.updated`. See [[settings-hooks]].
- **Per-customer caps (`maxused_user`)** enforce per `customer_id` at checkout. Guest checkouts typically create one customer record per email — see [[discount-stacking]] for the edge cases.
- **No per-product attachment regeneration** — Code PRO codes are code-based, with no storefront listing badges.
- **No audit log** — no actor, no diff history, no created_by / updated_by. Only the row's `created_at` / `updated_at`.
- **DB-unique constraint platform-wide** — `discounts_code_pro.code` is unique across the entire table; collisions return 422.
- **Container vs Code PRO mutually exclusive in cart** — at checkout, a customer cannot mix a Code PRO code with Container codes in the same cart. The cart's `discount_code` and `discount_container_code` slots are mutually exclusive — entering a Code PRO code clears the Container array and vice-versa.

## Plan-feature gating

- **Code PRO availability** — the parent Code PRO Discount requires the `discount-code-pro` plan-feature ON. Per-code POST/PATCH on this endpoint is NOT gated by a per-row counter once the parent exists.
- **Generator batch size** — `POST /generate` enforces the hard `max:5000` validator rule, which does NOT read the merchant's `discount-code-pro-generator` plan-feature value. The JSON-API endpoint is fixed at 5,000 codes per request regardless of plan; only the admin-panel generator on [[marketing-discounts-code-pro-generator]] honours the higher plan-feature cap. See [[api-discount-codes-pro-generator]].
- When a plan-feature gate fails on a parent-Discount create through [[api-discounts]], the exception surfaces as **HTTP 402 Payment Required** at the api2 handler — not 403.

## Equivalent UI

- [[marketing-discounts-code-pro]] — admin-panel per-code edit; the same recompute pipeline updates the redemption counts shown there.
- [[marketing-discounts-code-pro-generator]] — admin-panel generator (honours the plan-feature cap, unlike the API).

## Related

- [[api-discount-codes-pro]] — hub.
- [[json-api-v2]] — API hub.
- [[api-discounts]] — parent Code PRO Discount endpoint; carries the rolled-up `uses`.
- [[discount-stacking]] — uses-recompute, parent-aggregate, per-customer cap edge cases, mutually-exclusive cart slots.
- [[settings-hooks]] — `discount.*` events (no dedicated `discount_code_pro.*` event exists).

## Open questions

None.
