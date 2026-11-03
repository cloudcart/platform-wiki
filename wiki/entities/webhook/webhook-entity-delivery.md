---
type: entity
aliases: ["Webhook delivery", "Webhook payload", "Webhook request shape", "Webhook retries", "X-CloudCart-ApiKey", "Webhook retry sequence", "Доставка на уебхук", "Изпращане на уебхук"]
tags: [settings, developer, webhooks, integrations, delivery, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

# Webhook — Delivery

> Part of [[webhook]]. See the hub for the other aspects (events, configuration, failure handling, logging).

## Identity

**Delivery** is what happens when an event a [[webhook|Webhook]] subscribes to actually fires: CloudCart sends an HTTP POST carrying the affected entity to the Webhook's destination URL. Delivery is a **queued background job** on the `order-events8` queue — see [[settings-queue-view]] and [[notification-delivery]]. Each fire produces one initial attempt plus up to five retries on failure. This page covers the request shape, the authentication header, the success counter, and the retry timing. The classification of *which* failures retry vs auto-disable lives in [[webhook-entity-failure-handling]].

## Aliases

- **Webhook delivery** / **Webhook payload** — the outgoing POST and its body.
- **Webhook retries** / **Webhook retry sequence** — the repeated attempts on failure.
- **X-CloudCart-ApiKey** — the auto-injected authentication header.
- **Доставка на уебхук** / **Изпращане на уебхук** — Bulgarian equivalents.

## Key Attributes

**Outgoing request shape:**

```
POST <webhook.url>
Headers:
  X-CloudCart-ApiKey: <api-key value>
  <any merchant-configured custom headers>
  Content-Type: application/json
Body:
  [{ ...payload... }] ← array with one element (entity serialised as the public API model;
                          or v2 shape for order.* when the "new structure" toggle is on)
```

- **The payload is an array with a single element** — the affected entity serialised as the public REST API model, or the v2 shape for `order.*` when the "new structure" toggle is on (see [[webhook-entity-configuration]]).
- **Null fields are stripped** from the payload.
- **`X-CloudCart-ApiKey` is added automatically** — the value is the [[api-key|API Key]] the merchant linked. The receiver SHOULD validate this header before processing: it proves the request came from this specific CloudCart store, not from a forger spoofing the URL. The merchant does not add this header manually. For extra security (HMAC, Bearer tokens), the merchant adds those via the Custom headers field, sent alongside the auto-added key.

**Last-used count** — the table on [[settings-hooks]] shows a counter that increments by 1 **only on a successful delivery**. Failed attempts — even retried ones that eventually succeed — count only the final success, not each attempt. This is the merchant's at-a-glance answer to *"is this Webhook actually firing?"*.

**Delivery attempt sequence (verified 2026-06-11 against the platform code — delay formula is `(retries + 1) × 60` seconds, retries starts at 1):**

| Attempt | When |
|---------|------|
| 1 (initial) | Immediately on event fire — synchronously inside the triggering action for single-Webhook events; deferred by +60 seconds for `order.created` / `order.updated` when MORE THAN ONE active Webhook is subscribed (so checkout isn't slowed by multiple round-trips). |
| 2 | +120 seconds after attempt 1 failure |
| 3 | +180 seconds after attempt 2 failure |
| 4 | +240 seconds after attempt 3 failure |
| 5 | +300 seconds after attempt 4 failure |
| 6 | +360 seconds after attempt 5 failure |
| Give up | After attempt 6 fails — webhook **auto-disabled** (`active` flag flipped 1 → 0), admin alert raised, email goes out via the `alert_notification` channel (see [[admin-notification]] and [[settings-hooks-retry]] "Final give-up") |

**Total elapsed time from first failure to give-up: 20 minutes** (120 + 180 + 240 + 300 + 360 seconds = 1200 s). Each attempt has a **5-second HTTP timeout** (connect + total + read). Each retry re-evaluates the failure rules — if a transient failure turns into a permanent-failure status mid-retry, retries stop and the Webhook is auto-disabled (see [[webhook-entity-failure-handling]]).

## Where it appears

- [[settings-queue-view]] — webhook delivery jobs appear on the `order-events8` queue, visible during in-flight retries.
- [[settings-hooks]] — the last-used count column reflects successful deliveries.
- [[settings-admin-notifications]] — the final give-up raises an admin-panel alert.

## Related

- [[webhook]] — hub.
- [[webhook-entity-failure-handling]] — classification of which responses retry, auto-disable, or auto-delete.
- [[api-key]] — supplies the `X-CloudCart-ApiKey` value.
- [[settings-queue-view]] — the `order-events8` delivery queue.
- [[notification-delivery]] — the platform-wide event spine and retry semantics.
- [[admin-notification]] — the give-up alert.

## Open Questions

None.
