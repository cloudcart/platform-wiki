---
type: api-resource
resource_path: /api/v2/subscribers-channels
http_methods: [GET]
related_entity: subscriber
related_features: [marketing-subscribers, marketing-channels]
aliases: ["Subscriber Channels API querying", "subscribers-channels filtering and sorting", "subscribers-channels error examples", "subscribers-channels testing checklist"]
tags: [api, json-api-v2, marketing]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[api-subscribers-channels]]. See the hub for the other aspects (endpoints & attributes, channel rules & write side-effects).

# Subscriber Channels API — filtering, sorting & testing

## Purpose

The read side of the **per-channel deliverability rows** endpoint: which filter, sort, and include parameters are accepted; the common 422 error shapes; a paginated collection response; and an end-to-end CRUD testing recipe. The endpoint shape and attribute reference live on [[api-subscribers-channels-crud]]; the semantic write rules live on [[api-subscribers-channels-rules]].

## Endpoint

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/v2/subscribers-channels` | List channel rows across all subscribers. Supports filter / sort / include / page. |
| GET | `/api/v2/subscribers-channels/{id}` | Fetch one channel row. |
| GET | `/api/v2/subscribers-channels/{id}/subscriber` | Fetch the parent subscriber. |

See [[api-subscribers-channels-crud]] for the full method table (including POST / PATCH / DELETE) and [[json-api-v2]] for base URL / auth.

## Attributes

The readable attributes returned in responses are the same set documented on [[api-subscribers-channels-crud]] (`subscriber_id`, `channel`, `channel_identifier`, `marketing`, `verified`, `bounced`, `unsubscribed`, plus the read-only `bounced_status`, `hash`, `data`, `identified_at`, `created_at`, `updated_at`). This aspect covers which of those can be used as filter / sort keys.

## Relationships

`subscriber` (hasOne) is the only relationship and the only includable path — `include=subscriber` sideloads the parent [[subscriber|Subscriber]]. See [[api-subscribers-channels-crud]] for the relationship declaration.

## Filtering & sorting

### Allowed filtering parameters

No bespoke filter scopes are declared. Every column on the `subscribers_channels` row is auto-allowed (framework default): `filter[id]`, `filter[subscriber_id]`, `filter[channel]`, `filter[channel_identifier]`, `filter[marketing]`, `filter[verified]`, `filter[bounced]`, `filter[unsubscribed]`, `filter[hash]`, `filter[identified_at]`, `filter[created_at]`, `filter[updated_at]`.

Filtering is equality-only — there is no comparison-operator syntax (see [[json-api-v2]] hub).

### Allowed sort parameters

`subscriber_id`, `channel`, `channel_identifier`. Prefix with `-` for descending.

Sorting on `id`, `created_at`, `bounced`, etc., returns 422 — only the three declared keys are allowed.

### Allowed include paths

`include=subscriber` — sideloads the parent subscriber. No nested includes are declared.

## Side effects

GET requests have no side effects. Write-side effects (E.164 normalisation, segment re-evaluation, the `remove_channel` history entry, webhook behaviour) are documented on [[api-subscribers-channels-rules]].

## Example requests

### GET collection filtered by subscriber

```bash
curl -sS -X GET \
  "https://<store-host>/api/v2/subscribers-channels?filter[subscriber_id]=12345&include=subscriber" \
  -H "Accept: application/vnd.api+json" \
  -H "X-API-KEY: <YOUR_API_KEY>"
