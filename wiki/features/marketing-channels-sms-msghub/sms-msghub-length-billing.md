---
type: feature
nav_path: "Marketing → Channels → Channels setup → SMS Msg Hub → Length & billing"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["SMS MsgHub length", "SMS MsgHub billing", "MsgHub multi-part SMS", "MsgHub character counter", "MsgHub cost model", "MsgHub buy more credits"]
tags: [marketing, channels, sms, msghub, billing, length]
plan_gates: ["campaign.channel.sms_msghub_message"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-channels-sms-msghub]]. See the hub for the other aspects (overview, send pipeline, settings, DLR webhook).

# SMS MsgHub — Message length & billing

## Purpose

Documents how SMS message length translates into billable SMS parts, what the campaign-editor character counter shows, the per-send cost model, and what happens when the merchant's plan cap is exhausted.

## Where to find it

The character / SMS-part counter appears in the **campaign editor** when the merchant adds an **"SMS (msghub)"** action and types the body. The usage-versus-cap figure appears in the channel-card **Usage** modal (Marketing → Channels → Channels setup → SMS Msg Hub → Usage — see [[sms-msghub-overview]]).

## What the merchant can do here

- See the live **Characters** and **SMS** (parts) counts while composing the body.
- See SMS sent this billing cycle versus the plan cap in the Usage modal.
- **Buy more credits** (a feature pack) or upgrade the plan tier when the cap is reached.

## Settings & fields

### Length limits per encoding

| Encoding | Single SMS | Per part when concatenated |
|----------|-----------|----------------------------|
| GSM-7 (Latin / standard chars) | 160 chars | 153 chars/part |
| UCS-2 (Cyrillic or special chars) | 70 chars | 67 chars/part |

The MsgHub provider does the concatenation transparently, **but the merchant is billed per part**. There is no MsgHub-specific `MAX_MESSAGE_LENGTH` constant — the channel relies on MsgHub's own length enforcement.

### Campaign-editor counter

The character counter shows two figures: **Characters** → exact character count, and **SMS** → number of SMS parts the body translates to (labelled `remaining_characters` and `remaining_messages` in the translation file). When the body uses template variables, the merchant sees the warning: *"The calculated message length is approximate. When using variables, the actual length may vary significantly."*

## Business rules

### Cyrillic content multiplies cost fast

A 200-character Bulgarian (UCS-2) message is **3 parts** (200 ÷ 67 ≈ 3), tripling the per-recipient cost versus a single 70-char message. Merchants composing Cyrillic blasts should watch the SMS-part counter, not the character count, to estimate spend.

### Cost model — billed in SMS sends against the plan cap

The merchant is billed against the plan-cap on `campaign.channel.sms_msghub_message` — typically counted in "SMS sends" (the per-part billing above is the MsgHub-side cost that rolls into this). The exact billing is plan-dependent: entry-level plans get a small monthly quota plus the option to buy more credits; higher tiers bundle larger quotas.

### Plan-cap exhaustion → Buy more credits

When the cap is reached, the `feature_limit_reached` banner appears with a **Buy more credits** button on the channel card and on any campaign that uses the channel. The merchant either purchases a feature pack (e.g. 1,000 more SMS sends) or upgrades the plan tier. Note that an exhausted cap also auto-deactivates the channel on the next send attempt — see the plan-cap pre-flight on [[sms-msghub-send-pipeline]].

## Related

- [[marketing-channels-sms-msghub]] — hub.
- [[sms-msghub-send-pipeline]] — the plan-cap pre-flight that auto-deactivates on exhaustion.
- [[marketing-channels-usage]] — the shared Usage modal that shows sent-vs-cap.
- [[marketing-campaigns]] — where the editor's SMS-part counter appears.

## Open questions

No outstanding questions.
