---
type: api-resource
resource_path: /api/v2/discount-codes
http_methods: [GET, POST, PATCH, DELETE]
related_entity: discount-code
related_features: [marketing-discounts-codes, marketing-discounts]
aliases: ["Discount Codes API side effects", "Container codes redemption", "discount-codes single-use", "discount-codes uses recompute"]
tags: [api, json-api-v2, discounts, container-codes]
plan_gates: ["discount_coupon"]
created: 2026-06-10
updated: 2026-06-10
source_count: 6
---
# Discount Codes API — side effects & redemption

> Part of [[api-discount-codes]]. See the hub for the other aspects (attributes, examples).

## Purpose

This aspect catalogues the **write-time and redemption-time behaviour** of the `discount-codes` resource: what a CRUD write does (and does NOT) trigger, how a Container code is consumed at checkout, how stacking and the parent's `uses` counter are controlled at the parent-Container level, and the platform-wide DB-unique `code` constraint. For field semantics see [[api-discount-codes-attributes]]; for worked payloads see [[api-discount-codes-examples]].

## Endpoint

This aspect describes the effects of `POST` / `POST /generate` / `PATCH` / `DELETE` on `<store-host>/api/v2/discount-codes/` and the checkout-time consumption flow. Base URL, auth, headers: see [[json-api-v2]].

## Attributes

The effects below reference the row's `active` (flipped to `0` on redemption) and `code` (platform-wide unique) fields. Full attribute definitions: see [[api-discount-codes-attributes]].

## Relationships

No JSON-API relationship is declared, but the row participates in a **parent-controlled** lifecycle: stacking, the `uses` counter, and `total_value` cap all live on the parent Container Discount on [[api-discounts]], not on the row. See the hub [[api-discount-codes]].

## Filtering & sorting

Not applicable to this aspect — see [[api-discount-codes-examples]].

## Side effects

- **No dedicated webhook event** for discount-code CRUD. The platform's `HookEvent` enum exposes only `discount.created` / `discount.updated` / `discount.deleted` — and those fire from the parent Discount model, not from individual codes. A POST / generate / PATCH / DELETE here fires no webhook of its own. The parent Container Discount's `updated_at` is **not** touched by a child-code write either (the row write doesn't propagate to the parent).
- **Single-use consumption at checkout** — when a customer redeems a Container code at checkout, the platform flips the row's `active` to `0`. The row stays in the table for audit purposes; deletion is not automatic.
- **Sequential redemption with parent-Container cap** — the cart stores Container codes in an array (`discount_container_code`). The checkout engine iterates the array and consumes codes sequentially against the parent Container's `total_value` cap (per [[discount-stacking]]).
- **Parent-controlled stacking** — the row has no `code_apply` of its own; the cart engine reads the parent Container Discount's `code_apply` for the reject-on-conflict check. This means deactivating stacking on a Container campaign happens by PATCHing the parent on [[api-discounts]], not by anything on these rows.
- **No per-product attachment regeneration** — Container codes don't render on storefront listings (no "from X / now Y" badge), so the per-product attachment pipeline that runs for Global / Fixed discounts is a no-op for this resource.
- **Discount-uses recompute (parent-level)** — the parent Container Discount's `uses` counter is recomputed (not incremented) on every related order's status change via a 10-second-delayed job on the `order-events6` queue. Cancelled / refunded orders free the slot back up — see [[discount-stacking]].
- **No audit log** — no actor, no diff history, no created_by / updated_by. Only the row's `created_at` / `updated_at` are written.
- **DB-unique constraint platform-wide** — `discount_codes.code` is unique across the ENTIRE table, not per merchant. Attempting to POST a code that already exists on ANY merchant's store returns 422 with `code` error pointer.

## Equivalent UI

- [[marketing-discounts-codes]] — admin-panel Container codes list; redemption flips a code's row to inactive there too.
- [[marketing-discounts]] — parent Discount type picker (stacking / cap live on the parent).

## Related

- [[api-discount-codes]] — hub.
- [[json-api-v2]] — API hub.
- [[api-discounts]] — parent Container Discount endpoint (carries `code_apply`, `total_value`, `uses`).
- [[discount-stacking]] — Container parent-controlled stacking, sequential redemption, uses-recompute.
- [[discount-code]] — Discount Code entity reference.
- [[settings-hooks]] — `discount.*` events (no dedicated `discount_code.*` event exists).

## Open questions

- Verify how parent-Container linkage is resolved at redemption time given the `discount_codes` row carries no `discount_id` FK — confirm whether the cart engine looks up the parent by joining `discounts_to_targets` or by another bridge table, and whether an orphan code (one POSTed through this API without admin-panel context) is redeemable at all. `(verify)`
- Confirm whether a write here propagates to the parent Container Discount's `updated_at` (the platform side-effect chain — `discount.updated` webhook to subscribers — depends on this). The model lifecycle on a Container code does not touch the parent. `(verify)`
