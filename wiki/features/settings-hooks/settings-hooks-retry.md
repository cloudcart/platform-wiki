---
type: feature
nav_path: "Settings → Webhooks → Retry timeline"
route_name: hooks.settings
route_path: /admin/settings/hooks
aliases: ["Webhook retry", "Webhook retries", "6 attempts", "20 minutes", "Retry timeline", "Retryable failures"]
tags: [settings, webhooks, retry, queue, integrations]
plan_gates: []
created: 2026-06-10
updated: 2026-06-11
source_count: 3
---

> Part of [[settings-hooks]]. See the hub for the other aspects (events, delivery, auto-disable, modal, activity log, auth & headers).

# Webhooks — retry timeline & retryable failures

## Purpose

When the first delivery attempt fails AND the failure is **not classified as permanent** (see [[settings-hooks-auto-disable]] for the permanent list), the platform retries up to **5 more times** with a growing backoff. **Total 6 attempts**, total elapsed time from first failure to final give-up is **20 minutes**. After the 6th failed attempt, the webhook is **auto-disabled** and an email is sent to the merchant — see the give-up section below.

## Where to find it

The retry pipeline is automatic; there is no merchant-facing "retry now" control. Retries are visible on [[settings-queue-view]] as queued send-jobs on the `order-events8` queue.

## What the merchant can do here

- Watch retries flow through [[settings-queue-view]] — each row shows the scheduled run time.
- Fix the receiver mid-retry. Each retry re-evaluates the auto-disable rules — if a transient failure becomes one of the permanent codes (see [[settings-hooks-auto-disable]]) mid-retry, retries stop and the webhook is disabled.
- Wait. If the receiver recovers within 20 minutes, a later retry can still succeed.

## Settings & fields

### Retry timeline — 6 attempts over 20 minutes

| Attempt | When (delay from the previous failure) |
|---------|------|
| 1 (initial) | Immediately on event fire (or ~60 s later for multi-webhook order events — see [[settings-hooks-delivery]]) |
| 2 | +120 seconds after attempt 1 failure |
| 3 | +180 seconds after attempt 2 failure |
| 4 | +240 seconds after attempt 3 failure |
| 5 | +300 seconds after attempt 4 failure |
| 6 | +360 seconds after attempt 5 failure |
| Give up | After attempt 6 fails — the webhook is **auto-disabled** (`active = 0`); a panel alert + email go out — see "Final give-up" below |

**Total elapsed time from first failure to give-up: 20 minutes** (120 + 180 + 240 + 300 + 360 seconds = 1200 s = 20 min). The delay formula is `(retries + 1) × 60 seconds`, where `retries` is the attempt counter (starts at 1).

**Important: retries 2–6 are scheduled jobs on the queue** — the delay is the job's `->delay(...)` value. Actual wall-clock time depends on queue worker load; under normal conditions the delays above are precise within a few seconds.

### Final give-up — what happens after attempt 6 fails

When the 6th attempt fails on a transient error (HTTP 5xx, 408, 429, connection refused, read timeout, TLS error, etc.), the webhook is **auto-disabled**. Three things happen:

1. **The webhook flips to `active = 0`** in the DB — the row's `active` column transitions from 1 → 0. The merchant sees the **Active** toggle on [[settings-hooks]] flipped OFF.
2. **A panel alert is raised on [[settings-admin-notifications]]** — grouped per-webhook so the same broken receiver doesn't spam.
3. **An email is sent to the merchant** — but only when the webhook's status actually changes to disabled. So:
   - **Transient failures, attempts 1–5:** a panel alert is recorded on each failed attempt, but **no email per retry** (the webhook is still active).
   - **The 6th and final failure:** the webhook flips to disabled, so **one email** goes out at the end of the retry cycle.
   - **Permanent-code failures (404, 405, etc.):** the webhook is disabled on the **first** attempt (no retries) — single email then.

