---
type: feature
nav_path: "Marketing → Channels → Channels setup → Viber"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["Viber", "Viber Business Messages", "Viber channel", "Viber for Business", "Вайбър канал", "Viber съобщения"]
tags: [marketing, channels, viber, infobip, business-messages]
plan_gates: ["viber_messages"]
created: 2026-05-23
updated: 2026-06-10
source_count: 10
---

# Viber channel

## Purpose

The **Viber** channel delivers **Viber Business Messages** (transactional or promotional rich-text / image messages) through InfoBip's Viber Business gateway. It targets the Bulgarian and Balkan markets where Viber penetration on smartphones is very high — Viber complements (or replaces) SMS for time-sensitive marketing and order notifications.

What makes Viber distinctive in the CloudCart channel catalog:

- The sender shows as a **verified business** (green checkmark) — recipient trust is higher than for an SMS short code.
- The message can carry an **image** + an **action button** in addition to up to 1000 characters of text — closer to an in-app push card than an SMS.
- It is the **only marketing channel that supports merchant-supplied credentials** (Self-credentials path) `(verify)`.
- It is one of only two channels (with Email) whose DLR exposes a `SEEN` status — enabling `message_read` / `message_not_read` campaign-step branching.
- It uses a **dedicated plan-feature key** `viber_messages` instead of the generic `campaign.channel.{mapping}` pattern.

Because Viber Business is a paid channel both for CloudCart (InfoBip charges per delivered message) and for the merchant, plan-cap accounting, pricing, and promo-vs-service routing are all Viber-specific behaviours — covered across the aspect pages below.

## Where to find it

Sidebar → **Marketing** → **Channels** → **Channels setup** (route `campaigns-channels`, `/admin/marketing-new/campaigns/channels`) → **Viber** card. The card's actions (Install, Activate/Deactivate, Settings, System Message, Usage, Logs) open modals over the channels page — Viber settings render in the `MarketingChannelsSettingsModalViber` sub-component.

Channel mapping key: `viber_message`. Actions hit the channels API (base `/admin/api/core/marketing/campaigns/channels`):

- Status: `POST /{type}/status`
- Usage: `GET /{type}/usage`
- Logs: `/{mapping}/logs-list`
- Settings: `/{type}/settings`
- System-message status: `/viber-message/system-messages/{key}/status`
- Install / uninstall: via the applications API (`/admin/api/core/applications`).

The channel is **not installed by default**. The merchant clicks **Install** to activate it for the store.

## What the merchant can do here

- **Install** the channel — adds Viber to the configured channels list.
- **Activate / Deactivate** after install.
- **Settings** — edit the Viber sender name (when permitted) and configure Self-credentials (advanced).
- **System messages** — manage 7 per-event Viber templates (order placed, order shipped, etc.).
- **View Usage** — sent-count vs the `viber_messages` plan cap.
- **View Logs** — per-message delivery status with content preview.
- **Use this channel in a campaign step** — action type **"Viber message"** (`viber_message`).

## Sub-pages (in this cluster)

This channel is documented across 7 aspect pages — drill into the aspect that matches the question instead of reading every page.

