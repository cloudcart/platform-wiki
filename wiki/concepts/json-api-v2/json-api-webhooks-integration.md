---
type: concept
nav_path: "Concept → JSON-API v2 → Webhook integration"
aliases: ["JSON-API v2 webhooks", "API writes fire webhooks", "API webhook side-effects", "product.created via API", "order.updated via API", "JSON-API webhook parity"]
tags: [api, json-api, webhooks, hooks, integration, concepts]
created: 2026-06-10
updated: 2026-08-06
source_count: 2
---

> Part of [[json-api-v2]]. See the hub for the other aspects (auth, headers/envelope, pagination, filtering & sorting, endpoints, status codes, audit log, CORS & soft-delete, atomic operations).

# JSON-API v2 — Webhook integration

## Definition

**API writes fire the same webhooks as admin UI writes.** Both code paths go through the same record-save lifecycle, and webhook events (`product.created`, `order.updated`, `discount.created`, `customer.created`, `subscriber.created`, etc.) are dispatched **at the data layer where the record is saved** — not from the request handler. An integrator who creates a product via `POST /api/v2/products` will trigger the same `product.created` webhook deliveries to subscribed receivers as if the admin had clicked "Save" in the admin UI.

This parity is the cornerstone of "API as a peer of the admin panel" — it means automation that subscribes to webhooks does NOT need to distinguish between admin-UI-driven and API-driven changes for behavioural purposes. (If they need to distinguish for **audit** purposes, see [[json-api-audit-log]].)

## Scope

- The parity guarantee — API writes fire the same webhooks as admin UI writes.
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

- **JSON-API v2 webhook parity vs admin GraphQL webhook parity** — both fire from the same data layer, so both behave identically for hook subscribers.
- **Webhook side-effect (behavioural) vs audit-log entry (forensic)** — webhooks fire regardless of who wrote the data; audit-log capture is per-resource and inconsistent (see [[json-api-audit-log]]).
- **API writes fire webhooks vs storefront writes fire webhooks** — storefront mutations (cart/customer) also fire model-layer hooks. The webhook subscriber sees the same `product.updated` whether the change came from API, admin SPA, storefront customer action, scheduled job, or bulk import.

## How it works

### Hook dispatch from the data layer

Webhook events (`product.created`, `order.updated`, `discount.created`, `customer.created`, `subscriber.created`, etc.) are dispatched at the data layer where the record is saved — specifically when a record is created / updated / deleted — NOT from the request handler. This design choice has two consequences:

1. **Every code path that saves the record fires the hook** — the JSON-API v2 path, the admin GraphQL mutation, the admin SPA, the storefront mutation, scheduled tasks, command-line tools, bulk imports — all share the same save path and therefore all fire the same hook events.
2. **Hook subscribers cannot tell** (from the event payload alone) which code path triggered the save. The event payload carries the record state, not the actor identity. For actor identity, the integrator must consult the audit log — see [[json-api-audit-log]].

### Common API write → webhook event mapping

| API write | Triggered webhook event | Notes |
|---|---|---|
| `POST /api/v2/products` | `product.created` | Fires before search-engine sync; receivers must be idempotent. |
| `PATCH /api/v2/products/{id}` | `product.updated` | Chatty — fires on every stock save too; see [[settings-hooks]]. |
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

- **Idempotency is mandatory.** The `product.updated` webhook fires on every save — including every stock decrement, every search-engine sync, every bulk-import row. Subscribers that mutate downstream systems on every event will create duplicate work unless they dedupe.
- **The webhook does NOT carry actor identity.** A subscriber that needs to know "was this an API write or an admin write?" must consult the resource's audit log (only orders + products/variants have one — see [[json-api-audit-log]]).
- **Status-transition side-effects can cascade.** A `PATCH /orders/{id}` that changes status to `paid` fires `order.updated` AND triggers stock decrement (see [[inventory-decrement-timing]]) AND may trigger the invoice-issue side-effect AND the customer-email side-effect. The webhook subscriber sees one `order.updated` event but the downstream chain can be long.
- **Webhook-to-API-key association.** Webhooks created via `POST /api/v2/webhooks` are associated with the calling API key. Deleting that key (see [[json-api-auth]]) can affect those hook subscriptions; verify before deleting if the key has active hooks.

## Where it applies

- Every API write across all 31 writable resources fires the corresponding record-save event (and therefore any subscribed webhook).
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
