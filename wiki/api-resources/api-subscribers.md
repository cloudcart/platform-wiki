---
type: api-resource
resource_path: /api/v2/subscribers
http_methods: [GET, POST, PATCH, DELETE]
related_entity: subscriber
related_features: [marketing-subscribers, marketing-subscribers-custom-fields, marketing-subscribers-subscribe-forms, marketing-segments, marketing-channels]
aliases: ["Subscribers API", "JSON-API v2 subscribers", "API абонати", "/subscribers"]
tags: [api, json-api-v2, marketing]
plan_gates: ["subscribers"]
created: 2026-05-26
updated: 2026-06-10
source_count: 3
---
# Subscribers (JSON-API v2)

## Purpose

Programmatic CRUD on the merchant's marketing audience — the [[subscriber|Subscribers]] who form the targeting pool for [[marketing-campaigns]] and [[marketing-segments]]. External integrations use this endpoint to **push contacts in from external CRM / ESP / lead-generation tools**, **sync the subscriber list out to a data warehouse**, **bulk-update tag / channel state**, and **read the current audience** for downstream analytics.

A Subscriber is **distinct from a [[customer|Customer]]** (see [[subscriber-vs-customer]]) — this endpoint operates on the marketing-consent audience, not the buyer audience. A Subscriber needs at least one channel row (see [[api-subscribers-channels]]) to be reachable; the subscriber row itself carries identity (name, country) but no contact identifier.

