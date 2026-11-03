---
type: api-resource
resource_path: /api/v2/webhooks
http_methods: [GET, POST, PATCH, DELETE]
related_entity: webhook
related_features: [settings-hooks]
aliases: ["Webhook event catalog", "Supported webhook events", "20 webhook events", "Webhook event list", "order.deleted disabled", "Valid webhook events 422"]
tags: [api, json-api-v2, infra, webhooks, events]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---

> Part of [[api-webhooks]]. See the hub for the other aspects (CRUD surface, delivery contract, examples).

# Webhooks API — event catalog (JSON-API v2)

## Purpose

The authoritative list of event keys the `event` attribute accepts when creating or updating a webhook through `/api/v2/webhooks`. Read this aspect to answer *"which events can I subscribe to?"*, *"why does `order.deleted` get rejected?"*, and *"is there a `blog.*` event?"* The mechanics of setting the `event` field live in [[api-webhooks-crud]]; what gets delivered when an event fires lives in [[api-webhooks-delivery-contract]].

## Endpoint

The `event` value is set on POST (required) or PATCH (`sometimes`) at `/api/v2/webhooks` — see [[api-webhooks-crud]] for the method table. The validator rejects any string outside the catalogue below with a 422 enumerating the accepted set.

## Attributes

Only the `event` attribute is in scope for this aspect:

| Attribute | Type | Required? | Notes |
|---|---|---|---|
| `event` | string | **yes** on POST; `sometimes` on PATCH | Must be one of the **20 supported events** below. One webhook = one event — to subscribe to multiple events, POST multiple webhook rows. |

### The 20 supported events

The full list of event keys accepted by the `event` validator (per [[settings-hooks]] business rules). `order.deleted` is **disabled at code level** — the constant exists but is commented out — so the catalogue is **20 events in practice, not 21**:

| Group | Events |
|---|---|
| **Category** | `category.created`, `category.updated`, `category.deleted` |
| **Vendor** | `vendor.created`, `vendor.updated`, `vendor.deleted` |
| **Product** | `product.created`, `product.updated`, `product.deleted` |
| **Discount** | `discount.created`, `discount.updated`, `discount.deleted` |
| **Customer** | `customer.created`, `customer.updated`, `customer.deleted` |
| **Order** | `order.created`, `order.updated` (NO `order.deleted` — the constant is commented out) |
| **Subscriber** | `subscriber.created`, `subscriber.updated`, `subscriber.deleted` |

Sending any other string in the `event` attribute returns 422 with the message *"List of valid events: …"* enumerating the accepted set (added by the validator's `after` hook). The full 422 body is shown in [[api-webhooks-examples]].

### Resources with NO webhook events

**There are NO `blog.*`, `post.*`, `tag.*`, `redirect.*`, `webhook.*`, `shipping-provider.*`, or `payment-provider.*` events.** Integrations needing to monitor those resources must **poll** the corresponding API endpoint instead of subscribing.

## Relationships

None. Each event key maps conceptually to one platform entity ([[order]], [[product]], [[customer]], [[category]], [[vendor]], [[discount]], [[subscriber]]), but the webhook row exposes no JSON-API relationship — see [[api-webhooks-crud]].

## Filtering & sorting

Existing subscriptions can be filtered by their event with `filter[event]=order.created` and sorted with `sort=event` / `sort=-event` — see [[api-webhooks-crud]] for the full filter/sort rules.

## Side effects

Choosing an event is purely declarative — it determines **which** platform action will trigger a delivery to this webhook's `url`. Whether a given source of change (admin UI vs REST API vs import) actually fires the matching event is the cross-resource firing question (order events fire on every save; other resources' REST-write firing is unconfirmed — see Open questions). The delivery itself — retry schedule, auth header, auto-disable — is governed by [[api-webhooks-delivery-contract]].

## Equivalent UI

- [[settings-hooks]] — the admin-panel event picker exposes the same 20-event catalogue with the same `order.deleted` omission.

## Related

- [[api-webhooks]] — hub.
- [[settings-hooks]] — admin-panel surface; documents the same event business rules.
- [[webhook]] — entity reference.
- [[order]] / [[product]] / [[customer]] / [[category]] / [[vendor]] / [[discount]] / [[subscriber]] — the entities behind the 20 event types.
- [[api-orders]] / [[api-products]] / [[api-customers]] / [[api-categories]] / [[api-vendors]] / [[api-discounts]] / [[api-subscribers]] — the API resources whose write events fire webhooks subscribed here.

## Open questions

- **`order.deleted` re-enablement** — confirm whether the platform plans to re-enable `order.deleted` (currently commented out) or remove it from the documented catalogue entirely. (verify)
- **Cross-resource firing from REST writes** — whether JSON-API v2 writes fire `product.*` / `customer.*` / `category.*` / etc. webhooks is still unconfirmed; order events are well-established as firing on every save regardless of source. (verify)
