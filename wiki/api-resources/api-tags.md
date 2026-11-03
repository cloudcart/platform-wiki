---
type: api-resource
resource_path: /api/v2/tags
http_methods: [GET, POST, PATCH, DELETE]
related_entity: blog-tag
related_features: [marketing-blog-tags, marketing-blog-articles]
aliases: ["Tags API", "Blog Tags API", "JSON-API v2 tags", "API тагове", "/tags"]
tags: [api, json-api-v2, content]
plan_gates: []
created: 2026-05-26
updated: 2026-06-05
source_count: 4
---
# Tags (JSON-API v2)

## Purpose

Programmatic CRUD on the merchant's [[blog-tag|Blog Tags]] — the free-form flat labels attached to [[blog-article|Blog Articles]] for cross-categorisation, discovery, and SEO long-tail. Integrators use this endpoint to pre-create a tag vocabulary before bulk-importing articles via [[api-posts]], rename a tag centrally, delete obsolete tags to keep the storefront's `/blog/tag/<slug>` URL space tidy, and read the tag list for external autocomplete.

A Blog Tag is **distinct from a customer tag** (different domain — customer tags live on [[api-customer-tags]]) and **distinct from a [[blog-category|Blog Category]]**: a Category is the required hierarchical parent (one per Article) while Tags are an orthogonal flat taxonomy (many per Article).

## Endpoint

**URL base:** `<store-host>/api/v2/tags` — **full CRUD** (not read-only); no custom routes, no app requirements.

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/v2/tags` | List tags. Supports filter / sort / include / page. |
| GET | `/api/v2/tags/{id}` | Fetch one tag. |
| GET | `/api/v2/tags?filter[url_handle]=<slug>` | **Search-one** — when `url_handle` is the only filter, returns a single tag rather than a paginated list. |
| POST | `/api/v2/tags` | Create a tag. Requires `tag`. |
| PATCH | `/api/v2/tags/{id}` | Update a tag (rename). |
| DELETE | `/api/v2/tags/{id}` | Delete a tag. May return 422 `"Not Deletable"` if a domain-level guard rejects the delete. |

Authentication, host resolution, common headers, status codes, and rate limits: see [[json-api-v2]].

## Attributes

| Attribute | Type | Writable on POST? | Writable on PATCH? | Required? | Notes / validation |
|---|---|---|---|---|---|
| `tag` | string | yes | yes | **yes** on POST; `sometimes` on PATCH | `min:2` characters; unique (case-insensitive). The displayed tag label. Stored lowercase — `Summer-2026` and `SUMMER-2026` collide. |
| `url_handle` | string | yes | yes | no | `alpha_dash`, `max:191`, unique. Storefront URL: `/blog/tag/<url_handle>`. Auto-derived from `tag` if omitted. |
| `id` | integer | n/a | n/a | n/a | Hidden in attributes, but the JSON:API resource `id` still carries it per JSON:API conventions. |

No computed/appended attributes on this resource.

## Relationships

This resource exposes **no relationships** and no `?include=` paths. The Article ↔ Tag link is managed from the Article side via [[api-posts]] (the `tags` hasMany relationship on a post); there is no `articles` relationship here.

## Filtering & sorting

**Allowed `filter[*]` parameters:**

- `filter[url_handle]` — `filled|alpha_dash`. When sent as the only filter, triggers single-record mode (returns one tag, not a paginated list).
- Plus every column on the tag table — auto-merged, value-equality only. Examples: `filter[id]`, `filter[tag]`.

**Allowed `sort`:** `id`, `tag` (prefix with `-` for descending). **Pagination:** standard `page[size]` / `page[number]` — see [[json-api-v2]]. No include paths.

## Side effects

- **Tag names stored lowercase** — see Attributes; `Summer-2026` and `SUMMER-2026` collapse to one stored `summer-2026`.
- **Wildcard hygiene** — `%` and `_` are silently stripped from tag names (no validation warning). A POST with `tag = "tag1%tag2"` saves as `tag = "tag1tag2"`.
- **Per-Article cap: 100 tags** — enforced only at Article-side save (see [[marketing-blog-tags]] business rules / [[api-posts]]), NOT on tag-record creation here.
- **191-char `url_handle` cap** — enforced via `max:191`. `tag` has no explicit max validator (the save layer enforces it).
- **NO 301 redirect on rename or delete** — unlike [[api-posts]] and [[api-blogs]], which auto-track slug changes via URL-handle-history, a Blog Tag rename/delete creates no 301; inbound links to `/blog/tag/<old-slug>` silently break. Pair every PATCH/DELETE with a manual rule via [[api-redirects]] if SEO continuity matters.
- **NO sitemap inclusion** — `/blog/tag/<slug>` URLs are explicitly omitted from the auto-generated sitemap. Search engines discover tag pages only via internal links.
- **Cascade on delete** — DELETE removes the tag record + its M2M pivot rows. Articles previously tagged survive untagged; the slug is freed for re-use. If the domain-level delete guard rejects, the API returns HTTP 422 `"Not Deletable"` with the underlying message.
- **Webhooks** — no `tag.*` event in the webhook catalogue (the events on [[api-webhooks]] do NOT include blog tags). Integrations cannot subscribe; they must poll.
- **Bulk-delete uses a different (admin) endpoint** — admin bulk-delete is `DELETE /admin/api/core/blog/tags` with `{ids: []}`. JSON-API v2 supports only per-resource DELETE; bulk needs sequential per-tag calls (subject to the rate limit).

## Plan-feature gating

- No dedicated plan-feature counter — tag creation is not capped by a plan-feature limit.
- `marketing.blog_tags` admin permission gates admin-panel CRUD (independent of `blog_articles`, `blog_categories`, `blog_comments`). API-key permissioning is **separate** — any active API key has full access.

## Error examples (common 422 cases)

| Condition | `source.pointer` | `detail` |
|---|---|---|
| Missing `tag` on POST | `/data/attributes/tag` | *"The tag field is required"* |
| `tag` shorter than 2 chars | `/data/attributes/tag` | *"The tag must be at least 2 characters"* |
| Duplicate `tag` (case-insensitive) | `/data/attributes/tag` | *"The tag has already been taken"* |
| Duplicate `url_handle` | `/data/attributes/url_handle` | *"The url handle has already been taken"* |
| `url_handle` with disallowed characters | `/data/attributes/url_handle` | *"The url handle may only contain letters, numbers, dashes and underscores"* |
| Delete rejected by domain guard | n/a (top-level error) | *"Not Deletable"* with the underlying message. |
| Plan-expired | n/a | HTTP 402 *"Payment Required"* — plan past-due. |

## Example requests

All examples use `<store-host>` and `<YOUR_API_KEY>`.

### GET collection

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/tags?page[size]=50&sort=tag"
```

