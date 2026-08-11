---
type: concept
aliases: ["Notification delivery", "Email/SMS/webhook delivery", "Event-driven notifications"]
tags: [notifications, events, webhooks, email, sms, concepts]
created: 2026-05-21
updated: 2026-06-10
source_count: 2
---
# Notification delivery (email, SMS, webhook, admin-panel alert)

## Definition

How CloudCart turns an in-store event (a new order, a product change, a customer registration, a webhook receiver going down, an analytics aggregation finishing) into one or more **outbound notifications** — emails to customers, transactional SMS, HTTP webhooks to third-party systems, and admin-panel alerts visible to the merchant. The pattern is consistent across the platform: an in-store event fires **once** on the main request thread, **subscribers** dispatch one or more queued jobs, and each job is responsible for one delivery channel (an email job, an SMS job, a webhook delivery job, an analytics job, an admin-alert write).

The unifying rule is **fire the event once, let independent subscribers fan out to queues**. This is why a merchant clicking "Save Order" doesn't wait for the email, the webhook, the analytics document, and the admin alert — only the synchronous database write blocks the save; everything else runs asynchronously off separate queues.

This is the **hub** for the shared mechanism, so feature pages for individual notifications (order-confirmation email, abandoned-cart email, status-change SMS, etc.) don't have to repeat it. The detail is split across the five aspect pages below.

## Sub-pages (in this cluster)

The Assistant should drill into the aspect that matches the question, not read every page.

- [[notification-delivery-event-spine]] — the event → subscriber → queued job pattern; the four-channel fan-out table; the queue layout (`analytics2`, `order-events8`, `cc-system6`, mail, `campaigns-process`); per-order analytics delays.
- [[notification-delivery-retry]] — the per-channel retry profiles; webhook 6-attempts-over-15-minutes timeline + auto-disable codes; analytics hourly auto-resume; email reap-and-retry.
- [[notification-delivery-admin-alerts]] — the bell-icon Alerts feed; what raises an alert; in-panel alert vs. email escalation; no "mute the bell".
- [[notification-delivery-email-inventory]] — the ~30 customer-facing transactional email labels; the three bypass labels; the `customer_email_notifications` master switch.
- [[notification-delivery-suppression]] — the per-order `notify_customer` flag; the absence of a merchant-facing global mute; the analytics-only ops kill switch; marketing vs. transactional suppression.

## Scope

What this concept covers (across the five sub-pages):

- The shared event → subscriber → queued job pattern for all four outbound channels.
- The merchant-facing webhook system (`Settings → Webhooks`) and its retry semantics (full detail on [[settings-hooks]]).
- The admin-panel alert system — the bell icon at the top right of the admin panel.
- How [[analytics-pipeline|the analytics pipeline]] consumes the SAME event stream as the webhook pipeline.
- Email and SMS dispatch flow at a high level (per-channel details live on their feature pages).

What it does NOT cover:

- Marketing-campaign segmentation and audience selection (lives under Marketing → Campaigns).
- Inbound webhook handling (receiving HTTP from payment providers / couriers) — a different pattern under Apps.
- Push notifications to mobile apps — CloudCart has no mobile push channel today.

## Contrasts

- **Notification delivery vs. marketing campaigns**: notification delivery is **transactional** (one event → one or more outbound messages, no targeting / segmentation). Marketing campaigns are **broadcast** (one merchant action → message to a chosen segment). Different jobs, different queues. See [[notification-delivery-event-spine]].
- **Notification delivery vs. analytics aggregation**: both subscribe to the same events; notification subscribers dispatch the email / SMS / webhook job, analytics subscribers dispatch the per-order denormalisation job. Independent consumers, no shared state. See [[analytics-pipeline]].
- **Admin-panel alerts vs. customer-facing notifications**: alerts (the bell icon) are read by the merchant inside the admin panel; customer-facing notifications go to the customer's inbox / phone. Same infrastructure, different audience. See [[notification-delivery-admin-alerts]].
- **Merchant-facing webhooks vs. internal platform webhooks**: the merchant-facing system runs on `order-events8`; there is a SECOND internal-only webhook system on `cc-system6` that is NOT what the merchant configures on `Settings → Webhooks`. See [[settings-hooks]].

## Where it applies

- [[settings-hooks]] — outbound webhook configuration screen.
- [[settings-admin-notifications]] — admin-panel alert recipients / preferences.
- [[analytics-pipeline]] — the same event stream that drives webhooks also drives per-order analytics.
- [[apps-google-analytics]] — another parallel consumer of the same storefront events.
- [[settings-queue-view]] — visible queues that carry these jobs.
- [[settings-statuses]] — `order.updated` webhooks and status-change emails both fire on status change.
- [[marketing-omnichannel-mails-list]] — where transactional email templates are edited.
- [[orders-notify-customer]] — the per-order suppression toggle.

## Related

- [[settings-hooks]] — outbound webhook system, full retry detail.
- [[settings-admin-notifications]] — admin-panel alert recipients.
- [[settings-queue-view]] — visible queue list.
- [[analytics-pipeline]] — analytics is one consumer of this same event stream.
- [[settings-statuses]] — status-change events drive status-change emails and `order.updated` webhooks.
- [[order-status-workflow]] — lifecycle of an order's status, all of whose transitions emit events.
- [[cart-vs-order-lifecycle]] — cart events also flow through this pipeline.
- [[settings-api-keys]] — webhook authentication credential.
- [[background-queue-inventory]] — catalogue of all background processes; lists the outbound queues and their schedules / Queue View visibility.
- [[order-processing-pipeline]] — order events are the most common source of email/webhook/admin-notification fan-out.
- [[marketing-omnichannel-mails-list]] — transactional email template editor.

## Open Questions

None — all previously-flagged items resolved or distributed to sub-pages.
