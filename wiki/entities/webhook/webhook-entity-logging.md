---
type: entity
aliases: ["Webhook logging", "Webhook activity log", "Webhook delivery log", "Webhook troubleshooting", "Webhook diagnostics", "Лог на уебхук", "Диагностика на уебхук"]
tags: [settings, developer, webhooks, integrations, logging, troubleshooting, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

# Webhook — Logging and troubleshooting

> Part of [[webhook]]. See the hub for the other aspects (events, configuration, delivery, failure handling).

## Identity

**Logging** covers what the platform records about each [[webhook|Webhook]] delivery and — importantly — what the merchant can and cannot see of it. Every delivery attempt is recorded internally (timestamp, request payload, response code, error message), but that log is **NOT exposed in the admin panel for production stores**. This is the single biggest UX gap in webhook troubleshooting today: when a Webhook isn't behaving, the merchant has very limited self-serve visibility and must lean on the table's last-used count, their own receiver-side logs, or CloudCart support.

## Aliases

- **Webhook logging** / **Webhook activity log** / **Webhook delivery log** — the internal record of attempts.
- **Webhook troubleshooting** / **Webhook diagnostics** — the merchant-facing task this page supports.
- **Лог на уебхук** / **Диагностика на уебхук** — Bulgarian equivalents.

## Key Attributes

**The delivery log is internal and gated.** Every attempt is recorded internally with timestamp, request payload, response code, and error message. The log is gated by an internal `allowed_logging` allowlist that defaults to a single CloudCart test site. Production merchants **cannot self-serve the log from the admin UI** — they must contact CloudCart support to enable per-store logging, or log on their own receiver side.

**What the merchant CAN see without support:**

- **Last-used count** on [[settings-hooks]] — increments only on successful delivery (see [[webhook-entity-delivery]]). The fastest answer to *"is this Webhook firing at all?"*. A stuck-at-zero or stale count means deliveries aren't succeeding.
- **Active toggle state** — if the platform auto-disabled the Webhook (toggle flipped OFF), that is itself a signal the receiver returned a permanent-failure response. See [[webhook-entity-failure-handling]].
- **Admin-panel alerts** — auto-disable and final give-up raise a grouped alert on the bell icon ([[admin-notification]] / [[settings-admin-notifications]]) naming the reason and the affected URL.

**Troubleshooting workflow merchants can run themselves:**

1. **Check the last-used count** — if it's incrementing, deliveries succeed and the problem is on the receiver's processing side.
2. **Check the Active toggle** — if auto-disabled, the receiver returned a permanent-failure status; fix it and re-enable (see [[webhook-entity-failure-handling]]).
3. **Check the admin notification panel** for the disable reason and URL.
4. **Inspect the receiver's own logs** — the most reliable source of the actual payload and response, since the CloudCart-side log isn't self-serve.
5. **Verify the `X-CloudCart-ApiKey` header** matches the linked [[api-key|API Key]] (see [[webhook-entity-delivery]]).
6. **Contact CloudCart support** to enable per-store delivery logging if the above is inconclusive.

## Where it appears

- [[settings-hooks]] — last-used count + Active toggle; the only self-serve diagnostic surface.
- [[settings-admin-notifications]] — failure alerts.
- [[settings-queue-view]] — in-flight delivery jobs on the `order-events8` queue, visible during retries.

## Related

- [[webhook]] — hub.
- [[webhook-entity-delivery]] — the last-used count and request shape used for diagnosis.
- [[webhook-entity-failure-handling]] — the auto-disable signal a merchant reads from the toggle.
- [[settings-hooks]] — the management screen.
- [[settings-admin-notifications]] — failure alerts.
- [[settings-queue-view]] — the delivery queue.
- [[api-key]] — the authentication header to verify.

## Open Questions

- Whether CloudCart plans to surface the delivery log in the admin UI for production stores (currently the biggest webhook UX gap). `(verify)`
