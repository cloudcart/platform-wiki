---
type: entity
nav_path: "Entity → Marketing Campaign"
aliases: ["Marketing Campaign", "Campaign", "Newsletter campaign", "Promotional campaign", "Automation campaign", "Drip campaign", "Кампания", "Маркетингова кампания", "Имейл кампания", "Бюлетин"]
tags: [entity, marketing, campaigns, automation, email, sms, viber, push]
created: 2026-05-23
updated: 2026-06-10
source_count: 1
---

# Marketing Campaign

## Identity

A **Marketing Campaign** is a multi-channel message dispatch the merchant sends to a [[segment|Segment]] of [[subscriber|Subscribers]] — an email newsletter, a promotional SMS blast, a Viber discount announcement, a web-push back-in-stock alert, or any combination of these channels. The campaign carries: a name, a target Segment, one or more per-channel **actions** (the actual messages — Email + SMS + Viber + Web Push), a schedule (immediate / delayed / triggered by a customer event), and a delivery log per recipient. The merchant manages campaigns on [[marketing-campaigns]]; the underlying channel infrastructure is configured on [[marketing-channels]].

CloudCart distinguishes **two shapes** of campaign — `regular` (one-shot blast) and `automated` (multi-step flow triggered by a customer event). Both shapes share the same Campaign entity (one `type` field), the same actions / channels / logs / statistics structure, and the same gating on the merchant's anti-spam policy acceptance ([[marketing-campaigns-policy]]). The differences live in scheduling, recipient picking, and edit-time locks — see [[campaign-entity-types-regular-automated]].

This entity is one of the higher-state-count records in the platform: the lifecycle moves through Draft → Active → Inactive → Completed → Archived → Banned, with auto-archival on regular-campaign completion and edit-locks while Active. Stock-style attribution flows: every Order placed via a click on a campaign message back-references the originating `campaign_id` and `campaign_action_id` for revenue measurement. Per-recipient delivery is gated by a two-layer consent model and is auto-suppressed on bounce / abuse.

## Sub-pages (in this cluster)

This entity is split into 6 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[campaign-entity-types-regular-automated]] — the two shapes (`regular` vs `automated`), trigger conditions, snapshot-vs-stream recipient picking, re-enrolment semantics.
- [[campaign-entity-attributes-schema]] — every key attribute the merchant configures + the underlying status / progress / archive columns and the hourly-refreshed counter columns.
- [[campaign-entity-lifecycle]] — Draft → Active → Inactive → Completed → Archived → Banned state machine, auto-archive on completion, edit-lock while Active, copy / archive / delete distinctions.
- [[campaign-entity-relationships]] — Segment / Subscriber / CampaignAction / CampaignChannelLog / Order back-references, what gets soft-deleted with the campaign and what doesn't, plan-feature cap interaction.
- [[campaign-entity-consent-gating]] — the two-layer consent model (Customer-level + per-channel Subscriber), recipient deduplication, channel-availability checks, anti-spam policy gate, auto-bounce / auto-unsubscribe on failure.
- [[campaign-entity-attribution-statistics]] — how clicks on campaign messages stamp orders with `cc_campaign_*` metadata, how per-action and per-campaign counters roll up, the hourly aggregation lag, banned-from-channels computation.

## Aliases

- **Marketing Campaign** / **Campaign** — the canonical merchant-facing term in the admin UI ("Campaigns" sidebar item under Marketing).
- **Newsletter campaign** — informal phrasing when the campaign is email-only.
- **Promotional campaign** — informal phrasing when the campaign targets a sale or promotion.
- **Automation campaign** / **Drip campaign** — informal phrasing for the Automated type, specifically multi-step welcome / win-back sequences.
- Bulgarian: **Кампания** (standard), **Маркетингова кампания**, **Имейл кампания**, **Бюлетин** ("newsletter").

## Key Attributes

