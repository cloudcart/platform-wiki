---
type: concept
nav_path: "Concept → Subscriber vs Customer → Privacy, unsubscribe, deletion"
aliases: ["GDPR subscriber customer", "Right to erasure subscriber customer", "Unsubscribe semantics", "Subscriber delete vs Customer delete", "Customer ban no cascade", "set_on_customer_deleted job"]
tags: [customers, subscribers, marketing, gdpr, privacy, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[subscriber-vs-customer]]. See the hub for the other aspects (records, channels, consent, linkage, plan limits, admin surfaces).

# Subscriber vs Customer — privacy, unsubscribe and deletion

## Definition

Privacy flows on the platform are **channel-specific and record-specific** — the platform deliberately does not cascade between Customer and Subscriber records, because the merchant's legitimate interests on each side may differ (e.g., a banned Customer may still be a lawful marketing recipient if consent predated the ban; conversely, a Subscriber who unsubscribes still has their order history preserved).

Three principles drive the design:

1. **Unsubscribe suppresses ONE channel, not the whole record.** Clicking "unsubscribe" in an email footer flips `unsubscribed = yes` on the Email channel row only. The Customer record is untouched; the Phone / WebPush / Messenger channels are untouched.
2. **Customer delete and Subscriber delete are independent.** Deleting one does not delete the other. The merchant has to delete both for full erasure (GDPR right-to-be-forgotten).
3. **Customer ban does NOT cascade to Subscriber.** Banning a Customer stops them from logging in / ordering but leaves their marketing reach intact unless the merchant explicitly stops it.

## Scope

Covered:

- Unsubscribe semantics — channel-specific, transactional bypasses still work.
- Customer hard-delete — cascades to cart rows; the join-row cleanup is asynchronous via the subscribers queue.
- Subscriber hard-delete — cascades all channels, UUIDs, segments, events, custom fields, campaign action logs.
- Customer ban — does not cascade to the Subscriber.
- The GDPR right-to-erasure flow (delete both sides).
- The webhook events that fire on each side independently.

Not covered:

- The two-layer consent gate that decides reach before a send — see [[subscriber-vs-customer-consent]].
- Per-channel deliverability flag semantics — see [[subscriber-vs-customer-channels]].
- Plan-cap independence — see [[subscriber-vs-customer-limits]].

## Contrasts

- **Unsubscribe vs delete** — unsubscribe blocks future marketing on one channel; delete removes the record entirely. Unsubscribed Subscribers still count toward the `subscribers` plan limit; deleted Subscribers don't.
- **Customer delete vs Subscriber delete** — both must run for GDPR right-to-erasure. Each fires its own webhook (`customer.deleted`, `subscriber.deleted`).
- **Customer ban vs Customer delete** — ban stops login + ordering but keeps the record; delete removes the record. Neither cascades to the Subscriber.
- **Marketing send vs transactional send** — unsubscribe / Customer-level `marketing = no` block marketing only. Transactional sends (order confirmation, password reset, refund notification) bypass the gate and keep flowing.

## Where it applies

### Unsubscribe — channel-specific suppression

When a recipient interacts with marketing they received from CloudCart:

- **Clicks "Unsubscribe" in an email footer** → Email-channel `unsubscribed = yes`. Customer record untouched. Other channels (Phone, WebPush, Messenger) untouched. Future Email campaigns skip this Subscriber. Order-confirmation emails still go through (transactional sends bypass marketing flags — see [[subscriber-vs-customer-consent]]).
- **Hits the Web Push "block this site" browser dialog** → WebPush-channel `unsubscribed = yes`. Email keeps working.
- **Phones in and asks the merchant to remove all marketing** → the merchant uses [[marketing-subscribers]] bulk-decline-marketing, OR opens the Subscriber and toggles every channel's `marketing = no`, OR opens the Customer and toggles Customer-level `marketing = no` (which cascades to per-channel `no` via the consent propagation rule).

### Subscriber hard-delete

Deleting a Subscriber on [[marketing-subscribers]] cascade-cleans:

- All `SubscriberChannel` rows for this Subscriber.
- Tracking UUIDs.
- Segment memberships.
- Subscriber events (behaviour history).
- Subscriber custom-field values.
- Campaign action logs (opens, clicks, bounces — for this Subscriber).
- The `subscriber_to_customer` join rows for this Subscriber.

