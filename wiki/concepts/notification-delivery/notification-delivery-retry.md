---
type: concept
aliases: ["Notification retry semantics", "Per-channel retry", "Webhook retry timeline", "Email retry policy", "Analytics auto-resume"]
tags: [notifications, webhooks, email, queues, retry, concepts]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[notification-delivery]]. See the hub for the other aspects (event spine, admin alerts, transactional email inventory, customer suppression).

# Notification delivery — retry semantics

## Definition

Each of the four outbound channels has its own **retry profile**. The retry strategy is **deliberately different per channel**: webhook deliveries retry aggressively with back-off because external receivers may be transiently down; analytics aggregations have no merchant-visible retry because they auto-resume on the next hourly tick; transactional email follows the mail driver's own policy. A merchant who expects "if it failed, it'll just keep trying forever" is wrong for some channels and right for others — the distinction matters when diagnosing "the customer never got the email" vs "the webhook stopped firing".

## Scope

What this covers:

- The per-channel retry table (first attempt, retries, give-up time, failure surface).
- The webhook retry timeline in detail (6 attempts over 20 minutes).
- The analytics hourly auto-resume model.
- The transactional-email reap-and-retry behaviour.

What it does NOT cover:

- Which event triggers which job — see [[notification-delivery-event-spine]].
- The admin-alert surface that webhook give-up writes to — see [[notification-delivery-admin-alerts]].
- The full webhook configuration screen — see [[settings-hooks]].

## Contrasts

- **Aggressive retry (webhook) vs no merchant-visible retry (analytics)**: a failed webhook retries 5 times then gives up — auto-disabling the webhook and emailing the merchant; a failed hourly aggregation simply re-runs on the next tick with no alert, because it checkpoints and catches up automatically.
- **Job-level retry (email) vs provider-level retry (email delivery)**: the queue reaps stalled mail jobs on a timer, but actual delivery failures from the email provider are handled by the provider's own retry layer, not by re-queueing.
- **Auto-disable (webhook) vs silent retry (everything else)**: only the webhook channel can permanently disable itself on certain HTTP failure codes; no other channel removes itself from service.

## Where it applies

- [[settings-hooks]] — webhook screen showing active / auto-disabled state.
- [[notification-delivery-admin-alerts]] — where webhook give-up and auto-disable surface to the merchant.
- [[settings-queue-view]] — where stalled / retrying jobs are visible.
- [[analytics-pipeline]] — the auto-resuming hourly aggregation.

## Retry profiles across channels

| Channel | First attempt | Retries | Total time to give-up | Failure surface |
|---------|---------------|---------|----------------------|-----------------|
| **Webhook (Settings → Webhooks)** | Immediate (or +60s if multi-webhook on `order.*`) | 5 retries at +120s, +180s, +240s, +300s, +360s | 20 minutes | Admin alert + **email** on final auto-disable (active flag flips 1→0); also auto-disables on permanent failure codes (400/401/403/404/405/406/410/411 + DNS) |
| **Per-order analytics job** | Immediate (with 5s or 60s delay per event type) | Standard queue retry; releases & retries on transient failures | Per the queue's policy for that task | None to merchant; logged internally |
| **Hourly aggregation job** | At HH:01 UTC of next hour | Re-runs at every hour tick; checkpoints, so a single failed run resumes cleanly | Indefinite (auto-resumes) | None to merchant |
| **Transactional email** | Queued on the mail queue | Job-level retry — the platform's delivery queues reap stalled email tasks roughly every 10 minutes and re-run them. Transient delivery failures from the email provider (Elastic Email) are handled by the provider's own retry layer. | Per the email provider's policy | Usually silent; logged in the platform's mail queue and Elastic Email's send log |
| **Admin alert** | Synchronous write to the Alerts feed | N/A | N/A | Visible at the bell icon |

## Webhook delivery — 6 attempts over 20 minutes (verified 2026-06-11)

The full retry timeline lives on [[settings-hooks-retry]]. Key points:

- 1 initial attempt + 5 retries = 6 attempts total.
- Spacing: +120s, +180s, +240s, +300s, +360s — total **20 minutes** (1200 s) from first failure to give-up. Delay formula `(retries + 1) × 60` seconds (`retries` starts at 1).
- 5-second HTTP timeout per attempt.
- Permanent failures (400/401/403/404/405/406/410/411 + DNS unresolvable) skip retries and auto-disable the webhook on the **first** failure.
- **After the 6th failed transient attempt the webhook is auto-disabled too** (`active` flag flipped 1 → 0) and the merchant gets an email via the `alert_notification` channel — verified `HooksSendRaw.php` line 64.
- The literal string `please unsubscribe me` inside an exception message auto-deletes the webhook — **but only in error responses (4xx / 5xx / connection errors)**; a 200 OK with the phrase in body does NOT trigger it (verified `HookEventPost.php:242`, inside catch block).
- `X-CloudCart-ApiKey` header is auto-injected from the linked API key — see [[settings-api-keys]].

When a webhook permanently fails or finally gives up after all retries, the merchant finds out via the admin-alert bell — see [[notification-delivery-admin-alerts]].

## Analytics aggregation — hourly auto-resume (verified)

The aggregation job re-schedules itself at HH:01 UTC of the next hour. Each fan-out aggregation job (visitors, devices, traffic-source, products, etc.) records its own progress marker, so a missed hour catches up automatically — no merchant action needed, and no alert is raised. This is why there is no "analytics retry" surface for the merchant: the system is self-healing on the next tick. See [[analytics-pipeline]] for the aggregation chain.

## Why the differences matter to the merchant

- A **webhook** that stops firing has likely auto-disabled itself after permanent failures — check the bell and [[settings-hooks]], re-activate, and fix the receiver.
- An **email** that "didn't arrive" is rarely a retry problem — it is usually a suppression flag (see [[notification-delivery-suppression]]), a disabled template, or a provider-side spam / bounce. The queue retry only covers stalled *jobs*, not bounced *messages*.
- **Analytics** lag after an incident is expected to self-correct within the next hour; no merchant action is needed.

## Related

- [[notification-delivery]] — hub.
- [[settings-hooks]] — full webhook retry timeline + auto-disable.
- [[settings-api-keys]] — webhook authentication credential injected per attempt.
- [[analytics-pipeline]] — the auto-resuming hourly aggregation.
- [[settings-queue-view]] — where retrying / stalled jobs surface.
- [[background-queue-inventory]] — the delivery queues and their reap timers.

## Open Questions

None.
