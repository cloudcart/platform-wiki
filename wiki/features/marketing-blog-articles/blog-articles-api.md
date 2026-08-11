---
type: feature
nav_path: "Marketing → Blog → Articles → API"
route_name: blog-articles-list
route_path: /admin/marketing-new/blog/articles
aliases: ["Articles API access", "Blog API write paths", "Posts API behavior", "Programmatic articles", "API на блог статии", "Програмен достъп до статии"]
tags: [marketing, blog, articles, api, json-api-v2]
plan_gates: ["blog_articles"]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[marketing-blog-articles]]. See the hub for the other aspects (list, editor, CSV import, rules, storefront visibility).

# Blog Articles — programmatic access (JSON-API v2)

## Purpose

This aspect documents the **JSON-API v2** programmatic surface for blog articles — what an external integration can read and write, which side effects fire on save (same as the UI), and the small set of API-specific behaviours that differ from the modern editor. The merchant-facing API page is [[api-posts]] (resource named `posts`; the underlying entity is Blog Article).

This aspect exists so the support LLM knows where to look when an article changes "by itself" (the API is the most common second-actor on a store's content).

## Where to find it

External integrations call [[api-posts]] at `/api/v2/posts`. Authentication, rate limits, and the JSON-API spec apply per [[json-api-v2]]. The Author dropdown is exposed read-only at [[api-authors]] for filling external author pickers.

## What the merchant can do here

The merchant doesn't see this surface directly — but a connected integration (their CMS, a content-syncing app, a Zapier flow, a custom script) can:

- **Create** an article (POST `/api/v2/posts`).
- **Update** an article (PATCH `/api/v2/posts/{id}`).
- **Delete** an article (DELETE `/api/v2/posts/{id}` — same hard-delete + comment cascade as the admin).
- **List** articles (GET `/api/v2/posts`) with filtering / sorting / pagination per [[json-api-v2]].
- **Read** the available authors (GET `/api/v2/authors`).
- **Set `publish_date`** to schedule a future publication — the only path that exposes this field (the modern editor does not — see [[blog-articles-storefront-visibility]]).

## Settings & fields

### Endpoint summary

| Method | Path | Notes |
|--------|------|-------|
| GET | `/api/v2/posts` | List with `filter[*]`, `sort`, pagination. |
| GET | `/api/v2/posts/{id}` | Single resource. |
| POST | `/api/v2/posts` | Create. Runs the platform code validation — see [[blog-articles-rules]]. |
| PATCH | `/api/v2/posts/{id}` | Update. Same validation. |
| DELETE | `/api/v2/posts/{id}` | Hard delete; cascades to comments. |

The full attribute / relationship / filter / sort surface lives on [[api-posts]].

### Per-area permission

API writes are gated by `marketing.blog_articles` (the same key as the admin UI), separate from `marketing.blog_categories` / `marketing.blog_comments` / `marketing.blog_tags`. See [[blog-articles-rules]].

## Business rules

### Same side effects as the admin save

A POST / PATCH triggers the same pipeline as the admin save:

- **Auto-slug + uniqueness** — Title-driven slug on first save; `url_handle` must be unique per store.
- **301-redirect auto-creation** — When `url_handle` is renamed on an existing article, a 301 redirect is created from the OLD slug to the new — via [[marketing-seo-301-redirects]].
- **Per-category 500-article cap** — The save fails with *"The blog can not have more than 500"* if the target category already has 500 articles. See [[blog-articles-rules]].
- **Tag auto-creation, capped** — Up to 100 tags per article, each ≤ 191 chars; `%` and `_` are silently filtered.
- **Plan-feature cap on article count** — `blog_articles` numeric cap is checked before the 500-cap.

### API-specific behaviour that differs from the editor

- **Scheduled publishing IS active via the API.** Setting `publish_date` to a future time causes the storefront to hide the article until `publish_date <= now` — enforced by the global "Published" SQL scope (timezone-aware, end-of-minute). No cron fires; the scope check auto-passes. The modern admin editor does NOT expose `publish_date` — only the API and the legacy editor do. See [[blog-articles-storefront-visibility]].
- **Inline images mirrored asynchronously (same as editor).** When `content` contains `<img src="https://external-domain/...">`, a queue task (`text_image_from_url`) mirrors each image and rewrites the `src` AFTER the HTTP save returns. Failures are silently swallowed.
- **`image_url` upload is synchronous** for the featured cover image (same as editor).
- **No `active='yes'` default override.** Unlike the editor (which always submits `active='yes'`), the API uses whatever value the integration sends — so an external CMS can create articles directly in draft state.

### Cascade behaviour applies to API deletes too

DELETE on an article wipes the row from `blogs_articles` and cascades to all of its comments via `ON DELETE CASCADE` on `comment__articles_comments.item_id`. Deleting the parent blog category does NOT delete the article — the FK is `ON DELETE SET NULL` and the article survives orphaned. See [[blog-articles-rules]] + [[marketing-blog-category]].

### Comment policy still inherited from the category

The article's comment behaviour (off / pre-moderated / auto-approved) is read from the parent category at submission time, not stored on the article itself — even when the article was created via the API. See [[blog-articles-storefront-visibility]] + [[marketing-blog-category]].

### Bulk import is a separate path

For migrating existing content from WordPress / Ghost / Medium without a custom API integration, see [[apps-blog-csv-import]] + [[blog-articles-csv-import]]. That app maps a CSV file's columns into the 5 article fields it supports. Tags, excerpt, publish date, and SEO fields are NOT importable via CSV — the merchant has to add them manually after the bulk import, or via this API.

## Related

- [[marketing-blog-articles]] — hub.
- [[api-posts]] — JSON-API v2 resource page (full attribute / relationship catalogue).
- [[api-authors]] — read-only author lookup.
- [[json-api-v2]] — auth, rate limits, side-effects principle.
- [[blog-articles-list]] — admin UI equivalent for browsing.
- [[blog-articles-editor]] — admin UI equivalent for create / edit.
- [[blog-articles-rules]] — the platform code validation that the API runs.
- [[blog-articles-storefront-visibility]] — `publish_date` semantics (API is the only way to set it from a third party).
- [[blog-articles-csv-import]] — bulk-import alternative.
- [[apps-blog-csv-import]] — the app that powers CSV import.
- [[marketing-seo-301-redirects]] — auto-created on slug rename via API too.
- [[background-queue-inventory]] — async `text_image_from_url` mirroring queue.

## Open questions

- Whether the API surfaces a separate `bulk update-status` endpoint equivalent to `POST /admin/api/core/blog/articles/update-status`, or whether external integrations must PATCH each article individually, is `(verify)` against [[api-posts]].
