---
type: entity
nav_path: "Entity → Subscriber → Relationships"
aliases: ["Subscriber relationships", "Subscriber to Customer link", "subscriber_to_customer", "Multiple Subscribers per Customer", "Customer hard-delete cascade", "Subscribers tab on Customer", "Subscriber to Segment", "Subscriber UUIDs", "Subscriber events"]
tags: [entity, marketing, subscribers, relationships, customers, segments]
plan_gates: ["subscribers"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[subscriber]]. See the hub for the other aspects (attributes, channels, lifecycle, consent rules, API + plan).

# Subscriber — Relationships

## Identity

How the [[subscriber|Subscriber]] entity connects to other CloudCart records — Customers, Segments, channel rows, tracking UUIDs, events, Orders, Carts — and how those links arise, persist, and clean up. Also the explicit non-relationships: what a Subscriber is **not** (it is not a Customer, not a Customer Group, not a Segment).

## Aliases

- **Subscriber relationships** — the canonical name for this aspect.
- **`subscriber_to_customer`** — the join row that links a Subscriber to a Customer.
- **Subscribers tab** — the Customer-detail tab that lists linked Subscribers.
- **Customer hard-delete cascade** — the Customer-side deletion that also removes the linked Subscriber.

## Key Attributes

### Relationship summary

A Subscriber:

- **Has many** [[subscriber-entity-channels|SubscriberChannel]] rows — one per channel they're reachable on (Email, Phone, WebPush, Messenger). A Subscriber row CAN exist with only one channel.
- **May link to many** [[customer|Customers]] via the `subscriber_to_customer` join — one Subscriber can be linked to multiple Customers (typically when the same email was used across multiple registrations) or none (newsletter-only signups). Reverse: one Customer is linked to at most one Subscriber per channel-identifier.
- **Belongs to many** [[segment|Subscriber Segments]] via a Subscriber-to-segment pivot — segments are rule-based selections of subscribers (e.g., "RFM bucket = Champ"). A Customer with no Subscriber is **invisible to every segment**.
- **Has many** UUIDs — tracking-cookie identifiers from devices the Subscriber has been seen on.
- **Has many** events — every action the platform observed on this Subscriber (page-views, cart-adds, orders, opens, clicks).
- **Has many** custom-field values — defined per-merchant on [[marketing-subscribers-custom-fields]].
- **Has many** Subscriber-specific tags — separate taxonomy from Customer tags (the same word may exist as both a Customer tag and a Subscriber tag without overlap).
- **Has many** campaign-action-logs — per-action interaction records used by analytics and re-targeting.
- **Carries** an RFM-bucket assignment (one of 17 buckets) recomputed on a configurable interval — see [[subscriber-entity-attributes]].
- **Is referenced by** Orders (via `subscriber_id`) and Carts when the email matches at creation time — but the Order is owned by the [[customer|Customer]], not by the Subscriber.

### A Subscriber is NOT the same as

- **[[customer]]** — a Customer is a buyer / registered account. The two records can share an email but live in different sections, count against different plan caps, and have different lifecycles. See [[subscriber-vs-customer]] for the full distinction.
- **[[customer-group]]** — a Customer Group is a loyalty / discount tier on Customers; Subscribers don't have groups.
- **[[segment]]** — a Segment is a rule-based set of Subscribers; one Subscriber can be in many segments dynamically.

### Linkage with Customer at creation

When a Customer is created with the same email as an existing Subscriber, the `subscriber_to_customer` link row is created automatically. When an Order is created, the same linkage runs (if the order email matches a Subscriber). The merchant does not have to manually link the two — the platform pairs them by matching email at lifecycle events.

### Multiple Subscribers per Customer

The **Subscribers tab on [[customers-details|Customer details]]** shows ALL linked Subscriber rows (typically one per channel-identifier collision after merges). The canonical Subscriber for sends is the one with the matching channel-identifier for the requested send channel — there is **no global "primary" Subscriber** per Customer. Different channels can resolve to different linked Subscribers if they were created independently and never merged.

