---
type: concept
nav_path: "Concept → Subscriber vs Customer → Consent gate"
aliases: ["Two-layer marketing consent", "Customer marketing flag", "Per-channel marketing flag", "Second marketing rule", "Marketing-flag propagation", "OnMarketingChange cascade"]
tags: [customers, subscribers, marketing, consent, gdpr, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[subscriber-vs-customer]]. See the hub for the other aspects (records, channels, linkage, privacy, plan limits, admin surfaces).

# Subscriber vs Customer — the two-layer consent gate

## Definition

Marketing sends are gated by **two independent consent flags** the platform checks before dispatching anything to a recipient:

1. **Customer-level `marketing` flag** — a single yes/no on the Customer record. Set from the storefront (Account preferences) or by the merchant on [[customers-details]]. When `no`, the Customer is excluded from **ALL** marketing campaigns regardless of any per-channel state.
2. **SubscriberChannel-level `marketing` flag** — a yes/no per channel row (one for Email, one for Phone, one for Web Push, one for Messenger). When `no` on a channel, the Subscriber is excluded from campaigns **on that specific channel** even if the Customer-level flag is `yes`.

Both layers must allow delivery. A send is gated by the **AND** of the two. So a Subscriber whose Email channel has `marketing = yes` but whose linked Customer has `marketing = no` will NOT receive the email — the Customer-level flag overrides.

Then the platform layers the per-channel deliverability flags (`verified`, `unsubscribed`, `bounced`) on top — see [[subscriber-vs-customer-channels]]. The full eligibility predicate for an Email send is:

```
Customer.marketing = yes
AND SubscriberChannel(Email).marketing = yes
AND SubscriberChannel(Email).verified = yes
AND SubscriberChannel(Email).unsubscribed = no
AND SubscriberChannel(Email).bounced = no
```

Two layers exist because the merchant runs storefronts where marketing consent is sometimes mandatory and sometimes optional, and the platform needs to encode both "person-level intent" (Customer flag) and "channel-level intent" (per-channel flag) separately.

## Scope

Covered:

- The two consent flags and the AND gate.
- Marketing sends vs transactional sends — only marketing is gated.
- The **Second marketing** auto-reset rule.
- Marketing-flag propagation when bulk-toggled (Subscriber-side) or when the Customer-side flips.
- The asymmetry: opt-OUT cascades from Customer to all channels; opt-IN does NOT auto-cascade back.

Not covered:

- Per-channel deliverability flags beyond `marketing` — see [[subscriber-vs-customer-channels]].
- Unsubscribe / GDPR semantics — see [[subscriber-vs-customer-privacy]].
- How the consent box on checkout maps to record creation — see [[subscriber-vs-customer-records]].

## Contrasts

- **Customer-level `marketing` vs per-channel `marketing`** — Customer-level is the master switch covering all channels; per-channel is the fine-grained per-transport switch. The AND of the two gates the send.
- **Marketing send vs transactional send** — the two-layer consent gates **marketing** sends only. **Transactional** sends — order confirmation, password reset, refund notification, back-in-stock alerts the customer explicitly asked for — bypass the marketing flags. Suppressing marketing for a Customer / Subscriber does NOT block their order confirmation emails.
- **Opt-out cascade vs opt-in cascade** — opt-out from Customer-level cascades to per-channel `marketing = no` automatically. Opt-in from Customer-level does NOT automatically flip per-channel back to `yes` — each channel must be opted in explicitly.

## Where it applies

### Marketing send vs transactional send

The two-layer gate applies to **marketing** sends only. Transactional traffic — order confirmation, payment receipts, password reset, account-creation welcome, "Notify me when in stock" alerts the customer subscribed to — bypasses both flags. The merchant can disable marketing for a banned / unhappy customer without breaking their order-confirmation flow.

