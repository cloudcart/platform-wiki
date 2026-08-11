---
type: feature
nav_path: "Marketing → Channels → Channels setup → SMS Msg Hub"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["SMS Msg Hub", "SMS MsgHub", "SMS Link Mobility", "MsgHub", "SMS канал MsgHub", "SMS чрез MsgHub"]
tags: [marketing, channels, sms, msghub, link-mobility]
plan_gates: ["campaign.channel.sms_msghub_message"]
created: 2026-05-23
updated: 2026-06-10
source_count: 7
---
# SMS channel (Msg Hub)

## Purpose

The **SMS Msg Hub** channel delivers SMS text messages to the merchant's subscribers via the **Link Mobility / MsgHub Bulgaria** SMS aggregator (api.msghub.cloud). It's one of the two SMS providers CloudCart supports for marketing campaigns (the other is [[marketing-channels-sms-nth|NTH Mobile]]) — chosen by merchants who need time-sensitive promotional blasts, order-status SMS alerts, or Bulgaria-focused communication with strong DLR (delivery report) coverage.

The channel is **shared infrastructure**: every CloudCart merchant using SMS MsgHub sends from the same Link Mobility sub-account (`api_key` + `api_secret` provisioned at the platform level), under CloudCart's contract terms. The merchant doesn't enter their own credentials; CloudCart bills the merchant via the plan-cap on `campaign.channel.sms_msghub_message`.

This page is the **hub** for the SMS MsgHub cluster. It gives the orientation; each aspect below documents one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

## Sub-pages (in this cluster)

- [[sms-msghub-overview]] — install / activate / uninstall, the channel-card UI surface matrix (what modals exist and what's deliberately absent), and the MsgHub-vs-NTH decision.
- [[sms-msghub-send-pipeline]] — the synchronous-send distinguishing trait, HTTP-code status mapping (200=SENT / 202=DELIVERED / 4xx-5xx=ERROR), per-subscriber pre-flight checks, plan-cap pre-flight auto-deactivate, internal-title format.
- [[sms-msghub-settings]] — platform-level config (`id`, `sc`, bcrypt-hashed `api_key`/`api_secret`, sandbox/production URLs), the `/send` request shape + HMAC signing, per-merchant `installed`/`active`/`sandbox` settings, sandbox testing.
- [[sms-msghub-length-billing]] — 160/70-char GSM-7/UCS-2 limits, multi-part concatenation, the campaign-editor character counter, the cost model + plan-cap exhaustion → Buy-more-credits.
- [[sms-msghub-dlr-webhook]] — DLR delivery-report webhook handling (requires `sms_id` + `service_id`; routes by log-row lookup not `site_id` param), the Viber-service clarification, and the anti-spam policy gate.

## Where to find it

Sidebar → **Marketing** → **Channels** → **Channels setup** (route `campaigns-channels`, `/admin/marketing-new/campaigns/channels`) → find the **SMS Msg Hub** channel card. The card exposes its actions (Install, Activate/Deactivate toggle, Usage, Logs) inline — they open modals over the channels page rather than navigating to separate routes. The channel is **not installed by default**; the merchant clicks **Install** (one-click — no domain or credentials to set up). See [[sms-msghub-overview]] for the full card UI surface.

## What the merchant can do here

- **Install / Uninstall** the channel (must accept the [[marketing-campaigns-policy|anti-spam policy]] first) — see [[sms-msghub-overview]].
- **Activate / Deactivate** with the inline toggle.
- **View Usage** — SMS sent this billing cycle vs the plan cap — see [[sms-msghub-length-billing]].
- **View Logs** — per-message delivery status (SENT / DELIVERED / SEEN / ERROR / NOT_SENT) with destination, body, send time, and MsgHub `sms_id` for support traces.
- **Use this channel in a campaign step** — add an action of type **"SMS (msghub)"** (`sms_msghub_message`) when building a [[marketing-campaigns|Campaign]]. The editor offers a single text body (no rich content / images / buttons) with character-count and standard placeholders.

No per-merchant credentials are configurable from the UI — the platform's MsgHub contract is shared.

## Settings & fields

The MsgHub card surfaces the **bare minimum** — no Configuration wizard, no Settings modal, no System Messages list. Platform-level config (`id`, `sc`, credentials, endpoints) is set globally on CloudCart's behalf; per-merchant settings are limited to `installed` / `active` / sandbox toggles. The full field-level breakdown lives on [[sms-msghub-settings]]; the UI-surface matrix (which modals appear / are absent) lives on [[sms-msghub-overview]].

## Business rules

The detail behind each rule is on its aspect page:

- **Synchronous send** — MsgHub is the only marketing channel that POSTs to the provider inside the campaign-action thread; every other channel queues a job. See [[sms-msghub-send-pipeline]].
- **Per-subscriber pre-flight** — phone present, `unsubscribed=0`, `marketing=1`, `verified=1`, `bounced=0`. See [[sms-msghub-send-pipeline]].
- **Message length / billing** — billed per SMS part; Cyrillic UCS-2 messages rack up parts fast. See [[sms-msghub-length-billing]].
- **DLR webhook** is the source of truth for actual carrier delivery. See [[sms-msghub-dlr-webhook]].
- **Anti-spam policy gate** before install; SMS is heavily regulated and the merchant carries full liability. See [[sms-msghub-dlr-webhook]].

## Related

- [[marketing-channels]] — parent hub (all marketing channels).
- [[marketing-campaigns]] — campaigns use this channel for SMS delivery steps.
- [[marketing-channels-sms-nth]] — alternative SMS provider (shares the Phone subscriber-channel group).
- [[marketing-channels-viber]] — Viber Business Messages (also shares the Phone group).
- [[marketing-subscribers]] — subscribers' phone numbers live on the `Phone` SubscriberChannel row.
- [[marketing-campaigns-policy]] — anti-spam policy required before installation.
- [[notification-delivery]] — outbound delivery concept page.
- [[channel]] — Channel entity reference.

## Open questions

No outstanding questions.
