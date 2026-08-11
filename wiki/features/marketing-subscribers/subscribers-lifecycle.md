---
type: feature
nav_path: "Marketing → Subscribers → Lifecycle"
route_name: subscribers.list
route_path: /admin/marketing-new/subscribers
aliases: ["Subscriber lifecycle", "Subscriber sources", "Subscriber webhooks", "Subscriber GDPR erasure", "Subscriber plan cap", "Subscriber marketing consent"]
tags: [marketing, subscribers, lifecycle, gdpr, webhooks, plan-cap, sources]
plan_gates: ["subscribers"]
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---

> Part of [[marketing-subscribers]]. See the hub for related aspects (list view, bulk actions, detail modal, channels, import, settings).

# Subscribers — lifecycle, sources, consent, and GDPR

## Purpose

Subscriber identity is created, mutated, and (sometimes) erased on signals from many directions: storefront forms, customer registrations, order placements, API writes, CSV imports, GDPR requests. This aspect documents the source taxonomy, marketing-consent capture, the lifecycle webhooks, the GDPR-erasure cascade, the permission gate, and the chronological plan-cap rule that decides which subscribers are campaign-eligible.

## Where to find it

Mostly invisible UI — cross-cutting business rules. The merchant interacts with it through:

- The "Subscribed by" filter on [[subscribers-list-view]].
- The marketing-consent toggles on [[subscribers-bulk-actions]] and [[subscribers-detail-modal]].
- The `subscriber.*` webhook settings on [[settings-hooks]].
- The `marketing.subscribers` permission grant on [[settings-staff]].

## What the merchant can do here

- See the source attribution per subscriber (the "Subscribed by" column on [[subscribers-list-view]]).
- See and override the marketing-consent state per channel.
- Receive `subscriber.created` / `updated` / `deleted` webhook events in their hook receiver.
- See the plan-cap status via the Limits modal (see [[subscribers-settings]]).
- Grant the `marketing.subscribers` permission to a moderator from [[settings-staff]].

## Settings & fields

### Source tracking — "Subscribed by" (`subscriber_from`)

Every subscriber has a `subscriber_from` field set at creation. The 13 sources, with merchant-facing label:

| Constant | Label |
|----------|-------|
| `customer_login` | Customer login |
| `subscribe_form` | Popup and Form builder |
| `subscribe_from_missing_product` | Subscribe to an in-stock product |
| `import` | Import |
| `system` | From system |
| `customer_address_creating` | Customer address creating |
| `customer_address_deleting` | Customer address deleting |
| `customer_creating` | Customer creating |
| `order_creating` | Order creating |
| `messenger` | Facebook messenger |
| `contacts_form` | Contacts form |
| `web_push` | Web push |
| `API` | API |

This drives the `subscriber.from` segment condition and the "Subscribed by" filter on [[subscribers-list-view]]. **The list is mostly stable** — new sources are added carefully, because old segments may filter by them.

### Webhook events ([[settings-hooks]])

A subscriber's lifecycle fires three webhooks, processed by the standard retry pipeline:

- `subscriber.created` — new subscriber row created.
- `subscriber.updated` — channel data, marketing consent, tags, or custom fields changed.
- `subscriber.deleted` — subscriber removed.

### Permission gate

A moderator needs either the broad **Marketing** permission OR the specific **Subscribers** (`marketing.subscribers`) grant from [[settings-staff]] to list, view, edit, delete, import, export, tag, segment, or bulk-act on subscribers. Owners always pass. The export sub-action additionally honours the `marketing.subscribers_export` granular permission when configured.

## Business rules

### Subscriber identity model — distinct from Customer

A subscriber is a marketing-only record. Differences from a [[customer]]:

- A subscriber can exist with no customer account (signed up via popup, never registered).
- A single subscriber can map to multiple customers (same email reused across registrations, or merged later). This shows in the Customers tab on the [[subscribers-detail-modal]].
- A customer who registers without explicitly subscribing is still auto-created as a subscriber (source: `customer_creating`) but their channel may default to marketing-off.

See [[subscriber-vs-customer]] for the full contrast.

### Delete cascade — what's wiped

When the merchant deletes a subscriber (single row or bulk), the platform wipes the subscriber's channels, device IDs, tags, segment memberships, tracked events, custom-field values, and campaign history / campaign-action logs. **Linked orders and carts get their `subscriber_id` nulled** (the order / cart itself stays). A `subscriber.deleted` webhook fires.

### Marketing-consent capture — 4 paths in

The `accept_marketing` flag is per-channel, set in one of these ways:

