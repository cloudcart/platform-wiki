---
type: api-resource
resource_path: /api/v2/subscribers-channels
http_methods: [GET, POST, PATCH, DELETE]
related_entity: subscriber
related_features: [marketing-subscribers, marketing-channels, marketing-channels-email]
aliases: ["Subscriber Channels API CRUD", "subscribers-channels attributes", "subscribers-channels endpoints", "Subscriber channel attribute reference"]
tags: [api, json-api-v2, marketing]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[api-subscribers-channels]]. See the hub for the other aspects (channel rules & write side-effects, querying & testing).

# Subscriber Channels API — endpoints, attributes & CRUD

## Purpose

The endpoint shape, attribute reference, relationship, and plan-gating for the **per-channel deliverability rows** attached to a [[subscriber|Subscriber]]. This aspect answers "what can I read / write on a channel row, and what does each field mean". The semantic rules behind those fields (the `Email` / `Phone` allow-list, E.164 normalisation, what happens on `bounced` / `unsubscribed` flips) live on [[api-subscribers-channels-rules]]; read-side filtering, sorting, and the end-to-end testing recipe live on [[api-subscribers-channels-querying]].

Each row carries one channel's identifier (email address or phone number) plus that channel's marketing-consent and deliverability flags (verified, bounced).

## Endpoint

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/v2/subscribers-channels` | List channel rows across all subscribers. Supports filter / sort / include / page. |
| GET | `/api/v2/subscribers-channels/{id}` | Fetch one channel row. |
| POST | `/api/v2/subscribers-channels` | Create a channel row. Requires `subscriber_id` + `channel` + `channel_identifier` + `marketing` + `verified` + `bounced`. |
| PATCH | `/api/v2/subscribers-channels/{id}` | Update a channel row. The same field rules apply (`sometimes` on PATCH for the same set). |
| DELETE | `/api/v2/subscribers-channels/{id}` | Delete a channel row. The subscriber survives if other channels remain. Triggers a `remove_channel` history log entry on the parent subscriber. |
| GET | `/api/v2/subscribers-channels/{id}/subscriber` | Fetch the parent subscriber. |

No custom routes. No app-install gate at the route layer (the channels feature itself — Email / SMS-MsgHub / etc. — is gated separately at the channel-send infrastructure level; see [[marketing-channels]]).

Base URL details (host, auth, rate limit): see [[json-api-v2]] hub. All requests use `Accept: application/vnd.api+json`; body-carrying requests add `Content-Type: application/vnd.api+json`. Authenticate via `X-API-KEY` (see [[settings-api-keys]]).

## Attributes

| Attribute | Type | Writable on POST? | Writable on PATCH? | Required? | Notes / validation |
|---|---|---|---|---|---|
| `subscriber_id` | integer | yes | yes | **required**; must exist in the `subscribers` table | The parent Subscriber. Validated with `exists:subscribers,id`. |
| `channel` | string (enum) | yes | yes | **required**; must be `Email` or `Phone` | API allow-list is the platform code constant — currently `Email` + `Phone` ONLY. Sending `WebPush` or `Messenger` returns 422. See [[api-subscribers-channels-rules]]. |
| `channel_identifier` | string | yes | yes | **required**; format depends on `channel` | For `Email`: validated with the application framework's `email` rule. For `Phone`: any non-empty value, but **rewritten to E.164 format** by the validator before persistence — see [[api-subscribers-channels-rules]]. |
| `marketing` | integer `0` / `1` | yes | yes | **required** | Per-channel marketing consent. Distinct from any consent on the parent Subscriber row (there is none). Checked at campaign send time. |
| `verified` | integer `0` / `1` | yes | yes | **required** | Only meaningful for Email channels. Unverified addresses are excluded from most campaigns unless the email channel has the `unconfirmed_send` setting enabled. For Phone, the field is required by validation but functionally unused at send time. |
| `bounced` | integer `0` / `1` | yes | yes | **required** | Flag the channel as bounced (the email subsystem auto-sets this on hard bounce). Bounced channels are silently dropped from future sends. |
| `unsubscribed` | integer `0` / `1` | (writable via auto-fillable column) | (writable via auto-fillable column) | not in validator `rules` | The column exists on the row and is fillable; the validator does not declare it as required. Flipping to `1` excludes the channel from future sends (same effect as `bounced`). |
| `bounced_status` | string | **read-only** | **read-only** | — | Extended bounce-classification info (set by the email bounce-processor). Rejected on POST/PATCH. |
| `hash` | string | **read-only** | **read-only** | — | Internal opaque hash of the identifier (used in suppression / dedup paths). |
| `data` | json | **read-only** | **read-only** | — | Per-channel JSON metadata (e.g., WebPush subscription token payload, kept for legacy rows). |
| `identified_at` | datetime | **read-only** | **read-only** | — | When the identifier was first matched to a tracking cookie / device. |
| `created_at` / `updated_at` | datetime | — | — | — | Standard timestamps. |

## Relationships

| Name | Cardinality | Target type | Writable? | Notes |
|---|---|---|---|---|
| `subscriber` | hasOne | `subscribers` | read-only (set via `subscriber_id` attribute on create) | The parent [[subscriber\|Subscriber]] this channel row belongs to. See [[api-subscribers]]. |

The route registration declares `subscriber` as a hasMany (a quirk of how the relationship is registered); functionally each channel row has exactly one parent subscriber.

## Filtering & sorting

Filtering and sorting are documented in full on [[api-subscribers-channels-querying]]. In brief: every column is filterable (equality-only), and only `subscriber_id`, `channel`, `channel_identifier` are sortable; `include=subscriber` is the only include path.

## Side effects

Write side-effects (E.164 normalisation, the `CHANNELS_API` allow-list, bounce / unsubscribe flag behaviour, the `remove_channel` history entry on DELETE, automated-segment re-evaluation, webhook behaviour) are documented in full on [[api-subscribers-channels-rules]]. The CRUD-surface essentials:

- **DELETE** removes the row and returns **204 No Content**; the parent subscriber survives if other channels remain.
- **POST** returns **201 Created** with a `Location` header pointing at the new row.

## Plan-feature gating

- **No plan-feature gating at the API resource level.** The merchant's per-channel send infrastructure (Email / SMS / Viber / WebPush) is gated separately at send time; see [[marketing-channels-email]] / [[marketing-channels-sms-msghub]] / [[marketing-channels-sms-nth]] / [[marketing-channels-viber]] / [[marketing-channels-webpush]]. The API can create / read channel rows regardless of whether the merchant has the send infrastructure for that channel activated.
- **HTTP 402** — emitted only when the plan itself is expired / past-due / trial-ended.
- **HTTP 403** — not emitted by this resource.

## Example requests

### POST new Email channel

```bash
curl -sS -X POST \
  "https://<store-host>/api/v2/subscribers-channels" \
  -H "Accept: application/vnd.api+json" \
  -H "Content-Type: application/vnd.api+json" \
  -H "X-API-KEY: <YOUR_API_KEY>" \
  -d '{
    "data": {
      "type": "subscribers-channels",
      "attributes": {
        "subscriber_id": 12345,
        "channel": "Email",
        "channel_identifier": "ivan.petrov@example.com",
        "marketing": 1,
        "verified": 0,
        "bounced": 0
      }
    }
  }'
