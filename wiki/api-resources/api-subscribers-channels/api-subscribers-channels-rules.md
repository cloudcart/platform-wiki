---
type: api-resource
resource_path: /api/v2/subscribers-channels
http_methods: [POST, PATCH, DELETE]
related_entity: subscriber
related_features: [marketing-subscribers, marketing-channels, marketing-segments]
aliases: ["Subscriber Channels API rules", "subscribers-channels write side-effects", "CHANNELS_API allow-list", "Channel E.164 normalisation", "Channel consent and bounce rules"]
tags: [api, json-api-v2, marketing]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[api-subscribers-channels]]. See the hub for the other aspects (endpoints & attributes, querying & testing).

# Subscriber Channels API — channel rules & write side-effects

## Purpose

The semantic rules that govern writes to the **per-channel deliverability rows** of a [[subscriber|Subscriber]]: which channels the API may touch, how identifiers are validated and rewritten, and every side-effect a POST / PATCH / DELETE produces beyond persisting the row. The endpoint shape and attribute reference live on [[api-subscribers-channels-crud]]; read-side filtering / sorting / testing live on [[api-subscribers-channels-querying]].

## Endpoint

These rules apply to the write methods of `/api/v2/subscribers-channels`:

| Method | Path | Rules that apply |
|---|---|---|
| POST | `/api/v2/subscribers-channels` | Channel allow-list, identifier validation, E.164 normalisation, segment re-evaluation. |
| PATCH | `/api/v2/subscribers-channels/{id}` | Same validation; bounce / unsubscribe flag semantics; segment re-evaluation. |
| DELETE | `/api/v2/subscribers-channels/{id}` | `remove_channel` history entry; subscriber survives if other channels remain. |

See [[api-subscribers-channels-crud]] for the full method table and [[json-api-v2]] for base URL / auth.

## Attributes

The fields whose **behaviour** (as opposed to declaration) these rules govern. The full attribute table is on [[api-subscribers-channels-crud]].

- `channel` — constrained to the platform code allow-list (see below).
- `channel_identifier` — validated and, for Phone, rewritten (see below).
- `marketing` — per-channel consent; **no row-level `marketing` flag exists on the Subscriber itself** — consent is managed per channel.
- `verified` / `bounced` / `unsubscribed` — deliverability flags that gate send-time eligibility.

At campaign send time, the pipeline filters on `marketing = 1 AND bounced = 0 AND unsubscribed = 0 AND (verified = 1 OR channel.unconfirmed_send setting is on)`.

## Relationships

Writes here mutate the parent [[subscriber|Subscriber]] as a side-effect: the subscriber's `updated_at` touches on every channel-row save (see "Side effects" below). The relationship declaration itself is on [[api-subscribers-channels-crud]].

## Filtering & sorting

Not applicable to this aspect — it covers write behaviour only. Read-side filter / sort / include parameters are on [[api-subscribers-channels-querying]].

## Side effects

### Channel allow-list enforcement

**API-allowed channels are `Email` and `Phone` only** (the platform code allow-list). WebPush and Messenger rows DO exist on subscribers — they are created by storefront subscription flows (webpush prompt, Messenger opt-in) and consumed by the campaign-send pipeline — but they cannot be created or modified through this API resource. Sending `channel = "WebPush"`, `channel = "Messenger"`, or any other value returns **422** with the localised allow-list error on `/data/attributes/channel`.

### Phone → E.164 normalisation

On POST/PATCH where `channel = "Phone"`, the validator parses `channel_identifier` through libphonenumber and **rewrites it to E.164 format** (`+CCNNNNNNNNNN`) before persistence. A merchant who PATCHes `+359 88 555 1234` sees `+359885551234` on the next GET. Examples: `+359 87 123 4567` → `+359871234567`; `+1 (415) 555-1234` → `+14155551234`. Malformed numbers that libphonenumber cannot parse currently produce a server-side parse exception (a 500) rather than a clean 422 — see Open questions.

### Email format validation

When `channel = "Email"`, `channel_identifier` must pass the application framework's `email` validator. Bad emails return 422 with `source.pointer = "/data/attributes/channel_identifier"`.

### Identifier dedup is NOT enforced by the API validator

The validator does not declare a uniqueness rule on `channel_identifier`. Whether the underlying DB has a unique index (and what happens on a collision — silent merge, hard-error 500, or 422) is unverified at this layer; see Open questions.

### Bounce / unsubscribed flag changes

Flipping `bounced` or `unsubscribed` does NOT delete the row; the channel survives but is excluded from future sends. Flipping back to `0` re-enables sends — use with care, since re-enabling a previously bounced address can damage the store's sender reputation.

### DELETE writes a `remove_channel` history entry

The model's `deleted` hook logs `remove_channel` on the parent subscriber with the channel / identifier / marketing / verified / hash / data snapshot. This shows up in the subscriber's audit trail on [[marketing-subscribers]]. The subscriber survives if other channels remain.

### Automated-segment re-evaluation

Channel-row writes touch the parent subscriber's `updated_at` and re-trigger Automated-segment evaluation for that subscriber (`subscriber.has_channel`, `subscriber.email_marketing`, etc., re-evaluate within seconds — see [[marketing-segments]] business rules).

### Webhook behaviour — no dedicated channel events

Only `subscriber.*` events fire from the parent Subscriber lifecycle. Channel-row writes do NOT produce dedicated `subscriber_channel.created` / `.updated` / `.deleted` events. To listen for channel-state changes via webhooks, subscribe to `subscriber.updated` on [[settings-hooks]] — it fires when the subscriber's `updated_at` touches as a side effect of channel saves.

### No dedicated audit-log capture

Beyond the `remove_channel` entry on DELETE, channel POST/PATCH operations have no actor-identity audit log.

## Equivalent UI

- [[marketing-subscribers]] — subscriber detail → Channels tab; the same allow-list, normalisation, and bounce/unsubscribe semantics apply when a merchant edits a channel row by hand.
- [[marketing-channels-email]] / [[marketing-channels-sms-msghub]] / [[marketing-channels-sms-nth]] / [[marketing-channels-viber]] / [[marketing-channels-webpush]] — per-channel send infrastructure (this API manages recipient-side rows only; it does NOT send messages).
- [[marketing-segments]] — Automated segments that re-evaluate on channel writes.

## Related

- [[api-subscribers-channels]] — hub.
- [[json-api-v2]] — API hub.
- [[api-subscribers]] — parent Subscriber resource.
- [[settings-hooks]] — webhook subscriptions (no dedicated channel-level events; subscribe to `subscriber.updated`).
- [[marketing-subscribers]] — subscriber audit trail (where `remove_channel` lands).
- [[subscriber]] — Subscriber entity.

## Open questions

- Verify whether `verified = 1` set via the API skips the email double-opt-in confirmation the storefront subscribe-form normally enforces (i.e., does the API let integrations bypass deliverability verification, and if so, is that audit-logged?).
- Verify the failure mode when `channel = "Phone"` and `channel_identifier` cannot be parsed by libphonenumber — currently the validator's `validatorForResource` calls `$phoneUtil->parse(...)` unconditionally and a parse failure throws, which may produce a 500 instead of a clean 422. A defensive try/catch would yield a better error.
- Confirm the exact behaviour on duplicate `channel_identifier` POSTs (same Email / Phone already attached to another subscriber on the same store) — silent merge, 422, or DB-constraint 500.
