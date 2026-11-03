---
type: api-resource
resource_path: /api/v2/authors
http_methods: [GET]
related_entity: blog-article
related_features: [marketing-blog-articles, settings-staff]
aliases: ["Authors API", "Blog Authors API", "JSON-API v2 authors", "API автори", "/authors"]
tags: [api, json-api-v2, content]
plan_gates: []
created: 2026-05-26
updated: 2026-06-05
source_count: 4
---
# Authors (JSON-API v2)

## Purpose

**Read-only** mirror of the merchant's admin / staff list, exposed through a content-specific lens so external authoring tools can populate an **Author dropdown** when creating or editing a [[blog-article|Blog Article]] via [[api-posts]]. Integrators use this endpoint to **enumerate available authors** for an external CMS / authoring tool's author picker, and to **read author identity** for display (byline, attribution).

Each row returned by this endpoint corresponds to one admin/staff record on the store — the same `Admin` table that powers [[settings-staff]]. Creating, editing, or deleting an Admin user is **not** done through this resource; staff management happens in [[settings-staff]] (admin-panel-only — there is no JSON-API v2 resource for staff CRUD).

## Endpoint

- **URL base:** `<store-host>/api/v2/authors`
- **HTTP methods:** GET only (collection + single)
- **Read-only?** **YES** — the route is registered as `readOnly` in `api2/the platform code`. **POST / PATCH / DELETE return 405 Method Not Allowed** at the routing layer.
- **Custom routes:** none
- **App requirements:** none

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/v2/authors` | List authors (admin/staff records). Supports `page[number]` + `page[size]`. |
| GET | `/api/v2/authors/{id}` | Fetch one author by admin ID. |
| ❌ POST | `/api/v2/authors` | **405 Method Not Allowed.** Manage staff via [[settings-staff]]. |
| ❌ PATCH | `/api/v2/authors/{id}` | **405 Method Not Allowed.** Manage staff via [[settings-staff]]. |
| ❌ DELETE | `/api/v2/authors/{id}` | **405 Method Not Allowed.** Manage staff via [[settings-staff]]. |

Authentication, host resolution, common headers, status codes, and rate limits: see [[json-api-v2]].

## Attributes

All attributes are read-only.

| Attribute | Type | Writable on POST? | Writable on PATCH? | Required? | Notes |
|---|---|---|---|---|---|
| `id` | integer | n/a | n/a | n/a | Admin record primary key. JSON:API resource `id`. |
| `admin_type` | string | no | no | n/a | The staff role / type classifier. **Appended accessor** in the schema; the adapter aliases the underlying `type` column to `admin_type` to avoid clashing with the JSON:API top-level `type` member. |
| Other `Admin` columns (`first_name`, `last_name`, `email`, `created_at`, `updated_at`, …) | mixed | no | no | n/a | Returned per the base `Admin` model's default serialisation. The schema's `$appends` list contains only `admin_type` and `$hidden` excludes the raw `type` column — the visible payload depends on the model's `$hidden` array. |

Hidden in the schema: the raw `type` column (the API exposes the aliased `admin_type` instead).

## Relationships

The schema declares **no static relationships** (`$relationships = []`). The route is registered as a bare `readOnly` resource — no `hasOne` / `hasMany` is exposed.

Posts link **back** to authors via the `author` belongsTo relationship on [[api-posts]] — that is the path integrators use to discover which author wrote a given article.

## Filtering & sorting

**Allowed filtering parameters:**

- **None declared explicitly** — `$allowedFilteringParameters = []`.
- **However**, the framework auto-merges every column on the `admin` table into the allowed-filters list (see [[json-api-v2]] *"Filtering"* section). Practical examples: `filter[id]`, `filter[email]`, `filter[type]`. Filtering is value-equality only — no comparison operators.

**Allowed sort parameters:**

- **None declared** — `$allowedSortParameters = []`. The endpoint returns rows in DB-default order (typically by `id` ASC). Attempting `?sort=name` returns 422.

**Allowed include paths:**

- (none — `$allowedIncludePaths = []` explicitly AND `$relationships = []`).

## Side effects on write

GET-only. No writes triggered by this endpoint.

Operational context for read callers:

- **Author = Admin** — every author returned by this endpoint is a row in the `admin` table. There is no distinct "author profile" — the merchant's staff list IS the author list.
- **No deleted-staff cascade** — if a staff member who authored articles is deleted from [[settings-staff]], the article's `author_id` may end up dangling. The article does NOT cascade-delete with the author. Integrations reading historic articles should expect occasional `null` / missing author references.
- **No author-byline override** — the [[blog-article|Blog Article entity]] has a legacy free-text `author` byline column separate from `author_id`, but the modern flow uses the FK to an Admin record only. This endpoint surfaces the FK target, not the free-text byline.

## Plan-feature gating

- **No plan-feature gating on this endpoint** — every CloudCart store has at least one admin user. The merchant's `staff_seats` plan-feature limit governs **how many staff can be added** (enforced in [[settings-staff]]), not whether this endpoint is reachable.

## Error examples (common cases)

| Condition | Status | Notes |
|---|---|---|
| POST / PATCH / DELETE on this resource | **405 Method Not Allowed** | Blocked at the routing layer — the route is `readOnly`. |
| `?sort=name` (sort key not in allow-list) | **422 Unprocessable Entity** | `$allowedSortParameters` is empty. |
| `GET /api/v2/authors/{id}` with non-existent ID | **404 Not Found** | Standard JSON:API behaviour. |
| Plan-expired | **402 Payment Required** | Standard api2-layer plan check (see [[json-api-v2]]). |

## Example requests

All examples use `<store-host>` and `<YOUR_API_KEY>`. **Read-only resource** — only GET is supported.

### GET collection

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/authors?page[size]=20"
```

