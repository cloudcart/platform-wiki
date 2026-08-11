---
type: concept
nav_path: "Concept → Subscriber vs Customer → Linkage and conversion"
aliases: ["subscriber_to_customer join", "Subscriber to customer linkage", "Subscriber Customer conversion", "Anonymous subscriber upgrade", "UUID-anchored subscriber", "customer_login source", "order_creating linkage"]
tags: [customers, subscribers, marketing, linkage, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[subscriber-vs-customer]]. See the hub for the other aspects (records, channels, consent, privacy, plan limits, admin surfaces).

# Subscriber vs Customer — linkage and conversion paths

## Definition

When the same person exists as both a Customer and a Subscriber, the platform connects the two records through a **`subscriber_to_customer` join table**. The join is created automatically by recognised storefront events, and it can be one-to-many on the Subscriber side: **one Subscriber can be linked to multiple Customers**; **one Customer is linked to at most one Subscriber per channel-identifier**.

Linkage rows are created automatically when:

- The same email exists on both a Customer and a Subscriber → linked at Customer-creation time / Subscriber-creation time.
- A Customer logs in (`customer_login` source on the Subscriber-from list — visiting / logging-in upgrades an anonymous Subscriber into a customer-linked Subscriber).
- An order is created (`order_creating` source) — the order's Customer is linked to the Subscriber that owns the order's email.

The two records do **not** merge — they stay independent. Only the join row and the per-channel marketing flag (if the consent path flipped it) get updated.

## Scope

Covered:

- The `subscriber_to_customer` join semantics.
- Cardinality: one-Subscriber-to-many-Customers, one-Customer-to-one-Subscriber-per-channel.
- Subscriber → Customer conversion (newsletter signup buys).
- Customer → Subscriber conversion (buyer opts into marketing).
- The anonymous-visitor / UUID-anchored row upgrade path.
- What the merchant means by "convert subscribers to customers".

Not covered:

- Cleanup of the join row on Customer hard-delete — see [[subscriber-vs-customer-privacy]].
- Customer-side ban (no cascade to Subscriber) — see [[subscriber-vs-customer-privacy]].
- The two-layer consent gate that determines what reach actually happens after linkage — see [[subscriber-vs-customer-consent]].

## Contrasts

- **Linked vs unlinked Subscriber** — a Subscriber without a Customer link (newsletter-only signup) has no order history, no RFM activity, no Customer Group; they only appear on Subscriber-side surfaces.
- **One Subscriber, many Customers** — happens when the same email was used by two different storefront registrations (e.g., guest + later registered). The Subscriber detail's Customers tab lists every linked Customer with their order totals.
- **One Customer, one Subscriber per channel-identifier** — two Customers sharing an email both link to the same Subscriber; the Subscriber does not split.
- **Subscriber → Customer conversion vs Customer → Subscriber conversion** — both are normal merchant workflows; "convert subscribers to customers" means *get newsletter signups to buy*, "convert customers to subscribers" means *get buyers to opt into marketing*. They go in different directions and target different records.

## Where it applies

### The `subscriber_to_customer` join — cardinality

- **One Subscriber CAN be linked to multiple Customers.** Real-world cause: the same email was used for two different storefront registrations (e.g., one guest order and one registered account later). The Subscriber detail's Customers tab shows every linked Customer + their order totals + their lifetime income.
- **One Customer is linked to at most one Subscriber per channel-identifier.** Two different Customers sharing an email both link to the same Subscriber; the Subscriber row does not duplicate.

### Subscriber → Customer (newsletter signup converts to buyer)

1. Person fills the [[marketing-subscribers-subscribe-forms|popup form]] → Subscriber row created with `subscriber_from = subscribe_form`, Email channel `marketing = yes`, `verified` depends on flow (single opt-in vs double opt-in).
2. Days/weeks later, the same email places an order → guest Customer (or registered Customer) row created.
3. Order creation triggers the `order_creating` linkage flow → `subscriber_to_customer` join row created tying the existing Subscriber to the new Customer.
4. The Subscriber's RFM bucket is recomputed (they now have orders, so they move from "Without RFM Analysis" toward "New", "Champ", etc.).

