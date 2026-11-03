---
type: entity
nav_path: "Entity → Marketing Campaign → Relationships"
aliases: ["Campaign relationships", "CampaignAction", "CampaignChannelLog", "subscriber_to_campaigns pivot", "Campaign and Segment", "Campaign and Order back-reference", "Campaign plan cap", "Връзки на кампания"]
tags: [entity, marketing, campaigns, relationships]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[campaign]]. See the hub for the other aspects (types, attributes schema, lifecycle, consent gating, attribution & statistics).

# Campaign — Relationships

## Identity

A Campaign sits at the centre of a small graph of related records: the Segment it targets, the Subscribers in its funnel, the Actions (per-channel per-step messages), the per-recipient delivery logs, the Channels it uses, and the Orders that came from clicks. This page maps each relation, what gets carried back-and-forth, and what cascades on archive / soft-delete.

## Aliases

- **Action** = the per-channel per-step message body. The merchant edits actions as "Email content", "SMS content", "Viber content", "Web Push content" tabs (Regular) or as step-cards (Automated).
- **Channel log** = the per-(subscriber, action, delivery-attempt) record. Stored separately from the main campaign data.
- **Subscriber funnel row** = `subscriber_to_campaigns` = the in-funnel association record. One per (subscriber, campaign, re-enrolment cycle).

## Key Attributes

### What a Campaign relates to

| Direction | Target | Cardinality | Carries |
|-----------|--------|-------------|---------|
| Belongs to one | [[segment\|Segment]] via `segment_id` | 1: N (one segment, many campaigns) | The target audience. Required. |
| Has many | Action rows | 1: N | One per (channel, step). The actual messages. |
| Has many | Channel-log rows | 1: N | One per (subscriber, action) delivery attempt. The per-recipient delivery log. |
| Belongs to many | [[subscriber\|Subscribers]] via the `subscriber_to_campaigns` funnel association | M: N (with extra fields) | Subscribers currently in the campaign's funnel (waiting / executing / completed / removed). |
| Produces | [[order\|Orders]] tagged with `campaign_id` / `campaign_action_id` | 1: N | Revenue-attributed orders. See [[campaign-entity-attribution-statistics]]. |
| Uses | [[marketing-channels\|Marketing Channels]] | M: N (via actions) | At least one channel must be installed + verified for a campaign to be dispatchable on that channel. |

### What a Campaign is distinct from

- An [[email-template|Email Template]] — templates are transactional (order-confirmation, password-reset) fired automatically by platform events, NOT by merchant intent.
- A [[discount|Discount]] — campaigns CAN include discount codes inside the message body (the merchant manually inserts the code), but the discount and the campaign are independent records with independent counters.
- A per-product back-in-stock push notification — those are subscriber-level alerts on a specific product, not campaigns.

### The `subscriber_to_campaigns` funnel association

The M:N relation between Campaign and Subscriber is mediated by the `subscriber_to_campaigns` association, which carries extra fields per record:

- **`progress`** — per-subscriber funnel state (`waiting` / `waiting_delayed` / `delayed` / `executing` / `completed` / `removed`). NOT the same as the campaign-level `progress` — see [[campaign-entity-attributes-schema]].
- **`times_completed`** — counter incremented each time the subscriber finishes the flow. Used for Automated re-enrolment cycles.
- **Step / delay state** — Automated campaigns track which step the subscriber is at and when the next step fires.

For Automated campaigns with re-enrolment enabled, a subscriber accumulates one association record per cycle through the flow.

## Where it appears

- [[marketing-campaigns]] — the list page shows the related Segment name per row and lets the merchant drill into Subscribers / Logs sub-screens.
- [[marketing-campaigns-edit]] — the editor where actions (channel messages) are composed.
- [[marketing-campaigns-statistics]] — reads per-action counters rolled up from the per-recipient channel log.
- [[marketing-campaigns-statistics-log]] — the per-recipient log view.
- [[campaign-entity-attribution-statistics]] — how `campaign_id` / `campaign_action_id` get stamped on Orders.
- [[campaign-entity-lifecycle]] — what cascades on soft-delete.

### Channel availability gates the campaign

A campaign that includes an Email action requires the merchant to have the Email channel installed and verified ([[marketing-channels-email]]). Same for SMS / Viber / Web Push. The campaign editor warns the merchant when a channel needed by the campaign is not installed — the campaign can be saved as Draft but cannot be activated until the channel is available.

### Soft-delete cascades to actions, templates, logs, subscriber pivot (verified against backend)

When a campaign is soft-deleted (`deleted_at` set), the platform cascades the deletion to:

- Action rows (per-channel per-step messages)
- Action-template rows (the per-action template definitions)
- Action-log rows (per-action audit log)
- `subscriber_to_campaigns` funnel rows (detached from the subscribers)

The **separately-stored per-recipient channel-log rows are NOT auto-cleared** — they stay for audit purposes, just orphaned from the deleted campaign. This means GDPR-style data-export against a long-deleted campaign can still find delivery records.

### Plan-feature cap on `campaigns`

The `campaigns` plan-feature caps how many campaigns can exist on the store. The cap counts **non-archived** campaigns only — archived campaigns (those with an archive timestamp set) are excluded. So a merchant who hits the cap can archive old campaigns to free up headroom immediately, without losing log rows or statistics.

See [[plan-gates]] for the broader plan-feature framework and [[campaign-entity-lifecycle]] for the archive vs delete distinction.

### Recipient deduplication

A subscriber receives a Regular campaign's message **once** per channel — even if they enter the Segment multiple ways or the Segment includes them more than once. The per-recipient channel-log record is created with a uniqueness rule per (campaign_id, subscriber_id, channel).

For Automated campaigns with re-enrolment, each cycle through the flow creates a new funnel row on `subscriber_to_campaigns` but the per-cycle action deliveries dedup per (campaign, subscriber, channel, cycle).

## Related

- [[campaign]] — hub.
- [[campaign-entity-attributes-schema]] — column-level reference for the `segment_id` foreign key and the dual-`progress` distinction.
- [[campaign-entity-lifecycle]] — soft-delete cascade trigger.
- [[campaign-entity-consent-gating]] — how the subscriber pivot interacts with consent flags.
- [[campaign-entity-attribution-statistics]] — how Orders get the `campaign_id` / `campaign_action_id` back-reference.
- [[segment]] — the target-audience entity.
- [[subscriber]] — the recipient entity; gates delivery via per-channel consent.
- [[customer]] — when a subscriber is also a customer, the customer's `marketing` flag is the first consent gate (see [[campaign-entity-consent-gating]]).
- [[order]] — orders attributed to a campaign carry `campaign_id` / `campaign_action_id` back-references.
- [[discount]] — independent record; campaigns include discount codes manually.
- [[email-template]] — distinct concept; transactional vs marketing.
- [[marketing-channels]] — channel installation, sender domain verification.
- [[marketing-channels-email]] — Email channel configuration (DKIM / SPF / DMARC).
- [[plan-gates]] — the `campaigns` cap (archived rows don't count).

## Open Questions

- ⏸️ Whether the dedup constraint per (campaign_id, subscriber_id, channel) applies across Automated re-enrolment cycles or only within a single cycle. `(verify)`
- ⏸️ Whether deleting a Segment cascades to the campaigns referencing it, or leaves them orphaned with NULL `segment_id`. `(verify)`
