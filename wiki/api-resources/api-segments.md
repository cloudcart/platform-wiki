---
type: api-resource
resource_path: /api/v2/segments
http_methods: [GET]
related_entity: segment
related_features: [marketing-segments, marketing-segments-editor, marketing-segments-subscribers, marketing-segments-log, marketing-campaigns]
aliases: ["Segments API", "JSON-API v2 segments", "API сегменти", "/segments"]
tags: [api, json-api-v2, marketing]
plan_gates: ["segments"]
created: 2026-05-26
updated: 2026-06-05
source_count: 3
---
# Segments (JSON-API v2)

## Purpose

**Read-only** access to the merchant's [[segment|Segments]] — the saved audience queries that drive [[marketing-campaigns]] targeting. Integrations use this endpoint to enumerate segments (for their own picker UI), read a segment's current membership (via the `subscribers` relationship), and monitor segment counts for reporting.

Segment **creation and editing happens exclusively in the admin panel** via the visual rule builder on [[marketing-segments-editor]] — the API exposes no write path for the rule tree. A Segment is the **primary audience-selection object** for marketing: every [[campaign|Campaign]] targets exactly one Segment. See [[segment|Segment entity]] for the full model.

## Endpoint

**This resource is read-only** — only `GET` is exposed. POST / PATCH / DELETE are blocked at the routing layer and return **405 Method Not Allowed**.

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/v2/segments` | List segments. Supports `sort`, `include`, `page`. |
| GET | `/api/v2/segments/{id}` | Fetch one segment. |
| GET | `/api/v2/segments/{id}/subscribers` | Fetch the current subscriber membership (paginated). |
| GET | `/api/v2/segments/{id}/relationships/subscribers` | Linkage-only form of the membership. |
| (POST / PATCH / DELETE) | — | **Not registered.** Use [[marketing-segments-editor]]. |

No custom routes. No app-install gate at the route layer — the `segments` plan-feature governs whether the merchant has the Segments product at all (see [[marketing-segments]] business rules). Base URL, auth, and rate limit: see [[json-api-v2]] hub.

## Attributes

All attributes are read-only — there are no writable fields on this resource.

| Attribute | Type | Writable on POST? | Writable on PATCH? | Required? | Notes / validation |
|---|---|---|---|---|---|
| `name` | string | — | — | — | Merchant-given label (or auto-summary from the rule tree when not overridden). |
| `title` | string | — | — | — | Optional rename (admin-panel-only). Display rule: `title` if set, else `name`. |
| `channel` | string | — | — | — | Always `cloudcart` for modern segments. Force-set on create. |
| `type` | enum `regular` / `automated` | — | — | — | `regular` = One-time (frozen on Generate); `automated` = continuously re-evaluated. |
| `active` | enum `yes` / `no` | — | — | — | When `no`, the segment is excluded from rebuild jobs and campaign target pickers; existing campaigns see the frozen membership. |
| `last_execute` | datetime | — | — | — | When the last rebuild attempt finished (success or failure). |
| `subscribers_count` | integer | — | — | — | Cached count of current membership; reflects the post-plan-cap set (see Side effects). |
| `campaigns_count` | integer | — | — | — | Cached count of campaigns referencing this segment. When `> 0`, deletion is blocked. |
| `created_at` / `updated_at` | datetime | — | — | — | Standard timestamps. |

**Hidden by the schema (NOT returned even though they exist on the row):**

- `conditions` — the structured rule tree (admin-panel-only; deliberately hidden).
- `conditions_formatted` — the human-readable auto-summary.
- `inactive_errors` — the reason a segment self-disabled; the API surfaces only the resulting `active = no`.
- `processing` — internal flag set during a rebuild.
- `deleted_at` — soft-delete timestamp.

## Relationships

| Name | Cardinality | Target type | Writable? | Notes |
|---|---|---|---|---|
| `subscribers` | hasMany | `subscribers` | read-only | Current segment membership. Includes both rule-matched and manual hand-adds done in [[marketing-segments-subscribers]]. See [[api-subscribers]]. |

## Filtering & sorting

### Allowed filtering parameters

No bespoke filter scopes are declared; every column is auto-allowed (framework behaviour) — usable keys include `filter[id]`, `filter[name]`, `filter[type]`, `filter[active]`, `filter[channel]`, `filter[last_execute]`, `filter[created_at]`, `filter[updated_at]`. Filtering is equality-only — no `>=` / `<` / `like` operator syntax (see [[json-api-v2]] hub).

### Allowed sort parameters

`id`, `name`, `type`, `active`, `created_at`, `updated_at`. Prefix with `-` for descending. Multi-sort allowed: `sort=-active,name`.

### Allowed include paths

`include=subscribers` — sideloads the current membership. No nested include paths are declared; nested expansions (e.g., `subscribers.channels`) are NOT allowed and return 422.

## Side effects on write

This is a read-only resource — `GET` requests do not write. No webhooks fire, no jobs are queued, no audit-log entries are written.

Operational context that affects what `GET` returns:

- **Membership lag on Automated segments** — the full-population sweep runs every **300 seconds (5 minutes)**. Individual subscriber events re-evaluate active Automated segments for that one subscriber within seconds (near-live), but bulk-population changes can take up to 5 minutes to settle. One-time (`regular`) segments do NOT participate in the sweep — they're frozen until the merchant clicks Generate in [[marketing-segments]].
- **Auto-disable mid-rebuild** — if a segment references an uninstalled-app's condition (or a deleted custom field, etc.), the rebuild job auto-disables it (`active = no`). The API surfaces only `active = no`, not the reason (`inactive_errors` is hidden); the merchant must open [[marketing-segments]] to see why.
- **Import-induced delay** — while a CSV subscriber import is in flight, the evaluator delays itself by 300 seconds and restarts, so `subscribers_count` appears "stale" until the import finishes (intentional, to avoid churning segments mid-bulk-insert).
- **Plan-cap interaction (silent)** — when the store hits the `subscribers` plan-feature cap, evaluation silently filters subscribers below `subscribers.max_id` (chronological; see [[marketing-subscribers]]). The API returns the post-cap membership only.
- **Deletion blocked by `campaigns_count`** — admin-panel deletion is blocked when `campaigns_count > 0`. Integrations should respect this signal.

## Plan-feature gating

- **`segments` plan-feature** — gates whether the merchant has the Segments product. Without it, the table is empty and `GET /api/v2/segments` returns an empty list (the resource itself is not blocked).
- **`subscribers` plan-feature cap** — caps the subscriber-id horizon visible to evaluation (`subscribers.max_id`). See [[marketing-subscribers]] business rules.
- **HTTP 402 (Payment Required)** — emitted only when the merchant's plan has expired / past-due / trial-ended. Subscriber-cap overflows do NOT return 402 here; the silent cap applies instead. **HTTP 403** is not emitted by this resource.

## Error examples (common 422 cases)

No write surface and no bespoke validator rules — the only errors a caller hits are framework-level:

- **Invalid sort key** — `sort=foo` (not in the allow-list) → 422 with `errors[*].source.parameter = "sort"`.
- **Invalid include path** — `include=subscribers.channels` (not declared) → 422 with the unsupported-include message.
- **Out-of-range `page[size]`** — values outside `1..100` → 422 with `source.pointer = "/page/size"`.
- **404 Not Found** — `GET /api/v2/segments/{id}` where the ID does not exist (or was soft-deleted).

## Example requests

All requests require `Accept: application/vnd.api+json` and a valid API key in `X-API-KEY` (see [[settings-api-keys]]). POST / PATCH / DELETE on this resource always return **405 Method Not Allowed** — the write routes are not registered.

```bash
# GET collection (with sort + pagination)
curl -sS -X GET \
  "https://<store-host>/api/v2/segments?sort=-active,name&page[size]=10" \
  -H "Accept: application/vnd.api+json" -H "X-API-KEY: <YOUR_API_KEY>"

