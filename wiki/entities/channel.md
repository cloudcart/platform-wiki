---
type: entity
aliases: ["Marketing channel", "Communication channel", "Campaign channel", "Channel", "Канал", "Маркетингов канал", "Комуникационен канал"]
tags: [marketing, channels]
created: 2026-05-21
updated: 2026-05-23
source_count: 0
---
# Marketing Channel

## Identity

A **Marketing Channel** is a configured outbound message-delivery pipe that the merchant uses to reach their subscribers and customers: **Email** (newsletters, promo blasts, transactional confirmations), **SMS** via either MsgHub or NTH Mobile (time-sensitive offers, OTPs, order alerts), **Viber** Business Messages (rich text/image marketing on Viber), or **Web Push** (browser-native notifications via VAPID). Each channel ties a delivery provider (Elastic Email, Link Mobility, NTH, InfoBip, the customer's browser push service) to the merchant's store as a per-store installable, configurable, activatable unit — and exposes itself to [[marketing-campaigns|Campaigns]] as a step-action type. A campaign's step picks one channel; a subscriber needs a matching [[subscriber|SubscriberChannel]] row (Email address, phone number, Viber-capable phone, or WebPush endpoint) to be reachable; the per-channel plan-cap, sender configuration, and auto-suspend triggers determine how that delivery actually goes out.

## Aliases

- "Marketing channel" — typical merchant-facing term in the UI and docs.
- "Communication channel" — used in some help text (especially for Viber).
- "Campaign channel" — used in the routes (`campaigns.channels.*`) and the backend model class name (`CampaignChannels`).
- Bulgarian: "Канал" / "Маркетингов канал" / "Комуникационен канал".

## Key Attributes

| Attribute | What the merchant controls | Notes |
|-----------|----------------------------|-------|
| `mapping` | n/a (system-defined) | Stable identifier used in campaign action types, routes, log records. One of: `email`, `sms_msghub_message`, `sms_nth_message`, `viber_message`, `web_push` (plus disabled rows: `messenger_message`, `voice`). |
| `name` | n/a (system-translated) | Translatable merchant-facing name (`Email`, `SMS Msg Hub`, `SMS`, `Viber`, `Web Push`). |
| `group` | n/a | Bucket key: `email` / `phone` / `web_push`. Subscriber's `SubscriberChannel.channel` matches the channel manager's group. |
| `status` | n/a (platform-level) | Catalog-level status (1 = enabled, 0 = hidden). Disabled channels (`messenger_message`, `voice`) are still in the DB but not shown to merchants. |
| `installed` | Merchant clicks Install | Per-store setting indicating provider credentials are set up. Required before activation. |
| `active` | Merchant toggles on/off | Per-store. When OFF, campaigns using this channel auto-deactivate cascade. |
| `configured` | Multi-step setup (Email only) | Per-store. Email needs profile + verified domain + sender email; only then `configured = true`. |
| `verify` | DNS records validated (Email only) | Per-store. SPF + DKIM + Tracking CNAME + DMARC all valid. |
| `suspended_by` | Auto-set by platform | Per-store. Array of `{key: spam/bounced/open/cc_denied, value: threshold}` when reputation triggers auto-suspension. |
| `sandbox_status` / `sandbox_url` | Merchant toggle | Per-store. Redirects sends to inspection webhook for testing. |
| `unconfirmed_send` | Merchant toggle (Email only) | When TRUE, Email sends to subscribers whose channel is `verified = 0`. |
| `self_credentials_active` | Merchant toggle (Viber only) | When TRUE, Viber sends use the merchant's own InfoBip credentials (vs the CloudCart-shared sender). |
| Sender ID | Channel-specific | Email: verified domain mailbox; SMS MsgHub: "CloudCart" via Link Mobility; SMS NTH: "CloudCart" via NTH; Viber: "CloudCart" (default) or merchant's own; Web Push: storefront origin URL. |
| Plan-feature key | n/a (channel-specific) | `campaign.channel.email`, `campaign.channel.sms_msghub_message`, `campaign.channel.sms_nth_message`, `campaign.channel.web_push`, and `viber_messages` for Viber (uses the dedicated the platform code). |
| Subscriber channel mapping | n/a (channel-specific) | Email → the platform code; the two SMS + Viber → the platform code; Web Push → the platform code. |
| Auto-suspend thresholds | n/a (constants per-channel) | Email: `SUSPENDED_SPAM = 0.5`, `SUSPENDED_BOUNCED = 5`, `SUSPENDED_OPEN = 5`; abstract `SUSPENDED_COUNT_LIMIT = 500` (min sends before suspension can fire). |
| Message length cap | n/a (constants per-channel) | Email: no hard cap (sender's HTML); SMS: provider-side (160 GSM-7 / 70 UCS-2 per part); Viber: `MAX_MESSAGE_LENGTH = 1000`; Web Push: title ≤ 63, body ≤ 128. |

## Where it appears

- [[marketing-channels]] — main Channels setup hub.
- [[marketing-channels-email]] — Email channel page (Elastic Email).
- [[marketing-channels-sms-msghub]] — SMS via Link Mobility / MsgHub.
- [[marketing-channels-sms-nth]] — SMS via NTH Mobile.
- [[marketing-channels-viber]] — Viber Business Messages (InfoBip).
- [[marketing-channels-webpush]] — Browser WebPush (VAPID).
- [[marketing-campaigns]] — campaigns pick a channel per step; channel deactivation cascades to campaigns.
- [[marketing-campaigns-policy]] — anti-spam policy gate that must be accepted before any channel setup.
- [[marketing-subscribers]] — every subscriber has zero-to-many `SubscriberChannel` rows, one per channel they're reachable on.
- [[marketing-omnichannel-mails-list]] — transactional Email notifications use the Email channel for delivery; Viber and Web Push system messages cover the same role on those channels.

## Related

- [[campaign]] — Campaign entity (uses channels as delivery medium).
- [[subscriber]] — Subscriber entity (linked to channels via SubscriberChannel rows).
- [[email-template]] — Email channel template entity.
- [[plan-gates]] — `campaign.channel.*` and `viber_messages` plan-feature keys gate per-channel send volume.
- [[notification-delivery]] — concept page on platform-wide outbound delivery mechanisms.
- [[settings-hooks]] — `subscriber.*` webhook events fire on channel-driven subscribe / unsubscribe state changes.
- [[apps-smtp]] — alternative SMTP integration for Email.
- [[discount-stacking]] — unrelated (legacy stub link).

## Open Questions

- ⏸️ The exact list of channel-level events that fire `subscriber.*` webhooks — the Email channel fires unsubscribe webhooks; whether SMS / Viber / Web Push unsubscribes do the same is uncertain.
- ⏸️ The precise cascade when the merchant uninstalls a channel that's been actively used by campaigns — whether log data is preserved, whether existing in-flight campaign actions complete, etc.
- ⏸️ Whether the auto-suspend thresholds (`SUSPENDED_SPAM`, `SUSPENDED_BOUNCED`, `SUSPENDED_OPEN`) apply uniformly to all channels or only to Email, since only Email actively reports reputation back to the platform.
