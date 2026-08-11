---
type: concept
nav_path: "Concept → Subscriber vs Customer"
route_name: (none)
route_path: (none)
aliases: ["Subscriber vs Customer", "Customer vs Subscriber", "Marketing record vs buyer record", "Audience vs CRM", "Newsletter signup vs registered buyer", "Marketing-consent record vs purchase record", "Subscriber-customer relationship", "Абонат и клиент", "Абонат срещу клиент", "Купувач и абонат", "Контакт срещу клиент"]
tags: [customers, subscribers, marketing, concepts]
plan_gates: []
created: 2026-05-23
updated: 2026-06-10
source_count: 5
---

# Subscriber vs Customer

## Definition

**Customer** and **Subscriber** are two separate records the platform keeps about the people who interact with the store. They look similar (both have a name, both can have an email, both can receive emails), but they answer two different questions and live in two different sections of the admin panel.

- A **Customer** ([[customer]]) is **someone who bought from the store or registered an account to buy**. The Customer record carries identity, addresses, login credentials (registered only), order history, lifetime revenue, loyalty group, and saved payment methods. The merchant manages Customers on [[customers]].
- A **Subscriber** ([[subscriber]]) is **someone the platform has identified as a marketing-audience contact on at least one communication channel** (Email, Phone, Web Push, or Messenger). The Subscriber record carries an audience profile, per-channel rows, marketing-consent flags, RFM analytics, tags, custom fields, and segment memberships. The merchant manages Subscribers on [[marketing-subscribers]].

The same person — same email, same phone — can exist as **both** a Customer and a Subscriber. The platform links them through a join table (one Subscriber can be linked to multiple Customers; one Customer is linked to at most one Subscriber-per-channel), but **the records are independent**: editing one does not auto-update the other, and deleting one does not auto-delete the other.

A Subscriber row can exist with `marketing = no` on every channel — being a Subscriber is about **having a contact identifier in the audience pool**, not about having opted in. The marketing flags are then separately checked to decide who gets sends.

The merchant has to keep this distinction in mind every time they think about audience, marketing, sends, or privacy — because the answers to *"how many Customers do I have?"* and *"how many people will receive my next campaign?"* are different numbers, gated by different plan limits, and exported through different screens.

## Sub-pages (in this cluster)

This concept is split into 7 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[subscriber-vs-customer-records]] — the two-record model; what each side carries; the "what creates which record" matrix per storefront action; the guest-Customer case; "Mark as subscriber" on Customer import; data overlap vs divergence.
- [[subscriber-vs-customer-channels]] — the 4 channels (Email / Phone / WebPush / Messenger), the SubscriberChannel row shape, the 4 per-channel deliverability flags (`marketing`, `verified`, `unsubscribed`, `bounced`).
- [[subscriber-vs-customer-consent]] — the two-layer consent gate (Customer-level `marketing` AND per-channel `marketing`); the "Second marketing" auto-reset rule; opt-OUT cascade from Customer to all channels; opt-IN does NOT auto-cascade back.
- [[subscriber-vs-customer-linkage]] — the `subscriber_to_customer` join; cardinality; Subscriber → Customer and Customer → Subscriber conversion paths; the anonymous-visitor / UUID-anchored upgrade path.
- [[subscriber-vs-customer-privacy]] — channel-specific unsubscribe; Customer-delete vs Subscriber-delete (no cascade); async join-row cleanup; Customer ban does NOT cascade; GDPR right-to-erasure requires both sides.
- [[subscriber-vs-customer-limits]] — independent `customers` and `subscribers` plan caps; `subscribers.max_id` chronological-cap mechanism; over-cap Subscribers are visible but excluded from sends.
- [[subscriber-vs-customer-surfaces]] — admin-panel navigation map: which screens manage Customers, which manage Subscribers, which surface both side-by-side.

## Why it matters to the merchant

This is the single most-confused distinction in the admin panel. Merchants typically ask: *"Why is the campaign sending to 250 people when I have 800 customers?"* or *"Why didn't this customer get my newsletter — they bought from me last week!"* The answer is always the same: **Customer count ≠ Subscriber count**, and **placing an order does NOT automatically opt the buyer into marketing**.

Concrete consequences:

