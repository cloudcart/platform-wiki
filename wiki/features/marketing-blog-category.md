---
type: feature
nav_path: "Marketing → Blog → Category"
route_name: blog-categories
route_path: /admin/marketing-new/blog/category
aliases: ["Blog categories", "Blog category", "Blog sections", "Blogs", "Категории на блог", "Блог категории", "Блогове"]
tags: [marketing, blog, content, categories, taxonomy]
plan_gates: ["blog_categories"]
created: 2026-05-21
updated: 2026-06-10
source_count: 7
---
# Blog Categories

## Purpose

A **Blog Category** is the top-level container for blog articles — every article must belong to exactly one category (orphan articles are rejected with *"Blog is required"*). Categories give the storefront its blog navigation: the merchant might run separate categories for "News", "How-to guides", "Customer stories", and "Style tips", and each gets its own URL at `/blog/category/<slug>`. Each category has its own title, cover image, SEO meta, URL handle, and — critically — its own **comment policy** (off / moderated / automatic), which applies to every article inside it.

This page is **distinct from product categories** ([[products-categories]]) — different storefront namespace (`/blog/category/` vs `/category/`). Editing this page does not affect product categorisation.

## Sub-pages (in this cluster)

This feature is split into 5 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[blog-category-list]] — the list screen (columns, filters, bulk-delete) and the shared create/edit modal (Zod validation, title → slug, image card, two entry points).
- [[blog-category-comment-policy]] — the per-category `no` / `moderator` / `automatic` comment policy; how the switch + radio set it; how every article inherits it at submission time.
- [[blog-category-lifecycle]] — flat hierarchy (no parent/child), the 500-article cap, delete behaviour (FK `SET NULL` → orphaned articles), auto-create-on-import.
- [[blog-category-seo]] — SEO title / description fields, the SAVE-time name fallback, URL-handle auto-slug + 301 redirect on rename, cover-image rendering, sitemap inclusion.
- [[blog-category-api-plan-permissions]] — JSON-API v2 management via [[api-blogs]], the `blog_categories` plan gate, the `marketing.blog_categories` staff permission, cache flush, no-webhook behaviour.

## Where to find it

Sidebar → **Marketing** → **Blog** → **Category**.

Route name `blog-categories`; path `/admin/marketing-new/blog/category`. Header icon is the typewriter. There is no separate Add / Edit screen — both create and edit happen inside a modal opened from the list. The modal mechanics live on [[blog-category-list]].

## What the merchant can do here

- See and search a list of all blog categories; filter by **Comments** policy; **bulk-delete** — see [[blog-category-list]].
- **+ Add blog category** or click a row to open the shared create/edit modal — see [[blog-category-list]].
- Set the per-category **comment policy** (off / moderated / automatic) — see [[blog-category-comment-policy]].
- Upload a cover image, set SEO title / description, and override the URL handle — see [[blog-category-seo]].
- Manage categories programmatically via JSON-API v2 — see [[blog-category-api-plan-permissions]].

## Settings & fields

The full field table (Title, Comments, Cover image, URL handle, SEO title, SEO description), with validation and error strings, lives on [[blog-category-list]] (the form controls) and [[blog-category-seo]] (the SEO + URL-handle fields). The comment-policy enum (`no` / `moderator` / `automatic`) and its storefront effect are on [[blog-category-comment-policy]].

## Business rules

The non-obvious behaviours are distributed across the aspects:

- **Flat — no hierarchy**, the 500-article-per-category cap, and **delete → orphaned articles** (`ON DELETE SET NULL`) → [[blog-category-lifecycle]].
- **Comment policy is per-category, not per-article**, and is read at comment-submission time → [[blog-category-comment-policy]].
- **SEO fields fall back to the category name at SAVE time**, URL handle auto-slugs on create / locks on edit, renaming creates a 301 redirect, and the sitemap includes only categories with at least one active article → [[blog-category-seo]].
- **Plan cap (`blog_categories`), staff permission (`marketing.blog_categories`), cache flush, and the no-webhook rule** → [[blog-category-api-plan-permissions]].

## Plan gates

This feature is gated by the `blog_categories` plan-feature (Numeric + Access — per-plan category-count cap, counted against the Blog entity; lower plans cannot access the route at all). Full mapping, upsell behaviour, and feature-pack extension on [[blog-category-api-plan-permissions]]. See [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]].

## Related

- [[blog-category]] — the Blog Category entity page.
- [[blog-article]] — the Blog Article entity page.
- [[marketing-blog-articles]] — articles live inside categories; `blog_id` is a required FK.
- [[marketing-blog-comment]] — comment moderation; the policy comes from the article's parent category.
- [[marketing-blog-tags]] — orthogonal flat taxonomy; one article can have one category + many tags.
- [[products-categories]] — different concept (hierarchical product taxonomy); shares the word "category".
- [[marketing]] — parent hub.
- [[api-blogs]] — JSON-API v2 resource for managing blog categories.

## Open questions

No outstanding questions.
