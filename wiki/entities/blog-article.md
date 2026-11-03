---
type: entity
nav_path: "Entity → Blog Article"
aliases: ["Blog Article", "Blog post", "Article", "Post", "News article", "Блог статия", "Статия", "Публикация"]
tags: [entity, blog, marketing, content]
created: 2026-05-21
updated: 2026-06-10
source_count: 5
---
# Blog Article

## Identity

A **Blog Article** is a chronological piece of content — an article, news post, or guide — that the merchant publishes in the storefront's **Blog** section. Each Article is identified by a title and a URL handle, belongs to a [[blog-category|Blog Category]], can be tagged with one or more [[blog-tag|Blog Tags]], and carries a rich-text body that the merchant edits with the same WYSIWYG used for product descriptions. Articles power newsletter teasers ("Read our latest guide"), category-page content, SEO landing pages, and the storefront's blog index — they're the merchant's content-marketing surface inside CloudCart.

A Blog Article is distinct from a **product description** (which lives on a single [[product|Product]]) and from a **Static Page** (which is a one-off content page outside the chronological blog flow). Articles appear in dated lists ("Latest articles"), in [[blog-category|category]] feeds, in [[blog-tag|tag]] feeds, and in storefront modules (`recentArticles`, `blog-list`). The blog section is managed under Marketing → Blog Articles; see [[marketing-blog-articles]].

Visibility is driven by the `active` flag plus `published_at` — there is **no** `draft / published / archived` status enum on the article (the wiki previously claimed one; the actual column is `active`). See [[blog-article-entity-lifecycle]].

## Aliases

- **Blog Article** — the canonical merchant-facing term in the admin UI ("Add blog article", "Edit blog article").
- **Blog post** / **Post** — informal phrasing used by merchants who think in WordPress / Shopify terms.
- **Article** — short form used throughout the admin.
- **News article** — used by merchants whose blog functions as a news feed.
- **Блог статия** / **Статия** / **Публикация** — Bulgarian terms used interchangeably.

## Key Attributes

The article record carries a title, a unique `slug` / `url_handle`, a rich-text `body`, an optional `excerpt`, a featured `image`, an `active` visibility flag, a `published_at` datetime, SEO `meta_title` / `meta_description` overrides, a `sort_order` for pinning, plus the parent `category_id` FK and an M2M `tags` relationship. The full attribute table, cascade-delete rules (`category_id` is `ON DELETE SET NULL`), and per-language translation model live on [[blog-article-entity-data-model]].

Headline points:

- **One article belongs to one [[blog-category|Blog Category]]** via `category_id`, required at publish — see [[blog-article-entity-business-rules]].
- **Slug must be unique within the store**; renaming auto-creates a 301 redirect from the old slug.
- **Title length caps differ by save path** — 191 chars in the modern admin form, 3,191 at the model level (legacy editor / CSV import / API). Keep under 191 for cross-path safety.
- **The author is a store admin, not a customer** — `author_id` points at the `admins` table.
- **Per-language translations** of `title`, `body`, `excerpt`, and SEO fields are independent copies.

## Sub-pages (in this cluster)

This entity is split into 5 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[blog-article-entity-data-model]] — the full field table; `ON DELETE SET NULL` parent-category FK; tag M2M cascade rules; per-language translations.
- [[blog-article-entity-lifecycle]] — Draft / Scheduled / Published / Deleted states driven by `active` + `published_at`; passive timezone-aware scheduled publish; retire-vs-delete.
- [[blog-article-entity-business-rules]] — slug uniqueness, required-category-at-publish, SEO meta fallbacks, the 191/3191 title caps, `marketing.blog_articles` permission, plan limits, per-category comment moderation, comment-submission throttle.
- [[blog-article-entity-storefront]] — relationships; storefront surfaces (`/blog`, category, tag, article pages); `recentArticles` / `blog-list` modules; async inline-image mirroring.
- [[blog-article-entity-api]] — JSON-API v2 `posts` resource; identical side effects to the admin save; `publish_date` scheduled-publish (API/legacy only); sync cover vs async body images.

## Where it appears

- [[marketing-blog-articles]] — the master list + edit screen for blog articles.
- [[marketing-blog-category]] — blog category management; articles belong to one category.
- [[marketing-blog-tags]] — blog tag management; articles have many tags.
- [[marketing-blog-comment]] — comment moderation per article (policy inherited from the category).
- [[design-module-blog-article]] — the `recentArticles` / `blog-list` storefront module.
- [[api-posts]] — the JSON-API v2 `posts` resource for programmatic article management.

Storefront surfaces (detailed on [[blog-article-entity-storefront]]): the blog index `/blog`, category page `/blog/category/<slug>`, tag page `/blog/tag/<slug>`, the article page `/blog/<slug>`, and newsletter campaign teasers.

## Related

### Related entities

- [[blog-category]] — required parent at publish time.
- [[blog-tag]] — M2M tag relationship.
- [[blog-comment]] — comments on the article.
- [[file-asset]] — featured image and inline images.
- [[seo-redirect]] — slug changes create redirect entries.
- [[seo-meta]] — per-article SEO overrides.

### Cross-cutting concepts

- [[seo-handling]] — URL handles, redirects, meta tags — same machinery as products.
- [[multi-language]] — per-locale translations of article content.
- [[json-api-v2]] — programmatic access via the `posts` resource.

### Settings & feature pages

- [[marketing-blog-articles]] — primary admin screen.
- [[marketing-blog-category]] — category management.
- [[marketing-blog-tags]] — tag management.
- [[marketing-blog-comment]] — comment moderation.

## Open Questions

- ⏸️ Whether the storefront supports per-language slugs for articles in all multilang configurations, or only when a specific language-routing option is enabled.
