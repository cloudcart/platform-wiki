---
type: api-resource
resource_path: /api/v2/subscribers-tags
http_methods: [GET, POST, PATCH, DELETE]
related_entity: subscriber
related_features: [marketing-subscribers, marketing-segments, marketing-segments-editor]
aliases: ["Subscriber Tags API", "JSON-API v2 subscribers-tags", "API тагове на абонати", "/subscribers-tags"]
tags: [api, json-api-v2, marketing]
plan_gates: []
created: 2026-05-26
updated: 2026-06-05
source_count: 2
---
# Subscriber Tags (JSON-API v2)

## Purpose

Programmatic CRUD on the **subscriber-tag pivot rows** — the many-to-many links between [[subscriber|Subscribers]] and the merchant's subscriber-tag vocabulary. Integrations use it to attach a tag to a subscriber (e.g. a CRM marking contacts as `vip` or `newsletter-signup`), detach one, or read current tag membership for segmentation and analytics.

Subscriber tags are a **separate pivot table from [[api-customer-tags|customer tags]]** (subscribers vs customers) but **reuse the same underlying tag-name dictionary** — both reference the shared customer-tags table. This resource manages only the pivot link; see Side effects for the cascade implications.

A subscriber-tag membership drives segmentation: rules like *"Subscriber has tag `vip`"* read this pivot. Changing a subscriber's tags re-triggers Automated segment evaluation within seconds.

