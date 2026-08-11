---
type: entity
aliases: ["Webhook events", "Webhook event catalog", "Supported webhook events", "Webhook event types", "Уебхук събития", "Каталог на събитията"]
tags: [settings, developer, webhooks, integrations, events, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

# Webhook — Event catalog

> Part of [[webhook]]. See the hub for the other aspects (configuration, delivery, failure handling, logging).

## Identity

The **event catalog** is the fixed list of platform events a [[webhook|Webhook]] can subscribe to. Each Webhook subscribes to **exactly one** event from this catalog. The catalog is **7 entity types × 3 actions** (created / updated / deleted) = a theoretical 21, but `order.deleted` is disabled at the code level, so the picker on [[settings-hooks]] shows **20 events**. The event name is what tells the receiver *what happened* — a POST arriving from a `product.created` Webhook means a new product was just added; a POST from `customer.updated` means a customer record changed. The event also dictates which entity gets serialised into the delivery payload (see [[webhook-entity-delivery]]).

## Aliases

- **Webhook events** / **Webhook event types** — the merchant-facing collective term for the subscribable catalog.
- **Supported webhook events** — phrasing used in integration docs when listing what can be wired up.
- **Уебхук събития** / **Каталог на събитията** — Bulgarian equivalents.

## Key Attributes

The 20 supported events (7 entity types × 3 actions, minus `order.deleted`):

| Entity | Events |
|--------|--------|
| **Category** | `category.created`, `category.updated`, `category.deleted` |
| **Vendor** | `vendor.created`, `vendor.updated`, `vendor.deleted` |
| **Product** | `product.created`, `product.updated`, `product.deleted` |
| **Discount** | `discount.created`, `discount.updated`, `discount.deleted` |
| **Customer** | `customer.created`, `customer.updated`, `customer.deleted` |
| **Order** | `order.created`, `order.updated` (v2 payload toggle available on both); `order.deleted` is **disabled** — picker does NOT show it |
| **Subscriber** | `subscriber.created`, `subscriber.updated`, `subscriber.deleted` |

Firing semantics merchants must understand:

- **`*.updated` fires on EVERY save of the entity, not just on a meaningful change.** `order.updated` fires on a status change, an address edit, a payment confirmation, a line-item edit, an archive toggle, and so on. Receivers that only care about one kind of change must inspect the payload and filter themselves — the platform does NOT offer per-field event subscriptions. `product.updated` is similarly chatty: every stock decrement on an order fires it (see [[inventory-tracking]]), so receivers must be idempotent.
- **`order.deleted` is currently disabled at the code level.** No Webhook can subscribe to order deletion today. Archiving an order is a hide (not a delete) and has never fired `order.deleted`; permanent order delete on [[orders-details]] also does NOT propagate to Webhooks. Merchants who need this signal must poll the order list via [[api-orders]], or rely on related `customer.*` events.
- **One Webhook = one event.** To listen to several events (e.g. `order.created` + `order.updated`), the merchant creates one Webhook row per event — see [[webhook-entity-configuration]].

## Where it appears

- [[settings-hooks]] — the event picker (a dropdown of the 20 events) when creating or editing a Webhook.
- [[api-orders]] — the polling fallback for the missing `order.deleted` signal.
- [[notification-delivery]] — the same platform event stream also drives email / SMS / admin-panel alerts.

## Related

- [[webhook]] — hub.
- [[order]] — `order.created` / `order.updated` fire on order CRUD; `order.deleted` disabled.
- [[product]] — `product.*` events; `product.updated` is chatty (fires on stock changes).
- [[customer]] — `customer.*` events.
- [[category]] — `category.*` events.
- [[vendor]] — `vendor.*` events.
- [[discount]] — `discount.*` events.
- [[subscriber]] — `subscriber.*` events.
- [[inventory-tracking]] — stock changes fire `product.updated`.
- [[settings-statuses]] — status changes drive `order.updated`; the payload carries the status CODE, not the renamed label.

## Open Questions

None.