# GET single (with membership sideloaded)
curl -sS -X GET \
  "https://<store-host>/api/v2/segments/42?include=subscribers" \
  -H "Accept: application/vnd.api+json" -H "X-API-KEY: <YOUR_API_KEY>"
```

## Example responses

### GET collection (200) — paginated

```json
{
  "data": [
    {
      "type": "segments",
      "id": "42",
      "attributes": {
        "name": "VIP buyers (last 90 days)",
        "title": null,
        "channel": "cloudcart",
        "type": "automated",
        "active": "yes",
        "last_execute": "2026-06-05T08:15:00+00:00",
        "subscribers_count": 1284,
        "campaigns_count": 3,
        "created_at": "2026-04-12T11:02:18+00:00",
        "updated_at": "2026-06-05T08:15:00+00:00"
      },
      "relationships": {
        "subscribers": {
          "links": {
            "self": "https://<store-host>/api/v2/segments/42/relationships/subscribers",
            "related": "https://<store-host>/api/v2/segments/42/subscribers"
          }
        }
      }
    }
  ],
  "meta": {
    "page": {
      "current-page": 1,
      "per-page": 10,
      "from": 1,
      "to": 10,
      "total": 27,
      "last-page": 3
    }
  },
  "links": {
    "first": "https://<store-host>/api/v2/segments?page[number]=1&page[size]=10",
    "next": "https://<store-host>/api/v2/segments?page[number]=2&page[size]=10",
    "last": "https://<store-host>/api/v2/segments?page[number]=3&page[size]=10"
  }
}
```

### GET single (200)

```json
{
  "data": {
    "type": "segments",
    "id": "42",
    "attributes": {
      "name": "VIP buyers (last 90 days)",
      "type": "automated",
      "active": "yes",
      "subscribers_count": 1284,
      "campaigns_count": 3
    }
  }
}
```

### POST/PATCH/DELETE attempt (405)

```
HTTP/1.1 405 Method Not Allowed
Allow: GET, HEAD
Content-Type: application/vnd.api+json

{
  "errors": [
    {
      "status": "405",
      "title": "Method Not Allowed",
      "detail": "The POST method is not supported for this route. Supported methods: GET, HEAD."
    }
  ]
}
```

## Equivalent UI

- [[marketing-segments]] — segment list (mirrors `GET /api/v2/segments`).
- [[marketing-segments-editor]] — visual rule builder (admin-panel-only; no API equivalent).
- [[marketing-segments-subscribers]] — membership view (mirrors `GET.../subscribers`).
- [[marketing-segments-log]] — rebuild audit log (admin-panel-only).
- [[segment|Segment entity]] — full attribute reference.

## Related

- [[json-api-v2]] — API hub: auth, rate limit, side-effects principle.
- [[api-subscribers]] — Subscriber resource; use `filter[segment]` to pull subscribers by segment id.
- [[api-customers]] — Customer resource (distinct from Subscriber — segments target subscribers).
- [[settings-hooks]] — webhook subscriptions (no segment-level events fire).
- [[settings-api-keys]] — authentication setup.

## Open questions

- Confirm whether `subscribers_count` here reflects the post-plan-cap count (below `subscribers.max_id`) or the raw rule-matched count. The admin UI shows the post-cap "active" count; the API contract on this number is not verified end-to-end.
- Verify whether the `subscribers` relationship endpoint paginates membership for very large segments, and whether its `page[size]` is capped at the same `1..100` as top-level pagination.
