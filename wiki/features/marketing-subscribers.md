---
type: feature
nav_path: "Marketing → Subscribers"
route_name: subscribers.list
route_path: /admin/marketing-new/subscribers
aliases: ["Subscribers", "Newsletter subscribers", "Audience", "Абонати", "Маркетинг абонати"]
tags: [marketing, subscribers, channels, contacts]
plan_gates: ["subscribers"]
created: 2026-05-21
updated: 2026-06-10
source_count: 13
---
# Subscribers

## Purpose

A merchant-facing CRM of every person CloudCart has identified as **subscribed to the store's marketing on at least one channel** — Email, SMS / Phone, Web Push, or Messenger. Subscribers are CloudCart's central marketing-audience record: anyone who fills in a [[marketing-subscribers-subscribe-forms]] popup, registers as a [[customer]], orders, leaves an abandoned cart, or even just gets identified by a tracking UUID becomes a Subscriber (or merges into an existing one).

A subscriber is **distinct from a customer** (see [[subscriber-vs-customer]]) — a subscriber may have never bought anything (just signed up for the newsletter), and a single subscriber can be linked to multiple customer accounts (same email used across logins). The Subscribers page is the merchant's hub for managing the audience pool, channel subscriptions, tags, custom fields, RFM analytics, CSV import, and the cross-store marketing settings.

## Where to find it

Sidebar → **Marketing** → **Subscribers**.

The route is `/admin/marketing-new/subscribers`. Adjacent routes:

- `/admin/marketing-new/subscribers/fields` — custom fields applied to subscribers ([[marketing-subscribers-custom-fields]]).
- `/admin/marketing-new/subscribers/:id` — single subscriber detail view (loads inline as a modal — see [[subscribers-detail-modal]]).

## Sub-pages (in this cluster)

This feature is split into 7 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[subscribers-list-view]] — list columns, the 9 filter options, search, and the page-header strip (Import / Settings / Limits buttons).
- [[subscribers-bulk-actions]] — bulk delete, bulk-tag (`SubscribersTagsModal`), bulk-accept-marketing / bulk-decline-marketing; per-row Log / Delete / "Accepts marketing" toggle; side-effects on linked customers and segments.
- [[subscribers-detail-modal]] — `SubscribersDetailsModal` (channels card, statistics, tags, UUIDs, segments, linked customers, activity log) + the per-channel `MarketingChannelsLogChannelEditModal`.
- [[subscribers-channels]] — the 4 channel constants (`Email` / `Phone` / `Messenger` / `WebPush`), channel-identifier uniqueness, the merge flow, identity resolution (channel → customer → uuid → parent) on the platform code.
- [[subscribers-import]] — the 4-step CSV-import wizard (`SubscribersImportModal`), 2FA gate (`EXPORT_IMPORT_ACTION_IMPORT_SUBSCRIBERS`), 8 mappable fields, two-source tag stacking, plan-cap truncation.
- [[subscribers-settings]] — `SubscribersSettingsModal` (GDPR marketing / Revenue statuses / Bestseller interval / RFM interval) + `SubscribersLimitsModal` + RFM bucket catalogue + the 12-hour `subscribers_rfm` recompute cadence.
- [[subscribers-lifecycle]] — source taxonomy (`subscriber_from`), marketing-consent capture, email verification, webhooks (`subscriber.created` / `updated` / `deleted`), GDPR erasure cascade, permission gating, plan-tier subscriber cap.

Custom fields and subscribe-forms each have their own existing clusters and are NOT duplicated here:

- [[marketing-subscribers-custom-fields]] — per-subscriber custom-field definition screen.
- [[marketing-subscribers-subscribe-forms]] — storefront popup / form builder hub.

## What the merchant can do here

The Subscribers page is a launching point for everything in the cluster:

- See the full subscriber list with channels, marketing-consent, country, tags, and last-active date — see [[subscribers-list-view]].
- Filter & search by name, email, country, channel, segment, campaign, source, and tags — see [[subscribers-list-view]].
- Click any row to open the detail modal (channels, customers linked, segments, UUIDs, engagement stats, activity log) — see [[subscribers-detail-modal]].
- Bulk-edit selected rows (tag, accept / decline marketing, delete) — see [[subscribers-bulk-actions]].
- Import subscribers from CSV behind a 2FA challenge — see [[subscribers-import]].
- Configure cross-store settings (RFM interval, revenue-counting statuses, bestseller period, second-marketing rule) — see [[subscribers-settings]].
- Manage custom fields — see [[marketing-subscribers-custom-fields]].
- See plan-feature limits + "Upgrade" CTAs — see [[subscribers-settings]].
- Audit per-subscriber activity (subscribe / unsubscribe / channel changes / RFM moves / tag edits) — see [[subscribers-detail-modal]] and the RFM Log screen (`admin.subscribers.rfm.log`).

