---
type: entity
nav_path: "Entity → Order Status → JSON-API v2 access"
aliases: ["Order Status API", "PATCH order status", "Status code in webhooks", "Webhook payload stable rename", "API status validation"]
tags: [entity, orders, statuses, api, webhooks]
created: 2026-06-10
updated: 2026-08-06
source_count: 3
---

> Part of [[order-status]]. See the hub for the other aspects (canonical values, relationships, custom statuses, side-effects, edge cases).

# Order Status — JSON-API v2 access

## Identity

The order's `status` field is exposed via **JSON-API v2** — see [[api-orders]] for PATCH semantics, allowed values, and validation. The API mirrors the admin UI for status changes: the same 6 mutable canonical statuses + custom statuses are settable, the same hard gates apply, and the same 7-step side-effect cascade fires (see [[order-status-entity-side-effects]]). Webhook payloads carry the unchanged status CODE regardless of merchant renames.

## Aliases

- **PATCH order status** — the JSON-API v2 mutation.
- **`api2` namespace** — how API-driven history entries are attributed (rendered as "API" in [[orders-history]]).
- **`order.updated` webhook** — the event fired on every status change.
- **Status code stability** — the rule that webhooks emit codes, not labels.

## Key Attributes

### Settable vs gateway-only statuses via the API

The API supports the same 6 mutable canonical statuses + custom statuses available in the admin dropdown:

- `authorized`, `pending`, `paid`, `completed`, `cancelled`, `refunded` (mutable from UI / API)
- All custom statuses (slug-form, e.g., `order-awaiting-confirmation`)

The 5 gateway-driven statuses (`chargebacked`, `disputed`, `timeouted`, `failed`, `voided`) are **NOT settable** via the API — they're emitted only by payment-provider sync. See [[order-status-entity-canonical-values]] for the dropdown-vs-full-list distinction. (verify)

### Same hard gates apply

Status PATCH through JSON-API v2 runs through the same `validateChangeStatus` rule set as the UI:

- Rejects `completed` unless `paid` + `fulfilled`.
- Rejects `cancelled` on paid/completed orders.
- Rejects ANY status change on archived orders.
- Rejects when order-total exceeds authorized-amount (for `authorized → paid` capture).

The error messages match the UI variants (see [[order-status-entity-side-effects]] hard-gates table).

### Same side effects

Every API-driven status change fires the same 7-step cascade as a UI change:

1. History entry — with `api2` as the acting namespace, rendered as "API" in [[orders-history]].
2. Customer notification — the single status-change email template, when the order's `notify_customer` flag, the template's own active flag and the store-wide `customer_email_notifications` all allow it. There is no per-status toggle.
3. Stock decrement / restore — driven by `order_status_for_quantity_decrease` setting on [[settings-cart]].
4. Discount uses recount — driven by `discounts_used_statuses` on [[settings-cart]].
5. Negative-status authorization auto-cancel — see [[order-status-entity-edge-cases]].
6. Fulfillment auto-reset on negative status — see [[order-status-entity-edge-cases]].
7. Auto-created system return + the reversal lock on a cancelled / refunded committed sale — see [[order-status-entity-edge-cases]].
8. Auto-promotion to `completed` — if state matches `paid` + `fulfilled` + `order_complete = 1`.
9. `order.updated` webhook fires — with the unchanged status CODE.

### Webhook payload — stable across renames

The `status` field in the `order.updated` webhook payload always carries the **unchanged code**, never the merchant's renamed label.

- For built-ins: even if the merchant renames `pending` to "Awaiting confirmation" in [[settings-statuses]], the webhook payload's `status` field stays `pending`.
- For custom statuses: the payload carries the **stored slug** (e.g., `order-awaiting-confirmation`), NOT the display name. Renaming the display label does NOT change the key — integrations remain stable across renames. See [[order-status-entity-custom-statuses]] for the slug-generation rule.

This stability guarantee is the reason renames are safe for downstream tooling (analytics pipelines, fulfillment systems, accounting integrations).

### Webhook delivery is NOT serialized per-order

The platform fires each `order.updated` event independently — there is no per-Order serialization queue. If two status changes happen seconds apart and the subscriber's endpoint is slow, the second delivery can arrive **before** the first finishes processing. Subscribers should sort by the Order's `date_last_update` (carried in the payload) rather than rely on HTTP delivery order. (verify)

### Webhook events related to status

| Event | When it fires |
|-------|---------------|
| `order.created` | Order is first created (storefront submission, admin-placed Create order, API POST). Payload carries the initial status (`pending` default, `authorized` for pre-auth). |
| `order.updated` | ANY status change. Payload carries the new CODE (built-in) or slug (custom). |
| `order.deleted` | Order is hard-deleted from the system (rare — see [[orders-archive]] for the soft-delete model). |

All three are subscribable in [[settings-hooks]]. See [[json-api-v2]] for authentication and the side-effects principle.

## Where it appears

- [[api-orders]] — JSON-API v2 endpoint with PATCH semantics, allowed values, and validation.
- [[json-api-v2]] — API hub with auth + side-effects overview.
- [[settings-hooks]] — `order.created` / `order.updated` / `order.deleted` webhook subscriptions.
- [[orders-history]] — API-driven changes appear with `api2` namespace ("API" in the UI).
- [[settings-api-keys]] — PAT tokens for API authentication.

## Related

- [[order-status]] — hub.
- [[order-status-entity-side-effects]] — the full 7-step cascade the API triggers.
- [[order-status-entity-custom-statuses]] — slug-form for custom statuses in webhook payloads.
- [[order-status-entity-canonical-values]] — settable vs gateway-only statuses.
- [[api-orders]] — JSON-API v2 endpoint page.
- [[json-api-v2]] — API hub.

## Open Questions

None.