Subscribers created here are tagged with `subscribed_from = "API"` (automatically forced by the adapter when the caller doesn't supply a source) — the *"Subscribed from"* filter on [[marketing-subscribers]] surfaces them under that bucket, and the `subscriber.from` segment condition can target them.

This resource is large enough that it is split into a hub (this page) + aspect pages. This page is the navigation pivot; drill into the aspect that matches the question.

## Sub-pages (in this cluster)

- [[api-subscribers-list-crud]] — endpoint table, full attribute reference, the two relationships (`channels`, `tags`), and the POST / PATCH / DELETE request + response examples.
- [[api-subscribers-list-querying]] — filtering (the custom `filter[segment]` join, equality-only column filters), allowed sort keys, include paths, and read-side GET examples.
- [[api-subscribers-list-effects]] — write side-effects: `subscribed_from` auto-fill, `subscriber.*` webhooks, the silent `subscribers.max_id` plan cap, segment re-evaluation, DELETE cascade, the no-audit-log gap, plus the CRUD testing checklist.

(Per-channel deliverability/consent rows and the subscriber-tag pivot are separate resources: [[api-subscribers-channels]] and [[api-subscribers-tags]].)

## Endpoint

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/v2/subscribers` | List subscribers. Supports filter / sort / include / page. |
| GET | `/api/v2/subscribers/{id}` | Fetch one subscriber. |
| POST | `/api/v2/subscribers` | Create a subscriber. The adapter force-sets `subscribed_from = "API"` when omitted. |
| PATCH | `/api/v2/subscribers/{id}` | Update a subscriber. |
| DELETE | `/api/v2/subscribers/{id}` | Delete a subscriber. Cascades — see [[api-subscribers-list-effects]]. |
| GET / POST / PATCH / DELETE | `/api/v2/subscribers/{id}/relationships/<rel>` | Manage the `channels` and `tags` relationships in linkage-only form. |
| GET | `/api/v2/subscribers/{id}/<rel>` | Fetch related `channels` or `tags` as full resources. |

No custom routes. No app-install gate. Base URL details (host, auth, rate limit): see [[json-api-v2]] hub. Full method-by-method examples are on [[api-subscribers-list-crud]] (writes) and [[api-subscribers-list-querying]] (reads).

## Attributes

The Subscriber row carries identity (`country` — **required on POST**, `first_name`, `last_name`), an optional `customer_id` link, the `subscribed_from` source bucket, and a block of read-only campaign metrics (`total_sent`, `open_rate`, `click_rate`, `last_active_at`, etc.). `password` / `remember_token` are hidden from API responses. **`marketing` consent and `verified` / `bounced` deliverability flags are NOT on the subscriber row — they live on the per-channel rows ([[api-subscribers-channels]]).**

Full per-attribute table (writability on POST/PATCH, validation, read-only set, NULL semantics): see [[api-subscribers-list-crud]].

## Relationships

| Name | Cardinality | Target type | Writable? |
|---|---|---|---|
| `channels` | hasMany | `subscribers-channels` | writable (Email + Phone only via API) — see [[api-subscribers-channels]] |
| `tags` | hasMany | `subscribers-tags` | writable via relationship endpoints — see [[api-subscribers-tags]] |

Both relationships are includable. Full notes (the WebPush/Messenger allow-list, the `belongsTo` internal quirk on `tags`): see [[api-subscribers-list-crud]].

## Filtering & sorting

`filter[segment]` is a custom join filter (segment ID → members of that [[segment|Segment]]); every `subscribers` column is otherwise auto-allowed as an equality-only filter. Sort is restricted to `id`, `first_name`, `last_name`, `country`. Includes: `channels`, `tags` (no nested includes). Full detail + worked GET examples: see [[api-subscribers-list-querying]].

## Side effects

Writes auto-fill `subscribed_from = "API"`, fire `subscriber.created` / `subscriber.updated` / `subscriber.deleted` webhooks, trigger incremental segment re-evaluation, and apply the **silent** `subscribers.max_id` plan cap (over-cap subscribers are created but excluded from every segment/campaign — no HTTP 402 at this layer). DELETE cascades across channels, tags, segment memberships, and order/cart pointers. There is no dedicated audit-log capture. Full detail + the silent-cap worked scenario + testing checklist: see [[api-subscribers-list-effects]].

## Equivalent UI

- [[marketing-subscribers]] — subscriber list (mirrors `GET /api/v2/subscribers`).
- [[marketing-subscribers-custom-fields]] — custom-field admin (field DEFINITIONS are admin-panel-only; field VALUES are not yet exposed through this resource).
- [[marketing-subscribers-subscribe-forms]] — storefront subscribe forms (no captcha/rate-limit; apply rate limiting at the integration layer too).
- [[subscriber|Subscriber entity]] — full attribute reference.

## Related

- [[json-api-v2]] — API hub: auth, rate limit, side-effects principle.
- [[api-subscribers-list-crud]] — attributes, relationships, write examples (this cluster).
- [[api-subscribers-list-querying]] — filtering, sorting, includes, read examples (this cluster).
- [[api-subscribers-list-effects]] — write side-effects, plan cap, cascade, testing (this cluster).
- [[api-subscribers-channels]] — per-channel deliverability + consent rows. A subscriber needs at least one channel row to be reachable.
- [[api-subscribers-tags]] — subscriber-tag pivot.
- [[api-segments]] — read-only segments resource.
- [[api-customers]] — Customer resource (distinct from Subscriber — see [[subscriber-vs-customer]]).
- [[api-customer-tags]] — shared tag-dictionary (subscriber tags reuse the customer-tag table).
- [[settings-hooks]] — webhook subscriptions for `subscriber.*` events.
- [[settings-api-keys]] — authentication setup.

## Open questions

- Confirm whether `subscriber.created` / `subscriber.updated` webhooks fire reliably from JSON-API v2 writes end-to-end (the events are wired through `register_shutdown_function` from the model layer; admin-panel saves and storefront subscribe-form submits both fire them, but the API path's shutdown-hook delivery should be verified under load).
- Verify whether the silent `subscribers.max_id` cap is reflected in any header or warning that the API caller could surface to the merchant proactively, or whether the only signal is "subscriber created but missing from segments".
- Verify whether `marketing` / `gdpr_accepted` consent state is ever needed at the subscriber-row level for any integration use case. Today, both consents are managed exclusively via channel rows ([[api-subscribers-channels]] `marketing` field).
