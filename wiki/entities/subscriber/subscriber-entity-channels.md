---
type: entity
nav_path: "Entity → Subscriber → Channels"
aliases: ["SubscriberChannel", "Per-channel subscriber row", "Email channel", "Phone channel", "WebPush channel", "Messenger channel", "Channel identifier", "Default channel", "Merge subscribers flow", "Email verification gate", "Bounced channel", "Unsubscribed channel"]
tags: [entity, marketing, subscribers, channels, deliverability]
plan_gates: ["subscribers"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[subscriber]]. See the hub for the other aspects (attributes, lifecycle, consent rules, relationships, API + plan).

# Subscriber — Channels

## Identity

A **SubscriberChannel** row records how a [[subscriber|Subscriber]] is reachable on one specific channel — Email, Phone (SMS / Viber), Web Push, or Facebook Messenger. Each row carries the channel identifier (email address / phone number / push token / Page-Scoped User ID) and its **own** deliverability state: per-channel marketing consent, verification status, unsubscribed flag, bounced flag. A Subscriber has one channel row per channel they're reachable on; channels behave independently at send time.

## Aliases

- **SubscriberChannel** — the canonical name for the per-channel record.
- **Channel row** — informal name in admin UI.
- **Email channel** / **Phone channel** / **WebPush channel** / **Messenger channel** — the four channel types.
- **Default channel** — the first-created SubscriberChannel; drives list-view display.

## Key Attributes

### Channel types

| Channel | Identifier | Purpose |
|---------|------------|---------|
| **Email** | The email address | Newsletter, marketing email, abandoned-cart email (transactional sends bypass marketing gate). |
| **Phone** | The phone number (E.164 normalised) | SMS marketing, Viber marketing. |
| **WebPush** | A browser push-subscription token | Browser push marketing campaigns. |
| **Messenger** | Facebook Page-Scoped User ID (PSID) | Facebook Messenger marketing. |

### Per-channel fields

Per channel, the merchant edits (Subscriber detail → Channels → row):

| Per-channel field | What it stores | Notes |
|-------------------|----------------|-------|
| **Channel identifier** | The email / phone / PSID itself | Free text (validated per channel type). Uniqueness is enforced — duplicate-identifier collision triggers the merge-subscribers flow. |
| **Marketing consent** (per-channel `marketing`) | yes / no | Per-channel opt-in. Distinct from the Subscriber-row-level marketing flag. Both are checked at send time — see [[subscriber-entity-consent-rules]]. |
| **Verified** | yes / no | Only meaningful for Email. Unverified addresses are excluded from most campaigns unless the channel has `unconfirmed_send` enabled. |
| **Unsubscribed** | yes / no | Set when the subscriber clicks the "Unsubscribe" link in a campaign email footer (or equivalent for other channels). Channel-specific — clicking unsubscribe in an email does NOT unsubscribe from SMS / Viber. |
| **Bounced** | yes / no | Set by the email subsystem on a hard bounce. Bounced channels are silently dropped from future sends. |
| **`identified_at`** | Datetime | When the identifier was first matched to this Subscriber. |

### Per-channel state is independent

A Subscriber CAN be opted-in on Email and opted-out on SMS at the same time (or vice versa). Each SubscriberChannel row has its own `marketing`, `verified`, `unsubscribed`, `bounced`. Clicking "Unsubscribe" in an email footer only flips the Email channel; the Phone channel keeps `marketing = yes` and SMS / Viber sends continue. To fully suppress a person from all marketing, the merchant either:

- Flips every per-channel `marketing` to `no`, OR
- Flips the linked Customer's `marketing` to `no` (cascades to every per-channel `marketing` — see [[subscriber-entity-consent-rules]]), OR
- Deletes the Subscriber row entirely (cascades all channels — see [[subscriber-entity-lifecycle]]).

### Default channel — the first-created row

The first-created channel is the default — the green-check indicator in the list reflects the SubscriberChannel row with the earliest `created_at`. The identifier (email / phone) shown in the [[marketing-subscribers]] list is pulled from this first-created channel. There is **no merchant-facing toggle** to promote a different channel to "default" — the default is determined by creation order and only changes if the original default channel is deleted.

### Channel-identifier uniqueness triggers the merge flow

Editing a channel identifier to one that's already used by another Subscriber surfaces the merge flow with the message: *"This identifier is already in use by another subscriber. Do you want to merge the subscribers?"* The merge folds the second Subscriber's history (orders, carts, segments, tags, custom fields, events) into the first and deletes the second. The merged Subscriber's lifecycle event is documented on [[subscriber-entity-lifecycle]].

Identifier uniqueness is scoped **per channel type** — the same string can appear as an Email identifier on one Subscriber and (theoretically) as a Phone identifier on another, but two Email channels cannot share the same email address.

### Email verification gates sends

When a Subscriber's Email channel has `verified = no`, most campaigns refuse to send. The merchant can verify by:

1. Sending the verification email via the **"Send email with link to verify"** action on the Subscriber detail page.
2. Marking verified on import — the [[customers-import]] / Subscriber CSV import has a **"Mark all as verified"** checkbox.
3. Manually toggling `verified = yes` on the channel edit form.

Unverified addresses show the tooltip: *"No message will be sent to this email because it has not been verified."*

### Phone-number normalisation

Phone-channel identifiers are normalised to E.164 (international format with `+` and country code) before save. A merchant entering `0888123456` for a Bulgarian number is normalised to `+359888123456`. This avoids duplicate-identifier collisions where the same number was entered in two formats.

### Bounced and unsubscribed are silent at send time

A SubscriberChannel with `bounced = yes` or `unsubscribed = yes` is **silently dropped** from future campaign sends on that channel — no error surfaces to the merchant per send. The merchant audits these states via the channel-state column on [[marketing-subscribers]] and the per-channel filters on [[marketing-campaigns-subscribers]] (delivered / bounced / opened / unsubscribed buckets).

## Where it appears

- [[marketing-subscribers]] — list shows the default-channel identifier; channel-state filters (verified, bounced, unsubscribed).
- Subscriber detail page → **Channels** tab — per-channel edit (identifier, marketing, verified, unsubscribed, bounced).
- [[marketing-campaigns]] — campaign-builder picks the target channel; per-channel deliverability is read.
- [[marketing-campaigns-subscribers]] — per-campaign delivery report (delivered, opened, clicked, bounced, unsubscribed) reads channel-state.
- [[marketing-segments]] — segment conditions reference per-channel verification and unsubscribed state.

## Related

- [[subscriber]] — hub.
- [[subscriber-entity-attributes]] — Subscriber-row-level fields (separate from per-channel).
- [[subscriber-entity-consent-rules]] — two-layer consent gate; per-channel independence at send time.
- [[subscriber-entity-lifecycle]] — Merge flow and Bounced / Unsubscribed lifecycle states.
- [[channel]] — channel-type taxonomy.
- [[campaign]] — what a target audience plus per-channel deliverability resolves to.

## Open Questions

None.