The merchant-controlled identity of a campaign — the minimum to make it dispatchable. Each attribute is detailed (with column-level fidelity) on [[campaign-entity-attributes-schema]].

| Attribute | What the merchant controls | Pointer |
|-----------|----------------------------|---------|
| **Name** | Required, internal label (max 191 chars). | [[campaign-entity-attributes-schema]] |
| **Type** | `regular` / `automated`. Cannot be switched after creation. | [[campaign-entity-types-regular-automated]] |
| **Status** | `active` / `inactive` / `draft` / `archived` — the list-page tab. | [[campaign-entity-lifecycle]] |
| **Segment** | Required target audience — [[segment|Subscriber Segment]]. | [[campaign-entity-relationships]] |
| **Channel actions** | One action per channel per step — the actual messages. | [[campaign-entity-relationships]] |
| **Schedule** | Immediate / delayed / triggered by event. | [[campaign-entity-types-regular-automated]] |
| **Statistics** | Per-action delivery / open / click / order / revenue counters. | [[campaign-entity-attribution-statistics]] |
| **Banned reason** | NULL unless platform anti-spam moderation flagged the campaign. | [[campaign-entity-consent-gating]] |

## Where it appears

- [[marketing-campaigns]] — the master campaign list (Active / Inactive / Archived / Draft tabs) + the create / edit / statistics / subscribers / logs sub-screens.
- [[marketing-channels]] — the per-channel configuration screens. At least one channel must be installed and verified to send a campaign on that channel.
- [[marketing-channels-email]] — Email channel configuration including DKIM / SPF / DMARC and sender domain.
- [[marketing-campaigns-policy]] — the anti-spam acceptance screen gating first-send.
- [[marketing-segments]] — segments are the audiences campaigns target.
- [[marketing-subscribers]] — subscribers are the recipients.
- [[marketing-campaigns-statistics]] — per-campaign Statistics screen showing per-step delivery, opens, clicks, orders, conversion rate, revenue.

## Related

### Related entities

- [[segment]] — the target audience. Required on every campaign.
- [[subscriber]] — the recipients. Per-subscriber consent at customer level + per-channel level gates delivery.
- [[customer]] — when a subscriber is also a customer, the customer's `marketing` flag is the first consent gate.
- [[email-template]] — distinct concept: templates are transactional (order-confirmation, etc.), campaigns are merchant-driven marketing.
- [[discount]] — campaigns commonly include a discount code in the message body. The discount and the campaign are separate records.
- [[order]] — orders attributed to a campaign carry `campaign_id` / `campaign_action_id` back-references.

### Cross-cutting concepts

- [[notification-delivery]] — the two-layer consent model that gates every send — referenced from [[campaign-entity-consent-gating]].
- [[subscriber-vs-customer]] — the distinction between Subscribers (campaign recipients) and Customers (order placers).
- [[multi-language]] — campaign messages can be authored in multiple languages with per-subscriber locale-based delivery.
- [[plan-gates]] — the `campaigns` plan-feature caps how many campaigns can be live — see [[campaign-entity-relationships]] for the archived-don't-count rule.

### Settings & infrastructure

- [[marketing-campaigns-policy]] — anti-spam acceptance and ban / unban flow.
- [[marketing-channels]] — channel installation, sender domain verification, provider credentials.

## Open Questions

- ⏸️ Whether an Automated campaign whose trigger is "subscriber enters Segment X" re-fires when the same subscriber re-enters the segment after exiting — or whether each subscriber can pass through the flow only once. (Partial answer on [[campaign-entity-types-regular-automated]] — re-enrolment IS allowed by default on `subscriber_to_campaigns` separate pivot rows.)
- ⏸️ The exact behavior when a Regular campaign's Segment changes between save time and send time (e.g., a subscriber added to the Segment 5 minutes before send: do they get the message?).
- ⏸️ Whether a banned campaign that the merchant then resolves and re-activates resumes from where it stopped or restarts the funnel for in-progress subscribers.
