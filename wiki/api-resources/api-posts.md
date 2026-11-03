---
type: api-resource
resource_path: /api/v2/posts
http_methods: [GET, POST, PATCH, DELETE]
related_entity: blog-article
related_features: [marketing-blog-articles, marketing-blog-category, marketing-blog-tags, marketing-blog-comment, apps-blog-csv-import]
aliases: ["Posts API", "Blog Articles API", "JSON-API v2 posts", "API статии", "/posts"]
tags: [api, json-api-v2, content]
plan_gates: []
created: 2026-05-26
updated: 2026-06-05
source_count: 4
---
# Posts (JSON-API v2)

## Purpose

Programmatic CRUD on the merchant's [[blog-article|Blog Articles]] — the chronological content in the storefront Blog section. Typical uses: mirror content from an external CMS, bulk-create articles, schedule publish state, or read articles for cross-posting.

The resource is named `posts`, but the entity is **Blog Article**. Every article must belong to a [[blog-category|Blog Category]] (`blog` required at create) AND have an author (`author` required at create), and may carry many [[blog-tag|Blog Tags]]. A Post differs from a [[marketing-landing-pages|Landing Page]] and from a product description (on a [[product|Product]]).

## Endpoint

- **URL base:** `<store-host>/api/v2/posts` — **full CRUD** (GET collection + single, POST, PATCH, DELETE). No app requirements.
- **Custom routes:** none. Standard JSON:API relationship endpoints exist for `blog`, `author`, `tags` (`/api/v2/posts/{id}/relationships/<rel>`).

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/v2/posts` | List articles (filter / sort / include / page). |
| GET | `/api/v2/posts/{id}` | Fetch one article. |
| GET | `/api/v2/posts?filter[url_handle]=<slug>` | **Search-one** — `url_handle` as the only filter returns a single article, not a list. |
| POST | `/api/v2/posts` | Create. Requires `name`, `content`, `blog`, `author`. |
| PATCH | `/api/v2/posts/{id}` | Update. |
| DELETE | `/api/v2/posts/{id}` | Delete. May return 422 `"Not Deletable"`. |
| GET / PATCH / DELETE | `/api/v2/posts/{id}/relationships/{blog\|author\|tags}` | Manage one relationship. |

Authentication, host resolution, common headers, status codes, and rate limits: see [[json-api-v2]].

## Attributes

| Attribute | Type | Writable on POST? | Writable on PATCH? | Required? | Notes / validation |
|---|---|---|---|---|---|
| `name` | string | yes | yes | **yes** on POST; `sometimes` on PATCH | `min:3` chars. Article title. |
| `content` | string | yes | yes | **yes** on POST; `sometimes` on PATCH | Rich-text HTML body. No declared length limit. |
| `url_handle` | string | yes | yes | no | `alpha_dash`, `max:191`, unique. URL slug — drives `/blog/<slug>`; renaming auto-creates a 301 redirect. |
| `image_url` | URL | yes | yes | no | Uploaded synchronously on save (see Side effects). |
| `excerpt` / `short_description` | string | yes | yes | no | Summary on blog index / feeds / newsletter. Falls back to truncated `content`. |
| `active` | enum `yes` / `no` | yes | yes | no | Master visibility flag; `no` removes the article from `/blog/`. |
| `publish_date` | datetime | yes | yes | no | **Scheduled publishing IS active** — see Side effects. Not exposed in the modern admin editor; the API and legacy editor are. |
| `meta_title` / `meta_description` | string | yes | yes | no | SEO overrides; fall back to title / truncated body. |
| `blog_id` / `author_id` | integer | no | no | n/a | Read-only; set via the `blog` / `author` relationships. |
| `created_at` / `updated_at` | datetime | no | no | n/a | Read-only timestamps. |
| `image` | object | no | no | n/a | Internal file-asset reference. Upload via `image_url`. |
| `max_thumb_size` | integer | no | no | n/a | Derived display attribute. |
| `id` | integer | n/a | n/a | n/a | **Hidden** as an attribute, but the JSON:API resource `id` member carries the row's primary key. |

GET responses include the appended `image_url` accessor.

## Relationships

| Name | Cardinality | Target type | Writable? | Notes |
|---|---|---|---|---|
| `blog` | belongsTo | `blogs` | **Required** on POST | Parent [[blog-category\|Blog Category]] — see [[api-blogs]]. |
| `author` | belongsTo | `authors` | **Required** on POST | The article author — see [[api-authors]]. |
| `tags` | hasMany | `tags` | yes | Article tag links — see [[api-tags]]. Expects existing tag IDs; new tags are not auto-created here (unlike the admin editor). |

## Filtering & sorting

- **Filtering:** `filter[url_handle]` (`filled|alpha_dash`; as the only filter → single-record mode), **plus every article column** by value-equality (`filter[id]`, `filter[blog_id]`, `filter[author_id]`, `filter[active]`, `filter[publish_date]`, `filter[created_at]`, `filter[updated_at]`). No comparison operators.
- **Sorting:** `id`, `name`, `created_at`, `updated_at` (prefix `-` for descending).
- **Includes:** `blog`, `author`, `tags`.

## Side effects on write

- **Image upload synchronous on save** — the response is held until the image is fetched + stored, but failures are silently swallowed: a 2xx does NOT guarantee the image landed. A non-image `image_url` returns 422 (`/data/attributes/image_url`).
- **Inline images mirrored asynchronously** — external `<img src="https://...">` URLs in `content` are copied to CloudCart storage and the `src` rewritten by a background task; the save does NOT wait.
- **Scheduled publishing** — a future `publish_date` hides the article from `/blog/` until the timestamp passes. **No cron fires** — the "Published" SQL scope simply starts passing, and **no admin notification** fires.
- **URL-handle 301 auto-track** — changing `url_handle` records the old slug for 30-day fallback redirects; after that, save a permanent rule via [[api-redirects]].
- **Cascade on delete** — DELETE removes the article + its tag pivot rows + its [[blog-comment|Blog Comments]]; a rejected delete returns HTTP 422 `"Not Deletable"`.
- **Cache invalidation** — saving rebuilds cached category / tag feeds; external CDN / browser caches may lag.
- **No webhooks** — there is **no `post.*` event** ([[api-webhooks]]); integrations must poll.

**Plan / permission gating:** No plan-feature counter, but a **500-article cap per category** at create (422 *"The blog can not have more than 500"*). Admin-panel CRUD is gated by `marketing.blog_articles`; API-key access is separate — any active key has full access.

## Error examples (common 422 cases)

| Condition | `source.pointer` | `detail` |
|---|---|---|
| Missing required POST field (`name` / `content` / `blog` / `author`) | `/data/attributes/<field>` or `/data/relationships/<rel>` | *"The `<field>` field is required"* |
| `blog` references a non-existent category | `/data/relationships/blog` | *"The blog field must be a to-one relationship containing blogs resources"* |
| Duplicate `url_handle` | `/data/attributes/url_handle` | *"The url handle has already been taken"* |
| `image_url` returns non-image content | `/data/attributes/image_url` | *"The content at … is not a valid image file"* |
| 501st article in a category | `/data/attributes/blog_id` | *"The blog can not have more than 500"* |
| Plan-expired (402, not 422) | n/a | *"Payment Required"* — plan is past-due. |

## Example requests

Write methods add `-X <METHOD>` + `Content-Type: application/vnd.api+json`.

### GET collection with includes

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/posts?include=blog,author,tags&page[size]=20&sort=-created_at"
```

