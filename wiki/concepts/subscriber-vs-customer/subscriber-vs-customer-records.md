---
type: concept
nav_path: "Concept → Subscriber vs Customer → Two records"
aliases: ["Customer vs Subscriber records", "Customer record vs Subscriber record", "Guest customer vs subscriber", "Two-record model", "Subscriber record shape", "Customer record shape"]
tags: [customers, subscribers, marketing, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-11-09
source_count: 5
---

> Part of [[subscriber-vs-customer]]. See the hub for the other aspects (channels, consent, linkage, privacy, plan limits, admin surfaces).

# Subscriber vs Customer — the two records

## Definition

The platform keeps **two separate top-level records** about the people who interact with the store:

- A **Customer** ([[customer]]) — someone who **bought from the store or registered an account to buy**. The Customer record carries identity, addresses, login credentials (registered only), order history, lifetime revenue, loyalty / Customer Group, and saved payment-method tokens. Managed on [[customers]].
- A **Subscriber** ([[subscriber]]) — someone the platform has identified as a **marketing-audience contact on at least one communication channel** (Email, Phone, Web Push, Messenger). The Subscriber record carries the audience profile, per-channel rows, marketing-consent flags, RFM analytics bucket, tags, custom fields, segment memberships, and tracking UUIDs. Managed on [[marketing-subscribers]].

The same person — same email, same phone — can exist as **both** a Customer and a Subscriber. The platform links them through a join table (see [[subscriber-vs-customer-linkage]]), but **the records are separate**: editing one does not auto-update the other; deleting a Customer also deletes the linked Subscriber, not the reverse ([[subscriber-vs-customer-privacy]]).

A Subscriber row can exist with `marketing = no` on every channel — being a Subscriber is about **having a contact identifier in the audience pool**, not about having opted in. The marketing flags are then separately checked to decide who actually receives sends; see [[subscriber-vs-customer-consent]].

## Scope

Covered here:

- The two-record model and what each side carries.
- The "what creates which record" matrix per storefront action.
- The guest-Customer case.
- The "Mark as subscriber" import option as the only routine bulk-co-create path.
- Field overlap (small) vs field divergence (large).

Not covered:

- Per-channel deliverability flags — see [[subscriber-vs-customer-channels]].
- The two consent layers — see [[subscriber-vs-customer-consent]].
- How linkage rows form — see [[subscriber-vs-customer-linkage]].

## Contrasts

- **Customer record vs Subscriber record** — Customers carry order history, login, addresses, lifetime revenue, Customer Group. Subscribers carry channels, RFM bucket, segment memberships, marketing-consent state. The same person can be one, both, or neither.
- **Registered Customer vs guest Customer** — both are full Customer records with order history; guests sit in the **Guests** group with no password, so they cannot log in.
- **Subscriber row vs SubscriberChannel row** — the Subscriber row carries identity + audience-level metadata; the SubscriberChannel row carries per-channel marketing-consent + deliverability flags. A Subscriber has one row + many SubscriberChannel rows. See [[subscriber-vs-customer-channels]].
- **Customer count vs Subscriber count** — different numbers, gated by different plan limits (see [[subscriber-vs-customer-limits]]); only Customers have a file export.

## Where it applies

### What creates which record per storefront action

| Person did this | Customer record? | Subscriber record? |
|-----------------|------------------|---------------------|
| Placed an order as guest (no account) | **Yes** — guest Customer (group **Guests**), found again by email on the next guest order. | **Yes** — Email (+ phone) Subscriber linked to that Customer; marketing on only with consent. |
| Registered an account (no order yet) | **Yes** — registered Customer with login. | **Yes** — marketing on only with consent. |
| Signed up via popup / [[marketing-subscribers-subscribe-forms\|subscribe form]] | No — until they place an order. | **Yes** — Subscriber created with `subscribed_from = subscribe_form`. |
| Filled the Contacts form | No. | **Yes** — `subscribed_from = contacts_form`. |
| Subscribed to Web Push (browser permission) | No. | **Yes** — `subscribed_from = web_push` + a WebPush channel row. |
| Subscribed to "Notify me when in stock" | No. | **Yes** — `subscribed_from = subscribe_from_missing_product`. |
| Imported by the merchant from CSV | If imported on [[customers-import]]. | If imported on [[marketing-subscribers]] → Import. |
| Created by the merchant in admin | If created on [[customers]]. | If created on [[marketing-subscribers]]. |

Two takeaways:

1. **Buying does NOT give marketing consent.** A buyer-without-consent is a Customer whose Subscriber row has marketing off: order emails, no campaigns.
2. **Subscribing does NOT automatically register a Customer.** A newsletter signup is a Subscriber with no Customer until they actually place an order.

The platform **does** auto-create a Subscriber row in several customer-touching flows (registering as Customer, creating a Customer in admin, placing an order, adding a shipping address) — but the SubscriberChannel row that controls "will they receive marketing on Email" defaults to `marketing = no` unless consent was explicitly given.

### The guest-Customer case

A guest Customer is a full Customer record — order history, lifetime revenue, addresses — that cannot log in. Each order also creates or updates a linked Subscriber, so a guest counts as type **Customer** in segments; with no consent, all its channels have marketing off. With **Convert guests into members** on, the guest record becomes a registered Customer at the first order placed after the setting was turned on ([[checkout-flow-guest-vs-registered]]).

Consequence: a store with mostly guest orders and a quiet "Accept marketing" box has many Subscribers but few marketable ones.

### "Mark as subscriber" on Customer import

[[customers-import]] has a "Mark as subscriber" option that also creates Subscriber rows for the imported emails (Email channel, `marketing = yes` if the row's marketing column says so) — the only routine bulk path that subscribes Customers, for lists with prior consent.

[[marketing-subscribers]] → Import does the inverse: Subscriber-only rows, **no** Customer accounts — the right path for a newsletter list (the Customer importer would create empty Customer records).

### Data overlap, not data duplication

The two records carry **different** field sets. Overlap is intentionally small:

| Concept | Lives on Customer | Lives on Subscriber |
|---------|-------------------|---------------------|
| First name, last name | Yes (canonical for orders / invoices) | Yes (denormalised; updated from Customer when linked) |
| Email | Yes (canonical for login) | Yes (as the Email channel's `channel_identifier`) |
| Phone | On the address record (Customer has many addresses) | As the Phone channel's `channel_identifier` |
| Billing / shipping addresses | Yes (canonical) | No |
| Order history, lifetime revenue, last-order date | Yes (canonical; pre-aggregated snapshots) | Yes (denormalised summary: `last_order_id`, RFM bucket) |
| Customer Group, loyalty tier | Yes | No |
| Tags | Customer-tag table | Subscriber-tag table (distinct taxonomies) |
| Custom fields | [[customers-custom-fields]] | [[marketing-subscribers-custom-fields]] |
| Marketing-consent flag | Customer-level `marketing` | Per-channel `marketing` |
| RFM analytics bucket | No | Yes |
| Subscribed-from source | No | Yes (12 sources — see [[marketing-subscribers]]) |
| Identified-device UUIDs | No | Yes (tracking cookies) |
| Segment memberships | No (read-through Subscriber) | Yes |
| Login credentials | Yes (registered only) | No (Subscribers don't log in) |
| Saved payment-method tokens | Yes | No |

The two records are connected by the shared email (and phone, where applicable), and surfaced together on [[customers-details]] (Customer + linked Subscriber) and on [[marketing-subscribers]] detail (Subscriber + linked Customers).

## Related

- [[subscriber-vs-customer]] — hub.
- [[customer]] — Customer entity.
- [[subscriber]] — Subscriber entity.
- [[customers]] — Customer list screen.
- [[marketing-subscribers]] — Subscriber list screen.
- [[customers-import]] — "Mark as subscriber" option.
- [[customers-custom-fields]] — Customer-only custom fields.
- [[marketing-subscribers-custom-fields]] — Subscriber-only custom fields.

## Open Questions

None.