- [[viber-channel-settings]] — the Settings modal: dual-shape `regular.*` vs `self_credentials.*` payload; `different_sender`, `allow_self_credentials`, `allow_promo_messages`, `settings_type` flags; sender-name override.
- [[viber-channel-self-credentials]] — merchant-supplied InfoBip credentials; scenario provisioning via `createScenario`; audit-row to `application_history`; plan-cap bypass; promo-routing force-disabled.
- [[viber-channel-send-pipeline]] — queued dispatch with 5× retry / 2-second backoff; double-checked 1000-char `MAX_MESSAGE_LENGTH`; automatic service-vs-promo credential routing; `bulkId = {site_id}_{microtime}` for per-store DLR reconciliation; 5-second InfoBip API timeouts.
- [[viber-channel-dlr-status]] — DLR webhook (`/web-hook/viber-message?site_id=...`); InfoBip-to-CloudCart status mapping table (`DELIVERED → SENT`, `SEEN → SEEN`, etc.); cascade-to-prior-pending behaviour; `message_read` / `message_not_read` conditional branching.
- [[viber-channel-system-messages]] — 7 per-event templates (`customer_create`, `customer_forgot_password`, `cash_on_delivery`, `bank_wire_transfer`, `credit_card`, `order_status_change`, `order_status_fulfillment_change`); Viber-specific editor with Image + Button cards when `allow_promo_messages = true`; per-language fallback; per-template `sent_count`.
- [[viber-channel-plan-cap]] — dedicated `viber_messages` plan-feature key (not `campaign.channel.viber_message`); `viber_messages_subscription` gate for `different_sender`; internal pricing units (`prices.viber = 50` vs `prices.mobile = 10`); `'global.unlimited'` return for Self-credentials.
- [[viber-channel-message-format]] — InfoBip `omni/1/advanced` send-request JSON shape; verified-business badge requirements; customer-side OTT requirements; per-subscriber Phone-channel pre-flight (`unsubscribed=0`, `marketing=1`, `verified=1`, `bounced=0`); E.164 normalisation; no automatic SMS fallback.

## Settings & fields

The Viber card surfaces three top-level fields the merchant configures:

| Where | Field | Default | What it does |
|-------|-------|---------|--------------|
| Settings modal — Branch A | `regular.different_sender` | `false` | Premium sender via CloudCart's InfoBip account. See [[viber-channel-settings]]. |
| Settings modal — Branch A | `regular.from` | `"CloudCart"` | Viber Business sender name shown to the recipient. |
| Settings modal — Branch B | `self_credentials.*` (host / username / password / from / active) | n/a | Merchant's own InfoBip contract. See [[viber-channel-self-credentials]]. |

The detailed field documentation lives on the per-aspect pages — this hub catalogues the **navigation** to each surface, not the field minutiae.

## Business rules

The cross-cutting rules — split across aspects:

- **Plan-feature key is dedicated.** Viber uses `viber_messages`, not `campaign.channel.viber_message`. See [[viber-channel-plan-cap]].
- **Service-vs-Promo routing is automatic.** Adding an image or button flips the send to promo credentials. See [[viber-channel-send-pipeline]].
- **`SEEN` status enables branching.** Viber + Email are the only channels with `message_read` conditions. See [[viber-channel-dlr-status]].
- **Self-credentials bypass the plan cap.** Returns `'global.unlimited'`. See [[viber-channel-self-credentials]].
- **No automatic SMS fallback.** The merchant must explicitly chain a fallback step. See [[viber-channel-message-format]].
- **System messages have per-template counters.** Incremented on `DELIVERED` / `SENT` / `SEEN` / `CLICKED` DLR events. See [[viber-channel-system-messages]].

## Related

- [[marketing-channels]] — parent hub.
- [[marketing-campaigns]] — campaigns use this channel for Viber delivery steps.
- [[marketing-channels-sms-msghub]] — SMS via MsgHub (Phone subscriber-channel group; shares the same per-subscriber pre-flight rules).
- [[marketing-channels-sms-nth]] — SMS via NTH (Phone subscriber-channel group).
- [[marketing-subscribers]] — phone numbers live on the Phone SubscriberChannel row.
- [[marketing-campaigns-policy]] — anti-spam policy required before installation.
- [[marketing-omnichannel-mails-list]] — transactional notifications (some events have Viber system-message templates).
- [[notification-delivery]] — outbound delivery concept page.
- [[channel]] — Channel entity reference.
- [[plan-gates]] — cross-cutting plan-feature-key reference; `viber_messages` + `viber_messages_subscription`.
- [[marketing-channels-system-messages]] — cross-channel system-messages hub.
- [[marketing-channels-logs]] — cross-channel logs surface.
- [[marketing-channels-usage]] — cross-channel usage surface.

## Open questions

No outstanding questions on the hub itself — aspect-specific verifications are tracked on the per-aspect `## Open questions` sections.
