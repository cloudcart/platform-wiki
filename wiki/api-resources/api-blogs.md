---
type: api-resource
resource_path: /api/v2/blogs
http_methods: [GET, POST, PATCH, DELETE]
related_entity: blog-category
related_features: [marketing-blog-category, marketing-blog-articles, marketing-blog-comment, marketing-blog-tags]
aliases: ["Blogs API", "Blog Categories API", "JSON-API v2 blogs", "API блог категории", "/blogs"]
tags: [api, json-api-v2, content]
plan_gates: ["blog_categories"]
created: 2026-05-26
updated: 2026-06-05
source_count: 4
---
# Blogs (JSON-API v2)

## Purpose

Programmatic CRUD on the merchant's [[blog-category|Blog Categories]] — the top-level containers for the storefront Blog section. Every [[blog-article|Blog Article]] must belong to exactly one Blog Category (the `blog` foreign key is required at publish), so this resource is a prerequisite for any integration that creates articles via [[api-posts]]: mirror an external CMS taxonomy, pre-create categories before bulk import, or maintain per-category SEO metadata.

The API resource type is `blogs` (matching the table); merchants call these "Blog Categories" in the admin UI. A Blog Category is **distinct from a Product Category** ([[products-categories]]) — different storefront namespace (`/blog/category/` vs `/category/`), FLAT hierarchy (no `parent_id`), and its own comment system.

## Endpoint

- **URL base:** `<store-host>/api/v2/blogs` — **full CRUD** (GET collection + single, POST, PATCH, DELETE). No custom routes. Creation may be capped by the `blog_categories` plan-feature limit (see Side effects).

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/v2/blogs` | List categories. Supports filter / sort / page. |
| GET | `/api/v2/blogs/{id}` | Fetch one category. |
| GET | `/api/v2/blogs?filter[url_handle]=<slug>` | **Search-one** — `url_handle` as the only filter returns a single category, not a list. |
| POST | `/api/v2/blogs` | Create a category (requires `name`). |
| PATCH | `/api/v2/blogs/{id}` | Update a category. |
| DELETE | `/api/v2/blogs/{id}` | Delete a category. May return 422 `"Not Deletable"` if a domain guard rejects it. |

Authentication, host resolution, common headers, status codes, and rate limits: see [[json-api-v2]].

## Attributes

| Attribute | Type | Writable on POST? | Writable on PATCH? | Required? | Notes / validation |
|---|---|---|---|---|---|
| `name` | string | yes | yes | **yes** on POST; `sometimes` on PATCH | `min:3`. Drives the category page heading + breadcrumbs. |
| `url_handle` | string | yes | yes | no | `alpha_dash`, `max:191`, unique in `blogs`. Storefront URL `/blog/category/<url_handle>`. Renaming auto-creates a 301 redirect (30-day TTL). |
| `image_url` | URL | yes | yes | no | Reachable image URL, validated via `exif_imagetype`. Uploaded synchronously; failures silently swallowed. |
| `comments` | enum `no` / `moderator` / `automatic` | yes | yes | no | Comment policy for every Article in this category. **Per-category, not per-article** — see [[blog-category]]. |
| `created_at` / `updated_at` | datetime | no | no | n/a | Read-only timestamps. |
| `image` | object | no | no | n/a | Internal file-asset ref. Read-only — use `image_url` to upload. |
| `max_thumb_size` | integer | no | no | n/a | Derived display attribute. |

GET responses include the `image_url` accessor pointing at the stored cover image. `seo_title` / `seo_description` exist on the [[blog-category|Blog Category entity]] but are **not in the validator rules** — they may be accepted via attribute pass-through, but this is not guaranteed; verify per response.

## Relationships

**None exposed** — `blogs` is a bare resource (no `hasOne` / `hasMany`). To list articles inside a category, query [[api-posts]] with `include=blog` and group on the integration side.

## Filtering & sorting

- **Filter:** `filter[url_handle]` (`filled|alpha_dash`) — when sent as the only filter, triggers single-record mode (returns one resource, not a paginated list). Plus every `blogs` table column is auto-merged into the allowed-filters list — e.g. `filter[id]`, `filter[name]`, `filter[comments]`, `filter[created_at]`. Value-equality only, no comparison operators.
- **Sort:** `id`, `name`, `created_at`, `updated_at` (prefix `-` for descending; multi-sort `sort=-created_at,name`).
- **Include:** none.

## Side effects on write

- **Image upload is synchronous** — when `image_url` is set, the image is fetched + stored inside the `saved` callback, holding the HTTP response open until done. Failures are silently swallowed (no 422), so a successful response does **not** guarantee the image landed. The validator's `after` hook pre-checks the content is a valid image (`exif_imagetype`); a non-image fails 422 at `/data/attributes/image_url`.
- **Slug change → 301 auto-track** — changing `url_handle` records the old slug in URL-handle-history (30-day TTL) for fallback redirects. After 30 days the merchant should save a permanent rule via [[api-redirects]] for SEO continuity.
- **500-article cap** — enforced at article-creation time (not on the category). The 501st article via [[api-posts]] fails with *"The blog can not have more than 500"*.
- **SEO fallback at render** — empty `seo_title` / `seo_description` fall back to the category name; the API may store NULL when not sent.
- **Delete is NOT BLOCKED by attached articles** — the `blogs_articles.blog_id` FK is `ON DELETE SET NULL`, so deleting a category silently orphans its articles (`blog_id` → NULL); they then fail "Blog is required" on the next edit. Re-assign articles first. The DELETE path also runs the domain `remove`, which may reject with HTTP 422 `"Not Deletable"`. On delete, 301 rules with `redirect_type=blog` / `item_id=<this category>` are auto-cleaned (see [[api-redirects]]).
- **No webhooks** — there is no `blog.*` event in the webhook catalogue ([[api-webhooks]]); integrations must poll for category changes.
- **Sitemap** — the category page enters the sitemap only when it has ≥ 1 active article; empty categories are visible on the storefront but absent from the sitemap.
- **Plan / permission gating** — creation is capped by the `blog_categories` per-plan counter (422/402 at the cap; lower tiers may lack the Blog feature — see [[plan-vs-feature-pack]]). Admin CRUD is gated by the `marketing.blog_categories` permission, but API-key access is separate: any active API key has full access regardless of admin role.

## Error examples (common 422 cases)

| Condition | `source.pointer` | `detail` |
|---|---|---|
| Missing `name` on POST | `/data/attributes/name` | *"The name field is required"* |
| `name` shorter than 3 chars | `/data/attributes/name` | *"The name must be at least 3 characters"* |
| Duplicate `url_handle` | `/data/attributes/url_handle` | *"The url handle has already been taken"* |
| `image_url` returns non-image content | `/data/attributes/image_url` | *"The content at … is not a valid image file"* |
| `comments` unknown enum value | `/data/attributes/comments` | *"The selected comments is invalid"* |
| Plan past-due (402, not 422) | n/a | *"Payment Required"* |
| Domain `remove` rejects deletion | n/a (top-level) | *"Not Deletable"* |

## Example requests

### GET collection

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/blogs?page[size]=20&sort=-created_at"
```

