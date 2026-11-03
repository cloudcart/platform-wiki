---
type: entity
aliases: ["Webhook failure handling", "Webhook auto-disable", "Webhook auto-delete", "please unsubscribe me", "Webhook permanent failure", "Retryable webhook failures", "Авто-изключване на уебхук", "Грешки при уебхук"]
tags: [settings, developer, webhooks, integrations, errors, entity]
created: 2026-06-10
updated: 2026-06-11
source_count: 5
---

# Webhook — Failure handling

> Part of [[webhook]]. See the hub for the other aspects (events, configuration, delivery, logging).

## Identity

**Failure handling** is how the platform reacts when a [[webhook|Webhook]] delivery does not succeed. CloudCart classifies every failed response into one of three outcomes — **retry** (transient), **auto-disable** (the receiver knows it can't handle the request), or **auto-delete** (the receiver explicitly asks to be removed). This is the platform policing receiver uptime so the merchant doesn't have to — but it also means the merchant DOES have to fix a broken receiver and manually re-enable before deliveries resume. The retry timing itself (**20-minute window, 6 attempts** — verified 2026-06-11) lives in [[webhook-entity-delivery]] and [[settings-hooks-retry]]; this page covers which responses fall into which bucket.

## Aliases

- **Webhook failure handling** — the umbrella term.
- **Webhook auto-disable** / **Webhook auto-delete** — the two terminal failure outcomes.
- **`please unsubscribe me`** — the literal phrase that triggers auto-delete.
- **Авто-изключване на уебхук** / **Грешки при уебхук** — Bulgarian equivalents.

## Key Attributes

**Auto-disable rules (immediate — skip retries).** The Webhook is flipped to inactive on the FIRST attempt that returns:

- **HTTP status codes** indicating the receiver knows it can't handle the request: **400, 401, 403, 404, 405, 406, 410, 411**.
- **DNS error "Could not resolve host"** — the destination domain doesn't exist or DNS is broken.

After auto-disable, an alert appears in the admin notification panel ([[admin-notification]] / [[settings-admin-notifications]]) describing the disable reason and the affected URL. Alerts are grouped per-Webhook so a single broken receiver doesn't spam infinite alerts.

**Retryable failures (everything not in the auto-disable / auto-delete lists).** These trigger the six-attempt retry sequence:

- HTTP 5xx (server errors at the receiver).
- HTTP 408 (Request Timeout).
- HTTP 429 (rate limit).
- Connection refused (no service listening).
- Connection / read timeout (no response within 5 seconds).
- TLS / SSL handshake failures.
- Other HTTP error codes not in the permanent list.

So a receiver returning HTTP 503 because it is overwhelmed → CloudCart retries up to 5 more times over 20 minutes (delays 120 s, 180 s, 240 s, 300 s, 360 s = 1200 s total). A receiver returning HTTP 404 → CloudCart disables on the first failure.

**Final-attempt give-up auto-disables the webhook too.** If a transient failure persists across all 6 attempts, after the 6th failure the dispatcher calls `sendAlert($message, disableHook=true)` directly — the webhook is **auto-disabled** even though the failure was never "permanent". An email is sent to the merchant on that 1 → 0 transition of the `active` flag (via the always-on `alert_notification` channel — see [[admin-notifications-mandatory-three]]). See [[settings-hooks-retry]] "Final give-up" for the full mechanism.

**Auto-delete rule (`please unsubscribe me`).** If a delivery throws an exception whose `getMessage` contains the literal substring **`please unsubscribe me`**, the entire Webhook row is deleted (not just deactivated) — a graceful opt-out, no alert, no manual cleanup. Critical nuance: the trigger is checked **inside the catch block** of the delivery — so it fires only when the delivery throws (4xx / 5xx response, connection error, TLS error). **A 200 OK with `please unsubscribe me` in the body does NOT trigger auto-delete** — successful responses never enter the catch block. Receivers wanting a graceful opt-out must return a non-success status with the phrase in the body.

**Re-enable behaviour:**

- **Auto-disable persists until manual re-enable.** Once auto-disabled, the Webhook stays inactive even if the receiver comes back online — the platform does NOT auto-re-enable. The merchant must manually toggle Active ON from [[settings-hooks]] after confirming the receiver is fixed (see [[webhook-entity-configuration]]).
- **The first event after re-enable starts a fresh retry counter** — there is no "remember last failure" state.
- **No re-enable event fires.** There is no `webhook.re_enabled` event; re-enabling is a silent DB flip. The next matching event simply restarts the delivery pipeline.

## Where it appears

- [[settings-hooks]] — the auto-flipped Active toggle; manual re-enable after fixing the receiver.
- [[settings-admin-notifications]] — webhook failure alerts (auto-disable, final give-up) surface here.
- [[admin-notification]] — the per-Webhook grouped alert entity.

## Related

- [[webhook]] — hub.
- [[webhook-entity-delivery]] — the retry timing the failure rules feed into.
- [[admin-notification]] — auto-disable + final give-up raise a grouped admin alert.
- [[settings-admin-notifications]] — where failure alerts appear.
- [[settings-hooks]] — manual re-enable lives here.

## Open Questions

None.
