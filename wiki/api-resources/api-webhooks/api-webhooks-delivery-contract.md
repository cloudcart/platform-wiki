---
type: api-resource
resource_path: /api/v2/webhooks
http_methods: [GET, POST, PATCH, DELETE]
related_entity: webhook
related_features: [settings-hooks, settings-admin-notifications]
aliases: ["Webhook delivery contract", "Webhook retry schedule", "Webhook auto-disable", "Webhook auto-delete", "please unsubscribe me", "X-CloudCart-ApiKey header", "Webhook usage counter", "Webhook delivery attempts"]
tags: [api, json-api-v2, infra, webhooks, delivery, retries]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---

> Part of [[api-webhooks]]. See the hub for the other aspects (CRUD surface, event catalog, examples).

# Webhooks API — delivery contract (JSON-API v2)

## Purpose

What happens **after** a webhook is saved and a matching event fires: the auto-injected auth header, the retry schedule, the codes that auto-disable a subscription, the receiver-controlled auto-delete, the usage counter, alert surfacing, the request shape, order-event queueing, and activity-log gating. Read this aspect to answer *"why did my webhook stop firing?"*, *"how many times does CloudCart retry?"*, *"how do I make CloudCart unsubscribe me?"* Creating / editing the subscription is [[api-webhooks-crud]]; the accepted events are [[api-webhooks-event-catalog]].

## Endpoint

The delivery contract is not a separate endpoint — it is the runtime behaviour attached to every webhook row created via `/api/v2/webhooks` (see [[api-webhooks-crud]]). The only API levers over it are the `active` and `url` attributes; after an auto-disable, the integrator must manually PATCH `active = 1` after fixing the receiver.

## Attributes

Two attributes drive delivery behaviour at runtime:

| Attribute | Effect on delivery |
|---|---|
| `active` | When `0`, deliveries are skipped. The platform auto-flips this to `0` on permanent-failure codes (see below). Re-enable via PATCH `active = 1`. |
| `new_version` | Selects the v2 vs legacy payload shape for `order.created` / `order.updated`; ignored at delivery time for non-order events today. See [[api-webhooks-crud]]. |

## Relationships

The webhook's linked [[api-key|API Key]] is what supplies the `X-CloudCart-ApiKey` delivery header. The relationship is implicit (not a JSON-API relationship) — see [[api-webhooks-crud]].

## Filtering & sorting

Not applicable to the runtime delivery path. To find currently-disabled subscriptions for diagnostics, `filter[active]=0` on the collection endpoint — see [[api-webhooks-crud]].

## Side effects

Once a webhook is saved, the **runtime delivery contract** kicks in on every matching event fire (full reference also in [[settings-hooks]] business rules and the [[webhook]] entity):

- **Authentication header (auto-injected)** — every delivery sends `X-CloudCart-ApiKey: <api-key value>` derived from the linked API key. Receivers should validate this header.
- **Delivery attempt sequence** — up to **6 attempts** over **20 minutes** (1 initial + 5 retries at +120s, +180s, +240s, +300s, +360s — formula `(retries + 1) × 60` seconds, verified 2026-06-11 against the platform code). Each attempt has a 5-second HTTP timeout (connect + total + read). **After the 6th failed transient attempt the webhook is auto-disabled** (`active` flipped 1 → 0) and the merchant receives an email via the mandatory `alert_notification` channel.
- **Auto-disable on permanent failures** — HTTP **400, 401, 403, 404, 405, 406, 410, 411** OR a "Could not resolve host" DNS error flips the webhook's `active` to `0` on the FIRST failure (no retries) and raises an admin alert. The integrator must manually PATCH `active = 1` after fixing the receiver.
- **Auto-delete on substring match** — if a delivery throws an exception whose message contains the literal text `please unsubscribe me` ANYWHERE — substring match, not exact — the webhook row is **deleted entirely** (not just deactivated). Receiver-controlled graceful opt-out. **Only fires on error responses** (4xx / 5xx / connection errors) because the substring check sits inside the catch block of the platform code — a 200 OK with the phrase in body does NOT trigger auto-delete.
- **"Last used count" increments on EVERY attempt** — the usage counter is incremented on BOTH success and failure paths. So a failing webhook shows an inflated counter. Treat it as a **delivery attempt count**, NOT a successful-delivery count.
- **Alert dashboard surfacing** — every auto-disable and final give-up raises an admin alert visible on [[settings-admin-notifications]]. Re-activating a webhook clears the suppression flag.
- **Outgoing request shape** — `POST <url>` with `Content-Type: application/json`, body is a JSON array with one element (the entity serialised through the public API model, or the v2-shape for order events with `new_version=1`). Null fields are stripped.
- **Queueing logic for order events** — when multiple webhooks subscribe to the same order event, deliveries are dispatched through the `order-events8` queue with a 60-second delay. Single-webhook subscribers deliver directly (in-process).
- **Activity log gated** — every delivery attempt IS recorded internally, BUT the per-store activity log is gated by an internal allowlist defaulting to a single CloudCart test site. Production merchants have NO self-service way to read the activity log from the admin UI; integrators must log on their own receiver side to debug. See [[settings-hooks-activity-log]].

## Equivalent UI

- [[settings-hooks]] — the admin-panel surface documents the same retry / auto-disable / auto-delete pipeline.
- [[settings-admin-notifications]] — where auto-disable and final-give-up alerts surface.

## Related

- [[api-webhooks]] — hub.
- [[webhook]] — entity reference with per-failure-mode behaviour.
- [[settings-hooks]] — admin-panel surface; documents the queue / retry pipeline.
- [[settings-hooks-delivery]] — delivery mechanics on the admin side.
- [[settings-hooks-retry]] — retry schedule detail.
- [[settings-hooks-auto-disable]] — auto-disable codes detail.
- [[settings-hooks-activity-log]] — the gated activity log.
- [[settings-admin-notifications]] — failure alerts.
- [[api-key]] — supplies the auto-injected `X-CloudCart-ApiKey` header.
- [[notification-delivery]] — the platform's notification spine.

## Open questions

- **`please unsubscribe me` 200-OK behaviour** — per [[webhook]] Open Questions, the trigger may fire only on 4xx / 5xx responses; verify whether a 200 OK with the literal phrase in the body also triggers auto-delete. (verify)
- **`new_version` future scope** — for non-order events `new_version` is ignored at delivery time today; if CloudCart extends the v2 shape to other event types, existing webhooks would auto-opt-in. (verify)
