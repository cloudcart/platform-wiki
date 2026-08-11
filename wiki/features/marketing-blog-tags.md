---
type: feature
nav_path: "Marketing → Blog → Tags"
route_name: blog-tags
route_path: /admin/marketing-new/blog/tags
aliases: ["Blog tags", "Article tags", "Тагове на блог", "Етикети на статии", "Блог етикети"]
tags: [marketing, blog, tags, taxonomy, content]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 8
---

# Blog Tags

## Purpose

**Blog Tags** are a flat, free-form taxonomy that the merchant attaches to [[marketing-blog-articles]] alongside the article's required blog category. Where blog categories sit at the top of the hierarchy ("News", "How-to", "Customer stories"), tags cut sideways: an article might be in the "How-to" category and simultaneously tagged `summer-2026`, `outdoor`, `beginner`, and `under-100`. The merchant invents tag names freely — they don't need to be pre-approved.

Tags drive **storefront discovery** (every tag has its own `/blog/tag/<slug>` page), **cross-category browsing**, **SEO long-tail keywords**, and **related-content recommendations** on article pages. This page is **distinct from product tags** ([[products-tags]]) — different storage, different storefront namespace. A tag named `summer` on a blog article is unrelated to a tag named `summer` on a product.

This topic is split into focused aspect pages; this hub gives the overview and points to them.

## Sub-pages (in this cluster)

- [[blog-tags-list]] — the central admin screen: list columns, the Add / Edit modal, search, per-row Articles button (disabled at zero), bulk-delete repaging, and what the merchant can / cannot do.
- [[blog-tags-lifecycle]] — how tags are born (auto-create from the article editor vs "+ Add tag"), lowercase storage, race-safe uniqueness, input sanitization (`%`/`_` stripping), the 100-tags/191-chars caps, and delete cascade.
- [[blog-tags-storefront-seo]] — the `/blog/tag/<slug>` storefront page, SEO long-tail keywords, the no-301-on-rename/delete trap, sitemap exclusion, and the missing webhook events.
- [[blog-tags-api-permissions]] — JSON-API v2 endpoint surface, the PATCH-for-update exception, the granular `marketing.blog_tags` staff permission, and (absent) plan gating.

## Where to find it

Sidebar → **Marketing** → **Blog** → **Tags**.

Route name `blog-tags`; path `/admin/marketing-new/blog/tags`; component `MarketingBlogTagsPage`. Header icon is the tag icon (`far fa-tag`). The breadcrumb reads "Marketing → Article tags".

Unlike Blog Articles or Categories, this is a **centrally managed** tag list — the merchant CAN create, edit, and delete tags from this page without touching individual articles. (Compare with [[products-tags]], which has no central admin and is only edited from per-product editors.) The list is also auto-populated as soon as a merchant types a new tag into the [[marketing-blog-articles]] editor — auto-create on first use (see [[blog-tags-lifecycle]]).

## What the merchant can do here

- See, search, create, rename, delete, and bulk-delete blog tags from one central list — see [[blog-tags-list]].
- Jump from a tag to its filtered article list (Articles (N) button) — see [[blog-tags-list]].
- Let tags auto-create when typed into the article editor — see [[blog-tags-lifecycle]].
- Manage tags programmatically via JSON-API v2 — see [[blog-tags-api-permissions]].

What the merchant **cannot** do: set per-tag SEO metadata, build a tag hierarchy (tags are flat), assign tags to articles from this page, or merge two tags. Details on [[blog-tags-list]] and [[blog-tags-storefront-seo]].

## Settings & fields

A blog tag carries only two fields — the full table is on [[blog-tags-list]]:

| Field | Validation | Notes |
|-------|------------|-------|
| **Tag name** (`tag`) | Required. String, 2 ≤ length ≤ 191. **Unique**. | Stored lowercase. |
| **URL handle** (`url_handle`) | Auto-derived from the name. | Storefront URL `/blog/tag/<url_handle>`. |

Per-article caps (100 tags/article, 191 chars/tag) are enforced in the article editor, not here — see [[blog-tags-lifecycle]].

## Business rules

Each rule is documented in full on its aspect page:

- **Auto-create + lowercase + race-safe uniqueness + sanitization + delete cascade** — see [[blog-tags-lifecycle]].
- **`/blog/tag/<slug>` page, NO 301 on rename/delete, sitemap exclusion, no webhook events** — see [[blog-tags-storefront-seo]].
- **Endpoint surface, PATCH-for-update exception, `marketing.blog_tags` permission, not plan-gated** — see [[blog-tags-api-permissions]].

## Related

- [[marketing-blog-articles]] — tags attach to articles via the editor's multi-select.
- [[marketing-blog-category]] — orthogonal hierarchy (one category per article + many tags).
- [[marketing-blog-comment]] — comments live on articles, not on tags.
- [[products-tags]] — sister concept on products (different table, different semantics).
- [[marketing]] — parent hub.
- [[apps-blog-csv-import]] — tags are NOT mapped by the CSV importer (only 5 columns are imported); merchant must tag after import.
- [[blog-tag]] — entity page.
- [[blog-article]] — entity page.
- [[api-tags]] — JSON-API v2 tag resource.

## Open questions

No outstanding questions.
