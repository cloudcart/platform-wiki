---
type: feature
nav_path: "Marketing → Channels → Channels setup → Web Push"
route_name: campaigns-channels
route_path: /admin/marketing/campaigns/channels
aliases: ["Web Push", "Web push notifications", "Browser push", "Browser notifications", "Уеб пуш", "Пуш известия", "Browser push notifications"]
tags: [marketing, channels, web-push, vapid, pwa, browser-push]
plan_gates: ["campaign.channel.web_push"]
created: 2026-05-23
updated: 2026-11-09
source_count: 11
---

# Web Push channel

## Purpose

The **Web Push** channel delivers **browser push notifications** to the merchant's storefront visitors — short, tappable alerts that pop up on a customer's desktop or mobile browser even when the customer isn't on the merchant's site. Used in campaigns (flash sales, re-engagement, and automated campaigns on segments such as an abandoned cart or a product back in stock) and for order-status updates through its system messages. The built-in **Abandoned cart reminder** itself sends only by email or Messenger ([[abandoned-cart-channels]]).

Web Push works without an email address or phone number. The customer's "subscription identifier" is a per-device push endpoint URL (issued by their browser's push service — Mozilla Autopush, Google FCM, Apple WebPush gateway) plus a pair of cryptographic keys (`p256dh` + `auth`) the browser generated when the customer accepted the permission prompt.

Push delivery itself is done by the browser vendors' push services. Sends are metered against the plan's `campaign.channel.web_push` allowance like any channel ([[marketing-channels-cross-plan-caps]]); the allowance per plan and any price for installing the channel are in the billing catalogue (verify).

## Where to find it

Sidebar → **Marketing** → **Channels** → **Channels setup** (route `campaigns-channels`, `/admin/marketing/campaigns/channels`) → find the **Web Push** channel card. The card's actions (Install, Activate/Deactivate, Settings, System Message, Usage, Logs) open modals over the channels page — Web Push settings render in the `MarketingChannelsSettingsModalWebPush` sub-component.

Channel mapping key: `web_push`. Actions hit the channels API (base `/admin/api/core/marketing/campaigns/channels`): status via `POST /{type}/status`, usage via `GET /{type}/usage`, logs via `/{mapping}/logs-list`, settings via `/{type}/settings`. Install / uninstall is handled through the applications API (`/admin/api/core/applications`). The storefront subscribe endpoint is `POST /web-push-subscribe` (route `campaigns.channels.channel.web_push.subscribe`).

The channel is **not installed by default**.

## Sub-pages (in this cluster)

This feature is split into 7 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[webpush-channel-storefront-prompt]] — the **Settings - Web Push** modal; two-stage prompt design (CloudCart popup → native browser prompt); `checkout`, `popup_status`, `popup_text`, `popup_ok_button`, `popup_discard_button`, `popup_image`, `message`, `cookie_life_time`.
- [[webpush-channel-subscription-flow]] — `/web-push-subscribe` endpoint; `endpoint` + `p256dh` + `auth` keys; subscriber + WebPush channel row creation; `_cc_wp` cookie; implicit Email-channel link for logged-in customers; geo-IP + User-Agent capture.
- [[webpush-channel-send-pipeline]] — message validation (`max:63` / `max:128`); per-recipient pre-flight checks; restricted merge tags (only 3); queued send job with 5× retry + 2-second backoff; HTTP send-request shape; push-service status mapping.
- [[webpush-channel-dlr-webhook]] — delivery-report webhook (`dlrUrl`); `message_hash` + `status` validation; status mapping (`DELIVERED` / `CLICKED` / `PENDING`); admin-click filter; expired → unsubscribed.
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

### Allowed merge tags

| Tag | Aspect page |
|---|---|
| `{$subscriber_first_name}` | [[webpush-channel-send-pipeline]] |
| `{$subscriber_last_name}` | [[webpush-channel-send-pipeline]] |
| `{$shop_name}` | [[webpush-channel-send-pipeline]] |

### Plan-gate key

| Key | Notes |
|---|---|
| `campaign.channel.web_push` | Send-count cap; values per plan in the billing catalogue (verify). At the cap the channel is switched off. |

## Business rules

The deep mechanics live on each aspect page; what every merchant must know at this level:

- **Single platform VAPID key pair signs every storefront.** Merchants don't bring or generate VAPID keys.
- **`verified = 1` is implicit — no double opt-in.** Unlike Email / SMS / Viber, accepting the native browser permission prompt IS the verification gate. No `unconfirmed_send` switch. See [[webpush-channel-subscription-flow]].
- **Two-stage prompt design.** The CloudCart pre-prompt popup fires first; only customers who click Allow ever see the native browser prompt. Preserves the merchant's ability to re-prompt (the native prompt is one-shot per user). See [[webpush-channel-storefront-prompt]].
- **Only 3 merge tags allowed.** `{$subscriber_first_name}`, `{$subscriber_last_name}`, `{$shop_name}`. The 128-char body limit makes longer dynamic content impractical. See [[webpush-channel-send-pipeline]].
- **Conditional branching: `link_clicked` only.** No `message_read` — push services don't reliably report displayed. See [[webpush-channel-send-pipeline]].
- **Expired subscription → unsubscribed.** The subscriber's WebPush channel is marked unsubscribed until the customer subscribes again. See [[webpush-channel-send-pipeline]].
- **No catalogue triggers.** No campaign starts on a product being added or a price falling: automated campaigns start only when a subscriber gets into or out of a segment ([[campaigns-edit-step-2-trigger]]). New products are announced with a Regular campaign.
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
