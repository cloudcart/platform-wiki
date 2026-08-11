---
type: entity
nav_path: "Entity → Marketing Campaign → Consent gating"
aliases: ["Campaign consent", "Two-layer consent", "Anti-spam policy gate", "Banned campaign", "banned_reason", "Auto-bounce auto-unsubscribe", "Auto-verify on engagement", "Channel availability gate", "Съгласие на абоната", "Анти-спам политика"]
tags: [entity, marketing, campaigns, consent, anti-spam, deliverability]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[campaign]]. See the hub for the other aspects (types, attributes schema, lifecycle, relationships, attribution & statistics).

# Campaign — Consent gating

## Identity

Every campaign dispatch is gated by a chain of consent and policy checks before a single message goes out. The chain has four layers:

1. **Anti-spam policy acceptance** at the store level (one-time, before first send).
2. **Channel availability** — the channel for the action must be installed and verified.
3. **Two-layer subscriber consent** — Customer-level marketing flag + per-channel marketing flag, both required.
4. **Channel-level banned state** — the campaign's channels must not be suspended for spam / abuse.

Any of these failing suppresses the send (silently per-recipient or visibly per-campaign). The merchant sees the policy / channel / banned-state gates in the editor; the per-recipient consent gates are surfaced in the per-action delivery log.

## Aliases

- **Policy** = the platform's anti-spam acceptance gating first send.
- **Two-layer consent** = Customer-level `marketing` flag + per-channel `subscriber_channels.marketing` flag.
- **Banned** = the campaign's channel was suspended for spam complaints or abuse.
- **Verified** = `subscriber_channels.verified = 1`, set explicitly via double-opt-in OR implicitly via open / click engagement.
- **Bounced** = `subscriber_channels.bounced = 1` after hard-bounce; suppresses future sends.

## Key Attributes

### The four-layer gate

| Layer | Where it lives | Failure mode |
|-------|----------------|--------------|
| Anti-spam policy | Store-level, accepted once on [[marketing-campaigns-policy]] | Campaign cannot be created / activated until accepted. |
| Channel availability | [[marketing-channels]] — each channel must be installed + verified | Editor blocks activation for an action whose channel is missing. Campaign can stay Draft. |
| Customer-level consent | `customer.marketing = yes` when the subscriber is also a customer | Suppresses send for that recipient (logged in the per-recipient log). |
| Per-channel subscriber consent | `subscriber_channels.marketing = 1` per channel | Suppresses send on that channel for that recipient. |
| Channel banned state | Per-channel `banned_reason` getter | "Banned" indicator surfaces on the campaign; activation disabled. |

### Auto-bounce / auto-unsubscribe (verified against backend)

When a recipient's email hard-bounces, errors, or files an abuse report, the platform automatically:

1. Marks the `subscriber_channels` row as `bounced = 1` (preventing future sends to that email).
2. Removes the subscriber from the current campaign via `triggerRemove({earlyExit: true, rejectsMarketing: true})` — pulling them out of the funnel AND flipping their per-channel marketing-acceptance to false.
3. Logs the removal reason (`'abuse'`, `'hard_bounced'`, `'error'`) so the merchant can see WHY in the removal log.

So a single bad email automatically suppresses future sends to that recipient AND exits them from the campaign. The merchant doesn't have to manually clean their list. See [[marketing-campaigns-statistics-log]].

### Auto-verify on engagement (verified against backend)

When a recipient opens (SEEN) or clicks (CLICKED), the platform sets `subscriber_channels.verified = 1` automatically. So engaged-with channels are treated as verified addresses without an explicit double-opt-in — the click / open IS the verification signal.

## Where it appears

