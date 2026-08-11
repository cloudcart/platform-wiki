---
type: feature
nav_path: "Marketing → Channels → Channels setup → Web Push → Send pipeline"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["Web Push send pipeline", "Web push notification campaign step", "web_push.title web_push.body", "WebPush merge tags", "Web Push pre-flight checks", "CampaignWebPushSend", "Уеб пуш изпращане"]
tags: [marketing, channels, web-push, send-pipeline, validation, merge-tags, plan-gate]
plan_gates: ["campaign.channel.web_push"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-channels-webpush]]. See the hub for the other aspects (storefront prompt, subscription flow, VAPID config, DLR webhook, system messages, browser support).

# Web Push channel — Send pipeline

## Purpose

This aspect documents what happens **per recipient** when a campaign step of type **Web push notification** (`web_push`) fires: the message validation, the per-subscriber pre-flight checks, the restricted set of merge tags, the queued job that signs and POSTs the payload to the browser-vendor push service, and the status mapping that lands back on the campaign log.

The plan-cap key is **`campaign.channel.web_push`** — typically much higher than Email / SMS / Viber because the actual push delivery is **delivery-free for CloudCart** (browser-vendor push services don't charge). The cap exists to prevent abuse, not to track per-message cost.

## Where to find it

The campaign step is built in the campaign editor — sidebar → **Marketing** → **Campaigns** → open a campaign → add a step with action **"Web push notification"** (`web_push`). The editor shows a **rich-card message editor** with title, body, icon URL, image URL, click destination URL, and internal title.

The pipeline itself runs in the queue worker — no merchant-facing surface beyond the campaign step builder and the per-message [[webpush-channel-dlr-webhook|delivery log]].

## What the merchant can do here

- Build a Web Push campaign step with title / body / icon / image / link.
- Insert the three allowed merge tags into title or body — `{$subscriber_first_name}`, `{$subscriber_last_name}`, `{$shop_name}`.
- Run a **test send** to themselves (uses the same pipeline; counts against the plan cap unless the channel is sandboxed).
- Toggle **Sandbox** mode at the channel level — redirects sends to a webhook URL for inspection instead of the real push service.

## Settings & fields

### Hard-coded message limits

| Field | Validation rule |
|---|---|
| `web_push.title` | `required\|string\|max:63` — the notification headline |
| `web_push.body` | `required\|string\|max:128` — the notification body |
| `web_push.icon` | `string\|url` — small icon (e.g., 192×192) |
| `web_push.image` | `string\|url` — large hero image (e.g., 360×240) |
| `web_push.data.link` | `string\|url` — destination URL when the customer taps |
| `web_push.icon_type` | `in:internal,external` |
| `web_push.image_type` | `in:internal,external` |
| `internal_title` | `required\|string\|max:191` — merchant-side reference label |

The 63 / 128 limits reflect the typical browser-vendor maximums for visible title and body. Going over truncates the message client-side (most browsers add an ellipsis), which is why the platform pre-validates.

### Sandbox

| Setting | Effect |
|---|---|
| `sandbox_status = true` + `sandbox_url` | Sends are POSTed to `sandbox_url` for inspection instead of the real push service. Useful for debugging payloads. |

### Plan-cap key

| Key | Notes |
|---|---|
| `campaign.channel.web_push` | The per-merchant per-period send count cap. Typically much higher than Email / SMS / Viber (often unlimited on common tiers) because delivery is free for CloudCart. |

## Business rules

### Restricted merge tags — only 3 placeholders allowed

The Web Push channel overrides the universal tag set (Email / SMS / Viber expose dozens of tags including discount codes, order info, segment-bound vars) and keeps **only** three placeholders:

| Tag | Renders |
|---|---|
| `{$subscriber_first_name}` | Recipient's first name |
| `{$subscriber_last_name}` | Recipient's last name |
| `{$shop_name}` | Store's display name |

Other tags (`{$customer_email}`, `{$verify_url}`, `{$order_id}`, discount codes, etc.) are NOT rendered — they pass through as literal text. The 128-char body limit makes longer dynamic content impractical.

### Per-subscriber pre-flight checks

For each Web Push send, the platform checks the recipient's WebPush channel row:

- `channel_identifier` non-empty.
- `data.endpoint`, `data.keys.p256dh`, `data.keys.auth` all non-empty.
- `unsubscribed = 0`, `marketing = 1`, `bounced = 0`.
- The message template must have a non-empty body.

Note: unlike Email / SMS / Viber, Web Push does **NOT** require `verified = 1` — the act of accepting the native browser permission prompt and obtaining a valid push endpoint IS the verification. See [[webpush-channel-subscription-flow]].

### Queued dispatch — 5× retry, 2s backoff, 3s timeout

Sends are queued, not synchronous. The campaign action dispatches a Web Push send job with `retry(5, ..., 2000)`. Per-send Guzzle timeout to the push service is **3 seconds** (`client_options.timeout` — see [[webpush-channel-vapid-config]]).

### Send-request shape — exact HTTP

The queued job POSTs to the recipient's `endpoint` URL:

```
POST <recipient's endpoint URL>
Authorization: WebPush <VAPID JWT signed with VAPID_PRIVATE_KEY>
Crypto-Key: p256ecdsa=<VAPID public key>
Content-Encoding: aes128gcm
TTL: <seconds before the push service gives up retrying>
Content-Type: application/octet-stream
Body: <ECIES-encrypted JSON payload — title, body, icon, image, data, dlrUrl>
```

The browser's push service forwards the encrypted payload to the device, which decrypts it locally with its `p256dh` private key. CloudCart never sees the decrypted contents — push services are end-to-end encrypted between sender and device.

### Push payload includes the DLR webhook URL

The payload carries a `dlrUrl` field pointing at the per-store delivery-report webhook (`campaigns.channels.channel.web_push.webhook?site_id=...`). When the customer's browser receives the notification and OS-displays it, the service-worker fires a "displayed" / "clicked" callback back to that URL — updating the campaign log row. See [[webpush-channel-dlr-webhook]] for the webhook side.

### Variable substitution + URL shortening

The pipeline processes three keys for variable substitution: `title`, `body`, `data.link`. If `data.link` is empty after substitution, it falls back to the storefront's primary URL — so the customer always lands somewhere if they tap. Empty title / body render as empty strings without erroring.

The `data.link` URL goes through the same `cc_campaign[...]` shortener as Email / SMS / Viber, with `utm_medium = 'web_push'` injected. When the customer taps the notification and lands on the storefront, the click is recorded against the campaign + step + recipient.

### Conditional branching — `link_clicked` only

Web Push exposes only `link_clicked` / `link_not_clicked` campaign-step conditions. It does NOT support `message_read` — push services don't reliably report when the notification was displayed. For "did the recipient see it" branching, use Email or SMS.

### Status mapping — push service response → CloudCart log status

| Push service response | CloudCart log status |
|---|---|
| (success) | `SENT` |
| (subscription expired — `isSubscriptionExpired = true`) | `NOT_SENT` (with `expired` reason) — also flips the subscriber's WebPush channel to `bounced = 1` |
| `PENDING` | (null — keep current status, await DLR webhook) |
| (anything else / empty) | `NOT_SENT` |

### Expired subscription → permanently bounced

When the push service reports the subscription expired (the customer revoked permission, cleared site data, or uninstalled the browser), the per-recipient return value is the literal string `'expired'`. The downstream listener interprets this as a permanent failure and updates the subscriber's WebPush channel to `bounced = 1` so future campaigns skip it. The log row records `STATUS_NOT_SENT` with the expired marker. See [[webpush-channel-dlr-webhook]] for the downstream listener.

### Demo / test sends

Unlike Email (which bypasses Elastic Email for test sends — see [[email-channel-send-pipeline]]), Web Push test sends go through the same pipeline because the push service is free anyway. Test sends count against the plan-cap (verify) but cost CloudCart nothing.

## Related

- [[marketing-channels-webpush]] — hub.
- [[webpush-channel-vapid-config]] — provides the `VAPID_PRIVATE_KEY` used to sign every outgoing request.
- [[webpush-channel-subscription-flow]] — provides the `endpoint` + `p256dh` + `auth` consumed by every send.
- [[webpush-channel-dlr-webhook]] — receives the displayed / clicked callbacks the storefront's service-worker posts after a successful send.
- [[webpush-channel-system-messages]] — same pipeline, triggered by internal platform events (order status change, etc.) instead of campaigns.
- [[marketing-campaigns]] — campaigns use this pipeline for `web_push` action steps.
- [[email-channel-send-pipeline]] — sibling pipeline; demo-send semantics differ (Email bypasses Elastic Email, Web Push doesn't bypass).

## Open questions

- ⏸️ Whether test sends count against the plan-cap or are exempt — Email exempts them via the transactional `MailManager`, Web Push doesn't have an equivalent fallback path, but explicit verification of "test send counts toward cap" not done here.