## Settings & fields

The Subscribers cluster touches four configuration surfaces:

- **List & filter state** — column visibility, the 9 filter keys, per-row actions. See [[subscribers-list-view]].
- **Channel-edit fields** — `channel_identifier`, `verified`, `marketing`, `bounced`, `unsubscribed` per channel. See [[subscribers-channels]].
- **Cross-store settings** — `second_marketing`, `revenue_statuses`, `bestseller_period`, `rfm_interval`. See [[subscribers-settings]].
- **Import-wide options** — 2FA gate, header-row toggle, common tags, marketing-mark, verification method. See [[subscribers-import]].

## Business rules

The cluster's invariants live in their respective aspect pages. The cross-cutting rules every page references:

- **Subscriber ≠ Customer.** A subscriber can exist with no customer; one subscriber can link to multiple customers (`subscriber_to_customer`). See [[subscriber-vs-customer]] + [[subscribers-lifecycle]].
- **Identity resolves in a 4-step cascade** — channel match → customer match → uuid match → explicit parent id — before a new subscriber row is created. An anonymous visitor identified by uuid who later enters an email merges into the cookie-tracked row. See [[subscribers-channels]].
- **Channel-identifier uniqueness is enforced per channel.** Duplicate-identifier collision triggers the merge flow (`admin.subscribers.channels.merge`). See [[subscribers-channels]].
- **Plan cap is chronological, not random.** The `subscribers.max_id` setting (recomputed every 10 minutes) stores the Nth subscriber id; segment evaluators silently exclude newer ids. See [[subscribers-lifecycle]] + [[subscribers-settings]].
- **Marketing flip is asymmetric.** Customer `yes → no` propagates to every per-channel subscriber row; `no → yes` does NOT auto-flip back — opt-in is explicit per channel. See [[subscribers-lifecycle]].
- **RFM recompute is single-flighted every 12 hours.** No on-demand "recalculate now" button — the merchant waits, or relies on per-event re-evaluation. See [[subscribers-settings]].
- **Permission gate** — `hasApiPermission:marketing,marketing.subscribers`. See [[subscribers-lifecycle]].

## Programmatic access

Subscribers, their per-channel rows, and their tags can be managed via **JSON-API v2** — see [[api-subscribers]], [[api-subscribers-channels]], and [[api-subscribers-tags]]. Segments are exposed at [[api-segments]] but read-only (the rule tree is admin-panel-only via [[marketing-segments-editor]]).

Same side effects apply. A POST / PATCH through JSON-API v2 triggers the same downstream pipeline as the admin-panel save: `subscribers.max_id` plan-cap check, automated-segment membership re-evaluation, shared `customer_tags` dictionary updates, phone-number normalisation to E.164 via libphonenumber, and `subscriber.created` / `subscriber.updated` / `subscriber.deleted` webhook dispatch via [[settings-hooks]]. API-created subscribers land with `subscribed_from = 'API'`. The plan's subscriber cap applies identically.

See [[json-api-v2]] for authentication, rate limits, and the side-effects principle.

## Related

- [[marketing]] — parent hub.
- [[marketing-segments]] — primary consumer; segments group subscribers by rules.
- [[marketing-subscribers-subscribe-forms]] — storefront forms that create subscribers.
- [[marketing-subscribers-custom-fields]] — per-subscriber custom-field definitions.
- [[marketing-campaigns]] — uses subscribers as targets; reads their channel / marketing / verified state.
- [[apps-mailchimp]] — sync target for subscriber lists.
- [[settings-hooks]] — webhook events emitted for subscriber lifecycle.
- [[settings-staff]] — moderator permission grants for `marketing.subscribers`.
- [[subscriber-vs-customer]] — concept page distinguishing the two.
- [[customer]] — entity page; subscribers may link to customers.
- [[subscriber]] — entity page.
- [[notification-delivery]] — concept page on how channel sends are dispatched.
- [[background-queue-inventory]] — catalogue of all background processes; covers the every-10-minute subscriber-cap recomputation, 300-second segment-membership rebuild, 12-hour RFM recompute, and async subscriber CSV imports.

## Open questions

No outstanding questions.
