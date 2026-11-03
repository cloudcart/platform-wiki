---
type: api-resource
resource_path: /api/v2/subscribers-channels
http_methods: [GET, POST, PATCH, DELETE]
related_entity: subscriber
related_features: [marketing-subscribers, marketing-channels, marketing-channels-email, marketing-channels-sms-msghub, marketing-channels-sms-nth, marketing-channels-viber, marketing-channels-webpush]
aliases: ["Subscriber Channels API", "JSON-API v2 subscribers-channels", "API канали на абонат", "/subscribers-channels"]
tags: [api, json-api-v2, marketing]
plan_gates: []
created: 2026-05-26
updated: 2026-06-10
source_count: 3
---
# Subscriber Channels (JSON-API v2)

## Purpose

Programmatic CRUD on the **per-channel deliverability rows** attached to a [[subscriber|Subscriber]]. Each row carries one channel's identifier (email address or phone number) plus that channel's marketing-consent and deliverability flags (verified, bounced).

Integrations use this endpoint to:

- **Add a second channel to an existing subscriber** — e.g., the subscriber opted into Email and now also into SMS.
- **Mark a channel as bounced** when an external suppression list flags it.
- **Flip `verified = 1` after an external double-opt-in flow completes** (for Email channels).
- **Read deliverability state** before deciding whether to send through CloudCart.

**API-allowed channels are `Email` and `Phone` only** (the platform code allow-list). WebPush and Messenger rows DO exist on subscribers but cannot be created or modified through this API resource — see [[api-subscribers-channels-rules]] for the full allow-list mechanics. A channel's `marketing` flag is the per-channel consent; there is **no row-level `marketing` flag on the Subscriber itself**.

This resource is documented across three aspect pages. Drill into the one that matches the question.

## Sub-pages (in this cluster)

- [[api-subscribers-channels-crud]] — the endpoint method table; the full attribute reference (writable / read-only / required); the `subscriber` relationship; plan-feature gating; example POST / PATCH / DELETE requests and 200 / 201 responses.
- [[api-subscribers-channels-rules]] — channel rules & write side-effects: the `Email` / `Phone` allow-list, Phone → E.164 normalisation, email-format validation, bounce / unsubscribe flag behaviour, the `remove_channel` DELETE history entry, automated-segment re-evaluation, and webhook behaviour (no dedicated channel events).
- [[api-subscribers-channels-querying]] — the read side: allowed filter / sort / include parameters, the common 422 error shapes, a paginated GET-collection response, and the end-to-end CRUD testing checklist.

## Endpoint

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/v2/subscribers-channels` | List channel rows. Supports filter / sort / include / page — see [[api-subscribers-channels-querying]]. |
| GET | `/api/v2/subscribers-channels/{id}` | Fetch one channel row. |
| POST | `/api/v2/subscribers-channels` | Create a channel row — see [[api-subscribers-channels-crud]]. |
| PATCH | `/api/v2/subscribers-channels/{id}` | Update a channel row. |
| DELETE | `/api/v2/subscribers-channels/{id}` | Delete a channel row; the subscriber survives if other channels remain — see [[api-subscribers-channels-rules]]. |
| GET | `/api/v2/subscribers-channels/{id}/subscriber` | Fetch the parent subscriber. |

No custom routes. No app-install gate at the route layer. Base URL details (host, auth, rate limit): see [[json-api-v2]] hub.

## Attributes

A channel row carries `subscriber_id`, `channel` (`Email` / `Phone`), `channel_identifier`, the consent / deliverability flags `marketing` / `verified` / `bounced` / `unsubscribed`, and the read-only `bounced_status` / `hash` / `data` / `identified_at` / `created_at` / `updated_at`. The full per-field table (type, writable-on-POST / PATCH, required, validation) is on [[api-subscribers-channels-crud]].

## Relationships

`subscriber` (hasOne; set via `subscriber_id` on create) — the parent [[subscriber|Subscriber]] this channel row belongs to. See [[api-subscribers-channels-crud]] for the declaration detail and [[api-subscribers]] for the parent resource.

## Filtering & sorting

Equality-only filtering on every column; sortable on `subscriber_id` / `channel` / `channel_identifier` only; `include=subscriber` is the one include path. Full parameter list on [[api-subscribers-channels-querying]].

## Side effects

Writes normalise Phone identifiers to E.164, enforce the `Email` / `Phone` allow-list, re-evaluate automated segments, and (on DELETE) log a `remove_channel` history entry on the parent subscriber. There are no dedicated channel-level webhooks — subscribe to `subscriber.updated`. Full catalogue on [[api-subscribers-channels-rules]].

## Equivalent UI

- [[marketing-subscribers]] — subscriber detail → Channels tab; manual channel-row add / edit / delete.
- [[marketing-channels]] — channel management (which channels the store has activated at all — the send-infrastructure side).
- [[marketing-channels-email]] / [[marketing-channels-sms-msghub]] / [[marketing-channels-sms-nth]] / [[marketing-channels-viber]] / [[marketing-channels-webpush]] — per-channel send infrastructure (this API does NOT send messages — it manages the recipient-side rows only).
- [[subscriber|Subscriber entity]] — full per-channel attribute reference.

## Related

- [[json-api-v2]] — API hub.
- [[api-subscribers]] — parent Subscriber resource.
- [[api-subscribers-tags]] — subscriber-tag pivot.
- [[settings-hooks]] — webhook subscriptions (no dedicated channel-level events; subscribe to `subscriber.updated`).
- [[settings-api-keys]] — authentication setup.

## Open questions

- Confirm the exact behaviour on duplicate `channel_identifier` POSTs — see [[api-subscribers-channels-crud]] / [[api-subscribers-channels-rules]].
- Verify whether `verified = 1` set via the API skips the storefront email double-opt-in — see [[api-subscribers-channels-rules]].
- Verify the libphonenumber parse-failure mode (500 vs clean 422) — see [[api-subscribers-channels-rules]].
- Confirm whether `unsubscribed` is intended to be writable via the API — see [[api-subscribers-channels-crud]].
