---
type: concept
aliases: ["Admin alerts", "The bell icon", "Alerts feed", "Admin-panel notifications", "MakeAlert surface"]
tags: [notifications, alerts, admin-panel, concepts]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[notification-delivery]]. See the hub for the other aspects (event spine, retry semantics, transactional email inventory, customer suppression).

# Notification delivery — admin alerts (the bell icon)

## Definition

The platform-wide **admin-alert surface** is the Alerts feed reached via the **bell icon** at the top right of the admin panel. It is the merchant-facing side of notification delivery: where the platform tells the merchant — inside the admin panel, not in a customer's inbox — that something needs attention (a webhook auto-disabled, an export finished, an app was installed). Each alert carries a title, body, link, severity, and an optional grouping key so identical alerts don't pile up into a wall of duplicates.

Admin alerts are the only one of the four channels whose audience is the **merchant** rather than the **customer**. They use the same fan-out infrastructure (an event fires, a subscriber writes the alert) but the alert write is **synchronous** — there is no queue and no retry; it either writes or it doesn't.

## Scope

What this covers:

- The Alerts feed (bell icon) and what each alert record carries.
- The typical sources that raise an alert.
- The relationship between in-panel alerts and the optional email-to-merchant escalation.

What it does NOT cover:

- The event → subscriber → job mechanism that raises alerts — see [[notification-delivery-event-spine]].
- Webhook retry / auto-disable that *produces* the webhook alerts — see [[notification-delivery-retry]].
- The admin-notification recipient / preference screen — see [[settings-admin-notifications]].

## Contrasts

- **Admin-panel alerts vs. customer-facing notifications**: alerts are read by the merchant inside the admin panel; customer-facing notifications (order-confirmation emails, etc.) go to the customer's inbox or phone. Same delivery infrastructure, different audience.
- **In-panel bell vs. email-to-merchant**: the bell always shows the alert in-panel; whether an alert ALSO sends an email to the merchant depends on the admin's notification preferences on [[settings-admin-notifications]].
- **Synchronous alert write vs. queued channel work**: unlike webhooks, emails, and analytics jobs, the alert is written synchronously with no retry — it is a direct write to the Alerts feed.

## Where it applies

- [[settings-admin-notifications]] — which alerts also trigger an email-to-merchant, and the recipient addresses.
- [[settings-hooks]] — webhook auto-disable surfaces here AND on the bell.
- [[analytics-pipeline]] — async export-complete raises an alert with the download URL.
- [[settings-general]] — the store email used as the default recipient for escalated alerts.

## Typical alert sources

- **Webhook auto-disable** — a `Settings → Webhooks` row was deactivated because the receiver returned a permanent failure code (e.g. 404) or DNS failed. Surfaces here AND on [[settings-hooks]]. The mechanics of *why* it auto-disabled live on [[notification-delivery-retry]].
- **Webhook final give-up** — all retries exhausted on a delivery.
- **Export complete** — an async report export finished; the alert carries the download URL (the platform deliberately uses an admin alert here instead of an email).
- **App install / uninstall** — an app was added to or removed from the store.
- **Plan / subscription warnings** — billing or plan-limit notices.

## In-panel alert vs. email escalation

Every alert appears at the bell icon. Whether an alert ALSO escalates to an **email to the merchant** is controlled per alert type by the admin's notification preferences on [[settings-admin-notifications]] — for example, low-stock and out-of-stock notices can be set to email the store address on top of appearing in-panel. The recipient defaults to the store email from [[settings-general]] unless overridden.

The `alert_notification` mail label is one of three labels that bypass the per-mail Active toggle, but it is still gated by the global `customer_email_notifications` master switch — see [[notification-delivery-email-inventory]] for the gating rules. In practice this means a merchant cannot accidentally turn off critical alert emails by toggling an individual template, but a global notifications kill at the platform level would still suppress them.

## No "mute the bell" switch

There is no merchant-facing control to silence the bell or pause all admin alerts. Individual webhooks can be toggled inactive on [[settings-hooks]], and individual alert-email escalations can be turned off on [[settings-admin-notifications]], but the in-panel alert feed itself has no mute. See [[notification-delivery-suppression]] for the full picture of what can and cannot be suppressed across all four channels.

## Related

- [[notification-delivery]] — hub.
- [[settings-admin-notifications]] — admin-alert recipients + which alerts escalate to email.
- [[settings-hooks]] — webhook auto-disable surfaces here.
- [[settings-general]] — default recipient (store email).
- [[notification-delivery-retry]] — the webhook give-up / auto-disable that produces webhook alerts.
- [[notification-delivery-email-inventory]] — `alert_notification` label gating.

## Open Questions

None.
