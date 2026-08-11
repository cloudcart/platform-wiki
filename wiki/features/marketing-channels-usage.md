---
type: feature
nav_path: "Marketing → Channels → Channels setup → Usage"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["Channel usage", "Plan usage", "Email usage", "SMS usage", "Viber usage", "Web Push usage", "Channel quota", "Send limit", "Потребление", "Използване", "Лимит на канал", "Изпратени съобщения"]
tags: [marketing, channels, usage, monitoring, quota, plan]
plan_gates: ["campaign.channel.email", "campaign.channel.sms_msghub_message", "campaign.channel.sms_nth_message", "campaign.channel.web_push", "viber_messages"]
created: 2026-05-23
updated: 2026-06-10
source_count: 2
---

# Channel usage

## Purpose

The **Usage** modal is the merchant's send-count meter for each communication channel — it answers *"how many messages have I sent on this channel, and how many do I have left on my plan?"* It opens from the **Usage** action on any channel card on the Channels setup screen and is available for **all five** of the active channels: Email, SMS MsgHub, SMS NTH, Viber, and Web Push.

The modal headlines a 30-day date range in its title bar, then shows five card-level metrics: the plan **Limit**, the **Remaining** count, the **Total sent** (cumulative all-time), plus per-message engagement counters **Clicks** and **Opened**. When a merchant is about to hit their plan cap they can press the **Buy credit** button in the modal footer to jump to that channel's feature-pack purchase flow.

This modal is the merchant's primary lever for understanding *why* a campaign was blocked with *"You do not have enough credits for:name"* — Usage tells them exactly how close they are to (or how far past) the cap.

## Sub-pages (in this cluster)

This feature is split into 6 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[channels-usage-metrics]] — the five metric cards (Limit, Remaining, Total sent, Clicks, Opened); backend fields, formatting, NaN handling, grid layout.
- [[channels-usage-counter-model]] — the cumulative send counter; what counts as a send per channel (SMS NTH multi-part vs others); webhook vs send-time split; self-credentials counter exclusion.
- [[channels-usage-plan-limit]] — Limit = one-time + subscription bucket resolution; per-channel `plan_feature_key` table; how the plan value is resolved and the send-time block when the cap is reached.
- [[channels-usage-engagement-window]] — the fixed 30-day engagement window for Clicks and Opened; UTC-day boundaries vs locale title; campaign-only filter; display-vs-data range discrepancies.
- [[channels-usage-buy-credit]] — the Buy credit button; feature-event handoff to the feature-pack purchase modal; cap-recovery on success.
- [[channels-usage-alerts]] — the 80% threshold notification; CP-language locale; self-credentials suppression for Viber.

## Where to find it

Sidebar → **Marketing** → **Channels** → **Channels setup** → on any channel card → click **Usage** (pie-chart icon).

The Usage button is exposed on every installed channel card (Email, SMS MsgHub, SMS NTH, Viber, Web Push). The modal title changes per channel:

| Channel mapping | Modal title prefix |
|-----------------|--------------------|
| `email` | Email Usage |
| `sms_nth_message` | SMS Message Usage |
| `viber_message` | Viber Message Usage |
| `web_push` | Web Push Usage |
| `sms_msghub_message` | (falls back to empty prefix — see Open questions) |

The full title format is `{prefix} - {date_start} - {date_end}` (e.g., `Email Usage - 23.04.2026 - 23.05.2026`). The date range follows the store's configured display format (server setting `format.date`). See [[channels-usage-engagement-window]] for the data-vs-display range distinction.

## What the merchant can do here

- **See five metric cards** with Limit, Remaining, Total sent, Clicks, and Opened — see [[channels-usage-metrics]] for the per-card meaning and formatting.
- **Click Buy credit** in the modal footer to top up — emits a feature-modal event that opens the feature-pack purchase flow for this channel's `plan_feature_key`. See [[channels-usage-buy-credit]].
- **Close** the modal with the Close button.
- **See the live data range** in the modal title — always the 30 days ending today, in the store's locale-formatted date style.

## What the merchant cannot do here

- **Cannot change the date range** — the underlying engagement counters use a fixed 30-day UTC window; see [[channels-usage-engagement-window]].
- **Cannot reset the Total sent counter** — it never rolls over; see [[channels-usage-counter-model]].
- **Cannot purchase credit from the modal directly** — Buy credit hands off to the feature-pack purchase modal; see [[channels-usage-buy-credit]].
- **Cannot drill into individual sends** from here — use the channel card's **Logs** action ([[marketing-channels-logs]]).
- **Cannot view usage for channels they have not installed** — the Usage button is only rendered on cards for channels the merchant has installed and where usage tracking is available.

## Settings & fields

The modal body renders five labelled cards in a 3-column grid (responsive). The exhaustive per-card field table and per-channel `plan_feature_key` mapping live on the aspect pages:

- Per-card backend fields and formatting → [[channels-usage-metrics]].
- Per-channel `plan_feature_key` and one-time + subscription resolution → [[channels-usage-plan-limit]].
- Title-vs-data date range computation → [[channels-usage-engagement-window]].

## Business rules

The Usage system has six business-rule clusters, each documented on its aspect page:

- **Counter is cumulative, not per-cycle; SMS NTH multi-part counting; failed sends do not count; self-credentials excluded** → [[channels-usage-counter-model]].
- **Limit = one-time + subscription summed; `Unlimited` resolution; send-time block when the cap is reached** → [[channels-usage-plan-limit]].
- **Engagement counters use a fixed 30-day UTC window; campaign-only filter** → [[channels-usage-engagement-window]].
- **Buy credit emits a feature event, does not save; top-up grows the one-time bucket** → [[channels-usage-buy-credit]].
- **80% threshold alert routing and CP-language locale; self-credentials suppression for Viber** → [[channels-usage-alerts]].
- **Remaining can render negative**; treat any negative Remaining as "overdrawn — buy credits or upgrade" → [[channels-usage-metrics]].

## Related

- [[marketing-channels]] — parent channel-setup hub. The Usage button lives on every channel card there.
- [[marketing-channels-reputation]] — sibling modal on the Email channel card. Reputation tracks deliverability quality; Usage tracks send quantity vs plan cap.
- [[marketing-channels-email]], [[marketing-channels-sms-msghub]], [[marketing-channels-sms-nth]], [[marketing-channels-viber]], [[marketing-channels-webpush]] — sibling channel pages. Each one has its own Usage modal accessible from its card.
- [[marketing-channels-logs]] — per-recipient drill-down for individual sends and engagement.
- [[marketing-channels-system-messages]] — transactional traffic that shares the channel counter.
- [[marketing-campaigns]] — campaigns are blocked with *"You do not have enough credits for:name"* when Usage hits the cap.
- [[plan-gates]] — concept page on plan feature gating; defines the `campaign.channel.*` and `viber_messages` feature keys.
- [[plans]] — plan tiers that define the per-channel cap defaults.
- [[plan-feature]] — feature-pack purchase target the **Buy credit** button navigates to.
- [[settings-admin-notifications]] — admin notification routing for the 80% alert.
- [[notification-delivery]] — concept page on platform-wide outbound message routing.

## Open questions

- **`sms_msghub_message` title prefix** — falls through the explicit per-channel switch and renders an empty prefix. The full title becomes ` - {date_start} - {date_end}` (leading hyphen). `(verify)` whether this is by design (channel rebranded internally) or a missed case in the per-channel switch.
