---
type: api-resource
resource_path: /api/v2/subscribers
http_methods: [GET]
related_entity: subscriber
related_features: [marketing-subscribers, marketing-segments]
aliases: ["Subscribers API filtering", "Subscribers API sorting", "Subscribers API includes", "filter[segment] subscribers", "Subscribers GET examples"]
tags: [api, json-api-v2, marketing]
plan_gates: ["subscribers"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[api-subscribers]]. See the hub for the other aspects (attributes / CRUD, write side-effects).

# Subscribers API — filtering, sorting & includes

## Purpose

The read-side query surface of the [[subscriber|Subscribers]] JSON-API v2 resource: how to filter (including the custom `filter[segment]` join), which fields are sortable, which relationships are includable, and the concrete GET request + response shapes. For the writable attribute set and POST/PATCH/DELETE examples see [[api-subscribers-list-crud]]; for write side-effects see [[api-subscribers-list-effects]].

## Endpoint

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/v2/subscribers` | List subscribers. Supports filter / sort / include / page. |
| GET | `/api/v2/subscribers/{id}` | Fetch one subscriber. |
| GET | `/api/v2/subscribers/{id}/<rel>` | Fetch related `channels` or `tags` as full resources. |

All requests use `Accept: application/vnd.api+json` and authenticate via `X-API-KEY` (see [[settings-api-keys]]).

## Attributes

The full readable attribute set (identity fields + read-only campaign metrics) is documented on [[api-subscribers-list-crud]]. All attributes except `password` / `remember_token` (hidden) appear in GET responses. Consent + deliverability flags are NOT on the subscriber row — they are read via the `channels` include ([[api-subscribers-channels]]).

## Relationships

`channels` and `tags` are both includable (`include=channels`, `include=tags`). See [[api-subscribers-list-crud]] for cardinality and write rules; this page covers only how to *read* them via includes.

## Filtering & sorting

### Allowed filtering parameters

- `filter[segment]` — **custom join filter.** Takes a segment ID; rewrites the query to `whereHas('segments', WHERE subscribers_segments.id = ?)`. Returns subscribers currently attached to that [[segment\|Segment]] via the `subscriber_to_segments` pivot. Single value only — multi-segment filtering requires multiple calls. A non-existent segment ID returns an **empty collection** (no error — the inner join just yields nothing).
- Every column on the `subscribers` row is auto-allowed as a filter key (framework default). Common ones: `filter[id]`, `filter[customer_id]`, `filter[first_name]`, `filter[last_name]`, `filter[country]`, `filter[subscribed_from]`, `filter[deleted_customer]`, `filter[form_id]`, `filter[last_order_id]`, `filter[created_at]`, `filter[updated_at]`.

Filtering is equality-only — there is no comparison-operator syntax (see [[json-api-v2]] hub).

### Allowed sort parameters

`id`, `first_name`, `last_name`, `country`. Prefix with `-` for descending. Multi-sort allowed.

Sorting on any other field (e.g., `created_at`) returns **422**.

### Allowed include paths

`include=channels`, `include=tags`. Both top-level relationships are auto-merged into the include allow-list from the schema. No nested includes (e.g., `tags.tag`) are declared — nested expansions return **422**.

## Side effects

GET requests are read-only and produce no side effects. All write-path consequences (webhooks, plan cap, cascade) are documented on [[api-subscribers-list-effects]].

## Equivalent UI

- [[marketing-subscribers]] — the admin subscriber list; the *"Subscribed from"* filter, search, and column sorts mirror the query parameters here.
- [[marketing-segments]] — segment definitions that back the `filter[segment]` join.

## Example requests & responses

### GET collection filtered by segment

```bash
curl -sS -X GET \
  "https://<store-host>/api/v2/subscribers?filter[segment]=42&include=channels,tags&page[size]=10" \
  -H "Accept: application/vnd.api+json" \
  -H "X-API-KEY: <YOUR_API_KEY>"
```

`filter[segment]` is the custom join filter — it rewrites the query to `whereHas('segments', WHERE subscribers_segments.id = ?)`. A non-existent segment id returns an empty collection (not 404).

### GET single

```bash
curl -sS -X GET \
  "https://<store-host>/api/v2/subscribers/12345?include=channels,tags" \
  -H "Accept: application/vnd.api+json" \
  -H "X-API-KEY: <YOUR_API_KEY>"
```

### GET collection (200) — paginated

```json
{
  "data": [
    {
      "type": "subscribers",
      "id": "12345",
      "attributes": {
        "country": "BG",
        "first_name": "Ivan",
        "last_name": "Petrov",
        "subscribed_from": "API",
        "customer_id": null,
        "deleted_customer": 0,
        "total_sent": 0,
        "open_rate": 0,
        "click_rate": 0,
        "last_active_at": null,
        "created_at": "2026-06-05T09:12:44+00:00",
        "updated_at": "2026-06-05T09:12:44+00:00"
      },
      "relationships": {
        "channels": { "links": { "related": "https://<store-host>/api/v2/subscribers/12345/channels" } },
        "tags": { "links": { "related": "https://<store-host>/api/v2/subscribers/12345/tags" } }
      }
    }
  ],
  "meta": {
    "page": {
      "current-page": 1,
      "per-page": 10,
      "from": 1,
      "to": 10,
      "total": 348,
      "last-page": 35
    }
  }
}
```

### GET single (200) — channels sideloaded

```json
{
  "data": {
    "type": "subscribers",
    "id": "12345",
    "attributes": {
      "country": "BG",
      "first_name": "Ivan",
      "last_name": "Petrov",
      "subscribed_from": "API"
    },
    "relationships": {
      "channels": {
        "data": [
          { "type": "subscribers-channels", "id": "98765" },
          { "type": "subscribers-channels", "id": "98766" }
        ]
      },
      "tags": { "data": [] }
    }
  },
  "included": [
    {
      "type": "subscribers-channels",
      "id": "98765",
      "attributes": {
        "channel": "Email",
        "channel_identifier": "ivan.petrov@example.com",
        "marketing": 1,
        "verified": 0,
        "bounced": 0
      }
    },
    {
      "type": "subscribers-channels",
      "id": "98766",
      "attributes": {
        "channel": "Phone",
        "channel_identifier": "+359871234567",
        "marketing": 1,
        "verified": 0,
        "bounced": 0
      }
    }
  ]
}
```

### Common 422 query errors

- **Invalid sort key** — `sort=email` → 422 (only `id`, `first_name`, `last_name`, `country` are allowed).
- **Invalid include path** — `include=tags.tag` → 422 (nested includes not declared).
- **Invalid `filter[segment]`** — a non-existent segment ID returns an **empty collection**, not an error.

## Related

- [[api-subscribers]] — hub.
- [[api-subscribers-list-crud]] — attribute reference + write examples.
- [[api-subscribers-list-effects]] — write side-effects, plan cap, cascade, testing checklist.
- [[json-api-v2]] — API hub: equality-only filtering, pagination, status codes.
- [[api-segments]] — read-only segments resource that backs `filter[segment]`.
- [[marketing-subscribers]] — equivalent admin list.
- [[settings-api-keys]] — authentication setup.

## Open questions

- None.
