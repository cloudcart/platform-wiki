---
type: entity
nav_path: "Entity → Discount Code → Programmatic access"
aliases: ["Discount code API", "Coupon code API", "JSON-API discount codes", "api-discount-codes", "API код за отстъпка"]
tags: [entity, marketing, discounts, codes, api]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[discount-code]]. See the hub for the other aspects (two-table model, customer binding, usage limits, lifecycle).

# Discount Code — programmatic access

## Identity

This aspect covers how external integrations read and write Discount Codes through **JSON-API v2**. Because the two code types live in two separate tables (see [[discount-code-entity-tables]]), they are exposed as **two separate API resources**. Regular promo codes — the single `code` on a parent discount — are NOT a separate resource; they ride along as an attribute on the discounts resource.

## Aliases

- **Discount codes API** — the Container child-codes resource.
- **Code PRO API** — the Code PRO resource (carries per-code terms + a bulk generate endpoint).

## Key Attributes

The Discount Code entity is exposed via JSON-API v2 through two resources covering the two database tables:

| Resource | Backing table | What each row is |
|----------|---------------|------------------|
| [[api-discount-codes]] | `discount_codes` | A single-use coupon under a parent Container discount, with `code`, `type`, `value`, `active`. |
| [[api-discount-codes-pro]] | `discounts_code_pro` | A code carrying its own discount terms (conditions array, max_uses, customer groups, region, dates) under a parent Code PRO discount, plus a custom `POST /generate` endpoint for bulk generation. |

### Same side effects as the admin panel

A POST / PATCH / DELETE through JSON-API v2 triggers the same pipeline as the admin-panel actions:

- The per-row `active` toggle reflects identically at checkout lookup.
- The parent discount's `uses` counter recompute (a ~10-second-delayed background job on the `order-events6` queue) fires on counted-status transitions — see [[discount-code-entity-usage-limits]].
- The `discounts_code_pro.code` store-wide uniqueness constraint is enforced at the DB level.
- The `discount-code-pro-generator` plan-feature cap (HTTP 402 on overflow) is enforced for the bulk endpoint.
- The audit-log entry is written with `api2` as the source.

### Regular promo codes are an attribute, not a resource

**Regular promo codes** (the `discounts.code` column on the parent discount itself) are NOT a separate resource — they live as the `code` attribute on [[api-discounts]]. Only the two child-code tables get their own resources.

## Where it appears

- [[api-discount-codes]] — Container child codes resource.
- [[api-discount-codes-pro]] — Code PRO codes resource (+ bulk `POST /generate`).
- [[api-discounts]] — parent discounts resource; carries the single regular promo `code` attribute.
- [[settings-api-keys]] — where API authentication credentials are issued.

## Related

- [[discount-code]] — hub.
- [[api-discount-codes]] — Container child-codes resource.
- [[api-discount-codes-pro]] — Code PRO resource.
- [[api-discounts]] — parent discounts resource (regular promo code lives here).
- [[json-api-v2]] — authentication, rate-limit, and the same-side-effects principle.
- [[settings-hooks]] — webhooks fired on code writes.

## Open Questions

None.
