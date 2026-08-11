---
type: feature
nav_path: "Marketing → Channels → Channels setup"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["Channels", "Channels setup", "Communication channels", "Marketing channels", "Channel configuration", "Канали", "Настройка на канали", "Комуникационни канали"]
tags: [marketing, channels, campaigns, setup, integrations]
plan_gates: ["campaign.channel.email", "campaign.channel.sms_msghub_message", "campaign.channel.sms_nth_message", "campaign.channel.web_push", "viber_messages"]
created: 2026-05-23
updated: 2026-06-10
source_count: 9
---

# Channels setup

## Purpose

The **Channels setup** screen is the merchant's hub for every outbound message delivery pipe the store can use to reach its subscribers and customers: **Email**, **SMS (MsgHub)**, **SMS (NTH Message)**, **Viber Business Messages**, and **Browser Web Push**. Each channel is an installable + configurable + activatable unit — once installed and active, it shows up as an available send-medium when building a [[marketing-campaigns|campaign]] step (and for some channels, as a transactional pipe used by [[marketing-omnichannel-mails-list|Email notifications]] too).

The channel mapping keys (`email`, `sms_msghub_message`, `sms_nth_message`, `viber_message`, `web_push`) are the verbatim keys used across campaign actions, [[marketing-subscribers#Channels - Email, Phone, Messenger, WebPush|SubscriberChannel]] rows, routes, logs, and the plan-feature gating layer. See [[marketing-channels-cross-catalog]] for the full mapping table.

## Where to find it

Sidebar → **Marketing** → **Channels** (dropdown) → **Channels setup**. The route is `/admin/marketing-new/campaigns/channels`.

A `beforeEnter` guard requires the merchant to have accepted the [[marketing-campaigns-policy|anti-spam policy]] first — if `campaigns.anti_spam_policy_accepted` is falsy, the merchant is redirected to `/admin/marketing-new/campaigns/policy` before they ever see the channels page. See [[marketing-channels-cross-sandbox]] for the gate.

A second entry, **Email notifications**, sits beside this one under the same Channels dropdown and routes to the transactional Email notifications list at [[marketing-omnichannel-mails-list]] — those are per-event customer emails (order confirmation, welcome, etc.) and are not configured here.

## Sub-pages (in this cluster)

This feature is split into 7 cross-cutting aspect pages. Each aspect covers one well-scoped slice of the page's behaviour — the Assistant should drill into the aspect that matches the question, not read the whole cluster.

- [[marketing-channels-cross-catalog]] — the five channels with their `mapping` keys, providers, plan-feature keys, per-channel state fields, and sender-identity semantics per channel.
- [[marketing-channels-cross-lifecycle]] — dormant → installed → configured → active → suspended lifecycle, Install / Uninstall / Activate / Deactivate operations, and the deactivation cascade that auto-stops dependent campaigns.
- [[marketing-channels-cross-suspension]] — the four auto-suspend triggers (`spam`, `bounced`, `open`, `cc_denied`), default thresholds, the under-500-sends + 99%-reputation bootstrap exemption, and the `manual_allowed_suspended` / `manual_denied_suspended` override mechanism.
- [[marketing-channels-cross-plan-caps]] — per-channel plan caps, the 80% usage-alert notification, the Buy-more-credits feature-pack flow, and the Viber-only self-credentials override that bypasses CloudCart metering.
- [[marketing-channels-cross-sandbox]] — per-channel Sandbox URL redirect for testing without spending credits, the anti-spam policy gate, and the per-campaign pre-flight checks ("channel not configured / not active / out of credits").
- [[marketing-channels-cross-magic-vars]] — universal template variables (`{$unsubscribe_url}`, `{$cart_url}`, `{$checkout_url}`, `{$triggered_products:N}`), auto-verification on engagement, HARD_BOUNCED categorisation rules, and the subscriber-removal-on-fail cascade.
- [[marketing-channels-cross-ui-surfaces]] — the four-band card layout (Header / Actions / Restrictions / Sandbox), the seven overlay modals the page mounts, the deactivation confirmation dialog, and the lazy-load pattern for per-card usage stats.

## What the merchant can do here

- See the **list of all five channels** in card form with name, status, action buttons (Configure / Settings / Reputation / Usage / Logs / Install / Uninstall).
- **Install** / **Uninstall** a channel — see [[marketing-channels-cross-lifecycle]].
- **Activate / Deactivate** an installed channel with the inline toggle — see [[marketing-channels-cross-lifecycle]] for the deactivation cascade.
- **Configure** Email through the multi-step DKIM-verify flow — see [[marketing-channels-email]].
- **Edit Settings** per channel — Email / Viber / Web Push expose per-channel settings; Viber additionally exposes self-credentials ([[marketing-channels-cross-plan-caps]]).
- **View Reputation** (Email only) — [[marketing-channels-reputation]].
- **View Usage** per channel — [[marketing-channels-usage]].
- **View Logs** per channel — [[marketing-channels-logs]].
- **Edit System messages** for Viber and Web Push — [[marketing-channels-system-messages]].
- **Configure Sandbox** mode for testing without spending credits — see [[marketing-channels-cross-sandbox]].

## Settings & fields

This is a hub page. Per-channel settings (sender domain, credentials, system message templates, sandbox URL, VAPID keys, etc.) live on the channel-specific pages — see [[marketing-channels-email]], [[marketing-channels-viber]], [[marketing-channels-webpush]], [[marketing-channels-sms-msghub]], [[marketing-channels-sms-nth]]. Cross-cutting fields shared by all five channels (state values, mapping keys, sender identity table) are catalogued in [[marketing-channels-cross-catalog]].

## Business rules

This is a hub page. The cross-cutting business rules — lifecycle transitions, auto-suspension thresholds, plan-cap accounting, sandbox redirection, anti-spam policy gate, template-variable rendering, subscriber-removal cascades, and UI-surface quirks — are documented on the seven cross-cutting aspect pages listed above. Per-channel-specific rules live on the channel pages.

## Programmatic access

Channel-provider configuration (Elastic Email profile + domain DNS, MsgHub / NTH credentials, Viber sender ID, Web Push VAPID + popup text) is **admin-panel-only** — there is no JSON-API v2 resource for per-channel provider settings, reputation reads, usage counters, or system-message templates.

What IS exposed programmatically is the **per-subscriber channel row** (`SubscriberChannel`) via [[api-subscribers-channels]] — the row carrying `channel` (Email / Phone / WebPush / Messenger), `channel_identifier`, `marketing` (per-channel consent), `verified`, `unsubscribed`, and `bounced`. Integrations use this to bulk-add Email / Phone channels to existing subscribers, flip `marketing` per channel without touching the subscriber-level flag, or sync `unsubscribed` / `bounced` state from an external ESP. Side effects (segment-membership re-evaluation, uniqueness validation, phone E.164 normalisation, subscriber `updated` webhook) match the UI path — see [[marketing-channels-cross-magic-vars]] for the two-layer consent check that gates sends, and [[json-api-v2]] for auth and rate limits.

## Related

- [[marketing]] — parent hub.
- [[marketing-campaigns]] — campaigns use these channels as the delivery medium for each step.
- [[marketing-campaigns-policy]] — anti-spam policy gate that must be accepted before configuring any channel.
- [[marketing-channels-email]] — Email channel configuration (Elastic Email).
- [[marketing-channels-sms-msghub]] — SMS via MsgHub (Link Mobility).
- [[marketing-channels-sms-nth]] — SMS via NTH Mobile.
- [[marketing-channels-viber]] — Viber Business Messages.
- [[marketing-channels-webpush]] — Browser WebPush notifications.
- [[marketing-channels-logs]] — per-channel logs deep-dive.
- [[marketing-channels-usage]] — per-channel usage modal deep-dive.
- [[marketing-channels-reputation]] — Email reputation modal deep-dive.
- [[marketing-channels-system-messages]] — Viber / Web Push system message editor.
- [[marketing-subscribers]] — subscribers carry per-channel `SubscriberChannel` rows whose `marketing` / `verified` / `bounced` / `unsubscribed` flags gate per-channel sending.
- [[marketing-omnichannel-mails-list]] — transactional email notifications (separate from these promotional channels — uses the same Email channel for delivery).
- [[apps-smtp]] — alternative SMTP integration (when the merchant prefers to deliver via their own SMTP server instead of Elastic Email).
- [[notification-delivery]] — concept page on platform-wide outbound message routing.
- [[channel]] — Channel entity reference.
- [[plan-gates]] — `campaign.channel.*` and `viber_messages` plan-feature keys.

## Open questions

None — all previously-flagged items distributed to sub-pages.
