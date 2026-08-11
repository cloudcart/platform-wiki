---
type: entity
nav_path: "Entity → Blog Article → Programmatic access"
aliases: ["Blog Article API", "Article JSON-API v2", "posts resource", "Article API side effects", "Article publish_date API", "Article image_url API", "Article API scheduled publish"]
tags: [entity, blog, marketing, content, api, json-api-v2]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[blog-article]]. See the hub for the other aspects (data model, lifecycle, business rules, storefront & modules).

# Blog Article — Programmatic access

## Identity

A **[[blog-article|Blog Article]]** can be created and edited programmatically through **JSON-API v2**, where it is exposed as the `posts` resource. This aspect covers what an external integration can read and write, the side effects a write triggers (identical to the admin save), and the few behaviours that differ between the API path and the modern admin editor.

## Aliases

- **`posts` resource** — the JSON-API v2 resource name; the underlying entity is the Blog Article.
- **Article API** — informal phrasing for the programmatic surface.
- **`publish_date`** — the API field name for the scheduled-publish datetime.

## Key Attributes

### Endpoints

A Blog Article is managed via JSON-API v2 at [[api-posts]] (resource named `posts`; underlying entity is Blog Article). The Author dropdown is exposed read-only at [[api-authors]].

### Same side effects as the admin save

A POST / PATCH triggers the same pipeline as the admin save:

- auto-slug + uniqueness validation;
- **301-redirect auto-creation** on `url_handle` rename (via [[api-redirects]]);
- per-category 500-article cap;
- tag auto-creation (capped at 100 × 191 chars);
- comment-policy inheritance from the parent [[blog-category|Blog Category]].

See [[blog-article-entity-business-rules]] for the full rule set these enforce.

### API-specific behaviours worth knowing

- **Scheduled publishing IS active via the API** — `publish_date` in the future causes the storefront to hide the article until `publish_date <= now`, enforced by the global "Published" SQL scope (timezone-aware, end-of-minute). No cron fires; the scope check auto-passes. The modern admin editor doesn't expose this field — only the API and the legacy editor do. See [[blog-article-entity-lifecycle]].
- **Inline images mirrored asynchronously** — when `content` contains `<img src="https://external-domain/...">`, a queue task (`text_image_from_url`) mirrors each image into [[file-asset]] storage and rewrites the `src` AFTER the HTTP save returns. Failures are silently swallowed. See [[blog-article-entity-storefront]] for the same mechanism on the admin save path.
- **`image_url` upload is synchronous** for the featured cover image — unlike the body images, the cover is fetched before the response returns.
- **Per-area permission** — gated by `marketing.blog_articles`, separate from categories / comments / tags.

See [[json-api-v2]] for authentication, rate limits, and the side-effects principle, and [[settings-api-keys]] for credential management.

## Where it appears

- [[api-posts]] — the JSON-API v2 resource for Blog Articles.
- [[api-authors]] — read-only author dropdown.
- [[api-redirects]] — slug-rename 301 redirects.
- [[blog-article]] — entity hub.

## Related

- [[blog-article]] — hub.
- [[blog-article-entity-business-rules]] — the validations these API writes also enforce.
- [[blog-article-entity-lifecycle]] — `publish_date` scheduled-publish semantics.
- [[blog-article-entity-storefront]] — async inline-image mirroring.
- [[api-posts]] — the `posts` resource page.
- [[api-authors]] — read-only authors.
- [[api-redirects]] — redirect entries.
- [[json-api-v2]] — API hub (auth, rate limits, side-effects principle).
- [[settings-api-keys]] — API credentials.
- [[settings-hooks]] — webhooks fired on article writes.

## Open Questions

None.