## Endpoint

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/v2/subscribers-tags` | List subscriber-tag pivot rows across all subscribers. |
| GET | `/api/v2/subscribers-tags/{id}` | Fetch one pivot row. |
| POST | `/api/v2/subscribers-tags` | Create a pivot row (attach a tag to a subscriber). |
| PATCH | `/api/v2/subscribers-tags/{id}` | Update a pivot row. Rarely useful — the typical workflow is delete + recreate. |
| DELETE | `/api/v2/subscribers-tags/{id}` | Delete a pivot row (detach a tag from a subscriber). |
| GET | `/api/v2/subscribers-tags/{id}/subscriber` | Fetch the parent subscriber. |
| GET | `/api/v2/subscribers-tags/{id}/tag` | Fetch the linked tag. |

No custom routes. No app-install gate.

Base URL details (host, auth, rate limit): see [[json-api-v2]] hub.

## Attributes

The pivot row is intentionally minimal — most meaningful data lives on the linked subscriber and tag records. The validator declares **no `readOnlyAttributes`, no required `rules`, and no `allowedSortParameters`** — a thin pass-through over the pivot table. Consequences: no `required` / `exists` enforcement (bad FKs land at the DB layer), and every `sort=` is rejected (see Filtering & sorting).

| Attribute | Type | Writable on POST? | Writable on PATCH? | Required? | Notes / validation |
|---|---|---|---|---|---|
| `subscriber_id` | integer | yes (fillable) | yes (fillable) | not declared | FK to the parent [[subscriber\|Subscriber]] (`subscribers.id`). |
| `tag_id` | integer | yes (fillable) | yes (fillable) | not declared | FK into the shared customer-tags dictionary (`customer_tags.id`). |
| `created_at` / `updated_at` | datetime | — | — | — | Standard timestamps. |

**Practical convention**: set the link via the JSON-API **relationships** payload rather than via attributes — see Relationships below.

## Relationships

| Name | Cardinality | Target type | Writable? | Notes |
|---|---|---|---|---|
| `subscriber` | hasOne | `subscribers` | writable (attribute OR relationship payload) | The parent [[subscriber\|Subscriber]] — see [[api-subscribers]]. |
| `tag` | belongsTo | `customer-tags` | writable (attribute OR relationship payload) | The tag record in the shared `customer_tags` dictionary — see [[api-customer-tags]]. |

The route registration declares these as `hasMany`, but the functional model is one Subscriber ↔ one Tag per pivot row — a quirk of the registration.

## Filtering & sorting

### Allowed filtering parameters

No bespoke filter scopes are declared. Every column on the `tags__subscribers__items` pivot row is auto-allowed: `filter[id]`, `filter[subscriber_id]`, `filter[tag_id]`, `filter[created_at]`, `filter[updated_at]`.

Filtering is equality-only — there is no comparison-operator syntax (see [[json-api-v2]] hub).

### Allowed sort parameters

**None declared** — `$allowedSortParameters` is empty, so any `sort=` fails (422). Only the default ordering (`id` ASC) applies; to order by something else, fetch the related Subscriber or Tag instead.

### Allowed include paths

`include=subscriber`, `include=tag` — both registered relationships are auto-allowed. No nested includes (e.g. `subscriber.channels`) are declared.

## Side effects on write

- **Cascade on subscriber delete** — deleting a subscriber via [[api-subscribers]] DELETE (or admin panel) removes ALL of that subscriber's pivot rows.
- **Cascade on tag delete** — deleting the tag record via [[api-customer-tags]] DELETE removes every pivot row referencing it (across Subscribers AND Customers, since the dictionary is shared); the subscribers survive untagged. There is no API-level "delete from subscribers only".
- **Shared tag dictionary** — create a NEW tag name through [[api-customer-tags]] POST, then link it here; this resource only manages the pivot.
- **Automated-segment re-evaluation** — every create / delete fires an incremental segment-evaluation job for the affected subscriber. `subscriber.has_tag` segments update within seconds; full-population rebuilds run on a 300-second (5-minute) cadence (see [[marketing-segments]]).
- **`subscriber.updated` webhook (indirect)** — pivot writes touch the parent subscriber's `updated_at`, firing `subscriber.updated` to [[settings-hooks]] receivers. There is **no dedicated `subscriber_tag.created` / `.deleted` event** — subscribe to `subscriber.updated` for tag-change notifications.
- **No dedicated audit-log capture** — no actor-identity audit log; only the pivot row's `created_at` / `updated_at` timestamps.

## Plan-feature gating

No plan-feature gating at the resource level. The Segments product that consumes tag membership is gated separately by the `segments` feature (see [[api-segments]]). HTTP 402 fires only when the plan is expired / past-due / trial-ended; this resource never emits 403.

## Common error cases

This resource has the thinnest validator in the API surface — most errors come from the framework, not bespoke rules:

- **Any `sort=` parameter** → 422 (`allowedSortParameters` is empty). See the 422 example below.
- **Invalid include path** — e.g. `include=subscriber.channels` → 422 (nested includes not declared).
- **Out-of-range `page[size]`** — outside `1..100` → 422 with `source.pointer = "/page/size"`.
- **404 Not Found** — `GET /{id}` for a pivot row that does not exist (e.g. cascaded away by a Subscriber or Tag delete).
- **Non-existent FK** — POSTing an unknown `subscriber_id` / `tag_id` may surface as a 500 (DB foreign-key error), since no `exists` rule is declared.

## Example requests

All requests use `Accept: application/vnd.api+json`; body-carrying requests add `Content-Type: application/vnd.api+json`. Authenticate via `X-API-KEY` (see [[settings-api-keys]]). Create the tag in [[api-customer-tags]] first, then link its `tag_id` here.

### GET collection

```bash
curl -sS -X GET \
  "https://<store-host>/api/v2/subscribers-tags?filter[subscriber_id]=12345&include=subscriber,tag&page[size]=10" \
  -H "Accept: application/vnd.api+json" \
  -H "X-API-KEY: <YOUR_API_KEY>"
```

### POST — link a tag to a subscriber (attribute form)

```bash
curl -sS -X POST \
  "https://<store-host>/api/v2/subscribers-tags" \
  -H "Accept: application/vnd.api+json" \
  -H "Content-Type: application/vnd.api+json" \
  -H "X-API-KEY: <YOUR_API_KEY>" \
  -d '{
    "data": {
      "type": "subscribers-tags",
      "attributes": {
        "subscriber_id": 12345,
        "tag_id": 77
      }
    }
  }'
