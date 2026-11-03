---
type: entity
nav_path: "Entity → Blog Article → Data model"
aliases: ["Blog Article data model", "Blog Article fields", "Blog Article attributes", "Article slug", "Article body", "Article excerpt", "Article category_id", "Article translations", "Article cascade delete"]
tags: [entity, blog, marketing, content, data-model, fields]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[blog-article]]. See the hub for the other aspects (lifecycle, business rules, storefront & modules, programmatic access).

# Blog Article — Data model

## Identity

The data model of a **[[blog-article|Blog Article]]** is the set of fields the merchant configures on a single article — headline, URL handle, rich-text body, summary, featured image, SEO overrides, and the relationships to its parent [[blog-category|Blog Category]] and [[blog-tag|Blog Tags]]. The article is the merchant's content-marketing record: a title + URL handle + body, plus the metadata that controls how it appears on the storefront blog index, in category and tag feeds, and in newsletter teasers.

Three structural rules recur across the other aspects of this entity and are encoded here:

1. **Stock-style single record per article** — there is one article row carrying all of the fields below; the `body` is rich-text HTML edited with the same WYSIWYG editor as product descriptions.
2. **The parent-category FK is `ON DELETE SET NULL`** — deleting a [[blog-category|Blog Category]] does not cascade-delete its articles; they survive orphaned.
3. **Per-language translations are independent copies** — translating one locale never auto-fills another.

## Aliases

- **Blog Article fields** / **Article columns** / **Article record** — informal phrasing for the same attribute set.
- **`slug`** / **`url_handle`** — the URL handle; appears in tickets phrased as "the article address / link".
- **`body`** / **content** — the rich-text article body.
- **`excerpt`** / **short description** — the summary used in teasers.

## Key Attributes

| Field | What it stores | Notes |
|-------|----------------|-------|
| `title` | Article headline | Required. Displayed everywhere — list, edit header, storefront article page, RSS feed, newsletter teasers. |
| `slug` / `url_handle` | URL slug | Drives the storefront path `/blog/<slug>`. Renaming creates a 301 redirect from the old slug. Must be unique within the store. |
| `body` | Rich-text content | The article's main HTML body. Supports formatting, images (lifted into [[file-asset]] storage on save), embedded videos, internal links, and CTAs. Same rich-text editor as product descriptions. |
| `excerpt` / `short_description` | Summary text | Optional. Shown on the blog index, category feeds, and in newsletter teaser blocks. Falls back to a truncation of `body` when empty. |
| `author` | Author name / byline | Free text. Optional. Shown on the storefront article page when set. |
| `category_id` | FK → [[blog-category]] | Required at publish. Drives which category page lists the article and the breadcrumb on the storefront. |
| `tags` | M2M with [[blog-tag]] | Free-form tags for filtering and tag-feed pages. |
| `image` / `image_id` | Featured image | The hero image shown at the top of the article and as the thumbnail in lists. Optional but recommended for visual appeal. |
| `active` | yes / no | Master visibility flag. When `no`, the article is treated as Draft and hidden from the storefront. (There is no separate `status` enum on the article — the wiki previously claimed `draft / published / archived` values; the actual column is `active`.) |
| `published_at` | Datetime when published | Drives the chronological order of articles on the index. When in the future, the article is scheduled (treated as Draft until that time). |
| `meta_title` | SEO `<title>` | Optional override of the default (the article's title). Used in search results. |
| `meta_description` | SEO `<meta name="description">` | Optional override. Falls back to a truncation of `excerpt` / `body`. |
| `views` | Hit counter | Public article-page views. Read-only; updated by the storefront. |
| `sort_order` | Manual sort number | Lower = earlier; used when the merchant wants to pin specific articles above the chronological order. |
| `date_added`, `date_modified` | Timestamps | `date_added` = creation. `date_modified` = last save. |

## Cascade-delete rules

- **`category_id` / `blog_id` (FK)** — DB-level constraint is `ON DELETE SET NULL`. Deleting the parent [[blog-category|Blog Category]] does NOT cascade-delete the article. The article survives "orphaned" with `blog_id=NULL` and will fail the "Blog is required" validation on any subsequent edit (see [[blog-article-entity-business-rules]]).
- **`tags` (M2M `tags__articles_tags__items`)** — cascading delete on both sides: deleting an article removes its junction rows; deleting a tag removes its junction rows but the article survives untagged.
- **`author_id`** — points at the `admins` table; `ON DELETE SET NULL`. Deleting an admin clears the byline but the article survives.

## Per-language translations

The article carries **per-language translations** for `title`, `body`, `excerpt`, `meta_title`, and `meta_description` — multilang stores can publish the same article in multiple languages with independent SEO. Each language has its own copy — translating one language does NOT auto-translate others. The slug can also be per-language, though in many stores it stays the same across languages for consistent URLs. See [[multi-language]].

## Where it appears

- [[marketing-blog-articles]] — the master list + edit screen where every field above is set.
- [[blog-article]] — entity hub.
- The storefront article page (`/blog/<slug>`) renders `title`, `body`, `image`, `author`, and `published_at`.

## Related

- [[blog-article]] — hub.
- [[blog-category]] — parent via `category_id`.
- [[blog-tag]] — M2M via `tags`.
- [[file-asset]] — featured image + inline body images.
- [[multi-language]] — per-locale field translations.
- [[marketing-blog-articles]] — admin list + editor.

## Open Questions

None.
