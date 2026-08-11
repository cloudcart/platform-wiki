---
type: feature
nav_path: "Marketing → Channels → Channels setup → Web Push → System messages"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["Web Push system messages", "WebPush transactional templates", "order_status_change web push", "order_status_fulfillment_change web push", "Системни съобщения уеб пуш"]
tags: [marketing, channels, web-push, system-messages, transactional, internal-events]
plan_gates: ["campaign.channel.web_push"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-channels-webpush]]. See the hub for the other aspects (storefront prompt, subscription flow, VAPID config, send pipeline, DLR webhook, browser support).

# Web Push channel — System messages

## Purpose

The **System messages - Web Push** modal manages **per-event Web Push templates** that fire on internal platform events (order status change, fulfilment change) — not on merchant-built campaigns. Like Viber, Web Push maintains its own table of per-event templates (`web_push_system_messages`) with per-language rows. These templates are fired by internal events and are completely separate from the `web_push` campaign step ([[webpush-channel-send-pipeline]]).

The same channel pipeline (signing, encryption, send job, DLR webhook) is reused — what differs is the trigger (internal event vs campaign step) and the message source (per-event template vs ad-hoc campaign content).

## Where to find it

Sidebar → **Marketing** → **Channels** → **Channels setup** → **Web Push** channel card → **System Message** action. Title — *"System messages - Web Push"*. Lists **2 event templates**, each as a row with label + send-count + on/off switch.

Clicking a row opens the nested editor (`MarketingChannelsSystemMessagesConfiguration`) which surfaces four editable sections + a right-hand Chrome-style notification card live-preview.

## What the merchant can do here

- See the **2 event templates** and toggle each on or off via the row switch.
- See the per-template **send count** (driven by the [[webpush-channel-dlr-webhook|DLR webhook]] — `sent_count` increments on `DELIVERED` / `CLICKED`).
- Open a template to edit title, body, icon, image — see live preview.
- Insert merge tags from the variables legend (clickable pills copy to clipboard) — only 3 placeholders supported, same as campaigns.

## Settings & fields

### Event template list — exactly 2 rows

| Event | Label shown |
|---|---|
| `order_status_change` | When order status is changed |
| `order_status_fulfillment_change` | When order fulfilment status is changed |

Each row: label + send-count + on/off switch — identical layout to [[marketing-channels-viber|Viber]] system messages.

### Nested editor — four editable sections

When the merchant opens a template, the editor (`MarketingChannelsSystemMessagesConfiguration` configured for Web Push) shows:

| Section | Field | Editor type | Validation |
|---|---|---|---|
| 1 | **Web Push title** | Pill editor with variable insertion + AI assist + remaining-character counter | `required, max 63 chars` |
| 2 | **Web Push body** | Multiline pill editor with variable insertion + AI assist + remaining-character counter | `required, max 128 chars` |
| 3 | **Web Push icon** | Storage-type selector (Internal storage vs External URL), URL input (read-only when Internal), clear X, **Add image** link → `CcImageModal`, preview pane | `string\|url` |
| 4 | **Web Push image** | Same controls as icon, separate URL field | `string\|url` |

### Right-hand live preview

A Chrome-style notification card showing exactly what the customer will see in their browser's notification tray:

- Title (top line)
- Body (second line)
- Icon (thumbnail on the left)
- Image (large hero on the right)
- Host (from server settings — the storefront domain)
- Timestamp shown as *"now"*

### Allowed merge tags

Only three tags are rendered — identical to campaign-side Web Push (see [[webpush-channel-send-pipeline]] *"Restricted merge tags"*):

- `{$subscriber_first_name}`
- `{$subscriber_last_name}`
- `{$shop_name}`

The variables legend at the bottom of the editor shows clickable variable pills that auto-copy to clipboard for easy paste-in.

## Business rules

### System messages are per-language

The `web_push_system_messages` table has per-language rows — the merchant can have a different title/body per storefront language. The editor surfaces a language picker (verify) and saves a row per language.

### Switch OFF stops the send entirely

When the row switch is OFF, the corresponding internal event does NOT trigger a Web Push send for that template — even if subscribers exist. This is the merchant's "I don't want push notifications for order status changes" toggle.

### Same pipeline as campaigns — same validation, same pre-flight checks

System-message sends go through the **same** channel send pipeline as campaign sends — the only difference is the trigger source and the template lookup. That means:

- Same 63 / 128 character limits enforced.
- Same per-subscriber pre-flight checks (endpoint, p256dh, auth, `unsubscribed = 0`, `marketing = 1`, `bounced = 0`).
- Same retry policy (5× retries, 2-second backoff).
- Same signing with the platform VAPID private key.
- Same DLR webhook used for displayed / clicked feedback.

See [[webpush-channel-send-pipeline]] for the full pipeline.

### Send-count increments come from the DLR webhook

The `sent_count` shown next to each template is incremented by the [[webpush-channel-dlr-webhook|DLR webhook]] when the log row's status flips to `DELIVERED` or `CLICKED` AND the log row carries the matching `system_message_id`. Campaigns do not contribute to this counter — they have their own stats surfaces.

This means the counter measures **delivered+clicked notifications**, not "messages attempted to send". A merchant who sees `sent_count = 0` on an active template might still be successfully sending — just no devices have reported back `DELIVERED` yet.

### Event-driven, not subscriber-targeted

The system-message send fires once per **event** (an order status change) and resolves the recipient from the event payload — the order's customer's subscriber-side WebPush channel. Campaigns target subscriber **lists**; system messages target the specific customer attached to the event.

### Sandbox mode applies here too

When the channel is in sandbox mode (`sandbox_status = true`), system-message sends also redirect to `sandbox_url` instead of the real push service. The merchant cannot scope sandbox to campaigns only.

## Related

- [[marketing-channels-webpush]] — hub.
- [[webpush-channel-send-pipeline]] — shared send pipeline (validation, pre-flight checks, retries).
- [[webpush-channel-dlr-webhook]] — the webhook that increments per-template `sent_count`.
- [[webpush-channel-storefront-prompt]] — popup that drives subscription, which gates whether system messages have any recipients.
- [[marketing-omnichannel-mails-list]] — sibling concept: per-event templates for Email / SMS / Viber / Web Push managed centrally.
- [[marketing-channels-system-messages]] — cross-channel system-messages hub if it exists.
- [[orders-status-change]] — the event source for `order_status_change`.
- [[marketing-channels-viber]] — Viber has identical system-message UI patterns.

## Open questions

- ⏸️ Per-language UI behaviour of the editor (assumed language picker, not directly verified here).
- ⏸️ Whether sandbox can be scoped to campaigns vs system messages separately (currently assumed channel-wide).
