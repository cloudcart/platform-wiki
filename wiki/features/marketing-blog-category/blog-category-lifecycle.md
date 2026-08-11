---
type: feature
nav_path: "Marketing → Blog → Category → Structure & lifecycle"
route_name: blog-categories
route_path: /admin/marketing-new/blog/category
aliases: ["Blog category lifecycle", "Blog category hierarchy", "Blog category delete", "Orphaned blog articles", "500 article cap", "Auto-create blog category on import", "Структура на блог категория"]
tags: [marketing, blog, content, categories, taxonomy]
plan_gates: ["blog_categories"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-blog-category]]. See the hub for the other aspects (list & modal, comment policy, SEO, API/plan/permissions).

# Blog Categories — Structure & lifecycle

## Purpose

This aspect covers the structural and lifecycle rules of a blog category: that categories are **flat** (no hierarchy), that each can hold at most **500 articles**, what happens to articles when a category is **deleted** (they survive as orphaned, not cascade-deleted), and how categories get **auto-created on CSV import**. These are the rules a merchant hits when planning a content taxonomy or cleaning one up.

## Where to find it

Sidebar → **Marketing** → **Blog** → **Category**. Deletion uses the **Delete** row action or **bulk-delete** on the list ([[blog-category-list]]); the cap and orphan behaviour surface when working with [[marketing-blog-articles]].

## What the merchant can do here

- Delete a single category (row action) or several (bulk-delete) from the list.
- Re-assign articles to a different category before deleting (via [[marketing-blog-articles]]).
- Create flat categories only — there is no "add child category" action.

## Settings & fields

There are no lifecycle-specific form fields; the relevant field is the article-side **Blog** (`blog_id`) FK that ties an article to its category. The article-count cap (500) and the orphan state (`blog_id = NULL`) are state, not editable fields. See [[blog-category-list]] for the category's own fields.

## Business rules

### Hierarchy: NONE — blog categories are flat

Blog categories are a flat collection — there is no parent / child relationship. To simulate nesting ("News > Industry News"), the merchant would create two flat categories and use naming conventions. The storefront does NOT render a tree menu — only a flat list of categories with their articles paginated below.

This is intentionally different from [[products-categories]] (which has a nested tree). Blog categories optimise for SEO simplicity (each is its own indexable page) rather than navigational depth.

### Category cap on articles: 500

A category cannot hold more than **500 articles**. Hitting this cap blocks new article creation with *"The blog can not have more than 500"*. The merchant must split into multiple categories. There is no global cap on the number of categories themselves (that's a plan limit — see [[blog-category-api-plan-permissions]]). The 500 cap is enforced at article-create time, counted from the articles attached to the category — it is not stored on the category record.

### Delete behaviour: orphaned articles (FK is SET NULL, not CASCADE)

The article-to-category foreign key (`blogs_articles.blog_id`) uses **`ON DELETE SET NULL`** at the database level. When a category is deleted, every article in the category survives but becomes "uncategorised" with `blog_id=NULL` and:

- Remains in the [[marketing-blog-articles]] list (filter "Has blog: No" shows them).
- Still renders at `/article/<slug>` if `active='yes'` — the storefront article page does NOT require a category to render.
- Fails the **"Blog is required"** validation if the merchant tries to edit it — so the merchant must pick a new category before saving any edits.

To cleanly delete a category, the workflow is: filter [[marketing-blog-articles]] by this category, bulk-reassign or delete the articles, then delete the empty category. Deletion is **not blocked** by attached articles, so a careless delete silently orphans content.

### Auto-create-on-import

When a CSV row from [[apps-blog-csv-import]] references a blog category by name and that name doesn't yet exist, the import auto-creates the category before attaching the article. New auto-created categories default to `comments=automatic` unless overridden — see [[blog-category-comment-policy]].

### Storefront URLs and visibility

The storefront URL for a category is `/blog/category/<url_handle>` (the handle field is on [[blog-category-seo]]). The page renders all articles in the category where `active='yes'`. The category itself is always visible — there is **no "active" flag on the category**, only on individual articles. An empty category renders with "no articles yet" (but is excluded from the sitemap until it has an active article — see [[blog-category-seo]]).

### Storage

Categories are stored flat in the per-store database (no `parent_id` column, no soft-deletes). Confirmed against the backend Blog (category) module.

## Related

- [[marketing-blog-category]] — hub.
- [[marketing-blog-articles]] — articles live inside categories; `blog_id` is a required FK that goes NULL on category delete.
- [[blog-article]] — the article entity (carries `blog_id`).
- [[products-categories]] — different concept (hierarchical product taxonomy).
- [[apps-blog-csv-import]] — can auto-create categories on import.
- [[blog-category-seo]] — storefront URL, sitemap inclusion, and the `url_handle` field.

## Open questions

No outstanding questions.
