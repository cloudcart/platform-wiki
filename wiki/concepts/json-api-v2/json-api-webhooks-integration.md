---
type: concept
nav_path: "Concept → JSON-API v2 → Webhook integration"
aliases: ["JSON-API v2 webhooks", "API writes fire webhooks", "API webhook side-effects", "product.created via API", "order.updated via API", "JSON-API webhook parity"]
tags: [api, json-api, webhooks, hooks, integration, concepts]
created: 2026-06-10
updated: 2026-11-09
source_count: 3
---

> Part of [[json-api-v2]]. See the hub for the other aspects (auth, headers/envelope, pagination, filtering & sorting, endpoints, status codes, audit log, CORS & soft-delete, atomic operations).

# JSON-API v2 — Webhook integration

## Definition

**API writes fire the same webhooks as admin UI writes, with one exception: products.** Most events (`order.updated`, `customer.created`, `discount.created`, `subscriber.created`, `product.deleted`, etc.) are dispatched **at the data layer where the record is saved**, so an API write fires them exactly as an admin save does.

**`product.created` and `product.updated` fire only from saves in the admin panel.** A product created or changed through JSON-API v2 (or the Admin GraphQL API) sends neither, and nor do background imports ([[products-products]]). The one API exception: saving only a product's metafield values through Admin GraphQL sends `product.updated` ([[metafields-webhooks]]). An integration that needs to react to API product writes should act on its own write's response rather than wait for a webhook. (To tell writers apart for **audit**, see [[json-api-audit-log]].)

## Scope

- The parity rule, and the product exception.
- The hook-dispatch location (data layer, not request-handler layer) and why that matters.
- API-specific side-effects layered on top:
  - Products / variants change-log capture (`initiator = "api"` + key id + name).
  - Subscribers force-set to `subscribed_from = "API"`.
  - Orders routed through the shared status-change path which fires `order.updated` + status-transition side-effects.
- Practical implications for webhook subscribers.

Not covered:

- The audit-log mechanism for who-did-what — see [[json-api-audit-log]].
- The webhook subscription model and delivery semantics (retry, headers, signing) — see [[settings-hooks]] + [[notification-delivery]].
- The `webhooks` resource (programmatic management of subscriptions) — see [[json-api-endpoints]].

## Contrasts

- **JSON-API v2 vs Admin GraphQL** — both behave identically for hook subscribers, including the product exception.
- **Webhook side-effect (behavioural) vs audit-log entry (forensic)** — webhooks fire regardless of who wrote the data; audit-log capture is per-resource and inconsistent (see [[json-api-audit-log]]).
- **API writes vs storefront writes** — storefront mutations (cart/customer) also fire model-layer hooks. For products, only an admin-panel save sends `product.created` / `product.updated`.

## How it works

### Hook dispatch from the data layer

Webhook events (`order.updated`, `discount.created`, `customer.created`, `subscriber.created`, `product.deleted`, etc.) are dispatched at the data layer when a record is created / updated / deleted, NOT from the request handler. Two consequences:

1. **Every code path that saves the record fires the hook** — JSON-API v2, Admin GraphQL, the admin panel, the storefront, scheduled tasks, imports. Product create/update are the exception (above).
2. **Hook subscribers cannot tell** (from the event payload alone) which code path triggered the save. The event payload carries the record state, not the actor identity. For actor identity, the integrator must consult the audit log — see [[json-api-audit-log]].

### Common API write → webhook event mapping

| API write | Triggered webhook event | Notes |
|---|---|---|
| `POST /api/v2/products` | none | `product.created` fires only for admin-panel saves. |
| `PATCH /api/v2/products/{id}` | none | `product.updated` fires only for admin-panel saves. |
| `DELETE /api/v2/products/{id}` | `product.deleted` | Soft-delete sets `deleted_at`; the hook still fires. See [[json-api-cors-soft-delete]] for soft-delete read semantics. |
| `PATCH /api/v2/orders/{id}` (status change) | `order.updated` + any status-transition side-effects (invoice issue, customer email, etc.) | Routed through the shared status-change path. |
| `PATCH /api/v2/orders/{id}/fulfill` | `order.updated` (with fulfillment side-effect) | Custom route — the side-effect chain is identical to the admin **Fulfill products** action. |
| `POST /api/v2/customers` | `customer.created` | Records an API-origin flag for the audit trail. |
| `POST /api/v2/subscribers` | `subscriber.created` | Subscriber row has `subscribed_from = "API"` (force-set). |
| `POST /api/v2/discounts` | `discount.created` | No actor recorded in audit log — only `created_at` timestamp. |

### API-specific side-effects layered on top

In addition to the standard webhook events, API writes carry a small set of "this was the API" markers:

- **Products / variants change-log:** a separate per-line change-log records who edited which attribute. API writes are tagged with `initiator = "api"` AND capture the calling API key's id + name (verified for variants; products only capture the request IP). See [[json-api-audit-log]] for the full per-resource matrix.
- **Subscribers** created via API have `subscribed_from = "API"` so reports / segments can identify API-originated entries.
- **Orders** changed via API go through the shared status-change path which fires the standard `order.updated` webhook and any status-transition side-effects (invoice issue, customer email, etc.) — identical chain to the admin path. The order-history row records `namespace = "api2"`.

### Practical implications for webhook subscribers

- **Idempotency is mandatory.** Events can repeat for one change; subscribers that mutate downstream systems should dedupe.
- **API product writes are silent.** A product sync over the API cannot rely on `product.created` / `product.updated` to trigger its own follow-up steps.
- **The webhook does NOT carry actor identity.** A subscriber that needs to know "was this an API write or an admin write?" must consult the resource's audit log (only orders + products/variants have one — see [[json-api-audit-log]]).
- **Status-transition side-effects can cascade.** A `PATCH /orders/{id}` that changes status to `paid` fires `order.updated` AND triggers stock decrement (see [[inventory-decrement-timing]]) AND may trigger the invoice-issue side-effect AND the customer-email side-effect. The webhook subscriber sees one `order.updated` event but the downstream chain can be long.
- **Webhook-to-API-key association.** Webhooks created via `POST /api/v2/webhooks` are associated with the calling API key. Deleting that key (see [[json-api-auth]]) can affect those hook subscriptions; verify before deleting if the key has active hooks.

## Where it applies

- Every API write across the writable resources fires its record-save event (and any subscribed webhook), except product create / update.
- The `webhooks` resource itself supports CRUD via the API — so integrations can self-subscribe to events (see [[json-api-endpoints]] + [[settings-hooks]] for the admin UI equivalent).
- Status-transition side-effects on orders (invoice issue, customer notification, inventory decrement) are triggered by API writes the same as admin writes.

## Related

- [[json-api-v2]] — hub.
- [[json-api-audit-log]] — the forensic counterpart: who did the write.
- [[json-api-endpoints]] — the `webhooks` resource for programmatic subscription management.
- [[settings-hooks]] — admin UI for webhook subscriptions.
- [[notification-delivery]] — outbound delivery semantics, retries, failure handling.
- [[inventory-decrement-timing]] — order status changes via API also trigger the decrement chain.

## Open Questions

- **Per-event actor metadata** — the webhook payload doesn't carry actor identity (admin user vs API key vs storefront). A future addition to the payload (e.g., `meta.actor: {type: "api", key_id: 42}`) would let subscribers branch on origin without consulting the per-resource audit log `(verify roadmap)`.