### GET single by `url_handle` (single-record mode)

`url_handle` as the **only** filter returns a single resource object, not a list.

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/blogs?filter[url_handle]=news"
```

### POST create with image (URL)

```bash
curl -s -X POST \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/blogs" \
     -d '{
       "data": {
         "type": "blogs",
         "attributes": {
           "name": "Company News",
           "url_handle": "news",
           "comments": "moderator",
           "image_url": "https://cdn.example.com/blog/news-cover.jpg"
         }
       }
     }'
```

Base64 upload uses a `data:` URI in the same `image_url` field:

```bash
curl -s -X POST \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/blogs" \
     -d '{
       "data": {
         "type": "blogs",
         "attributes": {
           "name": "Press",
           "image_url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAAB..."
         }
       }
     }'
```

Note: `image_url` uploads **synchronously** — large images hold the HTTP response open until the fetch completes.

### PATCH toggle comments

```bash
curl -s -X PATCH \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/blogs/7" \
     -d '{
       "data": {
         "type": "blogs",
         "id": "7",
         "attributes": { "comments": "no" }
       }
     }'
```

### DELETE

```bash
curl -s -X DELETE \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/blogs/7"
```

Returns 204. Child articles are **not deleted** — `blog_id` → NULL (re-assign via [[api-posts]] PATCH first).

## Example responses

### GET collection success

```json
{
  "data": [
    {
      "type": "blogs",
      "id": "7",
      "attributes": {
        "name": "Company News",
        "url_handle": "news",
        "comments": "moderator",
        "image_url": "https://<store-host>/media/blogs/news-cover.jpg",
        "created_at": "2026-05-12T08:30:00+00:00",
        "updated_at": "2026-05-30T11:02:14+00:00"
      }
    }
  ],
  "meta": {
    "page": { "current-page": 1, "per-page": 20, "from": 1, "to": 1, "total": 1, "last-page": 1 }
  }
}
```

### GET single success / POST 201 Created

Both return the single resource object (POST responds 201):

```json
{
  "data": {
    "type": "blogs",
    "id": "7",
    "attributes": {
      "name": "Company News",
      "url_handle": "news",
      "comments": "moderator",
      "image_url": "https://<store-host>/media/blogs/news-cover.jpg"
    }
  }
}
```

### 422 — missing `name`

```
HTTP 422 Unprocessable Entity
{"errors":[{"status":"422","source":{"pointer":"/data/attributes/name"},"detail":"The name field is required"}]}
```

### 422 — invalid image at `image_url`

```
HTTP 422 Unprocessable Entity
{"errors":[{"status":"422","source":{"pointer":"/data/attributes/image_url"},"detail":"The content at https://cdn.example.com/not-an-image.txt is not a valid image file"}]}
```

## Equivalent UI

- [[marketing-blog-category]] — master list + create/edit modal.
- [[marketing-blog-articles]] — Article editor; its `blog` FK references a category created here.
- [[apps-blog-csv-import]] — CSV import auto-creates categories (default `comments=automatic`).
- [[blog-category|Blog Category entity]] — full attribute reference.

## Related

- [[json-api-v2]] — API hub.
- [[api-posts]] — Blog Article resource (the children; `blog` references this resource).
- [[api-authors]] — Author resource (read-only).
- [[api-tags]] — Blog Tag resource (orthogonal flat taxonomy).
- [[api-redirects]] — 301 redirect rules; auto-cascade on category delete.
- [[marketing-blog-category]] — admin UI.
- [[seo-handling]] — URL handles + redirects concept.
- [[settings-api-keys]] — authentication setup.

## Open questions

- Confirm whether `seo_title` / `seo_description` are settable via this API (no explicit validator rules, but attribute pass-through may accept them), and whether empty `seo_*` is auto-filled with the category name on save or stored NULL.
- Document the exact conditions under which the domain `remove` rejects deletion with 422 "Not Deletable".