The email is delivered via the `alert_notification` channel — one of the 3 **mandatory** admin-notification types that cannot be disabled by the merchant (see [[admin-notifications-mandatory-three]]). Recipient = `site_email` from [[settings-general]]. Email body uses the same `hooks.error.disable` template documented on [[notifications]].

**The same alert is visible in three places concurrently** — the email to the merchant's inbox, the [[notifications]] inbox at `/admin/notifications` (filterable by the **Alerts** tab), and the bell-icon dropdown at the top of every admin page. All three render the SAME text, which **includes the receiver's verbatim error response body** so the merchant can fix the integration without digging into a separate log surface. See [[notifications]] for the rendered message format and [[settings-hooks-auto-disable]] "Where the merchant reads the error message" for the closed loop.

**After give-up the platform never retries on its own.** The webhook stays disabled until the merchant manually flips the Active switch back ON — see [[settings-hooks-auto-disable]] for the re-enable flow.

### Retryable failures

Every failure NOT in the permanent-failure list (see [[settings-hooks-auto-disable]]) is retryable. The canonical retryable cases:

- **HTTP 5xx** — server errors at the receiver (the receiver is overwhelmed / crashing).
- **HTTP 408** — Request Timeout.
- **HTTP 429** — rate limit (the receiver wants to be slowed down).
- **Connection refused** — no service listening on the port.
- **Connection / read timeout** — no response or incomplete response within 5 seconds (see the 5-s timeout details in [[settings-hooks-delivery]]).
- **TLS/SSL handshake failures** — usually transient cert / negotiation glitches.
- **Most "other" HTTP error codes** not in the permanent list.

So a receiver returning **HTTP 503** because it's overwhelmed → CloudCart retries up to 5 more times over 20 minutes (then auto-disables on the 6th failed attempt). A receiver returning **HTTP 404** → CloudCart disables the webhook on the **first** failure (see [[settings-hooks-auto-disable]]).

### Dispatch queue

Every retry (attempts 2–7) is dispatched on the **`order-events8`** queue. Retry rows are visible on [[settings-queue-view]] with their scheduled run time. The job name and the per-row payload are platform internals — merchants identify the right rows by destination URL + event.

## Business rules

- **Each retry re-evaluates the auto-disable rules.** If a transient 503 turns into a 404 mid-retry (receiver redeploys with the endpoint removed), retries stop immediately and the webhook is auto-disabled on the current attempt — NOT after the 6-attempt window expires. The pipeline does NOT keep retrying past a now-permanent failure.
- **Successful retry mid-cycle counts as success.** If attempt 4 succeeds after attempts 1–3 failed, no more attempts run and no email is sent (the `active` flag never changed). The `last_used_at` counter increments on every attempt — failures included — see [[settings-hooks-activity-log]].
- **Per-event retry cycles are independent.** Two distinct order updates each get their own 6-attempt budget (each event starts a fresh count). There is no shared budget across events.
- **No exponential backoff and no jitter.** The pattern is **linear arithmetic** — delay = `(retries + 1) × 60` seconds, growing by exactly 60 s per cycle. A receiver returning 429 will not get exponentially-backed-off requests — just minute-stepped retries until the cycle ends. Receivers that want aggressive throttling should respond with a permanent code (see [[settings-hooks-auto-disable]]) and re-subscribe later.

## Related

- [[settings-hooks]] — hub.
- [[settings-hooks-delivery]] — first-attempt timing (sync vs deferred) + the 5-second timeout.
- [[settings-hooks-auto-disable]] — failures that skip the retry pipeline entirely.
- [[settings-hooks-activity-log]] — backend log of every attempt + the `last_used_at` counter.
- [[settings-queue-view]] — where retries are visible.
- [[settings-admin-notifications]] — final give-up alert surface.
- [[background-queue-inventory]] — covers webhook-delivery cadence and retries.

## Open questions

None — retry count (6), formula `(retries + 1) × 60`, total elapsed (~20 min), final auto-disable + single-email behaviour verified against backend 2026-06-11. Queue-worker latency may add a few seconds per attempt under load.
