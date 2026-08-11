---
type: entity
aliases: ["Blog Category", "Blog section", "Blog", "Category (blog)", "Категория на блог", "Блог категория", "Блог"]
tags: [blog, marketing, content, taxonomy, entity]
created: 2026-05-21
updated: 2026-05-26
source_count: 4
---
# Blog Category

## Identity

A **Blog Category** is the top-level container for [[blog-article|Blog Articles]] on the storefront — every Article must belong to **exactly one** Blog Category (publishing without one fails with *"Blog is required"*). Categories give the storefront its blog navigation: a merchant might run separate categories for *News*, *How-to guides*, and *Style tips*, each addressable at `/blog/category/<slug>` with its own hero image, title, SEO meta, and feed of articles. Its most distinctive setting is the **comment policy** (Automatic / Comments need approval / Comments off), which applies to every Article inside the category — commenting is managed per-category, not per-article. Categories are managed from the [[marketing-blog-category]] screen via a single create/edit modal — there is no separate Add or Edit screen.

A Blog Category is **distinct from a Product Category** ([[products-categories]] / [[category|product category entity]]): different storefront namespace (`/blog/category/` vs `/category/`), different cap rules, hierarchy, comment system, and content shape — editing one never affects the other. It is also distinct from a [[blog-tag|Blog Tag]]: tags are an orthogonal flat taxonomy where one Article carries many tags, while a Blog Category is the **single required parent** of each Article.

## Aliases

- **Blog Category** — the canonical merchant-facing term ("Add blog category", "Edit blog category").
- **Blog section** / **Category (blog)** — informal merchant phrasing.
- **Blog** — used loosely; the page header on [[marketing-blog-category]] is literally just **Category** under the Blog area, so merchants may say "create a new blog" meaning "create a new blog category".
- **Категория на блог** / **Блог категория** / **Блог** — Bulgarian terms used interchangeably across the Marketing → Blog area.

## Key Attributes

| Attribute | What the merchant controls | Notes |
|-----------|----------------------------|-------|
| **Title** (`name`) | Required free text, 3–191 chars | Errors: *"Name is required"* / *"Name is too long"* / *"Name is too short"*. Drives the category page heading and breadcrumbs. |
| **Comments policy** (`comments`) | Required — one of `no`, `moderator`, `automatic` | Drives every Article inside this Category at submission time. See Lifecycle / Comment policy below. Errors: *"Comments is required"* / *"Invalid comments type. Types: no,moderator,automatic"*. |
| **Cover image** (`image`) | Optional file upload | Hero banner on `/blog/category/<slug>` storefront page; thumbnail next to the title in the admin list (rendered `150x150`); optionally serves as the OG share image. Removable separately. |
| **URL handle** (`url_handle`) | Auto-derived from title at create; manually editable on edit | Storefront URL: `/blog/category/<url_handle>`. Renaming on an existing Category auto-creates a 301 redirect from the old slug (see [[marketing-seo-301-redirects]]). |
| **SEO title** (`seo_title`) | Optional, max 191 chars | `<title>` on the category page. Falls back to the Category name when empty. |
| **SEO description** (`seo_description`) | Optional, max 191 chars | `<meta name="description">` on the category page. Falls back to the Category name when empty. |
| **Created at** | n/a (auto) | Shown as a sortable column on the list. |
| **Updated at** | n/a (auto) | Shown as a column on the list; updated on every save. |

Blog Categories are **flat** (no parent) and have **no sort order** — the storefront and the admin list both render Categories newest-first by default; merchants cannot drag-reorder. There is **no `active` / `enabled` flag** — the storefront category page is always visible (an empty Category renders with "no articles yet").

**Delete with attached Articles** is **NOT blocked** — each child Article is silently unassigned (its Category link is cleared) rather than deleted. The Article remains saved but no longer belongs to any Category, and any next-publish save fails validation until the merchant re-assigns it. There is no cascade-or-reassign UI; re-assign Articles before deleting an active Category.

