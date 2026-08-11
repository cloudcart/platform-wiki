---
type: feature
nav_path: "Marketing → Channels → Channels setup → Usage → Counter model"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["Total sent counter", "Channel send counter", "Cumulative send count", "Per-channel counter", "SMS multi-part counting", "Self-credentials excluded from count", "Бройка изпратени съобщения", "Кумулативен брояч"]
tags: [marketing, channels, usage, counter, send, mongo]
plan_gates: ["campaign.channel.email", "campaign.channel.sms_msghub_message", "campaign.channel.sms_nth_message", "campaign.channel.web_push", "viber_messages"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-channels-usage]]. See the hub for the other aspects (metric cards, plan limit, engagement window, buy-credit flow, alerts).

# Channel usage — Counter model

## Purpose

The **Total sent** card on the Usage modal is backed by a per-channel cumulative counter. This page explains what that counter is, what increments it, what does **not** increment it, why an SMS NTH cap depletes faster than a Viber cap with the same campaign sends, and why self-credentials sends do not count against the plan.

The counter is the operational heart of the Usage system — every gating decision (*"can this campaign run?"*, *"should we fire the 80% alert?"*, *"is the channel banned?"*) is computed from this counter and the resolved plan limit. See [[channels-usage-plan-limit]] for the limit side.

## Where to find it

The counter value itself surfaces as the **Total sent** card on the Usage modal — Sidebar → **Marketing** → **Channels** → **Channels setup** → on any channel card → click **Usage** → **Total sent** card. There is no admin screen for editing the counter directly.

## What the merchant can do here

- **Read** the cumulative all-time send count for a channel.
- **Compare it** against the Limit card to estimate how soon a top-up is needed.
- **Verify** that a recent campaign actually sent — Total sent moves immediately after each successful send job.

## What the merchant cannot do here

- **Cannot reset the counter** — no scheduled rollover, no billing-cycle hook, no UI to clear it. Once incremented, it stays incremented.
- **Cannot exclude specific message types** — campaign-action sends, transactional sends, and system messages all share the same counter. A store with heavy order-confirmation traffic and no marketing campaigns will still see Total sent grow.
- **Cannot refund a send** — even bounced messages stay counted. The counter increments at send-job success, not at delivery webhook (see Business rules below).
- **Cannot see the counter for a channel that has never been activated** — the counter is created lazily on the first send.

## Settings & fields

The counter is a single per-store, per-channel running total. The fields exposed to the merchant via the Usage API are:

| API field | Source | Description |
|-----------|--------|-------------|
| `usage_count` | the counter's `total_sent` | The cumulative count rendered as **Total sent**. |
| `plan_remaining` | derived: `plan_value - usage_count` | Renders as **Remaining**. |

The counter is incremented by every successful per-channel send job — see Business rules for the per-channel counting rules.

## Business rules

### Counter increments on send-job success, not on delivery webhook

The counter increments fire from the per-channel send job at the moment the message is handed off to the upstream provider successfully (the `total_sent` and `successfully_sent` statistic fields both move). Webhooks that arrive later (`delivered`, `seen_message`, `opened_url`) increment **other** statistic fields but **not** `total_sent`.

Consequence: a message that is sent successfully then bounces back later is **still counted as one send against the cap**. Bouncing does not refund credits. To investigate undelivered sends use the channel's Logs (see [[marketing-channels-logs]]).

### SMS NTH counts multi-part sends individually; other channels count rows

There is a verified difference in how the count is tallied per channel:

- **SMS NTH** — sums the `total_sent` value directly. A 3-part SMS message contributes **3** to the count.
- **All other channels** (`email`, `viber_message`, `web_push`, `sms_msghub_message`) — counts **each send entry that has `total_sent > 0`**. A multi-part-ish payload that ends up as one send entry contributes **1**.

This is why an SMS NTH cap of 1,000 may deplete faster than a Viber cap of 1,000 even with the same number of campaign sends. A merchant who composes 300-character SMS NTH messages that split into 2 parts each will burn the cap at twice the rate of one-part messages.

### Self-credentials sends are excluded from the count

Verified hidden behaviour: the tally that computes the channel's total sends counts only sends where `self_credentials != 1` — so sends made via merchant-supplied credentials (currently only Viber InfoBip self-contract) are **not** counted toward the cap. Each such send is recorded with `self_credentials = 1`, and that flag excludes it from the count.

This is the mechanism that makes self-credentials effectively unlimited from a plan perspective. The Total sent card on the Usage modal still shows the **non-self-credentials count** — if a Viber merchant uses self-credentials exclusively, Total sent will stay at 0 even after thousands of sends.

### What counts as a "send" per channel

| Channel | One "send" equals | Notes |
|---------|-------------------|-------|
| Email | One outbound email | One recipient = one count. |
| SMS NTH | One SMS-part | A 300-char message split into 2 parts = **2** counts. |
| SMS MsgHub | One send | Not multi-part-aware by the same mechanism. |
| Viber | One send | One recipient = one count; self-credentials sends excluded. |
| Web Push | One device-send | A subscriber with 3 devices counts as **3**. |

### Per-subscriber de-duplication

Send-counter records are keyed uniquely per subscriber + customer + system event + store + channel. Duplicate sends to the same subscriber on the same channel for the same system event increment the existing record's `total_sent` and `successfully_sent` values rather than creating new records. This is why the per-template send counter on system messages reflects **unique-subscriber** count, not total dispatches.

### Failed sends do not count

If the send job fails before the upstream provider acknowledges the message (e.g., undeliverable address rejected at provider boundary, internal validation error), neither `total_sent` nor `successfully_sent` increments. The merchant pays no credits for these. Sends that fail **after** acknowledgement (bounces, delivery rejections via webhook) **do** count — see the first business rule above.

### Marketing and transactional traffic share the counter

The counter does not distinguish between campaign-action messages and transactional / system messages (order-confirmation email, abandoned-cart Viber, etc.) routed through the same channel. All live messages on the channel count against the same cap. A merchant who suspects their cap is being burned by transactional traffic should review which system messages are routed through that channel under [[marketing-channels-system-messages]].

## Related

- [[marketing-channels-usage]] — hub.
- [[channels-usage-metrics]] — the Total sent card on the Usage modal.
- [[channels-usage-plan-limit]] — how `plan_remaining` is computed against the counter.
- [[channels-usage-alerts]] — 80% threshold alert reads from this counter.
- [[channels-usage-buy-credit]] — what the merchant does when Remaining hits 0.
- [[marketing-channels-system-messages]] — transactional traffic that also counts.
- [[marketing-channels-logs]] — per-recipient drill-down for investigating sends.

## Open questions

No outstanding questions.
