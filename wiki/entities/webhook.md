---
type: entity
aliases: ["Webhook", "Web hook", "HTTP callback", "Event hook", "Outgoing webhook", "Уебхук", "Хук", "Известие за събитие"]
tags: [settings, developer, webhooks, integrations, events, entity]
created: 2026-05-21
updated: 2026-06-10
source_count: 4
---
# Webhook

## Identity

A **Webhook** is an outgoing HTTP callback the merchant configures so that CloudCart automatically POSTs the affected entity to a URL of the merchant's choosing whenever a specific platform event fires — a new order is placed (`order.created`), a customer record is edited (`customer.updated`), a product is removed (`product.deleted`), and similar. It is the platform's **push-based integration mechanism**: instead of an external system polling CloudCart's REST API every few minutes for changes, it subscribes once via a Webhook and CloudCart calls it the moment the event happens. The merchant manages Webhooks on [[settings-hooks]] (Sidebar → Settings → Webhooks).

A Webhook is the merchant's primary way to wire CloudCart into an external ERP / CRM / accounting / fulfillment system without writing polling code. It is **transactional** (one event = one delivery attempt per subscribed Webhook), **fire-and-forget from the merchant's side** (CloudCart handles retries and auto-disabling — see [[webhook-entity-delivery]] + [[webhook-entity-failure-handling]]), and **plan-included** (no plan-gate on the number of Webhooks). So the merchant doesn't police their own receiver uptime — but they DO have to fix a broken receiver before re-enabling.

A Webhook is distinct from an **inbound** webhook (where an external payment provider or courier POSTs INTO CloudCart) — those are handled per-app, not on [[settings-hooks]]. It is also distinct from CloudCart's internal `cc-system6` webhook queue, which is platform-only. See [[notification-delivery]] for how Webhooks fit alongside email, SMS, and admin-panel alerts as parallel consumers of the same event stream.

This entity is split into aspect pages below. The Assistant should drill into the aspect that matches the question, not read every page.

## Sub-pages (in this cluster)

- [[webhook-entity-events]] — the fixed catalog of 20 subscribable events (7 entity types × 3 actions, minus `order.deleted`); `*.updated` fires on every save; `order.deleted` disabled.
- [[webhook-entity-configuration]] — the configurable fields (URL, event, API key, custom headers, Active toggle, v2 payload toggle); one-Webhook-one-event; plan-included; store-scoped.
- [[webhook-entity-delivery]] — the outgoing request shape, `X-CloudCart-ApiKey` header, single-element payload array, last-used count, and the six-attempt 15-minute retry sequence.
- [[webhook-entity-failure-handling]] — retry vs auto-disable vs auto-delete classification; the permanent-failure status codes; the `please unsubscribe me` opt-out; manual re-enable.
- [[webhook-entity-logging]] — the internal-only delivery log (no self-serve admin view), what the merchant CAN see, and the troubleshooting workflow.

## Aliases

- **Webhook** / **Web hook** — the canonical merchant-facing term, used in the admin UI and the [[settings-hooks]] page header.
- **HTTP callback** / **Event hook** — informal phrasings in integration docs and support tickets.
- **Outgoing webhook** — disambiguates the merchant-facing system from inbound webhooks that payment providers / couriers POST into CloudCart.
- **Уебхук** / **Хук** / **Известие за събитие** — Bulgarian labels used interchangeably in the BG admin.

## Key Attributes

A Webhook is a **subscription definition** — it does not itself carry the event payload (that is per-delivery). Its core fields are summarised here; full detail in the aspect pages.

| Attribute | What it is | Aspect |
|-----------|-----------|--------|
| **Destination URL** | Required HTTP(S) URL CloudCart POSTs to | [[webhook-entity-configuration]] |
| **Event** | One event from the catalog of 20 | [[webhook-entity-events]] |
| **API key** | Linked [[api-key|API Key]]; value forwarded as `X-CloudCart-ApiKey` | [[webhook-entity-configuration]] + [[webhook-entity-delivery]] |
| **Custom headers** | Free-form key/value pairs for the merchant's own auth | [[webhook-entity-configuration]] |
| **Active** | Toggle; auto-flipped OFF on permanent failure | [[webhook-entity-failure-handling]] |
| **v2 payload toggle** | "It is used on a new structure" — only for `order.*` | [[webhook-entity-configuration]] |
| **Last-used count** | Increments only on successful delivery | [[webhook-entity-delivery]] |

Key facts: **one Webhook = one event** (create one row per event to subscribe to several); Webhooks are **store-scoped, not user-scoped**; deleting an [[api-key|API Key]] referenced by a Webhook is **blocked**; the platform **auto-disables** broken receivers and **auto-deletes** on the `please unsubscribe me` opt-out.

## Where it appears

- [[settings-hooks]] — the master management screen. List, create, edit, toggle Active, delete, bulk-delete. Site ID chip in the header. Last-used count column.
- [[settings-api-keys]] — shows in-use references; deleting a Key with a Webhook referencing it is blocked.
- [[settings-admin-notifications]] — webhook failure alerts (auto-disable, final give-up) surface here.
- [[settings-queue-view]] — webhook delivery jobs appear on the `order-events8` queue, visible during in-flight retries.

## Related

### Aspect pages

- [[webhook-entity-events]] — event catalog.
- [[webhook-entity-configuration]] — configurable fields.
- [[webhook-entity-delivery]] — request shape + retries.
- [[webhook-entity-failure-handling]] — auto-disable / auto-delete.
- [[webhook-entity-logging]] — logging + troubleshooting.

### Related entities

- [[api-key]] — every Webhook references an API Key for the `X-CloudCart-ApiKey` header; FK-blocks Key deletion when in use.
- [[order]] — `order.created` / `order.updated` fire on order CRUD (v2 payload shape available); `order.deleted` disabled.
- [[product]] — `product.*` events fire on product CRUD.
- [[customer]] — `customer.*` events.
- [[category]] — `category.*` events.
- [[vendor]] — `vendor.*` events.
- [[discount]] — `discount.*` events.
- [[subscriber]] — `subscriber.*` events.
- [[admin-notification]] — auto-disable + final give-up raise an admin-panel alert.

### Cross-cutting concepts

- [[notification-delivery]] — the platform-wide event spine that drives Webhooks alongside email, SMS, and admin alerts.
- [[settings-statuses]] — status changes drive `order.updated`; the payload carries the status CODE, not the renamed label.

## Open Questions

No outstanding questions — all items resolved or distributed to aspect pages.