The merchant can use the [[subscriber-entity-channels|Merge subscribers]] flow to consolidate when desired — editing a channel identifier on Subscriber A to an identifier already used by Subscriber B triggers the merge. See [[subscriber-entity-lifecycle]] for the Merged state.

### Customer hard-delete deletes the linked Subscriber too

When a Customer is hard-deleted, the platform fires a follow-up cleanup that finds and **deletes** the linked Subscriber as well (via the `subscriber_to_customer` join AND via matching email on the Subscriber's Email channel). The Subscriber is NOT left as an orphan — the entire row is removed, including all SubscriberChannel rows and child data (see the cascade-delete cleanup on [[subscriber-entity-lifecycle]]).

The **reverse is not symmetric**: deleting a Subscriber does NOT delete the linked Customer. The Customer row survives with its order history intact. The `subscriber_to_customer` link row is removed as part of the Subscriber's cascade-delete; the Customer's overview will then show no Subscriber link.

For full GDPR right-to-erasure, the merchant must delete the **Customer** (which cascades to the Subscriber), or delete both records explicitly.

### Orders / Carts SET NULL on Subscriber delete

When a Subscriber is hard-deleted, every Order and Cart that referenced it via `subscriber_id` has that column **nulled** (SET NULL — Orders and Carts survive intact, they just lose the marketing attribution). This preserves the commerce trail while removing the marketing-side link, which is consistent with the principle "marketing data is right-to-erasure; commerce records have their own retention rules."

### Segments are rule-based and dynamic

Segment membership is **not stored** as a permanent foreign key — segments are queries evaluated against the Subscriber pool on a schedule. When a Subscriber's attribute changes (e.g. RFM bucket recomputes, tag added, channel `marketing` flips), they automatically enter or leave the segments whose rules match. The segments themselves are managed on [[marketing-segments]].

### UUIDs and events

A Subscriber accumulates UUIDs (one per tracked device) and events (page-views, cart-adds, opens, clicks) over time. These drive the `last_active_at` field (see [[subscriber-entity-lifecycle]]), the RFM recomputation (see [[subscriber-entity-attributes]]), the abandoned-cart flow, and segment evaluation. All are wiped in the cascade-delete cleanup.

### Subscribers tab on Customer detail

The Customer overview at [[customers-details-overview]] shows the linked Subscriber's channels alongside the Customer's address / order data — this is the "Customers and Subscribers" surface the merchant uses to see the same email from both perspectives at once. Useful when investigating "I unsubscribed from email but I still got campaign X" tickets.

## Where it appears

- [[customers-details]] / [[customers-details-overview]] — Subscribers tab; the linked-Subscriber summary.
- [[marketing-subscribers]] — list shows the email and basic state; clicking through shows the linked Customer.
- [[marketing-segments]] / [[marketing-segments-subscribers]] — segment membership view.
- [[customer]] — Customer entity; carries the `marketing` flag that participates in the two-layer consent gate.
- [[order]] — Orders reference Subscriber via `subscriber_id`; this field is nulled on Subscriber delete.
- [[cart]] — Carts likewise carry `subscriber_id`.

## Related

- [[subscriber]] — hub.
- [[subscriber-entity-lifecycle]] — cascade-delete details (Subscriber delete cleans up 10 child tables; Customer delete cascades to Subscriber).
- [[subscriber-entity-channels]] — Merge flow for collapsing multiple Subscribers into one.
- [[subscriber-entity-consent-rules]] — most-restrictive rule when linked to multiple Customers.
- [[subscriber-vs-customer]] — the canonical Customer-vs-Subscriber distinction.
- [[customer]] — buyer / registered account.
- [[segment]] — rule-based Subscriber set.
- [[order]] / [[cart]] — commerce records that reference Subscriber via `subscriber_id`.

## Open Questions

None.
