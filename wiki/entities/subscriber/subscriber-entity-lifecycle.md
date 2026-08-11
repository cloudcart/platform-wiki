---
type: entity
nav_path: "Entity → Subscriber → Lifecycle"
aliases: ["Subscriber lifecycle", "Subscriber states", "Subscriber creation", "Subscriber merge", "Subscriber deletion", "Cascade-delete cleanup", "subscriber.created webhook", "subscriber.updated webhook", "subscriber.deleted webhook", "last_active_at refresh", "Second marketing auto-flip"]
tags: [entity, marketing, subscribers, lifecycle, webhooks]
plan_gates: ["subscribers"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[subscriber]]. See the hub for the other aspects (attributes, channels, consent rules, relationships, API + plan).

# Subscriber — Lifecycle

## Identity

The lifecycle of a [[subscriber|Subscriber]] from creation through eventual deletion or merge — every state the row passes through, the automatic transitions, the `last_active_at` refresh behaviour, the cascade-cleanup on delete, and the webhook events that fire so the merchant's external systems can stay in sync.

## Aliases

- **Subscriber lifecycle** — the canonical name for this aspect.
- **Subscriber states** — the 8-state catalogue.
- **Merge** — folding two Subscribers into one on identifier collision.
- **Cascade-delete** — the cleanup that wipes all of a Subscriber's related marketing records when the Subscriber is hard-deleted.
- **Second-marketing auto-flip** — the merchant-configurable rule that flips Email-channel `marketing` to `no` when checkout consent isn't re-confirmed.
- **`subscriber.created`** / **`subscriber.updated`** / **`subscriber.deleted`** — the three webhook events fired across lifecycle.

## Key Attributes

### The 8 lifecycle states

A Subscriber moves through these states:

1. **Created** — a new row is born. Created automatically (any of 13 sources — popup signup, customer registration, order creation, web push, etc.; see [[subscriber-entity-attributes]]) or manually (merchant creates on [[marketing-subscribers]] / via import / via API). The default channel may have `marketing = yes` (consent box ticked) or `marketing = no` (not ticked).
2. **Active (subscribed on at least one channel)** — at least one SubscriberChannel has `marketing = yes` AND deliverability flags allow sends. The Subscriber appears in campaign reach counts.
3. **Pending verification (Email channel)** — Email channel created with `verified = no`. Merchant sends the verification email (or imports with "Mark all as verified"); on click → `verified = yes`. Most campaigns refuse to send to `verified = no` addresses.
4. **Marketing-suppressed** — Subscriber-row-level `marketing = no` OR all channel-level `marketing = no`. Excluded from marketing sends. May still be tracked for analytics (Web Push opt-in, `last_active_at`, RFM).
5. **Unsubscribed (per channel)** — Subscriber clicked "Unsubscribe" in an email footer or equivalent → THAT channel's `unsubscribed = yes`. Other channels unaffected. Future sends on that channel are skipped silently.
6. **Bounced** — email subsystem detected a hard bounce → channel's `bounced = yes`. Silent drop from future sends.
7. **Merged** — merchant edits a channel identifier to one already used by another Subscriber → merge flow folds the second Subscriber's history (orders, carts, segments, tags, custom fields, events) into the first and deletes the second.
8. **Deleted** — hard delete on [[marketing-subscribers]]. Cascades all child rows (see below). Fires `subscriber.deleted` webhook. Per GDPR right-to-erasure, the platform writes a marketing-log row with the erasure reason but strips PII; the Subscriber-ID reference remains as a no-PII marker.

### Save-time transitions worth noting