```

## Example responses

### GET collection (200) — paginated

```json
{
  "data": [
    {
      "type": "subscribers-channels",
      "id": "98765",
      "attributes": {
        "subscriber_id": 12345,
        "channel": "Email",
        "channel_identifier": "ivan.petrov@example.com",
        "marketing": 1,
        "verified": 0,
        "bounced": 0,
        "unsubscribed": 0,
        "created_at": "2026-06-05T09:12:44+00:00",
        "updated_at": "2026-06-05T09:12:44+00:00"
      },
      "relationships": {
        "subscriber": {
          "links": { "related": "https://<store-host>/api/v2/subscribers-channels/98765/subscriber" }
        }
      }
    },
    {
      "type": "subscribers-channels",
      "id": "98766",
      "attributes": {
        "subscriber_id": 12345,
        "channel": "Phone",
        "channel_identifier": "+359871234567",
        "marketing": 1,
        "verified": 0,
        "bounced": 0,
        "unsubscribed": 0
      }
    }
  ],
  "meta": {
    "page": {
      "current-page": 1,
      "per-page": 10,
      "from": 1,
      "to": 2,
      "total": 2,
      "last-page": 1
    }
  }
}
```

### Common 422 cases

- **Missing required field on POST** — `{"errors":[{"status":"422","title":"Unprocessable Entity","detail":"The subscriber id field is required","source":{"pointer":"/data/attributes/subscriber_id"}}]}` (and similarly for `channel`, `channel_identifier`, `marketing`, `verified`, `bounced`).
- **Non-existent `subscriber_id`** — `"The selected subscriber id is invalid"` (the application framework `exists` rule failure).
- **Invalid `channel`** — sending `WebPush` or any value outside `Email` / `Phone` → `"The selected channel is invalid"` with the allow-list shown (see [[api-subscribers-channels-rules]]).
- **Bad email format** — `channel = "Email"`, `channel_identifier = "not-an-email"` → 422 on `channel_identifier`.
- **Read-only attribute on POST/PATCH** — sending `bounced_status`, `hash`, `data`, or `identified_at` → `"The <field> field is read only"`.
- **Invalid sort key** — `sort=created_at` → 422 (only `subscriber_id`, `channel`, `channel_identifier` are allowed).

### 422 — invalid `channel`

```json
{
  "errors": [
    {
      "status": "422",
      "title": "Unprocessable Entity",
      "detail": "The selected channel is invalid",
      "source": { "pointer": "/data/attributes/channel" }
    }
  ]
}
```

## Testing checklist

End-to-end CRUD verification (assumes an existing subscriber id `{SUB_ID}` — create one via [[api-subscribers]] first):

```
1. GET /api/v2/subscribers-channels?filter[subscriber_id]={SUB_ID}
   — confirm 200 and the channel set you expect.
2. POST /api/v2/subscribers-channels with:
     subscriber_id = {SUB_ID}
     channel = "Email"
     channel_identifier = "test+api@example.com"
     marketing = 1, verified = 0, bounced = 0
   — expect 201; capture `data.id` as {EMAIL_CH_ID}.
3. POST /api/v2/subscribers-channels with:
     subscriber_id = {SUB_ID}
     channel = "Phone"
     channel_identifier = "+359 87 123 4567" ← with spaces
     marketing = 1, verified = 0, bounced = 0
   — expect 201; capture `data.id` as {PHONE_CH_ID}.
4. GET /api/v2/subscribers-channels/{PHONE_CH_ID}
   — verify `channel_identifier == "+359871234567"` (E.164 normalised — no spaces, leading "+").
5. POST /api/v2/subscribers-channels with:
     subscriber_id = {SUB_ID}
     channel = "WebPush"
     channel_identifier = "any"
     marketing = 1, verified = 0, bounced = 0
   — expect 422 on /data/attributes/channel with "The selected channel is invalid".
6. Repeat step 5 with channel = "Messenger" — same 422.
7. PATCH /api/v2/subscribers-channels/{EMAIL_CH_ID} with attributes.marketing = 0
   — expect 200; verify on a follow-up GET.
8. PATCH /api/v2/subscribers-channels/{EMAIL_CH_ID} with attributes.marketing = 1
   — toggle back; verify.
9. DELETE /api/v2/subscribers-channels/{EMAIL_CH_ID}
   — expect 204. The parent subscriber survives (Phone row still exists).
10. GET /api/v2/subscribers-channels?filter[subscriber_id]={SUB_ID}
    — verify only the Phone row remains.
```

### Edge cases

- **`CHANNELS_API` allow-list is exactly `["Email", "Phone"]`** — `WebPush` and `Messenger` rows DO exist on subscribers but cannot be created or modified through this API; any other value is rejected with 422 on `/data/attributes/channel`. See [[api-subscribers-channels-rules]].
- **Sort allow-list is narrow** — only `subscriber_id`, `channel`, `channel_identifier` are sortable. `sort=created_at` and `sort=id` return 422.
- **Filtering is equality-only** — no comparison-operator syntax.

## Equivalent UI

- [[marketing-subscribers]] — subscriber detail → Channels tab; the read view of a subscriber's channel rows.
- [[subscriber|Subscriber entity]] — full per-channel attribute reference.

## Related

- [[api-subscribers-channels]] — hub.
- [[json-api-v2]] — API hub (filtering / pagination conventions).
- [[api-subscribers]] — parent Subscriber resource.
- [[settings-api-keys]] — authentication setup.
- [[subscriber]] — Subscriber entity.

## Open questions

- Confirm whether any default `page[size]` cap applies to this collection beyond the platform-wide JSON-API default (see [[json-api-v2]]).