### GET single

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/authors/12"
```

### POST / PATCH / DELETE — 405 Method Not Allowed

```bash
curl -s -X POST \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/authors" \
     -d '{"data":{"type":"authors","attributes":{"first_name":"Nope"}}}'
```

Returns:

```
HTTP 405 Method Not Allowed
{"errors":[{"status":"405","title":"Method Not Allowed"}]}
```

Same response for PATCH and DELETE. Manage staff via [[settings-staff]] (admin-panel only).

## Example responses

### GET collection success

```json
{
  "data": [
    {
      "type": "authors",
      "id": "12",
      "attributes": {
        "first_name": "Ivan",
        "last_name": "Petrov",
        "email": "ivan@example.com",
        "admin_type": "owner",
        "created_at": "2024-08-01T09:00:00+00:00",
        "updated_at": "2026-05-30T11:02:14+00:00"
      }
    }
  ],
  "meta": {
    "page": { "current-page": 1, "per-page": 20, "from": 1, "to": 1, "total": 1, "last-page": 1 }
  }
}
```

### GET single success

```json
{
  "data": {
    "type": "authors",
    "id": "12",
    "attributes": {
      "first_name": "Ivan",
      "last_name": "Petrov",
      "email": "ivan@example.com",
      "admin_type": "owner"
    }
  }
}
```

### 405 — write attempt

```
HTTP 405 Method Not Allowed
{"errors":[{"status":"405","title":"Method Not Allowed"}]}
```

## Testing checklist

1. `GET /authors` — confirm read.
2. `GET /authors/{id}` — verify the shape (includes the aliased `admin_type` accessor; the raw `type` column is hidden).
3. `POST /authors` — verify 405.
4. `PATCH /authors/{id}` — verify 405.
5. `DELETE /authors/{id}` — verify 405.

## Equivalent UI

- [[marketing-blog-articles]] — Article editor: the Author dropdown picks from this resource's listing.
- [[settings-staff]] — staff / admin management (where authors come from; admin-panel-only — no JSON-API resource for staff CRUD).
- [[blog-article|Blog Article entity]] — full attribute reference.

## Related

- [[json-api-v2]] — API hub.
- [[api-posts]] — Blog Article resource; the `author` belongsTo points at this resource.
- [[api-blogs]] — Blog Category resource.
- [[settings-staff]] — staff management.
- [[settings-api-keys]] — authentication setup.

## Open questions

- Document which `Admin` columns are actually exposed in the API response — the schema only `appends` `admin_type` and `hides` the raw `type` column; the rest of the payload (first_name / last_name / email / etc.) depends on the underlying `Admin` model's default visibility (`$hidden`). Verify by issuing a real GET against a test store.
- Confirm whether deactivated admin records (banned, locked, archived staff) are returned by this endpoint, or whether the `Admin` model's default scopes filter them out.