- **Marketing-campaign reach is the Subscriber count, NOT the Customer count.** A store can have 10,000 Customers and 1,200 Subscribers — only those 1,200 receive a newsletter. The other 8,800 bought without consenting to marketing.
- **GDPR / unsubscribe affects the Subscriber, not the Customer.** When a buyer clicks "unsubscribe" the **Subscriber**'s Email channel flips to `unsubscribed = yes`; the **Customer** record stays intact — order history, login, transactional emails keep working. See [[subscriber-vs-customer-privacy]].
- **Plan limits are different.** [[subscriber-vs-customer-limits]] covers the independent caps + the chronological cap mechanism.
- **Exports are different.** [[customers-export]] dumps Customer fields. [[marketing-subscribers]] → Import dumps Subscriber fields. The exports overlap in name + email and little else. See [[subscriber-vs-customer-records]].
- **Segments only see Subscribers.** [[marketing-segments]] are built on the Subscriber pool. A Customer who never opted into marketing is invisible to segments.
- **Orders only see Customers.** Every [[order|Order]] is attached to exactly one Customer. An Order has NO direct Subscriber link — the Subscriber connection is via the shared email.

## Scope

Covered across the 7 sub-pages: the two-record data model; the two-layer consent gate; the 4 channels + deliverability flags; conversion in both directions; the `subscriber_to_customer` join; privacy / unsubscribe / deletion (no auto-cascade); independent plan caps; the "Second marketing" auto-reset; the anonymous-visitor upgrade path.

NOT covered:

- Internal admin accounts ([[merchant-roles]]) — Owners, Moderators, and API access are a totally separate model.
- Marketing-segment construction or campaign mechanics — see [[marketing-segments]] and [[marketing-campaigns]].
- Storefront marketing-policy / GDPR settings (the UI labels at checkout / signup) — those live on store-level settings.
- The customer-group / loyalty-tier mechanism — that's Customer-only and lives on [[customers-custom-groups]].

## Contrasts

- **Subscriber vs Customer** — see [[subscriber-vs-customer-records]] for the data shapes.
- **Subscriber vs Customer Group** — Customer Group is a loyalty / discount tier assigned per Customer (static, manual). Segments are NOT Groups — segments select Subscribers dynamically by rule.
- **Subscriber vs Segment** — a [[segment|Segment]] is a rule-based set of Subscribers. Segments LIVE on Subscribers — a Customer with no Subscriber is invisible to every segment.
- **Subscriber row vs SubscriberChannel row** — see [[subscriber-vs-customer-channels]].
- **Marketing send vs transactional send** — see [[subscriber-vs-customer-consent]]. The two-layer gate covers marketing only.
- **Customer delete vs Subscriber delete** — see [[subscriber-vs-customer-privacy]]. No auto-cascade either direction.
- **`customers` plan cap vs `subscribers` plan cap** — see [[subscriber-vs-customer-limits]]. Separate meters.

## Where it applies

The Customer-vs-Subscriber distinction touches a large surface of the admin panel and the storefront. The detailed navigation map is on [[subscriber-vs-customer-surfaces]]. High-level landing points:

- **Storefront** — [[checkout-flow]] (the consent checkbox), [[marketing-subscribers-subscribe-forms]] (popup forms create Subscribers), storefront account preferences (Customer-level toggle).
- **Admin lists / detail** — [[customers]], [[customers-details]], [[marketing-subscribers]], [[subscriber]] detail.
- **Imports / exports** — [[customers-import]] (with the "Mark as subscriber" option), [[customers-export]], [[marketing-subscribers]] → Import.
- **Plan / privacy** — [[plan-gates]], [[notification-delivery]], [[settings-hooks]] (`customer.*` and `subscriber.*` webhook families).

## Related

- [[customer]] — Customer entity page.
- [[subscriber]] — Subscriber entity page.
- [[customers]] — Customers list screen.
- [[marketing-subscribers]] — Subscribers list screen.
- [[customer-group]] — Customer-only loyalty / discount tier.
- [[segment]] — Subscriber-only; groups Subscribers by rule.
- [[notification-delivery]] — applies the two-layer consent gate.
- [[marketing-campaigns]] — broadcasts; target Subscribers.
- [[marketing-segments]] — built on Subscribers.
- [[marketing-subscribers-subscribe-forms]] — popups that create Subscribers (not Customers).
- [[customers-import]] / [[customers-export]] — Customer-side bulk flows.
- [[customers-custom-fields]] — Customer custom fields (distinct from Subscriber custom fields).
- [[marketing-subscribers-custom-fields]] — Subscriber custom fields (distinct from Customer custom fields).
- [[plan-gates]] — separate `customers` vs `subscribers` caps.
- [[checkout-flow]] — where the marketing-consent checkbox is captured.
- [[settings-hooks]] — `customer.*` and `subscriber.*` webhook event families.

## Open Questions

No outstanding questions — all previously-flagged items resolved or distributed to sub-pages.
