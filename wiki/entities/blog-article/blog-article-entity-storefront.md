---
type: entity
nav_path: "Entity → Blog Article → Storefront & modules"
aliases: ["Blog Article storefront", "Blog Article modules", "recentArticles", "blog-list module", "Article inline images", "Article relationships", "Blog index page", "Article relations"]
tags: [entity, blog, marketing, content, storefront, modules]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[blog-article]]. See the hub for the other aspects (data model, lifecycle, business rules, programmatic access).

# Blog Article — Storefront & modules

## Identity

This aspect covers where a **[[blog-article|Blog Article]]** surfaces on the customer-facing storefront, the modules that embed article cards, the article's relationships to other entities, and the asynchronous handling of images pasted into the article body. It answers the merchant question "where does my published article actually show up?" and "why did the picture I pasted take a moment to appear?".

## Aliases

- **Blog index** — the `/blog` reverse-chronological list page.
- **`recentArticles`** / **`blog-list`** — storefront modules that embed article cards.
- **Article page** — the `/blog/<slug>` single-article view.

## Key Attributes

### Relationships

A Blog Article:

- **Belongs to one** [[blog-category|Blog Category]] via `category_id` — required at publish. Drives the storefront category feed and breadcrumb. See [[marketing-blog-category]].
- **Has many** [[blog-tag|Blog Tags]] via M2M — free-form tags. Tag pages list all articles with that tag. See [[marketing-blog-tags]].
- **Has many** [[blog-comment|Blog Comments]] 1:N — when the merchant enables commenting. Comments may be moderated (held for approval) or live. See [[marketing-blog-comment]].
- **Has many** translations — per-language overrides of title, body, excerpt, and SEO fields (see [[blog-article-entity-data-model]]).
- **References** [[file-asset|File Assets]] for the featured image and any inline images embedded in the body.
- **Appears in** storefront modules — `recentArticles`, `blog-list`, category-page feeds, and (optionally) related-products sections that point to an article.
- **Appears in** SEO redirect entries — when the slug changes, a 301 redirect from the old slug is auto-recorded (see [[seo-redirect]]).

### Storefront surfaces

- The blog index (`/blog`) lists all Published articles in reverse-chronological order.
- The blog category page (`/blog/category/<slug>`) lists articles in that category.
- The blog tag page (`/blog/tag/<slug>`) lists articles with that tag.
- The article page (`/blog/<slug>`) renders the article body, comments, and related articles.
- Storefront modules `recentArticles` and `blog-list` embed article cards on category pages, the home page, or static pages — see [[design-module-blog-article]].
- Newsletter campaigns frequently link to articles as teaser content.

### Modules surface only Published, recent articles

The `recentArticles` module and the `blog-list` module surface only articles in the computed Published state (`active = yes` and `published_at <= now` — see [[blog-article-entity-lifecycle]]). Drafts and Scheduled articles do not appear. Pinning specific articles above the chronological order is via `sort_order`.

### Inline images in body are mirrored to storage asynchronously

When the merchant pastes or drags an image into the rich-text editor, the editor saves the article with the external `<img src="...">` intact, then queues a background task to:

1. Download the external image into the store's media storage ([[file-asset]]).
2. Rewrite the article body's `<img src>` to a CloudCart-hosted URL.

The article briefly references the external URL on the storefront until the task finishes (seconds to minutes depending on queue depth). The task re-runs only when the merchant edits the body — re-saving without touching content does NOT re-queue. The same async mirroring applies to body images supplied via the API (see [[blog-article-entity-api]]).

## Where it appears

- The storefront blog index, category, tag, and article pages (`/blog`, `/blog/category/<slug>`, `/blog/tag/<slug>`, `/blog/<slug>`).
- [[design-module-blog-article]] — the `recentArticles` / `blog-list` storefront module.
- [[blog-article]] — entity hub.

## Related

- [[blog-article]] — hub.
- [[blog-article-entity-lifecycle]] — the Published-state gate the modules and feeds honour.
- [[blog-article-entity-data-model]] — the `sort_order`, `image`, `body` fields the storefront renders.
- [[blog-category]] — category feed + breadcrumb.
- [[blog-tag]] — tag feed.
- [[blog-comment]] — comments rendered on the article page.
- [[file-asset]] — featured + inline images.
- [[seo-redirect]] — slug-change redirects.
- [[design-module-blog-article]] — the storefront module.
- [[marketing-blog-category]] / [[marketing-blog-tags]] / [[marketing-blog-comment]] — sibling admin screens.

## Open Questions

None.