```

### POST — link a tag to a subscriber (relationship form)

The relationship form is the canonical JSON-API shape; either form works since both FK columns are fillable on the model.

```bash
curl -sS -X POST \
  "https://<store-host>/api/v2/subscribers-tags" \
  -H "Accept: application/vnd.api+json" \
  -H "Content-Type: application/vnd.api+json" \
  -H "X-API-KEY: <YOUR_API_KEY>" \
  -d '{
    "data": {
      "type": "subscribers-tags",
      "relationships": {
        "subscriber": { "data": { "type": "subscribers", "id": "12345" } },
        "tag": { "data": { "type": "customer-tags", "id": "77" } }
      }
    }
  }'
```

### DELETE (unlink)

```bash
curl -sS -i -X DELETE \
  "https://<store-host>/api/v2/subscribers-tags/55501" \
  -H "Accept: application/vnd.api+json" \
  -H "X-API-KEY: <YOUR_API_KEY>"
```

Returns **204 No Content** — only the pivot link is removed; the Subscriber and the Tag dictionary entry both survive.

## Example responses

### GET collection (200) — paginated

```json
{
  "data": [
    {
      "type": "subscribers-tags",
      "id": "55501",
      "attributes": {
        "subscriber_id": 12345,
        "tag_id": 77,
        "created_at": "2026-06-05T09:14:02+00:00",
        "updated_at": "2026-06-05T09:14:02+00:00"
      },
      "relationships": {
        "subscriber": { "links": { "related": "https://<store-host>/api/v2/subscribers-tags/55501/subscriber" } },
        "tag": { "links": { "related": "https://<store-host>/api/v2/subscribers-tags/55501/tag" } }
      }
    }
  ],
  "meta": {
    "page": {
      "current-page": 1,
      "per-page": 10,
      "from": 1,
      "to": 1,
      "total": 1,
      "last-page": 1
    }
  }
}
```

### GET single (200)

```json
{
  "data": {
    "type": "subscribers-tags",
    "id": "55501",
    "attributes": {
      "subscriber_id": 12345,
      "tag_id": 77
    }
  }
}
```

### POST 201 Created

```
HTTP/1.1 201 Created
Location: https://<store-host>/api/v2/subscribers-tags/55501
```

```json
{
  "data": {
    "type": "subscribers-tags",
    "id": "55501",
    "attributes": {
      "subscriber_id": 12345,
      "tag_id": 77,
      "created_at": "2026-06-05T09:14:02+00:00",
      "updated_at": "2026-06-05T09:14:02+00:00"
    }
  }
}
```

### 422 — sort rejected (no `allowedSortParameters`)

```json
{
  "errors": [
    {
      "status": "422",
      "title": "Unprocessable Entity",
      "detail": "Sort parameter is not allowed.",
      "source": { "parameter": "sort" }
    }
  ]
}
```

## Equivalent UI

- [[marketing-subscribers]] — subscriber detail → Tags multi-select; manual tag attach / detach. Bulk-tag actions on the subscriber list.
- [[marketing-segments-editor]] — segment-rule builder; `subscriber.has_tag` is one of the available condition fields.
- [[marketing-subscribers-custom-fields]] — distinct concept (custom fields are key-value data on the subscriber, not tags).

## Related

- [[json-api-v2]] — API hub.
- [[api-subscribers]] — parent Subscriber resource.
- [[api-subscribers-channels]] — per-channel deliverability rows (sibling pivot).
- [[api-customer-tags]] — the shared tag-dictionary resource (CRUD on the tag records themselves — the names; subscriber tags reuse this dictionary).
- [[api-segments]] — read-only segments resource (which consumes tag membership through the `subscriber.has_tag` segment rule).
- [[settings-hooks]] — webhook subscriptions (note: no dedicated subscriber-tag events; rely on `subscriber.updated`).

## Open questions

- Confirm whether the canonical POST workflow is attribute-based or relationship-based. Both should work given the fillable columns, but the absence of declared rules suggests the relationship form is intended.
- Verify whether duplicate pivot inserts (same `subscriber_id` + `tag_id`) are blocked by a unique composite index or silently duplicated. Internal tag-add helpers use a get-or-create path, suggesting a unique index is expected; the API path issues a plain insert.
- Verify the error surface for a non-existent `subscriber_id` / `tag_id` — whether the DB foreign-key constraint produces a 500 or the framework maps it to a 422.
