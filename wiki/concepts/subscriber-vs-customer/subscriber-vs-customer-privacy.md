---
type: concept
nav_path: "Concept → Subscriber vs Customer → Privacy, unsubscribe, deletion"
aliases: ["GDPR subscriber customer", "Right to erasure subscriber customer", "Unsubscribe semantics", "Subscriber delete vs Customer delete", "Customer ban no cascade", "set_on_customer_deleted job"]
tags: [customers, subscribers, marketing, gdpr, privacy, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-11-09
source_count: 5
---

> Part of [[subscriber-vs-customer]]. See the hub for the other aspects (records, channels, consent, linkage, plan limits, admin surfaces).

# Subscriber vs Customer — privacy, unsubscribe and deletion

## Definition

Privacy flows on the platform are **channel-specific and record-specific**. The one cascade between the two records is deletion of a Customer, which also deletes the linked Subscriber; unsubscribe and ban stay on their own side (a banned Customer may still be a lawful marketing recipient; a Subscriber who unsubscribes keeps their order history).

Three principles drive the design:

1. **Unsubscribe suppresses ONE channel, not the whole record.** Clicking "unsubscribe" in an email footer flips `unsubscribed = yes` on the Email channel row only. The Customer record is untouched; the Phone / WebPush / Messenger channels are untouched.
2. **Customer delete removes the Subscriber; Subscriber delete leaves the Customer.** Deleting a Customer queues a background job that deletes every Subscriber linked to that Customer or holding the same address on an Email channel.
3. **Customer ban does NOT cascade to Subscriber.** Banning a Customer stops them from logging in / ordering but leaves their marketing reach intact unless the merchant explicitly stops it.

## Scope

Covered:

- Unsubscribe semantics — channel-specific, transactional bypasses still work.
- Customer hard-delete — cascades to cart rows and, through a queued job, to the linked Subscriber(s).
- Subscriber hard-delete — cascades all channels, UUIDs, segments, events, custom fields, campaign action logs.
- Customer ban — does not cascade to the Subscriber.
- The GDPR right-to-erasure flow (deleting the Customer covers both).
- The webhook events that fire on each side independently.

Not covered:

- The two-layer consent gate that decides reach before a send — see [[subscriber-vs-customer-consent]].
- Per-channel deliverability flag semantics — see [[subscriber-vs-customer-channels]].
- Plan-cap independence — see [[subscriber-vs-customer-limits]].

## Contrasts

- **Unsubscribe vs delete** — unsubscribe blocks future marketing on one channel; delete removes the record entirely. Unsubscribed Subscribers still count toward the `subscribers` plan limit; deleted Subscribers don't.
- **Customer delete vs Subscriber delete** — the first also deletes the linked Subscriber; the second leaves the Customer. Each fires its own webhook (`customer.deleted`, `subscriber.deleted`).
- **Customer ban vs Customer delete** — ban stops login + ordering and leaves the Subscriber alone; delete removes the record and the linked Subscriber.
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
- The `subscriber_to_customer` join rows and segment log rows for this Subscriber; its orders and carts lose the reference to it.

The linked Customer is **NOT** deleted. The Customer keeps their order history, login, lifetime revenue. They simply no longer have a marketing reach until a new Subscriber is created (e.g., re-subscribing via a popup).

A `subscriber.deleted` webhook fires.

### Customer hard-delete — the linked Subscriber goes too

Hard-deleting a Customer on [[customers]] (single or bulk) deletes their cart rows but NOT their orders: each order keeps its own copy of the customer's name and email, so it survives the deletion. Nothing stops deleting a Customer who has orders.

Shortly after, a background job (`set_on_customer_deleted`) **deletes every Subscriber** linked to that Customer, and any Subscriber whose Email channel holds the Customer's email — with the full Subscriber cascade above and a `subscriber.deleted` webhook each. Until the job runs, the Subscriber is still visible. If the same person later logs in, orders or registers, a new Subscriber is created. Campaign statistics are not part of either cascade, so campaign totals keep counting the deleted subscriber (verify).

A `customer.deleted` webhook fires.

### Customer ban — no cascade to Subscriber

Banning a Customer via [[customers-details]] sets `banned = yes`, `date_banned`, and `banned_reason` on the Customer row. The Customer can no longer log in or place orders. **The linked Subscriber row is NOT touched** — there is no automatic ban → subscriber-unsubscribe cascade.

The merchant who wants to also stop marketing emails to a banned customer must separately unsubscribe / delete the linked Subscriber on [[marketing-subscribers]]. This is by design: a Customer banned for fraudulent orders may still be a legitimate marketing recipient on the brand's mailing list, especially if the email was originally captured before the ban.

### GDPR right-to-erasure — delete the Customer

The GDPR app only records erasure requests; it erases nothing by itself. The merchant acts on the request:

1. Delete the **Customer** via [[customers]] — this removes their carts and, through the queued job, their Subscriber(s). Their orders stay, with the customer's details copied on them.
2. A person who is only a Subscriber (form sign-up, no account or order) is deleted on [[marketing-subscribers]].
3. Each delete fires its own webhook (`customer.deleted`, `subscriber.deleted`).

Example: `john@example.com` is both a Customer and a Subscriber. Deleting him on [[customers]] removes the Customer and, shortly after, the Subscriber. Deleting only the Subscriber on [[marketing-subscribers]] leaves the Customer, his orders and his login.

### Webhook events fire independently

[[settings-hooks]] exposes the `customer.*` and `subscriber.*` event families separately:

- `customer.created`, `customer.updated`, `customer.deleted` — fire on Customer-side mutations.
- `subscriber.created`, `subscriber.updated`, `subscriber.deleted` — fire on Subscriber-side mutations.

When integrating with an external CRM / ESP, the common pattern is to subscribe to BOTH families. A consent change made on the Customer side cascades to the per-channel `marketing` on the Subscriber side (see [[subscriber-vs-customer-consent]]), and the external system needs to receive both `customer.updated` and `subscriber.updated` to keep its mirror coherent.

## Related

- [[subscriber-vs-customer]] — hub.
- [[subscriber-vs-customer-consent]] — the gate that interacts with `unsubscribed`, `marketing` flags.
- [[subscriber-vs-customer-channels]] — the per-channel flag layer.
- [[subscriber-vs-customer-linkage]] — the link used to find the Subscriber(s) deleted with a Customer.
- [[customers-details]] — Customer-side detail; ban / delete actions.
- [[customers]] — Customer list; bulk delete.
- [[marketing-subscribers]] — Subscriber list; bulk delete + per-channel toggles.
- [[settings-hooks]] — `customer.*` and `subscriber.*` webhook families.

## Open Questions

No outstanding questions.
