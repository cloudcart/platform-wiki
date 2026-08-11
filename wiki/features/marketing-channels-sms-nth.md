---
type: feature
nav_path: "Marketing → Channels → Channels setup → SMS"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["SMS NTH", "SMS NTH Mobile", "SMS channel NTH", "NTH SMS", "SMS канал NTH", "SMS чрез NTH"]
tags: [marketing, channels, sms, nth, nth-mobile]
plan_gates: ["campaign.channel.sms_nth_message"]
created: 2026-05-23
updated: 2026-06-10
source_count: 7
---
# SMS channel (NTH)

## Purpose

The **SMS NTH** channel delivers SMS text messages via **NTH Mobile** (nth-mobile.com), an SMS aggregator with a Bulgarian point-of-presence and an omni-channel REST API at `developers.nth.ch`. It's one of the two SMS providers CloudCart supports for marketing campaigns — listed alongside [[marketing-channels-sms-msghub|SMS Msg Hub]]. Merchants pick NTH for the same use cases as MsgHub (promotional blasts, abandoned-cart recovery, order alerts, OTPs) but with a different upstream provider — useful as a failover option or when the merchant's SMS-spending economics favour NTH's pricing.

Like MsgHub, this is a **shared CloudCart infrastructure channel**: every CloudCart merchant using SMS NTH sends from the same NTH sub-account (`SMSNTH_USERNAME` / `SMSNTH_PASSWORD` provisioned at the platform level), using the **"CloudCart"** alphanumeric sender ID, under the CloudCart contract terms. The merchant doesn't enter their own credentials; CloudCart bills the merchant via the plan-cap on `campaign.channel.sms_nth_message`.

In the merchant-facing UI, this channel appears simply as **"SMS"** (its DB row `name` is "SMS") — the "NTH" qualifier is only visible in the campaign-step action picker, where the merchant must choose between `sms_nth_message` and `sms_msghub_message` if both channels are installed.

This page is the **hub** for the SMS NTH cluster. It gives the orientation; each aspect below documents one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

## Sub-pages (in this cluster)

- [[sms-nth-overview]] — install / activate / uninstall lifecycle, the channel-card UI surface matrix (which modals exist and which are deliberately absent), where the merchant edits NTH SMS content, and the MsgHub-vs-NTH decision table.
- [[sms-nth-send-pipeline]] — the job-queued (asynchronous) dispatch distinguishing trait, the 5x-retry / 2-second-backoff wrapper, per-subscriber pre-flight checks, the in-worker plan-cap pre-flight auto-deactivate, internal-title format, and phone-number normalisation.
- [[sms-nth-settings]] — platform-level config (the platform code, env-driven host/port/credentials, hard-coded sender), the `/v1/omni-channel/message` request shape + HTTP Basic Auth, per-merchant `installed`/`active`/`sandbox` settings, message validation rules, sandbox testing.
- [[sms-nth-length-billing]] — 160/70-char GSM-7/UCS-2 segment limits, multi-part concatenation handled NTH-side, the campaign-editor character + SMS-part counter, the cost model + plan-cap exhaustion → Buy-more-credits, the `usage_alert` 80% threshold.
- [[sms-nth-dlr-webhook]] — the DLR delivery-report webhook (requires `messageId` + nested `status.code`), NTH's rich status vocabulary → CloudCart status mapping (including pass-through of unknown values), and the anti-spam policy gate.

## Where to find it

Sidebar → **Marketing** → **Channels** → **Channels setup** (route `campaigns-channels`, `/admin/marketing-new/campaigns/channels`) → find the **SMS** channel card. The card exposes its actions (Install, Activate/Deactivate, Usage, Logs) inline — they open modals over the channels page rather than navigating to separate routes. The channel is **not installed by default**; the merchant clicks **Install** (one-click — no domain, DNS, or credentials to set up). See [[sms-nth-overview]] for the full card UI surface.

Channel mapping key: `sms_nth_message`. Actions hit the channels API (base `/admin/api/core/marketing/campaigns/channels`): status via `POST /{type}/status`, usage via `GET /{type}/usage`, logs via `/{mapping}/logs-list`, settings via `/{type}/settings`. Install/uninstall is handled through the applications API (`/admin/api/core/applications`).

## What the merchant can do here

- **Install / Uninstall** the channel (must accept the [[marketing-campaigns-policy|anti-spam policy]] first) — see [[sms-nth-overview]].
- **Activate / Deactivate** the channel after install.
- **View Usage** — SMS sent this billing cycle vs the plan cap — see [[sms-nth-length-billing]].
- **View Logs** — per-message delivery status with destination phone number, message text, NTH-side status code, send time, and DLR-status updates — see [[sms-nth-dlr-webhook]].
- **Use this channel in a campaign step** — add an action of type **"SMS (NTH Message)"** (`sms_nth_message`) when building a [[marketing-campaigns|Campaign]]. The editor offers a single text body (no rich content / images / buttons), an Internal title (required, max 191 chars), and standard placeholders (`{$customer_first_name}`, `{$shop_name}`, `{$order_id}`, etc.).
- **Send a demo message** to a test number from the campaign editor before launching.

No per-merchant credentials are configurable from the UI — the platform's NTH contract is shared.

## Settings & fields

The NTH card surfaces the **bare minimum** — no Configuration wizard, no Settings modal, no System Messages list. Platform-level config (host, port, credentials, hard-coded "CloudCart" sender) is set globally on CloudCart's behalf; per-merchant settings are limited to `installed` / `active` / sandbox toggles. The full field-level breakdown — including the `/v1/omni-channel/message` request shape and HTTP Basic Auth — lives on [[sms-nth-settings]]; the UI-surface matrix (which modals appear / are absent) lives on [[sms-nth-overview]].

## Business rules

The detail behind each rule is on its aspect page:

- **Job-queued (asynchronous) send** — unlike MsgHub (synchronous inline), NTH dispatches a send job to the campaigns queue with a 5x-retry / 2-second-backoff wrapper, so a slow NTH response never stalls the campaign engine. See [[sms-nth-send-pipeline]].
- **Per-subscriber pre-flight** — phone present, `unsubscribed=0`, `marketing=1`, `verified=1`, `bounced=0`. See [[sms-nth-send-pipeline]].
- **Message length / billing** — billed per SMS part; Cyrillic UCS-2 messages rack up parts fast. See [[sms-nth-length-billing]].
- **DLR webhook** is the source of truth for actual carrier delivery; NTH's status vocabulary is richer than MsgHub's. See [[sms-nth-dlr-webhook]].
- **Anti-spam policy gate** before install; SMS is heavily regulated and the merchant carries full liability. See [[sms-nth-dlr-webhook]].

## Related

- [[marketing-channels]] — parent hub (all marketing channels).
- [[marketing-campaigns]] — campaigns use this channel for SMS delivery steps.
- [[marketing-channels-sms-msghub]] — the other SMS provider option (shares the Phone subscriber-channel group).
- [[marketing-channels-viber]] — Viber Business Messages (also shares the Phone group).
- [[marketing-subscribers]] — subscribers' phone numbers live on the `Phone` SubscriberChannel row.
- [[marketing-campaigns-policy]] — anti-spam policy required before installation.
- [[notification-delivery]] — outbound delivery concept page.
- [[channel]] — Channel entity reference.

## Open questions

No outstanding questions.
