---
type: entity
nav_path: "Entity → Subscriber → Consent rules"
aliases: ["Subscriber consent rules", "Two-layer consent", "Marketing consent gate", "Per-channel consent", "Second marketing rule", "GDPR marketing_policy precedence", "Customer marketing one-way sync", "Most-restrictive rule", "Place an order does not auto-subscribe"]
tags: [entity, marketing, subscribers, consent, gdpr, compliance]
plan_gates: ["subscribers"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[subscriber]]. See the hub for the other aspects (attributes, channels, lifecycle, relationships, API + plan).

# Subscriber — Consent rules

## Identity

How marketing consent is captured, stored, and **enforced at send time** for a [[subscriber|Subscriber]]. CloudCart uses a **two-layer consent model**: a Customer-level marketing flag (when the Subscriber is linked to a [[customer|Customer]]) AND a per-channel marketing flag (on each [[subscriber-entity-channels|SubscriberChannel]] row). Both must allow delivery — any one failing means no send. This page is the canonical reference for "why didn't this campaign reach this person?" support tickets.

## Aliases

- **Two-layer consent gate** — the principle that BOTH Customer-level AND per-channel marketing flags must be `yes`.
- **Per-channel consent independence** — Email opt-in does NOT mean SMS opt-in.
- **Second-marketing rule** — the auto-flip at checkout when consent isn't re-confirmed.
- **Most-restrictive rule** — when a Subscriber is linked to multiple Customers, the most-restrictive Customer wins.
- **GDPR precedence** — the storefront `marketing_policy` checkbox at checkout overrides admin-side bulk-flips on the next purchase.
- **Customer → Subscriber one-way sync** — opt-outs propagate to per-channel; opt-ins do NOT auto-flip back.

## Key Attributes

### Two layers of marketing consent

A marketing send (campaign) is gated by **both** layers:

1. **Customer-level `marketing`** (when linked to a Customer) — single yes/no on the [[customer|Customer]] record. When `no`, the Subscriber is excluded from ALL marketing campaigns regardless of per-channel state.
2. **SubscriberChannel-level `marketing`** (per channel row) — when `no` on a channel, the Subscriber is excluded from campaigns on THAT channel even if Customer-level is `yes`.

So a "deliverable" Subscriber on Email needs **all** of:

- Customer `marketing = yes` (if the Subscriber is linked to a Customer)
- Email-channel `marketing = yes`
- Email-channel `verified = yes`
- Email-channel `unsubscribed = no`
- Email-channel `bounced = no`

Any one failing → no send. Bounced and unsubscribed sends are dropped **silently** — no error to the merchant per send.

### Per-channel state is independent

A Subscriber CAN be opted-in on Email and opted-out on SMS at the same time (or vice versa). Each SubscriberChannel row has its own `marketing`, `verified`, `unsubscribed`, `bounced`. Clicking "Unsubscribe" in an email footer only flips the Email channel; the Phone channel keeps `marketing = yes` and SMS / Viber sends continue. To fully suppress a person from all marketing, the merchant either:

- Flips every per-channel `marketing` to `no`, OR
- Flips the linked Customer's `marketing` to `no` (cascades — see below), OR
- Deletes the Subscriber row (cascades all channels — see [[subscriber-entity-lifecycle]]).

### "Place an order" does NOT auto-subscribe

The platform DOES auto-create a Subscriber row when a Customer registers or places an order — but the Email-channel `marketing` defaults to **`no`** unless the consent box was explicitly ticked. A store with mostly guest orders and a quiet "accept marketing" box can have thousands of Customers and only a few Subscribers. This is by design and reflects the GDPR principle: silence is not consent.

### Customer marketing flag → Subscriber sync is one-way safe

When the linked Customer's `marketing` flips **`yes` → `no`**, every linked Subscriber's per-channel `marketing` flips to `no` too (bidirectional propagation of opt-outs).

The **reverse** — Customer `marketing` flips `no → yes` — does **NOT** auto-flip the per-channel flag back to `yes`. The merchant must manually re-enable per-channel to avoid accidental re-opt-in. This conservative design honours the most-recent explicit opt-out and prevents an accidental admin toggle from reactivating channels the customer previously opted out of.

