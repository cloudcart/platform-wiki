---
type: feature
nav_path: "Marketing → Channels → Channels setup → Reputation"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["Channel reputation", "Email reputation", "Reputation rate", "Sender reputation", "Репутация", "Репутация на канал", "Репутация на имейл канал"]
tags: [marketing, channels, reputation, monitoring, email, deliverability]
plan_gates: ["campaign.channel.email"]
created: 2026-05-23
updated: 2026-06-10
source_count: 2
---
# Channel reputation (Email)

## Purpose

The **Reputation** modal is the merchant's deliverability-health window for the **Email channel**. It surfaces the four percentages that Elastic Email computes for the store's dedicated Email sub-account — **spam rate**, **bounce rate**, **open rate**, **click rate** — plus a single roll-up **reputation rate** that headlines the modal. These numbers are the same ones CloudCart uses behind the scenes to decide whether to auto-suspend the channel: a merchant whose spam rate crosses the platform max, bounce rate crosses the platform max, or open rate falls below the platform min will see their Email channel suspended and every campaign that uses it stopped.

Reputation data is **only available for the Email channel** — the other four channels (SMS MsgHub, SMS NTH, Viber, Web Push) do not expose a Reputation button on their channel card, because their providers (Link Mobility, NTH Mobile, InfoBip, browser VAPID) do not feed reputation telemetry back into CloudCart. The Reputation modal is the merchant's read-only deliverability dashboard for Email — they can't change the numbers here, only diagnose them and take corrective action (clean the list, change content, lower send frequency) before CloudCart's auto-suspend triggers fire.

This cluster splits the topic into four aspects so the Assistant reads only the slice a question touches.

## Sub-pages (in this cluster)

- [[channels-reputation-modal]] — the Reputation modal UI surface: where to find it, the headline rate + four cards, the warning banner, read-only behaviour, what the merchant can / cannot do.
- [[channels-reputation-metrics]] — the four metric definitions (spam / open / bounce / click), the headline reputation rate, their backend source fields, and formatting / defaults.
- [[channels-reputation-sync]] — the 12-hour background reputation sync, the snapshot cache, the live Elastic Email fallback on cache miss, the full-account snapshot window, and UTC start-of-day keying.
- [[channels-reputation-auto-suspend]] — how reputation feeds auto-suspend: thresholds, the 500-message minimum, the 99% exemption, manual CC denial, the cascade to campaigns + admin notification, and API-key-expired auto-deactivation.

## Where to find it

Sidebar → **Marketing** → **Channels** → **Channels setup** → on the **Email** channel card → click **Reputation** (star icon).

The Reputation button only appears on the Email channel card — it is hidden on all other channels, and only after the Email channel is **fully configured** (profile → domain → DNS verify → sender email all complete). See [[channels-reputation-modal]] for the full surface and [[marketing-channels-email]] for the configuration prerequisite.

## What the merchant can do here

- **See the headline Reputation rate** (single roll-up percentage) in the modal footer.
- **See four card-level breakdown metrics** — Spam rate, Open rate, Bounce rate, Click rate — in the modal body. See [[channels-reputation-metrics]].
- **Read the warning banner** explaining the auto-suspend thresholds. See [[channels-reputation-auto-suspend]].
- **Close** the modal (Close button or backdrop-click).

## Settings & fields

The modal is **purely read-only** — there are no editable fields. The headline reputation rate and the four card metrics, their source fields and formatting, are documented in [[channels-reputation-metrics]]. The auto-suspend thresholds shown in the warning banner are documented in [[channels-reputation-auto-suspend]].

## Business rules

- Reputation is **Email-only**; non-`email` mappings reject with *"Reputation is only available for email channel"* (HTTP 400). See [[channels-reputation-modal]].
- Data refreshes on a **12-hour background sync**; a freshly-launched campaign may not show for up to 12 hours. See [[channels-reputation-sync]].
- The values reflect Elastic Email's **rolling full-account window**, not a CloudCart per-day computation; there is no date picker. See [[channels-reputation-sync]].
- After each sync the platform runs the **auto-suspend check**; tripping a threshold deactivates the channel and stops every campaign that uses it. See [[channels-reputation-auto-suspend]].
- The merchant **cannot clear an auto-suspend from this modal** — fix the underlying problem, wait for the next sync, and recovery lifts it (or contact CloudCart staff for a manual unsuspend). See [[channels-reputation-auto-suspend]].

## Related

- [[marketing-channels]] — parent channel-setup hub with the full auto-suspend flow.
- [[marketing-channels-email]] — Email channel configuration (profile, domain, DKIM/SPF/Tracking/DMARC verify, sender email). Reputation requires this to complete first.
- [[marketing-channels-usage]] — sibling modal on the same channel card. Reputation tracks deliverability quality; Usage tracks send quantity vs plan cap.
- [[marketing-channels-sms-msghub]], [[marketing-channels-sms-nth]], [[marketing-channels-viber]], [[marketing-channels-webpush]] — sibling channels. None expose a Reputation modal — Email is the only channel with provider-fed reputation telemetry.
- [[marketing-campaigns]] — campaigns are auto-stopped when reputation trips a threshold.
- [[plan-gates]] — `campaign.channel.email` plan-feature key required to have Email available at all.
- [[notification-delivery]] — concept page on platform-wide outbound message routing and deliverability.

## Open questions

No outstanding questions.
