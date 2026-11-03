---
type: feature
nav_path: "Settings → Webhooks → Delivery flow"
route_name: hooks.settings
route_path: /admin/settings/hooks
aliases: ["Webhook delivery", "Webhook timeout", "Sync vs async webhook", "Webhook first attempt", "5-second timeout", "Webhook queue"]
tags: [settings, webhooks, delivery, queue, integrations]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-hooks]]. See the hub for the other aspects (events, retry, auto-disable, modal, activity log, auth & headers).

# Webhooks — delivery flow & timing

## Purpose

Once an event fires, the platform classifies the subscription set, then **sends the first delivery attempt** to each subscriber. This page covers what happens between "the merchant clicks Save" and "the receiver gets the POST" — specifically the **5-second timeout**, the **sync-vs-deferred first-attempt decision**, and which deliveries are visible on [[settings-queue-view]].

## Where to find it

The delivery pipeline runs invisibly behind every save action. There is no merchant-visible "deliver now" control. The closest surfaces are:

- [[settings-queue-view]] — shows queued webhook jobs (only the deferred / retry attempts are visible there).
- [[settings-admin-notifications]] — surfaces auto-disable and final give-up alerts (see [[settings-hooks-auto-disable]]).

## What the merchant can do here

Nothing directly — delivery timing is fully automatic. The merchant influences it only by:

- Toggling a webhook's **Active** flag (inactive webhooks are skipped entirely — see [[settings-hooks-modal]]).
- Configuring more than one webhook on the same order event (this flips the first attempt from sync to a 60-second deferred queue job — see Sync vs deferred first attempt).
- Fixing a slow receiver (a receiver that takes > 5 seconds to respond fails every attempt — see Timeout below).

## Settings & fields

### Delivery lifecycle — first attempt

1. **Event fires** (e.g. an order is created). The platform finds all **active** webhooks subscribed to that event. If none → silent no-op.
2. **First attempt** runs (sync or deferred — see below).
3. **HTTP POST** with a default **5-second timeout** (connect + total + read — three Guzzle options, all 5 s).
4. **On success** — the webhook's `last_used_at` counter increments (see [[settings-hooks-activity-log]]).
5. **On failure** — the platform classifies the failure and either retries ([[settings-hooks-retry]]), auto-disables, or auto-deletes ([[settings-hooks-auto-disable]]).

### The 5-second timeout (enforced THREE times)

The outgoing HTTP request uses these Guzzle options (all set to **5 seconds**):

- `TIMEOUT: 5` — overall request timeout (connect + transfer).
- `CONNECT_TIMEOUT: 5` — TCP handshake timeout.
- `READ_TIMEOUT: 5` — between-bytes timeout while reading the response body.

A slow receiver that opens the connection quickly but takes > 5 s to start sending the response body **STILL fails**. Receivers should ACK fast with `200 OK` and process asynchronously — NOT do heavy work synchronously inside the webhook handler.

### Sync vs deferred first attempt

The first delivery attempt **typically runs synchronously inside the merchant's triggering action**. When the merchant clicks Save Product, the webhook fires inside that save request — and the 5-second timeout caps the worst-case wait the merchant experiences while the save spinner is shown.

**Exception**: for `order.created` and `order.updated` events when the store has **MORE THAN ONE active webhook subscribed**, the first attempt is **deferred by 60 seconds** so the customer's checkout completes fast (without waiting on multiple receiver round-trips).

| Scenario | First attempt runs |
|---|---|
| 1 active webhook on any event | **Synchronously** inside the triggering action (5 s max merchant wait). |
| 2+ active webhooks on `order.created` / `order.updated` | **Deferred 60 s** on the `order-events8` queue (visible in [[settings-queue-view]]). |
| 2+ active webhooks on non-order events | Synchronously (the 60 s defer rule is order-only). (verify) |

### Queue visibility

Every retry (attempts 2–7 — see [[settings-hooks-retry]]) is dispatched on the **`order-events8`** queue regardless of event type. The initial inline dispatch from the event handler is NOT queued for the single-webhook case — only the retries are.

On [[settings-queue-view]]:
- **Initial attempts on single-webhook events:** NOT visible (executed inline with the merchant action).
- **Initial attempts on multi-webhook order events:** visible (the 60-second-delayed event-fanout job followed by the per-webhook send job).
- **Retries (attempts 2–7):** always visible — send-job rows with delays of 60, 120, 180, 240, 300, 360 seconds.

## Business rules

- **Save-action latency.** Because the first attempt is sync for single-webhook setups, a slow receiver makes the merchant's save spinner hang up to 5 s. Merchants who add a webhook to a slow receiver should know this — there's no async opt-out for single-webhook events.
- **Order-event throughput.** The 60-second defer for multi-webhook order events exists specifically to keep checkout latency low. Adding a second active webhook to `order.created` automatically flips the dispatch model — the merchant doesn't configure this.
- **Inactive webhooks are skipped entirely.** No row in the queue, no attempt, no log line. See [[settings-hooks-modal]] for the toggle.

## Related

- [[settings-hooks]] — hub.
- [[settings-hooks-retry]] — the 7-attempt retry timeline + retryable failure classification.
- [[settings-hooks-auto-disable]] — the permanent-failure shortcut around the retry pipeline.
- [[settings-hooks-activity-log]] — the `last_used_at` counter + backend log gating.
- [[settings-queue-view]] — visibility surface for queued + retried delivery jobs (`order-events8`).
- [[settings-admin-notifications]] — auto-disable and final give-up alert surface.
- [[background-queue-inventory]] — catalogue of all background processes; covers webhook-delivery cadence and visibility on Queue View when a webhook is stuck.

## Open questions

- Confirm: do multi-webhook fanouts on non-order events also defer 60 s, or is the defer strictly `order.created` / `order.updated`? (verify)