### Most-restrictive rule when a Subscriber links to multiple Customers

When a Subscriber is linked to multiple Customers (same email registered multiple times), the marketing send is gated by the **most restrictive** Customer's flag — if ANY linked Customer has `marketing = no`, the Subscriber is excluded from sends. This conservative interpretation honours the most-recent opt-out across the linked-Customer set. See [[subscriber-entity-relationships]] for how multi-Customer linkage arises.

### Second-marketing auto-flip

When the **"Second marketing"** setting is ON in [[marketing-subscribers]] → Settings, a Subscriber who originally accepted marketing but **didn't re-confirm at checkout** (when marketing-consent at checkout is not mandatory) automatically has their Email-channel `marketing` flipped to `no`. The reasoning: "if the customer didn't actively re-confirm at purchase, treat that as having changed their mind."

Effect: after the order saves, the Subscriber stops appearing in future campaigns unless re-opted-in via a popup, an admin bulk-flip, or a new explicit consent capture. Some merchants run this rule permanently for aggressive list hygiene; others leave it off because they regard the original opt-in as durable until explicit unsubscribe.

### GDPR `marketing_policy` precedence

The merchant-facing GDPR `marketing_policy` (mandatory checkbox at checkout — configured on [[settings-general]]) takes **precedence** over per-channel overrides at the storefront. When GDPR mandates explicit consent at checkout, the per-channel `marketing` flag is set based on the checkout checkbox. Admin-side bulk-flips can still set per-channel `marketing`, but the storefront re-confirmation **re-applies the customer's choice on their next purchase**.

Practical consequence: a merchant who bulk-flips a population to `marketing = yes` will find those flags **reverting** the next time those customers check out without ticking the marketing box. The customer's checkout choice is the source of truth in GDPR-mandated mode.

### Email verification gates sends

When a Subscriber's Email channel has `verified = no`, most campaigns refuse to send — even if every consent flag is `yes`. Verification is a separate gate from consent. See [[subscriber-entity-channels]] for the three verification paths (verification email, "Mark all as verified" on import, manual toggle).

### Webhook receivers must respect the same gate

External CRM / ESP integrations syncing via `subscriber.created` / `subscriber.updated` ([[settings-hooks]]) receive the full per-channel marketing state. **Receivers must respect the two-layer rule themselves** when re-sending — a downstream ESP that only checks per-channel `marketing` will violate consent for Subscribers whose linked Customer has `marketing = no`. The CloudCart-internal sends (campaigns, abandoned-cart, transactional) apply the two-layer gate automatically; third-party sends are the merchant's responsibility.

## Where it appears

- [[marketing-campaigns]] — every campaign send applies the two-layer gate before queueing.
- [[marketing-campaigns-subscribers]] — per-campaign delivery report shows the gating outcome (delivered / suppressed / bounced / unsubscribed).
- [[marketing-subscribers]] → Settings — Second-marketing rule toggle.
- [[settings-general]] — GDPR `marketing_policy` configuration.
- [[checkout-flow]] — where the marketing-consent checkbox at checkout sets per-channel `marketing` for the order's Subscriber.
- [[abandoned-cart-recovery]] — the abandoned-cart email also applies the two-layer gate.

## Related

- [[subscriber]] — hub.
- [[subscriber-entity-channels]] — per-channel state (the second layer).
- [[subscriber-entity-attributes]] — Subscriber-row `marketing` flag and `gdpr_accepted`.
- [[subscriber-entity-relationships]] — multi-Customer linkage that triggers the most-restrictive rule.
- [[subscriber-entity-lifecycle]] — Second-marketing auto-flip as a save-time transition.
- [[subscriber-vs-customer]] — the canonical Customer-vs-Subscriber distinction.
- [[notification-delivery]] — the platform-wide consent / deliverability check applied at send time.
- [[checkout-flow]] — checkout consent capture.
- [[settings-general]] — GDPR `marketing_policy` setting.

## Open Questions

None.
