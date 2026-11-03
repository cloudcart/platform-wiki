---
type: concept
nav_path: "Concept → Subscriber vs Customer → Channels"
aliases: ["Subscriber channels", "SubscriberChannel", "Per-channel marketing", "Email Phone WebPush Messenger channels", "Channel deliverability flags", "verified unsubscribed bounced"]
tags: [customers, subscribers, marketing, channels, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[subscriber-vs-customer]]. See the hub for the other aspects (records, consent, linkage, privacy, plan limits, admin surfaces).

# Subscriber vs Customer — channels and deliverability flags

## Definition

A Subscriber is reachable through **communication channels**. Each channel the platform supports is a separate **SubscriberChannel** row attached to the Subscriber row, with its own identifier (the email / phone / push token / Messenger PSID) and its own set of deliverability flags. A Subscriber has one Subscriber row + many SubscriberChannel rows — one per channel they've been identified on.

The platform recognises **4 channels**:

| Channel | Identifier | Used for |
|---------|------------|----------|
| `Email` | the email address | Newsletter, abandoned-cart email, order-confirmation (transactional bypasses marketing gate) |
| `Phone` | the phone number | SMS marketing, Viber marketing — see [[marketing-channels-viber]] |
| `WebPush` | a push-subscription token | Browser-push marketing campaigns |
| `Messenger` | Facebook Page-Scoped User ID | Facebook Messenger marketing |

Per-channel rows are what makes the consent model channel-specific. A Subscriber can be opted-in for Email and opted-out for SMS at the same time, or any other combination — see below.

## Scope

Covered:

- The 4 channels and their identifiers.
- The 4 per-channel deliverability flags (`marketing`, `verified`, `unsubscribed`, `bounced`).
- The "deliverable on Email" check as the AND of all four flags + Customer-level `marketing`.
- Channel-vs-channel independence (Email opt-out leaves Phone alive).
- Why a Subscriber with no Email channel is unreachable on Email.

Not covered:

- The two-layer Customer + per-channel consent gate — see [[subscriber-vs-customer-consent]].
- Unsubscribe / GDPR semantics — see [[subscriber-vs-customer-privacy]].
- How channel rows get created from storefront actions — see [[subscriber-vs-customer-records]].

## Contrasts

- **Subscriber row vs SubscriberChannel row** — the Subscriber carries identity + audience metadata; the SubscriberChannel carries per-channel marketing-consent + deliverability flags. The platform gates a campaign send by reading the SubscriberChannel, not the Subscriber.
- **`marketing` vs `verified`** — `marketing` is "did they consent?"; `verified` is "did they confirm we have the right address?". Both must be `yes` for most campaigns.
- **`unsubscribed` vs `marketing = no`** — `unsubscribed` is a one-way latch set by the recipient clicking the unsubscribe footer (a strong signal); `marketing = no` is the consent flag, which the recipient or merchant can flip in either direction. Both block a send.
- **`bounced` vs `unsubscribed`** — `bounced` is set by the email subsystem detecting a hard bounce (address doesn't exist / mailbox full); `unsubscribed` is set by the recipient choosing not to receive. Both block sends; only `unsubscribed` reflects user intent.
- **Email channel vs Phone channel** — distinct rows, distinct flags. Unsubscribing from email never affects SMS.

## Where it applies

### The 4 per-channel deliverability flags

Each SubscriberChannel row carries:

- **`marketing = yes/no`** — has the merchant / customer / consent flow opted this channel into marketing? Default depends on creation path.
- **`verified = yes/no`** — has the address been confirmed via the verification link / opt-in flow? Most campaigns refuse to send to `verified = no` (configurable per channel; see [[marketing-subscribers]]).
- **`unsubscribed = yes/no`** — has the recipient clicked "unsubscribe" in a previous email footer (or the equivalent on other channels)? When `yes`, the platform never sends to this channel again until the merchant intervenes.
- **`bounced = yes/no`** — did the email subsystem detect a hard bounce? Bounced channels are silently dropped from future sends.

So a "deliverable" Subscriber on Email needs:

```
Customer marketing = yes
AND SubscriberChannel(Email).marketing = yes
AND SubscriberChannel(Email).verified = yes
AND SubscriberChannel(Email).unsubscribed = no
AND SubscriberChannel(Email).bounced = no
```

Any one failing means no send. The Customer-level gate is described in [[subscriber-vs-customer-consent]].

### Channel-vs-channel independence

Because each channel is its own row with its own flags, **a Subscriber can be opted-in on Email and opted-out on SMS at the same time**, or any other mix. Two real-world implications:

- **Unsubscribe is per-channel.** When a Subscriber clicks "unsubscribe" in an email footer, ONLY the Email channel row flips to `unsubscribed = yes`. Their Phone channel — if they had one — keeps `unsubscribed = no` and SMS / Viber sends continue. To stop everything, the merchant has to flip all channels off explicitly OR flip the Customer-level `marketing = no` (see [[subscriber-vs-customer-consent]]).
- **A Subscriber with no Email channel is unreachable on Email.** Subscriber rows can exist without an Email channel — e.g., a Web Push opt-in creates a Subscriber with only a WebPush channel; an SMS-import creates a Subscriber with only a Phone channel. Email campaigns target the union of Subscribers that HAVE an Email channel passing all deliverability flags. Subscribers without any Email channel are silently skipped from email campaigns.

### Subscribed-from source — provenance of the channel row

The Subscriber row carries a `subscriber_from` source explaining what creation path made the row. The 12 known sources include `subscribe_form`, `contacts_form`, `web_push`, `subscribe_from_missing_product`, `customer_creating`, `order_creating`, `customer_login`, `customer_address_add`, `subscriber_creating` (admin manual create), `subscriber_import`, `customer_import`, and "Mark as subscriber". The source is shown in the [[marketing-subscribers]] detail and is useful when investigating "why is this person on my list?" — see [[subscriber-vs-customer-privacy]] for the audit angle.

### Default channel-marketing per creation path

The `marketing` flag default on the Email channel depends on how the Subscriber was created:

- Auto-create from `customer_creating` / `order_creating` / `customer_address_add` → `marketing = no` (unless the consent box was ticked in that flow).
- Subscribe form / popup → `marketing = yes` (the form IS the consent).
- "Notify me when in stock" → `marketing = no` for general marketing (the consent was for the back-in-stock notification only; product re-stock notifications send regardless of `marketing` because the user explicitly asked for THAT specific signal).
- "Mark as subscriber" on Customer import → `marketing = yes` or `no` per the import row's marketing column.

## Related

- [[subscriber-vs-customer]] — hub.
- [[subscriber-vs-customer-consent]] — the two-layer gate (Customer + per-channel).
- [[subscriber-vs-customer-privacy]] — channel-specific suppression / unsubscribe / GDPR.
- [[subscriber-vs-customer-records]] — how channel rows get created from storefront actions.
- [[subscriber]] — Subscriber entity carries the channel rows.
- [[marketing-subscribers]] — Subscriber list; per-channel flags shown as columns.
- [[marketing-channels-viber]] — Viber as a Phone-channel transport.
- [[marketing-campaigns]] — reads per-channel deliverability before sending.

## Open Questions

None.
