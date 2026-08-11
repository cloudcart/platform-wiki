---
type: feature
nav_path: "Marketing → Channels → Channels setup → Web Push → Delivery webhook"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["Web Push DLR", "Web Push delivery report", "dlrUrl", "WebPush webhook", "campaigns.channels.channel.web_push.webhook", "Web Push delivery status", "Уеб пуш доклад за доставка"]
tags: [marketing, channels, web-push, webhook, dlr, delivery-report, bounced]
plan_gates: ["campaign.channel.web_push"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-channels-webpush]]. See the hub for the other aspects (storefront prompt, subscription flow, VAPID config, send pipeline, system messages, browser support).

# Web Push channel — Delivery-report webhook

## Purpose

The Web Push **delivery-report (DLR) webhook** receives "displayed" / "clicked" callbacks from the customer's browser AFTER a Web Push send has been accepted by the push service. The push payload includes a `dlrUrl` field that the storefront's service-worker calls back to when the OS-level notification UI fires. This is how the campaign log learns that a particular message was actually shown on the customer's device, and how `CLICKED` status (which drives `link_clicked` branching) propagates back to the campaign step.

The webhook also handles the **subscription-expired** flag from the send pipeline, flipping the subscriber's WebPush channel to `bounced = 1` so future campaigns skip the dead endpoint.

## Where to find it

There is no merchant-facing UI for this webhook — it's a platform-owned endpoint hit by the storefront's service worker. The merchant sees the **result** on the campaign step's log surface ([[marketing-channels-logs]]) — each row's status reflects what the webhook recorded.

Route name: `campaigns.channels.channel.web_push.webhook`. Pattern: `messages/web-push/{site_id}` (or similar — verify). The `dlrUrl` value in the push payload is `campaigns.channels.channel.web_push.webhook?site_id=<id>`.

## What the merchant can do here

Nothing directly. The merchant can:

- View per-message delivery status on the Web Push **Logs** modal — status values are written by this webhook.
- See the resulting `bounced = 1` state on a subscriber's WebPush channel row in [[marketing-subscribers]] (subscribers with `bounced = 1` are skipped on future sends).
- See the **system-message sent-count** counters increment on the [[webpush-channel-system-messages|System messages]] screen when an internal-event-driven send is delivered / clicked.

## Settings & fields

### Required webhook inbound fields

The webhook validates the inbound POST has BOTH:

| Field | Validation | Effect if missing |
|---|---|---|
| `message_hash` | Required | HTTP 400 |
| `status` | Required | HTTP 400 |

If both are present, the webhook dispatches a queued processor to update the matching campaign-log row.

### Status-mapping table

| Inbound `status` value | Result on the log row |
|---|---|
| `PENDING` | (null — keep current status; the send is still in flight) |
| `DELIVERED` | Sets log row status to `DELIVERED`. If the row carries `system_message_id`, also increments that system-message template's `sent_count`. |
| `CLICKED` | Sets log row status to `CLICKED`. Same `system_message_id` increment as above. Drives the `link_clicked` campaign-step condition for branching. |
| (empty / null) | Sets log row status to `STATUS_NOT_SENT`. |
| (any other non-empty value) | Sets log row status to that value verbatim. |

### Expired subscription side-effect

Separately from the inbound webhook, when the [[webpush-channel-send-pipeline|send pipeline]] gets an `isSubscriptionExpired = true` from the push service, the per-recipient return value is the literal string `'expired'`. The downstream listener updates the subscriber's WebPush channel:

| Field | Set to |
|---|---|
| `bounced` | `1` |

This permanently disqualifies the WebPush channel from future sends.

## Business rules

### Logged-in admin clicks are filtered out

The DLR webhook handler returns an empty response (no processing) when the inbound request is from a **`site` app namespace** AND has an **authenticated admin**. This prevents admin-side test clicks (when the merchant clicks their own test-send notification from the admin panel context) from polluting the merchant's campaign-log statistics. Real customer clicks (no admin auth in session) flow through normally.

### `PENDING` keeps current status

If the storefront's service-worker reports `PENDING` (e.g., the notification was queued by the OS but not yet displayed), the webhook does NOT overwrite the current log row status — it stays whatever the previous step set it to. This avoids clobbering a `SENT` status with a transient `PENDING`.

### `DELIVERED` / `CLICKED` increments system-message counters

If the campaign-log row carries a `system_message_id` (i.e., the send was triggered by an internal **system message** like order-status-changed, not by a campaign), and the new status is `DELIVERED` or `CLICKED`, the corresponding row in the `WebPushSystemMessages` table has its `sent_count` incremented. This drives the per-template send counts the merchant sees on the [[webpush-channel-system-messages|System messages]] modal.

Campaign-driven sends (no `system_message_id`) do not bump these counters — campaigns have their own stats surface.

### Expired → `bounced = 1` → skipped on future sends

The expired-subscription side-effect is **permanent** (until the customer re-subscribes from the storefront). The subscriber's WebPush channel row's `bounced` flag is checked on every send pre-flight (see [[webpush-channel-send-pipeline]] — *"Per-subscriber pre-flight checks"*). Once flipped to `1`, the merchant sees no more sends to that device + endpoint until the customer hits the [[webpush-channel-storefront-prompt|popup]] again and re-subscribes (which creates a new `endpoint` and a new WebPush channel row — the old one stays `bounced`).

### Webhook validation is permissive

The webhook accepts any non-empty `status` value (other than the special-cased `PENDING`) and writes it as-is. This means custom service-worker implementations could write arbitrary statuses to the log — there's no enum check. The platform's standard service worker only ever sends `DELIVERED`, `CLICKED`, `PENDING`, but a third-party PWA storefront could in theory write other values.

### Click attribution flows through the URL shortener, not this webhook

The actual **click event** (customer tapping the notification → landing on the storefront → click recorded against the campaign) is captured by the `cc_campaign[...]` URL shortener — see [[webpush-channel-send-pipeline]] *"URL shortening + UTM injection"*. The DLR webhook's `CLICKED` status is a parallel signal from the OS notification UI; the URL shortener is what records the actual landing-page click against the campaign step. In practice both fire for a real click — the webhook reports OS-level "user tapped the notification" and the shortener reports "user landed on the storefront from a campaign click".

### `message_hash` correlates the webhook to the log row

The `message_hash` field on the inbound webhook is the lookup key for finding the matching campaign-log row to update. It's set when the send job builds the push payload and embedded in the `dlrUrl` (or its callback body — verify). If the hash doesn't match any log row, the webhook silently no-ops.

## Related

- [[marketing-channels-webpush]] — hub.
- [[webpush-channel-send-pipeline]] — the send job that embeds the `dlrUrl` in every push payload and also surfaces the `expired` flag this webhook acts on.
- [[webpush-channel-subscription-flow]] — the subscribe handler that originally created the WebPush channel row that gets flipped to `bounced = 1` here.
- [[webpush-channel-system-messages]] — the `sent_count` counters this webhook increments.
- [[marketing-channels-logs]] — the per-channel log surface where these statuses become merchant-visible.
- [[marketing-subscribers]] — the subscribers screen where `bounced = 1` is surfaced and editable.

## Open questions

- ⏸️ Exact URL shape of the webhook (route name confirmed; full path not directly verified in this pass).
- ⏸️ Whether `message_hash` is the only correlation key or whether the webhook also accepts the log row's primary key.
