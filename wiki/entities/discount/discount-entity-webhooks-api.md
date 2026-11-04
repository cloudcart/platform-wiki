---
type: entity
nav_path: "Entity → Discount → Webhooks and API"
aliases: ["Discount webhooks", "Discount API", "Discount JSON-API v2", "discount.created", "discount.updated", "discount.deleted"]
tags: [marketing, discounts, entity, webhooks, api]
created: 2026-06-10
updated: 2026-11-04
source_count: 6
---

# Discount — Webhooks and API

> Part of [[discount]]. See the hub for related aspects (fields, lifecycle, business rules, stacking).

## Identity

How the Discount entity is exposed for programmatic access — webhook events and the JSON-API v2 endpoints and allowlist.

## Aliases

- "Discount webhooks" — the three `discount.*` events fired via [[settings-hooks]].
- "JSON-API v2 discounts" — the public API surface at [[api-discounts]].

## Key Attributes

### Webhook events

Three webhook events fire via [[settings-hooks]]:

| Event | When |
|-------|------|
| `discount.created` | A discount record is saved for the first time through the form or JSON-API. |
| `discount.updated` | A discount record is saved through the form or JSON-API. |
| `discount.deleted` | A discount is deleted through JSON-API. |

The Active switch, bulk status, list delete, `changeDiscountsStatus`, `discountsBulkDelete`, the expiry sweep, the uses recount, and any change to Fixed products, Code PRO codes or Container codes send none.

### JSON-API v2 endpoints

The Discount entity is exposed via **JSON-API v2** — see [[api-discounts]] for endpoints, attributes, relationships, and validation.

**Attributes exposed:** `type`, `type_value`, `settings`, `code`, `date_start`, `date_end`, `max_uses`, `maxused_user`, `customer_groups_target`, `geo_zone_id`, `code_apply`, `apply_regular_price`, `force_save`, plus the visual / display fields catalogued in [[discount-entity-fields]].

**Relationships:** `products`, `categories`, `vendors`, `selections`, `customer-groups`, `geo-zone`.

### Side effects of an API write

Reads use the `index` / `show` endpoints. A POST / PATCH runs the same save steps as the admin form:

- Plan quota check on create (HTTP **402** over quota).
- Per-variant row recompute (see [[discount-entity-lifecycle]]).
- Smart-collection refresh.
- Listing-engine repath.
- `discount.created` / `discount.updated` webhooks via [[settings-hooks]].

Neither API runs the admin form's checks; the three paths have separate validation.


### Type allowlist

JSON-API v2 writes allow **5 types**:

- `percent`
- `flat`
- `fixed`
- `shipping`
- `code-pro`

The admin panel also creates Quantity, Countdown and Container discounts; those cannot be created via JSON-API v2.


### `uses` counter recompute parity

The `uses` counter is recomputed identically (a 10-second-delayed job) on order-status changes regardless of how the discount was created — admin UI or API. See [[discount-entity-lifecycle]] for the full recompute semantics.

### Error responses

- **HTTP 402** — over a plan quota on create (`discount_global`, `discount_fixed` or `discount_coupon`).
- **HTTP 422** — validation failure from the API's own rules. The admin form's checks do not run here, so a percent is not limited to 100, and values are stored as sent (percent × 100, so 1000 means 10%).

## Where it appears

- [[api-discounts]] — the JSON-API v2 endpoint catalogue.
- [[settings-hooks]] — the webhook subscription screen where merchants enable `discount.created` / `discount.updated` / `discount.deleted`.
- [[json-api-v2]] — the cross-cutting API concept (authentication, rate-limit).

## Related

- [[discount]] — hub.
- [[discount-entity-fields]] — fields exposed via the API.
- [[discount-entity-lifecycle]] — `uses` recompute (parity with admin).
- [[discount-entity-business-rules]] — the admin form's rules and amount limits.
- [[api-discounts]] — endpoint reference.
- [[settings-hooks]] — webhook subscription.
- [[json-api-v2]] — API concept.
- [[plan-gates]] — per-type plan-feature counters (HTTP 402 overflow).

## Open Questions

None.
