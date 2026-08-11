---
type: feature
nav_path: "Marketing → Channels → Channels setup → SMS → Length & billing"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["SMS NTH length", "SMS NTH billing", "NTH SMS parts", "NTH cost model", "NTH usage alert", "NTH multi-part SMS"]
tags: [marketing, channels, sms, nth, billing, usage]
plan_gates: ["campaign.channel.sms_nth_message"]
created: 2026-06-10
updated: 2026-06-10
source_count: 7
---
# SMS NTH — message length & billing

> Part of [[marketing-channels-sms-nth]]. See the hub for the other aspects (overview, send pipeline, settings, DLR webhook).

## Purpose

This aspect documents **how an NTH SMS is counted and charged**: the GSM-7 / UCS-2 segment limits, multi-part concatenation (handled NTH-side), the campaign-editor character + SMS-part counter, the plan-cap cost model and exhaustion flow, and the `usage_alert` threshold.

## Where to find it

- The **character + SMS-part counter** appears live in the **campaign editor** when authoring an "SMS (NTH Message)" action body (see [[marketing-campaigns]]).
- The **Usage** modal (sent-count vs plan cap) opens from the **SMS** channel card under Sidebar → **Marketing** → **Channels** → **Channels setup** (`campaigns-channels`, `/admin/marketing-new/campaigns/channels`). Its title is *"SMS Message Usage - {date_start} - {date_end}"*.

## What the merchant can do here

- **See the projected length / parts** while writing the SMS body, before launching.
- **View Usage** — SMS sent this billing cycle against the plan cap.
- **Buy more credits** (feature pack) or upgrade the plan when the cap is reached.

## Settings & fields

There are no merchant-editable length / billing fields — the limits are protocol-driven and the cap is set by the plan. The relevant plan-feature key is `campaign.channel.sms_nth_message`.

## Business rules

### Message length and multi-part SMS

Standard SMS-protocol rules apply — **160 chars GSM-7** or **70 chars UCS-2** per segment. NTH handles the concatenation **server-side**; CloudCart shows the merchant the approximate character / SMS-parts count in the campaign editor.

The character counter shows both the raw character count and the projected number of SMS parts:

- single part = 160 GSM-7 chars / 70 UCS-2 chars;
- multi-part = 153 GSM-7 / 67 UCS-2 per part (the concatenation header consumes a few chars per segment).

**Cyrillic content forces UCS-2 mode** — a 200-char Bulgarian message is **3 parts**. This is the single biggest billing surprise for Bulgarian merchants: Cyrillic messages consume parts far faster than Latin ones.

The counter is **approximate** when variables are used. The campaign editor shows the note (translation key `variables_length_warning`): *"The calculated message length is approximate. When using variables, the actual length may vary significantly."* Runtime variable substitution (e.g. a long product name) can push a 1-part message into 2 parts.

### Cost model

NTH bills CloudCart **per SMS part**, which translates to the merchant's plan-cap consumption. Like MsgHub, the per-SMS pricing is rolled into CloudCart's contract — the merchant sees a **quota in their plan**, not a per-message rate. A 3-part Cyrillic message consumes 3 units of the quota.

The merchant is billed against the plan-cap on `campaign.channel.sms_nth_message`.

### Plan-cap exhaustion

When the cap is reached, the channel shows the `feature_limit_reached` banner with a **Buy more credits** button. The merchant either:

- purchases a **feature pack** (adding more SMS sends to the quota), or
- **upgrades** the plan.

Note: the plan-cap is also re-checked inside the send worker — if it's exhausted at send time the message aborts and the channel auto-deactivates (see [[sms-nth-send-pipeline]]).

### Usage-alert threshold

The per-channel `usage_alert` notification fires at the `USAGE_ALERT_PERCENTAGE = 80`% threshold — surfaced in the admin notification panel, giving the merchant a heads-up before the quota runs out.

## Related

- [[marketing-channels-sms-nth]] — hub.
- [[marketing-channels-sms-msghub]] — same per-part billing model (MsgHub counterpart).
- [[marketing-campaigns]] — the campaign editor hosts the live character / parts counter.
- [[notification-delivery]] — outbound delivery concept page.

## Open questions

No outstanding questions.
