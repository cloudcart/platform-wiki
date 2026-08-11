---
type: entity
nav_path: "Entity → Blog Article → Business rules"
aliases: ["Blog Article business rules", "Article slug uniqueness", "Article required category", "Article title length", "Article permission", "Article plan limit", "Article author", "Article SEO fallback", "Article comment moderation"]
tags: [entity, blog, marketing, content, business-rules, validation, permissions]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[blog-article]]. See the hub for the other aspects (data model, lifecycle, storefront & modules, programmatic access).

# Blog Article — Business rules

## Identity

The business rules of a **[[blog-article|Blog Article]]** are the validations, gating, and fallbacks the platform enforces on save and on display — slug uniqueness, required-category-at-publish, SEO meta fallbacks, title-length caps, permission gating, plan limits, and the per-category comment-moderation policy that articles inherit. These rules apply whether the article is saved from the admin editor or via the API.

## Aliases

- **Article validation rules** — informal phrasing for the same rule set.
- **Slug uniqueness** / **duplicate URL handle** — the most common save-blocking validation.
- **Required category** — the "Blog is required" publish validation.

## Key Attributes

The rules below behave as constraints (block save) or fallbacks (fill a default) on the article record.

### Slug uniqueness

Article slugs must be unique within the store. The platform blocks save on duplicate slug with a validation error. If the merchant renames a slug, the platform creates an SEO redirect from the old slug so external bookmarks and emails continue to work. See [[seo-redirect]].

### Required category at publish

An article cannot be `active = yes` without a `category_id`. The save validates this and rejects the publish. Drafts can exist without a category. The breadcrumb and category feed depend on this assignment. An article whose parent [[blog-category|Blog Category]] was deleted (`blog_id=NULL`, see [[blog-article-entity-data-model]]) will fail this "Blog is required" validation on the next edit.

### Featured image is optional but drives social-share appearance

When social platforms (Facebook, LinkedIn, etc.) crawl the article URL, they read the featured image as the `og:image`. Articles without a featured image fall back to the store's default share image — which is often unbranded — so the merchant should set one for social-share quality.

### SEO meta falls back to title + truncated body

When `meta_title` is empty, the storefront uses the article's `title` as the `<title>`. When `meta_description` is empty, it uses a truncation of `excerpt` (or `body` if `excerpt` is also empty). The merchant can override either to tune search-result snippets without editing the visible title or body. See [[seo-meta]].

### Title length: admin form 191, model-level 3191

The admin API form (the platform code) caps the article title at 191 characters with *"Name is too long"*. The model's underlying `_validateData` (used by legacy editor + CSV import + API v2) caps the title at **3,191 characters**. So depending on the save path, an unusually long title may be accepted by the API but rejected by the modern admin editor. Practical advice: keep titles under 191 for cross-path safety.

### Author is an admin user, not a customer

The `author_id` FK points at the `admins` table — every article author is a store admin (see [[settings-staff]]). DB-level constraint is `ON DELETE SET NULL` — deleting an admin clears the article's author but the article survives with no byline.

### Comments may be moderated (per-category, not per-article)

Comment moderation is a **per-[[blog-category|Blog Category]]** setting (not per article). The category's `comments` field is one of three values: `no` (commenting disabled), `moderator` (every new comment lands with status `pending` and must be approved by an admin from [[marketing-blog-comment]]), or `automatic` (every new comment lands with status `approved` and goes live immediately). All articles inside the category inherit the parent category's policy. See [[blog-comment]].

The storefront's `POST /blog/article/create-comment/{article_id}` endpoint is throttled at **5 submissions per 1 minute per IP** by the a submission throttle middleware. Exceeding the cap returns HTTP 429 with the error mapped to the `comment` field. This applies whether the visitor is a guest or a logged-in customer.

### No per-article views counter

There is **no dedicated `views` total surfaced in the admin** — the admin list does not show per-article view counts. Merchants who want article-level traffic data must use a separate web-analytics surface (e.g., the Google Analytics integration) — the platform itself does not track or expose per-article page-view totals in the UI.

### Permission gating

Article CRUD is gated by the granular `marketing.blog_articles` permission (separate from `marketing.blog_categories`, `marketing.blog_comments`, `marketing.blog_tags`). A role can have access to comments only, articles only, etc. Bulk publish/unpublish uses a single endpoint (`POST /admin/api/core/blog/articles/update-status`) with body `{ids: [], status: yes|no}` — all entries must exist in `blogs_articles`.

### Plan-tier limit on article count

Article creation is mapped to the `blog_articles` plan-feature limit (per the platform code). On lower tiers, the merchant may hit the plan cap before the per-category 500-cap — failures surface as the platform's standard plan-limit error. Same for the parent [[blog-category]] (`blog_categories` plan feature).

## Where it appears

- [[marketing-blog-articles]] — where every save-time validation fires.
- [[settings-staff]] — where `marketing.blog_articles` permission is granted per role.
- [[blog-article]] — entity hub.

## Related

- [[blog-article]] — hub.
- [[blog-article-entity-data-model]] — the fields these rules validate.
- [[blog-article-entity-lifecycle]] — the publish-state transitions these rules guard.
- [[blog-category]] — comment-moderation policy + plan limit live on the parent category.
- [[blog-comment]] — moderation queue the policy feeds.
- [[seo-redirect]] — slug-rename redirects.
- [[seo-meta]] — meta fallbacks.
- [[settings-staff]] — permission granting.

## Open Questions

None.