### Customer → Subscriber (buyer opts into marketing)

1. Person registers / orders without ticking the marketing-consent box → Customer with `marketing = no`, AND a Subscriber row is auto-created with `subscriber_from = customer_creating` / `order_creating`, but the Email-channel `marketing = no`.
2. Later, the Customer either:
   - Goes to their storefront Account preferences and ticks "Accept marketing" → Customer-level `marketing` flips to `yes`; the linked Subscriber's Email-channel `marketing` flips to `yes`.
   - Subscribes to the newsletter via a popup using the same email → the existing Subscriber's Email channel flips to `marketing = yes`.
   - Is bulk-marked by the merchant via [[marketing-subscribers]] → "Accept marketing" bulk action.
3. From now on, the Subscriber is reachable on Email campaigns; the Customer is reachable on Customer-level campaigns. The two-layer gate applies — see [[subscriber-vs-customer-consent]].

In both directions the underlying records do **not** merge. They stay independent. Only the join row and the per-channel marketing flag get updated.

### The anonymous-visitor / UUID-anchored upgrade path

Before a visitor identifies themselves on any channel (no email, no phone, no login), the platform can still track them via a cookie UUID — assigned the first time they visit and persisted client-side. Anchored to that UUID, the platform records pageviews, cart events, and other behavioural signals.

The moment the visitor identifies themselves (typing an email into a subscribe form, logging in, placing an order, ticking "remember me", filling the Contacts form), the UUID-anchored row becomes a **Subscriber**. The Subscriber inherits the prior behavioural history attached to the UUID, so segments that test on UUID-tracked behaviour ("visited 3+ products", "abandoned cart") light up retroactively.

Until identification, the row is an **"anonymous subscriber"** — visible to segment conditions that test on UUID-tracked behaviour but **not reachable via any campaign channel** (there's no identifier to send to). This intermediate state is invisible to most merchant-facing screens; it surfaces only via behavioural-trigger segments and [[abandoned-cart-recovery]].

### When linkage rows form — the recognised events

| Event | Source recorded on Subscriber | Customer side | Linkage created? |
|-------|-------------------------------|---------------|------------------|
| Storefront login | `customer_login` | Customer must exist | Yes |
| Storefront order created | `order_creating` | Customer (or guest Customer) is created or matched on email | Yes |
| Customer created in admin | `customer_creating` | Customer is the trigger | Yes |
| Customer adds shipping address | `customer_address_add` | Customer must exist | Yes (if Phone-channel is new) |
| Subscribe form submission with email matching an existing Customer | `subscribe_form` | Customer exists | Yes (resolved at insert time) |
| "Mark as subscriber" on Customer import | `customer_import` | Customer is the source | Yes |
| Standalone subscribe (no matching Customer yet) | `subscribe_form` etc. | No Customer | No (linkage forms later when a Customer with this email is created) |

## Related

- [[subscriber-vs-customer]] — hub.
- [[subscriber-vs-customer-records]] — what each record carries; "what creates which record".
- [[subscriber-vs-customer-consent]] — the two-layer gate that determines reach after linkage.
- [[subscriber-vs-customer-privacy]] — Customer hard-delete cleans up the join row asynchronously.
- [[subscriber]] — Subscriber entity; detail page lists every linked Customer.
- [[customer]] — Customer entity.
- [[customers-details]] — surfaces the linked Subscriber's channels.
- [[marketing-subscribers]] — shows `subscriber_from` source + linked Customers.
- [[marketing-subscribers-subscribe-forms]] — popup forms that create newsletter-only Subscribers.
- [[abandoned-cart-recovery]] — uses UUID-anchored behaviour to identify Subscribers before they identify themselves.

## Open Questions

None.