The linked Customer is **NOT** deleted. The Customer keeps their order history, login, lifetime revenue. They simply no longer have a marketing reach until a new Subscriber is created (e.g., re-subscribing via a popup).

A `subscriber.deleted` webhook fires.

### Customer hard-delete — join-row cleanup is async

Hard-deleting a Customer on [[customers]] cascades cart rows but NOT orders (orders survive because hard-deleting a Customer with order history is protected by an "empty customer" check — to delete a Customer with orders, the orders themselves must be deleted or anonymised first).

The Subscriber-side `subscriber_to_customer` join row is **NOT** cleaned up synchronously. The platform queues a background job on the **subscribers queue** (the canonical handler is `set_on_customer_deleted` (verify)) that cleans up the join so the Subscriber no longer points to a non-existent Customer. The cleanup is asynchronous (queued), so there is a brief window after the deletion during which the Subscriber may still appear linked to the deleted Customer.

The Subscriber itself is **NOT** auto-deleted — it remains as an independent marketing record (with its `unsubscribed`, `marketing`, channel data intact). The merchant who wants to fully erase the person must delete the Subscriber separately.

A `customer.deleted` webhook fires.

### Customer ban — no cascade to Subscriber

Banning a Customer via [[customers-details]] sets `banned = yes`, `date_banned`, and `banned_reason` on the Customer row. The Customer can no longer log in or place orders. **The linked Subscriber row is NOT touched** — there is no automatic ban → subscriber-unsubscribe cascade.

The merchant who wants to also stop marketing emails to a banned customer must separately unsubscribe / delete the linked Subscriber on [[marketing-subscribers]]. This is by design: a Customer banned for fraudulent orders may still be a legitimate marketing recipient on the brand's mailing list, especially if the email was originally captured before the ban.

### GDPR right-to-erasure — full deletion requires both sides

When a person exercises a right-to-erasure request:

1. The merchant deletes the **Subscriber** via [[marketing-subscribers]] (cascade-cleans channels, UUIDs, segments, events, custom fields, campaign action logs).
2. The merchant separately deletes the **Customer** via [[customers]] (cascade-cleans carts; orders need to be deleted or anonymised first).
3. Both deletes fire their own webhook events (`subscriber.deleted`, `customer.deleted`).

The platform does NOT chain the two deletes. The merchant has to do both if total erasure is the goal. A common workflow guide for support tickets: ALWAYS check both screens.

### Same email, two records, deletable independently — example

If `john@example.com` is both a Customer and a Subscriber:

- Deleting `john@example.com` on [[customers]] (Customer delete) → Customer row deleted, cart rows cascade-deleted, `customer.deleted` webhook fires. **The Subscriber row remains** — John can still receive marketing.
- Deleting `john@example.com` on [[marketing-subscribers]] (Subscriber delete) → Subscriber + all channels + UUIDs + segments + events deleted, `subscriber.deleted` webhook fires. **The Customer row remains** — John's order history is preserved, John can still log in.

Both deletes are necessary for full erasure. The platform does not chain them.

### Webhook events fire independently

[[settings-hooks]] exposes the `customer.*` and `subscriber.*` event families separately:

- `customer.created`, `customer.updated`, `customer.deleted` — fire on Customer-side mutations.
- `subscriber.created`, `subscriber.updated`, `subscriber.deleted` — fire on Subscriber-side mutations.

When integrating with an external CRM / ESP, the common pattern is to subscribe to BOTH families. A consent change made on the Customer side cascades to the per-channel `marketing` on the Subscriber side (see [[subscriber-vs-customer-consent]]), and the external system needs to receive both `customer.updated` and `subscriber.updated` to keep its mirror coherent.

## Related

- [[subscriber-vs-customer]] — hub.
- [[subscriber-vs-customer-consent]] — the gate that interacts with `unsubscribed`, `marketing` flags.
- [[subscriber-vs-customer-channels]] — the per-channel flag layer.
- [[subscriber-vs-customer-linkage]] — the join row that gets asynchronously cleaned on Customer delete.
- [[customers-details]] — Customer-side detail; ban / delete actions.
- [[customers]] — Customer list; bulk delete.
- [[marketing-subscribers]] — Subscriber list; bulk delete + per-channel toggles.
- [[settings-hooks]] — `customer.*` and `subscriber.*` webhook families.

## Open Questions

- Is the background job for `subscriber_to_customer` cleanup actually named `set_on_customer_deleted`, or is that a different handler? (verify)