The platform's [[notification-delivery]] layer is where the gate is applied. The same notification template can be sent transactionally (one-off, system-triggered) or as a campaign (marketing broadcast). Only the campaign path goes through the consent gate.

### The "Second marketing" rule — auto-reset on checkout

There's a setting on [[marketing-subscribers]] → Settings called **"Second marketing"** that captures an edge case:

> *"If a subscriber has accepted marketing and has not marked it when ordering (if it is not mandatory) to be marked as 'Does not accept marketing'."*

When this is ON, a Subscriber who:

1. Originally accepted marketing on signup (Email channel `marketing = yes`),
2. Then placed an order on a storefront where marketing-consent at checkout is **not** mandatory, AND
3. Did **not** re-tick the box at checkout,

— automatically has their Email-channel `marketing` flipped back to `no`. The merchant chose this behaviour: "if the customer didn't actively re-confirm at purchase, treat that as having changed their mind." This is one common reason why the Subscriber count can drop after a wave of orders.

### Marketing-flag propagation — both directions, but asymmetric

When the merchant bulk-toggles marketing on [[marketing-subscribers]]:

1. Every per-channel `marketing` flag is updated.
2. Every linked Customer's `marketing` flag is updated **to match**.
3. A marketing-change log entry is written recording the admin who made the change (`initiator = { key: 'sitecp', admin: <admin attrs> }`).
4. A background task re-evaluates all segments for the affected ids.

The reverse propagation runs when the **Customer-side `marketing` flips `yes → no`** from any source (Customer account preferences on storefront, [[customers-details]] toggle, bulk edit on [[customers]], JSON-API write): the platform's marketing-change cascade flips **every linked Subscriber's per-channel `marketing` to `no`** (one-way OPT-OUT propagation).

The asymmetry matters:

- **Opt-OUT cascades** from Customer-level down to every channel.
- **Opt-IN does NOT cascade.** When the Customer flips `no → yes`, per-channel rows stay at `no`. Each channel must be opted in explicitly (by the customer ticking a channel-specific consent on the storefront, by a subscribe-form re-submission, or by the merchant manually).

This is by design — opting back in on the Customer side is interpreted as "willing to receive again", but consent for a specific channel (e.g., SMS) is a separate decision the platform doesn't presume.

### What flips the Customer-level `marketing` flag

- Storefront Account → preferences toggle by the customer.
- [[customers-details]] toggle by the merchant.
- Bulk-edit on the Customer list ([[customers]]).
- JSON-API v2 PATCH on the Customer resource.
- The cascade from a Subscriber-side bulk toggle (see above).
- Auto-tick at checkout / registration when the consent box is ticked.

### What flips the per-channel `marketing` flag

- The checkout / signup consent box (sets Email-channel `marketing = yes/no` at record creation).
- The recipient clicking "unsubscribe" in an email footer (sets Email-channel `unsubscribed = yes`, which functionally blocks even though `marketing` may still be `yes`).
- The merchant bulk-toggling on [[marketing-subscribers]].
- The Subscriber detail screen per-channel toggle.
- The **Second marketing** auto-reset described above.
- The Customer-side opt-OUT cascade.
- A re-subscribe via a subscribe form (re-confirms `marketing = yes` and `verified = yes`).

## Related

- [[subscriber-vs-customer]] — hub.
- [[subscriber-vs-customer-channels]] — the per-channel deliverability flags this gate sits on top of.
- [[subscriber-vs-customer-privacy]] — unsubscribe and GDPR semantics that interact with the gate.
- [[subscriber-vs-customer-records]] — how the checkout consent box maps to the initial flag values.
- [[notification-delivery]] — the layer that applies the gate before dispatching marketing.
- [[marketing-subscribers]] — Subscribers list + the **Second marketing** setting.
- [[customers-details]] — Customer-side marketing toggle.
- [[customers]] — bulk-edit Customer-side `marketing`.
- [[marketing-campaigns]] — broadcasts; subject to the gate.

## Open Questions

None.