- **Source is set at creation, immutable afterwards** — `subscriber_from` records HOW the Subscriber entered the audience. The merchant cannot edit it later. See [[subscriber-entity-attributes]] for the 13 sources.
- **Second-marketing auto-flip** — when the "Second marketing" setting is ON in [[marketing-subscribers]] → Settings, a Subscriber who originally accepted marketing but didn't re-confirm at checkout (when marketing-consent at checkout is not mandatory) automatically has their Email-channel `marketing` flipped to `no`. The reasoning: "if the customer didn't actively re-confirm at purchase, treat that as having changed their mind." The full consent-gate interaction is on [[subscriber-entity-consent-rules]].
- **Linkage with Customer at creation** — when a Customer is created with the same email as an existing Subscriber, the `subscriber_to_customer` link row is created automatically. When an order is created, the same linkage runs. See [[subscriber-entity-relationships]].

### `last_active_at` auto-refresh (storefront-only)

When the Subscriber row is updated **from the storefront context** (i.e. by the visitor's own actions — submitting a popup form, clicking through an email, viewing pages with a tracked identifier), the save automatically overwrites `last_active_at` to "now" in the same save. Updates from the **admin namespace** (merchant editing a Subscriber row from [[marketing-subscribers]]) deliberately SKIP this so a merchant cleanup doesn't make every record look "recently active". This is why the `last_active` segment condition reflects true visitor activity, not merchant maintenance.

### Cascade-delete cleanup

When a Subscriber is hard-deleted, the delete cleanup runs in two phases:

**BEFORE the Subscriber itself is removed**, all of its related marketing records are wiped together:

- Per-action campaign interaction records
- Campaign memberships
- Segment memberships
- Tag assignments
- Tracking-device cookies
- Every subscriber channel
- The Subscriber's tracked events (by subscriber, by customer, and by tracking device)
- Custom-field values
- The Subscriber-to-Customer links

**AFTER the Subscriber is removed**, two follow-ups run:

- The segment membership-change history tied to this Subscriber is cleared.
- Linked Orders and Carts have their `subscriber_id` **nulled** (the Orders and Carts themselves survive, they just lose the marketing attribution).

Finally the platform fires the `subscriber.deleted` webhook to [[settings-hooks]] subscribers.

The destruction of a Subscriber is **total** on the marketing side (all consent rows, events, segment memberships, tags wiped) but **preserves the commerce trail** (orders + carts continue to exist with a null `subscriber_id`). See [[subscriber-entity-relationships]] for the converse — when a Customer is hard-deleted, the linked Subscriber is also deleted.

### Deletion is per-record (not bidirectional with Customer)

Deleting a Subscriber on [[marketing-subscribers]] does NOT delete the linked Customer. For GDPR right-to-erasure, the merchant must delete BOTH records explicitly (or use the Customer-side delete which cascades to the Subscriber — see [[subscriber-entity-relationships]]). The platform writes a marketing-log row with the erasure reason for compliance audit.

### Webhook events fire per-lifecycle event

- `subscriber.created` — new Subscriber created.
- `subscriber.updated` — channel data, marketing consent, tags, or custom fields changed.
- `subscriber.deleted` — Subscriber removed.

Useful for syncing the merchant's external CRM / ESP with CloudCart's audience. Configured on [[settings-hooks]]. Same payloads regardless of WHICH source created / updated / deleted the Subscriber (admin save, popup signup, API write, import row, customer-side cascade all fire the same events).

## Where it appears

- [[marketing-subscribers]] — list, detail, settings (Second marketing rule).
- [[marketing-subscribers]] → Settings — Second marketing on/off, RFM interval.
- [[settings-hooks]] — webhook configuration for `subscriber.created` / `updated` / `deleted`.
- [[customers]] / [[customers-details]] — Customer hard-delete cascades to linked Subscriber.

## Related

- [[subscriber]] — hub.
- [[subscriber-entity-channels]] — Merge flow trigger (identifier-uniqueness collision); per-channel Bounced / Unsubscribed states.
- [[subscriber-entity-consent-rules]] — Second-marketing auto-flip interaction with the two-layer consent gate.
- [[subscriber-entity-relationships]] — Customer cascade-delete and `subscriber_to_customer` linkage.
- [[settings-hooks]] — webhook configuration.
- [[marketing-subscribers]] — list / settings UI.

## Open Questions

None.