### POST create

```bash
curl -s -X POST \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/tags" \
     -d '{
       "data": {
         "type": "tags",
         "attributes": {
           "tag": "summer-2026",
           "url_handle": "summer-2026"
         }
       }
     }'
```

### PATCH rename

```bash
curl -s -X PATCH \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/tags/8" \
     -d '{
       "data": {
         "type": "tags",
         "id": "8",
         "attributes": {
           "tag": "summer-collection-2026",
           "url_handle": "summer-collection-2026"
         }
       }
     }'
```

(Rename creates no 301 — see Side effects.)

### DELETE

```bash
curl -s -X DELETE \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/tags/8"
```

(Returns 204; pivot rows cascade-removed.)

## Example responses

### GET collection success

```json
{
  "data": [
    { "type": "tags", "id": "3", "attributes": { "tag": "sale", "url_handle": "sale" } },
    { "type": "tags", "id": "8", "attributes": { "tag": "summer-2026", "url_handle": "summer-2026" } }
  ],
  "meta": {
    "page": { "current-page": 1, "per-page": 50, "from": 1, "to": 2, "total": 2, "last-page": 1 }
  }
}
```

### GET single success

```json
{
  "data": {
    "type": "tags",
    "id": "8",
    "attributes": { "tag": "summer-2026", "url_handle": "summer-2026" }
  }
}
```

### POST 201 Created

```json
{
  "data": {
    "type": "tags",
    "id": "8",
    "attributes": { "tag": "summer-2026", "url_handle": "summer-2026" }
  }
}
```

### 422 — duplicate `tag` (case-insensitive)

```
HTTP 422 Unprocessable Entity
{"errors":[{"status":"422","source":{"pointer":"/data/attributes/tag"},"detail":"The tag has already been taken"}]}
```

## Equivalent UI

- [[marketing-blog-tags]] — master management screen (Marketing → Blog → Tags). Create with "+ Add tag", edit by clicking the Name, delete per-row, bulk-delete, search by name.
- [[marketing-blog-articles]] — Article editor's Tags multi-select; the most common place tags are created (auto-create on first use). The API does NOT auto-create from the article side — passing a non-existing tag ID in the `tags` relationship on [[api-posts]] returns 422.
- [[blog-tag|Blog Tag entity]] — full attribute reference.

## Related

- [[json-api-v2]] — API hub.
- [[api-posts]] — Blog Article resource; the `tags` hasMany relationship references tags created here.
- [[api-blogs]] — Blog Category resource (orthogonal parent taxonomy).
- [[api-redirects]] — manual 301 redirect rules; **required** to preserve SEO on tag rename / delete (no auto-track).
- [[api-customer-tags]] — **distinct** customer-tag resource (different table, different domain).
- [[marketing-blog-tags]] — admin UI for Blog Tags.
- [[seo-handling]] — URL handles + redirects concept page.
- [[settings-api-keys]] — authentication setup.

## Open questions

- Confirm whether POST with a duplicate `tag` (case-insensitive) returns 422 or silently re-uses the existing tag.
- Document the conditions under which the domain-level delete guard rejects a DELETE and returns 422 "Not Deletable".
- Verify whether the endpoint can query tags by attached-article-count (e.g., "find tags with zero articles for cleanup"). The admin list surfaces this via the Articles (N) button; the API may need a custom filter.
