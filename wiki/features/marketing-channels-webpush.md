---
type: feature
nav_path: "Marketing → Channels → Channels setup → Web Push"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["Web Push", "Web push notifications", "Browser push", "Browser notifications", "Уеб пуш", "Пуш известия", "Browser push notifications"]
tags: [marketing, channels, web-push, vapid, pwa, browser-push]
plan_gates: ["campaign.channel.web_push"]
created: 2026-05-23
updated: 2026-06-10
source_count: 10
---

# Web Push channel

## Purpose

The **Web Push** channel delivers **browser push notifications** to the merchant's storefront visitors — short, tappable alerts that pop up on a customer's desktop or mobile browser even when the customer isn't on the merchant's site. Used for: cart abandonment recovery, restock alerts, promotional flash sales, order-status updates, and re-engagement of dormant subscribers.

Web Push works without an email address or phone number. The customer's "subscription identifier" is a per-device push endpoint URL (issued by their browser's push service — Mozilla Autopush, Google FCM, Apple WebPush gateway) plus a pair of cryptographic keys (`p256dh` + `auth`) the browser generated when the customer accepted the permission prompt. CloudCart stores these on the [[marketing-subscribers|subscriber's WebPush channel row]] and uses **VAPID** to sign every outgoing message so the browser's push service can verify the sender — see [[webpush-channel-vapid-config]].

The channel is **delivery-free for CloudCart** — the actual push delivery is handled by browser-vendor push services (free). The plan-cap on `campaign.channel.web_push` is therefore typically more generous than Email / SMS / Viber.

## Where to find it

Sidebar → **Marketing** → **Channels** → **Channels setup** (route `campaigns-channels`, `/admin/marketing-new/campaigns/channels`) → find the **Web Push** channel card. The card's actions (Install, Activate/Deactivate, Settings, System Message, Usage, Logs) open modals over the channels page — Web Push settings render in the `MarketingChannelsSettingsModalWebPush` sub-component.

Channel mapping key: `web_push`. Actions hit the channels API (base `/admin/api/core/marketing/campaigns/channels`): status via `POST /{type}/status`, usage via `GET /{type}/usage`, logs via `/{mapping}/logs-list`, settings via `/{type}/settings`. Install / uninstall is handled through the applications API (`/admin/api/core/applications`). The storefront subscribe endpoint is `POST /web-push-subscribe` (route `campaigns.channels.channel.web_push.subscribe`).

The channel is **not installed by default**. Merchant clicks **Install** to activate; no VAPID-key configuration is needed (CloudCart manages the platform-wide VAPID keys for all merchants — see [[webpush-channel-vapid-config]]).

## Sub-pages (in this cluster)

This feature is split into 7 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[webpush-channel-storefront-prompt]] — the **Settings - Web Push** modal; two-stage prompt design (CloudCart popup → native browser prompt); `checkout`, `popup_status`, `popup_text`, `popup_ok_button`, `popup_discard_button`, `popup_image`, `message`, `cookie_life_time`.
- [[webpush-channel-subscription-flow]] — `/web-push-subscribe` endpoint; `endpoint` + `p256dh` + `auth` keys; subscriber + WebPush channel row creation; `_cc_wp` cookie; implicit Email-channel link for logged-in customers; geo-IP + User-Agent capture.
- [[webpush-channel-vapid-config]] — platform-wide VAPID key pair; `VAPID_SUBJECT`, `VAPID_PUBLIC_KEY`, `VAPID_PRIVATE_KEY`, `VAPID_PEM_FILE`; `webpush:vapid` Artisan command; why merchants don't manage keys.
- [[webpush-channel-send-pipeline]] — message validation (`max:63` / `max:128`); per-recipient pre-flight checks; restricted merge tags (only 3); queued send job with 5× retry + 2-second backoff; HTTP send-request shape; push-service status mapping.
- [[webpush-channel-dlr-webhook]] — delivery-report webhook (`dlrUrl`); `message_hash` + `status` validation; status mapping (`DELIVERED` / `CLICKED` / `PENDING`); admin-click filter; expired → `bounced = 1`.
- [[webpush-channel-system-messages]] — System messages modal; 2 event templates (`order_status_change`, `order_status_fulfillment_change`); 4-section editor; live Chrome-style preview.
- [[webpush-channel-browser-support]] — Chrome / Firefox / Safari / iOS Safari / in-app-browser matrix; PWA requirement for Safari (16.1+ macOS, 16.4+ iOS); fallback strategy.

## What the merchant can do here

- **Install** the channel — adds Web Push to the configured channels list.
- **Activate / Deactivate** after install.
- **Settings** — configure the storefront permission-prompt UX. See [[webpush-channel-storefront-prompt]].
- **System messages** — manage per-event templates fired by internal events. See [[webpush-channel-system-messages]].
- **View Usage** — sent-count vs plan cap.
- **View Logs** — per-message delivery status with content preview.
- **Use this channel in a campaign step** — action type **"Web push notification"** (`web_push`). See [[webpush-channel-send-pipeline]].

## Settings & fields

Detail lives on the aspect pages; this is the quick-reference index.

### Per-channel settings the merchant can toggle

| Setting | Default | Aspect page |
|---|---|---|
| `checkout` | `0` | [[webpush-channel-storefront-prompt]] |
| `popup_status` | `true` | [[webpush-channel-storefront-prompt]] |
| `message` | overlay caption default | [[webpush-channel-storefront-prompt]] |
| `popup_text` / `popup_ok_button` / `popup_discard_button` / `popup_image` | (see aspect) | [[webpush-channel-storefront-prompt]] |
| `cookie_life_time` | `7` (clamped to [1, 365]) — not exposed in UI | [[webpush-channel-storefront-prompt]] |
| `sandbox_status` + `sandbox_url` | OFF | [[webpush-channel-send-pipeline]] |

### Hard-coded message limits

| Field | Validation | Aspect page |
|---|---|---|
| `web_push.title` | `required\|string\|max:63` | [[webpush-channel-send-pipeline]] |
| `web_push.body` | `required\|string\|max:128` | [[webpush-channel-send-pipeline]] |
| `web_push.icon` / `web_push.image` | `string\|url` | [[webpush-channel-send-pipeline]] |
| `web_push.data.link` | `string\|url` | [[webpush-channel-send-pipeline]] |
| `web_push.icon_type` / `web_push.image_type` | `in:internal,external` | [[webpush-channel-send-pipeline]] |
| `internal_title` | `required\|string\|max:191` | [[webpush-channel-send-pipeline]] |

### Platform-level VAPID (the platform code)

| Setting key | Source | Aspect page |
|---|---|---|
| `vapid.subject` | `env('VAPID_SUBJECT')` | [[webpush-channel-vapid-config]] |
| `vapid.public_key` | `env('VAPID_PUBLIC_KEY')` | [[webpush-channel-vapid-config]] |
| `vapid.private_key` | `env('VAPID_PRIVATE_KEY')` | [[webpush-channel-vapid-config]] |
| `vapid.pem_file` | `env('VAPID_PEM_FILE')` | [[webpush-channel-vapid-config]] |
| `client_options.timeout` | `3` (seconds) | [[webpush-channel-vapid-config]] |

### Allowed merge tags

| Tag | Aspect page |
|---|---|
| `{$subscriber_first_name}` | [[webpush-channel-send-pipeline]] |
| `{$subscriber_last_name}` | [[webpush-channel-send-pipeline]] |
| `{$shop_name}` | [[webpush-channel-send-pipeline]] |

### Plan-gate key

| Key | Notes |
|---|---|
| `campaign.channel.web_push` | Send-count cap. Typically much higher than other channels — push delivery is free for CloudCart. |

## Business rules

The deep mechanics live on each aspect page; what every merchant must know at this level:

- **Single platform VAPID key pair signs every storefront.** Merchants don't bring or generate VAPID keys. See [[webpush-channel-vapid-config]].
- **`verified = 1` is implicit — no double opt-in.** Unlike Email / SMS / Viber, accepting the native browser permission prompt IS the verification gate. No `unconfirmed_send` switch. See [[webpush-channel-subscription-flow]].
- **Two-stage prompt design.** The CloudCart pre-prompt popup fires first; only customers who click Allow ever see the native browser prompt. Preserves the merchant's ability to re-prompt (the native prompt is one-shot per user). See [[webpush-channel-storefront-prompt]].
- **Only 3 merge tags allowed.** `{$subscriber_first_name}`, `{$subscriber_last_name}`, `{$shop_name}`. The 128-char body limit makes longer dynamic content impractical. See [[webpush-channel-send-pipeline]].
- **Conditional branching: `link_clicked` only.** No `message_read` — push services don't reliably report displayed. See [[webpush-channel-send-pipeline]].
- **Expired subscription → `bounced = 1` permanently** until the customer re-subscribes. See [[webpush-channel-dlr-webhook]].
- **Safari requires the PWA path.** Web Push on Safari (macOS 16.1+ / iOS 16.4+) only works when the storefront is installed as a Web App. In-app browsers (Instagram, Facebook, TikTok) cannot subscribe at all. See [[webpush-channel-browser-support]].
- **Logged-in admin clicks are filtered from stats** by the DLR webhook to keep campaign statistics clean. See [[webpush-channel-dlr-webhook]].

## Related

- [[marketing-channels]] — parent channels hub (multi-channel framework + auto-suspend triggers).
- [[marketing-campaigns]] — campaigns use this channel for Web Push delivery steps.
- [[marketing-subscribers]] — subscribers' WebPush channel rows store `endpoint` + `p256dh` + `auth` keys.
- [[marketing-campaigns-policy]] — anti-spam policy that protects the shared VAPID identity.
- [[marketing-omnichannel-mails-list]] — transactional notifications (some events have WebPush system-message templates).
- [[marketing-channels-logs]] — per-channel log surface where DLR statuses become merchant-visible.
- [[notification-delivery]] — outbound delivery concept page.
- [[checkout-flow]] — the `checkout.return` route is where the Web Push popup fires when `checkout = true`.
- [[channel]] — Channel entity reference.
- [[marketing-channels-viber]] — sibling channel; identical System messages UI patterns.
- [[marketing-channels-email]] — universal fallback channel for customers Web Push can't reach.

## Open questions

No outstanding questions at the hub level. See aspect pages for narrow uncertainties.
