---
type: entity
nav_path: "Entity → Subscriber"
aliases: ["Subscriber", "Marketing subscriber", "Newsletter subscriber", "Audience member", "Contact", "Marketing contact", "Recipient", "Абонат", "Маркетинг абонат"]
tags: [entity, marketing, subscribers, channels, audience, customers]
plan_gates: ["subscribers"]
created: 2026-05-21
updated: 2026-06-10
source_count: 7
---

# Subscriber

## Identity

A **Subscriber** is a marketing-audience record — someone reachable on at least one communication channel (Email, Phone/SMS/Viber, Web Push, or Facebook Messenger). The Subscriber is CloudCart's central audience entity: it carries the contact identifier(s), per-channel subscription rows, marketing-consent flags, deliverability state (verified / unsubscribed / bounced), tags, custom fields, segment memberships, RFM analytics, and the audience source ("how did this person enter the audience?"). The merchant manages subscribers on [[marketing-subscribers]] and uses them as the targeting pool for [[marketing-campaigns]] and [[marketing-segments]].

A Subscriber is **distinct from a [[customer|Customer]]** — a Customer is a buyer (placed an order or registered an account); a Subscriber is a marketing-consented contact. The same person can be both (the records link via the shared email), one but not the other, or neither. The platform auto-creates a Subscriber row in many customer-touching flows (registering, ordering, adding an address), but the per-channel marketing flag defaults to `marketing = no` unless the person explicitly opted in. See [[subscriber-vs-customer]] for the full distinction — it's the single most-confused concept in the admin panel.

A Subscriber lives within the **Subscribers plan cap** (`subscribers` plan-feature), independent of the Customers cap. A store can have 10,000 Customers and 1,200 Subscribers; campaigns reach only the 1,200.

## Aliases

- **Subscriber** — the canonical term in admin UI and across the wiki.
- **Marketing subscriber** / **Newsletter subscriber** — used informally when emphasising the marketing focus.
- **Audience member** — used in segmentation / RFM contexts.
- **Contact** / **Marketing contact** — used in CRM-sync contexts (Mailchimp, external ESP).
- **Recipient** — used in send-side / delivery contexts.
- **Абонат** / **Маркетинг абонат** — Bulgarian equivalents.

## Sub-pages (in this cluster)

This entity is split into 6 aspect pages. The Assistant should drill into the aspect that matches the question, not read every page.

- [[subscriber-entity-attributes]] — Subscriber-row fields (names, country, marketing/GDPR flags, source, tenure, RFM bucket, tags, custom fields, UUIDs, force-marketing tokens) and the 13 `subscriber_from` sources.
- [[subscriber-entity-channels]] — SubscriberChannel rows (Email / Phone / WebPush / Messenger); per-channel `marketing` / `verified` / `unsubscribed` / `bounced`; default-channel rule; identifier uniqueness + merge flow.
- [[subscriber-entity-lifecycle]] — the 8 states (Created → Active → Pending → Suppressed → Unsubscribed → Bounced → Merged → Deleted); `last_active_at` auto-refresh from storefront writes; cascade-delete cleanup of 10 child tables; `subscriber.created` / `updated` / `deleted` webhook fires.
- [[subscriber-entity-consent-rules]] — the two-layer consent gate (Customer-level AND per-channel); "place an order does NOT auto-subscribe"; Second-marketing auto-flip; Customer → Subscriber one-way sync of opt-outs; most-restrictive rule when linked to multiple Customers; GDPR precedence at checkout.
- [[subscriber-entity-relationships]] — Customer linkage via `subscriber_to_customer`; multiple Subscribers per Customer; Customer hard-delete cascade; Segments membership; UUIDs / events; distinction from Customer, Customer Group, Segment.
- [[subscriber-entity-api-and-plan]] — JSON-API v2 (`api-subscribers`, `api-subscribers-channels`, `api-subscribers-tags`); side effects; the `subscribers` plan cap; CSV-import truncation; segment self-limit; webhook event catalogue.

## Key Attributes

The full per-field schema lives on [[subscriber-entity-attributes]] (Subscriber-row fields) and [[subscriber-entity-channels]] (per-channel SubscriberChannel rows). At a glance:

- **Subscriber-row** carries identity (first/last name, country), consent (`marketing`, `gdpr_accepted`), source (`subscriber_from` — 13 enum values), tenure (`created_at`, `last_active_at`), tags, custom fields, UUIDs, RFM bucket (1 of 17).
- **SubscriberChannel** rows (one per reachable channel) carry the channel identifier (email / phone / PSID), per-channel `marketing`, `verified`, `unsubscribed`, `bounced`.

A marketing send is gated by **both layers** — Customer-level marketing flag (when linked) AND per-channel marketing flag AND per-channel deliverability. Any one failing = no send. See [[subscriber-entity-consent-rules]] for the full gating model.

## Where it appears

- [[marketing-subscribers]] — the Subscriber list (search, filter, bulk-edit, import, settings).
- [[marketing-subscribers-custom-fields]] — Subscriber-specific custom-field definitions.
- [[marketing-subscribers-subscribe-forms]] — storefront popup / signup forms that CREATE Subscribers (not Customers).
- [[marketing-segments]] — segment builder, built on the Subscriber pool.
- [[marketing-segments-subscribers]] — segment-detail members view (lists Subscribers).
- [[marketing-campaigns]] — broadcasts; target Subscribers; reads per-channel deliverability.
- [[marketing-campaigns-subscribers]] — per-campaign target audience.
- [[customers-details]] — Customer detail surfaces the linked Subscriber's channels in the overview tab.
- [[customers-details-overview]] — "Customers and Subscribers" surface showing the same email from both perspectives.
- [[customers-import]] — has a "Mark as subscriber" option that co-creates Subscriber rows for imported emails.
- [[apps-mailchimp]] — Subscriber sync target for the Mailchimp integration.

## Related

### Related entities

- [[customer]] — buyer / registered account. May share an email with a Subscriber but is a separate record.
- [[customer-group]] — Customer-only concept (loyalty tier). Distinct from Subscriber.
- [[segment]] — rule-based set of Subscribers; one Subscriber can be in many segments.
- [[channel]] — the channel-type taxonomy (Email / Phone / WebPush / Messenger).
- [[campaign]] — marketing broadcasts that target Subscribers.
- [[subscriber-form]] — storefront subscribe-form definitions.

### Cross-cutting concepts

- [[subscriber-vs-customer]] — the canonical distinction page (the single most-confused topic in the admin panel).
- [[notification-delivery]] — how the two-layer consent (Customer-level + per-channel) is applied when a marketing send is dispatched.
- [[checkout-flow]] — where the marketing-consent checkbox at checkout decides whether a Subscriber row is auto-created with `marketing = yes` or `marketing = no`.
- [[plan-gates]] — the `subscribers` plan cap.
- [[abandoned-cart-recovery]] — the abandoned-cart email gates on Subscriber consent.

### Settings & webhooks

- [[marketing-subscribers]] → Settings — RFM interval, revenue statuses, bestseller period, Second marketing rule.
- [[settings-hooks]] — `subscriber.created` / `subscriber.updated` / `subscriber.deleted` webhook events.
- [[settings-general]] — store-level GDPR / marketing-policy settings that set the storefront consent labels.

## Open Questions

No outstanding questions — all items resolved or distributed to sub-pages.
