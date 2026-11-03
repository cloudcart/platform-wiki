---
type: entity
aliases: ["Webhook configuration", "Webhook setup", "Webhook fields", "Webhook destination URL", "Webhook custom headers", "Конфигурация на уебхук", "Настройка на уебхук"]
tags: [settings, developer, webhooks, integrations, configuration, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

# Webhook — Configuration

> Part of [[webhook]]. See the hub for the other aspects (events, delivery, failure handling, logging).

## Identity

**Configuration** is the set of fields the merchant fills in when creating a [[webhook|Webhook]] on [[settings-hooks]]. A Webhook is purely a **subscription definition** — it does not itself carry any event payload (that is per-delivery, see [[webhook-entity-delivery]]). Creating, editing, or deleting a Webhook is a synchronous database write with immediate effect: the next matching event fires the new configuration. The Webhook ties together a destination URL, a single event (see [[webhook-entity-events]]), an [[api-key|API Key]], optional custom headers, and an Active toggle.

## Aliases

- **Webhook configuration** / **Webhook setup** — the act of defining a subscription.
- **Webhook fields** — the individual configurable attributes.
- **Конфигурация на уебхук** / **Настройка на уебхук** — Bulgarian equivalents.

## Key Attributes

| Attribute | What the merchant controls | Notes |
|-----------|----------------------------|-------|
| **Destination URL** (`url`) | Required full HTTP(S) URL | Where CloudCart POSTs the event payload. Validated as a URL at create time. Must respond within 5 seconds; certain status codes auto-disable the Webhook — see [[webhook-entity-failure-handling]]. |
| **Event** (`event`) | Pick one from the catalog of 20 events | One Webhook = one event. To subscribe to multiple events, create multiple Webhook rows. See [[webhook-entity-events]]. |
| **API key** (`api_key_id`) | Required pick from the store's [[api-key|API Keys]] | The Key's value is auto-injected as the `X-CloudCart-ApiKey` header on every delivery — see [[webhook-entity-delivery]]. Deleting an API Key referenced by ANY Webhook is blocked by the platform. |
| **Active** | Toggle switch | When OFF, the Webhook stays configured but is skipped when the event fires. The platform AUTO-FLIPS this OFF on permanent-failure responses (see [[webhook-entity-failure-handling]]). The merchant must manually toggle it back ON after fixing the receiver. |
| **Custom headers** | Free-form key/value pairs | Sent alongside the auto-added `X-CloudCart-ApiKey` header. Use for the merchant's own auth scheme (HMAC signatures, Bearer tokens) or the receiver's content-routing needs. |
| **"It is used on a new structure"** toggle | Only appears for `order.created` / `order.updated` | Selects the v2 payload shape vs the legacy shape. The default and recommended choice for new integrations is the v2 shape — it matches the public REST API model and is more stable across CloudCart upgrades. |

Configuration rules:

- **One Webhook = one event.** A single Webhook subscribes to exactly one event. Each row has its own URL, API key, custom headers, and Active toggle. To listen to multiple events, create one row per event.
- **Plan-included — no per-Webhook quota.** There is no plan-gate on the number of Webhooks; every plan (including the free Start Up) can configure unlimited Webhooks. The only constraint is the shared delivery infrastructure (5-second timeout, 15-minute retry window — see [[webhook-entity-delivery]]), not a per-store quota. Failed attempts do NOT consume any merchant-visible rate-limit.
- **Site ID chip in the page header.** [[settings-hooks]] shows the store's Site ID as a chip — most receivers want it to identify which CloudCart store an event came from (useful for receivers serving multiple stores).
- **Deleting a linked API Key is blocked.** Deleting an API Key referenced by a Webhook fails with a clear error; the merchant must reassign or delete the Webhook first.

A Webhook is **store-scoped, not user-scoped** — it does not belong to a [[staff-member|Staff member]], has no per-staff visibility filtering (every moderator with the `settings.hooks` permission sees the same list), and is never auto-recreated after deletion. Once removed (by the merchant or by the `please unsubscribe me` auto-delete — see [[webhook-entity-failure-handling]]), the subscription is gone permanently and must be re-created from [[settings-hooks]].

## Where it appears

- [[settings-hooks]] — the master management screen: list, create, edit, toggle Active, delete, bulk-delete.
- [[settings-api-keys]] — the API Keys list shows in-use references; deleting a Key with a Webhook referencing it is blocked.

## Related

- [[webhook]] — hub.
- [[api-key]] — every Webhook references an API Key; FK-blocks Key deletion when in use.
- [[settings-hooks]] — the configuration screen.
- [[settings-api-keys]] — API Key management.
- [[staff-member]] — Webhooks are store-scoped, not bound to a staff member.
- [[plan-gates]] — no plan-gate on Webhook count.

## Open Questions

None.
