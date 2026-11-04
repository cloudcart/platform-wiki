---
type: api-resource
resource_path: /api/v2/discount-codes
http_methods: [GET, POST, PATCH, DELETE]
related_entity: discount-code
related_features: [marketing-discounts-codes, marketing-discounts]
aliases: ["Discount Codes API side effects", "Container codes redemption", "discount-codes reuse", "discount-codes uses recompute"]
tags: [api, json-api-v2, discounts, container-codes]
plan_gates: ["discount_global"]
created: 2026-06-10
updated: 2026-11-04
source_count: 6
---
# Discount Codes API — side effects & redemption

> Part of [[api-discount-codes]]. See the hub for the other aspects (attributes, examples).

## Purpose

This aspect catalogues the **write-time and redemption-time behaviour** of the `discount-codes` resource: what a CRUD write does (and does NOT) trigger, how a Container code behaves at checkout, how stacking and the `uses` counter belong to the Container Discount, and the platform-wide DB-unique `code` constraint. For field semantics see [[api-discount-codes-attributes]]; for worked payloads see [[api-discount-codes-examples]].

## Endpoint

This aspect describes the effects of `POST` / `POST /generate` / `PATCH` / `DELETE` on `<store-host>/api/v2/discount-codes/` and the checkout-time flow. Base URL, auth, headers: see [[json-api-v2]].

## Attributes

The effects below reference the row's `active` (`0` stops the code being entered) and `code` (platform-wide unique) fields. Full attribute definitions: see [[api-discount-codes-attributes]].

## Relationships

No JSON-API relationship is declared, and a code belongs to no Container: stacking, the `uses` counter, and the `total_value` cap all live on the Container Discount on [[api-discounts]], not on the row. See the hub [[api-discount-codes]].

## Filtering & sorting

Not applicable to this aspect — see [[api-discount-codes-examples]].

## Side effects

- **No dedicated webhook event** for discount-code CRUD. The platform's `HookEvent` enum exposes only `discount.created` / `discount.updated` / `discount.deleted` — and those fire from the Discount record, not from individual codes. A POST / generate / PATCH / DELETE here fires no webhook of its own. A Container Discount's `updated_at` is **not** touched by a code write either.
- **Not used up at checkout** — placing an order does not change a Container code. It stays active and can be entered again until it is deactivated or deleted.
- **Several codes against one Container's value** — the cart stores Container codes in an array (`discount_container_code`). All active Containers for the customer's region try the entered codes and the highest total wins; a code applies only if it fits what remains of that Container's value (per [[discount-stacking]]).
- **Stacking** — the row has no `code_apply` of its own. A Container code is never refused because a line holds a product discount. The Container's `code_apply` defaults to on and its admin form has no such switch.
- **No per-product attachment regeneration** — Container codes don't render on storefront listings (no "from X / now Y" badge), so the per-product attachment pipeline that runs for Global / Fixed discounts is a no-op for this resource.
- **Discount-uses recompute (Container-level)** — the Container Discount's `uses` counter is recomputed (not incremented) on every related order's status change via a 10-second-delayed job on the `order-events6` queue. Cancelled / refunded orders free the slot back up — see [[discount-stacking]].
- **No audit log** — no actor, no diff history, no created_by / updated_by. Only the row's `created_at` / `updated_at` are written.
- **DB-unique constraint platform-wide** — `discount_codes.code` is unique across the ENTIRE table, not per merchant. Attempting to POST a code that already exists on ANY merchant's store returns 422 with `code` error pointer.

## Equivalent UI

- [[marketing-discounts-codes]] — admin-panel Container codes list.
- [[marketing-discounts]] — parent Discount type picker (stacking / cap live on the Container).

## Related

- [[api-discount-codes]] — hub.
- [[json-api-v2]] — API hub.
- [[api-discounts]] — Container Discount endpoint (carries `code_apply`, `total_value`, `uses`).
- [[discount-stacking]] — Container stacking, uses-recompute.
- [[discount-code]] — Discount Code entity reference.
- [[settings-hooks]] — `discount.*` events (no dedicated `discount_code.*` event exists).

## Open questions

None.