```

### PATCH — toggle marketing consent off

```bash
curl -sS -X PATCH \
  "https://<store-host>/api/v2/subscribers-channels/98765" \
  -H "Accept: application/vnd.api+json" \
  -H "Content-Type: application/vnd.api+json" \
  -H "X-API-KEY: <YOUR_API_KEY>" \
  -d '{
    "data": {
      "type": "subscribers-channels",
      "id": "98765",
      "attributes": {
        "marketing": 0
      }
    }
  }'
```

### DELETE

```bash
curl -sS -i -X DELETE \
  "https://<store-host>/api/v2/subscribers-channels/98765" \
  -H "Accept: application/vnd.api+json" \
  -H "X-API-KEY: <YOUR_API_KEY>"
```

DELETE removes the channel row and writes a `remove_channel` history entry on the parent subscriber. The subscriber survives if other channels remain. Returns **204 No Content**.

## Example responses

### GET single (200)

```json
{
  "data": {
    "type": "subscribers-channels",
    "id": "98765",
    "attributes": {
      "subscriber_id": 12345,
      "channel": "Email",
      "channel_identifier": "ivan.petrov@example.com",
      "marketing": 1,
      "verified": 0,
      "bounced": 0
    }
  }
}
```

### POST 201 Created

```
HTTP/1.1 201 Created
Location: https://<store-host>/api/v2/subscribers-channels/98766
```

```json
{
  "data": {
    "type": "subscribers-channels",
    "id": "98766",
    "attributes": {
      "subscriber_id": 12345,
      "channel": "Email",
      "channel_identifier": "ivan.petrov@example.com",
      "marketing": 1,
      "verified": 0,
      "bounced": 0
    }
  }
}
```

A paginated GET-collection example lives on [[api-subscribers-channels-querying]].

## Equivalent UI

- [[marketing-subscribers]] — subscriber detail → Channels tab; manual channel-row add / edit / delete.
- [[marketing-channels]] — channel management (which channels the store has activated at all — the send-infrastructure side).
- [[subscriber|Subscriber entity]] — full per-channel attribute reference.

## Related

- [[api-subscribers-channels]] — hub.
- [[json-api-v2]] — API hub.
- [[api-subscribers]] — parent Subscriber resource.
- [[api-subscribers-tags]] — subscriber-tag pivot.
- [[subscriber]] — Subscriber entity.
- [[settings-api-keys]] — authentication setup.

## Open questions

- Confirm the exact behaviour on duplicate `channel_identifier` POSTs (same Email / Phone already attached to another subscriber on the same store). The validator does not declare uniqueness; the model layer's merge-subscribers helpers exist but it's not verified whether THIS endpoint triggers them, returns 422, or hard-errors at the DB constraint.
- Confirm whether `unsubscribed` is intended to be a writable attribute via the API (it's fillable on the model, not declared in `rules`, and not in `readOnlyAttributes`) or whether it's only meant to be set internally by the suppression / one-click-unsubscribe pipeline.
