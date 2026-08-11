---
type: entity
nav_path: "Entity → Discount → Webhooks and API"
aliases: ["Discount webhooks", "Discount API", "Discount JSON-API v2", "discount.created", "discount.updated", "discount.deleted"]
tags: [marketing, discounts, entity, webhooks, api]
created: 2026-06-10
updated: 2026-06-10
source_count: 6
---

# Discount — Webhooks and API

> Part of [[discount]]. See the hub for related aspects (fields, lifecycle, business rules, stacking).

## Identity

How the Discount entity is exposed for programmatic access — webhook events on CRUD, the internal `DiscountStatusChange` event used by the admin UI, and the JSON-API v2 endpoints / allowlist / same-side-effects guarantee.

## Aliases

- "Discount webhooks" — the three `discount.*` events fired via [[settings-hooks]].
- "JSON-API v2 discounts" — the public API surface at [[api-discounts]].

## Key Attributes

### Webhook events

Discount CRUD fires three webhook events via [[settings-hooks]]:

| Event | When |
|-------|------|
| `discount.created` | A discount is created. |
| `discount.updated` | A discount is edited or its `active` toggled. |
| `discount.deleted` | A discount is deleted. |

PRO child-code CRUD fires the parent discount's `discount.updated` event, not a separate event. (verify)

### Internal `DiscountStatusChange` event (admin UI only)

Toggling a discount's `active` flag fires the internal `DiscountStatusChange` event (broadcasted on the `discount` private channel for real-time admin UI updates) IN ADDITION to the `discount.updated` webhook. The webhook captures all discount edits including the active toggle; the broadcast event is specifically for the admin UI's per-product attachment regeneration spinner.

This event is **internal** — merchants subscribing to webhooks should rely on `discount.updated`, not the private channel.

### JSON-API v2 endpoints

The Discount entity is exposed via **JSON-API v2** — see [[api-discounts]] for endpoints, attributes, relationships, and validation.

**Attributes exposed:** `type`, `type_value`, `settings`, `code`, `date_start`, `date_end`, `max_uses`, `maxused_user`, `customer_groups_target`, `geo_zone_id`, `code_apply`, `apply_regular_price`, `force_save`, `msrp`, plus the visual / display fields catalogued in [[discount-entity-fields]].

**Relationships:** `products`, `categories`, `vendors`, `selections`, `customer-groups`, `geo-zone`.

### Same-side-effects principle

Reads use the `index` / `show` endpoints; writes (POST / PATCH / DELETE) trigger **the same pipeline as the admin-panel save**:

- Plan-feature usage-counter consumption (HTTP **402** on overflow).
- Per-product attachment recompute (see [[discount-entity-lifecycle]]).
- Smart-collection refresh.
- Listing-engine repath.
- The 10-minute activation cooldown.
- `discount.created` / `discount.updated` / `discount.deleted` webhooks via [[settings-hooks]].
- Audit-log entry with `api2` as the source.

### Type allowlist (admin parity)

API writes are subject to the **same 5-type allowlist** as the admin-panel:

- `percent`
- `flat`
- `fixed`
- `shipping`
- `code-pro`

`quantity` and `countdown` discounts cannot be created via JSON-API v2 (admin-panel only).

### `uses` counter recompute parity

The `uses` counter is recomputed identically (10-second-delayed job on `order-events6` queue) on order-status transitions to counted statuses regardless of how the parent discount was created — admin UI or API. See [[discount-entity-lifecycle]] for the full recompute semantics.

### Error responses

- **HTTP 402** — plan-feature overflow (e.g., trying to create a 6th `discount_global` on a 5-cap plan).
- **HTTP 422** — validation failure (e.g., `date_end <= date_start`, `flat` over 100,000 cents, etc. — see [[discount-entity-business-rules]] for the full validation set).

## Where it appears

- [[api-discounts]] — the JSON-API v2 endpoint catalogue.
- [[settings-hooks]] — the webhook subscription screen where merchants enable `discount.created` / `discount.updated` / `discount.deleted`.
- [[json-api-v2]] — the cross-cutting API concept (authentication, rate-limit, same-side-effects principle).

## Related

- [[discount]] — hub.
- [[discount-entity-fields]] — fields exposed via the API.
- [[discount-entity-lifecycle]] — `uses` recompute (parity with admin).
- [[discount-entity-business-rules]] — validation enforced on API writes (HTTP 422).
- [[api-discounts]] — endpoint reference.
- [[settings-hooks]] — webhook subscription.
- [[json-api-v2]] — API concept.
- [[plan-gates]] — per-type plan-feature counters (HTTP 402 overflow).

## Open Questions

None.