The **500-article cap per Category** is hard-enforced at Article-creation time with the message *"The blog can not have more than 500"*. This applies to every article-create path including CSV import.

**SEO fallback at SAVE time** — when the create / edit modal submits, blank `seo_title` and `seo_description` are auto-filled with the Category name before the request is sent. So "empty SEO" is stored as the Category name, not blank — merchants cannot leave SEO truly empty. The fallback is re-applied at storefront render time as a safety net.

**Sitemap inclusion** — the Category page `/blog/category/<slug>` is submitted to search engines only once the Category has at least one published (`active='yes'`) Article. Empty Categories are visible on the storefront but invisible to Google via sitemap until the first Article publishes.

**Plan-tier gate** — Category creation is capped by the `blog_categories` plan-feature limit. Lower-tier plans hit the plan cap before the 500-article business cap.

**Granular permission** — gated by `marketing.blog_categories` (separate from `marketing.blog_articles`, `marketing.blog_comments`, `marketing.blog_tags`). A role can moderate comments without being allowed to delete categories.

## Where it appears

- [[marketing-blog-category]] — the master list + create/edit modal (Sidebar → Marketing → Blog → Category).
- [[marketing-blog-articles]] — Article editor; the `blog_id` field picks which Category the Article belongs to (required at publish).
- [[marketing-blog-comment]] — comment moderation; each comment inherits its parent Category's `comments` policy at submission time.
- [[marketing-blog-tags]] — sibling flat taxonomy applied to the same Articles.
- [[apps-blog-csv-import]] — CSV import that can **auto-create** new Blog Categories on the fly when a row references a Category name that doesn't yet exist (new auto-created Categories default to `comments=automatic`).
- The storefront category page at `/blog/category/<url_handle>` — lists Articles where `active='yes'` (paginated).

## Programmatic access

A Blog Category can be managed via **JSON-API v2** at [[api-blogs]] (resource named `blogs`). Use it to mirror a content taxonomy from an external CMS, pre-create Categories before bulk-importing Articles via [[api-posts]], or maintain SEO metadata. A POST / PATCH runs the **same pipeline as the admin modal** — auto-slug, 301-redirect on `url_handle` rename, SEO fallback at save, the `blog_categories` plan cap, and the same unassign-not-block behaviour on delete (attached Articles survive unassigned, not deleted). API-specific: there is **no webhook event** for Blog Category CRUD, so integrations must poll. See [[json-api-v2]] for authentication and rate limits.

## Related

- [[blog-article]] — Articles belong to one Blog Category; `category_id` / `blog_id` is required FK at publish.
- [[blog-tag]] — orthogonal flat taxonomy; an Article has one Category + many Tags.
- [[blog-comment]] — comments inherit the parent Blog Category's `comments` policy.
- [[category]] — **distinct** product category entity (hierarchical), not to be confused with this.
- [[file-asset]] — the cover image is referenced as a file asset.
- [[seo-redirect]] — URL handle changes auto-create a 301 redirect from the old slug.
- [[seo-meta]] — per-category SEO title + description.
- [[seo-handling]] — concept page on URL handles, redirects, and meta tags.
- [[multi-language]] — per-language storefront rendering; Blog Categories localise their `name` / SEO fields in multilang stores.
- [[merchant-roles]] — Category management requires Marketing → Blog permission scope on the admin's role (see [[settings-staff]]).
- [[apps-disqus-comments]], [[apps-facebook-comments]] — third-party commenting apps that override the storefront's native comment form (the Category's `comments` setting effectively becomes inert once one of these is installed).

## Open Questions

- ⏸️ Whether the storefront supports **per-language slugs** for Blog Categories in all multilang configurations, or only when a specific language-routing option is enabled.
- ⏸️ Whether the URL-handle 301 redirect is per-store or per-locale on multilang sites — i.e., do all language slugs redirect at once or only the language whose handle changed.
