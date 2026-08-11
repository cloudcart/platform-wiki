---
type: feature
nav_path: "Settings → Webhooks → Supported events"
route_name: hooks.settings
route_path: /admin/settings/hooks
aliases: ["Webhook events", "Hook events", "Supported events", "Event catalogue", "21 events", "20 events"]
tags: [settings, webhooks, events, integrations]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[settings-hooks]]. See the hub for the other aspects (delivery, retry, auto-disable, modal, activity log, auth & headers).

# Webhooks — supported events & payload

## Purpose

The webhook subscription form requires the merchant to pick exactly one **event** from a fixed catalogue. The catalogue is `7 entity types × 3 actions = 21 events theoretically`, but **`order.deleted` is disabled at the code level** — the picker shows **20 events**. Each event has a stable string name (e.g. `product.updated`) that ships in the outgoing payload, and a payload shape that depends on the event group.

## Where to find it

Sidebar → Settings → **Webhooks** → **+ Add webhook** → **Event** dropdown.

## What the merchant can do here

- Pick exactly one event per webhook subscription. To listen to multiple events, the merchant creates one webhook row per event.
- For `order.created` / `order.updated`, additionally toggle **"It is used on a new structure"** to choose between the v2 and legacy v1 payload schema (see Settings & fields).
- See events grouped by entity in the dropdown (`searchable=true`, `groups=true`, `can-clear=false`).

## Settings & fields

### The 20 supported events, in 7 groups

| Group | Events | Sent when |
|-------|--------|-----------|
| **Category** | `category.created`, `category.updated`, `category.deleted` | A product category is added / edited / removed. |
| **Vendor** | `vendor.created`, `vendor.updated`, `vendor.deleted` | A brand / vendor record changes. |
| **Product** | `product.created`, `product.updated`, `product.deleted` | A product changes. (Stock-only changes also fire `product.updated` — see [[inventory-tracking]].) |
| **Discount** | `discount.created`, `discount.updated`, `discount.deleted` | A discount rule changes. |
| **Customer** | `customer.created`, `customer.updated`, `customer.deleted` | A customer account changes. |
| **Order** | `order.created`, `order.updated` (both support the v2 payload shape via `new_version`); **`order.deleted` is disabled — picker does NOT show it** | An order is placed or modified. Order deletion is currently not webhookable. |
| **Subscriber** | `subscriber.created`, `subscriber.updated`, `subscriber.deleted` | A newsletter subscriber record changes. |

### `order.deleted` quirk

The event-types map has `OrderDeleted` **commented out**. The picker exposes 20 events, not 21. The 6 order-related actions are limited to `order.created` and `order.updated`. Most merchants never need order deletion — orders are archived rather than hard-deleted in normal operations.

### Outgoing payload shape

```
POST <hook.url>
Headers:
  X-CloudCart-ApiKey: <api-key value, auto-added from the linked API key>
  <any merchant-configured custom headers>
  Content-Type: application/json
Body:
  [{ ...payload... }] ← array with one element (the entity serialised as a public API model)
```

- The body is **always an array** with one element — even for single-entity events.
- The entity is serialised through the public API model (same shape as JSON-API v2 — see [[json-api-v2]]).
- Null fields are stripped before sending.

### Order webhook v2 payload structure

`order.created` / `order.updated` (with `new_version` ON — the default) emit a rich **nested** object built by a dedicated order serialiser (not the generic API model). Top-level keys:

- **Identity / status** — `store_id`, `id`, `hash`, `status` (status **code**, not the merchant label), `created_at`, `updated_at`, `email_sent`, `abandoned`, `note_administrator`.
- **Documents** — `invoice_number` / `invoice_date`, `receipt_number` / `receipt_date`, `credit_number` / `credit_date` (all null unless an invoicing provider is active — see [[settings-invoicing]]).
- **Money** — `order_subtotal`, `order_total`, `currency`, plus the arrays `discounts[]`, `tax_vat[]`, `fees[]`.
- **Nested entities** — `customer` (includes its custom fields + geo-IP), `products[]` (each with its line `options`), `shipping[]`, `shipping_address`, `billing_address`, `payments[]` + the primary `payment`, and `weight`.

Each nested section has its own serialiser, so the shape is stable across both order events. Null fields are stripped before sending. **Non-order entity events** (product / customer / category / vendor / discount / subscriber) have **no custom builder** — they serialise the entity through the public API model, so the payload matches that resource's [[json-api-v2|JSON-API v2]] shape.

### v2 vs legacy v1 — the `new_version` toggle

- The **"It is used on a new structure"** switch only **appears in the UI** for `order.created` / `order.updated`.
- For all other event types the backend persists `new_version = 1` by default, but the field is **ignored at delivery time** (only order events read it).
- If CloudCart later extends the v2 schema to other event types, existing webhooks would auto-opt-in. Merchants who want guaranteed v1 should pre-set `new_version = 0` via JSON-API v2 (see [[api-webhooks]]) when creating the subscription. (verify)

### Subscriber events use distinct translation keys

`subscriber.created` / `subscriber.updated` / `subscriber.deleted` use translation keys like `hooks.action.subscriber.created` (not `subscriber.created`) for the human-readable label in the picker — but the actual event string sent to receivers is still `subscriber.created` etc. This is a cosmetic quirk in the picker only.

## Business rules

- **Status CODE, not status label.** When `order.updated` fires on a status transition, the payload carries the order's **status code** (e.g. `paid`, `pending`, `shipped`) — not the renamed merchant-facing label. Receivers must map codes to their own vocabulary. See [[settings-statuses]].
- **Stock-only product changes still fire `product.updated`.** A bulk inventory edit or an ERP sync that touches only the `quantity` field fans out `product.updated` — see [[inventory-tracking]]. Receivers must be idempotent because this event is chatty.
- **`product.*` events fire ONLY from admin-panel saves.** REST API v2 writes, background imports (CSV / XML / ERP), smart-collection re-evaluation, and storefront stock decrement do **not** fire `product.created` / `product.updated` — the search index still re-syncs, but webhook receivers see only admin-panel changes. An integration that writes products via the API will NOT receive its own webhook. See [[products-known-issues]].
- **`order.updated` fires on most order edits — but not all.** It fires on status change, line-item edits, address edits, and payment actions; it does **not** fire on archive / unarchive, the customer-info edit, a payment-method change, or while the order is still a draft. See [[order-pipeline-stage-5-edit]].
- **Two-phase order events.** `order.created` fires once at placement; subsequent changes fire `order.updated`. The full per-stage side-effect timeline (and which stage emits the webhook) is on [[order-processing-pipeline]].
- **One webhook per event.** A receiver wanting both `product.created` AND `product.updated` requires two webhook rows. The platform does NOT collapse them into one subscription.

## Related

- [[settings-hooks]] — hub.
- [[settings-hooks-delivery]] — when the payload actually goes out (sync vs deferred).
- [[settings-hooks-auth-headers]] — `X-CloudCart-ApiKey` injection + custom headers.
- [[api-webhooks]] — programmatic subscription via JSON-API v2 (same event catalogue).
- [[json-api-v2]] — the shared serialisation shape.
- [[settings-statuses]] — order status CODES vs merchant-facing labels in the payload.
- [[inventory-tracking]] — why `product.updated` fires on stock changes.

## Open questions

- Confirm whether `new_version = 0` for non-order events has ever been observed to flip schema for any receiver. (verify)
