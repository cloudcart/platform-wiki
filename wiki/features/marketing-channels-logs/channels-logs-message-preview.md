---
type: feature
nav_path: "Marketing → Channels → Channels setup → Logs → Message Preview"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["Channel logs message preview", "Message preview modal", "Email log preview", "Viber log preview", "Web Push log preview", "SMS log preview", "Channel mobile phone preview"]
tags: [marketing, channels, logs, preview, email, sms, viber, webpush]
plan_gates: ["campaign.channel.email", "campaign.channel.sms_msghub_message", "campaign.channel.sms_nth_message", "campaign.channel.web_push", "viber_messages"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-channels-logs]]. See the hub for the other aspects (table view, status vocabulary, subscriber drill-down, row lifecycle, system vs campaign).

# Channel logs — message preview

## Purpose

The **Message Preview** sub-modal shows the merchant exactly what was sent to the recipient — the rendered HTML for Email, or a mobile-phone-frame card for Viber / SMS / Web Push. It opens when the merchant clicks the channel icon on any log row in the [[channels-logs-table-view|table view]].

Modal size: `xll` for Email (to fit the iframe-rendered HTML); `lg` for Viber / SMS / Web Push. Title — *"Message Preview"*. Cancel button: *"Close"*. No Save button (read-only).

The body is a loader while the preview data is fetched, then renders per-channel content via the `MarketingChannelsLogsPreviewMessageData` component which branches on the channel type.

## Where to find it

Sidebar → **Marketing** → **Channels** → **Channels setup** → channel card's **Logs** button → click the channel icon (with tooltip *"Preview message"*) on any row.

## What the merchant can do here

- **See the message as the recipient saw it** — exact HTML render for Email, mobile-phone preview for SMS / Viber / Web Push.
- **Read the delivery metadata** — recipient destination, subscriber id, current status, and the four delivery timestamps.
- **See the campaign / segment lineage** — campaign name, action step number, segment name + segment conditions text (when applicable).

## What the merchant cannot do

- **Cannot edit the message** — the preview is read-only. To change a campaign action or system message, the merchant goes to the campaign editor or the [[marketing-channels-system-messages|System messages]] modal.
- **Cannot resend from the preview** — no Resend button. To re-send to a subscriber, re-target via a campaign or trigger the system event again.
- **Cannot export the rendered HTML** — Email's preview is an iframe URL pointing at a per-log HTML viewer; there's no "download" or "copy source" action.

## Settings & fields

### Fields shown on the preview

| Field | Notes |
|-------|-------|
| Channel name + icon | Top-of-card. |
| Recipient destination | Email / phone / push endpoint. |
| Subscriber name + id | When the subscriber still exists. |
| Status + status colour | Same canonical status as the table row — see [[channels-logs-status-vocabulary]]. |
| `sent_at` | Dispatch timestamp. Always populated. |
| `delivered_at` | Set when the provider's delivery webhook reports back. |
| `seen_at` | Set when the provider's read-receipt webhook reports back. |
| `updated_at` | Last status change. |
| Campaign info | Campaign name + action step number (`action_order + 1`). Empty for system-message rows. |
| Segment info | Segment name + segment conditions text. Empty for sends not tied to a segment. |
| Message content | Channel-specific render (see below). |

### Per-channel render

- **Email** — rendered HTML inside an iframe (`min-h-[420px], h-[min(70vh,720px)]`) so the merchant sees exactly what landed in the recipient's inbox. The iframe URL is a one-shot preview endpoint returned by the API.
- **Viber** — mobile-phone-frame component shows a chat-bubble preview with text + image + button (when the Viber message includes them).
- **SMS** (MsgHub + NTH) — mobile-phone-frame shows the body in a chat bubble.
- **Web Push** — mobile-phone-frame renders a Chrome-style notification card with the icon, title, body, image, host, and *"Now"* timestamp.

## Business rules

### Email preview falls back to type-inference when channel mapping is null (verify)

If the response's `data.channel.mapping` is null but `message.iframe_url` is present, the preview component still treats the row as Email and renders the iframe. This handles edge cases where channel metadata was lost but the rendered HTML survives. (verify)

### Viber + SMS bodies convert line breaks to `<br/>`

Viber and SMS bodies typically contain `\r\n` / `\n` line breaks. The preview component converts these to `<br/>` so the chat-bubble preview displays the message with correct line wrapping rather than as one collapsed paragraph.

### Web Push card mirrors Chrome notification style

The preview deliberately uses the Chrome-style notification card layout (icon left, title top, body below, host underneath, *"Now"* timestamp) — independent of which browser the recipient actually used. This is a visual approximation, not a per-browser render.

### `sent_at` is always set; `delivered_at` and `seen_at` are conditional

The preview always shows `sent_at` because every log row is created at dispatch. `delivered_at` / `seen_at` appear only when the corresponding provider webhook reported them — for example, SMS NTH never reports `seen_at` because there's no read-receipt mechanism (see [[channels-logs-status-vocabulary]] for the per-channel source matrix).

### The preview API is a separate single-log endpoint

The merchant's click triggers a fetch keyed by `log_id`. The endpoint loads the row plus its related message-content record (where the actual HTML / Viber text / Web Push payload was stored at send time), then asks the channel manager to format it for the modal — Email returns an iframe URL pointing at a per-log HTML viewer; SMS / Viber / Web Push return the raw message structure for the mobile-phone-frame preview.

This separation means: log rows hold metadata only; the actual rendered content lives in a separate store and is fetched on demand. A merchant who clicks Preview on a very old row may see a slower load while that content is fetched.

## Related

- [[marketing-channels-logs]] — hub.
- [[channels-logs-table-view]] — click the channel icon on any row to open this modal.
- [[channels-logs-status-vocabulary]] — the Status field mirrors the table-row status.
- [[channels-logs-subscriber-drilldown]] — sibling sub-modal opened from the Subscriber column.
- [[channels-logs-row-lifecycle]] — why `sent_at` is always set and the other timestamps are conditional.
- [[marketing-channels-email]] / [[marketing-channels-sms-msghub]] / [[marketing-channels-sms-nth]] / [[marketing-channels-viber]] / [[marketing-channels-webpush]] — channel references.
- [[marketing-channels-system-messages]] — system-message template editor; the per-row content originates here for `system message` rows.

## Open questions

None.
