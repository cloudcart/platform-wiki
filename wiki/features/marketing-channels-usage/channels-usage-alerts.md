---
type: feature
nav_path: "Marketing → Channels → Channels setup → Usage → Threshold alert"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["80% usage alert", "Channel cap warning", "Usage alert notification", "campaign.channel.usage notification", "USAGE_ALERT_PERCENTAGE", "Self-credentials alert suppression", "Предупреждение за лимит", "80 процента уведомление"]
tags: [marketing, channels, usage, alert, notification, threshold]
plan_gates: ["campaign.channel.email", "campaign.channel.sms_msghub_message", "campaign.channel.sms_nth_message", "campaign.channel.web_push", "viber_messages"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-channels-usage]]. See the hub for the other aspects (metric cards, counter model, plan limit, engagement window, buy-credit flow).

# Channel usage — 80% threshold alert

## Purpose

When a channel's cumulative send count crosses **80%** of its plan cap, the platform fires an admin notification to the merchant. This page documents when the alert fires, what it says, where the merchant reads it, why it can fire from a send-job rather than the Usage modal, and the one case where it does NOT fire (Viber with self-credentials).

The alert is the merchant's early-warning system between *"I have plenty of headroom"* and *"my next campaign got the You do not have enough credits error"*. Without it, the merchant only learns about the cap when a send fails.

## Where to find it

- The alert renders in the merchant's **admin notifications panel** (the bell / notification stream in the admin header).
- Notifications group under the key `campaign.channel.usage.{channel_mapping}` (e.g., `campaign.channel.usage.email`, `campaign.channel.usage.viber_message`).
- Alerts are written from the per-channel send job, **not** from opening the Usage modal — viewing the modal does not trigger an alert.

## What the merchant can do here

- **Read the alert** in the notifications panel — it identifies the channel by name and shows the current percentage hit.
- **Click through** the notification (if the panel exposes a link) to investigate.
- **Top up credits** via the Buy credit flow before the cap is fully consumed — see [[channels-usage-buy-credit]].
- **Configure admin notification routing** at [[settings-admin-notifications]] to control where the alert is delivered.

## What the merchant cannot do here

- **Cannot change the 80% threshold** — it is hard-coded as `USAGE_ALERT_PERCENTAGE = 80` server-side.
- **Cannot configure a per-channel different threshold** — one value applies to all channels.
- **Cannot snooze or acknowledge** the alert in a way that suppresses re-firing — the alert is governed by the send job that crosses the threshold, not by a sticky flag.
- **Cannot receive the alert** when self-credentials is enabled for the channel (currently only Viber — see Business rules).

## Settings & fields

### Alert configuration (read-only, server-defined)

| Setting | Value | Notes |
|---------|-------|-------|
| Threshold percentage | `USAGE_ALERT_PERCENTAGE = 80` | Hard-coded constant. Not merchant-configurable. |
| Notification group | `campaign.channel.usage.{channel_mapping}` | One group per channel — `email`, `sms_nth_message`, `sms_msghub_message`, `viber_message`, `web_push`. |
| Notification text | *"You have reached:percent of:total messages for your channel:channel limit"* | Translated into the admin CP language at write time. |
| Trigger point | Per-channel send job, after each successful send | The job calls a `sendUsageAlert` check after `incrementSystemField`. |
| Suppression condition | `use_self_credentials = true` for the channel | Currently only meaningful for Viber. |

### Alert message variables

| Variable | What it carries |
|----------|-----------------|
| `:percent` | The current percentage (computed as `total_sent / plan_value × 100`). |
| `:total` | The plan cap value (the resolved Limit — see [[channels-usage-plan-limit]]). |
| `:channel` | The localized channel name (e.g., *"Email"*, *"SMS"*, *"Viber"*). |

## Business rules

### The 80% threshold fires from the send job

Each per-channel send job calls `sendUsageAlert` after a successful send. The check compares the post-increment counter against the plan cap; if the new ratio crosses the 80% boundary and the alert has not yet been fired for this crossing, it fires. The Usage modal is read-only — opening it does **not** evaluate the threshold or fire an alert.

Consequence: a merchant who never sends a campaign but watches Total sent grow from transactional traffic will still get the alert — any send-job success can trigger it.

### The alert message uses the CP-language locale

Verified: when the threshold is crossed, the notification message is built with `withLocale(site('language_cp'), ...)` — the notification text uses the admin CP-language locale, not the storefront language. So an admin reading the notification panel in English sees the EN message even if the storefront serves customers in Bulgarian.

### Self-credentials suppresses the alert (Viber only)

If the channel has `use_self_credentials = true` — currently exposed only for Viber — the alert does **not** fire when the 80% threshold is crossed. This is consistent with the channel's broader self-credentials behaviour: sends are excluded from the counter (see [[channels-usage-counter-model]]), Remaining ≤ 0 does not flip the channel to banned, and the cap is effectively bypassed. There is no point alerting on a cap the merchant is not using.

For Email, SMS MsgHub, SMS NTH, and Web Push, self-credentials are not currently exposed in the UI — the plan cap always applies and the alert always fires at 80%.

### The 80% alert is independent of the feature-limit-reached ban

When Remaining drops to 0 or below, the channel's banned-reason flips to feature-limit-reached and the channel is suspended for new sends — see [[marketing-channels]] for the per-channel banned-reason mechanic. That ban is a separate event from the 80% alert and uses a different notification surface (channel-card status badge, not the admin notification panel).

A merchant should expect:

1. **80% notification** in the admin notifications panel — warning, no send block.
2. **100% reached** — channel banned with feature-limit-reached reason, *"You do not have enough credits for:name"* error on campaigns.
3. **Buy credit** → ban clears on the next page refresh.

### The alert does not fire for the unlimited case

When the plan resolves the feature key as `Unlimited`, `plan_value` is non-numeric and there is no percentage to cross. The 80% check short-circuits — the alert does not fire. The merchant on an unlimited plan never sees a usage alert for that channel.

### Alert routing follows the admin-notification settings

Where the alert lands (email digest, panel-only, etc.) depends on the merchant's [[settings-admin-notifications]] configuration. The alert is written to the notification group `campaign.channel.usage.{channel_mapping}` — merchants who turn off that group entirely will not receive the warning. Turning it off does **not** disable the cap or the send-time block; only the warning is silenced.

### Alert is per-channel, not per-store

Each channel evaluates the threshold independently using its own counter and its own plan cap. Crossing 80% on Email triggers `campaign.channel.usage.email`; crossing 80% on Viber triggers `campaign.channel.usage.viber_message`. The notifications are separate items in the panel.

## Related

- [[marketing-channels-usage]] — hub.
- [[channels-usage-counter-model]] — the counter that drives the percentage; explains why self-credentials sends are excluded.
- [[channels-usage-plan-limit]] — the cap value used in the percentage denominator.
- [[channels-usage-metrics]] — the Remaining card that goes to 0 when the cap is fully consumed.
- [[channels-usage-buy-credit]] — the recovery path from cap-reached back to working.
- [[settings-admin-notifications]] — admin notification routing.
- [[marketing-channels]] — channel-setup hub; per-channel banned-reason mechanic.

## Open questions

No outstanding questions.