- [[marketing-campaigns-policy]] — the anti-spam acceptance screen. **The policy is per-store, not per-campaign** — once accepted, every campaign the store creates inherits the acceptance. There is no per-campaign "did this campaign accept the policy" flag.
- [[marketing-channels]] — the channel installation + verification screens. At least one channel must be installed and verified for a campaign to send on that channel.
- [[marketing-channels-email]] — Email channel configuration including DKIM / SPF / DMARC and sender domain.
- [[marketing-subscribers]] — per-subscriber consent flags (Customer-level `marketing` + per-channel `marketing` + per-channel `verified` + per-channel `bounced`).
- [[marketing-campaigns-statistics-log]] — the per-recipient delivery log with removal reasons.
- [[marketing-campaigns-banned-info]] — the channel-banned info surface where the merchant sees the reason a channel (and therefore the campaigns using it) is currently suspended.
- [[campaign-entity-lifecycle]] — for how a banned campaign blocks activation and what resolution looks like.

### Two-layer consent — the order of checks

For each (subscriber, channel) pair the platform checks:

1. The subscriber's **Customer-level** marketing consent (if the subscriber is also a customer, `customer.marketing = yes`).
2. The subscriber's **per-channel** marketing consent (Email channel `marketing = 1`, SMS channel `marketing = 1`, etc.).

Either gate failing suppresses the send on that channel for that subscriber. See [[notification-delivery]] for the full delivery pipeline.

This means a subscriber who is also a customer has TWO independent unsubscribe surfaces:

- Customer profile → marketing toggle (kills all marketing across all channels)
- Per-channel preferences → individual channel toggle (kills only that channel)

### The `banned_reason` is computed from channels, not stored (verified against backend)

The merchant sees a "banned" indicator on a campaign when the campaign's referenced channel is suspended (e.g., Email channel's spam complaint rate crossed the 50% threshold). The reason is computed on-the-fly by walking the campaign's actions, resolving each action's channel, and checking that channel's `banned_reason` getter — see [[marketing-campaigns-banned-info]]. The campaign row itself doesn't carry a per-campaign banned flag; "banned" is a transient property of the channels it uses.

This means: a campaign can become "banned" without any change to its own row — the merchant only needs to fix the underlying channel's deliverability problem to clear the ban.

### Anti-spam policy gate — one-time per store

Before the merchant's FIRST campaign can be sent, the merchant must accept the platform's [[marketing-campaigns-policy|anti-spam policy]]. The policy requires confirming the sender controls the recipient list (no purchased lists, no scraping), the unsubscribe link works, the from-name is identifiable, etc.

After acceptance, campaigns are sendable; the platform reserves the right to ban specific campaigns retroactively if abuse is detected. A banned campaign cannot send until the merchant resolves the flagged issue.

## Related

- [[campaign]] — hub.
- [[campaign-entity-lifecycle]] — Banned state semantics and how it blocks activation.
- [[campaign-entity-relationships]] — subscriber pivot and channel-availability gate.
- [[campaign-entity-attribution-statistics]] — what counts as a delivery vs a suppression in the per-recipient log.
- [[subscriber]] — the recipient entity; carries the per-channel consent flags.
- [[customer]] — the Customer-level `marketing` flag (first consent gate).
- [[notification-delivery]] — the cross-cutting two-layer consent concept used across all merchant-driven messaging.
- [[subscriber-vs-customer]] — clarifies the dual-identity overlap that makes the two-layer model necessary.
- [[marketing-campaigns-policy]] — anti-spam policy acceptance screen.
- [[marketing-channels]] — channel installation + verification.
- [[marketing-channels-email]] — DKIM / SPF / DMARC + sender domain.
- [[marketing-campaigns-banned-info]] — channel-level banned reason source.
- [[marketing-subscribers]] — subscriber consent management.
- [[marketing-campaigns-statistics-log]] — per-recipient removal log.

## Open Questions

- ⏸️ Whether a banned campaign that the merchant then resolves and re-activates resumes from where it stopped or restarts the funnel for in-progress subscribers. `(verify)`
- ⏸️ Whether `subscriber_channels.verified = 1` set via open / click counts the same as DOI-verified for deliverability heuristics. `(verify)`
