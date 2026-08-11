---
type: concept
aliases: ["Notification event spine", "Event-driven fan-out", "Notification queue layout", "Four-channel fan-out", "Notification subscribers"]
tags: [notifications, events, webhooks, queues, concepts]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[notification-delivery]]. See the hub for the other aspects (retry semantics, admin alerts, transactional email inventory, customer suppression).

# Notification delivery — the event spine

## Definition

The shared mechanism behind every outbound notification in CloudCart. When something happens in the store — a new order, a product change, a customer registration, a webhook receiver going down, an analytics aggregation finishing — a single in-store event fires **once** on the main request thread, and a set of independent **subscribers** fan the work out to **queued jobs**. Each job owns exactly one delivery channel: one job sends an email, another delivers a webhook, another writes the per-order analytics document, another raises an admin alert.

The unifying rule is **fire the event once, let independent subscribers fan out to queues**. This is why a merchant clicking "Save Order" doesn't wait for the email to be sent, the webhook to be delivered, the analytics document to be denormalised, and the admin alert to be checked — only the synchronous database write blocks the save. Everything else happens asynchronously, in the background, off separate queues.

## Scope

What this covers:

- The event → subscriber → queued job pattern shared across all four channels.
- The four-channel fan-out table (which event drives which webhook / analytics / email / alert).
- The queue layout — which queue carries which kind of job.
- Why each subscriber runs independently with no shared state.

What it does NOT cover:

- The per-channel retry profiles — see [[notification-delivery-retry]].
- The admin-alert surface itself (the bell icon) — see [[notification-delivery-admin-alerts]].
- The catalogue of transactional email types — see [[notification-delivery-email-inventory]].
- Per-order customer suppression and the absence of a global mute — see [[notification-delivery-suppression]].

## Contrasts

- **Notification delivery vs. marketing campaigns**: notification delivery is **transactional** (one event → one or more outbound messages, no targeting / segmentation). Marketing campaigns are **broadcast** (one merchant action → message to a chosen segment of subscribers). They use different jobs and different queues — campaign work runs on `campaigns-process`.
- **Notification delivery vs. analytics aggregation**: both subscribe to the same in-store events (e.g., `OrderCreated`). Notification subscribers dispatch the email / SMS / webhook delivery job; analytics subscribers dispatch the per-order denormalisation job onto `analytics2`. Independent consumers, no shared state — see [[analytics-pipeline]].
- **Merchant-facing webhooks vs. internal platform webhooks**: the merchant-facing webhook system runs on the `order-events8` queue. There is a SECOND, internal-only webhook system on the `cc-system6` queue — that one is platform internal, NOT what the merchant configures on `Settings → Webhooks`. See [[settings-hooks]].

## Where it applies

- [[settings-hooks]] — outbound webhook configuration screen; the webhook channel of the fan-out.
- [[analytics-pipeline]] — the analytics consumer reads the same event stream.
- [[settings-queue-view]] — the visible queues that carry these jobs.
- [[settings-statuses]] — status-change emails and `order.updated` webhooks both fire on the same status-change event.
- [[apps-google-analytics]] — another parallel consumer of the same storefront events.

## How the four channels share one event spine

| In-store event | Webhook (Settings → Webhooks) | Analytics | Email / SMS | Admin alert |
|--------------|-------------------------------|-----------|-------------|-------------|
| Order created | `order.created` webhook (60s delay if multi-webhook) | per-order job on `analytics2`, 60s delay | order-confirmation email; SMS if configured per app | none by default; merchant can configure |
| Order status change | `order.updated` webhook | per-order job on `analytics2`, immediate | status-change email / SMS per [[settings-statuses]] | none |
| Fulfilment add / remove | `order.updated` webhook | per-order job | shipping-notification email | none |
| Order payment updated | `order.updated` webhook | per-order job | payment-receipt email | none |
| Order line-item add / edit / remove | `order.updated` webhook | per-order job (5s delay) | usually silent for merchant edits | none |
| Product created / updated / deleted | `product.created` / `.updated` / `.deleted` webhook | no analytics job — products are catalogue, not events | none | none |
| Customer created | `customer.*` webhook | none | welcome email if configured | none |
| Subscriber created | `subscriber.*` webhook | links the subscriber UUID (see below) | subscription-confirmation email | none |
| Webhook delivery hard-fails (HTTP 404 / 410 / DNS) | this IS the webhook system | none | none | alert raised, surfaces on the bell icon |
| Analytics aggregation failure | none | logged at job level | none | none |
| Async export complete | none | none | no — uses admin alert instead | alert raised with the export download link |

Each subscriber binds its own handler per event and queues its own job. A single order-created event can therefore fan out to a webhook (if subscribed), an analytics job (always, unless the site is opted out), a confirmation email (if the mail template is enabled), and — rarely — an admin alert, all at once, all independently.

## Queue layout (verified)

| Queue name | What runs there |
|------------|-----------------|
| `analytics` | Hourly aggregation jobs (visitors, devices, traffic source, products — see [[analytics-pipeline]]) |
| `analytics2` | Per-order denormalisation jobs |
| `analytics8` | Driver-level scheduling (recurring aggregation trigger, industry statistic) |
| `order-events8` | Merchant-facing webhook deliveries (first attempt + retries) |
| `cc-system6` | Internal-only platform webhook job |
| Mail queue (default) | Transactional emails (order confirmation, status change, password reset, etc.) |
| `campaigns-process` | Marketing-campaign processing, including browser-data collection for marketing analytics |

All analytics, order-event, and webhook queues run on the `the analytics store-queue-hetzner-cloud` connection in production (`the analytics store-queue-local` in development). See [[background-queue-inventory]] for the full catalogue of background processes and their visibility on [[settings-queue-view|Queue View]].

### Per-order analytics fast lane

When the platform fires the order-created event, the analytics order subscriber enqueues a job onto `analytics2` with a 60-second delay. The delay is deliberate — it gives the checkout / order-creation request time to commit cleanly without the analytics write contending for the same site DB connection. For lighter line-edit events (line-item add / edit / remove, discount changes, shipping changes, payment updates) the delay is 5 seconds. For status-change / fulfilment / payment-sync events the delay is 0 (immediate dispatch).

### Side-effect work runs after the response is sent

Some bindings queue their side-effect on response `terminate` — i.e. AFTER the response has already been sent to the visitor's browser. The subscriber-UUID binding (linking an anonymous visitor's UUID to a known subscriber) works this way: the visitor never waits for the analytics binding write. Browser-data collection is additionally rate-limited via cache — the data-layer endpoint dispatches its collection job onto `campaigns-process` only once per unique user-agent per week, preventing one job per visitor from flooding the queue.

## Related

- [[notification-delivery]] — hub.
- [[settings-hooks]] — outbound webhook system + queue.
- [[analytics-pipeline]] — analytics consumer of the same event stream.
- [[settings-queue-view]] — visible queue list.
- [[background-queue-inventory]] — full catalogue of background processes and their queues / schedules.
- [[settings-statuses]] — status-change events drive both emails and `order.updated` webhooks.
- [[order-processing-pipeline]] — order events are the most common source of fan-out.

## Open Questions

None.
