---
type: api-resource
resource_path: /api/v2/webhooks
http_methods: [GET, POST, PATCH, DELETE]
related_entity: webhook
related_features: [settings-hooks, settings-api-keys, settings-admin-notifications]
aliases: ["Webhooks API", "Hooks API", "Event subscriptions API", "JSON-API v2 webhooks", "API уебхукове", "API хукове", "/webhooks"]
tags: [api, json-api-v2, infra, webhooks, events]
plan_gates: []
created: 2026-05-26
updated: 2026-06-10
source_count: 5
---
# Webhooks (JSON-API v2)

## Purpose

Programmatic CRUD on the merchant's **webhook subscriptions** — the outbound HTTP callbacks CloudCart fires when specific platform events occur. The API is the programmatic parallel to the admin-panel screen at [[settings-hooks]]; once a webhook is created here it is indistinguishable from one created through the admin UI.

External integrations use this endpoint to **self-register a webhook on install** (a third-party integration can subscribe itself to `order.created` / `product.updated` etc. without the merchant manually configuring it in [[settings-hooks]]), to **read existing subscriptions** for diagnostics or audit, to **bulk-manage subscriptions** across many CloudCart stores from a single integration platform, and to **lifecycle subscriptions** (disable, re-enable, delete). Most integrators favour this over asking the merchant to configure webhooks manually — it lets the integration handshake itself in one programmatic step on install.

This page is the **hub** for the webhooks API cluster. It carries the slim definition + the navigation map; each aspect below carries the full detail for its slice.

## Sub-pages (in this cluster)

This resource is split into 4 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[api-webhooks-crud]] — the REST surface: endpoint table, full attribute reference (`url`, `event`, `active`, `new_version`, `request_headers`, `api_key_id`), relationships, filtering & sorting, and the on-write side effects (auto-fill `api_key_id`, full header-replace, no reachability check, delete-422).
- [[api-webhooks-event-catalog]] — the 20 supported event keys, the disabled `order.deleted` constant, which resources have NO events, and the unknown-event 422.
- [[api-webhooks-delivery-contract]] — runtime delivery behaviour after save: the `X-CloudCart-ApiKey` header, the 6-attempt retry schedule, auto-disable HTTP codes, auto-delete on `please unsubscribe me`, the usage counter, alert surfacing, request shape, order-event queueing, and activity-log gating.
- [[api-webhooks-examples]] — copy-paste curl requests + JSON responses, the common-422 error table, the plan-feature gating rules, and the 7-step testing checklist.

## Endpoint

- **URL base:** `<store-host>/api/v2/webhooks`
- **HTTP methods:** GET (collection + single), POST, PATCH, DELETE — **full CRUD**. One webhook = one event.
- **App requirements:** none — every CloudCart store with at least one API key can subscribe webhooks.

Full method/path table, per-method behaviour, and the `api_key_id` auto-fill rule: see [[api-webhooks-crud]]. Authentication, host resolution, common headers, status codes, and rate limits: see [[json-api-v2]].

## Attributes

The writable attributes are `url` (**required** on POST), `event` (**required** on POST, one of the 20-event catalogue), `active`, `new_version`, `request_headers`, and `api_key_id` (POST-only — read-only on PATCH). Timestamps and `id` are read-only. Full type / validation / writability table + the header full-replace semantics: see [[api-webhooks-crud]]. The accepted `event` values: see [[api-webhooks-event-catalog]].

## Relationships

None exposed via this endpoint. The underlying webhook row references an [[api-key|API Key]] (foreign key `api_key_id`), but the relationship is **not surfaced as a JSON-API relationship** — the key value is auto-forwarded as the `X-CloudCart-ApiKey` header on every delivery. See [[api-webhooks-crud]] for the implicit-reference details.

## Filtering & sorting

No filters are declared explicitly, but the framework auto-merges every column on the `hooks` table into the allowed list (value-equality only) — `filter[event]`, `filter[active]`, `filter[url]`, `filter[api_key_id]`. Sortable: `id`, `url`, `event` (prefix `-` for descending). No include paths. See [[api-webhooks-crud]].

## Side effects

Webhook CRUD here is the **same behaviour as the admin-panel form** on [[settings-hooks]]. On write: `api_key_id` auto-fills to the first API key when omitted; `request_headers` are **fully replaced** on every POST AND PATCH; there is **no reachability check** at save time; DELETE may return 422 `"Not Deletable"`. Full on-write detail: [[api-webhooks-crud]]. After save, the **runtime delivery contract** governs retries, auto-disable, auto-delete, and the auto-injected auth header — see [[api-webhooks-delivery-contract]].

## Equivalent UI

- [[settings-hooks]] — the admin-panel CRUD page (same row shape, same validation, same delivery contract).
- [[settings-api-keys]] — API keys page; deleting a key referenced by a webhook is blocked.
- [[settings-admin-notifications]] — auto-disable + final-give-up alerts surface here.

## Related

- [[json-api-v2]] — API hub.
- [[webhook]] — full entity reference with lifecycle states + per-failure-mode behaviour.
- [[settings-hooks]] — admin-panel management surface (also documents the queue / retry pipeline).
- [[settings-api-keys]] — API keys. Webhooks reference one key for the auto-header. Deletion blocked while referenced.
- [[settings-admin-notifications]] — failure alerts.
- [[api-key]] — API key entity.
- [[notification-delivery]] — concept page on the platform's notification spine.
- [[order]] / [[product]] / [[customer]] / [[category]] / [[vendor]] / [[discount]] / [[subscriber]] — the entities behind the 20 event types.
- [[api-orders]] / [[api-products]] / [[api-customers]] / [[api-categories]] / [[api-vendors]] / [[api-discounts]] / [[api-subscribers]] — the API resources whose write events fire webhooks subscribed here.

## Open questions

- **Webhook firing from JSON-API v2 writes** — confirmed gap in [[api-products]] open questions: admin-panel saves DO fire `product.*` webhooks but REST API and imports historically did NOT. Whether JSON-API v2 writes fire `product.*` / `customer.*` / `category.*` / etc. webhooks is still unconfirmed — verify against the actor-event pipeline. (Order events are well-established as firing on every save regardless of source.) (verify)
- **`new_version` default** — the column defaults to `1` for every webhook; for non-order events it is ignored at delivery time today, but a future v2-shape extension could auto-opt-in existing webhooks. Integrations pinning to v1 should explicitly send `new_version: 0` at create.
- **`order.deleted` re-enablement** — confirm whether the platform plans to re-enable `order.deleted` (currently commented out) or remove it from the documented catalogue entirely. (verify)
- **`please unsubscribe me` 200-OK behaviour** — per [[webhook]] Open Questions, the trigger may fire only on 4xx / 5xx responses; verify whether a 200 OK with the literal phrase in the body also triggers auto-delete. (verify)