- **Storefront** — the "Accept marketing" box (label `marketing.yes` / `marketing.no`) in checkout, signup, or subscribe form. If GDPR is active the policy page is the GDPR `marketing_policy` setting, otherwise the store's `checkout_terms_page` setting.
- **Admin override** — the channel-edit form ([[subscribers-detail-modal]]) or bulk-marketing actions ([[subscribers-bulk-actions]]).
- **Auto-on at signup** — "Mark all email allow marketing" on CSV import ([[subscribers-import]]).
- **Force-on / Force-off** — constants `FORCE_MARKETING_ON` / `FORCE_MARKETING_OFF` (`force-1` / `force-0`) carry an explicit override through the storefront subscribe flow even if the box wasn't ticked (legacy field, see [[checkout-flow]]).

The "Second marketing" setting ([[subscribers-settings]]) adds a rule: if a subscriber accepted marketing at signup but did NOT re-confirm at checkout (when marketing is optional), the system flips them to "Does not accept marketing."

### Customer marketing-flip propagates ONE WAY to subscriber

When a linked Customer's `marketing` flag flips `yes → no` (admin or storefront preferences), a background task flips each linked per-channel marketing flag off. **The REVERSE (`no → yes`) does NOT auto-flip per-channel back on** — the merchant must re-enable each channel explicitly.

Rationale: opt-out propagates automatically, opt-in requires explicit per-channel consent. The bulk admin action on [[subscribers-bulk-actions]] is symmetric — bulk-accept-marketing DOES propagate yes both directions, being an explicit admin operation.

### Plan cap is chronological, not random

When the plan's `subscribers` feature is finite, a recurring background task (every 10 minutes) computes the **Nth subscriber id** (sorted ascending) among non-bounced, non-unsubscribed, marketing-on contacts — N being the plan's cap. This id is stored as the `subscribers.max_id` setting. Segment evaluation then silently excludes any subscriber newer than that id from campaigns and segments.

Practical implications:

- The "active" subscribers are the **chronologically earliest** N opt-ins, not random.
- The cap is recomputed every 10 minutes, so bulk-deleting bounced / unsubscribed contacts opens slots within ~10 minutes.
- The cap is global per store, not per segment.
- An admin sees ALL subscribers in the list (no cap filter), but only eligible ones appear in segment counts / campaign reach.
- On an unlimited plan the `subscribers.max_id` setting is removed.

When the store approaches the cap, the alert reads: *"You reached the limit of feature **Subscribers - :limit** — To continue you should purchase a feature pack or upgrade to a plan with higher limits!"* Two paths out: prune bounced / unsubscribed via [[subscribers-bulk-actions]], or upgrade the plan via [[subscribers-settings]]. Some segments self-limit to the first `:limit` of the population, per the "Active for segments" / `planLimit` condition.

### GDPR — erasure and right-to-be-forgotten

When a customer exercises their GDPR right to erasure, the platform runs the subscriber-delete cascade above and writes a marketing-log entry recording the deletion reason for compliance audit. Email PII is stripped from logs; the subscriber-ID reference remains as a no-PII marker. The cascade is symmetric: erasing the customer account also strips the linked subscriber row's PII (the audit-marker row remains).

### Custom fields — per-subscriber attributes

Subscribers support arbitrary **custom fields** defined at `/admin/marketing-new/subscribers/fields` ([[marketing-subscribers-custom-fields]]). Once defined they appear in subscribe forms ([[marketing-subscribers-subscribe-forms]]) and as the `subscriber.custom_field` segment condition (*"where custom field ':field' is ':options'"*). These are distinct from [[customer]] custom fields, which the `customer.custom_field` condition reads.

## Related

- [[marketing-subscribers]] — hub.
- [[subscribers-list-view]] — surfaces the source filter + plan-cap eligibility.
- [[subscribers-bulk-actions]] — explicit admin marketing flips (symmetric).
- [[subscribers-detail-modal]] — per-channel marketing toggles.
- [[subscribers-channels]] — channel identity + merge that this aspect's cascade tears down.
- [[subscribers-import]] — `subscriber_from = 'import'` source attribution + plan-cap truncation.
- [[subscribers-settings]] — Limits modal + chronological-cap setting `subscribers.max_id`.
- [[settings-hooks]] — `subscriber.created` / `updated` / `deleted` webhooks.
- [[settings-staff]] — `marketing.subscribers` permission grant.
- [[subscriber-vs-customer]] — concept contrast.
- [[customer]] — entity; marketing-flip propagates from customer side.
- [[marketing-subscribers-custom-fields]] — custom-field definitions on subscribers.
- [[marketing-subscribers-subscribe-forms]] — storefront forms that create subscribers.
- [[background-queue-inventory]] — plan-cap recompute + consent-propagation tasks.
- [[checkout-flow]] — `FORCE_MARKETING_ON` / `FORCE_MARKETING_OFF` storefront override.

## Open questions

None.