### GET single by `url_handle`

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/posts?filter[url_handle]=spring-sale-2026"
```

### POST minimal (`blog` + `author` required)

```bash
curl -s -X POST \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/posts" \
     -d '{
       "data": {
         "type": "posts",
         "attributes": {
           "name": "Spring Sale 2026",
           "content": "<p>Our biggest spring sale is here.</p>",
           "url_handle": "spring-sale-2026",
           "excerpt": "Save up to 40% on selected items.",
           "active": "yes"
         },
         "relationships": {
           "blog": { "data": { "type": "blogs", "id": "7" } },
           "author": { "data": { "type": "authors", "id": "12" } }
         }
       }
     }'
```

For **scheduled publishing**, add `"publish_date": "2026-12-01T08:00:00+00:00"` to the attributes (see Side effects). **PATCH** sends the same `{"data":{"type":"posts","id":"…","attributes":{…}}}` shape with only changed fields; **DELETE** returns 204.

## Example responses

### GET collection (with `?include=blog,author,tags`)

```json
{
  "data": [
    {
      "type": "posts",
      "id": "45",
      "attributes": {
        "name": "Spring Sale 2026",
        "url_handle": "spring-sale-2026",
        "excerpt": "Save up to 40% on selected items.",
        "active": "yes",
        "publish_date": "2026-03-01T08:00:00+00:00",
        "image_url": "https://<store-host>/media/posts/spring-sale-2026.jpg",
        "created_at": "2026-02-20T12:00:00+00:00",
        "updated_at": "2026-02-28T09:11:00+00:00"
      },
      "relationships": {
        "blog": { "data": { "type": "blogs", "id": "7" } },
        "author": { "data": { "type": "authors", "id": "12" } },
        "tags": { "data": [{ "type": "tags", "id": "3" }, { "type": "tags", "id": "8" }] }
      }
    }
  ],
  "included": [
    { "type": "blogs", "id": "7", "attributes": { "name": "Company News", "url_handle": "news" } },
    { "type": "authors", "id": "12", "attributes": { "admin_type": "owner" } },
    { "type": "tags", "id": "3", "attributes": { "tag": "sale", "url_handle": "sale" } },
    { "type": "tags", "id": "8", "attributes": { "tag": "spring", "url_handle": "spring" } }
  ],
  "meta": {
    "page": { "current-page": 1, "per-page": 20, "from": 1, "to": 1, "total": 1, "last-page": 1 }
  }
}
```

A POST 201 returns the same shape with the new `id`. Validation failures return 422 per the error table above.

## Equivalent UI

- [[marketing-blog-articles]] — article list + editor (full CRUD).
- [[marketing-blog-category]] — the `blog` parent.
- [[marketing-blog-tags]] — the `tags` relationship.
- [[marketing-blog-comment]] — comment moderation (cascades on delete).
- [[apps-blog-csv-import]] — CSV import (DOES NOT map tags).
- [[blog-article|Blog Article entity]] — full attribute reference.

## Related

- [[json-api-v2]] — API hub.
- [[api-blogs]] — Blog Category (required parent).
- [[api-authors]] — Author (read-only).
- [[api-tags]] — Blog Tag.
- [[api-redirects]] — manual 301 rules (after the 30-day URL-handle-history TTL).
- [[marketing-blog-articles]] — admin UI.
- [[seo-handling]] — URL handles + redirects.
- [[settings-api-keys]] — authentication setup.

## Open questions

- Whether the caller must pre-create tags via [[api-tags]] before attaching them, or whether the API auto-creates new tag names by string match (the admin editor auto-creates; the API path is unverified). `(verify)`
- Whether a silently-swallowed image-upload failure leaves the article saved without the image, and whether any retry path exists. `(verify)`
- The exact conditions under which a delete is rejected with 422 `"Not Deletable"`. `(verify)`
